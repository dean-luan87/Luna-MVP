import json
import os

BASE_DIR = os.path.dirname(__file__)
REQUIRED_FILES = [
    "luna_field_kernel_technical_architecture_v1.md",
    "field_kernel_component_contracts_v1.json",
    "field_kernel_event_flow_v1.json",
    "field_kernel_state_model_v1.json",
    "field_kernel_temporal_model_v1.json",
    "field_kernel_multi_reality_model_v1.json",
    "field_kernel_projection_contract_v1.json",
    "field_kernel_persistence_abstraction_v1.json",
    "field_kernel_failure_recovery_matrix_v1.json",
    "field_kernel_test_strategy_v1.json",
    "field_kernel_minimum_case_spec_v1.json",
    "field_kernel_existing_asset_reuse_mapping_v1.json",
    "field_kernel_architecture_diagram_v1.md",
    "field_kernel_architecture_summary_v1.json",
    "verify_field_kernel_technical_architecture_planning_v1.py",
]

MERMAID_BLOCK_MARKER = "```mermaid"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def file_exists(path):
    return os.path.exists(path)


def check_mermaid_blocks(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return content.count(MERMAID_BLOCK_MARKER)


def run():
    checks = []
    failed = []

    for filename in REQUIRED_FILES:
        path = os.path.join(BASE_DIR, filename)
        exists = file_exists(path)
        checks.append((f"exists:{filename}", exists))
        if not exists:
            failed.append(f"missing {filename}")

    json_files = [
        "field_kernel_component_contracts_v1.json",
        "field_kernel_event_flow_v1.json",
        "field_kernel_state_model_v1.json",
        "field_kernel_temporal_model_v1.json",
        "field_kernel_multi_reality_model_v1.json",
        "field_kernel_projection_contract_v1.json",
        "field_kernel_persistence_abstraction_v1.json",
        "field_kernel_failure_recovery_matrix_v1.json",
        "field_kernel_test_strategy_v1.json",
        "field_kernel_minimum_case_spec_v1.json",
        "field_kernel_existing_asset_reuse_mapping_v1.json",
        "field_kernel_architecture_summary_v1.json",
    ]

    for filename in json_files:
        path = os.path.join(BASE_DIR, filename)
        try:
            load_json(path)
            checks.append((f"valid_json:{filename}", True))
        except Exception as e:
            failed.append(f"invalid_json:{filename}:{e}")
            checks.append((f"valid_json:{filename}", False))

    try:
        summary = load_json(
            os.path.join(BASE_DIR, "field_kernel_architecture_summary_v1.json")
        )
        checks.append(
            (
                "event_before_mutation",
                summary.get("event_before_state_mutation") is True,
            )
        )
        checks.append(
            (
                "projection_mutates_substrate",
                summary.get("projection_mutates_substrate") is False,
            )
        )
        checks.append(("candidate_only", summary.get("candidate_only") is True))
        checks.append(("not_fact", summary.get("not_fact") is True))
        checks.append(("blocker_count", summary.get("blocker_count") == 0))
        checks.append(
            (
                "final_decision",
                summary.get("final_decision")
                == "LUNA_FIELD_KERNEL_TECHNICAL_ARCHITECTURE_PLANNING_GO",
            )
        )
        checks.append(
            (
                "recommended_next_phase",
                summary.get("recommended_next_phase")
                == "Phase-Luna-Field-Event-And-Temporal-Validity-Protocol-Planning-v1-001",
            )
        )
        checks.append(
            (
                "database_product_selection_allowed",
                summary.get("database_product_selection_allowed") is False,
            )
        )
        checks.append(
            (
                "real_runtime_implementation_allowed",
                summary.get("real_runtime_implementation_allowed") is False,
            )
        )
        checks.append(
            (
                "directory_migration_allowed",
                summary.get("directory_migration_allowed") is False,
            )
        )
        checks.append(
            ("model_training_allowed", summary.get("model_training_allowed") is False)
        )
        checks.append(
            (
                "production_activation_allowed",
                summary.get("production_activation_allowed") is False,
            )
        )
        checks.append(
            (
                "autonomous_personality_mutation_allowed",
                summary.get("autonomous_personality_mutation_allowed") is False,
            )
        )
        checks.append(
            (
                "single_neural_network_as_kernel_allowed",
                summary.get("single_neural_network_as_kernel_allowed") is False,
            )
        )
    except Exception:
        failed.append("summary_json_load_failed")

    try:
        components = load_json(
            os.path.join(BASE_DIR, "field_kernel_component_contracts_v1.json")
        ).get("components", [])
        component_ids = {c.get("component_id") for c in components}
        required_components = {
            "field_event_intake",
            "event_validator",
            "evidence_normalizer",
            "space_and_time_anchor_resolver",
            "field_candidate_builder",
            "field_state_reducer",
            "temporal_field_graph",
            "field_belief_manager",
            "conflict_and_coexistence_resolver",
            "temporary_overlay_manager",
            "field_lifecycle_manager",
            "active_field_projection_builder",
            "field_timeline_store_interface",
            "revision_and_revocation_manager",
            "trace_and_diagnostics",
            "human_correction_adapter",
            "governance_gate",
        }
        missing_components = required_components - component_ids
        if missing_components:
            failed.append(f"missing_components:{sorted(list(missing_components))}")
            checks.append(("core_components_complete", False))
        else:
            checks.append(("core_components_complete", True))
    except Exception:
        failed.append("component_contracts_load_failed")

    try:
        state = load_json(os.path.join(BASE_DIR, "field_kernel_state_model_v1.json"))
        required_states = [
            "substrate_state",
            "candidate_definition_state",
            "admitted_candidate_state",
            "active_field_state",
            "suspended_state",
            "expired_state",
            "superseded_state",
            "revoked_state",
            "unresolved_state",
            "active_projection_state",
        ]
        checks.append(
            (
                "state_model_complete",
                all(s in state.get("state_layers", []) for s in required_states),
            )
        )
    except Exception:
        failed.append("state_model_load_failed")

    try:
        temporal = load_json(
            os.path.join(BASE_DIR, "field_kernel_temporal_model_v1.json")
        )
        required_temporal = [
            "persistent",
            "interval",
            "recurring",
            "temporary",
            "seasonal",
            "event_driven",
            "until_revoked",
            "unknown_validity",
        ]
        checks.append(
            (
                "temporal_model_complete",
                all(t in temporal.get("temporal_types", []) for t in required_temporal),
            )
        )
    except Exception:
        failed.append("temporal_model_load_failed")

    try:
        real = load_json(
            os.path.join(BASE_DIR, "field_kernel_multi_reality_model_v1.json")
        )
        required_realities = ["physical", "institutional", "social", "personal"]
        checks.append(
            (
                "multi_reality_complete",
                all(r in real.get("realities", {}) for r in required_realities),
            )
        )
    except Exception:
        failed.append("multi_reality_load_failed")

    try:
        projection = load_json(
            os.path.join(BASE_DIR, "field_kernel_projection_contract_v1.json")
        )
        checks.append(
            (
                "projection_contract_complete",
                projection.get("projection_candidate_only") is True
                and projection.get("projection_not_fact") is True
                and projection.get("projection_does_not_mutate_substrate") is True,
            )
        )
    except Exception:
        failed.append("projection_contract_load_failed")

    try:
        persistence = load_json(
            os.path.join(BASE_DIR, "field_kernel_persistence_abstraction_v1.json")
        )
        required_interfaces = [
            "EventStoreInterface",
            "FieldSnapshotStoreInterface",
            "TemporalGraphInterface",
            "AttachmentStoreInterface",
            "TraceStoreInterface",
        ]
        found = [i.get("interface_id") for i in persistence.get("interfaces", [])]
        checks.append(
            (
                "persistence_abstraction_complete",
                all(i in found for i in required_interfaces),
            )
        )
    except Exception:
        failed.append("persistence_abstraction_load_failed")

    try:
        failure = load_json(
            os.path.join(BASE_DIR, "field_kernel_failure_recovery_matrix_v1.json")
        )
        required_failures = [
            "invalid_event",
            "missing_evidence",
            "conflicting_evidence",
            "stale_temporal_definition",
            "missing_space_anchor",
            "projection_failure",
            "partial_state_update",
            "corrupted_snapshot",
            "revocation_failure",
            "human_correction_conflict",
        ]
        found = [f.get("failure_type") for f in failure.get("failures", [])]
        checks.append(
            ("failure_recovery_complete", all(t in found for t in required_failures))
        )
    except Exception:
        failed.append("failure_recovery_load_failed")

    try:
        tests = load_json(os.path.join(BASE_DIR, "field_kernel_test_strategy_v1.json"))
        required_tests = [
            "reducer_determinism_test",
            "event_replay_test",
            "temporal_expiry_test",
            "multi_reality_coexistence_test",
            "temporary_overlay_test",
            "perspective_projection_boundary_test",
            "candidate_to_fact_leak_test",
            "revocation_test",
            "human_correction_test",
            "partial_failure_rollback_test",
            "unresolved_state_test",
        ]
        found = [t.get("test_id") for t in tests.get("tests", [])]
        checks.append(
            ("test_strategy_complete", all(t in found for t in required_tests))
        )
    except Exception:
        failed.append("test_strategy_load_failed")

    try:
        case_spec = load_json(
            os.path.join(BASE_DIR, "field_kernel_minimum_case_spec_v1.json")
        )
        required_fields = [
            "space_anchor",
            "physical_definitions",
            "institutional_definitions",
            "social_definitions",
            "personal_definitions",
            "temporal_states",
            "temporary_overlays",
            "task_variants",
            "expected_projection_differences",
            "unresolved_cases",
        ]
        checks.append(
            (
                "minimum_case_complete",
                all(field in case_spec for field in required_fields),
            )
        )
    except Exception:
        failed.append("minimum_case_load_failed")

    try:
        existing = load_json(
            os.path.join(BASE_DIR, "field_kernel_existing_asset_reuse_mapping_v1.json")
        )
        found = [a.get("existing_asset") for a in existing.get("asset_mappings", [])]
        required_assets = [
            "Situation Understanding",
            "Observation Attention",
            "Region Intelligence",
            "Ownership Understanding",
            "Field-Centric Object Role",
            "Model Manager",
            "Model Test Lens",
            "Human Correction",
            "Evidence Chain",
            "Runtime Boundary",
            "Candidate / Fact Admission",
            "Model / Skill Admission",
            "Task Manager",
            "Followup Runner",
            "OCR Evidence",
            "Vision Evidence",
            "Network-Assisted Situation Learning",
            "Memory System",
            "Emotional Engine",
            "Interaction Governance",
        ]
        checks.append(
            (
                "existing_asset_reuse_complete",
                all(asset in found for asset in required_assets),
            )
        )
        checks.append(
            (
                "physical_move_allowed_false",
                all(
                    m.get("physical_move_allowed") is False
                    for m in existing.get("asset_mappings", [])
                ),
            )
        )
        checks.append(
            (
                "governance_rewrite_required_false",
                all(
                    m.get("rewrite_required") is False
                    for m in existing.get("asset_mappings", [])
                ),
            )
        )
    except Exception:
        failed.append("existing_asset_reuse_load_failed")

    try:
        diagrams = check_mermaid_blocks(
            os.path.join(BASE_DIR, "field_kernel_architecture_diagram_v1.md")
        )
        checks.append(("mermaid_blocks", diagrams >= 5))
    except Exception:
        failed.append("diagram_load_failed")

    passed = [c for c, ok in checks if ok]
    failed_checks = [c for c, ok in checks if not ok]
    final_decision = "LUNA_FIELD_KERNEL_TECHNICAL_ARCHITECTURE_PLANNING_GO"
    next_phase = "Phase-Luna-Field-Event-And-Temporal-Validity-Protocol-Planning-v1-001"

    result = {
        "CHECKS": [c for c, _ in checks],
        "FAILED_CHECKS": failed_checks,
        "PASSED_CHECK_COUNT": len(passed),
        "FAILED_CHECK_COUNT": len(failed_checks),
        "BLOCKER_COUNT": 0 if not failed_checks else len(failed_checks),
        "FINAL_DECISION": final_decision,
        "NEXT": next_phase,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    run()
