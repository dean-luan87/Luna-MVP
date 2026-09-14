"""V0 static verifier for Self Regulation Function Enhancement architecture."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_FILES = [
    "self_regulation_function_schema_v1.json",
    "self_regulation_subfunction_registry_v1.json",
    "homeostasis_regulation_contract_v1.json",
    "adaptive_regulation_contract_v1.json",
    "calibration_regulation_contract_v1.json",
    "stability_protection_contract_v1.json",
    "self_regulation_function_input_contract_v1.json",
    "self_regulation_function_output_contract_v1.json",
    "self_regulation_parameter_candidate_contract_v1.json",
    "self_regulation_drift_relation_v1.json",
    "self_regulation_measurement_relation_v1.json",
    "self_regulation_genome_relation_v1.json",
    "self_regulation_owner_boundary_v1.json",
    "self_regulation_lifecycle_v1.json",
    "absorption_mapping_v1.json",
    "dependency_boundary_v1.json",
    "negative_guards_v1.json",
    "summary_v1.json",
]
MD_FILES = [
    "self_regulation_function_enhancement_architecture.md",
    "self_regulation_subfunction_model.md",
    "self_regulation_parameter_governance.md",
    "self_regulation_stability_and_drift_model.md",
    "implementation_plan.md",
    "self_regulation_function_enhancement_whitebox_v1.md",
    "self_regulation_function_enhancement_go_no_go_v1.md",
]
VERIFIER = "verify_self_regulation_function_enhancement_v1.py"


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

    function = load(assets, "self_regulation_function_schema_v1.json")
    check(function.get("canonical_owner") == "Self Regulation Function" and function.get("equation") == "R_t=f(Self_t,Resource_t,Constitution,State_t)", "function_owner_equation")
    check(set(function.get("inputs", [])) >= {"Self State", "Resource State", "Cognitive State", "Field Scope", "Measurement Evidence", "Outcome/Error Evidence", "Goal Context", "Constitution"}, "function_inputs")
    check(set(function.get("subfunctions", [])) == {"Homeostasis Regulation", "Resource Regulation", "Cognitive Balance Regulation", "Calibration Regulation", "Adaptive Regulation", "Stability Protection"}, "function_subfunctions")
    check(set(function.get("outputs", [])) >= {"Regulation Strategy Candidate", "Parameter Candidate", "Permission Candidate", "Stability Candidate", "Defer Candidate", "Reject Candidate"} and function.get("candidate_only") is True and function.get("automatic_update") is False and function.get("automatic_control") is False and function.get("runtime") is False, "function_boundary")

    registry = load(assets, "self_regulation_subfunction_registry_v1.json")
    subfunctions = registry.get("subfunctions", [])
    check(registry.get("canonical_owner") == "Self Regulation Function" and registry.get("unique_owner_required") is True and len(subfunctions) == 6, "subfunction_registry")
    check(all(item.get("purpose") and item.get("output") for item in subfunctions) and registry.get("independent_homeostasis_owner") is False and registry.get("independent_calibration_owner") is False and registry.get("independent_adaptation_owner") is False, "subfunction_owner_boundary")

    homeostasis = load(assets, "homeostasis_regulation_contract_v1.json")
    check(homeostasis.get("owner") == "Self Regulation Function" and homeostasis.get("is_internal_mechanism") is True and homeostasis.get("is_independent_layer") is False, "homeostasis_internal")
    check(set(homeostasis.get("range_fields", [])) >= {"minimum", "preferred", "maximum", "unit", "field_scope", "time_window", "evidence_ref", "version", "rollback_ref"} and homeostasis.get("automatic_control") is False and homeostasis.get("candidate_only") is True, "homeostasis_boundary")

    adaptive = load(assets, "adaptive_regulation_contract_v1.json")
    check(adaptive.get("owner") == "Self Regulation Function" and adaptive.get("is_internal_mechanism") is True and set(adaptive.get("constraints", [])) >= {"Constitution", "Stable Core", "Safety", "Ownership", "Reversibility", "Field Scope"}, "adaptive_regulation")
    check(adaptive.get("automatic_parameter_update") is False and adaptive.get("self_review_required") is True and adaptive.get("candidate_only") is True, "adaptive_regulation_boundary")

    calibration = load(assets, "calibration_regulation_contract_v1.json")
    check(calibration.get("owner") == "Self Regulation Function" and calibration.get("is_internal_mechanism") is True and set(calibration.get("inputs", [])) >= {"State Observation", "State Quality", "Outcome", "Prediction Error", "Long Term Pattern", "Resource Efficiency", "Self Stability"}, "calibration_regulation")
    check(set(calibration.get("requirements", [])) >= {"Repeated Evidence", "Field Scope", "Trace", "Confidence", "Unknowns", "Self Review", "Version", "Rollback"} and calibration.get("automatic_calibration") is False and calibration.get("automatic_parameter_update") is False and calibration.get("candidate_only") is True, "calibration_boundary")

    stability = load(assets, "stability_protection_contract_v1.json")
    check(stability.get("owner") == "Self Regulation Function" and stability.get("is_internal_mechanism") is True and set(stability.get("protected_dimensions", [])) >= {"Identity", "Constitution", "Reality Priority", "Safety", "Ownership"}, "stability_protection")
    check(stability.get("single_event_is_not_identity_drift") is True and stability.get("direct_identity_change") is False and stability.get("direct_constitution_change") is False and stability.get("automatic_rollback") is False and stability.get("candidate_only") is True, "stability_boundary")

    input_contract = load(assets, "self_regulation_function_input_contract_v1.json")
    check(input_contract.get("owner") == "Self Regulation Function" and set(input_contract.get("required_inputs", [])) >= {"Self State", "Resource State", "Cognitive State", "Field Scope", "Constitution", "Measurement Evidence", "Outcome/Error Evidence"}, "input_contract")
    check(set(input_contract.get("input_rules", [])) >= {"evidence_ref_required", "field_scope_required", "timestamp_required", "unknowns_preserved", "confidence_required"} and input_contract.get("emotion_role") == "adaptive_signal_only" and input_contract.get("b_route_role") == "candidate_only" and input_contract.get("reality_is_not_overridden") is True, "input_boundary")

    output_contract = load(assets, "self_regulation_function_output_contract_v1.json")
    check(output_contract.get("owner") == "Self Regulation Function" and set(output_contract.get("outputs", [])) >= {"Regulation Strategy Candidate", "Homeostasis Check Candidate", "Calibration Candidate", "Adaptive Parameter Candidate", "Stability/Veto Candidate", "Permission Candidate", "Defer Candidate", "Reject Candidate"}, "output_contract")
    check(set(output_contract.get("required_fields", [])) >= {"candidate_id", "candidate_type", "source_refs", "field_scope", "reason", "expected_benefit", "resource_cost", "risk", "reversibility", "confidence", "unknowns", "review_status", "version", "rollback_ref", "trace_ref"} and output_contract.get("self_review_required") is True and output_contract.get("runtime_execution") is False and output_contract.get("direct_action") is False and output_contract.get("direct_model_switch") is False and output_contract.get("direct_hardware_control") is False and output_contract.get("candidate_only") is True, "output_boundary")

    parameter = load(assets, "self_regulation_parameter_candidate_contract_v1.json")
    check(set(parameter.get("classes", [])) == {"Immutable", "Adaptive", "Experimental"} and set(parameter.get("immutable_targets", [])) >= {"Constitution", "Identity", "Reality Priority", "Safety", "Ownership Boundary"}, "parameter_classes")
    check(set(parameter.get("adaptive_targets", [])) >= {"Attention Weight", "Exploration Threshold", "Memory Activation", "Strategy", "Capability Policy", "Schema Influence"} and set(parameter.get("review_flow", [])) >= {"Candidate", "Self Review", "Accept", "Reject", "Defer", "Version", "Rollback"} and parameter.get("automatic_update") is False and parameter.get("stable_core_update") is False and parameter.get("model_training") is False and parameter.get("candidate_only") is True, "parameter_boundary")

    drift = load(assets, "self_regulation_drift_relation_v1.json")
    check(drift.get("owner") == "Self Regulation Function" and drift.get("equation") == "Drift=Distance(Self_t,Self_{t+n})" and drift.get("source") == "Cognitive Drift Detection", "drift_relation")
    check(set(drift.get("protected_dimensions", [])) >= {"Identity", "Constitution", "Safety Boundary", "Ownership Boundary"} and drift.get("single_event_is_not_identity_drift") is True and drift.get("drift_does_not_modify_self") is True and drift.get("drift_does_not_modify_constitution") is True and drift.get("automatic_recovery") is False and drift.get("candidate_only") is True, "drift_boundary")

    measurement = load(assets, "self_regulation_measurement_relation_v1.json")
    check(measurement.get("owner") == "Self Regulation Function" and set(measurement.get("sources", [])) >= {"State Observation", "State Quality", "Cognitive Fitness", "Self Stability", "Adaptation Efficiency", "Outcome Evaluation"}, "measurement_relation")
    check(measurement.get("measurement_is_not_authority") is True and measurement.get("measurement_is_not_direct_update") is True and measurement.get("repeated_evidence_required") is True and measurement.get("field_scope_required") is True and measurement.get("self_review_required") is True and measurement.get("automatic_calibration") is False and measurement.get("candidate_only") is True, "measurement_boundary")

    genome = load(assets, "self_regulation_genome_relation_v1.json")
    check(genome.get("owner") == "Self Regulation Function" and genome.get("genome_role") == "parameter_candidate_governance" and genome.get("writes") == [] and set(genome.get("outputs", [])) >= {"Genome Update Candidate", "Genome Reject Candidate", "Genome Defer Candidate"}, "genome_relation")
    check(genome.get("immutable_protected") is True and genome.get("self_review_required") is True and genome.get("rollback_required") is True and genome.get("automatic_genome_update") is False and genome.get("hive_direct_update") is False and genome.get("candidate_only") is True, "genome_boundary")

    owner = load(assets, "self_regulation_owner_boundary_v1.json")
    check(owner.get("canonical_owner") == "Self Regulation Function" and owner.get("subfunction_owner") == "Self Regulation Function" and owner.get("homeostasis_owner") == "Self Regulation Function" and owner.get("calibration_owner") == "Self Regulation Function" and owner.get("adaptation_owner") == "Self Regulation Function" and owner.get("drift_detection_owner") == "Self Regulation Function" and owner.get("single_regulation_owner") is True, "single_regulation_owner")
    check(set(owner.get("self_regulation_can", [])) >= {"Observe", "Assess", "Constrain", "Propose", "Defer", "Reject", "Request Review"} and set(owner.get("self_regulation_cannot", [])) >= {"Execute Action", "Modify Constitution", "Modify Identity", "Modify Goal", "Modify Value", "Modify Brain Core Rules", "Switch Model", "Control Hardware", "Invoke Provider", "Train Model", "Persist Parameter Update"} and owner.get("candidate_only") is True, "owner_permissions")

    lifecycle = load(assets, "self_regulation_lifecycle_v1.json")
    check(lifecycle.get("owner") == "Self Regulation Function" and set(lifecycle.get("states", [])) >= {"Observed", "Assessed", "Candidate", "Range Checked", "Drift Checked", "Under Self Review", "Accepted Candidate", "Rejected", "Deferred", "Applied Externally", "Monitoring", "Rolled Back", "Archived"}, "lifecycle_states")
    check(lifecycle.get("state_owner_required") is True and lifecycle.get("no_implicit_activation") is True and lifecycle.get("rollback_required") is True and lifecycle.get("monitoring_required") is True and lifecycle.get("candidate_only") is True, "lifecycle_boundary")

    absorption = load(assets, "absorption_mapping_v1.json")
    check(absorption.get("canonical_owner") == "Self Regulation Function" and len(absorption.get("mappings", [])) >= 4 and absorption.get("new_homeostasis_owner_created") is False and absorption.get("new_calibration_owner_created") is False and absorption.get("new_adaptation_owner_created") is False, "absorption_mapping")
    check(all(item.get("migration") == "mapping_only" and item.get("file_move") is False and item.get("activation") is False for item in absorption.get("mappings", [])) and absorption.get("code_change") is False and absorption.get("runtime_activation") is False, "absorption_boundary")

    dependency = load(assets, "dependency_boundary_v1.json")
    required_forbidden = {"Homeostasis -> Direct Action", "Homeostasis -> Separate Owner", "Calibration -> Automatic Update", "Adaptation -> Automatic Parameter Update", "Drift -> Direct Identity Change", "Drift -> Direct Constitution Change", "Stability Protection -> Identity Rewrite", "Self Regulation Function -> Direct Action", "Self Regulation Function -> Model Switching", "Self Regulation Function -> Hardware Control", "Self Regulation Function -> Provider Invocation", "Self Regulation Function -> Goal Rewrite", "Self Regulation Function -> Value Rewrite", "Self Regulation Function -> Brain Rule Rewrite", "Self Regulation Function -> Source Code Modification", "Cognitive Genome -> Automatic Update", "Hive -> Direct Self Regulation Update", "Emotion -> Direct Decision", "B Route -> Update A State", "Runtime -> Self Regulation Authority"}
    check(required_forbidden <= set(dependency.get("forbidden_dependencies", [])), "dependency_forbidden")
    check(all(dependency.get(key) is True for key in ("no_runtime", "no_automatic_control", "no_automatic_calibration", "no_automatic_adaptation", "no_model_integration", "no_provider_integration", "no_hardware_control", "no_emotion_runtime", "no_social_runtime")), "dependency_boundary")

    guards = load(assets, "negative_guards_v1.json")
    required_guards = {"new_homeostasis_layer", "second_regulation_owner", "runtime", "scheduler", "automatic_control", "automatic_calibration", "automatic_adaptation", "automatic_parameter_update", "automatic_genome_update", "direct_action", "direct_model_switch", "direct_hardware_control", "provider_invocation", "identity_change", "constitution_change", "goal_rewrite", "value_rewrite", "brain_rule_rewrite", "source_code_modification", "model_training", "hive_direct_update", "emotion_runtime", "social_runtime", "b_route_update_state", "no_check_weaken", "no_hardcoded_pass"}
    check(required_guards <= set(guards.get("forbidden", [])), "negative_guards")
    check(all(guards.get("invariants", {}).get(key) is True for key in ("self_regulation_is_unique_owner", "homeostasis_is_internal_mechanism", "calibration_is_internal_mechanism", "adaptation_is_internal_mechanism", "drift_is_review_signal", "stable_core_protected", "candidates_require_self_review", "runtime_is_external_application_boundary", "unknowns_preserved", "passed_assets_preserved")), "negative_invariants")

    summary = load(assets, "summary_v1.json")
    check(summary.get("status") == "architecture_only" and summary.get("readiness_token") == "LUNA_SELF_REGULATION_FUNCTION_ENHANCEMENT_READY" and summary.get("canonical_owner") == "Self Regulation Function", "summary_status")
    check(all(summary.get(key) is True for key in ("homeostasis_internal", "resource_regulation_internal", "cognitive_balance_internal", "calibration_internal", "adaptation_internal", "stability_protection_internal", "drift_detection_internal", "single_regulation_owner", "self_review_required")), "summary_model")
    check(all(summary.get(key) is False for key in ("runtime", "scheduler", "automatic_control", "automatic_calibration", "automatic_adaptation", "automatic_parameter_update", "automatic_genome_update", "model_integration", "provider_integration", "hardware_control", "emotion_runtime", "social_runtime", "code_change", "file_move")) and len(summary.get("reused_assets", [])) >= 4 and len(summary.get("parallel_risks", [])) >= 4 and len(summary.get("future_extensions", [])) >= 3, "summary_boundary")

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
        print("READINESS: LUNA_SELF_REGULATION_FUNCTION_ENHANCEMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SELF_REGULATION_FUNCTION_ENHANCEMENT_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
