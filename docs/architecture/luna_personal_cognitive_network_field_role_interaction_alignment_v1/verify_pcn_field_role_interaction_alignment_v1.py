"""Read-only V2 verifier for PCN Field / Role Interaction Alignment v1."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DOCS_ROOT = ROOT.parents[1]
PCN_ROOT = DOCS_ROOT / "architecture/luna_personal_cognitive_network_planning_v1"

REQUIRED_FILES = {
    "field_boundary_model_candidate.json",
    "role_boundary_model_candidate.json",
    "temporary_field_occupation_model_candidate.json",
    "field_boundary_adaptation_model_candidate.json",
    "field_resonance_model_candidate.json",
    "field_role_interaction_type_registry_candidate.json",
    "role_competition_projection_model_candidate.json",
    "multi_relation_role_field_scenario_candidate.json",
    "historical_field_relationship_reactivation_candidate.json",
    "cognitive_interaction_kernel_boundary_candidate.json",
    "interaction_kernel_observation_axis_boundary_candidate.json",
    "field_role_interaction_resource_constraint_candidate.json",
    "field_role_interaction_nested_constraint_candidate.json",
    "pcn_field_role_interaction_alignment_impact_review.md",
    "field_role_interaction_stress_test_candidate.json",
    "field_role_interaction_risk_review.md",
    "field_role_interaction_alignment_summary.md",
    "alignment_change_manifest.json",
    "phase_contract.json",
    "verify_pcn_field_role_interaction_alignment_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}
MARKDOWN_FILES = {name for name in REQUIRED_FILES if name.endswith(".md")}
REFERENCE_PATHS = [
    "architecture/luna_personal_cognitive_network_planning_v1/personal_cognitive_network_object_model_candidate.json",
    "architecture/luna_context_foundation_module_closure_v1/context_to_pcn_handoff_contract_candidate.json",
    "architecture/luna_cognitive_field_architecture_v1/field_state_schema.json",
    "architecture/luna_cognitive_field_temporal_evolution_architecture_v1/field_identity_schema.json",
    "architecture/luna_role_architecture_v1/role_schema.json",
    "architecture/cognitive_role_relationship_system_v1/relationship_context_schema_v1.json",
    "architecture/luna_self_social_self_architecture_refactoring_v1/self_social_boundary_contract_v1.json",
]


def main() -> int:
    checks = 0
    failures: list[str] = []

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    # Required files and exact phase-directory scope.
    actual_files = {path.name for path in ROOT.iterdir() if path.is_file()}
    for name in sorted(REQUIRED_FILES):
        check((ROOT / name).is_file(), f"required_file:{name}")
    check(actual_files == REQUIRED_FILES, "exact_phase_file_set")

    # JSON parse and Markdown presence.
    parsed: dict[str, dict] = {}
    for name in sorted(JSON_FILES):
        try:
            value = json.loads((ROOT / name).read_text(encoding="utf-8"))
            check(isinstance(value, dict), f"json_object:{name}")
            parsed[name] = value
        except (OSError, json.JSONDecodeError):
            check(False, f"json_parse:{name}")
    for name in sorted(MARKDOWN_FILES):
        check(bool((ROOT / name).read_text(encoding="utf-8").strip()), f"markdown_nonempty:{name}")

    for relative in REFERENCE_PATHS:
        check((DOCS_ROOT / relative).is_file(), f"reference_exists:{relative}")

    # Verifier syntax and read-only dependency surface.
    source = (ROOT / "verify_pcn_field_role_interaction_alignment_v1.py").read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
        check(True, "verifier_ast")
    except SyntaxError:
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast")
    imports = {
        node.names[0].name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import) and node.names
    }
    imports.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    check(imports.issubset({"__future__", "ast", "hashlib", "json", "pathlib"}), "verifier_standard_library_only")
    check(
        imports <= {"__future__", "ast", "hashlib", "json", "pathlib"},
        "verifier_no_runtime_or_model_import",
    )
    write_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"write_text", "write_bytes", "unlink", "rename", "replace", "mkdir", "rmdir"}:
                write_calls.append(node.func.attr)
    check(not write_calls, "verifier_read_only")

    # Planning markers.
    for name, payload in sorted(parsed.items()):
        if name not in {"alignment_change_manifest.json", "phase_contract.json"}:
            check(payload.get("status") == "PLANNING_CANDIDATE", f"planning_status:{name}")

    field = parsed["field_boundary_model_candidate.json"]
    hard = field["boundary_classes"]["HARD_BOUNDARY"]
    fuzzy = field["boundary_classes"]["FUZZY_BOUNDARY"]
    check(
        set(hard["allowed_sources"])
        == {
            "physical_constraint",
            "governance_constraint",
            "permission_constraint",
            "legal_or_organizational_relationship",
            "explicit_task_responsibility",
            "confirmed_structural_boundary",
        },
        "hard_boundary_sources",
    )
    check(hard["pcn_override_allowed"] is False and hard["context_override_allowed"] is False, "hard_boundary_not_blurred")
    check(fuzzy["regions"] == ["CORE_REGION", "STRONG_REGION", "FUZZY_EDGE", "WEAK_ASSOCIATION"], "fuzzy_boundary_regions")
    check(fuzzy["binary_inside_outside_required"] is False, "field_boundary_not_binary")
    check(field["rules"]["field_state_reducer_remains_sole_state_mutation_authority"] is True, "field_reducer_sole_writer")

    role = parsed["role_boundary_model_candidate.json"]
    check(
        [item["tier"] for item in role["projection_tiers"]]
        == ["ROLE_CORE", "STRONG_PROJECTION", "FUZZY_PROJECTION", "CANDIDATE_PROJECTION"],
        "role_fuzzy_projection_tiers",
    )
    check(role["multiplicity"]["same_person_multiple_active_role_projections_allowed"] is True, "multi_role_allowed")
    check(role["multiplicity"]["simultaneous_roles_imply_conflict"] is False, "multi_role_not_default_conflict")
    check({"context_relevance", "field_relevance", "relationship_relevance"}.issubset(set(role["activation_constraints"])), "role_joint_activation_constraints")

    occupation = parsed["temporary_field_occupation_model_candidate.json"]
    check(
        occupation["occupation_states"]
        == ["NONE", "TEMPORARY_OCCUPATION", "REPEATED_OCCUPATION", "PERSISTENT_INFLUENCE_CANDIDATE"],
        "occupation_states",
    )
    check(occupation["rules"]["occupation_does_not_transfer_ownership"] is True, "occupation_not_ownership")
    check(occupation["rules"]["automatic_structural_change"] is False, "occupation_not_structural_mutation")

    adaptation = parsed["field_boundary_adaptation_model_candidate.json"]
    check(
        adaptation["candidate_flow"]
        == ["ACTIVATION", "TEMPORARY_OCCUPATION", "REPEATED_INTERACTION", "PERSISTENT_INFLUENCE", "STRUCTURAL_CHANGE_CANDIDATE"],
        "adaptation_flow",
    )
    check(adaptation["rules"]["single_event_core_field_modification"] is False, "single_event_no_field_change")
    check(adaptation["rules"]["fixed_time_threshold"] is False, "adaptation_no_fixed_time_threshold")
    check("future_emotion_influence_reference_only" in adaptation["evaluation_constraints"], "future_emotion_reference_only")

    resonance = parsed["field_resonance_model_candidate.json"]
    check(
        set(resonance["similarity_basis"])
        == {"role_structure", "relationship_structure", "task_structure", "benefit_cost_structure", "historical_experience_structure", "context_similarity"},
        "resonance_structural_inputs",
    )
    check(set(resonance["outputs"]) == {"RESONANCE_CANDIDATE", "RELATED_HISTORICAL_PROJECTION", "ACTIVATION_CANDIDATE"}, "resonance_outputs")
    check("CAUSAL_FACT" in resonance["forbidden_outputs"], "resonance_not_causal")
    check(resonance["rules"]["same_name_or_type_is_sufficient"] is False, "resonance_not_name_type_only")

    registry = parsed["field_role_interaction_type_registry_candidate.json"]
    expected_types = {"RESONANCE", "COMPETITION", "TEMPORARY_OCCUPATION", "OVERLAP", "COEXISTENCE", "FUSION_CANDIDATE", "HISTORICAL_REACTIVATION"}
    actual_types = {item["type"] for item in registry["interaction_types"]}
    check(actual_types == expected_types, "interaction_type_registry")
    check(len(registry["interaction_types"]) == len(actual_types), "interaction_type_unique")
    for item in registry["interaction_types"]:
        check(all(item.get(key) for key in ("definition", "sources", "targets", "forbidden_inference", "owner_boundary")), f"interaction_type_complete:{item['type']}")
    check(registry["rules"]["multiple_active_fields_imply_conflict"] is False, "multiple_fields_not_default_conflict")

    competition = parsed["role_competition_projection_model_candidate.json"]
    check(competition["rules"]["pcn_expresses_competition_candidate_only"] is True, "competition_candidate_only")
    check(competition["rules"]["pcn_selects_winner"] is False and competition["rules"]["interaction_kernel_selects_winner"] is False, "competition_not_arbitration")
    check("future_decision_arbitration" in competition["rules"]["final_selection_owner"], "future_arbitration_owner")

    scenario = parsed["multi_relation_role_field_scenario_candidate.json"]
    check(len(scenario["timeline"]) == 3, "multi_relation_timeline")
    check(scenario["relationship_rules"]["multiple_distinct_relationships_per_pair_allowed"] is True, "multi_relationship_coexistence")
    check(scenario["relationship_rules"]["relationship_end_means_delete"] is False, "ended_relationship_not_deleted")
    check(set(scenario["relationship_rules"]["former_spouse_relation_states"]) == {"HISTORICAL", "DORMANT", "REACTIVATABLE"}, "historical_relationship_states")
    check(scenario["relationship_rules"]["colleague_relation_survives_divorce"] is True, "colleague_relation_separated")

    reactivation = parsed["historical_field_relationship_reactivation_candidate.json"]
    check(set(reactivation["reactivation_triggers"]) == {"structure_similarity", "object_overlap", "relationship_trigger"}, "historical_reactivation_triggers")
    check("ACTIVATION_CANDIDATE" in reactivation["outputs"], "historical_activation_candidate")
    check({"EMOTION_CONCLUSION", "CAUSAL_FACT", "DECISION"}.issubset(set(reactivation["forbidden_outputs"])), "historical_reactivation_no_conclusion")
    check(reactivation["rules"]["historical_projection_is_current_reality"] is False, "historical_not_current_reality")

    kernel = parsed["cognitive_interaction_kernel_boundary_candidate.json"]
    check(set(kernel["observed_patterns"]) == expected_types, "kernel_observed_patterns")
    check(set(kernel["ownership_split"]["pcn_owns"]) == {"network_connections", "activation_candidates", "context_projections"}, "pcn_ownership_preserved")
    check(kernel["ownership_split"]["interaction_kernel_owns"] == ["local_interaction_candidate"], "kernel_local_candidate_owner")
    check(kernel["negative_boundaries"]["is_pcn_owner"] is False, "kernel_not_pcn_owner")
    check(kernel["negative_boundaries"]["is_cnn_or_convolution_implementation"] is False, "kernel_not_cnn")
    check(kernel["negative_boundaries"]["mutates_source_objects"] is False, "kernel_no_source_mutation")

    axis = parsed["interaction_kernel_observation_axis_boundary_candidate.json"]
    check(axis["owners"]["observation_axis"] != axis["owners"]["interaction_kernel"], "axis_kernel_owner_distinct")
    check(axis["rules"]["observation_axis_is_interaction_kernel"] is False, "axis_kernel_distinction")
    check(axis["rules"]["interaction_kernel_selects_perspective"] is False, "kernel_not_axis_selector")

    resource = parsed["field_role_interaction_resource_constraint_candidate.json"]
    check(all(value is None for value in resource["fixed_limits"].values()), "no_fixed_field_role_interaction_limits")
    check(resource["rules"]["resource_governance_bounds_expansion"] is True, "resource_bounded_interaction")
    check(resource["pressure_policy"]["delete_core_field"] is False, "resource_no_core_field_delete")
    check(resource["pressure_policy"]["delete_core_role"] is False and resource["pressure_policy"]["delete_relationship"] is False, "resource_no_role_relationship_delete")

    nested = parsed["field_role_interaction_nested_constraint_candidate.json"]
    expected_relations = {
        "Field_to_Role", "Field_to_Relationship", "Field_to_Context", "Role_to_Relationship",
        "Context_to_Interaction", "PCN_to_Interaction", "Resource_to_Interaction",
        "Observation_Axis_to_Interaction", "Future_Emotion_to_Interaction",
        "Future_Causal_to_Interaction", "Future_Decision_to_Interaction",
    }
    actual_relations = {item["relation"] for item in nested["relations"]}
    check(actual_relations == expected_relations, "nested_constraint_relations")
    check(len(actual_relations) == len(nested["relations"]), "nested_relation_unique")
    for item in nested["relations"]:
        check(all(item.get(key) for key in nested["required_relation_fields"]), f"nested_relation_complete:{item['relation']}")
    check(nested["rules"]["unique_mutation_owner_per_source_object"] is True, "no_second_writer")
    check(nested["rules"]["future_placeholders_inactive"] is True, "future_placeholders_inactive")

    stress = parsed["field_role_interaction_stress_test_candidate.json"]
    expected_cases = {
        "CASE_1_TEMPORARY_OVERTIME_AT_HOME", "CASE_2_LONG_TERM_OVERTIME_AT_HOME",
        "CASE_3_SPOUSES_AND_COLLEAGUES", "CASE_4_DIVORCED_BUT_STILL_COLLEAGUES",
        "CASE_5_MEETING_REACTIVATES_FORMER_RELATION", "CASE_6_TWO_SAME_TYPE_WORK_FIELDS",
        "CASE_7_FATHER_AND_EMPLOYEE_ROLE_TENSION", "CASE_8_SPOUSES_BUILD_BUSINESS_TOGETHER",
    }
    check(stress["case_count"] == 8, "stress_case_count")
    check({item["case_id"] for item in stress["cases"]} == expected_cases, "stress_case_coverage")
    check(all(item["validates"] and item["expected"] for item in stress["cases"]), "stress_case_expectations")

    impact = (ROOT / "pcn_field_role_interaction_alignment_impact_review.md").read_text(encoding="utf-8")
    for area in ("Object Model", "Link Model", "Activation", "Dormancy / Reactivation", "Growth", "Nested Constraints", "Scenario Simulation"):
        check(area in impact, f"impact_area:{area}")
    for classification in ("COMPATIBLE_AS_IS", "REFERENCE_UPDATE_REQUIRED_LATER", "SKELETON_MUST_ACCOUNT_FOR", "BLOCKED"):
        check(classification in impact, f"impact_classification:{classification}")
    check("No assessed PCN planning area is `BLOCKED`" in impact, "impact_no_blocker")

    risk = (ROOT / "field_role_interaction_risk_review.md").read_text(encoding="utf-8")
    risk_terms = [
        "physical place", "binary inside/outside", "Core Field", "Multiple Roles", "overwrites an old Relationship",
        "Historical Relationship deleted", "Causal Fact", "absorbed by PCN", "CNN", "score-versus-score",
        "fixed numeric limits", "Nested-loop living-system",
    ]
    for term in risk_terms:
        check(term in risk, f"risk_review:{term}")

    summary = (ROOT / "field_role_interaction_alignment_summary.md").read_text(encoding="utf-8")
    for topic in (
        "Field Boundary", "Role Boundary", "Occupation", "Expansion / Contraction", "Resonance", "Competition",
        "Overlap / Coexistence", "Historical Reactivation", "Interaction Kernel", "Observation Axis", "PCN Impact",
        "Resource Constraint", "Nested Constraint", "Stress Test",
    ):
        check(topic in summary, f"summary_topic:{topic}")
    check("There is no second writer" in summary, "summary_no_second_writer")

    manifest = parsed["alignment_change_manifest.json"]
    expected_created = REQUIRED_FILES
    check(set(manifest["created_files"]) == expected_created, "manifest_created_files")
    check(manifest["modified_existing_files"] == [], "manifest_no_existing_modification")
    check(manifest["code_files_changed"] == [], "manifest_no_code_change")
    check(manifest["runtime_files_changed"] == [], "manifest_no_runtime_change")
    for flag in (
        "active_schema_changed", "active_contract_changed", "owner_changed", "pcn_planning_modified",
        "interaction_runtime_created", "migration_executed",
    ):
        check(manifest[flag] is False, f"manifest_false:{flag}")

    protected = manifest["protected_pcn_planning_hashes"]
    check(set(protected) == {path.name for path in PCN_ROOT.iterdir() if path.is_file()}, "protected_pcn_file_set")
    for name, expected_hash in sorted(protected.items()):
        actual_hash = hashlib.sha256((PCN_ROOT / name).read_bytes()).hexdigest()
        check(actual_hash == expected_hash, f"protected_pcn_hash:{name}")

    phase = parsed["phase_contract.json"]
    check(phase["execution_mode"] == "Planning Only", "phase_planning_only")
    check(phase["implementation_started"] is False, "phase_no_implementation")
    check(phase["pcn_skeleton_started"] is False, "phase_no_pcn_skeleton")
    check(phase["interaction_runtime_started"] is False, "phase_no_interaction_runtime")
    check(phase["next_phase_not_authorized"] is True, "phase_next_not_authorized")
    check(phase["verification_authority"] == {"V0": "AGENT_STATIC_ONLY", "V1": "NOT_AUTHORIZED", "V2": "USER_TERMINAL_ONLY", "V3": "CHATGPT_ONLY"}, "phase_verification_authority")
    check(phase["expected_success_readiness"] == "LUNA_PCN_FIELD_ROLE_INTERACTION_ALIGNMENT_READY", "phase_readiness_token")
    check(phase["go_declared"] is False, "phase_no_go")

    failed_count = len(failures)
    blocker_count = failed_count
    if failures:
        final_decision = "BLOCKED_BY_VERIFIER_FAILURE"
        readiness = "LUNA_PCN_FIELD_ROLE_INTERACTION_ALIGNMENT_REMEDIATION_REQUIRED"
        next_step = "REMEDIATE_REPORTED_FAILURES_ONLY"
    else:
        final_decision = "V2_FINAL_VERIFICATION_PASSED"
        readiness = "LUNA_PCN_FIELD_ROLE_INTERACTION_ALIGNMENT_READY"
        next_step = "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"

    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - failed_count}")
    print(f"FAILED_CHECK_COUNT: {failed_count}")
    print(f"BLOCKER_COUNT: {blocker_count}")
    print(f"FINAL_DECISION: {final_decision}")
    print(f"READINESS: {readiness}")
    print(f"NEXT: {next_step}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
