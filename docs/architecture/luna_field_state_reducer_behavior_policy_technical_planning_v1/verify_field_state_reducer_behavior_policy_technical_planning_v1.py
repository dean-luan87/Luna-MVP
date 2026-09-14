from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "field_state_reducer_behavior_policy_technical_plan_v1.md",
    "field_state_reducer_behavior_policy_registry_v1.json",
    "field_state_reducer_policy_eligibility_matrix_v1.json",
    "field_state_reducer_state_type_policy_mapping_v1.json",
    "field_state_reducer_policy_precedence_matrix_v1.json",
    "field_state_reducer_policy_composition_contract_v1.json",
    "field_state_reducer_temporal_policy_matrix_v1.json",
    "field_state_reducer_confidence_policy_matrix_v1.json",
    "field_state_reducer_conflict_policy_matrix_v1.json",
    "field_state_reducer_owner_correction_policy_v1.json",
    "field_state_reducer_overlay_policy_v1.json",
    "field_state_reducer_policy_decision_schema_v1.json",
    "field_state_reducer_policy_replay_contract_v1.json",
    "field_state_reducer_behavior_policy_minimum_cases_v1.json",
    "field_state_reducer_behavior_policy_test_strategy_v1.json",
    "field_state_reducer_behavior_policy_negative_guards_v1.json",
    "field_state_reducer_behavior_policy_governance_mapping_v1.json",
    "field_state_reducer_behavior_policy_diagram_v1.md",
    "field_state_reducer_behavior_policy_summary_v1.json",
    "verify_field_state_reducer_behavior_policy_technical_planning_v1.py",
]

JSON_FILES = [name for name in REQUIRED_FILES if name.endswith(".json")]

EXPECTED_CHECK_COUNT = 94
EXPECTED_FINAL_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_TECHNICAL_PLANNING_GO"
)
EXPECTED_NEXT = "Phase-Luna-Field-State-Reducer-Behavior-Policy-Controlled-Skeleton-Implementation-v1-001"
EXPECTED_FAILURE_DECISION = (
    "LUNA_FIELD_STATE_REDUCER_BEHAVIOR_POLICY_TECHNICAL_PLANNING_BLOCKED"
)
EXPECTED_FAILURE_NEXT = "Phase-Luna-Field-State-Reducer-Behavior-Policy-Technical-Planning-Output-Contract-Correction-v1-001"

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

EXPECTED_TEMPORAL_KEYS = {
    "not_yet_valid",
    "active",
    "expiring",
    "expired",
    "suspended",
    "revoked",
    "superseded",
    "unknown",
}


def _load_json(filename: str) -> Dict[str, Any]:
    with open(BASE_DIR / filename, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _count_mermaid_blocks(markdown_text: str) -> int:
    count = 0
    for line in markdown_text.splitlines():
        if line.strip().lower().startswith("```mermaid"):
            count += 1
    return count


def main() -> int:
    checks: List[Dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [name for name in REQUIRED_FILES if not (BASE_DIR / name).exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        "missing=" + ",".join(missing) if missing else "all_present",
    )

    invalid_json: List[str] = []
    for filename in JSON_FILES:
        try:
            _load_json(filename)
        except Exception as exc:
            invalid_json.append(f"{filename}:{exc}")
    add(
        "all_json_valid",
        len(invalid_json) == 0,
        ";".join(invalid_json) if invalid_json else "valid",
    )

    if missing or invalid_json:
        failed = [c for c in checks if not c["passed"]]
        print("CHECKS")
        for c in checks:
            print(f"- [{'PASS' if c['passed'] else 'FAIL'}] {c['name']}")
        print("FAILED_CHECKS")
        for c in failed:
            print(
                f"- {c['name']}: {c['detail'] if c['detail'] else 'condition_not_met'}"
            )
        print("PASSED_CHECK_COUNT")
        print(sum(1 for c in checks if c["passed"]))
        print("FAILED_CHECK_COUNT")
        print(len(failed))
        print("BLOCKER_COUNT")
        print(len(failed))
        print("FINAL_DECISION")
        print(EXPECTED_FAILURE_DECISION)
        print("NEXT")
        print(EXPECTED_FAILURE_NEXT)
        return 1

    registry = _load_json("field_state_reducer_behavior_policy_registry_v1.json")
    eligibility = _load_json("field_state_reducer_policy_eligibility_matrix_v1.json")
    state_mapping = _load_json("field_state_reducer_state_type_policy_mapping_v1.json")
    precedence = _load_json("field_state_reducer_policy_precedence_matrix_v1.json")
    composition = _load_json("field_state_reducer_policy_composition_contract_v1.json")
    temporal = _load_json("field_state_reducer_temporal_policy_matrix_v1.json")
    confidence = _load_json("field_state_reducer_confidence_policy_matrix_v1.json")
    conflict = _load_json("field_state_reducer_conflict_policy_matrix_v1.json")
    owner = _load_json("field_state_reducer_owner_correction_policy_v1.json")
    overlay = _load_json("field_state_reducer_overlay_policy_v1.json")
    decision_schema = _load_json("field_state_reducer_policy_decision_schema_v1.json")
    replay = _load_json("field_state_reducer_policy_replay_contract_v1.json")
    minimum_cases = _load_json(
        "field_state_reducer_behavior_policy_minimum_cases_v1.json"
    )
    strategy = _load_json("field_state_reducer_behavior_policy_test_strategy_v1.json")
    guards = _load_json("field_state_reducer_behavior_policy_negative_guards_v1.json")
    governance = _load_json(
        "field_state_reducer_behavior_policy_governance_mapping_v1.json"
    )
    summary = _load_json("field_state_reducer_behavior_policy_summary_v1.json")

    diagram_text = (
        BASE_DIR / "field_state_reducer_behavior_policy_diagram_v1.md"
    ).read_text(encoding="utf-8")

    policies = registry.get("policies", [])
    policy_ids = {p.get("policy_id") for p in policies if isinstance(p, dict)}

    # 03-12 policy registry checks
    add("policy_count_exact_11", len(policies) == 11)
    add("policy_ids_exact_match", policy_ids == EXPECTED_POLICY_IDS)
    add(
        "all_policies_implemented_false",
        all(p.get("implemented") is False for p in policies if isinstance(p, dict)),
    )
    add(
        "all_policies_runtime_callable_false",
        all(
            p.get("runtime_callable") is False for p in policies if isinstance(p, dict)
        ),
    )
    add(
        "all_policies_real_execution_false",
        all(p.get("real_execution") is False for p in policies if isinstance(p, dict)),
    )
    add(
        "all_policies_state_write_allowed_false",
        all(
            p.get("state_write_allowed") is False
            for p in policies
            if isinstance(p, dict)
        ),
    )
    add(
        "all_policies_fact_promotion_allowed_false",
        all(
            p.get("fact_promotion_allowed") is False
            for p in policies
            if isinstance(p, dict)
        ),
    )
    add(
        "all_policies_action_trigger_allowed_false",
        all(
            p.get("action_trigger_allowed") is False
            for p in policies
            if isinstance(p, dict)
        ),
    )
    add(
        "global_simple_average_default_false",
        registry.get("global_simple_average_default") is False,
    )
    add(
        "policy_registry_complete_true",
        registry.get("policy_registry_complete") is True,
    )

    matrix = eligibility.get("eligibility_matrix", [])

    # 13-20 eligibility checks
    add("eligibility_rows_exact_11", len(matrix) == 11)
    add(
        "eligibility_policy_ids_match_registry",
        {row.get("policy_id") for row in matrix if isinstance(row, dict)} == policy_ids,
    )
    add(
        "eligibility_no_direct_state_write_all_false",
        all(row.get("direct_state_write_allowed") is False for row in matrix),
    )
    add(
        "eligibility_no_fact_promotion_all_false",
        all(row.get("fact_promotion_allowed") is False for row in matrix),
    )
    add(
        "eligibility_no_action_trigger_all_false",
        all(row.get("action_trigger_allowed") is False for row in matrix),
    )
    add(
        "eligibility_no_provider_recall_all_false",
        all(row.get("provider_recall_allowed") is False for row in matrix),
    )
    add(
        "eligibility_no_external_lookup_all_false",
        all(row.get("external_lookup_allowed") is False for row in matrix),
    )
    add(
        "eligibility_real_execution_all_false",
        all(row.get("real_execution") is False for row in matrix),
    )

    mappings = state_mapping.get("state_type_mappings", {})

    # 21-28 state mapping checks
    add("state_type_mapping_count_exact_12", len(mappings) == 12)
    add("state_type_keys_exact_match", set(mappings.keys()) == EXPECTED_STATE_TYPES)
    add(
        "state_type_mapping_complete_true",
        state_mapping.get("state_type_mapping_complete") is True,
    )
    add(
        "latest_event_global_default_all_false",
        all(v.get("latest_event_global_default") is False for v in mappings.values()),
    )
    add(
        "highest_confidence_global_default_all_false",
        all(
            v.get("highest_confidence_global_default") is False
            for v in mappings.values()
        ),
    )
    add(
        "state_mapping_fact_promotion_all_false",
        all(v.get("fact_promotion_allowed") is False for v in mappings.values()),
    )
    add(
        "state_mapping_default_fallback_present",
        all(
            isinstance(v.get("default_fallback_policy"), str)
            and v.get("default_fallback_policy")
            for v in mappings.values()
        ),
    )
    add(
        "state_mapping_minimum_support_present",
        all(
            isinstance(v.get("minimum_support_policy"), str)
            and v.get("minimum_support_policy")
            for v in mappings.values()
        ),
    )

    precedence_rules = precedence.get("precedence_rules", [])

    # 29-35 precedence checks
    add("precedence_rule_count_at_least_10", len(precedence_rules) >= 10)
    add(
        "precedence_matrix_complete_true",
        precedence.get("precedence_matrix_complete") is True,
    )
    add(
        "owner_correction_not_auto_higher_than_confirmed_fact_true",
        precedence.get("owner_correction_not_auto_higher_than_confirmed_fact") is True,
    )
    add(
        "precedence_override_allowed_all_true",
        all(rule.get("override_allowed") is True for rule in precedence_rules),
    )
    add(
        "precedence_fact_promotion_all_false",
        all(rule.get("fact_promotion_allowed") is False for rule in precedence_rules),
    )
    add(
        "revocation_over_latest_rule_exists",
        any(
            rule.get("higher_policy") == "revocation_override"
            and rule.get("lower_policy") == "latest_valid_event"
            for rule in precedence_rules
        ),
    )
    add(
        "conflict_over_confidence_rule_exists",
        any(
            rule.get("higher_policy") == "conflict_preservation"
            and rule.get("lower_policy") == "highest_confidence_valid_event"
            for rule in precedence_rules
        ),
    )

    # 36-43 composition checks
    deterministic_order = composition.get("deterministic_composition_order", [])
    add(
        "composition_contract_complete_true",
        composition.get("composition_contract_complete") is True,
    )
    add(
        "maximum_composition_depth_exact_3",
        composition.get("maximum_composition_depth") == 3,
    )
    add(
        "policy_result_feed_forward_allowed_true",
        composition.get("policy_result_feed_forward_allowed") is True,
    )
    add(
        "policy_side_effect_allowed_false",
        composition.get("policy_side_effect_allowed") is False,
    )
    add(
        "state_write_during_composition_allowed_false",
        composition.get("state_write_during_composition_allowed") is False,
    )
    add(
        "action_trigger_during_composition_allowed_false",
        composition.get("action_trigger_during_composition_allowed") is False,
    )
    add(
        "non_composable_policy_pairs_non_empty",
        len(composition.get("non_composable_policy_pairs", [])) > 0,
    )
    add(
        "deterministic_composition_order_covers_registry",
        EXPECTED_POLICY_IDS.issubset(set(deterministic_order)),
    )

    temporal_map = temporal.get("temporal_statuses", {})

    # 44-53 temporal checks
    add(
        "temporal_policy_matrix_complete_true",
        temporal.get("temporal_policy_matrix_complete") is True,
    )
    add("temporal_status_count_exact_8", len(temporal_map) == 8)
    add(
        "temporal_status_keys_exact_match",
        set(temporal_map.keys()) == EXPECTED_TEMPORAL_KEYS,
    )
    add(
        "expired_support_eligible_false",
        temporal_map.get("expired", {}).get("support_eligible") is False,
    )
    add(
        "revoked_support_eligible_false",
        temporal_map.get("revoked", {}).get("support_eligible") is False,
    )
    add(
        "suspended_support_eligible_false",
        temporal_map.get("suspended", {}).get("support_eligible") is False,
    )
    add(
        "revoked_reactivation_allowed_false",
        temporal_map.get("revoked", {}).get("reactivation_allowed") is False,
    )
    add(
        "expired_active_state_support_allowed_false",
        temporal_map.get("expired", {}).get("active_state_support_allowed") is False,
    )
    add(
        "suspended_active_state_support_allowed_false",
        temporal_map.get("suspended", {}).get("active_state_support_allowed") is False,
    )
    add(
        "temporal_fact_promotion_all_false",
        all(v.get("fact_promotion_allowed") is False for v in temporal_map.values()),
    )

    confidence_map = confidence.get("state_type_confidence_policies", {})

    # 54-61 confidence checks
    add(
        "confidence_policy_matrix_complete_true",
        confidence.get("confidence_policy_matrix_complete") is True,
    )
    add("confidence_policy_count_exact_12", len(confidence_map) == 12)
    add(
        "confidence_simple_average_global_default_all_false",
        all(
            v.get("simple_average_global_default") is False
            for v in confidence_map.values()
        ),
    )
    add(
        "confidence_no_automatic_100_all_true",
        all(
            v.get("no_automatic_100_confidence") is True
            for v in confidence_map.values()
        ),
    )
    add(
        "confidence_fabricated_confidence_all_false",
        all(
            v.get("fabricated_confidence_allowed") is False
            for v in confidence_map.values()
        ),
    )
    add(
        "confidence_minimum_le_maximum_all",
        all(
            isinstance(v.get("minimum_threshold"), (int, float))
            and isinstance(v.get("maximum_cap"), (int, float))
            and float(v.get("minimum_threshold")) <= float(v.get("maximum_cap"))
            for v in confidence_map.values()
        ),
    )
    add(
        "uncertainty_state_minimum_threshold_zero",
        confidence_map.get("uncertainty_state", {}).get("minimum_threshold") == 0.00,
    )
    add(
        "conflict_state_minimum_threshold_zero",
        confidence_map.get("conflict_state", {}).get("minimum_threshold") == 0.00,
    )

    conflict_cases = conflict.get("conflict_cases", [])

    # 62-69 conflict checks
    add(
        "conflict_policy_matrix_complete_true",
        conflict.get("conflict_policy_matrix_complete") is True,
    )
    add("conflict_case_count_exact_10", len(conflict_cases) == 10)
    add(
        "unresolved_conflict_preservation_supported_true",
        conflict.get("unresolved_conflict_preservation_supported") is True,
    )
    add(
        "conflict_preserve_when_unresolved_all_true",
        all(c.get("preserve_conflict_when_unresolved") is True for c in conflict_cases),
    )
    add(
        "conflict_winner_required_all_false",
        all(c.get("winner_required") is False for c in conflict_cases),
    )
    add(
        "conflict_fact_promotion_all_false",
        all(c.get("fact_promotion_allowed") is False for c in conflict_cases),
    )
    add(
        "conflict_direct_state_write_all_false",
        all(c.get("direct_state_write_allowed") is False for c in conflict_cases),
    )
    add(
        "conflict_active_vs_revoked_case_exists",
        any(c.get("scenario") == "active_vs_revoked" for c in conflict_cases),
    )

    # 70-79 owner and overlay checks
    add(
        "owner_correction_is_candidate_true",
        owner.get("owner_correction_is_candidate") is True,
    )
    add(
        "owner_correction_is_fact_false", owner.get("owner_correction_is_fact") is False
    )
    add(
        "owner_direct_state_mutation_allowed_false",
        owner.get("direct_state_mutation_allowed") is False,
    )
    add(
        "owner_supporting_evidence_required_true",
        owner.get("supporting_evidence_required") is True,
    )
    add(
        "owner_correction_override_confirmed_fact_without_review_false",
        owner.get("correction_can_override_confirmed_fact_without_review") is False,
    )
    add(
        "overlay_is_separate_state_layer_true",
        overlay.get("overlay_is_separate_state_layer") is True,
    )
    add(
        "overlay_substrate_mutation_allowed_false",
        overlay.get("substrate_mutation_allowed") is False,
    )
    add(
        "overlay_can_replace_substrate_permanently_false",
        overlay.get("overlay_can_replace_substrate_permanently") is False,
    )
    add(
        "overlay_end_auto_restore_without_evidence_false",
        overlay.get("overlay_end_auto_restore_without_evidence") is False,
    )
    add(
        "overlay_conflict_preserved_true",
        overlay.get("overlay_conflict_preserved") is True,
    )

    # 80-87 decision and replay checks
    add(
        "policy_decision_schema_complete_true",
        decision_schema.get("decision_schema_complete") is True,
    )
    add(
        "decision_schema_fields_at_least_20",
        len(decision_schema.get("schema_fields", [])) >= 20,
    )
    add(
        "decision_schema_state_mutation_executed_false",
        decision_schema.get("state_mutation_executed") is False,
    )
    add(
        "decision_schema_fact_promotion_executed_false",
        decision_schema.get("fact_promotion_executed") is False,
    )
    add(
        "decision_schema_action_trigger_executed_false",
        decision_schema.get("action_trigger_executed") is False,
    )
    add(
        "policy_replay_contract_complete_true",
        replay.get("replay_contract_complete") is True,
    )
    add(
        "deterministic_policy_replay_true",
        replay.get("deterministic_policy_replay") is True,
    )
    add(
        "replay_external_runtime_dependency_all_false",
        replay.get("external_lookup_during_replay_allowed") is False
        and replay.get("provider_recall_during_replay_allowed") is False
        and replay.get("action_trigger_during_replay_allowed") is False
        and replay.get("current_runtime_state_dependency_allowed") is False
        and replay.get("policy_version_fallback_allowed") is False,
    )

    cases = minimum_cases.get("cases", [])

    # 88-94 final checks
    add("minimum_cases_count_exact_12", len(cases) == 12)
    add(
        "minimum_cases_all_execution_flags_false",
        all(
            c.get("state_mutation_allowed") is False
            and c.get("fact_promotion_allowed") is False
            and c.get("action_trigger_allowed") is False
            for c in cases
        ),
    )
    add(
        "behavior_policy_test_strategy_complete_true",
        strategy.get("test_strategy_complete") is True,
    )
    add(
        "behavior_policy_negative_guards_complete_true",
        guards.get("negative_guards_complete") is True,
    )
    add(
        "governance_mapping_complete_and_boundaries_true",
        governance.get("governance_mapping_complete") is True
        and governance.get("policy_layer_has_fact_admission_authority") is False
        and governance.get("policy_layer_has_action_trigger_authority") is False
        and governance.get("policy_layer_has_direct_state_store_write_authority")
        is False,
    )
    add("diagram_mermaid_blocks_at_least_6", _count_mermaid_blocks(diagram_text) >= 6)
    add(
        "summary_contract_exact_match",
        summary.get("planning_only") is True
        and summary.get("behavior_policy_planning_completed") is True
        and summary.get("policy_count") == 11
        and summary.get("state_type_count") == 12
        and summary.get("minimum_case_count") == 12
        and summary.get("policy_functions_implemented") is False
        and summary.get("policy_runtime_callable") is False
        and summary.get("real_policy_execution") is False
        and summary.get("real_reduction_implemented") is False
        and summary.get("real_reduction_executed") is False
        and summary.get("state_mutation_executed") is False
        and summary.get("fact_promotion_executed") is False
        and summary.get("action_trigger_executed") is False
        and summary.get("provider_recall_executed") is False
        and summary.get("external_lookup_executed") is False
        and summary.get("blocker_count") == 0
        and summary.get("final_decision") == EXPECTED_FINAL_DECISION
        and summary.get("recommended_next_phase") == EXPECTED_NEXT,
    )

    failed = [c for c in checks if not c["passed"]]
    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(failed)
    blocker_count = failed_count

    if len(checks) != EXPECTED_CHECK_COUNT:
        failed_count += 1
        blocker_count += 1
        failed.append(
            {
                "name": "expected_check_count_exact_94",
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
        print("- [FAIL] expected_check_count_exact_94")

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
