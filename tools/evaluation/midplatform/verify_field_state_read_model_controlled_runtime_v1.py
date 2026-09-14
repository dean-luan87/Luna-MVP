#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODULE = "luna.field_state_read_model"
VERIFIER = "verify_field_state_read_model_controlled_runtime_v1"


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
RUNTIME_DIR = Path("capabilities/midplatform/core/field_state_read_model/runtime")
RUNNER_PATH = Path(
    "tools/evaluation/midplatform/run_field_state_read_model_controlled_runtime_v1.py"
)
RUNNER_REPORT_PATH = Path(
    "_tmp_eval_out/field_state_read_model_controlled_runtime_v1_smoke_v0/field_state_read_model_controlled_runtime_v1.json"
)
TYPES_PATH = RUNTIME_DIR / "field_state_read_model_runtime_types_v1.py"
ADAPTER_PATH = RUNTIME_DIR / "field_state_read_model_controlled_source_adapter_v1.py"
RUNTIME_PATH = RUNTIME_DIR / "field_state_read_model_controlled_runtime_v1.py"
ENVELOPE_PATH = RUNTIME_DIR / "field_state_read_model_runtime_envelope_builder_v1.py"


def _abs(path: Path) -> Path:
    return (WORKSPACE_ROOT / path).absolute()


def _read_text(path: Path) -> str:
    return _abs(path).read_text(encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(_read_text(path))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {"check_id": check_id, "title": title, "passed": passed, "details": details}


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    runtime_files = [
        RUNTIME_DIR / "__init__.py",
        TYPES_PATH,
        ADAPTER_PATH,
        ENVELOPE_PATH,
        RUNTIME_PATH,
        RUNNER_PATH,
        RUNNER_REPORT_PATH,
    ]
    checks.append(
        _check(
            1, "runtime files exist", all(_abs(path).exists() for path in runtime_files)
        )
    )

    types_text = _read_text(TYPES_PATH)
    adapter_text = _read_text(ADAPTER_PATH)
    runtime_text = _read_text(RUNTIME_PATH)
    envelope_text = _read_text(ENVELOPE_PATH)
    runner_text = _read_text(RUNNER_PATH)
    runner_report = _read_json(RUNNER_REPORT_PATH)

    checks.append(
        _check(
            2,
            "source adapter modes complete",
            all(
                token in types_text
                for token in (
                    "candidate_available",
                    "candidate_unavailable",
                    "candidate_malformed",
                    "source_rejected",
                )
            ),
        )
    )
    checks.append(
        _check(
            3,
            "five runtime statuses complete",
            all(
                token in types_text
                for token in (
                    "runtime_completed",
                    "runtime_partial",
                    "runtime_unavailable",
                    "runtime_rejected",
                    "runtime_error_contained",
                )
            ),
        )
    )
    checks.append(
        _check(
            4,
            "no reducer import",
            "field_state_reducer" not in (adapter_text + runtime_text + envelope_text),
        )
    )
    checks.append(
        _check(
            5,
            "no state write",
            not any(
                token in (adapter_text + runtime_text + envelope_text)
                for token in ("write_text(", "write_bytes(", "open(")
            ),
        )
    )
    checks.append(
        _check(
            6,
            "no external I/O",
            not any(
                token in (adapter_text + runtime_text + envelope_text)
                for token in ("requests", "urllib", "socket", "http://", "https://")
            ),
        )
    )
    checks.append(
        _check(
            7,
            "no real store connection",
            not any(
                token in (adapter_text + runtime_text + envelope_text)
                for token in (
                    "sqlite",
                    "redis",
                    "postgres",
                    "mysql",
                    "mongodb",
                    "connect(",
                )
            ),
        )
    )
    checks.append(
        _check(
            8,
            "no model import/execution",
            not any(
                token in (adapter_text + runtime_text + envelope_text)
                for token in (
                    "torch",
                    "transformers",
                    "gemini",
                    "qwen",
                    "model_manager",
                    "vision_manager",
                )
            ),
        )
    )
    checks.append(
        _check(
            9,
            "no runtime loop",
            "while True"
            not in (adapter_text + runtime_text + envelope_text + runner_text),
        )
    )
    checks.append(
        _check(
            10,
            "runtime request contract complete",
            all(
                token in types_text
                for token in (
                    "runtime_request_id",
                    "query",
                    "source_request",
                    "trace_ref",
                    "replay_key",
                    "metadata",
                )
            ),
        )
    )
    checks.append(
        _check(
            11,
            "runtime envelope contract complete",
            all(
                token in types_text
                for token in (
                    "runtime_status",
                    "source_status",
                    "read_status",
                    "read_result",
                    "runtime_attempted",
                    "read_api_invoked",
                    "external_io_executed",
                    "state_mutation_executed",
                    "runtime_loop_executed",
                    "candidate_only",
                    "boundary_flags",
                    "error_reason",
                )
            ),
        )
    )
    checks.append(
        _check(
            12,
            "scenario count >=24",
            int(runner_report.get("total_cases", 0)) >= 24,
            f"total_cases={runner_report.get('total_cases', 0)}",
        )
    )
    checks.append(
        _check(
            13,
            "all source modes covered",
            sorted(runner_report.get("source_modes_covered") or [])
            == [
                "candidate_available",
                "candidate_malformed",
                "candidate_unavailable",
                "source_rejected",
            ],
        )
    )
    checks.append(
        _check(
            14,
            "all runtime statuses covered",
            sorted(runner_report.get("runtime_statuses_covered") or [])
            == [
                "runtime_completed",
                "runtime_error_contained",
                "runtime_partial",
                "runtime_rejected",
                "runtime_unavailable",
            ],
        )
    )
    checks.append(
        _check(
            15,
            "deterministic replay true",
            bool(runner_report.get("runtime_deterministic") is True),
        )
    )
    checks.append(
        _check(
            16,
            "input immutability true",
            bool(runner_report.get("input_immutability_preserved") is True),
        )
    )
    checks.append(
        _check(
            17,
            "provenance preserved true",
            bool(runner_report.get("provenance_preserved") is True),
        )
    )
    checks.append(
        _check(
            18,
            "contract dryrun compatibility true",
            bool(runner_report.get("contract_dryrun_compatible") is True),
        )
    )
    checks.append(
        _check(
            19,
            "passed_cases=total_cases",
            runner_report.get("passed_cases") == runner_report.get("total_cases"),
        )
    )
    checks.append(
        _check(20, "failed_cases=[]", runner_report.get("failed_cases") == [])
    )
    checks.append(
        _check(
            21, "unhandled_exceptions=0", runner_report.get("unhandled_exceptions") == 0
        )
    )
    checks.append(
        _check(
            22,
            "boundary preserved",
            bool(runner_report.get("boundary_preserved") is True),
        )
    )
    checks.append(
        _check(
            23,
            "external_io_executed=false",
            bool(runner_report.get("external_io_executed") is False),
        )
    )
    checks.append(
        _check(
            24,
            "state_mutation_executed=false",
            bool(runner_report.get("state_mutation_executed") is False),
        )
    )
    checks.append(
        _check(
            25,
            "runtime_loop_executed=false",
            bool(runner_report.get("runtime_loop_executed") is False),
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
    boundary_preserved = bool(runner_report.get("boundary_preserved") is True)
    controlled_runtime_ready = failed_checks == 0 and boundary_preserved
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if controlled_runtime_ready
        else "BLOCKED_BY_CONTROLLED_RUNTIME"
    )

    return {
        "module": MODULE,
        "verifier": VERIFIER,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "boundary_preserved": boundary_preserved,
        "controlled_runtime_ready": controlled_runtime_ready,
        "final_decision_candidate": final_decision_candidate,
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["controlled_runtime_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
