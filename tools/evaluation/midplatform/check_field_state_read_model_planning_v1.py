#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


CHECKER = "check_field_state_read_model_planning_v1"
MODULE = "luna.field_state_read_model.planning_checker"


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

INVENTORY_DOC = Path(
    "docs/architecture/field_kernel/field_state_read_model_asset_inventory_v1.md"
)
PLAN_DOC = Path(
    "docs/architecture/field_kernel/field_state_read_model_technical_plan_v1.md"
)
TYPES_FILE = Path(
    "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_model_types_v1.py"
)
QUERY_SCHEMA = Path(
    "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_query_schema_v1.json"
)
RESULT_SCHEMA = Path(
    "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_result_schema_v1.json"
)


def _abs(path: Path) -> Path:
    return (WORKSPACE_ROOT / path).absolute()


def _exists(path: Path) -> bool:
    return _abs(path).exists()


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


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    required_assets = [INVENTORY_DOC, PLAN_DOC, TYPES_FILE, QUERY_SCHEMA, RESULT_SCHEMA]
    missing = [str(p) for p in required_assets if not _exists(p)]
    checks.append(
        _check(
            1,
            "planning assets exist",
            len(missing) == 0,
            "missing=" + ",".join(missing),
        )
    )

    inventory_text = _read_text(INVENTORY_DOC) if _exists(INVENTORY_DOC) else ""
    plan_text = _read_text(PLAN_DOC) if _exists(PLAN_DOC) else ""
    types_text = _read_text(TYPES_FILE) if _exists(TYPES_FILE) else ""
    query_schema = _read_json(QUERY_SCHEMA) if _exists(QUERY_SCHEMA) else {}
    result_schema = _read_json(RESULT_SCHEMA) if _exists(RESULT_SCHEMA) else {}

    inventory_sections_ok = all(
        heading in inventory_text
        for heading in (
            "## A. 现有正式主干",
            "## B. 可直接复用资产",
            "## C. 应扩展资产",
            "## D. Legacy / stub / duplicate assets",
            "## E. 真实缺口",
            "## F. 结构性 blocker",
            "## G. Dependency 与 ownership 边界",
        )
    )
    checks.append(_check(2, "inventory sections are complete", inventory_sections_ok))

    formal_mainline_ok = all(
        item in inventory_text
        for item in (
            "field_state_reducer/module/",
            "field_state_reducer_manifest_v1.json",
            "field_state_reducer_module_baseline_v1.json",
            "run_field_state_reducer_module_integration_v1.py",
        )
    )
    checks.append(_check(3, "formal mainline identified", formal_mainline_ok))

    reuse_extend_legacy_gap_blocker_ok = all(
        token in inventory_text
        for token in (
            "## B. 可直接复用资产",
            "## C. 应扩展资产",
            "## D. Legacy / stub / duplicate assets",
            "## E. 真实缺口",
            "## F. 结构性 blocker",
        )
    )
    checks.append(
        _check(
            4,
            "reuse/extend/legacy/gap/blocker are explicit",
            reuse_extend_legacy_gap_blocker_ok,
        )
    )

    mutation_authority_ok = (
        "Field State Reducer: only mutation authority" in inventory_text
        and "Reducer remains the only mutation authority" in plan_text
    )
    checks.append(
        _check(5, "mutation authority belongs to Reducer", mutation_authority_ok)
    )

    read_only_boundary_ok = all(
        token in plan_text
        for token in (
            "read-only state access",
            "state mutation.",
            "event reduction.",
            "fact admission.",
            "runtime loop ownership.",
        )
    )
    checks.append(
        _check(6, "Read Model read-only boundary is explicit", read_only_boundary_ok)
    )

    query_required = {
        "query_id",
        "requester_ref",
        "query_scope",
        "required_fields",
        "trace_ref",
        "replay_key",
    }
    result_required = {
        "query_id",
        "read_status",
        "projection",
        "state_version",
        "source_state_ref",
        "provenance_refs",
        "trace_ref",
        "replay_key",
        "boundary_flags",
    }
    io_contract_ok = query_required.issubset(
        set(query_schema.get("required_fields") or [])
    ) and result_required.issubset(set(result_schema.get("required_fields") or []))
    checks.append(
        _check(7, "input/output contract fields are complete", io_contract_ok)
    )

    status_set = {
        "read_ready",
        "partial_projection",
        "insufficient_state",
        "stale_state",
        "state_unavailable",
        "query_rejected",
    }
    status_ok = status_set.issubset(
        set(result_schema.get("read_status_registry") or [])
    )
    checks.append(_check(8, "status semantics are complete", status_ok))

    provenance_trace_version_replay_ok = all(
        token in plan_text
        for token in (
            "provenance/trace/version/replay",
            "trace_ref",
            "replay_key",
            "state_version",
        )
    )
    checks.append(
        _check(
            9,
            "provenance/trace/version/replay preserved",
            provenance_trace_version_replay_ok,
        )
    )

    combined_text = (inventory_text + "\n" + plan_text + "\n" + types_text).lower()
    has_no_runtime = ("no runtime loop" in combined_text) or (
        "runtime loop ownership" in combined_text
    )
    has_no_state_write = ("no state write" in combined_text) or (
        "state mutation" in combined_text
    )
    has_no_model_execution = ("no real model execution" in combined_text) or (
        "real model execution" in combined_text
    )
    no_runtime_ok = has_no_runtime and has_no_state_write and has_no_model_execution
    checks.append(
        _check(
            10,
            "no real runtime/state write/model execution in planning assets",
            no_runtime_ok,
        )
    )

    roadmap_ok = all(
        token in plan_text
        for token in (
            "Controlled Skeleton",
            "Contract DryRun",
            "Controlled Read Runtime",
            "Module Integration",
            "Promotion / Baseline",
        )
    )
    checks.append(_check(11, "implementation roadmap is clear", roadmap_ok))

    checker_source = _read_text(
        Path("tools/evaluation/midplatform/check_field_state_read_model_planning_v1.py")
    )
    checker_readonly_ok = not any(
        re.search(pattern, checker_source)
        for pattern in (
            r"\bsubprocess\b",
            r"\bos\.system\s*\(",
            r"\brun_.*\(",
            r"\bverify_.*\(",
        )
    )
    checks.append(
        _check(
            12, "checker is read-only and does not call runners", checker_readonly_ok
        )
    )

    passed_checks = sum(1 for c in checks if c["passed"])
    failed_items = [
        {"check_id": c["check_id"], "title": c["title"], "details": c["details"]}
        for c in checks
        if not c["passed"]
    ]
    failed_checks = len(failed_items)
    blocker_count = failed_checks

    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if failed_checks == 0
        else "BLOCKED_BY_PLANNING_INCONSISTENCY"
    )

    return {
        "module": MODULE,
        "checker": CHECKER,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "planning_ready": failed_checks == 0,
        "final_decision_candidate": final_decision_candidate,
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("failed_checks", 1) == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
