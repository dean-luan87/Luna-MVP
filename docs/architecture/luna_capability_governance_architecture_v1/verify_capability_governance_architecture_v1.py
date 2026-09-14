"""V0 static verifier for Luna Capability Governance Architecture.

Planning Only: validates ownership and boundary contracts without executing
Capability Runtime, Model, Provider, Hardware, Scheduler, Upgrade, Recovery,
or Action behavior.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "capability_governance_model_v1.json", "capability_owner_definition_v1.json",
    "capability_registry_boundary_v1.json", "model_manager_boundary_v1.json",
    "provider_boundary_v1.json", "capability_lifecycle_contract_v1.json",
    "capability_admission_hierarchy_v1.json", "capability_calibration_contract_v1.json",
    "capability_health_model_v1.json", "self_regulation_capability_interface_v1.json",
    "brain_capability_request_contract_v1.json", "capability_runtime_boundary_v1.json",
    "capability_governance_permission_matrix_v1.json", "capability_duplicate_mapping_v1.json",
)
MD_ASSETS = (
    "luna_capability_governance_architecture_v1.md",
    "capability_governance_whitebox_v1.md",
    "capability_governance_go_no_go_v1.md",
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

    governance = data.get("capability_governance_model_v1.json", {})
    owner = data.get("capability_owner_definition_v1.json", {})
    registry = data.get("capability_registry_boundary_v1.json", {})
    model = data.get("model_manager_boundary_v1.json", {})
    provider = data.get("provider_boundary_v1.json", {})
    lifecycle = data.get("capability_lifecycle_contract_v1.json", {})
    admission = data.get("capability_admission_hierarchy_v1.json", {})
    calibration = data.get("capability_calibration_contract_v1.json", {})
    health = data.get("capability_health_model_v1.json", {})
    self_reg = data.get("self_regulation_capability_interface_v1.json", {})
    brain = data.get("brain_capability_request_contract_v1.json", {})
    runtime = data.get("capability_runtime_boundary_v1.json", {})
    permissions = data.get("capability_governance_permission_matrix_v1.json", {})
    duplicate = data.get("capability_duplicate_mapping_v1.json", {})

    layers = governance.get("layers", [])
    layer_names = [row.get("layer") for row in layers]
    check(len(layers) >= 8, "governance_layers")
    check(len(layer_names) == len(set(layer_names)) and all(layer_names), "governance_layer_names_unique")
    check(all(row.get("owner") and row.get("answers") and row.get("outputs") for row in layers), "governance_layer_completeness")
    check(governance.get("canonical_flow") == ["Capability Requirement", "Capability Registry", "Capability Admission", "Model/Provider/Runtime Qualification", "Calibration", "Controlled Available", "Capability Runtime", "Evidence"], "governance_canonical_flow")
    check(governance.get("rules", {}).get("capability_is_subject") is True, "governance_capability_subject")
    check(governance.get("rules", {}).get("model_is_implementation_resource") is True, "governance_model_resource")
    check(governance.get("rules", {}).get("capability_owner_unique") is True, "governance_owner_unique")
    check(governance.get("rules", {}).get("admission_required") is True, "governance_admission")

    check(owner.get("owner") == "Capability Registry", "capability_owner_registry")
    check(set(["Capability Identity", "Capability Schema", "Capability Contract", "Capability Dependencies", "Capability Lifecycle"]).issubset(set(owner.get("owned_concepts", []))), "capability_owned_concepts")
    check(set(["Model Version", "Provider", "Runtime Scheduling", "Decision", "Goal", "Action"]).issubset(set(owner.get("not_owned", []))), "capability_owner_boundary")
    check(owner.get("rules", {}).get("one_capability_one_owner") is True, "capability_one_owner")

    check(registry.get("owner") == "Capability Registry", "registry_owner")
    check(set(["Capability Identity", "Capability Schema", "Capability Contract", "Capability Dependencies", "Capability Lifecycle"]).issubset(set(registry.get("stores", []))), "registry_stores")
    check(registry.get("rules", {}).get("registry_is_not_scheduler") is True, "registry_not_scheduler")
    check(registry.get("rules", {}).get("registry_is_not_model_manager") is True, "registry_not_model_manager")

    check(model.get("owner") == "Model Manager", "model_manager_owner")
    check(set(["Model Identity", "Version", "Resource Requirement", "Runtime Compatibility", "Deployment Status"]).issubset(set(model.get("manages", []))), "model_manager_scope")
    check(set(["Capability Value", "Goal", "Decision", "Action", "Reality", "Identity"]).issubset(set(model.get("does_not_decide", []))), "model_manager_boundary")
    check(model.get("binding", {}).get("from") == "Capability", "model_binding_capability_first")
    check(model.get("rules", {}).get("capability_first") is True, "model_capability_first")
    check(model.get("rules", {}).get("manager_not_cognitive_owner") is True, "model_not_cognitive_owner")

    check(provider.get("owner") == "Provider Governance", "provider_owner")
    check(provider.get("flow") == ["Capability", "Provider Adapter", "Model", "Evidence Candidate"], "provider_flow")
    check(set(["Decision", "State", "Reality", "Goal", "Identity", "Memory"]).issubset(set(provider.get("does_not_own", []))), "provider_boundary")
    check(provider.get("rules", {}).get("provider_isolation") is True, "provider_isolation")
    check(provider.get("rules", {}).get("evidence_gateway_required") is True, "provider_evidence_gateway")

    check(lifecycle.get("states") == ["Candidate", "Registered", "Testing", "Active", "Degraded", "Suspended", "Retired"], "lifecycle_states")
    check(len(lifecycle.get("transitions", [])) >= 6, "lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("active_requires_admission") is True, "lifecycle_admission")
    check(lifecycle.get("rules", {}).get("degraded_is_not_identity_failure") is True, "lifecycle_local_degradation")
    check(lifecycle.get("rules", {}).get("no_automatic_transition") is True, "lifecycle_no_auto")

    check(admission.get("primary_admission") == "Capability Admission", "admission_primary")
    check(admission.get("flow") == ["New Capability Candidate", "Capability Review", "Risk Assessment", "Evidence Requirement", "Admission Decision", "Active"], "admission_flow")
    check(set(["Model Qualification", "Provider Qualification", "Runtime Qualification"]).issubset(set(admission.get("qualification_branches", []))), "admission_qualification_branches")
    check(admission.get("owners", {}).get("capability_review") == "Capability Governance", "admission_capability_owner")
    check(admission.get("rules", {}).get("capability_admission_is_primary") is True, "admission_capability_first")
    check(admission.get("rules", {}).get("all_branches_required_before_active") is True, "admission_branches_required")

    check(calibration.get("owner") == "Capability Calibration", "calibration_owner")
    check(set(["Accuracy", "Stability", "Latency", "Resource Cost", "Failure Rate"]).issubset(set(calibration.get("metrics", []))), "calibration_metrics")
    check(calibration.get("rules", {}).get("capability_level_assessment") is True, "calibration_capability_level")
    check(calibration.get("rules", {}).get("model_internal_training_out_of_scope") is True, "calibration_no_training")
    check(calibration.get("rules", {}).get("no_auto_upgrade") is True, "calibration_no_auto_upgrade")

    check(set(["Healthy", "Warning", "Degraded", "Critical", "Unknown"]).issubset(set(health.get("states", []))), "health_states")
    check(set(["Capability Health Score", "Capability Health Candidate", "Self State Synchronization Candidate"]).issubset(set(health.get("outputs", []))), "health_outputs")
    check(health.get("rules", {}).get("health_not_identity") is True, "health_not_identity")
    check(health.get("rules", {}).get("health_not_system_failure") is True, "health_not_system_failure")
    check(health.get("rules", {}).get("local_failure_isolated") is True, "health_failure_isolation")

    check(self_reg.get("flow") == ["Self Regulation", "Capability Health Query", "Capability Governance", "Candidate Options", "Brain Evaluation", "Adjustment"], "self_reg_flow")
    check(set(["Report Health Change", "Request Health Query", "Propose Degradation", "Propose Recovery"]).issubset(set(self_reg.get("self_regulation_can", []))), "self_reg_can")
    check(set(["Direct Model Switch", "Direct Provider Invocation", "Bypass Admission", "Automatic Upgrade"]).issubset(set(self_reg.get("self_regulation_cannot", []))), "self_reg_cannot")
    check(self_reg.get("rules", {}).get("proposal_only") is True, "self_reg_proposal_only")
    check(self_reg.get("rules", {}).get("admission_retained_by_governance") is True, "self_reg_admission_owner")

    check(brain.get("request_owner") == "Brain / Cognitive Core", "brain_request_owner")
    check(brain.get("flow") == ["Brain", "Capability Request", "Capability Governance", "Capability Runtime", "Evidence"], "brain_request_flow")
    check(set(["Named Model", "Provider Version", "Hardware Driver", "Runtime Scheduler"]).issubset(set(brain.get("brain_does_not_select", []))), "brain_model_isolation")
    check(brain.get("rules", {}).get("capability_not_model_request") is True, "brain_capability_not_model")
    check(brain.get("rules", {}).get("request_is_not_action") is True, "brain_request_not_action")

    check(runtime.get("flow") == ["Capability Request", "Capability Runtime", "Provider Adapter", "Model", "Evidence Return"], "runtime_flow")
    check(set(["Execution Context", "Invocation Lifecycle", "Result Collection", "Failure Trace"]).issubset(set(runtime.get("runtime_owns", []))), "runtime_scope")
    check(set(["Capability Value", "Goal", "Decision", "Identity", "Reality Authority", "Admission"]).issubset(set(runtime.get("runtime_does_not_own", []))), "runtime_boundary")
    check(runtime.get("rules", {}).get("runtime_executes_only_admitted_request") is True, "runtime_admitted_only")
    check(runtime.get("rules", {}).get("runtime_not_decision_authority") is True, "runtime_not_decision")

    permission_rows = permissions.get("rows", [])
    check(len(permission_rows) >= 7, "permission_rows")
    check(all(row.get("actor") and row.get("can") is not None and row.get("cannot") is not None for row in permission_rows), "permission_completeness")
    check(permissions.get("rules", {}).get("capability_governance_no_goal") is True, "permission_no_goal")
    check(permissions.get("rules", {}).get("capability_governance_no_decision") is True, "permission_no_decision")
    check(permissions.get("rules", {}).get("provider_evidence_only") is True, "permission_provider_evidence")
    check(permissions.get("rules", {}).get("admission_required") is True, "permission_admission")

    groups = duplicate.get("groups", [])
    check(len(groups) >= 5, "duplicate_groups")
    check(all(row.get("group") and row.get("canonical_owner") and row.get("existing_assets") and row.get("decision") and row.get("delete") is False for row in groups), "duplicate_mapping_complete")
    check(duplicate.get("rules", {}).get("no_delete") is True, "duplicate_no_delete")
    check(duplicate.get("rules", {}).get("canonical_mapping_only") is True, "duplicate_mapping_only")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports: set[str] = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    check(not imports.intersection({"capability_runtime", "model_training", "auto_upgrade", "hardware_runtime"}), "planning_no_execution_import")
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
        print("READINESS: LUNA_CAPABILITY_GOVERNANCE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CAPABILITY_GOVERNANCE_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
