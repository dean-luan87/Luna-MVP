"""V0 static verifier for Cognitive State Observation and Measurement Architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "state_observation_function_schema.json", "cognitive_metric_registry.json",
    "state_quality_contract.json", "understanding_metric.json",
    "decision_quality_metric.json", "memory_utility_metric.json",
    "self_stability_metric.json", "adaptation_efficiency_metric.json",
    "cognitive_fitness_contract.json", "hive_metric_interface.json",
    "self_calibration_metric_relation.json", "b_route_evaluation_mapping.json",
    "state_transition_quality_mapping.json", "ownership_registry.json",
    "dependency_boundary.json", "negative_guards.json", "summary.json",
]
MD_FILES = [
    "cognitive_state_observation_model.md", "cognitive_metric_system.md",
    "state_quality_model.md", "cognitive_fitness_model.md",
    "hive_measurement_interface.md", "implementation_plan.md",
]
VERIFIER = "verify_state_observation_measurement_architecture_v1.py"
METRICS = ["field_understanding_score", "understanding_stability", "uncertainty_management_score", "decision_quality", "memory_utility", "self_stability", "adaptation_efficiency"]


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

    observation = load(assets, "state_observation_function_schema.json")
    check(observation["equation"] == "O_t=H(L_t)" and set(observation["inputs"]) >= {"Core State Vector", "State Transition Trace", "Field Scope", "Observation Window"}, "observation_function")
    check(set(observation["outputs"]) >= {"Observation Candidate", "Metric Input Candidate", "Unknowns", "Confidence"} and set(observation["required_fields"]) >= {"observation_id", "state_vector_ref", "metric_id", "field_scope", "window", "source", "timestamp", "confidence", "unknowns", "trace_ref"}, "observation_fields")
    check(observation["observation_is_not_full_state"] is True and observation["observation_is_not_reality"] is True and observation["read_only"] is True and observation["automatic_state_write"] is False and observation["candidate_only"] is True and observation["runtime"] is False, "observation_boundary")

    registry = load(assets, "cognitive_metric_registry.json")
    check([item["metric_id"] for item in registry["metrics"]] == METRICS, "metric_registry")
    check(all(item.get("name") and item.get("direction") and item.get("scope") for item in registry["metrics"]), "metric_registry_fields")
    check(registry["single_reward_forbidden"] is True and registry["metric_is_not_decision_authority"] is True and registry["metric_is_not_identity"] is True and registry["candidate_only"] is True, "metric_registry_boundary")

    quality = load(assets, "state_quality_contract.json")
    check(quality["equation"] == "Q_t=f(L_t,Outcome_t)" and set(quality["inputs"]) >= {"State Vector", "Outcome", "Goal Context", "Safety Result", "Resource Cost", "Understanding Change", "Continuity", "Unknowns"}, "quality_function")
    check(set(quality["outputs"]) >= {"State Quality Candidate", "Quality Dimension Candidates", "Confidence", "Limitations"} and set(quality["dimensions"]) >= {"goal_achievement", "safety", "resource_efficiency", "understanding_correction", "continuity", "uncertainty_management"}, "quality_dimensions")
    check(quality["single_outcome_is_not_long_term_quality"] is True and quality["quality_is_not_decision"] is True and quality["quality_is_not_parameter_update"] is True and quality["repeated_evidence_required_for_calibration"] is True and quality["candidate_only"] is True, "quality_boundary")

    understanding = load(assets, "understanding_metric.json")
    check(set(understanding["metrics"]) >= {"field_identification_accuracy", "entity_relation_accuracy", "change_detection", "understanding_stability", "reasonable_revision"} and set(understanding["inputs"]) >= {"Field State", "Evidence", "Understanding Candidate", "Validation Result", "Prediction Error"}, "understanding_metric")
    check(set(understanding["outputs"]) >= {"Field Understanding Score Candidate", "Understanding Stability Candidate", "Correction Quality Candidate"} and understanding["confidence_calibrated"] is True and understanding["error_persistence_is_penalized"] is True and understanding["reasonable_revision_is_rewarded"] is True and understanding["automatic_belief_update"] is False and understanding["candidate_only"] is True, "understanding_boundary")

    decision = load(assets, "decision_quality_metric.json")
    check(set(decision["inputs"]) >= {"Decision Candidate", "Available Information", "Goal", "Value", "Risk", "Resource Cost", "Outcome"} and set(decision["dimensions"]) >= {"information_use", "risk_judgment", "cost_control", "reversibility", "constraint_compliance", "outcome_alignment"}, "decision_metric")
    check(set(decision["outputs"]) >= {"Decision Quality Candidate", "Process Quality Candidate", "Tradeoff Candidate"} and decision["outcome_success_is_not_only_metric"] is True and decision["decision_metric_does_not_execute"] is True and decision["automatic_decision_change"] is False and decision["candidate_only"] is True, "decision_boundary")

    memory = load(assets, "memory_utility_metric.json")
    check(set(memory["inputs"]) >= {"Memory Influence", "Current Understanding", "Field Context", "Decision Quality", "Outcome", "Counterfactual Memory Omission Candidate"} and set(memory["outputs"]) >= {"Memory Utility Candidate", "Activation Relevance Candidate", "Influence Cost Candidate"}, "memory_metric")
    check(memory["utility_is_improvement_contribution"] is True and memory["more_memory_is_not_always_better"] is True and memory["memory_is_not_reality"] is True and memory["automatic_memory_write"] is False and memory["candidate_only"] is True, "memory_boundary")

    self_metric = load(assets, "self_stability_metric.json")
    check(set(self_metric["inputs"]) >= {"Self State", "Identity Reference", "Constitution", "Safety Boundary", "Outcome Sequence", "State Difference", "Recovery Trace"} and set(self_metric["outputs"]) >= {"Self Stability Candidate", "Continuity Candidate", "Boundary Preservation Candidate", "Recovery Candidate"}, "self_metric")
    check(set(self_metric["dimensions"]) >= {"identity_continuity", "boundary_preservation", "invariant_compliance", "recovery_quality"} and self_metric["short_term_failure_does_not_define_identity"] is True and self_metric["stable_core_protected"] is True and self_metric["metric_does_not_modify_self"] is True and self_metric["candidate_only"] is True, "self_boundary")

    adaptation = load(assets, "adaptation_efficiency_metric.json")
    check(set(adaptation["inputs"]) >= {"Initial State", "Adapted State", "Outcome Improvement", "Resource Cost", "Time", "Risk", "Reversibility"} and set(adaptation["outputs"]) >= {"Adaptation Efficiency Candidate", "Gain per Cost Candidate", "Time to Stable Candidate", "Risk Adjusted Gain Candidate"}, "adaptation_metric")
    check(set(adaptation["dimensions"]) >= {"improvement_gain", "resource_efficiency", "time_efficiency", "stability_after_adaptation", "risk_adjustment"} and adaptation["automatic_adaptation"] is False and adaptation["metric_does_not_update_parameter"] is True and adaptation["candidate_only"] is True, "adaptation_boundary")

    fitness = load(assets, "cognitive_fitness_contract.json")
    check(fitness["equation"] == "Fitness=f(Understanding,Decision,Resource,Adaptation,Self Stability)" and set(fitness["inputs"]) >= {"Understanding Metrics", "Decision Quality", "Resource Efficiency", "Adaptation Efficiency", "Self Stability", "Field Scope"}, "fitness_function")
    check(set(fitness["outputs"]) >= {"Cognitive Fitness Candidate", "Fitness Dimensions", "Confidence", "Unknowns"} and set(fitness["dimensions"]) == {"understanding", "decision", "resource", "adaptation", "self_stability"}, "fitness_dimensions")
    check(fitness["fitness_is_field_specific"] is True and fitness["fitness_is_not_competition"] is True and fitness["fitness_is_not_user_reward"] is True and fitness["fitness_is_not_decision_authority"] is True and fitness["cross_field_normalization_required"] is True and fitness["candidate_only"] is True, "fitness_boundary")

    hive = load(assets, "hive_metric_interface.json")
    check(hive["input_tuple"] == ["State Vector", "Transition Pattern", "Outcome Quality"] and set(hive["inputs"]) >= {"State Observation", "Transition Trace", "Metric Candidates", "Field Scope", "Genome/Parameter Version"}, "hive_interface")
    check(set(hive["outputs"]) >= {"Comparative Evidence", "Metric Confidence", "State Quality Candidate", "Optimization Candidate", "Unknowns"} and hive["hive_is_observer_only"] is True and hive["hive_has_no_write_permission"] is True and hive["privacy_scope_required"] is True and hive["self_review_required"] is True and hive["automatic_optimization"] is False and hive["hive_connection"] is False and hive["candidate_only"] is True, "hive_boundary")

    calibration = load(assets, "self_calibration_metric_relation.json")
    check(calibration["flow"] == ["State Observation", "Metric Candidates", "State Quality", "Outcome", "Calibration Candidate", "Self Review"], "calibration_flow")
    check(set(calibration["inputs"]) >= {"State Quality", "Prediction Error", "Capability Performance", "Long Term Pattern", "Self Stability", "Resource Efficiency"} and set(calibration["outputs"]) >= {"Calibration Candidate", "Metric Weight Candidate", "Parameter Improvement Candidate", "No Change Candidate"}, "calibration_io")
    check(calibration["repeated_evidence_required"] is True and calibration["field_scope_required"] is True and calibration["self_review_required"] is True and calibration["automatic_calibration"] is False and calibration["automatic_parameter_update"] is False and calibration["candidate_only"] is True, "calibration_boundary")

    b_route = load(assets, "b_route_evaluation_mapping.json")
    check(set(b_route["inputs"]) >= {"Predicted State Trajectory", "Predicted Outcomes", "State Quality Function", "Cognitive Fitness Function", "Unknowns"} and set(b_route["outputs"]) >= {"Trajectory Quality Candidate", "Future Fitness Candidate", "Risk Candidate", "Alternative Candidate"}, "b_route_mapping")
    check(b_route["b_route_is_simulation_only"] is True and b_route["predicted_quality_is_not_actual_quality"] is True and b_route["virtual_outcome_is_not_experience"] is True and b_route["b_route_cannot_update_state"] is True and b_route["b_route_cannot_update_parameters"] is True and b_route["b_route_runtime"] is False and b_route["candidate_only"] is True, "b_route_boundary")

    transition_quality = load(assets, "state_transition_quality_mapping.json")
    check(set(transition_quality["inputs"]) >= {"Previous State", "Next State Candidate", "State Difference", "Transition Function", "Outcome", "Stability Constraint"} and set(transition_quality["outputs"]) >= {"Transition Quality Candidate", "Stability Candidate", "Efficiency Candidate", "Continuity Candidate"}, "transition_quality")
    check(set(transition_quality["dimensions"]) >= {"directional_improvement", "stability", "resource_cost", "reversibility", "continuity", "outcome_alignment"} and transition_quality["state_difference_required"] is True and transition_quality["quality_is_not_automatic_transition"] is True and transition_quality["candidate_only"] is True, "transition_quality_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership["ownership"]
    owners = [item["owner"] for item in records]
    modules = [item["module"] for item in records]
    check(ownership["unique_owner_required"] is True and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"State Observation", "Cognitive Metrics", "State Quality", "Field Understanding Metric", "Decision Quality Metric", "Memory Utility Metric", "Self Stability Metric", "Adaptation Efficiency Metric", "Cognitive Fitness", "Hive Metrics", "Self Calibration", "B Route Evaluation", "Transition Quality", "Runtime"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Observation -> State Write", "Metric -> Direct Decision", "Metric -> Direct Action", "Quality -> Automatic Parameter Update", "Fitness -> Identity Change", "Fitness -> Constitution Change", "Memory Utility -> Reality Override", "Hive -> Direct State Modification", "Hive -> Direct Parameter Update", "Self Calibration -> Automatic Calibration", "B Route -> Actual Quality Claim", "B Route -> Virtual Outcome as Experience", "B Route -> Update State", "Runtime -> Metric Authority", "Emotion -> Metric Override"}
    check(required_forbidden <= set(dependency["forbidden_dependencies"]), "dependency_forbidden")
    check(dependency["no_runtime"] is True and dependency["no_automatic_scoring_action"] is True and dependency["no_automatic_optimization"] is True and dependency["no_hive_connection"] is True and dependency["no_b_route_runtime"] is True and dependency["no_parameter_update"] is True and dependency["no_self_modification"] is True, "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "automatic_scoring_action", "automatic_optimization", "hive_connection", "b_route_runtime", "parameter_update", "self_modification", "observation_state_write", "metric_direct_decision", "metric_direct_action", "quality_automatic_parameter_update", "fitness_identity_change", "fitness_constitution_change", "memory_utility_reality_override", "hive_direct_state_modification", "hive_direct_parameter_update", "self_calibration_automatic_calibration", "b_route_actual_quality_claim", "b_route_virtual_outcome_experience", "b_route_update_state", "runtime_metric_authority", "emotion_metric_override", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards["forbidden"]), "negative_guards")
    check(all(guards["invariants"].get(key) is True for key in ("observation_is_read_only", "metrics_are_candidates", "quality_is_not_decision", "self_stability_protected", "fitness_is_field_specific", "hive_observer_only", "b_route_prediction_is_not_actual", "calibration_requires_review", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary["status"] == "architecture_only" and summary["readiness_token"] == "LUNA_COGNITIVE_STATE_OBSERVATION_MEASUREMENT_ARCHITECTURE_READY", "summary_status")
    check(summary["observation_equation"] == "O_t=H(L_t)" and summary["quality_equation"] == "Q_t=f(L_t,Outcome_t)" and summary["metrics"] == ["Field Understanding Score", "Understanding Stability", "Uncertainty Management Score", "Decision Quality", "Memory Utility", "Self Stability", "Adaptation Efficiency"] and summary["cognitive_fitness"] is True and summary["hive_measurement"] is True and summary["self_calibration_relation"] is True and summary["b_route_evaluation"] is True and summary["state_transition_quality"] is True, "summary_model")
    check(summary["runtime"] is False and summary["automatic_scoring_action"] is False and summary["automatic_optimization"] is False and summary["hive_connection"] is False and summary["b_route_runtime"] is False and summary["parameter_update"] is False and summary["self_modification"] is False, "summary_boundary")
    check(len(summary["reusable_assets"]) >= 4 and len(summary["parallel_risks"]) >= 4 and len(summary["future_extensions"]) >= 3, "summary_inventory")

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
        print("READINESS: LUNA_COGNITIVE_STATE_OBSERVATION_MEASUREMENT_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_STATE_OBSERVATION_MEASUREMENT_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

