"""V0 static contract verifier for Dynamic Cognitive Function Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "cognitive_state_vector_schema.json", "cognitive_function_contract.json",
    "self_regulation_function_contract.json", "parameter_space_schema.json",
    "cognitive_genome_schema.json", "adaptive_adjustment_contract.json",
    "hive_evaluation_interface.json", "parameter_evolution_boundary.json",
    "state_machine_migration_mapping.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "dynamic_cognitive_function_architecture.md", "cognitive_state_vector_model.md",
    "self_regulation_function_model.md", "cognitive_parameter_genome_model.md",
    "adaptive_evolution_boundary.md",
]
VERIFIER = "verify_dynamic_function_architecture_v1.py"
COMPONENTS = ["observation_activation", "understanding_confidence", "risk_attention", "exploration_drive", "memory_activation", "decision_pressure"]
STATES = ["Observation", "Understanding", "Decision", "Action", "Reflection", "Learning"]


def load(assets: dict[str, dict], name: str) -> dict:
    if name not in assets:
        assets[name] = json.loads((ROOT / name).read_text(encoding="utf-8"))
    return assets[name]


def main() -> int:
    checks = 0
    failed: list[str] = []

    def check(condition: bool, label: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failed.append(label)

    expected = set(JSON_FILES) | set(MD_FILES) | {VERIFIER}
    files = {p.name for p in ROOT.iterdir() if p.is_file()}
    check(expected <= files, "required_assets")
    check({p.name for p in ROOT.glob("*.py")} == {VERIFIER}, "no_runtime_python")
    assets: dict[str, dict] = {}
    for name in JSON_FILES:
        try:
            value = load(assets, name)
            check(isinstance(value, dict), f"json_object:{name}")
        except (OSError, json.JSONDecodeError):
            check(False, f"json_parse:{name}")
    for name in MD_FILES:
        try:
            check((ROOT / name).read_text(encoding="utf-8").strip() != "", f"markdown_nonempty:{name}")
        except OSError:
            check(False, f"markdown_read:{name}")
    try:
        ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        check(True, "verifier_ast")
    except (OSError, SyntaxError):
        check(False, "verifier_ast")

    vector = load(assets, "cognitive_state_vector_schema.json")
    check(vector["components"] == COMPONENTS, "vector_components")
    check(vector["component_range"] == [0.0, 1.0] and vector["bounded_values_required"] is True, "vector_bounds")
    check(set(vector["required_fields"]) >= {"vector_id", "field_ref", "flow_ref", "timestamp", "components", "source_evidence", "confidence", "unknowns", "parameter_profile_ref"}, "vector_fields")
    check(vector["vector_is_not_reality"] is True and vector["vector_is_not_decision"] is True and vector["vector_is_not_action"] is True and vector["vector_is_not_memory"] is True and vector["candidate_only"] is True and vector["runtime"] is False, "vector_boundary")

    function = load(assets, "cognitive_function_contract.json")
    check(function["equation"] == "C(t+1) = F(C(t), Field(t), Self(t), Goal(t))", "function_equation")
    check(set(function["inputs"]) == {"Cognitive State Vector", "Field State", "Self State", "Goal State"}, "function_inputs")
    check(set(function["outputs"]) == {"State Vector Update Candidate", "Attention Policy Candidate", "Threshold Candidate", "Reconsideration Candidate"}, "function_outputs")
    check(function["function_is_interface_only"] is True and function["continuous_update_runtime"] is False and function["automatic_update"] is False and function["decision_authority"] is False and function["action_execution"] is False and function["reality_mutation"] is False and function["unknowns_preserved"] is True and function["trace_required"] is True and function["candidate_only"] is True, "function_boundary")

    regulation = load(assets, "self_regulation_function_contract.json")
    check(regulation["equation"] == "R(t) = f(Self, Resource, Constitution)", "regulation_equation")
    check(set(regulation["inputs"]) == {"Self State", "Capability Health", "Resource State", "Self Rhythm", "Constitution"}, "regulation_inputs")
    check(set(regulation["outputs"]) == {"Attention Budget Candidate", "Exploration Budget Candidate", "Compute Budget Candidate", "Risk Threshold Candidate", "Learning Permission Candidate"}, "regulation_outputs")
    check(regulation["self_protective_precedence"] is True and regulation["resource_output_is_hint"] is True and regulation["does_not_generate_reality"] is True and regulation["does_not_override_understanding"] is True and regulation["does_not_select_decision_alone"] is True and regulation["does_not_switch_model"] is True and regulation["does_not_control_hardware"] is True and regulation["does_not_approve_learning_alone"] is True and regulation["does_not_modify_identity"] is True and regulation["does_not_modify_constitution"] is True and regulation["candidate_only"] is True and regulation["runtime"] is False, "regulation_boundary")

    parameters = load(assets, "parameter_space_schema.json")
    check(parameters["dimensions"] == ["perception", "cognition", "memory", "decision", "resource_risk"], "parameter_dimensions")
    check(set(parameters["parameter_required_fields"]) >= {"parameter_id", "name", "dimension", "value", "range", "unit", "source", "mutable", "risk_level", "validation_metric", "rollback_ref"}, "parameter_fields")
    check(set(parameters["allowed_examples"]) >= {"risk_sensitivity", "memory_decay_rate", "exploration_threshold", "context_weight", "uncertainty_tolerance"}, "parameter_examples")
    check(parameters["bounded_values_required"] is True and parameters["parameter_is_not_identity"] is True and parameters["parameter_is_not_constitution"] is True and parameters["parameter_is_not_decision_authority"] is True and parameters["automatic_tuning"] is False and parameters["runtime"] is False and parameters["candidate_only"] is True, "parameter_boundary")

    genome = load(assets, "cognitive_genome_schema.json")
    check(genome["genome_components"] == ["perception_tendencies", "cognitive_tendencies", "memory_tendencies", "decision_tendencies", "resource_risk_tendencies"], "genome_components")
    check(set(genome["required_fields"]) >= {"genome_id", "version", "parameter_refs", "field_scope", "provenance", "validation_history", "risk_profile", "rollback_ref"}, "genome_fields")
    check(genome["genome_is_parameter_bundle"] is True and genome["genome_is_not_biological"] is True and genome["genome_is_not_identity"] is True and genome["genome_is_not_personality_authority"] is True and genome["genome_has_no_decision_authority"] is True and genome["self_review_required_for_change"] is True and genome["automatic_evolution"] is False and genome["candidate_only"] is True, "genome_boundary")

    adjustment = load(assets, "adaptive_adjustment_contract.json")
    check(set(adjustment["inputs"]) == {"Cognitive State Vector", "Field Context", "Self Regulation Output", "Outcome Evidence", "Parameter Space", "Utility Candidate"}, "adjustment_inputs")
    check(set(adjustment["outputs"]) == {"Parameter Adjustment Candidate", "Threshold Adjustment Candidate", "No Change Candidate", "Defer Candidate"}, "adjustment_outputs")
    check(set(adjustment["requirements"]) >= {"evidence", "field_scope", "expected_benefit", "cost", "risk", "reversibility", "validation_metric"}, "adjustment_requirements")
    check(adjustment["self_review_required"] is True and adjustment["constitution_review_required"] is True and adjustment["automatic_adjustment"] is False and adjustment["automatic_rollback"] is False and adjustment["direct_model_parameter_update"] is False and adjustment["direct_identity_change"] is False and adjustment["candidate_only"] is True, "adjustment_boundary")

    hive = load(assets, "hive_evaluation_interface.json")
    check(hive["input_tuple"] == ["Field", "Cognitive Genome", "Outcome"], "hive_tuple")
    check(set(hive["inputs"]) >= {"anonymized_field_context", "genome_version", "outcome_evidence", "capability_metrics", "risk_metrics"}, "hive_inputs")
    check(set(hive["outputs"]) == {"Parameter Improvement Candidate", "Comparative Evidence", "Confidence", "Unknowns"}, "hive_outputs")
    check(hive["hive_is_observer_not_authority"] is True and hive["external_hive_connection"] is False and hive["direct_luna_modification"] is False and hive["self_review_required"] is True and hive["accept_reject_defer_required"] is True and hive["privacy_boundary_required"] is True and hive["candidate_only"] is True and hive["runtime"] is False, "hive_boundary")

    evolution = load(assets, "parameter_evolution_boundary.json")
    check(evolution["flow"] == ["Hive Observation", "Parameter Improvement Candidate", "Luna Self Review", "Accept/Reject/Defer", "Parameter Evolution Candidate"], "evolution_flow")
    check(set(evolution["mutable_targets"]) >= {"Cognitive State Vector Parameters", "Attention Threshold Candidate", "Exploration Threshold Candidate", "Memory Decay Candidate", "Risk Sensitivity Candidate", "Context Weight Candidate"}, "evolution_mutable")
    check(set(evolution["protected_targets"]) >= {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules", "Reality", "Current Goal Directly"}, "evolution_protected")
    check(set(evolution["approval_owners"]) == {"Self Governance", "Constitution Governance", "Capability Governance"} and evolution["automatic_parameter_evolution"] is False and evolution["automatic_self_modification"] is False and evolution["hive_has_no_write_permission"] is True and evolution["rollback_required"] is True and evolution["versioning_required"] is True and evolution["candidate_only"] is True, "evolution_boundary")

    migration = load(assets, "state_machine_migration_mapping.json")
    check(migration["source"] == "Cognitive State Machine" and migration["target"] == "Dynamic Cognitive Function Model", "migration_direction")
    check([item["legacy_state"] for item in migration["mapping"]] == STATES and all(item["vector_dimensions"] for item in migration["mapping"]), "migration_coverage")
    check(migration["state_machine_remains_compatible"] is True and migration["dynamic_model_replaces_runtime_state_machine"] is False and migration["migration_is_architecture_mapping_only"] is True and migration["automatic_migration"] is False and migration["candidate_only"] is True, "migration_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Cognitive State Vector", "Dynamic Cognitive Function", "Self Regulation Function", "Parameter Space", "Cognitive Genome", "Adaptive Adjustment", "Hive Evaluation", "State Machine Migration", "Self", "Constitution", "Runtime", "B Route"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Dynamic Function -> Reality Mutation", "Dynamic Function -> Direct Decision Commit", "Dynamic Function -> Execute Action", "Self Regulation Function -> Switch Model", "Self Regulation Function -> Hardware Control", "Hive Evaluation -> Direct Luna Modification", "Hive Evaluation -> Parameter Write", "Adaptive Adjustment -> Automatic Tuning", "Parameter Evolution -> Automatic Self Modification", "B Route -> Direct Parameter Adoption", "Runtime -> Parameter Governance", "Emotion -> Direct Parameter Adoption"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_runtime"] is True and dependency["no_automatic_tuning"] is True and dependency["no_hive_connection"] is True and dependency["no_parameter_learning"] is True and dependency["no_self_automatic_modification"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True and dependency["no_model_integration"] is True and dependency["no_hardware_control"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "automatic_tuning", "hive_connection", "parameter_learning", "automatic_self_modification", "emotion_runtime", "b_route_runtime", "model_integration", "hardware_control", "dynamic_function_reality_mutation", "dynamic_function_decision_commit", "dynamic_function_execute_action", "self_regulation_switch_model", "self_regulation_hardware_control", "hive_direct_luna_modification", "hive_parameter_write", "hive_self_modification", "adaptive_automatic_tuning", "parameter_automatic_self_modification", "parameter_identity_change", "parameter_constitution_change", "b_route_direct_parameter_adoption", "runtime_parameter_governance", "emotion_direct_parameter_adoption", "provider_parameter_authority", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("vector_is_bounded", "function_is_candidate_only", "self_regulation_is_resource_governance", "parameter_space_is_auditable", "genome_is_not_identity", "hive_is_observer_not_authority", "self_review_required", "protected_targets_preserved", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_DYNAMIC_FUNCTION_ARCHITECTURE_READY", "summary_status")
    check(summary["equations"] == ["C(t+1) = F(C(t), Field(t), Self(t), Goal(t))", "R(t) = f(Self, Resource, Constitution)"] and summary["vector_components"] == COMPONENTS and summary["state_machine_migration"] is True and summary["cognitive_genome_is_parameter_bundle"] is True and summary["hive_is_candidate_source_only"] is True and summary["self_review_required"] is True, "summary_model")
    check(set(summary["protected_targets"]) >= {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules", "Reality"}, "summary_protected")
    check(summary["runtime"] is False and summary["automatic_tuning"] is False and summary["hive_connection"] is False and summary["parameter_learning"] is False and summary["self_automatic_modification"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False and summary["model_integration"] is False and summary["hardware_control"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 6 and len(summary["parallel_risks"]) >= 4 and len(summary["future_extensions"]) >= 3, "summary_inventory")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        check(not imports & forbidden_imports, "verifier_no_runtime_imports")
    except (OSError, SyntaxError):
        check(False, "verifier_no_runtime_imports")

    blockers = len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {checks - blockers}")
    print(f"FAILED_CHECK_COUNT: {blockers}")
    print(f"BLOCKER_COUNT: {blockers}")
    if blockers:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_DYNAMIC_FUNCTION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_DYNAMIC_FUNCTION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

