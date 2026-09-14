"""V0 static verifier for Luna Capability Execution Boundary.

Planning Only: validates request, admission, evidence, feedback, failure, and
trace contracts without importing or executing Model, Provider, Hardware,
Runtime, OCR, SLAM, Camera, or Action code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "capability_request_contract_v1.json",
    "capability_intent_mapping_contract_v1.json",
    "capability_admission_gateway_v1.json",
    "capability_selection_boundary_v1.json",
    "capability_execution_contract_v1.json",
    "evidence_return_gateway_v1.json",
    "capability_feedback_loop_v1.json",
    "capability_failure_handling_v1.json",
    "capability_trace_schema_v1.json",
    "capability_os_interface_v1.json",
    "capability_cognitive_core_interface_v1.json",
    "capability_l3_boundary_v1.json",
    "capability_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_capability_execution_boundary_architecture_v1.md",
    "capability_execution_whitebox_v1.md",
    "capability_execution_go_no_go_v1.md",
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

    request = data.get("capability_request_contract_v1.json", {})
    mapping = data.get("capability_intent_mapping_contract_v1.json", {})
    admission = data.get("capability_admission_gateway_v1.json", {})
    selection = data.get("capability_selection_boundary_v1.json", {})
    execution = data.get("capability_execution_contract_v1.json", {})
    evidence = data.get("evidence_return_gateway_v1.json", {})
    feedback = data.get("capability_feedback_loop_v1.json", {})
    failure = data.get("capability_failure_handling_v1.json", {})
    trace = data.get("capability_trace_schema_v1.json", {})
    os_interface = data.get("capability_os_interface_v1.json", {})
    core_interface = data.get("capability_cognitive_core_interface_v1.json", {})
    l3 = data.get("capability_l3_boundary_v1.json", {})
    boundary = data.get("capability_dependency_boundary_v1.json", {})

    check(request.get("owner") == "L2 Cognitive Core Governance", "request_owner")
    check({"request_id", "source_module", "capability_need", "context", "priority", "constraint", "deadline", "confidence_requirement"}.issubset(set(request.get("schema", []))), "request_schema")
    check({"model", "provider"}.issubset(set(request.get("forbidden_fields", []))), "request_no_provider_name")
    check(request.get("rules", {}).get("need_not_provider") is True, "request_need_not_provider")
    check(request.get("rules", {}).get("governance_admission_required") is True, "request_admission")

    check({"intent", "required_capability", "optional_capability", "forbidden_capability"}.issubset(set(mapping.get("schema", []))), "mapping_schema")
    check(mapping.get("rules", {}).get("provider_agnostic") is True, "mapping_provider_agnostic")
    check(mapping.get("rules", {}).get("mapping_not_decision") is True, "mapping_not_decision")

    check(admission.get("pipeline", [])[0:3] == ["Capability Request", "Registry Lookup", "Capability Profile"], "admission_pipeline")
    check({"Permission Check", "Health Check", "Calibration Check", "Resource Check", "Admission Result"}.issubset(set(admission.get("pipeline", []))), "admission_checks")
    check({"exists", "trusted", "context_fit", "permission", "health", "calibration", "resource_budget"}.issubset(set(admission.get("required_checks", []))), "admission_required_checks")
    check(admission.get("rules", {}).get("no_bypass") is True, "admission_no_bypass")
    check(admission.get("rules", {}).get("admission_not_execution") is True, "admission_not_execution")

    check({"Capability Requirement", "Capability Profile", "Current Resource State", "Admission Result"}.issubset(set(selection.get("inputs", []))), "selection_inputs")
    check(selection.get("output") == "Capability Candidate", "selection_output")
    check(selection.get("rules", {}).get("selection_is_not_brain_decision") is True, "selection_not_brain")
    check(selection.get("rules", {}).get("provider_is_implementation_option") is True, "selection_provider_option")

    check(execution.get("output_type") == "Evidence Candidate", "execution_evidence_output")
    check({"capability", "input_type", "permission", "resource_budget"}.issubset(set(execution.get("input_schema", []))), "execution_input_schema")
    check({"source", "content", "confidence", "timestamp", "context", "limitation", "provenance"}.issubset(set(execution.get("output_schema", []))), "execution_output_schema")
    check({"create Goal", "modify Memory", "control Brain", "write Reality"}.issubset(set(execution.get("provider_not_allowed", []))), "provider_permissions")
    check(execution.get("rules", {}).get("direct_decision_forbidden") is True, "execution_no_decision")

    check(evidence.get("pipeline", [])[0:3] == ["Provider Output", "Evidence Validation", "Context Binding"], "evidence_pipeline")
    check({"source", "content", "confidence", "timestamp", "context", "limitation", "provenance", "trace_id"}.issubset(set(evidence.get("evidence_schema", []))), "evidence_schema")
    check(evidence.get("rules", {}).get("provider_output_is_not_fact") is True, "evidence_not_fact")
    check(evidence.get("rules", {}).get("gateway_required") is True, "evidence_gateway_required")
    check(evidence.get("rules", {}).get("unknown_preserved") is True, "evidence_unknown")

    check(feedback.get("pipeline", [])[0:3] == ["Execution Result", "Capability Performance Evidence", "Calibration Update Candidate"], "feedback_pipeline")
    check(feedback.get("rules", {}).get("no_auto_model_update") is True, "feedback_no_model_update")
    check(feedback.get("rules", {}).get("candidate_only") is True, "feedback_candidate_only")

    check({"Capability unavailable", "Capability degraded", "Capability conflict", "Capability timeout"}.issubset(set(failure.get("failure_types", []))), "failure_types")
    check(failure.get("pipeline") == ["Failure", "Diagnostics", "Degrade", "Alternative Candidate", "Unknown Preservation"], "failure_pipeline")
    check(failure.get("rules", {}).get("unknown_preserved") is True, "failure_unknown")
    check(failure.get("rules", {}).get("no_auto_model_switch") is True, "failure_no_auto_switch")

    check({"Cognitive Request", "Capability Selection", "Provider Reference", "Evidence", "Validation", "Cognitive Update"}.issubset(set(trace.get("chain", []))), "trace_chain")
    check({"trace_id", "request_id", "capability", "selection_reference", "provider_reference", "evidence_reference", "validation_reference"}.issubset(set(trace.get("fields", []))), "trace_fields")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_not_authority")

    check({"Lifecycle Contract", "Admission Contract", "Resource State", "Event Contract", "Trace Contract"}.issubset(set(os_interface.get("inputs", []))), "os_interface_inputs")
    check({"Constitution", "Cognitive Flow Authority", "Goal", "Decision", "Reality"}.issubset(set(os_interface.get("os_not_modified", []))), "os_interface_boundary")
    check(os_interface.get("rules", {}).get("capability_does_not_control_os") is True, "capability_no_os_control")

    check({"Capability Requirement", "Observation Requirement", "Context", "Priority", "Constraint"}.issubset(set(core_interface.get("core_inputs", []))), "core_interface_inputs")
    check({"Brain Judgment", "Goal", "Decision", "Belief", "Reality"}.issubset(set(core_interface.get("core_not_modified", []))), "core_interface_boundary")
    check(core_interface.get("rules", {}).get("request_origin_is_core") is True, "core_request_origin")
    check(core_interface.get("rules", {}).get("provider_not_direct_core") is True, "provider_not_direct_core")

    check("Emotion → Direct Capability Control" in l3.get("forbidden", []), "l3_emotion_guard")
    check("Social Field → Provider Invocation" in l3.get("forbidden", []), "l3_social_guard")
    check(l3.get("rules", {}).get("direct_invocation_forbidden") is True, "l3_no_direct_invocation")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Provider → Brain Control", "Capability → Goal Creation", "Capability → Decision Ownership", "Capability → Reality Modification", "Emotion → Capability Direct Control"):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 5, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("evidence_gateway_required") is True, "dependency_evidence_gateway")
    check(boundary.get("rules", {}).get("provider_isolation") is True, "dependency_provider_isolation")
    check(boundary.get("rules", {}).get("no_runtime_execution") is True, "dependency_no_runtime")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
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
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CAPABILITY_EXECUTION_BOUNDARY_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
