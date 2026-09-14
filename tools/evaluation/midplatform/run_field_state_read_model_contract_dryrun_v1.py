#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).absolute().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

REPORT_PATH = (
    REPO_ROOT
    / "_tmp_eval_out"
    / "field_state_read_model_contract_dryrun_v1_smoke_v0"
    / "field_state_read_model_contract_dryrun_v1.json"
)
MATRIX_PATH = (
    REPO_ROOT
    / "capabilities/midplatform/core/field_state_read_model/dryrun/field_state_read_model_contract_matrix_v1.json"
)

from capabilities.midplatform.core.field_state_read_model.dryrun import (  # noqa: E402
    build_contract_fixtures_v1,
)
from capabilities.midplatform.core.field_state_read_model.module import (  # noqa: E402
    get_default_boundary_flags_v1,
    read_field_state,
)


EXPECTED_BOUNDARY_FLAGS = get_default_boundary_flags_v1()
ALLOWED_FINAL_DECISIONS = {
    "READY_FOR_USER_TERMINAL_VERIFICATION",
    "BLOCKED_BY_CONTRACT_DRYRUN",
}


def _result_to_dict(result: Any) -> Dict[str, Any]:
    return asdict(result)


def _stable_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _run_case(fixture: Dict[str, Any]) -> Dict[str, Any]:
    case_id = str(fixture["case_id"])
    query = copy.deepcopy(fixture["query"])
    state_candidate = copy.deepcopy(fixture["state_candidate"])
    original_query = copy.deepcopy(query)
    original_state = copy.deepcopy(state_candidate)

    result = _result_to_dict(read_field_state(query, state_candidate))

    passed_checks: List[bool] = []
    passed_checks.append(result.get("read_status") == fixture["expected_status"])
    passed_checks.append(result.get("runtime_executed") is False)
    passed_checks.append(
        dict(result.get("boundary_flags") or {}) == EXPECTED_BOUNDARY_FLAGS
    )
    passed_checks.append(query == original_query)
    passed_checks.append(state_candidate == original_state)

    rejection_reason = str(result.get("rejection_reason") or "")
    for token in fixture.get("expected_rejection_contains", []):
        passed_checks.append(token in rejection_reason)

    projection = dict(result.get("projection") or {})
    projection_keys = tuple(key for key in projection.keys() if key != "missing_fields")
    expected_projection_keys = tuple(fixture.get("expected_projection_keys", []))
    if expected_projection_keys:
        passed_checks.append(projection_keys == expected_projection_keys)

    expected_missing_fields = list(fixture.get("expected_missing_fields", []))
    if expected_missing_fields or "missing_fields" in projection:
        passed_checks.append(
            list(projection.get("missing_fields", [])) == expected_missing_fields
        )

    expected_provenance_refs = list(fixture.get("expected_provenance_refs", []))
    if expected_provenance_refs:
        passed_checks.append(
            list(result.get("provenance_refs") or []) == expected_provenance_refs
        )

    if case_id == "stable_json_serialization":
        second = _result_to_dict(
            read_field_state(copy.deepcopy(query), copy.deepcopy(state_candidate))
        )
        passed_checks.append(_stable_json(result) == _stable_json(second))

    if case_id == "deterministic_replay":
        second = _result_to_dict(
            read_field_state(copy.deepcopy(query), copy.deepcopy(state_candidate))
        )
        passed_checks.append(_stable_json(result) == _stable_json(second))

    if case_id == "boundary_flags_constant":
        passed_checks.append(
            dict(result.get("boundary_flags") or {}) == EXPECTED_BOUNDARY_FLAGS
        )

    if case_id == "runtime_executed_false":
        passed_checks.append(result.get("runtime_executed") is False)

    if case_id == "candidate_only_true":
        passed_checks.append(
            bool((result.get("boundary_flags") or {}).get("candidate_only") is True)
        )

    return {
        "case_id": case_id,
        "expected_status": fixture["expected_status"],
        "read_status": result.get("read_status"),
        "module_status": result.get("module_status"),
        "passed": all(passed_checks),
        "query_input_immutability_preserved": query == original_query,
        "state_candidate_immutability_preserved": state_candidate == original_state,
        "boundary_preserved": dict(result.get("boundary_flags") or {})
        == EXPECTED_BOUNDARY_FLAGS,
        "runtime_executed": result.get("runtime_executed"),
        "provenance_refs": result.get("provenance_refs"),
        "trace_ref": result.get("trace_ref"),
        "replay_key": result.get("replay_key"),
        "state_version": result.get("state_version"),
        "source_state_ref": result.get("source_state_ref"),
        "rejection_reason": rejection_reason,
        "projection": projection,
        "stable_json": _stable_json(result),
    }


def run() -> Dict[str, Any]:
    fixtures = build_contract_fixtures_v1()
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    rows = [_run_case(fixture) for fixture in fixtures]

    matrix_ids = []
    for ids in (matrix.get("scenario_categories") or {}).values():
        matrix_ids.extend(ids)
    matrix_ids = list(matrix_ids)
    report_ids = [row["case_id"] for row in rows]

    failed_cases = [row["case_id"] for row in rows if not row["passed"]]
    total_cases = len(rows)
    passed_cases = total_cases - len(failed_cases)
    contract_matrix_complete = (
        len(matrix_ids) == int(matrix.get("expected_total_cases") or 0)
        and len(report_ids) == len(matrix_ids)
        and sorted(report_ids) == sorted(matrix_ids)
    )

    priority_expectations = {
        "invalid_query_overrides_unavailable": "query_rejected",
        "unavailable_overrides_stale": "state_unavailable",
        "stale_overrides_insufficient": "stale_state",
        "insufficient_overrides_partial": "insufficient_state",
        "partial_overrides_ready": "partial_projection",
    }
    status_priority_preserved = all(
        next(row for row in rows if row["case_id"] == case_id)["read_status"]
        == expected
        for case_id, expected in priority_expectations.items()
    )

    invalid_query_case_ids = set(
        matrix.get("scenario_categories", {}).get("invalid_queries", [])
    )
    invalid_state_case_ids = set(
        matrix.get("scenario_categories", {}).get("invalid_state_candidates", [])
    )
    legal_read_case_ids = set(
        matrix.get("scenario_categories", {}).get("legal_reads", [])
    )

    schema_type_consistent = all(
        row["read_status"] in tuple(matrix.get("priority_order") or []) for row in rows
    )
    deterministic_serialization = next(
        row for row in rows if row["case_id"] == "stable_json_serialization"
    )["passed"]
    deterministic_replay = next(
        row for row in rows if row["case_id"] == "deterministic_replay"
    )["passed"]
    input_immutability_preserved = all(
        row["query_input_immutability_preserved"] for row in rows
    )
    boundary_preserved = all(row["boundary_preserved"] for row in rows)
    unhandled_exceptions = 0

    provenance_preserved = next(
        row for row in rows if row["case_id"] == "stable_provenance_order"
    )
    provenance_preserved = list(provenance_preserved["provenance_refs"] or []) == [
        "prov_b",
        "prov_a",
        "prov_c",
    ]

    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if not failed_cases
        and contract_matrix_complete
        and status_priority_preserved
        and schema_type_consistent
        and deterministic_serialization
        and deterministic_replay
        and input_immutability_preserved
        and boundary_preserved
        and provenance_preserved
        else "BLOCKED_BY_CONTRACT_DRYRUN"
    )
    if final_decision_candidate not in ALLOWED_FINAL_DECISIONS:
        final_decision_candidate = "BLOCKED_BY_CONTRACT_DRYRUN"

    report = {
        "module": "luna.field_state_read_model",
        "runner": "run_field_state_read_model_contract_dryrun_v1",
        "dryrun_only": True,
        "runtime_executed": False,
        "total_cases": total_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "contract_matrix_complete": contract_matrix_complete,
        "status_priority_preserved": status_priority_preserved,
        "schema_type_consistent": schema_type_consistent,
        "deterministic_serialization": deterministic_serialization,
        "deterministic_replay": deterministic_replay,
        "input_immutability_preserved": input_immutability_preserved,
        "boundary_preserved": boundary_preserved,
        "unhandled_exceptions": unhandled_exceptions,
        "provenance_preserved": provenance_preserved,
        "cases": rows,
        "final_decision_candidate": final_decision_candidate,
        "coverage": {
            "legal_reads": len(legal_read_case_ids),
            "priority_conflicts": len(priority_expectations),
            "invalid_queries": len(invalid_query_case_ids),
            "invalid_state_candidates": len(invalid_state_case_ids),
        },
    }
    return report


def main() -> int:
    report = run()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return (
        0
        if report["final_decision_candidate"] == "READY_FOR_USER_TERMINAL_VERIFICATION"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
