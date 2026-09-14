"""V0 static verifier for Luna State Transition Model Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "state_transition_function_schema.json", "core_state_dependency_contract.json",
    "field_transition_contract.json", "understanding_transition_contract.json",
    "goal_transition_contract.json", "value_transition_contract.json",
    "memory_transition_contract.json", "resource_transition_contract.json",
    "self_transition_contract.json", "state_stability_constraint.json",
    "state_momentum_model.json", "state_elasticity_model.json",
    "state_persistence_model.json", "b_route_prediction_mapping.json",
    "hive_state_metric_mapping.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "state_transition_model.md", "core_state_dependency_graph.md",
    "state_stability_model.md", "state_momentum_elasticity_model.md",
    "self_transition_boundary.md", "implementation_plan.md",
]
VERIFIER = "verify_state_transition_model_architecture_v1.py"
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

    schema = load(assets, "state_transition_function_schema.json")
    check(schema["equation"] == "L(t+1)=F(L(t),Reality(t))" and schema["core_states"] == CORE_STATES, "transition_schema")
    check(set(schema["required_fields"]) >= {"transition_id", "source_state_vector", "reality_input", "state_difference", "update_candidates", "constraints", "timestamp", "field_scope", "unknowns", "trace_ref"}, "transition_fields")
    check(schema["state_difference_required"] is True and schema["candidate_updates_only"] is True and schema["automatic_transition"] is False and schema["runtime"] is False and schema["prediction_runtime"] is False, "transition_boundary")

    dependency = load(assets, "core_state_dependency_contract.json")
    check(set(dependency["nodes"]) >= {"Reality", "Field", "Self", "Understanding", "Goal", "Value", "Memory", "Resource", "Action Candidate", "Outcome"}, "dependency_nodes")
    check(set(dependency["allowed_edges"]) >= {"Reality -> Field", "Field -> Understanding", "Memory -> Understanding", "Understanding -> Goal", "Goal -> Value", "Value -> Action Candidate", "Action Candidate -> Outcome", "Outcome -> Memory", "Resource -> Global Regulation", "Self -> Boundary Governance"}, "dependency_edges")
    check(dependency["feedback_edges_are_candidates"] is True and dependency["reality_precedence"] is True and dependency["self_boundary_precedence"] is True and dependency["resource_is_global_constraint"] is True and dependency["direct_execution"] is False and dependency["candidate_only"] is True, "dependency_boundary")

    field = load(assets, "field_transition_contract.json")
    check(field["equation"] == "Field(t+1)=f(Field(t),Reality)" and set(field["inputs"]) >= {"Current Field", "Reality Evidence", "Temporal Continuity", "Spatial Continuity", "Entity Continuity", "Task Continuity", "Role Continuity"}, "field_transition")
    check(set(field["outputs"]) >= {"Field State Update Candidate", "Field Identity Candidate", "Field Transition Candidate", "Field Difference Candidate"} and field["field_is_not_reality"] is True and field["field_does_not_modify_self"] is True and field["field_does_not_execute"] is True and field["automatic_update"] is False and field["candidate_only"] is True, "field_boundary")

    understanding = load(assets, "understanding_transition_contract.json")
    check(understanding["equation"] == "Understanding(t+1)=f(Understanding(t),Evidence,Memory)" and set(understanding["inputs"]) >= {"Current Understanding", "Evidence", "Memory Influence", "Prediction Error", "Field Context", "Unknowns"}, "understanding_transition")
    check(set(understanding["outputs"]) >= {"Understanding Update Candidate", "Belief Confidence Candidate", "Hypothesis Revision Candidate", "Unknown Preservation Candidate"} and understanding["reality_precedence"] is True and understanding["memory_is_context_not_authority"] is True and understanding["single_evidence_not_certainty"] is True and understanding["automatic_update"] is False and understanding["candidate_only"] is True, "understanding_boundary")

    goal = load(assets, "goal_transition_contract.json")
    check(goal["equation"] == "Goal(t+1)=f(Goal(t),Understanding,Value)" and set(goal["inputs"]) >= {"Current Goal", "Understanding", "Value State", "Self Constraint", "Resource State", "Task Context"}, "goal_transition")
    check(set(goal["outputs"]) >= {"Goal Activation Candidate", "Goal Priority Candidate", "Goal Suppression Candidate", "Goal Reconsideration Candidate"} and goal["goal_is_not_action"] is True and goal["goal_is_not_created_automatically"] is True and goal["self_constraint_required"] is True and goal["automatic_update"] is False and goal["candidate_only"] is True, "goal_boundary")

    value = load(assets, "value_transition_contract.json")
    check(set(value["inputs"]) >= {"Goal State", "Benefit", "Cost", "Risk", "Resource State", "Constitution"} and set(value["outputs"]) >= {"Utility Update Candidate", "Priority Candidate", "Hard Constraint Candidate", "Tradeoff Candidate"}, "value_transition")
    check(value["hard_constraints_precede_score"] is True and value["value_is_not_decision_authority"] is True and value["value_is_not_action"] is True and value["automatic_update"] is False and value["candidate_only"] is True, "value_boundary")

    memory = load(assets, "memory_transition_contract.json")
    check(memory["equation"] == "Memory(t+1)=f(Memory(t),Experience,Value)" and set(memory["inputs"]) >= {"Current Memory State", "Validated Experience", "Value State", "Reinforcement", "Temporal Decay", "Context Scope"}, "memory_transition")
    check(set(memory["outputs"]) >= {"Memory Update Candidate", "Pattern Candidate", "Compression Candidate", "Dormancy Candidate"} and memory["memory_is_historical_influence"] is True and memory["memory_is_not_reality"] is True and memory["experience_validation_required"] is True and memory["automatic_memory_write"] is False and memory["candidate_only"] is True, "memory_boundary")

    resource = load(assets, "resource_transition_contract.json")
    check(set(resource["inputs"]) >= {"Current Resource State", "Self Regulation", "Self Rhythm", "Capability Health", "Task Demand", "Field Risk"} and set(resource["outputs"]) >= {"Resource State Candidate", "Attention Budget Candidate", "Compute Budget Candidate", "Exploration Permission Candidate", "Risk Threshold Candidate"}, "resource_transition")
    check(resource["resource_is_constraint_not_goal"] is True and resource["resource_output_is_hint"] is True and resource["resource_does_not_execute"] is True and resource["automatic_resource_control"] is False and resource["candidate_only"] is True, "resource_boundary")

    self_transition = load(assets, "self_transition_contract.json")
    check(self_transition["equation"] == "Self(t+1)=f(Self(t),GrowthCandidate)" and set(self_transition["inputs"]) >= {"Current Self State", "Validated Growth Candidate", "Evidence", "Self Boundary", "Constitution", "Risk", "Reversibility"}, "self_transition")
    check(set(self_transition["stable_core"]) >= {"Identity", "Constitution", "Safety Boundary", "Ownership Boundary"} and set(self_transition["adaptive_targets"]) >= {"Capability", "Strategy", "Cognitive Parameters", "Schema", "Thresholds"}, "self_layers")
    check(set(self_transition["outputs"]) >= {"Self Review Candidate", "Capability Update Candidate", "Strategy Update Candidate", "Reject Candidate", "Defer Candidate"} and self_transition["self_review_required"] is True and self_transition["automatic_self_update"] is False and self_transition["identity_change"] is False and self_transition["constitution_change"] is False and self_transition["candidate_only"] is True, "self_boundary")

    stability = load(assets, "state_stability_constraint.json")
    check(stability["constraint"] == "Delta L < Threshold unless governed exception" and set(stability["inputs"]) >= {"Current State Vector", "Candidate State Vector", "Evidence Strength", "Risk", "Impact", "Time Window", "Self Boundary"}, "stability_constraint")
    check(set(stability["outputs"]) >= {"Stability Review Candidate", "Accept Difference Candidate", "Reject Difference Candidate", "Defer Difference Candidate"} and stability["stable_core_protected"] is True and stability["short_term_noise_does_not_change_identity"] is True and stability["high_risk_reaction_can_be_fast"] is True and stability["threshold_is_field_scoped"] is True and stability["automatic_acceptance"] is False and stability["candidate_only"] is True, "stability_boundary")

    momentum = load(assets, "state_momentum_model.json")
    check(momentum["definition"] == "Past state influence on next state candidate" and set(momentum["inputs"]) >= {"Previous State Vector", "Current Evidence", "Recent Outcome", "Time Since Transition"} and set(momentum["outputs"]) >= {"Momentum Candidate", "Persistence Weight Candidate", "Reconsideration Candidate"}, "momentum_model")
    check(set(momentum["parameters"]) >= {"momentum_weight", "decay_rate", "minimum_persistence_window"} and momentum["field_scoped"] is True and momentum["versioned"] is True and momentum["rollback_required"] is True and momentum["not_scheduler"] is True and momentum["automatic_update"] is False and momentum["candidate_only"] is True, "momentum_boundary")

    elasticity = load(assets, "state_elasticity_model.json")
    check(set(elasticity["inputs"]) >= {"State Difference", "Risk", "Evidence Strength", "Self Regulation", "Current State"} and set(elasticity["outputs"]) >= {"Entry Elasticity Candidate", "Exit Elasticity Candidate", "Hysteresis Candidate"}, "elasticity_model")
    check(set(elasticity["parameters"]) >= {"entry_threshold", "exit_threshold", "recovery_rate", "risk_escalation_rate"} and elasticity["risk_entry_can_be_fast"] is True and elasticity["risk_exit_can_be_slow"] is True and elasticity["not_scheduler"] is True and elasticity["automatic_transition"] is False and elasticity["candidate_only"] is True, "elasticity_boundary")

    persistence = load(assets, "state_persistence_model.json")
    check(persistence["definition"] == "Continuity of one Luna State Vector across time" and set(persistence["inputs"]) >= {"State Vector Version", "Identity Reference", "Field Continuity", "Trace History", "Snapshot Reference"} and set(persistence["outputs"]) >= {"Persistence Candidate", "Continuity Check Candidate", "Restore Candidate"}, "persistence_model")
    check(set(persistence["requirements"]) >= {"stable_identity_ref", "version", "timestamp", "trace_ref", "field_scope"} and persistence["same_subject_continuity"] is True and persistence["reinitialization_without_governance"] is False and persistence["snapshot_is_not_memory"] is True and persistence["runtime"] is False and persistence["candidate_only"] is True, "persistence_boundary")

    b_route = load(assets, "b_route_prediction_mapping.json")
    check(b_route["target"] == "L(t+n)" and set(b_route["inputs"]) >= {"Current Core State Vector", "Candidate Transition Function", "Candidate Parameters", "Candidate Reality Sequence", "Unknowns"} and set(b_route["outputs"]) >= {"Future State Candidate", "Trajectory Candidate", "Risk Candidate", "Alternative Candidate"}, "b_route_mapping")
    check(b_route["b_route_is_simulation_only"] is True and b_route["prediction_is_not_reality"] is True and b_route["virtual_outcome_is_not_experience"] is True and b_route["b_route_cannot_modify_a_state"] is True and b_route["b_route_cannot_update_parameters"] is True and b_route["b_route_runtime"] is False and b_route["candidate_only"] is True, "b_route_boundary")

    hive = load(assets, "hive_state_metric_mapping.json")
    check(hive["comparison_tuple"] == ["State Transition Quality", "Function Parameters", "Outcome Quality"] and set(hive["metrics"]) >= {"state_stability", "goal_achievement", "safety_result", "prediction_error", "resource_efficiency", "recovery_quality", "capability_growth", "continuity_quality"}, "hive_metrics")
    check(set(hive["outputs"]) >= {"Transition Comparison Candidate", "Parameter Improvement Candidate", "Metric Confidence", "Unknowns"} and hive["hive_is_observer_only"] is True and hive["hive_has_no_write_permission"] is True and hive["self_review_required"] is True and hive["automatic_optimization"] is False and hive["hive_runtime"] is False and hive["candidate_only"] is True, "hive_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"State Transition Function", "Field Transition", "Understanding Transition", "Goal Transition", "Value Transition", "Memory Transition", "Resource Transition", "Self Transition", "Stability Constraint", "State Momentum", "State Elasticity", "State Persistence", "B Route Prediction", "Hive State Metrics", "Runtime"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency_contract = load(assets, "dependency_boundary.json")
    required_forbidden = {"Memory -> Override Reality", "Self Transition -> Direct Identity Change", "Self Transition -> Direct Constitution Change", "Stability Constraint -> Automatic Acceptance", "Momentum -> Scheduler", "Elasticity -> Automatic Transition", "Persistence -> Reinitialize Identity", "B Route -> Override A Route", "B Route -> Virtual Outcome as Experience", "B Route -> Update Parameters", "Hive -> Direct State Modification", "Hive -> Direct Parameter Update", "Value -> Execute Action", "Goal -> Execute Action", "Decision -> Reality Mutation", "Runtime -> Transition Authority", "Emotion -> Direct Invariant Change"}
    check(required_forbidden <= set(dependency_contract["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency_contract["no_state_runtime"] is True and dependency_contract["no_prediction_runtime"] is True and dependency_contract["no_scheduler"] is True and dependency_contract["no_automatic_transition"] is True and dependency_contract["no_b_route_runtime"] is True and dependency_contract["no_hive_runtime"] is True and dependency_contract["no_automatic_learning"] is True and dependency_contract["no_identity_change"] is True and dependency_contract["no_constitution_change"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"state_runtime", "prediction_runtime", "scheduler", "automatic_transition", "b_route_runtime", "hive_runtime", "automatic_learning", "identity_change", "constitution_change", "memory_override_reality", "learning_direct_self_update", "single_outcome_direct_memory_write", "self_transition_direct_identity_change", "self_transition_direct_constitution_change", "stability_automatic_acceptance", "momentum_scheduler", "elasticity_automatic_transition", "persistence_reinitialize_identity", "b_route_override_a_route", "b_route_virtual_outcome_experience", "b_route_update_parameters", "hive_direct_state_modification", "hive_direct_parameter_update", "value_execute_action", "goal_execute_action", "decision_reality_mutation", "runtime_transition_authority", "emotion_direct_invariant_change", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("reality_precedence", "seven_state_vector_preserved", "state_difference_required", "stable_core_protected", "momentum_is_not_scheduler", "elasticity_is_not_automatic_transition", "persistence_preserves_identity", "b_route_candidate_only", "hive_observer_only", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_STATE_TRANSITION_MODEL_ARCHITECTURE_READY", "summary_status")
    check(summary["equation"] == "L(t+1)=F(L(t),Reality(t))" and summary["core_states"] == CORE_STATES and summary["dependency_graph"] is True and summary["component_transitions"] is True and summary["stability_constraint"] is True and summary["state_momentum"] is True and summary["state_elasticity"] is True and summary["state_persistence"] is True and summary["b_route_prediction_mapping"] is True and summary["hive_state_metric_mapping"] is True, "summary_model")
    check(summary["runtime"] is False and summary["prediction_runtime"] is False and summary["scheduler"] is False and summary["automatic_transition"] is False and summary["b_route_runtime"] is False and summary["hive_runtime"] is False and summary["automatic_learning"] is False and summary["identity_change"] is False and summary["constitution_change"] is False, "summary_boundary")
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
        print("READINESS: LUNA_COGNITIVE_STATE_TRANSITION_MODEL_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_STATE_TRANSITION_MODEL_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

