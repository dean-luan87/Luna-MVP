from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent

EXPECTED_FINAL_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_CONTROLLED_POLICY_EVALUATION_TECHNICAL_PLANNING_GO"
)
EXPECTED_NEXT = "Phase-Luna-Field-State-Reducer-Controlled-Policy-Evaluation-Controlled-Skeleton-Implementation-v1-001"
EXPECTED_FAILURE_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_CONTROLLED_POLICY_EVALUATION_TECHNICAL_PLANNING_BLOCKED"
)
EXPECTED_FAILURE_NEXT = (
    "REMEDIATE_FIELD_STATE_REDUCER_CONTROLLED_POLICY_EVALUATION_TECHNICAL_PLANNING"
)
EXPECTED_CHECK_COUNT = 68

REQUIRED_FILES = [
    "field_state_reducer_controlled_policy_evaluation_technical_plan_v1.md",
    "field_state_reducer_policy_evaluation_input_schema_v1.json",
    "field_state_reducer_policy_evaluation_status_registry_v1.json",
    "field_state_reducer_policy_evaluation_condition_type_registry_v1.json",
    "field_state_reducer_policy_evaluation_operator_registry_v1.json",
    "field_state_reducer_policy_evaluation_rule_schema_v1.json",
    "field_state_reducer_policy_evaluation_matrix_v1.json",
    "field_state_reducer_policy_evidence_sufficiency_contract_v1.json",
    "field_state_reducer_policy_temporal_evaluation_contract_v1.json",
    "field_state_reducer_policy_confidence_evaluation_contract_v1.json",
    "field_state_reducer_policy_conflict_evaluation_contract_v1.json",
    "field_state_reducer_policy_governance_evaluation_contract_v1.json",
    "field_state_reducer_policy_evaluation_result_schema_v1.json",
    "field_state_reducer_policy_evaluation_trace_schema_v1.json",
    "field_state_reducer_policy_evaluation_replay_contract_v1.json",
    "field_state_reducer_policy_evaluation_rejection_reason_registry_v1.json",
    "field_state_reducer_policy_evaluation_minimum_cases_v1.json",
    "field_state_reducer_policy_evaluation_test_strategy_v1.json",
    "field_state_reducer_policy_evaluation_negative_guards_v1.json",
    "field_state_reducer_policy_evaluation_summary_v1.json",
    "verify_field_state_reducer_controlled_policy_evaluation_technical_planning_v1.py",
]

EXPECTED_POLICY_IDS = {
    "latest_valid_event",
    "highest_confidence_valid_event",
    "multi_event_consensus",
    "negative_event_override",
    "revocation_override",
    "expiration_degrade",
    "conflict_preservation",
    "insufficient_evidence_unresolved",
    "explicit_owner_override_candidate",
    "temporary_overlay_separation",
    "no_state_change",
}

EXPECTED_STATE_TYPES = {
    "presence_state",
    "accessibility_state",
    "path_state",
    "obstruction_state",
    "facility_state",
    "service_state",
    "environmental_condition_state",
    "human_activity_state",
    "navigation_relevance_state",
    "temporary_overlay_state",
    "uncertainty_state",
    "conflict_state",
}


def _load_json(name: str) -> Dict[str, Any]:
    with open(BASE_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [name for name in REQUIRED_FILES if not (BASE_DIR / name).exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        ";".join(missing) if missing else "ok",
    )

    json_files = [name for name in REQUIRED_FILES if name.endswith(".json")]
    invalid_json: List[str] = []
    for name in json_files:
        try:
            _load_json(name)
        except Exception as exc:
            invalid_json.append(f"{name}:{exc}")
    add(
        "all_json_valid",
        len(invalid_json) == 0,
        ";".join(invalid_json) if invalid_json else "ok",
    )

    input_schema = _load_json(
        "field_state_reducer_policy_evaluation_input_schema_v1.json"
    )
    status_registry = _load_json(
        "field_state_reducer_policy_evaluation_status_registry_v1.json"
    )
    condition_registry = _load_json(
        "field_state_reducer_policy_evaluation_condition_type_registry_v1.json"
    )
    operator_registry = _load_json(
        "field_state_reducer_policy_evaluation_operator_registry_v1.json"
    )
    rule_schema = _load_json(
        "field_state_reducer_policy_evaluation_rule_schema_v1.json"
    )
    eval_matrix = _load_json("field_state_reducer_policy_evaluation_matrix_v1.json")
    evidence_contract = _load_json(
        "field_state_reducer_policy_evidence_sufficiency_contract_v1.json"
    )
    temporal_contract = _load_json(
        "field_state_reducer_policy_temporal_evaluation_contract_v1.json"
    )
    confidence_contract = _load_json(
        "field_state_reducer_policy_confidence_evaluation_contract_v1.json"
    )
    conflict_contract = _load_json(
        "field_state_reducer_policy_conflict_evaluation_contract_v1.json"
    )
    governance_contract = _load_json(
        "field_state_reducer_policy_governance_evaluation_contract_v1.json"
    )
    result_schema = _load_json(
        "field_state_reducer_policy_evaluation_result_schema_v1.json"
    )
    trace_schema = _load_json(
        "field_state_reducer_policy_evaluation_trace_schema_v1.json"
    )
    replay_contract = _load_json(
        "field_state_reducer_policy_evaluation_replay_contract_v1.json"
    )
    rejection_registry = _load_json(
        "field_state_reducer_policy_evaluation_rejection_reason_registry_v1.json"
    )
    minimum_cases = _load_json(
        "field_state_reducer_policy_evaluation_minimum_cases_v1.json"
    )
    test_strategy = _load_json(
        "field_state_reducer_policy_evaluation_test_strategy_v1.json"
    )
    negative_guards = _load_json(
        "field_state_reducer_policy_evaluation_negative_guards_v1.json"
    )
    summary = _load_json("field_state_reducer_policy_evaluation_summary_v1.json")

    statuses = list(status_registry.get("statuses", []))
    condition_types = list(condition_registry.get("condition_types", []))
    operators = list(operator_registry.get("operators", []))
    policies = list(eval_matrix.get("policies", []))
    temporal_statuses = dict(temporal_contract.get("temporal_statuses", {}))
    confidence_rows = list(confidence_contract.get("state_type_contracts", []))
    conflict_types = list(conflict_contract.get("conflict_types", []))
    rejection_reasons = list(rejection_registry.get("rejection_reasons", []))
    cases = list(minimum_cases.get("cases", []))

    add("evaluation_statuses_complete_10", len(statuses) == 10)
    add("condition_types_complete_18", len(condition_types) == 18)
    add("operators_complete_15", len(operators) == 15)
    add(
        "all_operators_implemented_false",
        all(o.get("implemented") is False for o in operators),
    )
    add(
        "all_operators_runtime_callable_false",
        all(o.get("runtime_callable") is False for o in operators),
    )

    required_input_fields = {
        "evaluation_id",
        "reducer_run_id",
        "field_id",
        "state_type",
        "policy_id",
        "admitted_events",
        "existing_state_snapshot",
        "temporal_snapshot",
        "confidence_policy_snapshot",
        "conflict_snapshot",
        "owner_correction_snapshot",
        "overlay_snapshot",
        "provenance_snapshot",
        "policy_registry_version",
        "eligibility_matrix_version",
        "evaluation_contract_version",
        "evaluation_requested_at",
    }
    add(
        "input_schema_complete",
        required_input_fields.issubset(set(input_schema.get("required_fields", []))),
    )
    add(
        "input_runtime_dependency_false",
        input_schema.get("runtime_state_dependency_requested") is False,
    )
    add(
        "input_provider_recall_false",
        input_schema.get("provider_recall_requested") is False,
    )
    add(
        "input_external_lookup_false",
        input_schema.get("external_lookup_requested") is False,
    )
    add("input_model_call_false", input_schema.get("model_call_requested") is False)
    add("input_state_write_false", input_schema.get("state_write_requested") is False)
    add(
        "input_action_trigger_false",
        input_schema.get("action_trigger_requested") is False,
    )

    required_rule_fields = {
        "rule_id",
        "policy_id",
        "condition_type",
        "operator",
        "expected_value",
        "input_path",
        "required",
        "blocking",
        "rejection_reason",
        "evaluation_order",
        "short_circuit_allowed",
        "trace_required",
        "candidate_only",
        "fact_promotion_allowed",
    }
    add(
        "rule_schema_complete",
        required_rule_fields.issubset(set(rule_schema.get("required_fields", []))),
    )

    add("evaluation_matrix_policy_count_11", len(policies) == 11)
    add(
        "evaluation_matrix_policy_ids_exact",
        {p.get("policy_id") for p in policies} == EXPECTED_POLICY_IDS,
    )
    add(
        "all_evaluation_rows_candidate_only",
        all(p.get("candidate_only") is True for p in policies),
    )
    add(
        "all_evaluation_rows_selection_executed_false",
        all(p.get("selection_executed") is False for p in policies),
    )

    add(
        "evidence_sufficiency_contract_complete",
        evidence_contract.get("evidence_sufficiency_contract_complete") is True,
    )
    add(
        "no_evidence_fabrication_true",
        evidence_contract.get("no_evidence_fabrication") is True,
    )
    add(
        "insufficient_evidence_safe_fallback",
        evidence_contract.get("insufficient_evidence_default")
        == "unresolved_or_no_state_change",
    )

    add("temporal_statuses_complete_8", len(temporal_statuses) == 8)
    add(
        "expired_support_ineligible",
        temporal_statuses.get("expired", {}).get("support_eligible") is False,
    )
    add(
        "revoked_support_ineligible",
        temporal_statuses.get("revoked", {}).get("support_eligible") is False,
    )
    add(
        "suspended_refresh_required",
        temporal_statuses.get("suspended", {}).get("refresh_required") is True,
    )
    add(
        "unknown_not_auto_eligible",
        temporal_statuses.get("unknown", {}).get("support_eligible") is False,
    )

    confidence_state_types = {row.get("state_type") for row in confidence_rows}
    add(
        "confidence_state_types_complete_12",
        confidence_state_types == EXPECTED_STATE_TYPES,
    )
    add(
        "confidence_no_simple_average_all_true",
        all(row.get("no_simple_average_default") is True for row in confidence_rows),
    )
    add(
        "confidence_no_automatic_100_all_true",
        all(row.get("no_automatic_100") is True for row in confidence_rows),
    )
    add(
        "confidence_fabricated_false",
        all(
            row.get("fabricated_confidence_allowed") is False for row in confidence_rows
        ),
    )
    add(
        "confidence_calculation_implemented_false",
        all(row.get("calculation_implemented") is False for row in confidence_rows),
    )

    add("conflict_types_at_least_10", len(conflict_types) >= 10)
    add(
        "unresolved_conflict_preserved",
        all(
            c.get("evaluation_status_when_unresolved")
            in {"unresolved_conflict", "governance_review_required", "blocked"}
            and c.get("preserve_conflict") is True
            for c in conflict_types
        ),
    )
    add(
        "conflict_winner_fabrication_false",
        all(c.get("winner_fabrication_allowed") is False for c in conflict_types),
    )

    deps = {
        d.get("dependency_id")
        for d in governance_contract.get("governance_dependencies", [])
    }
    add(
        "governance_contract_complete",
        governance_contract.get("governance_contract_complete") is True
        and {
            "owner_correction_review",
            "fact_admission_dependency",
            "permission_admission_dependency",
            "human_review_dependency",
            "protocol_version_dependency",
            "provenance_dependency",
            "change_control_dependency",
            "runtime_boundary_dependency",
        }.issubset(deps),
    )
    add(
        "evaluation_no_fact_admission_authority",
        governance_contract.get("evaluation_has_fact_admission_authority") is False,
    )
    add(
        "evaluation_no_state_write_authority",
        governance_contract.get("evaluation_has_direct_state_write_authority") is False,
    )
    add(
        "evaluation_no_action_trigger_authority",
        governance_contract.get("evaluation_has_action_trigger_authority") is False,
    )
    add(
        "owner_correction_candidate_only",
        governance_contract.get("owner_correction_candidate_only") is True,
    )

    result_fields = {
        "evaluation_id",
        "policy_id",
        "state_type",
        "evaluation_status",
        "satisfied_rule_ids",
        "unsatisfied_rule_ids",
        "blocked_rule_ids",
        "skipped_rule_ids",
        "missing_input_fields",
        "evidence_sufficiency_status",
        "temporal_evaluation_status",
        "confidence_evaluation_status",
        "conflict_evaluation_status",
        "governance_evaluation_status",
        "rejection_reasons",
        "selection_candidate_allowed",
        "evaluation_trace_ref",
        "replay_key",
        "evaluated_contract_versions",
    }
    add(
        "result_schema_complete",
        result_fields.issubset(set(result_schema.get("required_fields", []))),
    )
    add(
        "result_policy_selection_false",
        result_schema.get("policy_selection_executed") is False,
    )
    add(
        "result_policy_execution_false",
        result_schema.get("policy_execution_executed") is False,
    )
    add(
        "result_state_mutation_false",
        result_schema.get("state_mutation_executed") is False,
    )
    add(
        "result_fact_promotion_false",
        result_schema.get("fact_promotion_executed") is False,
    )
    add(
        "result_action_trigger_false",
        result_schema.get("action_trigger_executed") is False,
    )
    add("result_runtime_false", result_schema.get("runtime_execution") is False)

    trace_fields = {
        "trace_id",
        "evaluation_id",
        "policy_id",
        "ordered_rule_ids",
        "evaluated_rule_ids",
        "rule_results",
        "short_circuit_steps",
        "evidence_refs",
        "temporal_refs",
        "confidence_refs",
        "conflict_refs",
        "governance_refs",
        "rejection_reason_refs",
        "snapshot_versions",
        "replay_key",
        "created_at",
    }
    add(
        "trace_schema_complete",
        trace_fields.issubset(set(trace_schema.get("required_fields", []))),
    )

    add(
        "replay_contract_complete",
        replay_contract.get("replay_contract_complete") is True,
    )
    add(
        "replay_runtime_dependency_false",
        replay_contract.get("current_runtime_state_dependency_allowed") is False,
    )
    add(
        "replay_provider_false",
        replay_contract.get("provider_recall_during_replay_allowed") is False,
    )
    add(
        "replay_external_lookup_false",
        replay_contract.get("external_lookup_during_replay_allowed") is False,
    )
    add(
        "replay_model_false",
        replay_contract.get("model_call_during_replay_allowed") is False,
    )
    add(
        "replay_version_fallback_false",
        replay_contract.get("policy_version_fallback_allowed") is False,
    )

    add("rejection_reasons_at_least_20", len(rejection_reasons) >= 20)

    required_case_ids = {
        "latest_valid_event_eligible_case",
        "latest_valid_event_revoked_block_case",
        "highest_confidence_threshold_pass_case",
        "highest_confidence_threshold_fail_case",
        "consensus_source_diversity_pass_case",
        "consensus_contradiction_block_case",
        "expired_support_ineligible_case",
        "suspended_missing_refresh_case",
        "revoked_support_ineligible_case",
        "unresolved_conflict_case",
        "insufficient_evidence_case",
        "owner_correction_review_required_case",
        "overlay_separate_evaluation_case",
        "missing_version_snapshot_case",
    }
    add(
        "minimum_cases_complete_14",
        len(cases) == 14 and {c.get("case_id") for c in cases} == required_case_ids,
    )
    add(
        "minimum_cases_no_selection",
        all(c.get("policy_selection_executed") is False for c in cases),
    )
    add(
        "minimum_cases_no_execution",
        all(c.get("policy_execution_executed") is False for c in cases),
    )
    add(
        "minimum_cases_no_mutation",
        all(c.get("state_mutation_executed") is False for c in cases),
    )

    strategy_checks = set(test_strategy.get("checks", []))
    required_strategy = {
        "Required Files",
        "JSON Validation",
        "Status Registry",
        "Condition Registry",
        "Operator Registry",
        "Evaluation Matrix 11 Policies",
        "Evidence Sufficiency",
        "Temporal Status 8",
        "Confidence Contract 12 State Types",
        "Conflict Contract",
        "Governance Boundary",
        "Result Schema",
        "Trace Schema",
        "Replay Snapshot",
        "Rejection Reason Registry",
        "Minimum Cases",
        "Evaluation not Selection",
        "No Policy Execution",
        "No State Mutation",
        "No Fact Promotion",
        "No Action Trigger",
        "No Provider",
        "No External Lookup",
        "No Model",
        "No Runtime",
        "No Production Execution",
    }
    add("test_strategy_complete", required_strategy.issubset(strategy_checks))

    guards = negative_guards.get("guards", {})
    required_guards = {
        "no_evaluation_engine_implementation",
        "no_real_condition_execution",
        "no_real_policy_eligibility_execution",
        "no_policy_selection",
        "no_policy_execution",
        "no_precedence_execution",
        "no_composition_execution",
        "no_confidence_calculation",
        "no_conflict_resolution",
        "no_owner_correction_fact_promotion",
        "no_overlay_substrate_mutation",
        "no_state_mutation",
        "no_fact_promotion",
        "no_action_trigger",
        "no_provider_recall",
        "no_external_lookup",
        "no_model_call",
        "no_database",
        "no_scheduler",
        "no_message_queue",
        "no_event_consumer",
        "no_runtime_loop",
        "no_training",
        "no_migration",
        "no_production_execution",
        "no_previous_phase_semantic_rewrite",
        "no_physical_delete",
    }
    add("negative_guards_complete", required_guards.issubset(set(guards.keys())))

    add(
        "summary_counts_exact",
        summary.get("policy_count") == 11
        and summary.get("state_type_count") == 12
        and summary.get("evaluation_status_count") == 10
        and summary.get("condition_type_count") == 18
        and summary.get("operator_count") == 15
        and summary.get("minimum_case_count") == 14,
    )
    add("planning_only_true", summary.get("planning_only") is True)
    add(
        "evaluation_engine_implemented_false",
        summary.get("evaluation_engine_implemented") is False,
    )
    add(
        "no_runtime_or_production",
        summary.get("runtime_implemented") is False
        and summary.get("runtime_executed") is False
        and summary.get("production_execution") is False,
    )
    add("blocker_count_zero", summary.get("blocker_count") == 0)
    add(
        "final_decision_exact_match",
        summary.get("final_decision") == EXPECTED_FINAL_DECISION,
    )
    add("next_exact_match", summary.get("recommended_next_phase") == EXPECTED_NEXT)

    failed = [c for c in checks if not c["passed"]]
    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(failed)
    blocker_count = failed_count

    if len(checks) != EXPECTED_CHECK_COUNT:
        failed_count += 1
        blocker_count += 1
        failed.append(
            {
                "name": "expected_check_count_exact_68",
                "passed": False,
                "detail": f"actual={len(checks)} expected={EXPECTED_CHECK_COUNT}",
            }
        )

    final_decision = (
        EXPECTED_FINAL_DECISION if blocker_count == 0 else EXPECTED_FAILURE_DECISION
    )
    next_value = EXPECTED_NEXT if blocker_count == 0 else EXPECTED_FAILURE_NEXT

    print("CHECKS")
    for c in checks:
        print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
    if len(checks) != EXPECTED_CHECK_COUNT:
        print("- [FAIL] expected_check_count_exact_68")

    print("FAILED_CHECKS")
    if failed:
        for c in failed:
            print(
                f"- {c['name']}: {c['detail'] if c['detail'] else 'condition_not_met'}"
            )
    else:
        print("- NONE")

    print("PASSED_CHECK_COUNT")
    print(passed_count)
    print("FAILED_CHECK_COUNT")
    print(failed_count)
    print("BLOCKER_COUNT")
    print(blocker_count)
    print("FINAL_DECISION")
    print(final_decision)
    print("NEXT")
    print(next_value)

    return 0 if blocker_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
