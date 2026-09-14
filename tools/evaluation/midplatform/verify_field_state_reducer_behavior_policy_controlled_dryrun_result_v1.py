from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.evaluation.midplatform.run_field_state_reducer_behavior_policy_controlled_dryrun_v1 import (  # noqa: E402
    run_field_state_reducer_behavior_policy_controlled_dryrun_v1,
)


def verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1() -> Dict[
    str, Any
]:
    result = run_field_state_reducer_behavior_policy_controlled_dryrun_v1()
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    case_results = result.get("case_results", [])
    by_case = {row.get("case_id"): row for row in case_results}

    add("all_20_cases_executed", len(case_results) == 20)

    positive_ids = {
        "registry_loading_case",
        "baseline_placeholder_chain_case",
        "repeated_identical_input_case",
        "reversed_candidate_order_case",
        "conflict_preservation_candidate_case",
        "temporary_overlay_candidate_case",
        "owner_correction_candidate_case",
        "insufficient_evidence_no_state_change_case",
    }
    negative_ids = {
        "unknown_policy_id_rejection_case",
        "unknown_state_type_rejection_case",
        "missing_policy_registry_snapshot_case",
        "missing_eligibility_snapshot_case",
        "missing_precedence_snapshot_case",
        "missing_composition_snapshot_case",
        "runtime_request_rejection_case",
        "direct_state_write_rejection_case",
        "fact_promotion_rejection_case",
        "action_trigger_rejection_case",
        "provider_recall_rejection_case",
        "external_lookup_rejection_case",
    }

    positive_passed = 0
    for cid in positive_ids:
        row = by_case.get(cid, {})
        ok = (
            row.get("validation_passed") is True
            and row.get("skeleton_called") is True
            and row.get("resulting_state_candidate") is None
            and row.get("boundary", {}).get("policy_execution_executed") is False
            and row.get("boundary", {}).get("precedence_execution_executed") is False
            and row.get("boundary", {}).get("composition_execution_executed") is False
            and row.get("boundary", {}).get("confidence_aggregation_executed") is False
            and row.get("boundary", {}).get("conflict_resolution_executed") is False
            and row.get("boundary", {}).get("state_mutation_executed") is False
            and row.get("boundary", {}).get("fact_promotion_executed") is False
            and row.get("boundary", {}).get("action_trigger_executed") is False
            and row.get("boundary", {}).get("runtime_execution") is False
        )
        positive_passed += 1 if ok else 0
    add("positive_8_cases_passed", positive_passed == 8)

    negative_expected_codes = {
        "unknown_policy_id_rejection_case": "unknown_policy_id",
        "unknown_state_type_rejection_case": "unknown_state_type",
        "missing_policy_registry_snapshot_case": "missing_policy_registry_snapshot",
        "missing_eligibility_snapshot_case": "missing_eligibility_matrix_snapshot",
        "missing_precedence_snapshot_case": "missing_precedence_snapshot",
        "missing_composition_snapshot_case": "missing_composition_snapshot",
        "runtime_request_rejection_case": "runtime_execution_forbidden",
        "direct_state_write_rejection_case": "direct_state_write_forbidden",
        "fact_promotion_rejection_case": "fact_promotion_forbidden",
        "action_trigger_rejection_case": "action_trigger_forbidden",
        "provider_recall_rejection_case": "provider_recall_forbidden",
        "external_lookup_rejection_case": "external_lookup_forbidden",
    }

    negative_passed = 0
    for cid in negative_ids:
        row = by_case.get(cid, {})
        ok = (
            row.get("validation_passed") is False
            and row.get("skeleton_called") is False
            and row.get("structured_error_code") == negative_expected_codes[cid]
            and row.get("boundary", {}).get("state_mutation_executed") is False
            and row.get("boundary", {}).get("runtime_execution") is False
        )
        negative_passed += 1 if ok else 0
    add("negative_12_cases_rejected", negative_passed == 12)

    add("no_unhandled_exceptions", result.get("unhandled_exceptions") == 0)
    add(
        "deterministic_comparison_passed",
        result.get("deterministic_comparison", {}).get("passed") is True,
    )
    add(
        "reversed_candidate_order_passed",
        result.get("reversed_candidate_order_passed") is True,
    )
    add(
        "fixture_immutability_passed", result.get("fixture_immutability_passed") is True
    )
    add(
        "registry_immutability_passed",
        result.get("registry_immutability_passed") is True,
    )
    add("no_active_state_created", result.get("active_states_created") == 0)
    add("no_state_mutation_executed", result.get("state_mutations_executed") == 0)

    failed = [c for c in checks if not c["passed"]]
    report = {
        "checks": checks,
        "passed_checks": sum(1 for c in checks if c["passed"]),
        "failed_checks": len(failed),
        "blocker_count": len(failed),
        "positive_passed": positive_passed,
        "negative_passed": negative_passed,
        "unhandled_exceptions": result.get("unhandled_exceptions"),
        "deterministic_comparison_passed": result.get(
            "deterministic_comparison", {}
        ).get("passed"),
        "reversed_candidate_order_passed": result.get(
            "reversed_candidate_order_passed"
        ),
        "fixture_immutability_passed": result.get("fixture_immutability_passed"),
        "registry_immutability_passed": result.get("registry_immutability_passed"),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    output = verify_field_state_reducer_behavior_policy_controlled_dryrun_result_v1()
    raise SystemExit(0 if output.get("failed_checks") == 0 else 1)
