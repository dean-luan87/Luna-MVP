#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


MODULE = "luna.field_state_read_model"
VERIFIER = "verify_field_state_read_model_controlled_skeleton_v1"


def _is_workspace_root(candidate: Path) -> bool:
    return (
        (candidate / "AGENTS.md").exists()
        and (candidate / "capabilities").is_dir()
        and (candidate / "tools" / "evaluation" / "midplatform").is_dir()
    )


def _derive_workspace_root() -> Path:
    cwd = Path.cwd()
    if _is_workspace_root(cwd):
        return cwd.absolute()

    script_abs = Path(__file__).absolute()
    for candidate in (script_abs.parent, *script_abs.parents):
        if _is_workspace_root(candidate):
            return candidate.absolute()

    raise RuntimeError("Unable to determine workspace root")


WORKSPACE_ROOT = _derive_workspace_root()
MODULE_DIR = Path("capabilities/midplatform/core/field_state_read_model/module")
RUNNER_PATH = Path(
    "tools/evaluation/midplatform/run_field_state_read_model_controlled_skeleton_v1.py"
)
RUNNER_REPORT_PATH = Path(
    "_tmp_eval_out/field_state_read_model_controlled_skeleton_v1_smoke_v0/field_state_read_model_controlled_skeleton_v1.json"
)


def _abs(path: Path) -> Path:
    return (WORKSPACE_ROOT / path).absolute()


def _read_text(path: Path) -> str:
    return _abs(path).read_text(encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(_read_text(path))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "title": title,
        "passed": passed,
        "details": details,
    }


def _module_files() -> List[Path]:
    return [
        MODULE_DIR / "__init__.py",
        MODULE_DIR / "field_state_read_model_module_types_v1.py",
        MODULE_DIR / "field_state_read_model_query_validator_v1.py",
        MODULE_DIR / "field_state_read_model_projection_builder_v1.py",
        MODULE_DIR / "field_state_read_model_result_builder_v1.py",
        MODULE_DIR / "field_state_read_model_module_api_v1.py",
        RUNNER_PATH,
        RUNNER_REPORT_PATH,
    ]


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    missing = [str(path) for path in _module_files() if not _abs(path).exists()]
    checks.append(
        _check(
            1, "module files exist", len(missing) == 0, "missing=" + ",".join(missing)
        )
    )

    types_text = _read_text(MODULE_DIR / "field_state_read_model_module_types_v1.py")
    api_text = _read_text(MODULE_DIR / "field_state_read_model_module_api_v1.py")
    projection_text = _read_text(
        MODULE_DIR / "field_state_read_model_projection_builder_v1.py"
    )
    validator_text = _read_text(
        MODULE_DIR / "field_state_read_model_query_validator_v1.py"
    )
    result_text = _read_text(MODULE_DIR / "field_state_read_model_result_builder_v1.py")
    runner_text = _read_text(RUNNER_PATH)
    runner_result = _read_json(RUNNER_REPORT_PATH)

    status_ok = all(
        status in types_text
        for status in (
            "read_ready",
            "partial_projection",
            "insufficient_state",
            "stale_state",
            "state_unavailable",
            "query_rejected",
        )
    )
    checks.append(_check(2, "six read statuses exist", status_ok))

    reducer_import_absent = "field_state_reducer" not in (
        api_text + projection_text + validator_text + result_text
    )
    checks.append(_check(3, "reducer mutation API not imported", reducer_import_absent))

    no_state_write = not any(
        token in (api_text + projection_text + result_text)
        for token in ("write_text(", "write_bytes(", "open(", "state_store", "persist")
    )
    checks.append(_check(4, "no state write operation", no_state_write))

    no_store_connection = not any(
        token in (api_text + projection_text + result_text + runner_text)
        for token in ("sqlite", "redis", "postgres", "mysql", "mongodb", "connect(")
    )
    checks.append(_check(5, "no real state store connection", no_store_connection))

    no_model_execution = not any(
        token in (api_text + projection_text + result_text + runner_text)
        for token in (
            "torch",
            "transformers",
            "model_manager",
            "vision_manager",
            "gemini",
            "qwen",
        )
    )
    checks.append(_check(6, "no model execution import", no_model_execution))

    no_runtime_loop = "runtime_loop" in types_text and "while True" not in (
        api_text + runner_text
    )
    checks.append(_check(7, "no runtime loop", no_runtime_loop))

    input_contract_ok = all(
        field_name in types_text
        for field_name in (
            "query_id",
            "requester_ref",
            "query_scope",
            "field_state_ref",
            "snapshot_ref",
            "task_ref",
            "scene_ref",
            "object_ref",
            "temporal_scope",
            "required_fields",
            "trace_ref",
            "replay_key",
            "metadata",
        )
    )
    checks.append(_check(8, "input contract fields complete", input_contract_ok))

    output_contract_ok = all(
        field_name in types_text
        for field_name in (
            "query_id",
            "read_status",
            "projection",
            "state_version",
            "source_state_ref",
            "provenance_refs",
            "trace_ref",
            "replay_key",
            "stale_reason",
            "insufficiency_reason",
            "rejection_reason",
            "boundary_flags",
            "module_status",
            "runtime_executed",
        )
    )
    checks.append(_check(9, "output contract fields complete", output_contract_ok))

    runtime_false = "runtime_executed: bool = False" in types_text
    checks.append(_check(10, "runtime_executed=false", runtime_false))

    candidate_only_boundary = all(
        token in types_text
        for token in (
            '"read_only": True',
            '"candidate_only": True',
            '"state_mutation": False',
            '"event_reduction": False',
            '"fact_admission": False',
        )
    )
    checks.append(_check(11, "candidate_only boundary", candidate_only_boundary))

    preservation_ok = all(
        token in (types_text + projection_text + result_text)
        for token in (
            "provenance_refs",
            "trace_ref",
            "state_version",
            "replay_key",
        )
    )
    checks.append(
        _check(12, "provenance/trace/version/replay preserved", preservation_ok)
    )

    deterministic_projection = (
        "sorted(required_fields)" in projection_text and "random" not in projection_text
    )
    checks.append(_check(13, "deterministic projection", deterministic_projection))

    input_immutability = (
        'dict(state_candidate.get("state_payload") or {})' in projection_text
        and "dict(query)" not in api_text
    )
    checks.append(_check(14, "input immutability", input_immutability))

    scenario_count_ok = all(
        token in runner_text
        for token in (
            "full_projection_read_ready",
            "partial_projection",
            "insufficient_state",
            "stale_state",
            "state_unavailable",
            "invalid_query_missing_required_field",
            "invalid_query_no_state_reference",
            "provenance_trace_version_preserved",
            "input_immutability",
            "deterministic_replay",
        )
    )
    checks.append(_check(15, "runner scenario count >=10", scenario_count_ok))

    checks.append(
        _check(
            16,
            "runner passed_cases == total_cases",
            runner_result.get("passed_cases") == runner_result.get("total_cases"),
        )
    )
    checks.append(
        _check(17, "failed_cases=[]", runner_result.get("failed_cases") == [])
    )
    checks.append(
        _check(
            18, "unhandled_exceptions=0", runner_result.get("unhandled_exceptions") == 0
        )
    )

    passed_checks = sum(1 for check in checks if check["passed"])
    failed_items = [
        {
            "check_id": check["check_id"],
            "title": check["title"],
            "details": check["details"],
        }
        for check in checks
        if not check["passed"]
    ]
    failed_checks = len(failed_items)
    blocker_count = failed_checks
    boundary_preserved = bool(runner_result.get("boundary_preserved") is True)
    skeleton_ready = failed_checks == 0 and boundary_preserved
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if skeleton_ready
        else "BLOCKED_BY_CONTROLLED_SKELETON"
    )

    return {
        "module": MODULE,
        "verifier": VERIFIER,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "boundary_preserved": boundary_preserved,
        "skeleton_ready": skeleton_ready,
        "final_decision_candidate": final_decision_candidate,
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["skeleton_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
