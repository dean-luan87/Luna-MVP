"""V0 static verifier for the Cognitive Homeostasis and Adaptive Balance architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "homeostasis_schema.json",
    "state_range_contract.json",
    "adaptive_balance_contract.json",
    "drift_detection_contract.json",
    "stable_core_constraint.json",
    "adaptive_layer_constraint.json",
    "experimental_layer_constraint.json",
    "cognitive_genome_update_boundary.json",
    "state_quality_balance_mapping.json",
    "hive_stability_metric.json",
    "emotion_future_signal_boundary.json",
    "b_route_stability_evaluation.json",
    "ownership_registry.json",
    "dependency_boundary.json",
    "negative_guards.json",
    "summary.json",
]
MD_FILES = [
    "cognitive_homeostasis_model.md",
    "adaptive_balance_model.md",
    "state_range_constraint_model.md",
    "cognitive_drift_detection.md",
    "genome_adaptation_boundary.md",
    "implementation_plan.md",
]
VERIFIER = "verify_homeostasis_adaptive_balance_architecture_v1.py"


def load(assets: dict[str, dict], name: str) -> dict:
    if name not in assets:
        try:
            value = json.loads((ROOT / name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            value = {}
        assets[name] = value if isinstance(value, dict) else {}
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
        value = load(assets, name)
        check(isinstance(value, dict) and bool(value), f"json_parse:{name}")
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

    homeostasis = load(assets, "homeostasis_schema.json")
    check(homeostasis.get("is_constraint_layer") is True and homeostasis.get("is_eighth_state") is False, "homeostasis_constraint_layer")
    check(set(homeostasis.get("inputs", [])) >= {"Core State Vector", "State Quality", "Resource State", "Risk", "Cognitive Invariants", "Field Scope"}, "homeostasis_inputs")
    check(set(homeostasis.get("outputs", [])) >= {"Homeostasis Check Candidate", "Range Adjustment Candidate", "Stability Candidate", "Defer Candidate"} and set(homeostasis.get("required_fields", [])) >= {"homeostasis_id", "state_ref", "range_refs", "quality_ref", "risk", "resource", "field_scope", "timestamp", "confidence", "unknowns", "trace_ref"}, "homeostasis_contract")
    check(homeostasis.get("stable_core_protected") is True and homeostasis.get("automatic_control") is False and homeostasis.get("candidate_only") is True and homeostasis.get("runtime") is False, "homeostasis_boundary")

    ranges = load(assets, "state_range_contract.json")
    check(set(ranges.get("range_fields", [])) >= {"minimum", "preferred", "maximum", "unit", "field_scope", "time_window", "evidence_ref", "version", "rollback_ref"} and ranges.get("minimum_preferred_maximum_required") is True, "state_range_fields")
    check(ranges.get("field_scoped") is True and ranges.get("universal_threshold_forbidden") is True and ranges.get("out_of_range_is_not_automatic_command") is True and ranges.get("candidate_only") is True, "state_range_boundary")

    balance = load(assets, "adaptive_balance_contract.json")
    check(set(balance.get("inputs", [])) >= {"Outcome Quality", "Cognitive Fitness", "Resource Cost", "Risk", "Self Stability", "Drift", "State Range"} and set(balance.get("constraints", [])) >= {"Constitution", "Safety", "Identity", "Ownership", "Resource", "Homeostasis"}, "adaptive_balance_inputs")
    check(balance.get("quality_is_not_maximization_only") is True and balance.get("stability_precedes_optimization") is True and balance.get("drift_penalty_requires_review") is True and balance.get("automatic_adaptation") is False and balance.get("candidate_only") is True, "adaptive_balance_boundary")

    drift = load(assets, "drift_detection_contract.json")
    check(drift.get("equation") == "Drift=Distance(Self_t,Self_{t+n})" and set(drift.get("protected_dimensions", [])) >= {"Identity", "Constitution", "Safety Boundary", "Ownership Boundary"}, "drift_model")
    check(drift.get("field_scoped") is True and drift.get("threshold_required") is True and drift.get("single_event_is_not_identity_drift") is True and drift.get("automatic_self_change") is False and drift.get("candidate_only") is True, "drift_boundary")

    stable = load(assets, "stable_core_constraint.json")
    check(set(stable.get("immutable", [])) >= {"Safety Principles", "Identity", "Reality Priority", "Constitution", "Ownership Boundary", "Unknown Preservation"} and stable.get("violation_is_non_compensatory") is True, "stable_core")
    check(set(stable.get("protected_from", [])) >= {"Optimization", "Learning", "Memory", "Hive", "B Route", "Emotion", "Experimental Parameter"} and stable.get("automatic_change") is False and stable.get("candidate_only") is True, "stable_core_boundary")

    adaptive = load(assets, "adaptive_layer_constraint.json")
    check(set(adaptive.get("adaptive", [])) >= {"Attention Weight", "Exploration Threshold", "Memory Activation", "Strategy", "Capability", "Schema", "Cognitive Parameters"}, "adaptive_layer")
    check(set(adaptive.get("requirements", [])) >= {"Evidence", "Field Scope", "Utility", "Risk", "Reversibility", "Self Review", "Version", "Rollback"} and adaptive.get("stable_core_protection") is True and adaptive.get("automatic_change") is False and adaptive.get("model_training") is False and adaptive.get("candidate_only") is True, "adaptive_layer_boundary")

    experimental = load(assets, "experimental_layer_constraint.json")
    check(set(experimental.get("experimental", [])) >= {"New Strategy", "Unvalidated Threshold", "Candidate Weight", "Prototype Behavior"} and set(experimental.get("requirements", [])) >= {"Isolation", "Field Scope", "Limited Exposure", "Evidence Collection", "Risk Limit", "Rollback", "Self Review"}, "experimental_layer")
    check(set(experimental.get("cannot_modify", [])) >= {"Identity", "Constitution", "Safety Boundary", "Reality", "Core Brain Rules"} and set(experimental.get("promotion_requires", [])) >= {"Repeated Evidence", "State Quality", "Cognitive Fitness", "Stability", "Explicit Admission"} and experimental.get("automatic_promotion") is False and experimental.get("automatic_activation") is False and experimental.get("candidate_only") is True, "experimental_layer_boundary")

    genome = load(assets, "cognitive_genome_update_boundary.json")
    check(set(genome.get("classes", [])) == {"Immutable", "Adaptive", "Experimental"} and set(genome.get("immutable_targets", [])) >= {"Safety", "Identity", "Reality Priority", "Constitution"} and set(genome.get("adaptive_targets", [])) >= {"Attention Weight", "Exploration Threshold", "Memory Activation", "Strategy", "Capability"}, "genome_classes")
    check(set(genome.get("update_flow", [])) >= {"Measurement", "Homeostasis Check", "Drift Check", "Self Review", "Accept/Reject/Defer", "Versioned Candidate"} and genome.get("automatic_update") is False and genome.get("self_review_required") is True and genome.get("rollback_required") is True and genome.get("candidate_only") is True, "genome_update_boundary")

    quality = load(assets, "state_quality_balance_mapping.json")
    check(set(quality.get("inputs", [])) >= {"Outcome Quality", "Cognitive Fitness", "Resource Cost", "Risk", "Self Stability", "Drift", "Homeostasis Status"} and set(quality.get("dimensions", [])) >= {"performance", "stability", "resource_efficiency", "adaptation", "drift", "safety"}, "quality_balance")
    check(quality.get("stability_is_not_secondary") is True and quality.get("high_quality_high_drift_requires_review") is True and quality.get("automatic_optimization") is False and quality.get("candidate_only") is True, "quality_balance_boundary")

    hive = load(assets, "hive_stability_metric.json")
    check(hive.get("comparison_tuple") == ["Outcome Quality", "Cognitive Fitness", "Stability"] and set(hive.get("inputs", [])) >= {"State Quality", "Cognitive Fitness", "Self Stability", "Drift", "Range Compliance", "Recovery Quality"}, "hive_stability_metric")
    check(hive.get("hive_is_observer_only") is True and hive.get("hive_has_no_write_permission") is True and hive.get("field_scope_required") is True and hive.get("self_review_required") is True and hive.get("automatic_optimization") is False and hive.get("hive_runtime") is False and hive.get("candidate_only") is True, "hive_boundary")

    emotion = load(assets, "emotion_future_signal_boundary.json")
    check(emotion.get("future_role") == "Adaptive Signal" and set(emotion.get("outputs", [])) >= {"Homeostasis Influence Candidate", "Risk Weight Adjustment Candidate", "Exploration Modulation Candidate"}, "emotion_signal")
    check(emotion.get("emotion_is_not_decision_signal") is True and emotion.get("emotion_is_not_state_owner") is True and emotion.get("emotion_does_not_modify_identity") is True and emotion.get("emotion_does_not_modify_constitution") is True and emotion.get("emotion_runtime") is False and emotion.get("future_interface_only") is True and emotion.get("candidate_only") is True, "emotion_boundary")

    b_route = load(assets, "b_route_stability_evaluation.json")
    check(set(b_route.get("inputs", [])) >= {"Future State Trajectory", "Outcome Quality Candidate", "Cognitive Fitness Candidate", "Stability Function", "Drift Function", "Unknowns"} and set(b_route.get("outputs", [])) >= {"Stable Trajectory Candidate", "High Drift Candidate", "Homeostasis Risk Candidate", "Alternative Trajectory Candidate"}, "b_route_stability")
    check(b_route.get("b_route_is_simulation_only") is True and b_route.get("future_stability_is_candidate") is True and b_route.get("b_route_does_not_update_a_state") is True and b_route.get("b_route_does_not_modify_self") is True and b_route.get("b_route_does_not_update_genome") is True and b_route.get("b_route_runtime") is False and b_route.get("candidate_only") is True, "b_route_boundary")

    ownership = load(assets, "ownership_registry.json")
    records = ownership.get("ownership", [])
    owners = [item.get("owner") for item in records]
    modules = [item.get("module") for item in records]
    check(ownership.get("unique_owner_required") is True and len(records) >= 13 and len(owners) == len(set(owners)) and len(modules) == len(set(modules)), "unique_owners")
    check({"Homeostasis", "State Range", "Adaptive Balance", "Drift Detection", "Stable Core", "Adaptive Layer", "Experimental Layer", "Cognitive Genome", "State Quality Balance", "Hive Stability Metric", "Emotion Future Signal", "B Route Stability", "Runtime"} <= set(modules), "ownership_coverage")
    check(all(item.get("writer") and item.get("reader") for item in records), "ownership_writer_reader")

    dependency = load(assets, "dependency_boundary.json")
    required_forbidden = {"Homeostasis -> Direct Action", "State Range -> Automatic Control", "Adaptive Balance -> Automatic Optimization", "Drift -> Direct Identity Change", "Drift -> Direct Constitution Change", "Adaptive Layer -> Stable Core Change", "Experimental Layer -> Core Activation", "Genome -> Automatic Update", "Hive -> Direct State Modification", "Hive -> Direct Genome Update", "Emotion -> Direct Decision", "Emotion -> Direct Identity Change", "B Route -> Override A Route", "B Route -> Update State", "B Route -> Update Genome", "Runtime -> Homeostasis Authority", "Quality -> Direct Action"}
    check(required_forbidden <= set(dependency.get("forbidden_dependencies", [])), "dependency_forbidden")
    check(all(dependency.get(key) is True for key in ("no_runtime", "no_automatic_control", "no_automatic_optimization", "no_hive_runtime", "no_b_route_runtime", "no_emotion_runtime", "no_identity_change", "no_constitution_change")), "dependency_boundary")

    guards = load(assets, "negative_guards.json")
    required_guards = {"runtime", "automatic_control", "automatic_optimization", "hive_runtime", "b_route_runtime", "emotion_runtime", "identity_change", "constitution_change", "homeostasis_direct_action", "range_automatic_control", "balance_automatic_optimization", "drift_direct_identity_change", "drift_direct_constitution_change", "adaptive_layer_stable_core_change", "experimental_layer_core_activation", "genome_automatic_update", "hive_direct_state_modification", "hive_direct_genome_update", "emotion_direct_decision", "emotion_direct_identity_change", "b_route_override_a_route", "b_route_update_state", "b_route_update_genome", "runtime_homeostasis_authority", "quality_direct_action", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards.get("forbidden", [])), "negative_guards")
    check(all(guards.get("invariants", {}).get(key) is True for key in ("homeostasis_is_constraint_layer", "stable_core_protected", "adaptive_layer_requires_governance", "experimental_layer_isolated", "drift_requires_review", "stability_balances_quality", "hive_observer_only", "emotion_is_adaptive_signal_only", "b_route_candidate_only", "unknowns_preserved")), "negative_invariants")

    summary = load(assets, "summary.json")
    check(summary.get("status") == "architecture_only" and summary.get("readiness_token") == "LUNA_COGNITIVE_HOMEOSTASIS_ADAPTIVE_BALANCE_ARCHITECTURE_READY", "summary_status")
    check(all(summary.get(key) is True for key in ("homeostasis_constraint_layer", "state_ranges", "adaptive_balance", "drift_detection", "stable_core", "adaptive_layer", "experimental_layer", "genome_update_boundary", "hive_stability_metric", "emotion_future_signal", "b_route_stability_evaluation")), "summary_model")
    check(all(summary.get(key) is False for key in ("runtime", "automatic_control", "automatic_optimization", "hive_runtime", "b_route_runtime", "emotion_runtime", "identity_change", "constitution_change")) and len(summary.get("reusable_assets", [])) >= 4 and len(summary.get("parallel_risks", [])) >= 4 and len(summary.get("future_extensions", [])) >= 3, "summary_boundary")

    forbidden_imports = {"subprocess", "socket", "requests", "cv2", "torch", "transformers", "sqlite3", "psycopg2"}
    try:
        tree = ast.parse((ROOT / VERIFIER).read_text(encoding="utf-8"))
        imports: set[str] = set()
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
        print("READINESS: LUNA_COGNITIVE_HOMEOSTASIS_ADAPTIVE_BALANCE_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_HOMEOSTASIS_ADAPTIVE_BALANCE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
