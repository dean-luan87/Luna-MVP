# -*- coding: utf-8 -*-
"""Verify Field State Reducer controlled dryrun runner result v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.evaluation.midplatform.run_field_state_reducer_controlled_dryrun_v1 import (
    run_field_state_reducer_controlled_dryrun_v1,
)


def _to_map(case_results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {item.get("case_id", ""): item for item in case_results}


def verify_field_state_reducer_controlled_dryrun_result_v1() -> Dict[str, Any]:
    result = run_field_state_reducer_controlled_dryrun_v1()
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    case_results = result.get("case_results", [])
    by_case = _to_map(case_results)

    add("all_16_cases_executed", len(case_results) == 16)

    positive_ids = {
        "baseline_all_fixtures_case",
        "repeated_identical_input_case",
        "reversed_input_order_case",
        "single_event_case",
        "conflict_fixture_case",
        "overlay_fixture_case",
    }
    negative_ids = {
        "non_admitted_event_rejection_case",
        "raw_observation_rejection_case",
        "missing_temporal_snapshot_case",
        "missing_version_snapshot_case",
        "unstable_event_id_case",
        "direct_mutation_request_case",
        "provider_recall_request_case",
        "external_lookup_request_case",
        "action_trigger_request_case",
        "event_mutation_guard_case",
    }

    positive_ok = True
    for case_id in positive_ids:
        row = by_case.get(case_id, {})
        if not row:
            positive_ok = False
            continue
        if row.get("validation_passed") is not True:
            positive_ok = False
        if row.get("reduction_decision") != "skeleton_no_state_change":
            positive_ok = False
        if row.get("resulting_state") is not None:
            positive_ok = False
        boundary = row.get("boundary", {})
        if boundary.get("state_mutation_executed") is not False:
            positive_ok = False
        if boundary.get("runtime_execution") is not False:
            positive_ok = False
    add("positive_6_cases_placeholder_contract", positive_ok)

    expected_negative_error = {
        "non_admitted_event_rejection_case": "non_admitted_event_not_allowed",
        "raw_observation_rejection_case": "raw_observation_not_allowed",
        "missing_temporal_snapshot_case": "missing_temporal_snapshot",
        "missing_version_snapshot_case": "missing_version_snapshot",
        "unstable_event_id_case": "unstable_event_order",
        "direct_mutation_request_case": "direct_state_mutation_forbidden",
        "provider_recall_request_case": "provider_recall_forbidden",
        "external_lookup_request_case": "external_lookup_forbidden",
        "action_trigger_request_case": "action_trigger_forbidden",
        "event_mutation_guard_case": "non_admitted_event_not_allowed",
    }

    negative_ok = True
    for case_id in negative_ids:
        row = by_case.get(case_id, {})
        if not row:
            negative_ok = False
            continue
        if row.get("validation_passed") is not False:
            negative_ok = False
        if row.get("skeleton_called") is not False:
            negative_ok = False
        expected_code = expected_negative_error[case_id]
        actual_codes = row.get("structured_error_codes", [])
        if expected_code not in actual_codes:
            negative_ok = False
        boundary = row.get("boundary", {})
        if boundary.get("state_mutation_executed") is not False:
            negative_ok = False
        if boundary.get("runtime_execution") is not False:
            negative_ok = False
    add("negative_10_cases_rejected_with_expected_errors", negative_ok)

    add("no_unhandled_exceptions", result.get("unhandled_exceptions") == 0)
    add(
        "deterministic_comparison_passed",
        result.get("deterministic_comparison_passed") is True,
    )
    add(
        "fixture_immutability_passed", result.get("fixture_immutability_passed") is True
    )
    add("no_active_state_created", result.get("resulting_active_states_created") == 0)
    add("no_state_mutation_executed", result.get("state_mutations_executed") == 0)

    failed = [c for c in checks if not c["passed"]]
    return {
        "checks": checks,
        "passed_checks": sum(1 for c in checks if c["passed"]),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
    }


def main() -> int:
    report = verify_field_state_reducer_controlled_dryrun_result_v1()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("failed_checks") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
