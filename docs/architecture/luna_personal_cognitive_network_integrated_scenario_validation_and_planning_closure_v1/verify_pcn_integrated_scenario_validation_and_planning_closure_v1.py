#!/usr/bin/env python3
"""Final verifier for the PCN integrated planning-closure phase.

This verifier is intentionally read-only and standard-library-only.  It validates
planning assets and derives the closure decision from the evidence recorded in
those assets; it does not execute a PCN, Runtime, model, graph, or persistence
operation.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


BASE = Path(__file__).absolute().parent
REPO = Path.cwd()
PCN_PLANNING = REPO / "docs/architecture/luna_personal_cognitive_network_planning_v1"
ALIGNMENT = REPO / "docs/architecture/luna_personal_cognitive_network_field_role_interaction_alignment_v1"

REQUIRED_FILES = {
    "pcn_integrated_cognitive_flow_model_candidate.json",
    "pcn_integrated_state_model_candidate.json",
    "pcn_integrated_scenario_suite_candidate.json",
    "cognitive_interaction_kernel_integrated_validation.json",
    "pcn_nested_constraint_closure_review.json",
    "pcn_planning_conflict_matrix.json",
    "pcn_planning_closure_decision_candidate.json",
    "pcn_open_questions_registry.json",
    "pcn_integrated_architecture_risk_review.md",
    "pcn_integrated_scenario_validation_and_planning_closure_summary.md",
    "pcn_integrated_planning_closure_change_manifest.json",
    "phase_contract.json",
    "verify_pcn_integrated_scenario_validation_and_planning_closure_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "pcn_integrated_architecture_risk_review.md",
    "pcn_integrated_scenario_validation_and_planning_closure_summary.md",
    "verify_pcn_integrated_scenario_validation_and_planning_closure_v1.py",
}

EXPECTED_SCENARIOS = {
    "SCENARIO_01_SIMPLE_WEATHER_QUERY",
    "SCENARIO_02_TEMPORARY_OVERTIME_AT_HOME",
    "SCENARIO_03_LONG_TERM_OVERTIME_AT_HOME",
    "SCENARIO_04_SPOUSES_AND_COLLEAGUES",
    "SCENARIO_05_DIVORCED_BUT_STILL_COLLEAGUES",
    "SCENARIO_06_MEETING_HISTORICAL_REACTIVATION",
    "SCENARIO_07_SAME_TYPE_WORK_FIELD_RESONANCE",
    "SCENARIO_08_FATHER_VS_EMPLOYEE",
    "SCENARIO_09_SPOUSES_BUILD_BUSINESS",
    "SCENARIO_10_DORMANT_OLD_FRIEND_REACTIVATION",
    "SCENARIO_11_SUBJECTIVE_WRONG_CAUSAL_ASSOCIATION",
    "SCENARIO_12_RESOURCE_DEGRADATION",
}

EXPECTED_CONFLICT_AREAS = {
    "Object Model",
    "Link Model",
    "Activation",
    "Growth",
    "Dormancy",
    "Subjective Cognition",
    "Resource Constraint",
    "Nested Constraints",
    "Scenario Model",
    "Context Handoff",
    "Memory Boundary",
    "Causal Boundary",
}

EXPECTED_NESTED_RELATIONS = {
    "Context_to_PCN",
    "Field_to_Role",
    "Role_to_Relationship",
    "Memory_to_PCN",
    "Resource_to_PCN",
    "Observation_Axis_to_Interaction",
    "PCN_to_Interaction",
    "Emotion_to_Interaction",
    "Intent_to_PCN",
    "Causal_to_PCN",
    "Experience_to_PCN",
    "Decision_to_Interaction",
}


def load_json(name: str) -> dict:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_file_hashes(directory: Path) -> dict[str, str]:
    return {
        path.name: sha256(path)
        for path in sorted(directory.iterdir())
        if path.is_file()
    }


def imported_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def main() -> int:
    failed: list[str] = []
    check_count = 0

    def check(condition: bool, name: str) -> None:
        nonlocal check_count
        check_count += 1
        if not condition:
            failed.append(name)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "required_file_set")

    documents: dict[str, dict] = {}
    for name in sorted(JSON_FILES):
        try:
            documents[name] = load_json(name)
            check(True, f"json_parse_{name}")
        except (OSError, UnicodeError, json.JSONDecodeError):
            documents[name] = {}
            check(False, f"json_parse_{name}")

    for name in (
        "pcn_integrated_architecture_risk_review.md",
        "pcn_integrated_scenario_validation_and_planning_closure_summary.md",
    ):
        text = (BASE / name).read_text(encoding="utf-8") if (BASE / name).exists() else ""
        check(bool(text.strip()), f"markdown_nonempty_{name}")

    verifier_source = Path(__file__).read_text(encoding="utf-8")
    try:
        verifier_tree = ast.parse(verifier_source)
        check(True, "verifier_ast_parse")
    except SyntaxError:
        verifier_tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast_parse")
    allowed_imports = {"__future__", "ast", "hashlib", "json", "pathlib"}
    check(imported_roots(verifier_tree) <= allowed_imports, "verifier_standard_library_only")

    phase = documents.get("phase_contract.json", {})
    manifest = documents.get("pcn_integrated_planning_closure_change_manifest.json", {})
    flow = documents.get("pcn_integrated_cognitive_flow_model_candidate.json", {})
    state = documents.get("pcn_integrated_state_model_candidate.json", {})
    suite = documents.get("pcn_integrated_scenario_suite_candidate.json", {})
    kernel = documents.get("cognitive_interaction_kernel_integrated_validation.json", {})
    nested = documents.get("pcn_nested_constraint_closure_review.json", {})
    conflicts = documents.get("pcn_planning_conflict_matrix.json", {})
    questions = documents.get("pcn_open_questions_registry.json", {})
    closure = documents.get("pcn_planning_closure_decision_candidate.json", {})

    for name, document in documents.items():
        if name != "phase_contract.json":
            check(document.get("status") == "PLANNING_CANDIDATE", f"planning_status_{name}")

    expected_forward = [
        "CURRENT_CONTEXT",
        "FIELD_ROLE_ACTIVATION",
        "RELATED_RELATIONSHIP_ACTIVATION",
        "PCN_LOCAL_NETWORK_ACTIVATION",
        "INTERACTION_CANDIDATE",
        "ACTIVE_COGNITIVE_PROJECTION",
        "FUTURE_INTENT_CAUSAL_HANDOFF",
    ]
    check(flow.get("forward_coordination") == expected_forward, "integrated_forward_coordination")
    flow_rules = flow.get("rules", {})
    check(flow_rules.get("single_direction_pipeline") is False, "flow_not_single_pipeline")
    check(flow_rules.get("bidirectional_means_mutual_write") is False, "flow_no_mutual_write")
    check(flow_rules.get("source_owner_precedence") is True, "flow_source_owner_precedence")
    check(flow_rules.get("current_reality_precedence") is True, "flow_reality_precedence")
    check(flow_rules.get("unknown_preserved") is True, "flow_unknown_preserved")
    check(flow_rules.get("interaction_output_is_candidate_only") is True, "flow_interaction_candidate_only")
    check(flow_rules.get("future_handoff_is_runtime") is False, "flow_future_handoff_inactive")
    flow_relations = flow.get("nested_relations", [])
    check(len(flow_relations) == 8, "flow_nested_relation_count")
    check(all(item.get("source_mutation_allowed") is False for item in flow_relations), "flow_nested_no_source_mutation")
    future_relations = flow.get("future_nested_relations", [])
    check(len(future_relations) == 4, "flow_future_relation_count")
    check(all(item.get("status") == "INACTIVE_FUTURE_HANDOFF" and item.get("mutual_write") is False for item in future_relations), "flow_future_relations_inactive")
    check(flow.get("candidate_only") is True, "flow_candidate_only")
    check(flow.get("runtime_implemented") is False and flow.get("skeleton_implemented") is False, "flow_no_implementation")

    expected_state_groups = {
        "FIELD_STATE": {"CORE_ACTIVE", "SECONDARY_ACTIVE", "TEMPORARILY_OCCUPIED", "HISTORICAL", "DORMANT_REFERENCE"},
        "ROLE_STATE": {"PRIMARY_ACTIVE", "SECONDARY_ACTIVE", "WEAK_ACTIVE", "DORMANT", "REACTIVATED"},
        "RELATIONSHIP_STATE": {"ACTIVE", "HISTORICAL", "DORMANT", "REACTIVATED", "MULTI_RELATION_COEXISTING"},
        "PCN_LINK_STATE": {"ACTIVE", "WEAK", "DORMANT", "REACTIVATED"},
        "INTERACTION_STATE": {"RESONANCE", "COMPETITION", "OCCUPATION", "OVERLAP", "COEXISTENCE", "FUSION_CANDIDATE", "HISTORICAL_REACTIVATION"},
    }
    state_groups = state.get("state_groups", {})
    check(set(state_groups) == set(expected_state_groups), "state_group_names")
    for group, expected_values in expected_state_groups.items():
        check(set(state_groups.get(group, [])) == expected_values, f"state_values_{group}")
    semantics = state.get("semantics", {})
    check(semantics.get("planning_expression_candidates") is True, "state_planning_expressions")
    check(semantics.get("fixed_fsm_enforcement") is False, "state_no_fixed_fsm")
    check(semantics.get("automatic_transition") is False, "state_no_automatic_transition")
    check(semantics.get("fixed_time_threshold") is False, "state_no_fixed_threshold")
    check(semantics.get("state_implies_source_mutation") is False, "state_no_source_mutation")
    check(semantics.get("multiple_states_may_coexist") is True, "state_coexistence")
    check(semantics.get("transition_requires_context_resource_evidence_and_owner_review") is True, "state_transition_governed")
    check(state.get("candidate_only") is True and state.get("active_schema") is False and state.get("runtime_implemented") is False, "state_planning_only")

    scenarios = suite.get("scenarios", [])
    scenario_by_id = {item.get("scenario_id"): item for item in scenarios if isinstance(item, dict)}
    check(set(scenario_by_id) == EXPECTED_SCENARIOS, "scenario_id_set")
    check(suite.get("scenario_count") == 12 == len(scenarios), "scenario_count")
    scenario_all_pass = len(scenarios) == 12 and all(item.get("validation", {}).get("passes") is True for item in scenarios)
    check(scenario_all_pass, "scenario_suite_all_pass")
    check(all(item.get("expected_candidates") and item.get("forbidden_results") for item in scenarios), "scenario_expectations_and_guards")

    s1 = scenario_by_id.get("SCENARIO_01_SIMPLE_WEATHER_QUERY", {})
    check(s1.get("validation", {}).get("minimum_sufficient_expansion") is True, "scenario_simple_minimum_expansion")
    s2 = scenario_by_id.get("SCENARIO_02_TEMPORARY_OVERTIME_AT_HOME", {})
    check(s2.get("validation", {}).get("multi_field_coexistence") is True, "scenario_temporary_multi_field")
    check(s2.get("validation", {}).get("multi_role_coexistence") is True, "scenario_temporary_multi_role")
    check(s2.get("validation", {}).get("temporary_occupation_not_structural") is True, "scenario_temporary_not_structural")
    s3 = scenario_by_id.get("SCENARIO_03_LONG_TERM_OVERTIME_AT_HOME", {})
    check(s3.get("validation", {}).get("repeated_occupation_candidate") is True, "scenario_repeated_occupation_candidate")
    check(s3.get("validation", {}).get("structural_change_requires_later_governance") is True, "scenario_structural_change_governed")
    check(s3.get("validation", {}).get("fixed_threshold_forbidden") is True, "scenario_no_fixed_threshold")
    s4 = scenario_by_id.get("SCENARIO_04_SPOUSES_AND_COLLEAGUES", {})
    check(s4.get("validation", {}).get("person_pair_not_duplicated") is True, "scenario_person_pair_not_duplicated")
    check(s4.get("validation", {}).get("multi_relationship_coexistence") is True, "scenario_multi_relationship")
    check(s4.get("validation", {}).get("role_projection_varies_by_field") is True, "scenario_role_projection_by_field")
    s5 = scenario_by_id.get("SCENARIO_05_DIVORCED_BUT_STILL_COLLEAGUES", {})
    check(s5.get("validation", {}).get("relation_state_separation") is True, "scenario_relationship_state_separation")
    check(s5.get("validation", {}).get("ended_relationship_not_deleted") is True, "scenario_ended_relationship_retained")
    check(s5.get("validation", {}).get("future_emotion_only") is True, "scenario_emotion_future_only")
    s6 = scenario_by_id.get("SCENARIO_06_MEETING_HISTORICAL_REACTIVATION", {})
    check(s6.get("validation", {}).get("current_colleague_reality_precedence") is True, "scenario_historical_reality_precedence")
    check(s6.get("validation", {}).get("historical_projection_only") is True, "scenario_historical_projection_only")
    check(s6.get("validation", {}).get("no_emotion_or_causal_conclusion") is True, "scenario_no_emotion_causal_conclusion")
    s7 = scenario_by_id.get("SCENARIO_07_SAME_TYPE_WORK_FIELD_RESONANCE", {})
    check(s7.get("validation", {}).get("role_relationship_task_benefit_cost_history_compared") is True, "scenario_resonance_comparison_dimensions")
    check(s7.get("validation", {}).get("resonance_not_same_outcome") is True, "scenario_resonance_not_outcome")
    check(s7.get("validation", {}).get("resonance_not_causal") is True, "scenario_resonance_not_causal")
    s8 = scenario_by_id.get("SCENARIO_08_FATHER_VS_EMPLOYEE", {})
    check(s8.get("validation", {}).get("multi_field_coexistence") is True, "scenario_competition_multi_field")
    check(s8.get("validation", {}).get("multi_role_coexistence") is True, "scenario_competition_multi_role")
    check(s8.get("validation", {}).get("competition_not_arbitration") is True, "scenario_competition_not_arbitration")
    check(s8.get("validation", {}).get("future_self_decision_arbitration") is True, "scenario_future_arbitration_owner")
    s9 = scenario_by_id.get("SCENARIO_09_SPOUSES_BUILD_BUSINESS", {})
    check(s9.get("validation", {}).get("overlap_allowed") is True, "scenario_overlap_allowed")
    check(s9.get("validation", {}).get("coexistence_allowed") is True, "scenario_coexistence_allowed")
    check(s9.get("validation", {}).get("competition_not_default") is True, "scenario_competition_not_default")
    check(s9.get("validation", {}).get("fusion_candidate_only") is True, "scenario_fusion_candidate_only")
    s10 = scenario_by_id.get("SCENARIO_10_DORMANT_OLD_FRIEND_REACTIVATION", {})
    check(s10.get("validation", {}).get("dormant_not_deleted") is True, "scenario_dormant_not_deleted")
    check(s10.get("validation", {}).get("high_relevance_reactivation") is True, "scenario_dormant_reactivation")
    check(s10.get("validation", {}).get("resource_bounded_history") is True, "scenario_history_resource_bounded")
    s11 = scenario_by_id.get("SCENARIO_11_SUBJECTIVE_WRONG_CAUSAL_ASSOCIATION", {})
    check(s11.get("validation", {}).get("personal_subjective") is True, "scenario_subjective_link_preserved")
    check(s11.get("validation", {}).get("truth_status_not_promoted") is True, "scenario_truth_not_promoted")
    check(s11.get("validation", {}).get("causal_fact_not_generated") is True, "scenario_causal_fact_not_generated")
    check(s11.get("validation", {}).get("strength_not_truth") is True, "scenario_strength_not_truth")
    s12 = scenario_by_id.get("SCENARIO_12_RESOURCE_DEGRADATION", {})
    check(s12.get("validation", {}).get("high_resource_expands_relevant_scope") is True, "scenario_high_resource_scope")
    check(s12.get("validation", {}).get("low_resource_shrinks_active_scope") is True, "scenario_low_resource_scope")
    check(s12.get("validation", {}).get("low_resource_does_not_delete_or_mutate") is True, "scenario_low_resource_no_mutation")

    expected_kernel_inputs = {
        "CONTEXT", "ACTIVE_FIELD", "ACTIVE_ROLE", "RELATIONSHIP",
        "CURRENT_NEED_REFERENCE", "PCN_ACTIVATION", "RESOURCE_CONSTRAINT", "OBSERVATION_AXIS",
    }
    check(set(kernel.get("required_inputs", [])) == expected_kernel_inputs, "kernel_required_inputs")
    check(kernel.get("allowed_outputs") == ["INTERACTION_CANDIDATE"], "kernel_only_interaction_candidate")
    interaction_types = {item.get("type") for item in kernel.get("validated_interactions", [])}
    check(interaction_types == {"RESONANCE", "COMPETITION", "OCCUPATION", "OVERLAP", "HISTORICAL_REACTIVATION"}, "kernel_interaction_types")
    check(all(item.get("candidate_only") is True for item in kernel.get("validated_interactions", [])), "kernel_interactions_candidate_only")
    owner_separation = kernel.get("owner_separation", {})
    check(owner_separation and all(value is False for value in owner_separation.values()), "kernel_owner_separation")
    kernel_guards = kernel.get("negative_boundaries", {})
    check(kernel_guards and all(value is False for value in kernel_guards.values()), "kernel_negative_boundaries")
    kernel_compatible = kernel.get("validation_result") == "BOUNDARY_COMPATIBLE" and kernel.get("candidate_only") is True
    check(kernel_compatible, "kernel_boundary_compatible")

    nested_relations = nested.get("relations", [])
    check({item.get("relation") for item in nested_relations} == EXPECTED_NESTED_RELATIONS, "nested_relation_set")
    check(nested.get("relation_count") == 12 == len(nested_relations), "nested_relation_count")
    check(all(item.get("feedback_allowed") is True for item in nested_relations), "nested_feedback_allowed")
    check(all(item.get("constraint_allowed") is True for item in nested_relations), "nested_constraint_allowed")
    check(all(item.get("projection_allowed") is True for item in nested_relations), "nested_projection_allowed")
    nested_no_source_mutation = all(item.get("source_mutation_forbidden") is True for item in nested_relations)
    check(nested_no_source_mutation, "nested_source_mutation_forbidden")
    current_count = sum(item.get("lifecycle") == "CURRENT" for item in nested_relations)
    future_count = sum(item.get("lifecycle") == "FUTURE_INACTIVE" for item in nested_relations)
    check(current_count == 7 and future_count == 5, "nested_lifecycle_partition")
    closure_rules = nested.get("closure_rules", {})
    check(closure_rules.get("mutual_influence_means_mutual_write") is False, "nested_no_mutual_write")
    check(closure_rules.get("single_direction_pipeline") is False, "nested_not_single_pipeline")
    check(closure_rules.get("source_owner_precedence") is True, "nested_source_owner_precedence")
    check(closure_rules.get("unique_mutation_owner_per_source_object") is True, "nested_unique_mutation_owner")
    check(closure_rules.get("future_relations_are_active_runtime") is False, "nested_future_inactive")
    check(closure_rules.get("nested_loop_structure_preserved") is True, "nested_loop_preserved")

    conflict_records = conflicts.get("records", [])
    allowed_conflict_statuses = {"COMPATIBLE", "CLARIFICATION_REQUIRED", "BLOCKED"}
    check(set(conflicts.get("allowed_statuses", [])) == allowed_conflict_statuses, "conflict_allowed_statuses")
    check({item.get("area") for item in conflict_records} == EXPECTED_CONFLICT_AREAS, "conflict_area_set")
    computed_counts = {status: sum(item.get("status") == status for item in conflict_records) for status in allowed_conflict_statuses}
    check(conflicts.get("counts") == computed_counts, "conflict_counts_derived")
    conflict_blockers = computed_counts["BLOCKED"]
    check(conflicts.get("blocker_count") == conflict_blockers == 0, "conflict_no_blocker")
    check(conflicts.get("closure_permitted") is (conflict_blockers == 0), "conflict_closure_derived")
    clarifications = [item for item in conflict_records if item.get("status") == "CLARIFICATION_REQUIRED"]
    check(all(item.get("closure_effect") == "NON_BLOCKING_SKELETON_REQUIREMENT" for item in clarifications), "conflict_clarifications_nonblocking")

    allowed_question_classes = {"DEFERRED_IMPLEMENTATION_DETAIL", "BLOCKER"}
    question_records = questions.get("questions", [])
    check(set(questions.get("allowed_classifications", [])) == allowed_question_classes, "question_allowed_classifications")
    check(len(question_records) == 8, "question_count")
    check(len({item.get("question_id") for item in question_records}) == len(question_records), "question_ids_unique")
    check(all(item.get("classification") in allowed_question_classes for item in question_records), "question_classifications_valid")
    computed_question_blockers = sum(item.get("classification") == "BLOCKER" for item in question_records)
    computed_deferred = sum(item.get("classification") == "DEFERRED_IMPLEMENTATION_DETAIL" for item in question_records)
    check(questions.get("blocker_count") == computed_question_blockers == 0, "question_no_blocker")
    check(questions.get("deferred_count") == computed_deferred == 8, "question_deferred_count")
    check(all(item.get("owner_or_boundary_change") is False for item in question_records if item.get("classification") == "DEFERRED_IMPLEMENTATION_DETAIL"), "deferred_questions_no_owner_change")
    classification_rule = questions.get("classification_rule", "")
    check(all(token in classification_rule for token in ("Owner", "Object Model", "Core Boundary", "Source Mutation", "BLOCKER")), "question_blocker_rule")

    stability_checks = closure.get("stability_checks", {})
    check(len(stability_checks) == 12, "closure_stability_check_count")
    stability_all = len(stability_checks) == 12 and all(value is True for value in stability_checks.values())
    check(stability_all, "closure_stability_all_true")
    source_mutation_detected = not nested_no_source_mutation
    second_writer_detected = not bool(closure_rules.get("unique_mutation_owner_per_source_object"))
    derived_inputs = {
        "scenario_suite_all_pass": scenario_all_pass,
        "conflict_matrix_blocker_count": conflict_blockers,
        "open_question_blocker_count": computed_question_blockers,
        "interaction_kernel_boundary_compatible": kernel_compatible,
        "source_mutation_detected": source_mutation_detected,
        "second_writer_detected": second_writer_detected,
    }
    check(closure.get("decision_inputs") == derived_inputs, "closure_inputs_derived")
    ready_for_controlled_skeleton = (
        stability_all
        and scenario_all_pass
        and conflict_blockers == 0
        and computed_question_blockers == 0
        and kernel_compatible
        and not source_mutation_detected
        and not second_writer_detected
    )
    derived_closure_decision = "READY_FOR_CONTROLLED_SKELETON" if ready_for_controlled_skeleton else "REMEDIATION_REQUIRED"
    check(closure.get("decision") == derived_closure_decision, "closure_decision_derived")
    check(closure.get("decision_is_derived_not_hardcoded") is True, "closure_not_hardcoded")
    check(closure.get("readiness_means_authorization") is False, "closure_readiness_not_authorization")
    check(closure.get("implementation_authorized") is False, "closure_no_implementation_authority")
    check(closure.get("skeleton_authorized") is False, "closure_no_skeleton_authority")
    check(closure.get("next_phase_authorized") is False, "closure_no_next_phase_authority")
    check(closure.get("candidate_only") is True, "closure_candidate_only")

    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_file_set")
    check(manifest.get("modified_existing_files") == [], "manifest_no_existing_modification")
    check(manifest.get("code_files_changed") == [], "manifest_no_code_change")
    check(manifest.get("runtime_files_changed") == [], "manifest_no_runtime_change")
    false_flags = (
        "active_schema_changed", "active_contract_changed", "owner_metadata_changed",
        "pcn_runtime_created", "pcn_skeleton_created", "interaction_runtime_created", "causal_runtime_created",
    )
    check(all(manifest.get(flag) is False for flag in false_flags), "manifest_no_active_or_runtime_change")
    check(manifest.get("manifest_scope") == "ADDITIVE_PLANNING_CLOSURE_ASSETS_ONLY", "manifest_scope")
    try:
        actual_pcn_hashes = direct_file_hashes(PCN_PLANNING)
        check(manifest.get("protected_pcn_planning_hashes") == actual_pcn_hashes, "protected_pcn_planning_hashes")
    except OSError:
        check(False, "protected_pcn_planning_hashes")
    try:
        actual_alignment_hashes = direct_file_hashes(ALIGNMENT)
        check(manifest.get("protected_alignment_hashes") == actual_alignment_hashes, "protected_alignment_hashes")
    except OSError:
        check(False, "protected_alignment_hashes")

    expected_phase = "Phase-Luna-Personal-Cognitive-Network-Integrated-Scenario-Validation-And-Planning-Closure-v1-001"
    check(phase.get("phase") == expected_phase, "phase_identity")
    check(phase.get("stage") == "PCN Integrated Scenario Validation And Planning Closure", "phase_stage")
    check(phase.get("execution_mode") == "Planning Only", "phase_execution_mode")
    check(phase.get("previous_phase") == "Phase-Luna-Personal-Cognitive-Network-Field-Role-Interaction-Alignment-v1-001", "phase_previous")
    check(phase.get("previous_phase_decision") == "LUNA_PCN_FIELD_ROLE_INTERACTION_ALIGNMENT_READY", "phase_previous_decision")
    check(set(phase.get("required_final_files", [])) == REQUIRED_FILES, "phase_required_final_files")
    check(phase.get("simulation_only") is True, "phase_simulation_only")
    check(phase.get("implementation_started") is False, "phase_no_implementation")
    check(phase.get("runtime_started") is False, "phase_no_runtime")
    check(phase.get("pcn_skeleton_started") is False, "phase_no_skeleton")
    check(phase.get("next_phase_not_authorized") is True, "phase_no_next_authority")
    check(phase.get("go_declared") is False, "phase_no_go")
    authority = phase.get("verification_authority", {})
    check(authority.get("V0") == "AGENT_STATIC_ONLY", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")
    check(phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop_point")
    expected_command = "python3 docs/architecture/luna_personal_cognitive_network_integrated_scenario_validation_and_planning_closure_v1/verify_pcn_integrated_scenario_validation_and_planning_closure_v1.py"
    check(phase.get("user_terminal_commands") == [expected_command], "phase_user_terminal_command")
    check(phase.get("expected_success_decision") == "V2_FINAL_VERIFICATION_PASSED", "phase_success_decision")
    check(phase.get("expected_success_readiness") == "LUNA_PCN_INTEGRATED_SCENARIO_VALIDATION_AND_PLANNING_CLOSURE_READY", "phase_success_readiness")
    check(phase.get("expected_next") == "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT", "phase_success_next")
    check(phase.get("expected_failure_decision") == "BLOCKED_BY_VERIFIER_FAILURE", "phase_failure_decision")
    check(phase.get("expected_failure_readiness") == "LUNA_PCN_INTEGRATED_SCENARIO_VALIDATION_AND_PLANNING_CLOSURE_REMEDIATION_REQUIRED", "phase_failure_readiness")
    check(phase.get("expected_failure_next") == "REMEDIATE_REPORTED_FAILURES_ONLY", "phase_failure_next")
    check(len(phase.get("completion_report_format", [])) >= 20, "phase_completion_report_complete")
    for reference in phase.get("input_assets", []) + phase.get("required_pre_read", []):
        check((REPO / reference).exists(), f"reference_exists_{reference}")

    risk_text = (BASE / "pcn_integrated_architecture_risk_review.md").read_text(encoding="utf-8")
    numbered_risks = [line for line in risk_text.splitlines() if line.lstrip().split(".", 1)[0].isdigit() and "." in line]
    check(len(numbered_risks) == 13, "risk_review_thirteen_risks")
    risk_tokens = (
        "Knowledge Graph", "fixed FSM", "Field", "Role", "relationships", "Interaction",
        "Resonance", "Resource", "Dormancy", "Subjective", "pipeline", "second Writer", "structural expansion",
    )
    check(all(token in risk_text for token in risk_tokens), "risk_review_required_topics")
    check("DEFERRED_IMPLEMENTATION_DETAIL" in risk_text and "blocker" in risk_text.lower(), "risk_review_residual_classification")

    summary_text = (BASE / "pcn_integrated_scenario_validation_and_planning_closure_summary.md").read_text(encoding="utf-8")
    summary_tokens = (
        "READY_FOR_CONTROLLED_SKELETON", "not implementation authorization", "Twelve scenario results",
        "Multi", "Temporary Occupation", "Resonance", "Historical Reactivation", "Dormancy",
        "Subjective Cognition", "Resource Degradation", "Interaction Kernel", "Nested Constraints",
        "zero `BLOCKED`", "zero open-question blockers", "waits for user-terminal V2",
    )
    check(all(token in summary_text for token in summary_tokens), "summary_required_topics")
    check(all(str(index) + "." in summary_text for index in range(1, 13)), "summary_twelve_scenarios")
    check("Runtime" in summary_text and "Skeleton" in summary_text and "source mutation" in summary_text, "summary_negative_boundary")

    passed_count = check_count - len(failed)
    blocker_count = len(failed)
    if failed:
        final_decision = "BLOCKED_BY_VERIFIER_FAILURE"
        readiness = "LUNA_PCN_INTEGRATED_SCENARIO_VALIDATION_AND_PLANNING_CLOSURE_REMEDIATION_REQUIRED"
        next_step = "REMEDIATE_REPORTED_FAILURES_ONLY"
    else:
        final_decision = "V2_FINAL_VERIFICATION_PASSED"
        readiness = "LUNA_PCN_INTEGRATED_SCENARIO_VALIDATION_AND_PLANNING_CLOSURE_READY"
        next_step = "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"

    print(f"CHECKS: {check_count}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {passed_count}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {blocker_count}")
    print(f"FINAL_DECISION: {final_decision}")
    print(f"READINESS: {readiness}")
    print(f"NEXT: {next_step}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
