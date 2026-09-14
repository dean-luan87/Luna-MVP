"""V0 static verifier for Luna Cognitive Self Regulation Architecture.

Planning Only: validates observation, health, regulation, degradation,
recovery, governance, lifecycle and interface contracts. It does not execute
live self-regulation, model/provider/hardware/action code, or learning code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "self_observation_schema_v1.json",
    "self_health_state_schema_v1.json",
    "self_capability_regulation_contract_v1.json",
    "capability_homeostasis_policy_v1.json",
    "resource_regulation_contract_v1.json",
    "degradation_management_contract_v1.json",
    "recovery_management_contract_v1.json",
    "adaptation_governance_contract_v1.json",
    "self_regulation_lifecycle_v1.json",
    "self_regulation_brain_interface_v1.json",
    "self_regulation_capability_interface_v1.json",
    "self_regulation_model_interface_v1.json",
    "self_regulation_learning_interface_v1.json",
    "self_regulation_boundary_v1.json",
)
MD_ASSETS = (
    "luna_cognitive_self_regulation_architecture_v1.md",
    "self_regulation_whitebox_v1.md",
    "self_regulation_go_no_go_v1.md",
)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    data: dict[str, dict] = {}
    for name in JSON_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                data[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")
    for name in MD_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    observation = data.get("self_observation_schema_v1.json", {})
    health = data.get("self_health_state_schema_v1.json", {})
    capability = data.get("self_capability_regulation_contract_v1.json", {})
    homeostasis = data.get("capability_homeostasis_policy_v1.json", {})
    resource = data.get("resource_regulation_contract_v1.json", {})
    degradation = data.get("degradation_management_contract_v1.json", {})
    recovery = data.get("recovery_management_contract_v1.json", {})
    governance = data.get("adaptation_governance_contract_v1.json", {})
    lifecycle = data.get("self_regulation_lifecycle_v1.json", {})
    brain = data.get("self_regulation_brain_interface_v1.json", {})
    capability_interface = data.get("self_regulation_capability_interface_v1.json", {})
    model = data.get("self_regulation_model_interface_v1.json", {})
    learning = data.get("self_regulation_learning_interface_v1.json", {})
    boundary = data.get("self_regulation_boundary_v1.json", {})

    check({"Runtime", "Hardware", "Capability", "Model", "Memory", "Resource"}.issubset(set(observation.get("sources", []))), "observation_sources")
    check({"observation_id", "source", "subject", "observed_change", "timestamp", "confidence", "evidence_refs", "unknown"}.issubset(set(observation.get("schema", []))), "observation_schema")
    check(observation.get("rules", {}).get("read_only") is True, "observation_read_only")
    check(observation.get("rules", {}).get("non_decisional") is True, "observation_non_decisional")
    check(observation.get("rules", {}).get("provenance_required") is True, "observation_provenance")

    check({"Healthy", "Warning", "Degraded", "Critical", "Recovery Required", "Unknown"}.issubset(set(health.get("health_states", []))), "health_states")
    check({"Hardware Health", "Software Health", "Capability Health", "Model Health", "Resource Health"}.issubset(set(health.get("health_domains", []))), "health_domains")
    check({"health_id", "domain", "state", "severity", "evidence_refs", "confidence", "unknown", "timestamp"}.issubset(set(health.get("schema", []))), "health_schema")
    check(len(health.get("transitions", [])) >= 5, "health_transitions")
    check(health.get("rules", {}).get("assessment_not_decision") is True, "health_not_decision")
    check(health.get("rules", {}).get("recovery_validation_required") is True, "health_recovery_validation")

    check({"Self Observation Event", "Health State", "Current Task", "Risk", "Resource State", "Capability Profile"}.issubset(set(capability.get("inputs", []))), "capability_regulation_inputs")
    check("Capability Regulation Candidate" in capability.get("outputs", []), "capability_regulation_output")
    check(capability.get("rules", {}).get("proposes_not_admits") is True, "capability_proposes_not_admits")
    check(capability.get("rules", {}).get("capability_governance_admission_required") is True, "capability_governance_admission")
    check(capability.get("rules", {}).get("no_direct_provider_call") is True, "capability_no_provider_call")

    check({"Task Requirement", "Risk Level", "Resource State", "Capability Health", "Calibration Evidence"}.issubset(set(homeostasis.get("inputs", []))), "homeostasis_inputs")
    check({"Maintain", "Reduce Frequency", "Use Lightweight Option", "Use Alternate Capability", "Request Recovery"}.issubset(set(homeostasis.get("options", []))), "homeostasis_options")
    check(homeostasis.get("rules", {}).get("candidate_only") is True, "homeostasis_candidate_only")
    check(homeostasis.get("rules", {}).get("admission_required") is True, "homeostasis_admission")
    check(homeostasis.get("rules", {}).get("automatic_model_switch_forbidden") is True, "homeostasis_no_auto_switch")

    check({"CPU", "GPU", "Memory", "Energy", "Network", "Storage"}.issubset(set(resource.get("resource_domains", []))), "resource_domains")
    check({"Resource Observation", "Task Priority", "Risk", "Capability Requirement"}.issubset(set(resource.get("inputs", []))), "resource_inputs")
    check("Resource Regulation Candidate" in resource.get("outputs", []), "resource_output")
    check(resource.get("rules", {}).get("candidate_only") is True, "resource_candidate_only")
    check(resource.get("rules", {}).get("no_hardware_control") is True, "resource_no_hardware_control")

    check({"Health State", "Capability Failure", "Resource Constraint", "Self Limitation", "Risk"}.issubset(set(degradation.get("inputs", []))), "degradation_inputs")
    check({"Degraded Capability Profile", "Fallback Candidate", "Unknown Increase Candidate"}.issubset(set(degradation.get("outputs", []))), "degradation_outputs")
    check(degradation.get("rules", {}).get("graceful_degradation") is True, "degradation_graceful")
    check(degradation.get("rules", {}).get("unknown_increased_explicitly") is True, "degradation_unknown")
    check(degradation.get("rules", {}).get("reversible") is True, "degradation_reversible")

    check(recovery.get("pipeline") == ["Failure", "Diagnosis", "Recovery Candidate", "Validation", "Apply Candidate", "Monitor"], "recovery_pipeline")
    check({"Current Version Restore", "Historical Version Candidate", "Alternate Model Candidate", "Alternate Provider Candidate"}.issubset(set(recovery.get("recovery_options", []))), "recovery_options")
    check(recovery.get("rules", {}).get("validation_before_apply") is True, "recovery_validation")
    check(recovery.get("rules", {}).get("rollback_required") is True, "recovery_rollback")
    check(recovery.get("rules", {}).get("no_automatic_provider_switch") is True, "recovery_no_auto_switch")
    check(recovery.get("rules", {}).get("no_code_modification") is True, "recovery_no_code_change")

    check(governance.get("adoption_pipeline") == ["Observation", "Assessment", "Candidate", "Evidence", "Review", "Admission", "Apply Candidate", "Monitor"], "governance_pipeline")
    check({"Constitution", "Value", "Identity", "Goal", "Brain Core Rules", "Emotion Runtime", "Social Identity", "Model Parameters", "Source Code"}.issubset(set(governance.get("forbidden_targets", []))), "governance_forbidden_targets")
    check(governance.get("rules", {}).get("admission_required") is True, "governance_admission")
    check(governance.get("rules", {}).get("rollback_required") is True, "governance_rollback")
    check(governance.get("rules", {}).get("automatic_adaptation_forbidden") is True, "governance_no_auto")

    check({"Observed", "Assessed", "Candidate", "Under Review", "Admitted", "Applied Candidate", "Monitoring", "Recovered", "Degraded", "Rejected", "Revoked", "Archived"}.issubset(set(lifecycle.get("states", []))), "lifecycle_states")
    check({"regulation_id", "state", "created_at", "updated_at", "owner", "source_trace", "rollback_ref"}.issubset(set(lifecycle.get("schema", []))), "lifecycle_schema")
    check(len(lifecycle.get("transitions", [])) >= 9, "lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("apply_is_candidate") is True, "lifecycle_apply_candidate")
    check(lifecycle.get("rules", {}).get("no_implicit_activation") is True, "lifecycle_no_implicit_activation")

    check({"Self Health State", "Degraded Capability Profile", "Recovery Candidate", "Resource Constraint", "Risk"}.issubset(set(brain.get("inputs", []))), "brain_inputs")
    check({"Self Regulation Context", "Capability Constraint Context", "Recovery Review Request"}.issubset(set(brain.get("outputs", []))), "brain_outputs")
    check(brain.get("rules", {}).get("brain_retains_judgment") is True, "brain_authority")
    check(brain.get("rules", {}).get("context_not_decision") is True, "brain_context_only")
    check(brain.get("rules", {}).get("no_goal_change") is True, "brain_no_goal_change")

    check({"Capability Regulation Candidate", "Capability Requirement", "Resource Constraint", "Admission Policy", "Calibration Evidence"}.issubset(set(capability_interface.get("inputs", []))), "capability_interface_inputs")
    check("Admitted Capability Option Candidate" in capability_interface.get("outputs", []), "capability_interface_outputs")
    check(capability_interface.get("rules", {}).get("capability_governance_owns_admission") is True, "capability_interface_owner")
    check(capability_interface.get("rules", {}).get("self_regulation_proposes") is True, "capability_interface_proposes")
    check(capability_interface.get("rules", {}).get("model_manager_provides_options") is True, "capability_interface_model_manager")

    check({"Model Selection Candidate", "Resource Constraint", "Capability Requirement", "Model Health", "Version Registry"}.issubset(set(model.get("inputs", []))), "model_interface_inputs")
    check({"Model Option Candidate", "Version Recovery Candidate", "Model Health Evidence"}.issubset(set(model.get("outputs", []))), "model_interface_outputs")
    check(model.get("rules", {}).get("model_manager_is_provider_of_options") is True, "model_manager_options_only")
    check(model.get("rules", {}).get("no_automatic_switch") is True, "model_no_auto_switch")
    check(model.get("rules", {}).get("no_brain_access") is True, "model_no_brain_access")

    check({"Health History", "Failure Pattern", "Degradation Pattern", "Recovery Outcome", "Expectation Difference"}.issubset(set(learning.get("inputs", []))), "learning_inputs")
    check({"Learning Signal", "Capability Limitation Evidence", "Self Evolution Input Candidate"}.issubset(set(learning.get("outputs", []))), "learning_outputs")
    check(learning.get("rules", {}).get("learning_is_separate_from_stability") is True, "learning_stability_boundary")
    check(learning.get("rules", {}).get("self_regulation_does_not_auto_learn") is True, "learning_no_auto")
    check(learning.get("rules", {}).get("self_evolution_receives_candidate") is True, "learning_self_evolution")

    forbidden = set(boundary.get("forbidden", []))
    for item in (
        "Self Regulation → Constitution",
        "Self Regulation → Value Rewrite",
        "Self Regulation → Identity Rewrite",
        "Self Regulation → Goal Rewrite",
        "Self Regulation → Brain Core Rule Rewrite",
        "Self Regulation → Source Code Modification",
        "Self Regulation → Model Training",
        "Self Regulation → Parameter Update",
        "Self Regulation → Emotion Runtime",
        "Self Regulation → Social Identity Runtime",
        "Self Regulation → Direct Action",
        "Self Regulation → Direct Reality Mutation",
        "Self Regulation → Provider Direct Call",
    ):
        check(item in forbidden, f"boundary_guard:{item}")
    check(boundary.get("rules", {}).get("self_model_extension") is True, "boundary_self_model_extension")
    check(boundary.get("rules", {}).get("candidate_only") is True, "boundary_candidate_only")
    check(boundary.get("rules", {}).get("capability_admission_externalized") is True, "boundary_admission_externalized")
    check(boundary.get("rules", {}).get("model_manager_boundary_preserved") is True, "boundary_model_manager")
    check(boundary.get("rules", {}).get("no_runtime_execution") is True, "boundary_no_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"runtime_learning", "model_training", "emotion_runtime", "social_runtime", "provider_runtime"}), "planning_no_forbidden_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "planning_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_COGNITIVE_SELF_REGULATION_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_COGNITIVE_SELF_REGULATION_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
