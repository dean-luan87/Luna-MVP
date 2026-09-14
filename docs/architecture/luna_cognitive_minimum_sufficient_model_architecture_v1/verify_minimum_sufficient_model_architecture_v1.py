"""V0 static verifier for Luna Minimum Sufficient Cognitive Model Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "luna_state_vector_schema.json", "core_state_registry.json", "state_transition_contract.json",
    "field_state_mapping.json", "self_state_mapping.json", "understanding_state_mapping.json",
    "goal_state_mapping.json", "value_state_mapping.json", "memory_state_mapping.json",
    "resource_state_mapping.json", "cognitive_invariant_contract.json", "stable_core_boundary.json",
    "adaptive_layer_boundary.json", "function_parameter_mapping.json", "hive_metric_mapping.json",
    "b_route_simulation_mapping.json", "ownership_registry.json", "dependency_boundary.json",
    "negative_guards.json", "summary.json",
]
MD_FILES = [
    "minimum_sufficient_cognitive_model.md", "luna_state_vector_model.md",
    "cognitive_invariant_model.md", "module_to_state_mapping.md",
    "dynamic_function_simplification.md", "implementation_plan.md",
]
VERIFIER = "verify_minimum_sufficient_model_architecture_v1.py"
CORE_STATES = ["Field", "Self", "Understanding", "Goal", "Value", "Memory", "Resource"]


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

    vector = load(assets, "luna_state_vector_schema.json")
    check(vector["components"] == CORE_STATES and vector["equation"] == "L(t+1) = F(L(t), Reality(t))", "vector_definition")
    check(set(vector["required_fields"]) >= {"state_vector_id", "version", "timestamp", "field_state", "self_state", "understanding_state", "goal_state", "value_state", "memory_state", "resource_state", "provenance", "unknowns", "trace_ref"}, "vector_fields")
    check(vector["single_core_vector"] is True and vector["vector_is_not_reality"] is True and vector["vector_is_not_database"] is True and vector["vector_is_not_action"] is True and vector["vector_is_not_personality"] is True and vector["candidate_updates_only"] is True and vector["runtime"] is False, "vector_boundary")

    registry = load(assets, "core_state_registry.json")
    states = [item["state"] for item in registry["states"]]
    check(states == CORE_STATES and registry["unique_core_state_owner"] is True, "core_state_registry")
    check(all(item.get("question") and item.get("owner") and item.get("components") for item in registry["states"]), "core_state_fields")
    check(registry["module_is_not_core_state"] is True and registry["second_truth_source_forbidden"] is True and registry["candidate_only"] is True, "core_state_boundary")

    transition = load(assets, "state_transition_contract.json")
    check(transition["equation"] == "L(t+1) = F(L(t), Reality(t))" and set(transition["inputs"]) >= {"Current Luna State Vector", "Reality Evidence", "Field Transition", "Self Constraint", "Outcome Feedback"}, "transition_inputs")
    check(set(transition["outputs"]) >= {"State Vector Update Candidate", "Function Parameter Candidate", "Reconsideration Candidate", "No Change Candidate"} and set(transition["transition_metadata"]) >= {"source", "field_scope", "timestamp", "confidence", "unknowns", "trace_ref"}, "transition_outputs")
    check(transition["reality_precedence"] is True and transition["automatic_state_update"] is False and transition["direct_action"] is False and transition["direct_identity_change"] is False and transition["candidate_only"] is True and transition["runtime"] is False, "transition_boundary")

    field = load(assets, "field_state_mapping.json")
    check(field["core_state"] == "Field" and set(field["components"]) == {"space", "time", "environment", "relationships", "events"}, "field_mapping")
    check(set(field["source_modules"]) >= {"Cognitive Field", "Field Temporal Evolution", "External Evidence", "Social Self", "Role"} and set(field["outputs"]) >= {"Field State Candidate", "Field Transition Candidate", "Field Influence Candidate"}, "field_mapping_io")
    check(field["field_is_not_reality"] is True and field["field_is_input_state_space"] is True and field["field_does_not_override_self"] is True and field["candidate_only"] is True, "field_boundary")

    self_state = load(assets, "self_state_mapping.json")
    check(self_state["core_state"] == "Self" and self_state["components"] == ["identity", "capability", "boundary", "regulation"], "self_mapping")
    check(set(self_state["stable_core"]) >= {"Identity", "Constitution", "Safety Boundary", "Ownership Boundary"} and set(self_state["adaptive_layer"]) >= {"Capability", "Strategy", "Cognitive Parameters", "Schema", "Knowledge"}, "self_layers")
    check(set(self_state["source_modules"]) >= {"Self Model", "Self Regulation", "Self Rhythm", "Self Evolution", "Self World Boundary", "Constitution"} and self_state["self_does_not_modify_constitution_automatically"] is True and self_state["self_does_not_modify_identity_automatically"] is True and self_state["candidate_only"] is True, "self_boundary")

    understanding = load(assets, "understanding_state_mapping.json")
    check(understanding["core_state"] == "Understanding" and understanding["components"] == ["belief", "hypothesis", "confidence", "unknowns"], "understanding_mapping")
    check(set(understanding["source_modules"]) >= {"Hypothesis", "Belief", "Expectation", "Reality Validation", "Cognitive Schema", "Attention"} and set(understanding["outputs"]) >= {"Understanding Candidate", "Confidence Update Candidate", "Prediction Error Candidate", "Unknown Preservation Candidate"}, "understanding_io")
    check(understanding["reality_precedence"] is True and understanding["belief_is_not_reality"] is True and understanding["single_evidence_not_certainty"] is True and understanding["candidate_only"] is True, "understanding_boundary")

    goal = load(assets, "goal_state_mapping.json")
    check(goal["core_state"] == "Goal" and goal["components"] == ["intent", "task", "priority", "activation"], "goal_mapping")
    check(set(goal["source_modules"]) >= {"Intent", "Goal", "Task", "Goal Activation Function", "Value Utility"} and set(goal["outputs"]) >= {"Goal Activation Candidate", "Goal Priority Candidate", "Goal Suppression Candidate", "Task Direction Candidate"}, "goal_io")
    check(goal["goal_is_not_action"] is True and goal["goal_is_not_created_by_state_mapping"] is True and goal["self_constraint_required"] is True and goal["candidate_only"] is True, "goal_boundary")

    value = load(assets, "value_state_mapping.json")
    check(value["core_state"] == "Value" and value["components"] == ["benefit", "cost", "risk", "utility"], "value_mapping")
    check(set(value["source_modules"]) >= {"Value Utility", "Cognitive Utility Model", "Self Resource", "Constitution", "Goal"} and set(value["outputs"]) >= {"Utility Candidate", "Priority Candidate", "Hard Constraint Candidate", "Tradeoff Candidate"}, "value_io")
    check(value["hard_constraints_precede_score"] is True and value["value_is_not_decision_authority"] is True and value["value_is_not_action"] is True and value["candidate_only"] is True, "value_boundary")

    memory = load(assets, "memory_state_mapping.json")
    check(memory["core_state"] == "Memory" and memory["components"] == ["activation", "influence", "decay", "context_dependency"], "memory_mapping")
    check(set(memory["source_modules"]) >= {"Memory", "Experience", "Information Lifecycle", "Knowledge Boundary", "Schema"} and set(memory["outputs"]) >= {"Historical Influence Candidate", "Memory Activation Candidate", "Pattern Candidate", "Context Dependency Candidate"}, "memory_io")
    check(memory["memory_is_historical_influence"] is True and memory["memory_is_not_reality"] is True and memory["memory_does_not_override_current_field"] is True and memory["automatic_memory_write"] is False and memory["candidate_only"] is True, "memory_boundary")

    resource = load(assets, "resource_state_mapping.json")
    check(resource["core_state"] == "Resource" and resource["components"] == ["compute", "time", "energy", "attention", "network", "storage"], "resource_mapping")
    check(set(resource["source_modules"]) >= {"Self Regulation", "Self Rhythm", "Capability Governance", "Runtime Health", "Resource Governance"} and set(resource["outputs"]) >= {"Resource Budget Candidate", "Capability Budget Candidate", "Attention Budget Candidate", "Risk Threshold Candidate"}, "resource_io")
    check(resource["resource_is_constraint_not_goal"] is True and resource["resource_output_is_hint"] is True and resource["resource_does_not_execute"] is True and resource["automatic_resource_control"] is False and resource["candidate_only"] is True, "resource_boundary")

    invariant = load(assets, "cognitive_invariant_contract.json")
    check(set(invariant["invariants"]) >= {"Reality Priority", "Safety", "Ownership", "Self Identity", "Constitution", "Unknown Preservation", "Unique State Owner"}, "invariant_set")
    check(invariant["stable_core"] is True and invariant["invariant_is_not_parameter"] is True and invariant["invariant_is_not_goal"] is True and invariant["invariant_is_not_utility_score"] is True and invariant["invariant_violation_is_non_compensatory"] is True and invariant["review_required_for_change"] is True and invariant["automatic_change"] is False and invariant["candidate_only"] is True, "invariant_boundary")

    stable = load(assets, "stable_core_boundary.json")
    check(set(stable["stable_core"]) >= {"Reality Priority", "Constitution", "Identity", "Safety Boundary", "Ownership Boundary", "Unknown Preservation", "Unique State Owner"}, "stable_core")
    check(set(stable["change_requires"]) >= {"Constitution Governance", "Self Review", "Evidence", "Impact Analysis", "Explicit Change Control"} and stable["automatic_change"] is False and stable["direct_learning_change"] is False and stable["direct_hive_change"] is False and stable["direct_b_route_change"] is False and stable["candidate_only"] is True, "stable_boundary")

    adaptive = load(assets, "adaptive_layer_boundary.json")
    check(set(adaptive["adaptive_layer"]) >= {"Capability", "Strategy", "Cognitive Parameters", "Schema", "Knowledge", "Thresholds", "Weights"}, "adaptive_layer")
    check(set(adaptive["allowed_change_sources"]) >= {"Validated Experience", "Outcome Evaluation", "Selective Learning", "Self Calibration", "Approved Optimization Candidate"} and set(adaptive["change_requires"]) >= {"Field Scope", "Evidence", "Utility", "Risk", "Reversibility", "Self Review", "Versioning", "Rollback"}, "adaptive_governance")
    check(set(adaptive["protected_targets"]) >= {"Constitution", "Identity", "Safety Boundary", "Reality", "Core Brain Rules"} and adaptive["automatic_change"] is False and adaptive["model_training"] is False and adaptive["parameter_update"] is False and adaptive["candidate_only"] is True, "adaptive_boundary")

    function_params = load(assets, "function_parameter_mapping.json")
    check([item["state"] for item in function_params["mapping"]] == CORE_STATES and all(item["functions"] and item["parameters"] for item in function_params["mapping"]), "function_parameter_mapping")
    check(function_params["parameters_are_bounded"] is True and function_params["field_scope_required"] is True and function_params["version_required"] is True and function_params["rollback_required"] is True and function_params["automatic_update"] is False and function_params["candidate_only"] is True, "function_parameter_boundary")

    hive = load(assets, "hive_metric_mapping.json")
    check(hive["comparison_tuple"] == ["Luna State Vector", "Function Parameters", "Outcome Quality"] and set(hive["metrics"]) >= {"goal_achievement", "safety_result", "resource_efficiency", "understanding_accuracy", "prediction_error", "capability_stability", "learning_value", "recovery_quality"}, "hive_metrics")
    check(set(hive["outputs"]) >= {"State Comparison Candidate", "Parameter Improvement Candidate", "Metric Confidence", "Unknowns"} and hive["hive_is_observer_only"] is True and hive["hive_has_no_write_permission"] is True and hive["privacy_scope_required"] is True and hive["self_review_required"] is True and hive["automatic_optimization"] is False and hive["candidate_only"] is True, "hive_boundary")

    b_route = load(assets, "b_route_simulation_mapping.json")
    check(b_route["simulation_target"] == "L(t+n)" and set(b_route["inputs"]) >= {"Current Luna State Vector", "Candidate Function Parameters", "Candidate Field Evolution", "Unknowns"} and set(b_route["outputs"]) >= {"Future State Candidate", "Outcome Candidate", "Risk Candidate", "Reconsideration Candidate"}, "b_route_mapping")
    check(b_route["b_route_is_future_interface_only"] is True and b_route["b_route_does_not_override_a_route"] is True and b_route["b_route_does_not_modify_self"] is True and b_route["b_route_does_not_turn_virtual_outcome_into_experience"] is True and b_route["b_route_does_not_update_parameters"] is True and b_route["b_route_runtime"] is False and b_route["candidate_only"] is True, "b_route_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    states_owned = [item["state"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(states_owned) == len(set(states_owned)), "unique_owners")
    check({"Field", "Self", "Understanding", "Goal", "Value", "Memory", "Resource", "Cognitive Invariant", "Runtime", "Hive Metrics", "B Route Simulation"} <= set(states_owned), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Memory -> Override Reality", "Learning -> Direct Constitution Change", "Hive -> Direct State Modification", "Hive -> Direct Parameter Update", "B Route -> Override A Route", "B Route -> Direct Self Modification", "B Route -> Virtual Outcome as Experience", "Value -> Execute Action", "Goal -> Execute Action", "Decision -> Direct Reality Mutation", "Module -> Create Second Core Vector", "Emotion -> Direct Invariant Change"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_runtime"] is True and dependency["no_state_machine_runtime"] is True and dependency["no_hive_runtime"] is True and dependency["no_b_route_runtime"] is True and dependency["no_automatic_learning"] is True and dependency["no_automatic_parameter_update"] is True and dependency["no_identity_change"] is True and dependency["no_constitution_change"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "state_machine_runtime", "hive_runtime", "b_route_runtime", "automatic_learning", "automatic_parameter_update", "identity_change", "constitution_change", "memory_override_reality", "memory_direct_identity_change", "experience_direct_self_modification", "learning_direct_constitution_change", "learning_direct_identity_change", "hive_direct_state_modification", "hive_direct_parameter_update", "b_route_override_a_route", "b_route_direct_self_modification", "b_route_virtual_outcome_experience", "value_execute_action", "goal_execute_action", "decision_direct_reality_mutation", "resource_direct_hardware_control", "module_second_core_vector", "emotion_direct_invariant_change", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("seven_core_states", "single_core_vector", "stable_core_protected", "adaptive_layer_requires_governance", "reality_precedence", "unique_state_owner", "hive_observer_only", "b_route_candidate_only", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_MINIMUM_SUFFICIENT_MODEL_ARCHITECTURE_READY", "summary_status")
    check(summary["core_states"] == CORE_STATES and summary["equation"] == "L(t+1) = F(L(t), Reality(t))" and summary["single_core_vector"] is True and summary["cognitive_invariants"] is True and summary["stable_core"] is True and summary["adaptive_layer"] is True and summary["hive_metric_mapping"] is True and summary["b_route_simulation_mapping"] is True, "summary_model")
    check(summary["runtime"] is False and summary["state_machine_runtime"] is False and summary["hive_runtime"] is False and summary["b_route_runtime"] is False and summary["automatic_learning"] is False and summary["automatic_parameter_update"] is False and summary["identity_change"] is False and summary["constitution_change"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_MINIMUM_SUFFICIENT_MODEL_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_MINIMUM_SUFFICIENT_MODEL_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

