#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


MODULE = "luna.field_state_read_model"
VERIFIER = "verify_field_state_read_model_contract_dryrun_v1"


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
FIXTURES_PATH = Path(
    "capabilities/midplatform/core/field_state_read_model/dryrun/field_state_read_model_contract_fixtures_v1.py"
)
MATRIX_PATH = Path(
    "capabilities/midplatform/core/field_state_read_model/dryrun/field_state_read_model_contract_matrix_v1.json"
)
RUNNER_REPORT_PATH = Path(
    "_tmp_eval_out/field_state_read_model_contract_dryrun_v1_smoke_v0/field_state_read_model_contract_dryrun_v1.json"
)
QUERY_SCHEMA_PATH = Path(
    "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_query_schema_v1.json"
)
RESULT_SCHEMA_PATH = Path(
    "capabilities/midplatform/core/field_state_read_model/planning/field_state_read_result_schema_v1.json"
)
MODULE_TYPES_PATH = Path(
    "capabilities/midplatform/core/field_state_read_model/module/field_state_read_model_module_types_v1.py"
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


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    checks.append(_check(1, "fixture file exists", _abs(FIXTURES_PATH).exists()))
    checks.append(_check(2, "contract matrix exists", _abs(MATRIX_PATH).exists()))

    matrix = _read_json(MATRIX_PATH)
    runner_report = _read_json(RUNNER_REPORT_PATH)
    query_schema = _read_json(QUERY_SCHEMA_PATH)
    result_schema = _read_json(RESULT_SCHEMA_PATH)
    module_types_text = _read_text(MODULE_TYPES_PATH)

    total_cases = int(runner_report.get("total_cases", 0))
    checks.append(
        _check(
            3, "scenario count >=45", total_cases >= 45, f"total_cases={total_cases}"
        )
    )

    statuses = set(result_schema.get("read_status_registry") or [])
    checks.append(
        _check(
            4,
            "six statuses covered",
            statuses
            == {
                "read_ready",
                "partial_projection",
                "insufficient_state",
                "stale_state",
                "state_unavailable",
                "query_rejected",
            },
        )
    )

    priority_cases = set(
        (matrix.get("scenario_categories") or {}).get("priority_conflicts", [])
    )
    runner_case_ids = {
        str(case.get("case_id")) for case in (runner_report.get("cases") or [])
    }
    checks.append(
        _check(
            5, "priority conflicts covered", priority_cases.issubset(runner_case_ids)
        )
    )

    invalid_query_cases = set(
        (matrix.get("scenario_categories") or {}).get("invalid_queries", [])
    )
    checks.append(
        _check(
            6,
            "invalid query cases covered",
            invalid_query_cases.issubset(runner_case_ids),
        )
    )

    invalid_state_cases = set(
        (matrix.get("scenario_categories") or {}).get("invalid_state_candidates", [])
    )
    checks.append(
        _check(
            7,
            "invalid state candidate cases covered",
            invalid_state_cases.issubset(runner_case_ids),
        )
    )

    unknown_field_case = next(
        case
        for case in (runner_report.get("cases") or [])
        if case.get("case_id") == "unknown_query_field"
    )
    checks.append(
        _check(
            8,
            "unknown field rejected",
            "unknown_fields_not_allowed"
            in str(unknown_field_case.get("rejection_reason") or ""),
        )
    )

    duplicate_case = next(
        case
        for case in (runner_report.get("cases") or [])
        if case.get("case_id") == "duplicate_required_fields"
    )
    checks.append(
        _check(
            9,
            "duplicate required fields rejected",
            "duplicate_required_fields"
            in str(duplicate_case.get("rejection_reason") or ""),
        )
    )

    input_required = set(query_schema.get("required_fields") or [])
    result_required = set(result_schema.get("required_fields") or [])
    schema_aligned = all(
        token in module_types_text for token in input_required | result_required
    )
    checks.append(_check(10, "schema/type fields aligned", schema_aligned))

    checks.append(
        _check(
            11,
            "deterministic serialization true",
            bool(runner_report.get("deterministic_serialization") is True),
        )
    )
    checks.append(
        _check(
            12,
            "deterministic replay true",
            bool(runner_report.get("deterministic_replay") is True),
        )
    )
    checks.append(
        _check(
            13,
            "query immutability true",
            bool(runner_report.get("input_immutability_preserved") is True),
        )
    )

    candidate_immutability = all(
        bool(case.get("state_candidate_immutability_preserved") is True)
        for case in (runner_report.get("cases") or [])
    )
    checks.append(_check(14, "candidate immutability true", candidate_immutability))

    checks.append(
        _check(
            15,
            "provenance preservation true",
            bool(runner_report.get("provenance_preserved") is True),
        )
    )
    checks.append(
        _check(
            16,
            "runtime_executed=false",
            bool(runner_report.get("runtime_executed") is False),
        )
    )
    checks.append(
        _check(
            17,
            "boundary preserved",
            bool(runner_report.get("boundary_preserved") is True),
        )
    )
    checks.append(
        _check(
            18,
            "passed_cases=total_cases",
            runner_report.get("passed_cases") == runner_report.get("total_cases"),
        )
    )
    checks.append(
        _check(19, "failed_cases=[]", runner_report.get("failed_cases") == [])
    )
    checks.append(
        _check(
            20, "unhandled_exceptions=0", runner_report.get("unhandled_exceptions") == 0
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
    skeleton_ready = failed_checks == 0 and boundary_preserved
    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if skeleton_ready
        else "BLOCKED_BY_CONTRACT_DRYRUN"
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
    return (
        0
        if report["final_decision_candidate"] == "READY_FOR_USER_TERMINAL_VERIFICATION"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
