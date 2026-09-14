#!/usr/bin/env python3

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REQUIRED_FILES = [
    "field_event_and_temporal_validity_protocol_v1.md",
    "field_event_envelope_schema_v1.json",
    "field_event_type_registry_v1.json",
    "temporal_validity_schema_v1.json",
    "temporal_validity_type_registry_v1.json",
    "temporal_status_transition_matrix_v1.json",
    "field_event_admission_contract_v1.json",
    "field_event_replay_contract_v1.json",
    "temporary_overlay_protocol_v1.json",
    "field_event_conflict_resolution_matrix_v1.json",
    "field_event_revision_revocation_protocol_v1.json",
    "field_event_minimum_case_timeline_v1.json",
    "field_event_protocol_test_strategy_v1.json",
    "field_event_existing_asset_reuse_mapping_v1.json",
    "field_event_protocol_diagram_v1.md",
    "field_event_temporal_protocol_summary_v1.json",
    "verify_field_event_temporal_validity_protocol_planning_v1.py",
]

JSON_FILES = [f for f in REQUIRED_FILES if f.endswith(".json")]
EXPECTED_DECISION = "LUNA_FIELD_EVENT_TEMPORAL_VALIDITY_PROTOCOL_PLANNING_GO"
EXPECTED_NEXT = "Phase-Luna-Field-State-Reducer-Technical-Planning-v1-001"


def load_json(filename):
    with open(BASE_DIR / filename, "r", encoding="utf-8") as handle:
        return json.load(handle)


def has_all(items, expected):
    item_set = set(items)
    return all(value in item_set for value in expected)


def count_mermaid_blocks(markdown_text):
    lines = [line.strip() for line in markdown_text.splitlines()]
    labels = set()
    for line in lines:
        if "[" in line and "]" in line and "-->" in line:
            tokens = line.replace("-->", " ").split()
            for token in tokens:
                if "[" in token:
                    labels.add(token.split("[")[0])
    return len(labels)


def main():
    checks = []

    def add_check(name, passed, detail=""):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    missing = [name for name in REQUIRED_FILES if not (BASE_DIR / name).exists()]
    add_check(
        "required_files_exist",
        len(missing) == 0,
        "missing=" + ",".join(missing) if missing else "all_present",
    )

    invalid = []
    for filename in JSON_FILES:
        try:
            load_json(filename)
        except Exception as exc:
            invalid.append((filename, str(exc)))
    add_check(
        "all_json_valid",
        len(invalid) == 0,
        ";".join([f"{name}:{err}" for name, err in invalid]) if invalid else "valid",
    )

    if missing or invalid:
        passed = sum(1 for c in checks if c["passed"])
        failed = [c for c in checks if not c["passed"]]
        print("CHECKS")
        for c in checks:
            state = "PASS" if c["passed"] else "FAIL"
            print(f"- [{state}] {c['name']}")
        print("FAILED_CHECKS")
        for c in failed:
            print(f"- {c['name']}: {c['detail']}")
        print("PASSED_CHECK_COUNT")
        print(passed)
        print("FAILED_CHECK_COUNT")
        print(len(failed))
        print("BLOCKER_COUNT")
        print(len(failed))
        print("FINAL_DECISION")
        print("LUNA_FIELD_EVENT_TEMPORAL_VALIDITY_PROTOCOL_PLANNING_BLOCKED")
        print("NEXT")
        print(
            "Phase-Luna-Field-Event-And-Temporal-Validity-Protocol-Planning-Output-Contract-Correction-v1-001"
        )
        raise SystemExit(1)

    envelope = load_json("field_event_envelope_schema_v1.json")
    registry = load_json("field_event_type_registry_v1.json")
    temporal_schema = load_json("temporal_validity_schema_v1.json")
    temporal_types = load_json("temporal_validity_type_registry_v1.json")
    temporal_matrix = load_json("temporal_status_transition_matrix_v1.json")
    admission = load_json("field_event_admission_contract_v1.json")
    replay = load_json("field_event_replay_contract_v1.json")
    overlay = load_json("temporary_overlay_protocol_v1.json")
    conflict = load_json("field_event_conflict_resolution_matrix_v1.json")
    revision = load_json("field_event_revision_revocation_protocol_v1.json")
    timeline = load_json("field_event_minimum_case_timeline_v1.json")
    test_strategy = load_json("field_event_protocol_test_strategy_v1.json")
    asset_mapping = load_json("field_event_existing_asset_reuse_mapping_v1.json")
    summary = load_json("field_event_temporal_protocol_summary_v1.json")

    diagram_text = (BASE_DIR / "field_event_protocol_diagram_v1.md").read_text(
        encoding="utf-8"
    )

    expected_envelope_fields = [
        "event_id",
        "event_type",
        "schema_version",
        "occurred_at",
        "observed_at",
        "asserted_at",
        "recorded_at",
        "source_scope",
        "owner_scope",
        "perspective_scope",
        "field_scope",
        "space_anchor_refs",
        "target_object_refs",
        "evidence_refs",
        "trace_refs",
        "governance_refs",
        "temporal_validity",
        "confidence",
        "candidate_only",
        "not_fact",
        "revision",
        "supersedes_event_ref",
        "correlation_id",
        "causation_event_ref",
        "replayable",
        "reversible",
        "revoked",
        "revocation_reason",
        "extension_data",
    ]
    add_check(
        "event_envelope_core_fields_complete",
        has_all(envelope.get("core_fields", []), expected_envelope_fields),
        "core_fields_missing",
    )

    expected_categories = {
        "observation",
        "assertion",
        "lifecycle",
        "temporal",
        "correction",
        "transition",
    }
    category_names = {item.get("category") for item in registry.get("categories", [])}
    registry_complete = expected_categories.issubset(category_names)
    add_check(
        "event_type_registry_complete", registry_complete, "category_set_incomplete"
    )

    expected_temporal_types = {
        "persistent",
        "interval",
        "recurring",
        "temporary",
        "seasonal",
        "event_driven",
        "until_revoked",
        "inherited",
        "unknown_validity",
    }
    add_check(
        "temporal_validity_types_complete_9",
        has_all(
            temporal_types.get("temporal_validity_types", []), expected_temporal_types
        ),
        "temporal_types_incomplete",
    )

    expected_statuses = {
        "pending",
        "active",
        "inactive",
        "stale",
        "expired",
        "suspended",
        "revoked",
        "unknown",
    }
    add_check(
        "temporal_status_complete_8",
        has_all(temporal_schema.get("temporal_statuses", []), expected_statuses),
        "temporal_statuses_incomplete",
    )

    forbidden = temporal_matrix.get("forbidden_transitions", [])
    conditional = temporal_matrix.get("conditional_transitions", [])

    revoked_to_active_forbidden = any(
        item.get("from") == "revoked"
        and item.get("to") == "active"
        and item.get("allowed") is False
        for item in forbidden
    )
    add_check(
        "revoked_not_to_active",
        revoked_to_active_forbidden,
        "revoked_transition_missing",
    )

    expired_to_active_forbidden = any(
        item.get("from") == "expired"
        and item.get("to") == "active"
        and item.get("allowed") is False
        and item.get("requires_new_evidence") is True
        for item in forbidden
    )
    add_check(
        "expired_not_to_active_without_new_evidence",
        expired_to_active_forbidden,
        "expired_transition_rule_missing",
    )

    suspended_reactivation_rule = any(
        item.get("from") == "suspended"
        and item.get("to") == "active"
        and item.get("allowed") is True
        and item.get("requires_refresh_evidence") is True
        for item in conditional
    )
    add_check(
        "suspended_reactivation_requires_refresh_evidence",
        suspended_reactivation_rule,
        "suspended_rule_missing",
    )

    add_check(
        "admission_does_not_equal_fact_true",
        admission.get("admission_does_not_equal_fact") is True,
        "admission_flag_missing",
    )
    add_check(
        "admission_does_not_equal_state_mutation_true",
        admission.get("admission_does_not_equal_state_mutation") is True,
        "admission_mutation_flag_missing",
    )

    add_check(
        "deterministic_replay_true",
        replay.get("deterministic_replay_required") is True,
        "deterministic_replay_required_not_true",
    )
    add_check(
        "provider_recall_during_replay_false",
        replay.get("provider_recall_during_replay_allowed") is False,
        "provider_recall_flag_invalid",
    )
    add_check(
        "action_trigger_during_replay_false",
        replay.get("action_trigger_during_replay_allowed") is False,
        "action_trigger_flag_invalid",
    )

    overlay_types = overlay.get("overlay_types", [])
    add_check(
        "temporary_overlay_types_complete_8",
        len(overlay_types) == 8,
        "overlay_type_count_not_8",
    )

    overlay_matrix = overlay.get("overlay_class_matrix", [])
    substrate_all_false = len(overlay_matrix) == 8 and all(
        row.get("substrate_mutation_allowed") is False for row in overlay_matrix
    )
    add_check(
        "substrate_mutation_allowed_all_false",
        substrate_all_false,
        "overlay_substrate_rule_invalid",
    )

    refresh_all_true = len(overlay_matrix) == 8 and all(
        row.get("refresh_required_after_end") is True for row in overlay_matrix
    )
    add_check(
        "refresh_required_after_end_all_true",
        refresh_all_true,
        "overlay_refresh_rule_invalid",
    )

    conflict_rows = conflict.get("conflict_matrix", [])
    add_check(
        "conflict_types_complete_8", len(conflict_rows) == 8, "conflict_count_not_8"
    )
    add_check(
        "fact_promotion_allowed_all_false",
        len(conflict_rows) == 8
        and all(row.get("fact_promotion_allowed") is False for row in conflict_rows),
        "conflict_fact_promotion_invalid",
    )

    add_check(
        "physical_delete_allowed_false",
        revision.get("physical_delete_allowed") is False,
        "physical_delete_allowed_not_false",
    )
    add_check(
        "correction_requires_new_event_true",
        revision.get("correction_requires_new_event") is True,
        "correction_requires_new_event_not_true",
    )

    timeline_complete = (
        timeline.get("timeline_complete") is True
        and len(timeline.get("timeline", [])) >= 6
    )
    add_check("xiaobeimen_timeline_complete", timeline_complete, "timeline_incomplete")

    add_check(
        "test_strategy_complete",
        test_strategy.get("test_strategy_complete") is True
        and len(test_strategy.get("test_categories", [])) >= 7,
        "test_strategy_incomplete",
    )

    add_check(
        "existing_asset_mapping_complete",
        asset_mapping.get("mapping_complete") is True
        and len(asset_mapping.get("asset_mapping", [])) >= 8,
        "asset_mapping_incomplete",
    )

    mermaid_block_count = count_mermaid_blocks(diagram_text)
    add_check(
        "mermaid_at_least_5_blocks",
        mermaid_block_count >= 5,
        f"mermaid_blocks={mermaid_block_count}",
    )

    mapping_rows = asset_mapping.get("asset_mapping", [])
    add_check(
        "physical_move_allowed_all_false",
        len(mapping_rows) > 0
        and all(row.get("physical_move_allowed") is False for row in mapping_rows),
        "physical_move_allowed_not_all_false",
    )

    core_governance_rows = [
        row for row in mapping_rows if row.get("asset") == "Core Governance Assets"
    ]
    core_governance_ok = (
        len(core_governance_rows) == 1
        and core_governance_rows[0].get("rewrite_required") is False
    )
    add_check(
        "core_governance_assets_rewrite_required_false",
        core_governance_ok,
        "core_governance_rewrite_flag_invalid",
    )

    boundaries_ok = (
        summary.get("direct_state_mutation_allowed") is False
        and summary.get("database_implementation_allowed") is False
        and summary.get("scheduler_implementation_allowed") is False
        and summary.get("real_runtime_implementation_allowed") is False
        and summary.get("directory_migration_allowed") is False
        and summary.get("model_training_allowed") is False
        and summary.get("production_activation_allowed") is False
    )
    add_check(
        "execution_migration_training_production_boundaries_false",
        boundaries_ok,
        "boundary_flags_invalid",
    )

    add_check(
        "candidate_only_true",
        summary.get("candidate_only") is True,
        "candidate_only_not_true",
    )
    add_check("not_fact_true", summary.get("not_fact") is True, "not_fact_not_true")
    add_check(
        "blocker_count_zero",
        summary.get("blocker_count") == 0,
        "blocker_count_not_zero",
    )
    add_check(
        "final_decision_exact_match",
        summary.get("final_decision") == EXPECTED_DECISION,
        "final_decision_mismatch",
    )
    add_check(
        "next_exact_match",
        summary.get("recommended_next_phase") == EXPECTED_NEXT,
        "recommended_next_phase_mismatch",
    )

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    blocker_count = len(failed)

    final_decision = (
        EXPECTED_DECISION
        if blocker_count == 0
        else "LUNA_FIELD_EVENT_TEMPORAL_VALIDITY_PROTOCOL_PLANNING_BLOCKED"
    )
    next_phase = (
        EXPECTED_NEXT
        if blocker_count == 0
        else "Phase-Luna-Field-Event-And-Temporal-Validity-Protocol-Planning-Output-Contract-Correction-v1-001"
    )

    print("CHECKS")
    for c in checks:
        state = "PASS" if c["passed"] else "FAIL"
        print(f"- [{state}] {c['name']}")

    print("FAILED_CHECKS")
    if failed:
        for c in failed:
            print(f"- {c['name']}: {c['detail']}")
    else:
        print("- NONE")

    print("PASSED_CHECK_COUNT")
    print(passed)
    print("FAILED_CHECK_COUNT")
    print(len(failed))
    print("BLOCKER_COUNT")
    print(blocker_count)
    print("FINAL_DECISION")
    print(final_decision)
    print("NEXT")
    print(next_phase)

    raise SystemExit(0 if blocker_count == 0 else 1)


if __name__ == "__main__":
    main()
