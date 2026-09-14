#!/usr/bin/env python3
"""Read-only V2 verifier for Intent Architecture Planning v1.

This verifier validates phase-local planning artifacts and referenced asset
existence.  It does not import Luna runtime code, activate contracts, or mutate
the repository.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


PHASE_DIR = Path(__file__).resolve().parent
WORKSPACE = PHASE_DIR.parents[2]

REQUIRED_FILES = {
    "intent_architecture_plan_v1.md",
    "intent_concept_boundary_matrix_v1.json",
    "intent_owner_boundary_candidate_v1.json",
    "potential_intent_schema_candidate_v1.json",
    "intent_candidate_schema_v1.json",
    "intent_state_model_candidate_v1.json",
    "intent_formation_contract_candidate_v1.json",
    "intent_competition_coexistence_model_candidate_v1.json",
    "intent_temporary_dominance_model_candidate_v1.json",
    "intent_carryover_model_candidate_v1.json",
    "intent_self_influence_boundary_candidate_v1.json",
    "intent_field_role_relationship_boundary_candidate_v1.json",
    "intent_emotion_influence_boundary_candidate_v1.json",
    "intent_memory_experience_boundary_candidate_v1.json",
    "intent_resource_constraint_model_candidate_v1.json",
    "intent_nested_constraint_model_candidate_v1.json",
    "intent_to_causal_handoff_contract_candidate_v1.json",
    "intent_minimum_scenario_suite_v1.json",
    "intent_existing_asset_reuse_mapping_v1.json",
    "intent_architecture_risk_review_v1.md",
    "intent_open_questions_registry_v1.json",
    "intent_planning_change_manifest_v1.json",
    "phase_contract.json",
    "verify_intent_architecture_planning_v1.py",
}

JSON_FILES = sorted(name for name in REQUIRED_FILES if name.endswith(".json"))


def load_json(name: str) -> dict[str, Any]:
    with (PHASE_DIR / name).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a JSON object")
    return value


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, name: str) -> None:
        checks.append(name)
        if not condition:
            failures.append(name)

    actual_files = {path.name for path in PHASE_DIR.iterdir() if path.is_file()}
    for filename in sorted(REQUIRED_FILES):
        check(filename in actual_files, f"file_{filename}")
    check(actual_files == REQUIRED_FILES, "phase_file_set_exact")

    documents: dict[str, dict[str, Any]] = {}
    for filename in JSON_FILES:
        try:
            documents[filename] = load_json(filename)
            check(True, f"json_parse_{filename}")
        except (OSError, ValueError, TypeError):
            documents[filename] = {}
            check(False, f"json_parse_{filename}")

    phase = documents["phase_contract.json"]
    check(phase.get("phase") == "Phase-Luna-Intent-Architecture-Planning-v1-001", "phase_identity")
    check(phase.get("stage") == "Intent Architecture Planning", "phase_stage")
    check(phase.get("execution_mode") == "Planning Only", "phase_execution_mode")
    check(phase.get("execution_profile") == "Architecture Planning / Contract Candidate Only", "phase_execution_profile")
    check(phase.get("previous_phase") == "Phase-Luna-Personal-Cognitive-Network-Module-Closure-v1-001", "phase_previous")
    check(phase.get("previous_phase_decision") == "PCN_MODULE_CLOSURE_VERIFIED", "phase_previous_decision")
    check(phase.get("owner") == "Intent Governance", "phase_owner")
    check(set(phase.get("required_final_files", [])) == REQUIRED_FILES, "phase_required_files")
    authority = phase.get("verification_authority", {})
    check(authority.get("V0") == "AGENT_STATIC_ONLY", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")
    check(phase.get("agent_stop_status") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop_status")
    check(phase.get("next_phase_not_automatically_authorized") is True, "phase_no_auto_next")
    check(phase.get("expected_success_readiness") == "LUNA_INTENT_ARCHITECTURE_PLANNING_READY", "phase_success_readiness")

    manifest = documents["intent_planning_change_manifest_v1.json"]
    check(manifest.get("change_scope") == "NEW_PHASE_DIRECTORY_ONLY", "manifest_scope")
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_files")
    for field in (
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "runtime_changes",
        "active_schema_changes",
        "active_contract_changes",
        "owner_metadata_changes",
        "implementation_modules_created",
    ):
        check(manifest.get(field) == [], f"manifest_empty_{field}")
    check(manifest.get("final_verifier_executed_by_agent") is False, "manifest_verifier_authority")

    plan_text = (PHASE_DIR / "intent_architecture_plan_v1.md").read_text(encoding="utf-8")
    plan_topics = [
        "subjective",
        "future-oriented",
        "directional",
        "state-changing tendency",
        "Potential Intent Candidate",
        "Intent Governance",
        "Multiple Intent candidates",
        "Temporary dominance",
        "Field or Context transition does not terminate Intent",
        "Mental Field Continuity",
        "Strength, confidence, priority, and truth",
        "Intent-to-Causal Handoff Candidate",
        "Intent is not an Action",
        "No fixed duration",
        "No existing asset",
    ]
    for index, topic in enumerate(plan_topics, start=1):
        check(topic.lower() in plan_text.lower(), f"plan_topic_{index:02d}")

    matrix = documents["intent_concept_boundary_matrix_v1.json"]
    boundaries = matrix.get("boundaries", [])
    boundary_by_concept = {item.get("concept"): item for item in boundaries}
    expected_concepts = {
        "Need",
        "Drive",
        "Desire",
        "Goal",
        "Task",
        "Attention",
        "Emotion",
        "PCN Activation",
        "Strong Cognitive Link",
        "Repeated Activation",
        "Field Pressure",
        "Role Obligation",
        "Decision",
        "Action",
    }
    check(set(boundary_by_concept) == expected_concepts, "concept_matrix_complete")
    check(all(item.get("is_intent") is False for item in boundaries), "concepts_not_intent")
    check(all(item.get("owner_independent") is True for item in boundaries), "concept_owner_independence")
    check(all(bool(item.get("non_equivalence")) for item in boundaries), "concept_non_equivalence")

    owner = documents["intent_owner_boundary_candidate_v1.json"]
    check(owner.get("canonical_owner") == "Intent Governance", "owner_canonical")
    check(owner.get("unique_owner") is True, "owner_unique")
    expected_owned = {
        "Potential Intent Candidate",
        "Intent Candidate",
        "Intent State Candidate",
        "Intent Interaction Candidate",
        "Intent Trace Candidate",
    }
    check(set(owner.get("owned_candidate_types", [])) == expected_owned, "owner_candidate_types")
    forbidden_owners = set(owner.get("forbidden_ownership", []))
    for forbidden in ("Context", "Personal Cognitive Network", "Self", "Memory", "Emotion", "Causal", "Decision", "Action", "Task", "Runtime", "Reality"):
        check(forbidden in forbidden_owners, f"owner_forbidden_{forbidden.lower().replace(' ', '_')}")
    check(owner.get("active_owner_metadata_changed") is False, "owner_metadata_unchanged")

    potential = documents["potential_intent_schema_candidate_v1.json"]
    potential_required = set(potential.get("required", []))
    for field in ("source_refs", "context_refs", "pcn_refs", "why_candidate", "supporting_refs", "uncertainty", "alternative_candidates", "provenance", "formation_trace", "resource_constraint_ref"):
        check(field in potential_required, f"potential_required_{field}")
    potential_guards = potential.get("planning_guards", {})
    check(potential_guards.get("insufficient_evidence_preserved") is True, "potential_insufficient_evidence")
    check(potential_guards.get("automatic_promotion_forbidden") is True, "potential_no_auto_promotion")
    check(potential_guards.get("context_does_not_create_intent") is True, "potential_no_context_creation")
    check(potential_guards.get("pcn_does_not_create_intent") is True, "potential_no_pcn_creation")
    check(potential_guards.get("active_schema") is False, "potential_not_active")

    candidate = documents["intent_candidate_schema_v1.json"]
    candidate_required = set(candidate.get("required", []))
    for field in ("direction_candidate", "future_state_relation", "strength_candidate", "confidence_candidate", "priority_candidate", "truth_status", "uncertainty", "provenance", "formation_trace", "carryover_candidate"):
        check(field in candidate_required, f"candidate_required_{field}")
    dimensions = candidate.get("dimension_independence", {})
    check(all(value is True for value in dimensions.values()), "candidate_dimensions_independent")
    check(candidate.get("active_schema") is False, "candidate_not_active")

    state_model = documents["intent_state_model_candidate_v1.json"]
    expected_states = {"UNKNOWN", "POTENTIAL", "FORMING", "ACTIVE_CANDIDATE", "SUPPRESSED", "DORMANT", "REACTIVATED", "RESOLVED_CANDIDATE", "ABANDONED_CANDIDATE"}
    actual_states = {item.get("state") for item in state_model.get("state_candidates", [])}
    check(actual_states == expected_states, "state_candidates_complete")
    check(state_model.get("model_kind") == "SEMANTIC_STATE_CANDIDATES_NOT_PRODUCTION_ENUM_OR_FSM", "state_not_runtime_fsm")
    not_frozen = set(state_model.get("not_frozen", []))
    check("numeric score thresholds" in not_frozen, "state_no_score_threshold")
    check("fixed duration thresholds" in not_frozen, "state_no_duration_threshold")
    check(state_model.get("guards", {}).get("single_winner_required") is False, "state_no_single_winner")

    formation = documents["intent_formation_contract_candidate_v1.json"]
    check(formation.get("owner") == "Intent Governance", "formation_owner")
    check(formation.get("input_mode") == "SOURCE_OWNED_REFERENCE_ONLY", "formation_reference_only")
    prohibited_sources = set(formation.get("prohibited_source_authority", []))
    for phrase in ("Context creates Intent", "PCN creates Intent", "Field pressure equals Intent", "Role obligation equals Intent", "Memory recall equals Intent", "Emotion creates Intent"):
        check(phrase in prohibited_sources, f"formation_guard_{phrase.lower().replace(' ', '_')}")
    check(formation.get("automatic_promotion") is False, "formation_no_auto_promotion")
    check(formation.get("fixed_score_threshold") is False, "formation_no_threshold")
    check(formation.get("runtime_behavior") is False, "formation_no_runtime")
    check(formation.get("active_contract") is False, "formation_not_active")

    competition = documents["intent_competition_coexistence_model_candidate_v1.json"]
    interaction_types = {item.get("type") for item in competition.get("interaction_candidates", [])}
    expected_interactions = {"COEXISTENCE", "COMPETITION", "CONFLICT", "SUPPRESSION", "AMPLIFICATION", "INHIBITION", "TEMPORARY_DOMINANCE", "REACTIVATION"}
    check(interaction_types == expected_interactions, "competition_interactions_complete")
    competition_guards = competition.get("guards", {})
    check(competition_guards.get("competition_is_decision") is False, "competition_not_decision")
    check(competition_guards.get("temporary_dominance_is_decision") is False, "dominance_not_decision")
    check(competition_guards.get("winner_take_all") is False, "competition_no_winner_take_all")
    check(any("no winner deletion" == item for item in competition.get("preservation_rules", [])), "competition_no_deletion")

    dominance = documents["intent_temporary_dominance_model_candidate_v1.json"]
    dominance_fields = set(dominance.get("dominance_candidate_fields", []))
    for field in ("dominant_candidate_ref", "suppressed_candidate_refs", "source_refs", "context_refs", "release_condition_candidates", "provenance"):
        check(field in dominance_fields, f"dominance_field_{field}")
    check(all(value is False for value in dominance.get("guards", {}).values()), "dominance_guards")

    carryover = documents["intent_carryover_model_candidate_v1.json"]
    carryover_rules = " ".join(carryover.get("core_rules", []))
    check("Field transition does not imply Intent termination" in carryover_rules, "carryover_field_continuity")
    check("Context transition does not imply Intent termination" in carryover_rules, "carryover_context_continuity")
    check(carryover.get("mental_field_continuity_relation", {}).get("merged") is False, "carryover_mental_field_separate")
    check(carryover.get("guards", {}).get("context_switch_forces_termination") is False, "carryover_no_forced_termination")

    self_boundary = documents["intent_self_influence_boundary_candidate_v1.json"]
    check(self_boundary.get("intent_owner") == "Intent Governance", "self_boundary_intent_owner")
    check(self_boundary.get("self_owner") == "Self Layer / Self Governance", "self_boundary_self_owner")
    self_forbidden = " ".join(self_boundary.get("forbidden", []))
    check("Intent mutates Identity" in self_forbidden, "self_no_identity_mutation")
    check("Intent rewrites Constitution" in self_forbidden, "self_no_constitution_mutation")

    field_role = documents["intent_field_role_relationship_boundary_candidate_v1.json"]
    source_names = {item.get("source") for item in field_role.get("source_boundaries", [])}
    check(source_names == {"Field", "Role", "Relationship"}, "field_role_relationship_complete")
    check(all(item.get("cross_write") is False for item in field_role.get("source_boundaries", [])), "field_role_no_cross_write")

    emotion = documents["intent_emotion_influence_boundary_candidate_v1.json"]
    check(emotion.get("integration_status") == "FUTURE_REFERENCE_BOUNDARY_ONLY", "emotion_future_only")
    emotion_forbidden = " ".join(emotion.get("forbidden", []))
    check("Emotion creates Intent" in emotion_forbidden, "emotion_no_creation")
    check("Intent modifies Emotion state directly" in emotion_forbidden, "emotion_no_cross_write")

    memory = documents["intent_memory_experience_boundary_candidate_v1.json"]
    memory_forbidden = " ".join(memory.get("forbidden", []))
    check("Memory recall equals Intent" in memory_forbidden, "memory_not_intent")
    check("Experience pattern equals Intent" in memory_forbidden, "experience_not_intent")
    check("Intent writes Memory" in memory_forbidden, "intent_no_memory_write")
    check("Intent writes Experience" in memory_forbidden, "intent_no_experience_write")

    resource = documents["intent_resource_constraint_model_candidate_v1.json"]
    not_frozen_limits = resource.get("not_frozen", {})
    check(all(value is None for value in not_frozen_limits.values()), "resource_no_fixed_caps")
    resource_preservation = set(resource.get("preservation_requirements", []))
    check({"source references", "dormant candidates", "provenance", "uncertainty"}.issubset(resource_preservation), "resource_preservation")
    resource_forbidden = " ".join(resource.get("forbidden", []))
    check("force a winner" in resource_forbidden, "resource_no_winner")
    check("change truth status because of resource scarcity" in resource_forbidden, "resource_no_truth_change")

    nested = documents["intent_nested_constraint_model_candidate_v1.json"]
    expected_pairs = {"Context ↔ Intent", "PCN ↔ Intent", "Self ↔ Intent", "Field ↔ Intent", "Role ↔ Intent", "Relationship ↔ Intent", "Memory Reference ↔ Intent", "Emotion Reference ↔ Intent", "Resource ↔ Intent", "Future Causal ↔ Intent", "Future Decision ↔ Intent"}
    actual_pairs = {item.get("pair") for item in nested.get("nested_relations", [])}
    check(actual_pairs == expected_pairs, "nested_relations_complete")
    check(all(item.get("cross_write") is False for item in nested.get("nested_relations", [])), "nested_no_cross_write")
    nested_rules = set(nested.get("core_rules", []))
    check("Owner independence does not mean isolation" in nested_rules, "nested_independence_not_isolation")
    check("Influence does not grant mutation authority" in nested_rules, "nested_influence_not_authority")

    handoff = documents["intent_to_causal_handoff_contract_candidate_v1.json"]
    check(handoff.get("producer_owner") == "Intent Governance", "handoff_producer")
    check(handoff.get("consumer_owner") == "Causal Governance", "handoff_consumer")
    required_payload = set(handoff.get("required_payload", []))
    for field in ("intent_candidate_refs", "competition_refs", "suppression_refs", "context_refs", "pcn_refs", "resource_ref", "provenance", "uncertainty"):
        check(field in required_payload, f"handoff_payload_{field}")
    forbidden_output = set(handoff.get("forbidden_output", []))
    for value in ("causal explanation", "selected Decision", "Action command", "Task creation", "Runtime instruction"):
        check(value in forbidden_output, f"handoff_forbidden_{value.lower().replace(' ', '_')}")
    check(handoff.get("consumer_mutation_authority_over_intent") is False, "handoff_no_consumer_mutation")
    check(handoff.get("active_contract") is False, "handoff_not_active")

    scenarios_doc = documents["intent_minimum_scenario_suite_v1.json"]
    scenarios = scenarios_doc.get("scenarios", [])
    check(scenarios_doc.get("scenario_count") == 12, "scenario_declared_count")
    check(len(scenarios) == 12, "scenario_actual_count")
    expected_ids = {
        "S01_WEATHER_QUERY_NO_LONG_TERM_INTENT",
        "S02_FINDING_KEYS_EXPLICIT_INTENT",
        "S03_FAMILY_FIELD_TEMPORARY_WORK_DOMINANCE",
        "S04_LONG_OVERTIME_WORK_FAMILY_COEXISTENCE",
        "S05_UNFINISHED_WORK_CARRYOVER_HOME",
        "S06_SPOUSE_AND_COLLEAGUE_INTENTS_COEXIST",
        "S07_DIVORCED_BUT_COLLEAGUES",
        "S08_OLD_RELATION_DORMANT_REACTIVATION",
        "S09_FEAR_CROSSING_SAFETY_AVOIDANCE",
        "S10_SAYS_FINE_ABNORMAL_BEHAVIOR",
        "S11_LONG_TERM_ELECTRONIC_LIFE_DIRECTION",
        "S12_LOW_RESOURCE_PROJECTION_SHRINK",
    }
    check({item.get("scenario_id") for item in scenarios} == expected_ids, "scenario_ids_complete")
    required_case_fields = set(scenarios_doc.get("required_case_fields", []))
    check(all(required_case_fields.issubset(item) for item in scenarios), "scenario_fields_complete")
    check(all(item.get("source_owners") for item in scenarios), "scenario_source_owners")
    check(all(item.get("unknowns") for item in scenarios), "scenario_unknowns")
    check(all(item.get("forbidden_conclusions") for item in scenarios), "scenario_forbidden_conclusions")
    check(all(item.get("expected_handoff") for item in scenarios), "scenario_expected_handoff")

    reuse = documents["intent_existing_asset_reuse_mapping_v1.json"]
    expected_categories = {
        "existing_intent_like_assets",
        "existing_goal_like_assets",
        "existing_task_assets",
        "existing_decision_assets",
        "existing_self_drive_assets",
        "existing_emotion_influence_assets",
        "existing_memory_influence_assets",
        "existing_role_field_influence_assets",
    }
    check(all(category in reuse for category in expected_categories), "reuse_categories_complete")
    dispositions = set(reuse.get("disposition_registry", []))
    expected_dispositions = {"REUSE", "REFERENCE_ONLY", "NEEDS_ALIGNMENT", "FUTURE_EXTENSION", "DO_NOT_REUSE"}
    check(dispositions == expected_dispositions, "reuse_dispositions_complete")
    mapped_items = [item for category in expected_categories for item in reuse.get(category, [])]
    check(all(item.get("disposition") in dispositions for item in mapped_items), "reuse_dispositions_valid")
    check(all(item.get("conflict") is False for item in mapped_items), "reuse_no_item_conflicts")
    check(reuse.get("structural_owner_conflict") is False, "reuse_no_structural_conflict")
    check(reuse.get("parallel_intent_system_required") is False, "reuse_no_parallel_system")
    check(all((WORKSPACE / item.get("location", "")).exists() for item in mapped_items), "reuse_references_exist")

    risk_text = (PHASE_DIR / "intent_architecture_risk_review_v1.md").read_text(encoding="utf-8")
    risk_topics = ["Parallel Intent system", "Classifier collapse", "PCN activation conflation", "Single-winner collapse", "Dominance/Decision collapse", "Carryover/Context merge", "Action Intent naming collision", "Runtime premature activation", "No structural owner conflict"]
    for index, topic in enumerate(risk_topics, start=1):
        check(topic.lower() in risk_text.lower(), f"risk_topic_{index:02d}")

    questions = documents["intent_open_questions_registry_v1.json"]
    check(questions.get("blocking_question_count") == 0, "questions_no_blockers")
    check(len(questions.get("questions", [])) >= 10, "questions_sufficient")
    check(all(item.get("blocking") is False for item in questions.get("questions", [])), "questions_nonblocking")
    check(all(str(item.get("disposition", "")).startswith("DEFER_") for item in questions.get("questions", [])), "questions_deferred")

    verifier_source = (PHASE_DIR / "verify_intent_architecture_planning_v1.py").read_text(encoding="utf-8")
    verifier_tree = ast.parse(verifier_source)
    imported_roots: set[str] = set()
    forbidden_calls: list[str] = []
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in {"exec", "eval", "compile", "__import__"}:
                forbidden_calls.append(node.func.id)
    check(imported_roots.issubset({"__future__", "ast", "json", "pathlib", "typing"}), "verifier_standard_library_only")
    check(not ({"subprocess", "os", "socket", "requests", "urllib", "runtime", "capabilities"} & imported_roots), "verifier_no_runtime_model_network_import")
    check(not forbidden_calls, "verifier_no_dynamic_execution")
    check("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED" in verifier_source, "verifier_success_decision_literal")
    check("READINESS: LUNA_INTENT_ARCHITECTURE_PLANNING_READY" in verifier_source, "verifier_success_readiness_literal")
    check("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" in verifier_source, "verifier_next_literal")

    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_INTENT_ARCHITECTURE_PLANNING_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
    else:
        print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
        print("READINESS: LUNA_INTENT_ARCHITECTURE_PLANNING_READY")
        print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
