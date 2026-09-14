"""V0 static contract verifier for Dynamic Function Meta Architecture Refactoring."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "module_function_mapping.json", "function_space_schema.json",
    "field_dynamic_input_contract.json", "attention_function_contract.json",
    "memory_influence_function_contract.json", "self_regulation_function_mapping.json",
    "uncertainty_exploration_function_contract.json", "belief_confidence_dynamics_contract.json",
    "goal_activation_function_contract.json", "utility_decision_function_contract.json",
    "learning_parameter_evolution_contract.json", "parameter_governance_contract.json",
    "cognitive_genome_interface.json", "hive_observation_contract.json",
    "legacy_architecture_compatibility.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "dynamic_function_refactoring_architecture.md", "module_to_function_mapping_model.md",
    "parameter_governance_model.md", "cognitive_genome_governance_model.md",
    "implementation_boundary_plan.md",
]
VERIFIER = "verify_dynamic_function_refactoring_v1.py"
MAPPED_MODULES = ["Field", "Attention", "Memory", "Self Rhythm", "Uncertainty Exploration", "Belief/Understanding", "Goal", "Value Utility", "Decision Arbitration", "Selective Learning"]


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

    mapping = load(assets, "module_function_mapping.json")
    mapped = [item["module"] for item in mapping["mappings"]]
    check(mapped == MAPPED_MODULES, "module_mapping_coverage")
    check(all(item["function_role"] and item["source_phase"] and item["owner_preserved"] is True for item in mapping["mappings"]), "module_mapping_fields")
    check(mapping["mapping_is_not_replacement"] is True and mapping["automatic_migration"] is False and mapping["new_owner_creation"] is False and mapping["runtime"] is False, "module_mapping_boundary")

    space = load(assets, "function_space_schema.json")
    check(len(space["function_spaces"]) == 10 and set(space["function_spaces"]) >= {"field_input_space", "attention_resource_function", "memory_influence_function", "self_regulation_function", "exploration_drive_function", "confidence_dynamics_function", "goal_activation_function", "utility_function", "decision_function", "parameter_evolution_function"}, "function_space")
    check(set(space["required_fields"]) >= {"function_id", "input_refs", "parameter_refs", "output_candidate_types", "field_scope", "owner", "trace_ref", "unknowns"}, "function_space_fields")
    check(space["function_output_is_candidate"] is True and space["function_is_not_runtime"] is True and space["function_is_not_action"] is True and space["function_is_not_decision_authority"] is True and space["bounded_parameters_required"] is True and space["runtime"] is False, "function_space_boundary")

    field = load(assets, "field_dynamic_input_contract.json")
    check(field["field_role"] == "Input State Space" and set(field["inputs"]) >= {"Field State Vector", "Field Influence Weight", "Field Transition Signal", "Temporal Context", "Spatial Context", "Role Context", "Task Context"}, "field_input")
    check(set(field["outputs"]) == {"Cognitive Function Input Candidate", "Field Weight Adjustment Candidate", "Field Transition Candidate"} and field["field_is_not_reality"] is True and field["field_does_not_execute"] is True and field["field_does_not_modify_self"] is True and field["field_does_not_override_constitution"] is True and field["candidate_only"] is True and field["runtime"] is False, "field_boundary")

    attention = load(assets, "attention_function_contract.json")
    check(attention["function_role"] == "Resource Allocation Function" and set(attention["parameters"]) == {"risk_sensitivity", "novelty_sensitivity", "task_sensitivity"}, "attention_function")
    check(set(attention["inputs"]) >= {"Cognitive State Vector", "Self State", "Field State", "Goal Activation", "Risk", "Resource Budget"} and set(attention["outputs"]) >= {"Attention Allocation Candidate", "Resource Distribution Candidate", "Priority Threshold Candidate"}, "attention_io")
    check(attention["attention_is_not_state_owner"] is True and attention["attention_does_not_execute"] is True and attention["attention_does_not_write_memory"] is True and attention["attention_does_not_change_goal"] is True and attention["automatic_allocation"] is False and attention["candidate_only"] is True, "attention_boundary")

    memory = load(assets, "memory_influence_function_contract.json")
    check(memory["function_role"] == "Historical Influence Function" and set(memory["parameters"]) >= {"activation_strength", "influence_weight", "context_dependency", "decay_rate"}, "memory_function")
    check(set(memory["inputs"]) >= {"Current Field", "Memory Layers", "Context Match", "Recency", "Reinforcement", "Memory Reliability"} and set(memory["outputs"]) >= {"Memory Activation Candidate", "Context Influence Candidate", "Historical Comparison Candidate"}, "memory_io")
    check(memory["memory_is_not_reality"] is True and memory["memory_is_not_decision_authority"] is True and memory["memory_does_not_override_current_field"] is True and memory["memory_does_not_create_goal"] is True and memory["automatic_recall"] is False and memory["candidate_only"] is True, "memory_boundary")

    self_map = load(assets, "self_regulation_function_mapping.json")
    check(self_map["parent_function"] == "Self Regulation Function" and self_map["subfunctions"] == ["Rhythm Controller", "Resource Budget", "Risk Boundary", "Evolution Permission"], "self_mapping")
    check(set(self_map["inputs"]) >= {"Self State", "Resource State", "Capability Health", "Self Rhythm", "Constitution"} and set(self_map["outputs"]) >= {"Attention Budget Candidate", "Exploration Budget Candidate", "Compute Budget Candidate", "Risk Threshold Candidate", "Learning Permission Candidate"}, "self_mapping_io")
    check(self_map["self_rhythm_is_subfunction"] is True and self_map["outputs_are_hints"] is True and self_map["does_not_select_decision_alone"] is True and self_map["does_not_switch_model"] is True and self_map["does_not_control_hardware"] is True and self_map["does_not_modify_identity"] is True and self_map["does_not_modify_constitution"] is True and self_map["candidate_only"] is True, "self_mapping_boundary")

    exploration = load(assets, "uncertainty_exploration_function_contract.json")
    check(exploration["function_role"] == "Exploration Drive Function" and set(exploration["parameters"]) == {"uncertainty_tolerance", "information_gain_sensitivity", "exploration_cost_threshold"}, "exploration_function")
    check(set(exploration["inputs"]) >= {"Unknown State", "Uncertainty", "Expected Information Gain", "Exploration Cost", "Risk", "Goal Relevance", "Self Regulation Budget"} and set(exploration["outputs"]) >= {"Exploration Priority Candidate", "Observation Request Candidate", "Defer Exploration Candidate"}, "exploration_io")
    check(exploration["exploration_is_not_action"] is True and exploration["exploration_is_not_learning"] is True and exploration["exploration_does_not_resolve_unknown_automatically"] is True and exploration["hard_safety_constraint"] is True and exploration["automatic_exploration"] is False and exploration["candidate_only"] is True, "exploration_boundary")

    belief = load(assets, "belief_confidence_dynamics_contract.json")
    check(belief["equation"] == "Belief(t+1) = f(Belief(t), Evidence, PredictionError)" and set(belief["parameters"]) >= {"evidence_weight", "prediction_error_sensitivity", "confidence_decay", "contradiction_threshold"}, "belief_function")
    check(set(belief["outputs"]) >= {"Confidence Update Candidate", "Belief Revision Candidate", "Contradiction Candidate", "Unknown Preservation Candidate"} and belief["reality_precedence"] is True and belief["belief_is_not_reality"] is True and belief["single_evidence_is_not_certainty"] is True and belief["automatic_belief_update"] is False and belief["candidate_only"] is True, "belief_boundary")

    goal = load(assets, "goal_activation_function_contract.json")
    check(goal["function_role"] == "Goal Activation Function" and set(goal["parameters"]) >= {"goal_activation_threshold", "task_relevance_weight", "resource_suppression_weight", "risk_priority_weight"}, "goal_function")
    check(set(goal["inputs"]) >= {"Goal Candidates", "Current Field", "Value Utility", "Self State", "Resource State", "Risk", "Task Demand"} and set(goal["outputs"]) >= {"Goal Activation Candidate", "Goal Suppression Candidate", "Goal Reconsideration Candidate", "Goal Priority Candidate"}, "goal_io")
    check(goal["goal_is_not_created_by_function"] is True and goal["goal_is_not_action"] is True and goal["self_constraint_required"] is True and goal["constitution_constraint_required"] is True and goal["automatic_goal_activation"] is False and goal["candidate_only"] is True, "goal_boundary")

    utility = load(assets, "utility_decision_function_contract.json")
    check(utility["utility_equation"] == "Utility = f(Value, Goal, Resource, Risk)" and utility["decision_equation"] == "Decision = f(Understanding, Goal, Value, Self)", "utility_equations")
    check(set(utility["utility_inputs"]) == {"Value", "Goal", "Resource", "Risk"} and set(utility["decision_inputs"]) == {"Understanding", "Goal", "Value", "Self"} and set(utility["outputs"]) >= {"Utility Candidate", "Priority Candidate", "Decision Candidate", "Reconsideration Candidate"}, "utility_io")
    check(utility["hard_constraints_precede_score"] is True and utility["utility_is_not_decision_authority"] is True and utility["decision_is_not_action"] is True and utility["self_has_veto_context"] is True and utility["automatic_decision"] is False and utility["candidate_only"] is True, "utility_boundary")

    learning = load(assets, "learning_parameter_evolution_contract.json")
    check(learning["function_role"] == "Parameter Evolution Function" and set(learning["inputs"]) >= {"Validated Experience", "Pattern/Schema Candidate", "Outcome Evidence", "Learning Utility", "Capability Gap", "Self Review"}, "learning_function")
    check(set(learning["targets"]) >= {"Schema Candidate", "Parameter Adjustment Candidate", "Threshold Candidate", "Weight Candidate", "Capability Growth Candidate"} and set(learning["outputs"]) >= {"Parameter Evolution Candidate", "No Change Candidate", "Defer Candidate", "Reject Candidate"}, "learning_io")
    check(learning["self_review_required"] is True and learning["constitution_review_required"] is True and learning["automatic_learning"] is False and learning["automatic_parameter_update"] is False and learning["automatic_schema_update"] is False and learning["model_training"] is False and learning["identity_change"] is False and learning["candidate_only"] is True, "learning_boundary")

    governance = load(assets, "parameter_governance_contract.json")
    check(set(governance["required_fields"]) >= {"parameter_id", "version", "range", "unit", "field_scope", "provenance", "evidence", "risk", "validation_metric", "rollback_ref"}, "parameter_governance_fields")
    check(governance["lifecycle"] == ["Proposed", "Evaluated", "Reviewed", "Accepted", "Rejected", "Deferred", "Versioned", "RolledBack", "Archived"], "parameter_lifecycle")
    check(set(governance["review_owners"]) == {"Self Governance", "Constitution Governance", "Capability Governance"} and set(governance["hard_constraints"]) >= {"Constitution", "Identity Boundary", "Safety Boundary", "Resource Boundary", "Capability Feasibility"}, "parameter_governance_owners")
    check(governance["automatic_tuning"] is False and governance["cross_field_unscoped_transfer"] is False and governance["evidence_required"] is True and governance["rollback_required"] is True and governance["versioning_required"] is True and governance["candidate_only"] is True, "parameter_governance_boundary")

    genome = load(assets, "cognitive_genome_interface.json")
    check(set(genome["genome_inputs"]) >= {"Parameter Space", "Field Scope", "Outcome History", "Risk Profile"} and set(genome["genome_outputs"]) >= {"Genome Profile Candidate", "Comparative Evaluation Candidate", "Parameter Improvement Candidate"}, "genome_interface")
    check(genome["genome_is_not_identity"] is True and genome["genome_is_not_personality_authority"] is True and genome["genome_is_not_decision_authority"] is True and genome["field_scope_required"] is True and genome["version_required"] is True and genome["rollback_required"] is True and genome["self_review_required"] is True and genome["external_write_permission"] is False and genome["candidate_only"] is True, "genome_boundary")

    hive = load(assets, "hive_observation_contract.json")
    check(hive["observation_tuple"] == ["Field", "Cognitive Genome", "Outcome"] and set(hive["outputs"]) == {"Comparative Evidence", "Parameter Improvement Candidate", "Confidence", "Unknowns"}, "hive_observation")
    check(hive["hive_role"] == "observer_and_candidate_provider" and hive["hive_is_not_owner"] is True and hive["hive_has_no_write_permission"] is True and hive["privacy_and_scope_required"] is True and hive["self_review_required"] is True and hive["automatic_optimization"] is False and hive["hive_connection"] is False and hive["candidate_only"] is True, "hive_boundary")

    compatibility = load(assets, "legacy_architecture_compatibility.json")
    check(set(compatibility["preserved_modules"]) >= {"Field", "Memory Layers", "Knowledge Boundary", "Self Boundary", "Value Utility", "Decision Arbitration", "Outcome Evaluation", "Selective Learning"}, "legacy_preservation")
    check(compatibility["mapping_is_additive"] is True and compatibility["old_owner_preserved"] is True and compatibility["old_lifecycle_preserved"] is True and compatibility["old_contracts_remain_canonical"] is True and compatibility["dynamic_layer_is_meta_architecture"] is True and compatibility["file_move"] is False and compatibility["file_delete"] is False and compatibility["code_refactor"] is False and compatibility["module_replacement"] is False and compatibility["runtime_activation"] is False and compatibility["automatic_migration"] is False, "legacy_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Module Function Mapping", "Function Space", "Field Function", "Attention Function", "Memory Influence Function", "Self Regulation Function", "Exploration Function", "Belief Confidence Function", "Goal Activation Function", "Utility Decision Function", "Parameter Evolution Function", "Parameter Governance", "Cognitive Genome", "Hive Observation", "Self", "Constitution", "Runtime", "B Route"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Meta Function -> Replace Legacy Module", "Meta Function -> Direct Reality Mutation", "Meta Function -> Execute Action", "Attention Function -> Direct State Mutation", "Self Regulation -> Switch Model", "Self Regulation -> Hardware Control", "Goal Function -> Direct Action", "Utility Function -> Commit Decision", "Decision Function -> Execute Action", "Learning Function -> Automatic Parameter Update", "Hive -> Direct Luna Modification", "Hive -> Parameter Write", "Genome -> Identity Change", "B Route -> Direct Parameter Adoption", "Runtime -> Parameter Authority", "Emotion -> Direct Parameter Adoption"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_code_refactor"] is True and dependency["no_file_move"] is True and dependency["no_module_replacement"] is True and dependency["no_runtime"] is True and dependency["no_automatic_tuning"] is True and dependency["no_hive_connection"] is True and dependency["no_parameter_learning"] is True and dependency["no_self_automatic_modification"] is True and dependency["no_emotion_runtime"] is True and dependency["no_b_route_runtime"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"code_refactor", "file_move", "module_replacement", "runtime", "automatic_tuning", "hive_connection", "parameter_learning", "automatic_self_modification", "emotion_runtime", "b_route_runtime", "meta_function_replace_module", "meta_function_reality_mutation", "meta_function_execute_action", "field_function_reality_authority", "attention_function_direct_state_mutation", "memory_influence_override_reality", "self_regulation_switch_model", "self_regulation_hardware_control", "exploration_resolve_unknown", "belief_create_reality", "goal_direct_action", "utility_commit_decision", "decision_execute_action", "learning_automatic_parameter_update", "learning_model_training", "hive_direct_luna_modification", "hive_parameter_write", "genome_identity_change", "parameter_constitution_change", "b_route_direct_parameter_adoption", "runtime_parameter_authority", "emotion_direct_parameter_adoption", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("legacy_modules_preserved", "mapping_is_meta_architecture", "owners_preserved", "candidate_outputs", "self_review_required", "constitution_precedence", "hive_observer_only", "genome_not_identity", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_ARCHITECTURE_DYNAMIC_FUNCTION_REFACTORING_READY", "summary_status")
    check(summary["meta_architecture"] is True and set(summary["preserved_modules"]) >= {"Field", "Memory Layers", "Knowledge Boundary", "Self Boundary", "Value Utility", "Decision Arbitration", "Outcome Evaluation", "Selective Learning"} and summary["function_mapping_count"] == 10 and summary["parameter_governance"] is True and summary["cognitive_genome"] is True and summary["hive_observation_interface"] is True and summary["self_review_required"] is True, "summary_model")
    check(summary["runtime"] is False and summary["code_refactor"] is False and summary["file_move"] is False and summary["module_replacement"] is False and summary["automatic_tuning"] is False and summary["hive_connection"] is False and summary["parameter_learning"] is False and summary["self_automatic_modification"] is False and summary["emotion_runtime"] is False and summary["b_route_runtime"] is False and summary["model_integration"] is False and summary["hardware_integration"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_ARCHITECTURE_DYNAMIC_FUNCTION_REFACTORING_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_ARCHITECTURE_DYNAMIC_FUNCTION_REFACTORING_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

