"""V0 static verifier for Dynamic Function and Self Adaptive Integration Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "dynamic_function_schema.json", "cognitive_function_registry.json",
    "function_parameter_mapping.json", "state_vector_mapping.json",
    "self_regulation_contract.json", "self_calibration_contract.json",
    "adaptive_parameter_schema.json", "cognitive_genome_schema.json",
    "parameter_evolution_boundary.json", "hive_observation_contract.json",
    "optimization_candidate_contract.json", "field_function_relation.json",
    "memory_function_relation.json", "attention_function_relation.json",
    "decision_function_relation.json", "learning_function_relation.json",
    "a_route_mapping_contract.json", "b_route_boundary_contract.json",
    "ownership_registry.json", "dependency_boundary.json",
    "negative_guards.json", "summary.json",
]
MD_FILES = [
    "dynamic_function_self_adaptive_architecture.md", "cognitive_function_mapping.md",
    "self_regulation_calibration_model.md", "cognitive_genome_parameter_governance.md",
    "hive_optimization_boundary.md", "implementation_plan.md",
]
VERIFIER = "verify_dynamic_function_self_adaptive_integration_architecture_v1.py"
FUNCTIONS = ["field_input_space", "attention_function", "memory_influence_function", "prior_knowledge_function", "confidence_dynamics_function", "goal_drive_function", "utility_function", "decision_function", "error_signal_function", "parameter_evolution_candidate_generator"]


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

    schema = load(assets, "dynamic_function_schema.json")
    check(schema["layers"] == ["Self Constitution", "Self Regulation Function", "Dynamic Cognitive Function", "Cognitive Capability Modules", "Self Calibration Function", "Adaptive Parameter Candidate", "Self Review"], "schema_layers")
    check(set(schema["required_fields"]) >= {"function_id", "owner", "inputs", "parameters", "outputs", "field_scope", "trace_ref", "unknowns"}, "schema_fields")
    check(schema["outputs_are_candidates"] is True and schema["function_is_not_runtime"] is True and schema["function_is_not_action"] is True and schema["function_is_not_decision_authority"] is True and schema["self_review_required"] is True and schema["runtime"] is False, "schema_boundary")

    registry = load(assets, "cognitive_function_registry.json")
    check([item["function_id"] for item in registry["functions"]] == FUNCTIONS, "function_registry")
    check(all(item.get("module") and item.get("role") for item in registry["functions"]), "function_registry_fields")
    check(registry["unique_function_owner"] is True and registry["mapping_is_not_replacement"] is True and registry["runtime"] is False, "function_registry_boundary")

    parameters = load(assets, "function_parameter_mapping.json")
    function_ids = [item["function_id"] for item in parameters["mappings"]]
    check(set(function_ids) >= {"attention_function", "memory_influence_function", "confidence_dynamics_function", "goal_drive_function", "utility_function", "decision_function", "error_signal_function", "parameter_evolution_candidate_generator"}, "parameter_mapping")
    check(all(item["parameters"] for item in parameters["mappings"]), "parameter_mapping_fields")
    check(parameters["parameters_are_bounded"] is True and parameters["field_scope_required"] is True and parameters["version_required"] is True and parameters["rollback_required"] is True and parameters["automatic_update"] is False and parameters["candidate_only"] is True, "parameter_mapping_boundary")

    vector = load(assets, "state_vector_mapping.json")
    check(vector["vector_components"] == ["observation_activation", "understanding_confidence", "risk_attention", "exploration_drive", "memory_activation", "decision_pressure"], "state_vector_components")
    check([item["state"] for item in vector["mapping"]] == ["Observation", "Understanding", "Decision", "Action", "Reflection", "Learning"], "state_vector_states")
    check(vector["legacy_state_machine_preserved"] is True and vector["vector_is_not_runtime_state"] is True and vector["mapping_is_architecture_only"] is True and vector["candidate_only"] is True, "state_vector_boundary")

    regulation = load(assets, "self_regulation_contract.json")
    check(regulation["equation"] == "R(t)=f(Self,Resource,Constitution)" and set(regulation["inputs"]) == {"Self State", "Resource State", "Capability Health", "Self Rhythm", "Constitution"}, "regulation_equation_inputs")
    check(set(regulation["outputs"]) == {"Attention Budget", "Compute Budget", "Exploration Permission", "Risk Threshold", "Learning Permission"}, "regulation_outputs")
    check(regulation["outputs_are_candidates_or_hints"] is True and regulation["self_protective_precedence"] is True and regulation["does_not_generate_goal"] is True and regulation["does_not_select_decision_alone"] is True and regulation["does_not_switch_model"] is True and regulation["does_not_control_hardware"] is True and regulation["does_not_modify_identity"] is True and regulation["does_not_modify_constitution"] is True and regulation["automatic_regulation"] is False and regulation["candidate_only"] is True and regulation["runtime"] is False, "regulation_boundary")

    calibration = load(assets, "self_calibration_contract.json")
    check(calibration["equation"] == "Calibration=f(Outcome,History,Performance)" and set(calibration["inputs"]) >= {"Outcome", "Prediction Error", "Capability Performance", "Long-term Pattern", "Field Scope", "Parameter History"}, "calibration_equation_inputs")
    check(set(calibration["outputs"]) >= {"Optimization Candidate", "Calibration Confidence", "No Change Candidate", "Defer Candidate"}, "calibration_outputs")
    check(calibration["calibration_is_not_learning_runtime"] is True and calibration["calibration_is_not_automatic_update"] is True and calibration["evidence_required"] is True and calibration["field_scope_required"] is True and calibration["versioning_required"] is True and calibration["rollback_required"] is True and calibration["self_review_required"] is True and calibration["does_not_modify_identity"] is True and calibration["does_not_modify_constitution"] is True and calibration["candidate_only"] is True and calibration["runtime"] is False, "calibration_boundary")

    adaptive = load(assets, "adaptive_parameter_schema.json")
    check(adaptive["parameter_classes"] == ["Constitution Parameter", "Adaptive Parameter", "Learned Parameter"], "parameter_classes")
    check(set(adaptive["required_fields"]) >= {"parameter_id", "class", "name", "value", "range", "unit", "field_scope", "provenance", "evidence", "risk", "validation_metric", "version", "rollback_ref"}, "adaptive_parameter_fields")
    check(adaptive["constitution_parameter_mutable"] is False and adaptive["adaptive_parameter_requires_review"] is True and adaptive["learned_parameter_is_candidate"] is True and adaptive["identity_parameter_protected"] is True and adaptive["safety_parameter_protected"] is True and adaptive["automatic_update"] is False and adaptive["candidate_only"] is True, "adaptive_parameter_boundary")

    genome = load(assets, "cognitive_genome_schema.json")
    check(genome["layers"] == ["Fixed Genome", "Adaptive Genome", "Learned Genome"], "genome_layers")
    check(genome["fixed_genome"]["mutable"] is False and genome["adaptive_genome"]["mutable"] is True and genome["adaptive_genome"]["requires_self_review"] is True and genome["learned_genome"]["mutable"] == "candidate_only" and genome["learned_genome"]["requires_evidence"] is True, "genome_mutability")
    check(set(genome["required_fields"]) >= {"genome_id", "version", "parameter_refs", "field_scope", "provenance", "validation_history", "risk_profile", "rollback_ref"} and genome["genome_is_not_biological"] is True and genome["genome_is_not_identity"] is True and genome["genome_has_no_decision_authority"] is True and genome["automatic_evolution"] is False and genome["candidate_only"] is True, "genome_boundary")

    evolution = load(assets, "parameter_evolution_boundary.json")
    check(evolution["flow"] == ["Outcome Feedback", "Self Calibration", "Optimization Candidate", "Self Review", "Accept/Reject/Defer", "Adaptive Parameter Candidate"], "evolution_flow")
    check(set(evolution["mutable_targets"]) >= {"Attention Weight", "Exploration Threshold", "Memory Activation Weight", "Confidence Threshold", "Goal Activation Threshold", "Decision Reconsideration Threshold", "Strategy Weight"}, "evolution_targets")
    check(set(evolution["protected_targets"]) >= {"Constitution", "Identity", "Safety Boundary", "Core Brain Rules", "Reality", "Current Goal Directly"} and set(evolution["approval_owners"]) == {"Self Governance", "Constitution Governance", "Capability Governance"}, "evolution_protected")
    check(evolution["automatic_parameter_update"] is False and evolution["automatic_self_modification"] is False and evolution["rollback_required"] is True and evolution["versioning_required"] is True and evolution["candidate_only"] is True, "evolution_boundary")

    hive = load(assets, "hive_observation_contract.json")
    check(hive["observation_tuple"] == ["Field", "Cognitive Genome", "Outcome"] and set(hive["inputs"]) >= {"Field Context", "Genome Version", "Outcome Evidence", "Performance Metrics", "Risk Metrics"}, "hive_inputs")
    check(set(hive["outputs"]) >= {"Performance Analysis", "Optimization Candidate", "Comparative Evidence", "Confidence", "Unknowns"} and hive["hive_role"] == "observer_and_candidate_provider" and hive["hive_is_not_owner"] is True and hive["hive_has_no_write_permission"] is True and hive["external_hive_connection"] is False and hive["privacy_scope_required"] is True and hive["self_review_required"] is True and hive["automatic_optimization"] is False and hive["candidate_only"] is True, "hive_boundary")

    optimization = load(assets, "optimization_candidate_contract.json")
    check(set(optimization["required_fields"]) >= {"candidate_id", "source", "field_scope", "parameter_refs", "expected_benefit", "cost", "risk", "reversibility", "evidence", "validation_metric", "rollback_ref", "unknowns"}, "optimization_fields")
    check(set(optimization["sources"]) == {"Self Calibration", "Hive Observation", "Outcome Evaluation", "Selective Learning"} and set(optimization["outputs"]) == {"Accept Candidate", "Reject Candidate", "Defer Candidate", "Revise Candidate"}, "optimization_flow")
    check(optimization["self_review_required"] is True and optimization["constitution_review_required"] is True and optimization["capability_governance_review_required"] is True and optimization["direct_update"] is False and optimization["automatic_adoption"] is False and optimization["candidate_only"] is True, "optimization_boundary")

    field = load(assets, "field_function_relation.json")
    check(field["function_role"] == "Input State Space" and set(field["inputs"]) >= {"Field State Vector", "Temporal State", "Spatial State", "Environment State", "Relationship State", "Role State", "Task State"} and set(field["outputs"]) >= {"Dynamic Function Input Candidate", "Field Influence Weight Candidate", "Field Transition Signal Candidate"}, "field_relation")
    check(field["field_is_not_reality"] is True and field["field_does_not_override_self"] is True and field["field_does_not_execute"] is True and field["candidate_only"] is True, "field_relation_boundary")

    memory = load(assets, "memory_function_relation.json")
    check(memory["function_role"] == "Historical Influence Function" and set(memory["inputs"]) >= {"Current Field", "Memory Layers", "Context Match", "Temporal Decay", "Reinforcement", "Reliability"} and set(memory["outputs"]) >= {"Activation Candidate", "Influence Weight Candidate", "Context Dependency Candidate"}, "memory_relation")
    check(memory["memory_is_not_database_only"] is True and memory["memory_is_not_reality"] is True and memory["memory_is_not_decision_authority"] is True and memory["memory_does_not_override_current_field"] is True and memory["automatic_memory_write"] is False and memory["candidate_only"] is True, "memory_relation_boundary")

    attention = load(assets, "attention_function_relation.json")
    check(attention["function_role"] == "Attention Function" and set(attention["inputs"]) >= {"Field", "Goal", "Uncertainty", "Self Budget", "Cognitive State Vector"} and set(attention["parameters"]) == {"risk_sensitivity", "novelty_sensitivity", "task_sensitivity"} and set(attention["outputs"]) >= {"Cognitive Resource Allocation Candidate", "Attention Weight Candidate", "Priority Threshold Candidate"}, "attention_relation")
    check(attention["attention_is_not_state_owner"] is True and attention["attention_is_not_decision_authority"] is True and attention["attention_does_not_execute"] is True and attention["automatic_allocation"] is False and attention["candidate_only"] is True, "attention_relation_boundary")

    decision = load(assets, "decision_function_relation.json")
    check(decision["function_role"] == "Decision Function" and decision["equation"] == "Decision=f(Understanding,Goal,Value,Self)" and set(decision["inputs"]) >= {"Understanding", "Goal", "Value", "Self", "Risk", "Resource"} and set(decision["outputs"]) >= {"Decision Candidate", "Priority Candidate", "Reconsideration Candidate"}, "decision_relation")
    check(decision["decision_is_not_action"] is True and decision["self_has_veto_context"] is True and decision["hard_constraints_precede_selection"] is True and decision["automatic_decision"] is False and decision["candidate_only"] is True, "decision_relation_boundary")

    learning = load(assets, "learning_function_relation.json")
    check(learning["function_role"] == "Parameter Evolution Candidate Generator" and set(learning["inputs"]) >= {"Outcome", "Prediction Error", "Experience", "Pattern", "Schema", "Learning Utility", "Self Review"} and set(learning["outputs"]) >= {"Parameter Evolution Candidate", "Schema Candidate", "Threshold Candidate", "Weight Candidate", "No Change Candidate"}, "learning_relation")
    check(learning["learning_is_not_automatic_update"] is True and learning["learning_is_not_model_training"] is True and learning["learning_requires_self_review"] is True and learning["learning_does_not_modify_identity"] is True and learning["learning_does_not_modify_constitution"] is True and learning["candidate_only"] is True, "learning_relation_boundary")

    a_route = load(assets, "a_route_mapping_contract.json")
    check(a_route["flow"] == ["Reality", "Field", "Dynamic Cognitive Function", "Understanding", "Decision", "Action", "Outcome", "Self Calibration", "Parameter Evolution"], "a_route_flow")
    check(a_route["a_route_purpose"] == "current_reality_cognition" and a_route["dynamic_function_is_interpretive_layer"] is True and a_route["self_adaptive_is_governance_layer"] is True and a_route["outcome_is_error_signal_candidate"] is True and a_route["parameter_evolution_is_candidate"] is True and a_route["runtime"] is False and a_route["action_execution"] is False and a_route["automatic_learning"] is False and a_route["candidate_only"] is True, "a_route_boundary")

    b_route = load(assets, "b_route_boundary_contract.json")
    check(b_route["b_route_status"] == "future_interface_only" and b_route["b_route_cannot_modify_a_function"] is True and b_route["b_route_cannot_modify_self"] is True and b_route["b_route_cannot_directly_update_parameter"] is True and b_route["b_route_cannot_turn_virtual_outcome_into_experience"] is True and b_route["b_route_cannot_override_reality"] is True and b_route["b_route_cannot_override_decision"] is True and b_route["b_route_runtime"] is False and b_route["route_mixing"] is False, "b_route_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Dynamic Function", "Field Function", "Attention Function", "Memory Function", "Knowledge Function", "Belief/Understanding Function", "Goal Function", "Value Function", "Decision Function", "Outcome Error Function", "Learning Function", "Self Regulation Function", "Self Calibration Function", "Adaptive Parameter", "Cognitive Genome", "Hive", "Self", "Constitution", "Runtime", "B Route"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Dynamic Function -> Runtime", "Dynamic Function -> Direct Action", "Dynamic Function -> Reality Mutation", "Self Regulation -> Switch Model", "Self Regulation -> Hardware Control", "Self Calibration -> Automatic Parameter Update", "Knowledge -> Replace Reality", "Memory -> Override Reality", "Goal -> Direct Action", "Value -> Commit Decision", "Decision -> Execute Action", "Outcome -> Direct Self Modification", "Learning -> Automatic Parameter Update", "Learning -> Model Training", "Hive -> Direct Parameter Modification", "Hive -> Direct Self Change", "Genome -> Identity Change", "B Route -> Modify A Function", "B Route -> Direct Parameter Adoption", "B Route -> Virtual Outcome as Experience", "Runtime -> Adaptive Parameter Authority", "Emotion -> Direct Parameter Adoption"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_runtime"] is True and dependency["no_automatic_tuning"] is True and dependency["no_hive_connection"] is True and dependency["no_parameter_update"] is True and dependency["no_self_automatic_modification"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True and dependency["no_model_integration"] is True and dependency["no_hardware_control"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "automatic_tuning", "hive_connection", "parameter_update", "automatic_self_modification", "emotion_runtime", "b_route_runtime", "model_integration", "hardware_control", "dynamic_function_runtime", "dynamic_function_direct_action", "dynamic_function_reality_mutation", "self_regulation_switch_model", "self_regulation_hardware_control", "self_calibration_automatic_update", "self_calibration_identity_change", "knowledge_replace_reality", "memory_override_reality", "goal_direct_action", "value_commit_decision", "decision_execute_action", "outcome_direct_self_modification", "learning_automatic_parameter_update", "learning_model_training", "hive_direct_parameter_modification", "hive_direct_self_change", "genome_identity_change", "b_route_modify_a_function", "b_route_direct_parameter_adoption", "b_route_virtual_outcome_experience", "runtime_adaptive_parameter_authority", "emotion_direct_parameter_adoption", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("meta_architecture_only", "legacy_modules_preserved", "dynamic_functions_are_candidate_producers", "self_regulation_controls_resources_and_risk", "self_calibration_requires_history", "parameter_governance_required", "hive_observer_only", "genome_not_identity", "b_route_separate", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_DYNAMIC_FUNCTION_SELF_ADAPTIVE_INTEGRATION_ARCHITECTURE_READY", "summary_status")
    check(summary["layers"] == ["Self Constitution", "Self Regulation Function", "Dynamic Cognitive Function", "Cognitive Capability Modules", "Self Calibration Function", "Adaptive Parameter Candidate", "Self Review"] and summary["mapping_functions"] == 10 and summary["self_regulation"] is True and summary["self_calibration"] is True and summary["adaptive_parameter_governance"] is True and summary["cognitive_genome"] is True and summary["hive_observation"] is True and summary["legacy_architecture_preserved"] is True, "summary_model")
    check(summary["runtime"] is False and summary["automatic_tuning"] is False and summary["hive_connection"] is False and summary["parameter_update"] is False and summary["self_automatic_modification"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False and summary["model_integration"] is False and summary["hardware_control"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 7 and len(summary["parallel_risks"]) >= 4 and len(summary["future_extensions"]) >= 3, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_DYNAMIC_FUNCTION_SELF_ADAPTIVE_INTEGRATION_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_DYNAMIC_FUNCTION_SELF_ADAPTIVE_INTEGRATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

