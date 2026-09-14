#!/usr/bin/env python3

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPECTED_FINAL_DECISION = "LUNA_FIELD_STATE_REDUCER_TECHNICAL_PLANNING_GO"
EXPECTED_NEXT = (
    "Phase-Luna-Field-State-Reducer-Controlled-Skeleton-Implementation-v1-001"
)

REQUIRED_FILES = [
    "field_state_reducer_technical_plan_v1.md",
    "field_state_schema_v1.json",
    "field_state_type_registry_v1.json",
    "field_state_status_registry_v1.json",
    "field_state_status_transition_matrix_v1.json",
    "field_state_reducer_input_contract_v1.json",
    "field_state_reducer_output_contract_v1.json",
    "field_state_reduction_policy_registry_v1.json",
    "field_state_event_ordering_contract_v1.json",
    "field_state_conflict_resolution_matrix_v1.json",
    "field_state_temporal_reduction_contract_v1.json",
    "field_state_confidence_aggregation_contract_v1.json",
    "field_state_provenance_trace_schema_v1.json",
    "field_state_replay_contract_v1.json",
    "field_state_minimum_case_timeline_v1.json",
    "field_state_existing_asset_reuse_mapping_v1.json",
    "field_state_reducer_protocol_diagram_v1.md",
    "field_state_reducer_test_strategy_v1.json",
    "field_state_reducer_governance_mapping_v1.json",
    "field_state_reducer_negative_guards_v1.json",
    "field_state_reducer_summary_v1.json",
    "verify_field_state_reducer_technical_planning_v1.py",
]

JSON_FILES = [name for name in REQUIRED_FILES if name.endswith(".json")]


def load_json(filename):
    with open(BASE_DIR / filename, "r", encoding="utf-8") as handle:
        return json.load(handle)


def has_all(items, expected):
    item_set = set(items)
    return all(v in item_set for v in expected)


def count_mermaid_blocks(markdown_text):
    return markdown_text.count("```mermaid")


def main():
    checks = []

    def add(name, passed, detail=""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [name for name in REQUIRED_FILES if not (BASE_DIR / name).exists()]
    add(
        "required_files_exist",
        len(missing) == 0,
        "missing=" + ",".join(missing) if missing else "ok",
    )

    invalid = []
    for filename in JSON_FILES:
        try:
            load_json(filename)
        except Exception as exc:
            invalid.append(f"{filename}:{exc}")
    add("all_json_valid", len(invalid) == 0, ";".join(invalid) if invalid else "ok")

    if missing or invalid:
        failed = [c for c in checks if not c["passed"]]
        print("CHECKS")
        for c in checks:
            s = "PASS" if c["passed"] else "FAIL"
            print(f"- [{s}] {c['name']}")
        print("FAILED_CHECKS")
        for c in failed:
            print(f"- {c['name']}: {c['detail']}")
        print("PASSED_CHECK_COUNT")
        print(sum(1 for c in checks if c["passed"]))
        print("FAILED_CHECK_COUNT")
        print(len(failed))
        print("BLOCKER_COUNT")
        print(len(failed))
        print("FINAL_DECISION")
        print("LUNA_FIELD_STATE_REDUCER_TECHNICAL_PLANNING_BLOCKED")
        print("NEXT")
        print("REMEDIATE_FIELD_STATE_REDUCER_TECHNICAL_PLANNING")
        raise SystemExit(1)

    schema = load_json("field_state_schema_v1.json")
    type_registry = load_json("field_state_type_registry_v1.json")
    status_registry = load_json("field_state_status_registry_v1.json")
    transition = load_json("field_state_status_transition_matrix_v1.json")
    input_contract = load_json("field_state_reducer_input_contract_v1.json")
    output_contract = load_json("field_state_reducer_output_contract_v1.json")
    ordering = load_json("field_state_event_ordering_contract_v1.json")
    conflict = load_json("field_state_conflict_resolution_matrix_v1.json")
    temporal = load_json("field_state_temporal_reduction_contract_v1.json")
    provenance = load_json("field_state_provenance_trace_schema_v1.json")
    replay = load_json("field_state_replay_contract_v1.json")
    timeline = load_json("field_state_minimum_case_timeline_v1.json")
    reuse = load_json("field_state_existing_asset_reuse_mapping_v1.json")
    test_strategy = load_json("field_state_reducer_test_strategy_v1.json")
    governance = load_json("field_state_reducer_governance_mapping_v1.json")
    summary = load_json("field_state_reducer_summary_v1.json")

    diagram_text = (BASE_DIR / "field_state_reducer_protocol_diagram_v1.md").read_text(
        encoding="utf-8"
    )

    expected_core_fields = {
        "state_id",
        "field_id",
        "state_type",
        "state_value",
        "state_status",
        "confidence",
        "effective_from",
        "effective_until",
        "source_event_ids",
        "supporting_event_ids",
        "opposing_event_ids",
        "ignored_event_ids",
        "reducer_version",
        "reduction_policy_version",
        "temporal_snapshot_ref",
        "conflict_refs",
        "provenance_chain",
        "supersedes_state_id",
        "derived_not_observed",
        "created_at",
        "updated_at",
    }
    add(
        "field_state_schema_core_fields_complete",
        has_all(schema.get("core_fields", []), expected_core_fields),
    )

    expected_state_types = {
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
    actual_state_types = {
        item.get("state_type") for item in type_registry.get("state_types", [])
    }
    add("field_state_types_complete", expected_state_types.issubset(actual_state_types))

    expected_statuses = {
        "candidate",
        "provisional",
        "active",
        "degraded",
        "uncertain",
        "conflicted",
        "suspended",
        "expired",
        "revoked",
        "superseded",
        "unresolved",
    }
    add(
        "field_state_statuses_complete",
        has_all(status_registry.get("statuses", []), expected_statuses),
    )

    add(
        "reducer_single_mutation_authority_true",
        summary.get("reducer_is_single_mutation_authority") is True,
    )

    direct_mutation_false = (
        summary.get("vision_state_mutation_allowed") is False
        and summary.get("ocr_state_mutation_allowed") is False
        and summary.get("speech_state_mutation_allowed") is False
        and summary.get("navigation_state_mutation_allowed") is False
        and summary.get("memory_state_mutation_allowed") is False
        and summary.get("planner_state_mutation_allowed") is False
        and summary.get("skill_state_mutation_allowed") is False
        and summary.get("provider_state_mutation_allowed") is False
    )
    add("direct_module_state_mutation_all_false", direct_mutation_false)

    add(
        "event_admitted_not_equal_state_created",
        summary.get("event_admitted_not_equal_state_created") is True,
    )
    add(
        "event_active_not_equal_state_active",
        summary.get("event_active_not_equal_state_active") is True,
    )

    add(
        "reducer_input_only_admitted_events",
        input_contract.get("reducer_input_only_admitted_events") is True,
    )
    prohibited = input_contract.get("prohibited_inputs", {})
    add("raw_observation_consumption_false", prohibited.get("raw_observation") is False)
    add("provider_recall_false", prohibited.get("provider_recall") is False)
    add("external_lookup_false", replay.get("external_lookup_during_replay") is False)
    add("action_trigger_false", replay.get("action_trigger_during_replay") is False)

    add("deterministic_replay_true", replay.get("deterministic_replay") is True)
    add(
        "stable_tie_breaker_defined", ordering.get("stable_tie_breaker_defined") is True
    )

    forbidden = transition.get("forbidden_transitions", [])
    add(
        "revoked_to_active_false",
        any(
            i.get("from") == "revoked"
            and i.get("to") == "active"
            and i.get("allowed") is False
            for i in forbidden
        ),
    )
    add(
        "expired_to_active_without_new_event_false",
        any(
            i.get("from") == "expired"
            and i.get("to") == "active"
            and i.get("allowed") is False
            and i.get("without_new_event") is True
            for i in forbidden
        ),
    )
    add(
        "suspended_to_active_without_refresh_false",
        any(
            i.get("from") == "suspended"
            and i.get("to") == "active"
            and i.get("allowed") is False
            and i.get("without_refresh_evidence") is True
            for i in forbidden
        ),
    )
    add(
        "superseded_to_active_false",
        any(
            i.get("from") == "superseded"
            and i.get("to") == "active"
            and i.get("allowed") is False
            for i in forbidden
        ),
    )
    add(
        "conflicted_to_active_without_resolution_false",
        any(
            i.get("from") == "conflicted"
            and i.get("to") == "active"
            and i.get("allowed") is False
            and i.get("without_conflict_resolution") is True
            for i in forbidden
        ),
    )

    add(
        "overlay_substrate_mutation_false",
        temporal.get("overlay_substrate_mutation_false") is True,
    )
    add(
        "overlay_end_requires_refresh_true",
        temporal.get("overlay_end_requires_refresh_true") is True,
    )

    add(
        "conflict_preservation_supported",
        conflict.get("conflict_preservation_supported") is True,
    )
    add(
        "unresolved_state_supported", conflict.get("unresolved_state_supported") is True
    )
    rules = conflict.get("conflict_rules", [])
    add(
        "fact_promotion_allowed_all_false",
        len(rules) > 0 and all(r.get("fact_promotion_allowed") is False for r in rules),
    )

    guards = load_json("field_state_reducer_negative_guards_v1.json").get("guards", {})
    add("physical_delete_allowed_false", guards.get("no_physical_delete") is True)

    expected_trace_fields = {
        "trace_id",
        "state_id",
        "reducer_run_id",
        "reducer_version",
        "policy_version",
        "input_event_ids",
        "ordered_event_ids",
        "accepted_event_ids",
        "rejected_event_ids",
        "ignored_event_ids",
        "conflict_ids",
        "temporal_snapshot",
        "decision_steps",
        "resulting_state_hash",
        "replay_key",
        "created_at",
    }
    add(
        "provenance_trace_complete",
        provenance.get("provenance_trace_complete") is True
        and has_all(provenance.get("fields", []), expected_trace_fields),
    )

    add(
        "xiaobeimen_timeline_complete",
        timeline.get("xiaobeimen_timeline_complete") is True
        and len(timeline.get("timeline_steps", [])) >= 11,
    )
    add("test_strategy_complete", test_strategy.get("test_strategy_complete") is True)
    add(
        "governance_mapping_complete",
        governance.get("governance_mapping_complete") is True,
    )
    add(
        "existing_asset_mapping_complete",
        reuse.get("existing_asset_mapping_complete") is True
        and len(reuse.get("mappings", [])) == 10,
    )

    add("mermaid_at_least_5_blocks", count_mermaid_blocks(diagram_text) >= 5)

    add("candidate_only_true", summary.get("candidate_only") is True)
    add("planning_only_true", summary.get("planning_only") is True)
    add("runtime_implemented_false", summary.get("runtime_implemented") is False)
    add("reducer_executed_false", summary.get("reducer_executed") is False)
    add("database_created_false", summary.get("database_created") is False)
    add("scheduler_created_false", summary.get("scheduler_created") is False)
    add("migration_executed_false", summary.get("migration_executed") is False)
    add("training_executed_false", summary.get("training_executed") is False)
    add("production_execution_false", summary.get("production_execution") is False)
    add("blocker_count_zero", summary.get("blocker_count") == 0)
    add(
        "final_decision_exact_match",
        summary.get("final_decision") == EXPECTED_FINAL_DECISION,
    )
    add("next_exact_match", summary.get("next") == EXPECTED_NEXT)

    failed = [c for c in checks if not c["passed"]]
    passed_count = sum(1 for c in checks if c["passed"])
    failed_count = len(failed)
    blocker_count = failed_count

    final_decision = (
        EXPECTED_FINAL_DECISION
        if blocker_count == 0
        else "LUNA_FIELD_STATE_REDUCER_TECHNICAL_PLANNING_BLOCKED"
    )
    next_phase = (
        EXPECTED_NEXT
        if blocker_count == 0
        else "REMEDIATE_FIELD_STATE_REDUCER_TECHNICAL_PLANNING"
    )

    print("CHECKS")
    for c in checks:
        s = "PASS" if c["passed"] else "FAIL"
        print(f"- [{s}] {c['name']}")

    print("FAILED_CHECKS")
    if failed:
        for c in failed:
            d = c["detail"] if c["detail"] else "condition_not_met"
            print(f"- {c['name']}: {d}")
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
    print(next_phase)

    raise SystemExit(0 if blocker_count == 0 else 1)


if __name__ == "__main__":
    main()
