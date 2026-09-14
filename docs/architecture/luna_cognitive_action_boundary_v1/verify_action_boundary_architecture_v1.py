"""V0 static verifier for Luna Cognitive Action Boundary architecture.

Planning Only: validates request, candidate, risk, permission, validation,
feedback, failure, trace, and Human Override contracts without importing or
executing Action, Hardware, Robot, API, Provider, or Runtime code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "action_boundary_layer_definition_v1.json",
    "action_request_contract_v1.json",
    "action_candidate_management_v1.json",
    "action_risk_evaluation_contract_v1.json",
    "action_permission_check_v1.json",
    "action_validation_gateway_v1.json",
    "action_execution_contract_v1.json",
    "action_outcome_feedback_v1.json",
    "action_trace_schema_v1.json",
    "action_failure_handling_v1.json",
    "human_override_boundary_v1.json",
    "action_l1_interface_v1.json",
    "action_l2_interface_v1.json",
    "action_l3_interface_v1.json",
    "action_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_action_boundary_architecture_v1.md",
    "action_boundary_whitebox_v1.md",
    "action_boundary_go_no_go_v1.md",
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

    layer = data.get("action_boundary_layer_definition_v1.json", {})
    request = data.get("action_request_contract_v1.json", {})
    candidates = data.get("action_candidate_management_v1.json", {})
    risk = data.get("action_risk_evaluation_contract_v1.json", {})
    permission = data.get("action_permission_check_v1.json", {})
    validation = data.get("action_validation_gateway_v1.json", {})
    execution = data.get("action_execution_contract_v1.json", {})
    outcome = data.get("action_outcome_feedback_v1.json", {})
    trace = data.get("action_trace_schema_v1.json", {})
    failure = data.get("action_failure_handling_v1.json", {})
    override = data.get("human_override_boundary_v1.json", {})
    l1 = data.get("action_l1_interface_v1.json", {})
    l2 = data.get("action_l2_interface_v1.json", {})
    l3 = data.get("action_l3_interface_v1.json", {})
    boundary = data.get("action_dependency_boundary_v1.json", {})

    required_subsystems = {"Action Request Layer", "Action Candidate Management", "Action Risk Evaluation", "Action Permission Check", "Action Validation Gateway", "Execution Contract", "Outcome Feedback", "Action Trace", "Action Failure Handling", "Human Override Boundary"}
    check(layer.get("layer") == "L2 → External World Boundary", "action_layer")
    check(required_subsystems.issubset(set(layer.get("subsystems", []))), "action_subsystems")
    check(layer.get("rules", {}).get("candidate_before_execution") is True, "action_candidate_before_execution")
    check(layer.get("rules", {}).get("runtime_disabled") is True, "action_runtime_disabled")
    check({"Action execution", "Goal ownership", "Value modification", "Decision creation"}.issubset(set(layer.get("not_authority", []))), "action_not_authority")

    check(request.get("source_required") == "Decision Commitment", "request_decision_source")
    check({"action_request_id", "source_decision", "intent", "target", "context", "confidence", "risk_level", "expected_outcome"}.issubset(set(request.get("schema", []))), "request_schema")
    check({"Raw Provider Output", "Emotion Direct", "Capability Direct"}.issubset(set(request.get("forbidden_sources", []))), "request_forbidden_sources")
    check(request.get("rules", {}).get("decision_not_execution") is True, "request_not_execution")
    check(request.get("rules", {}).get("brain_direct_executor_forbidden") is True, "request_brain_guard")

    check({"candidate_id", "action_type", "benefit", "risk", "dependency", "confidence"}.issubset(set(candidates.get("schema", []))), "candidate_schema")
    check(candidates.get("rules", {}).get("candidate_not_action") is True, "candidate_not_action")
    check(candidates.get("rules", {}).get("multiple_candidates_allowed") is True, "candidate_alternatives")
    check(candidates.get("rules", {}).get("no_auto_execution") is True, "candidate_no_auto_execution")

    check({"Physical Risk", "Social Risk", "Privacy Risk", "Resource Risk"}.issubset(set(risk.get("dimensions", []))), "risk_dimensions")
    check({"risk_level", "risk_reason", "required_confirmation"}.issubset(set(risk.get("schema", []))), "risk_schema")
    check(risk.get("rules", {}).get("risk_required_before_permission") is True, "risk_before_permission")
    check(risk.get("rules", {}).get("unknown_escalates") is True, "risk_unknown_escalation")

    check({"Constitution", "Safety", "Permission", "Context"}.issubset(set(permission.get("checks", []))), "permission_checks")
    check({"Action Candidate", "Risk Evaluation", "Active Role", "Context"}.issubset(set(permission.get("inputs", []))), "permission_inputs")
    check(permission.get("rules", {}).get("constitution_check_required") is True, "permission_constitution")
    check(permission.get("rules", {}).get("no_implicit_authority") is True, "permission_no_implicit")

    check(validation.get("pipeline") == ["Action Candidate", "Risk Evaluation", "Permission Check", "Context Validation", "Action Approved Candidate"], "validation_pipeline")
    check(validation.get("output") == "Action Approved Candidate", "validation_output")
    check(validation.get("rules", {}).get("approved_is_not_execution") is True, "validation_not_execution")
    check(validation.get("rules", {}).get("all_gates_required") is True, "validation_all_gates")

    check(execution.get("input") == "Action Approved Candidate", "execution_input")
    check(execution.get("future_output") == "Outcome Evidence", "execution_feedback")
    check(execution.get("execution_owner") == "Future Action Runtime", "execution_future_owner")
    check({"Action Runtime", "Hardware Control", "Robot Movement", "API Execution", "External Side Effect"}.issubset(set(execution.get("not_implemented", []))), "execution_not_implemented")
    check(execution.get("rules", {}).get("execution_future_only") is True, "execution_future_only")
    check(execution.get("rules", {}).get("no_current_side_effect") is True, "execution_no_side_effect")

    check(outcome.get("pipeline") == ["Action Future", "Outcome", "Outcome Evidence", "Experience", "Learning"], "outcome_pipeline")
    check({"outcome_id", "action_request_id", "execution_reference", "outcome_state", "evidence", "expected_vs_actual"}.issubset(set(outcome.get("schema", []))), "outcome_schema")
    check({"Success", "Failure", "Partial Success", "Unexpected Outcome", "Unknown"}.issubset(set(outcome.get("outcome_states", []))), "outcome_states")
    check(outcome.get("rules", {}).get("outcome_reenters_cognition") is True, "outcome_reentry")

    check({"Observation", "Context", "Decision", "Action Candidate", "Validation", "Outcome"}.issubset(set(trace.get("chain", []))), "trace_chain")
    check({"trace_id", "observation_reference", "context_reference", "decision_reference", "candidate_reference", "risk_reference", "permission_reference", "outcome_reference"}.issubset(set(trace.get("fields", []))), "trace_fields")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_not_authority")

    check({"Action Rejected", "Execution Failed", "Partial Success", "Unexpected Outcome"}.issubset(set(failure.get("failure_types", []))), "failure_types")
    check(failure.get("pipeline") == ["Failure", "Record", "Analyze", "Update Context", "Re-evaluate"], "failure_pipeline")
    check(failure.get("rules", {}).get("failure_not_automatically_decision_error") is True, "failure_not_decision_error")
    check(failure.get("rules", {}).get("no_auto_retry") is True, "failure_no_auto_retry")

    check({"override_type", "authority", "timestamp", "reason"}.issubset(set(override.get("schema", []))), "override_schema")
    check({"High Risk", "Critical Risk", "Medical", "Property", "Safety"}.issubset(set(override.get("required_for", []))), "override_required_cases")
    check(override.get("rules", {}).get("human_authority_explicit") is True, "override_authority")
    check(override.get("rules", {}).get("override_not_implicit_action") is True, "override_not_action")

    check({"Lifecycle Contract", "Trace Contract", "Event Contract", "Recovery Contract"}.issubset(set(l1.get("inputs", []))), "l1_interface_inputs")
    check({"Constitution", "Runtime Rules", "Governance Authority"}.issubset(set(l1.get("l1_not_modified", []))), "l1_interface_boundary")
    check(l1.get("rules", {}).get("l1_owns_lifecycle") is True, "l1_interface_lifecycle")
    check({"Decision Commitment", "Intent", "Goal", "Context", "Confidence"}.issubset(set(l2.get("inputs", []))), "l2_interface_inputs")
    check({"Goal", "Value", "Decision", "Brain", "Reality"}.issubset(set(l2.get("l2_not_modified", []))), "l2_interface_boundary")
    check(l2.get("rules", {}).get("decision_source_required") is True, "l2_decision_source")
    check("Emotion → Direct Action" in l3.get("forbidden", []), "l3_emotion_guard")
    check("Social Field → Execution" in l3.get("forbidden", []), "l3_social_guard")
    check(l3.get("rules", {}).get("direct_execution_forbidden") is True, "l3_no_execution")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Brain → Direct Action", "Emotion → Direct Action", "Capability → Action Authority", "Provider → Action Authority", "Action Boundary → Goal Ownership", "Action Boundary → Value Modification"):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 5, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("validation_required") is True, "dependency_validation")
    check(boundary.get("rules", {}).get("execution_future_only") is True, "dependency_future_execution")
    check(boundary.get("rules", {}).get("no_external_side_effect") is True, "dependency_no_side_effect")

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
    print("READINESS: LUNA_ACTION_BOUNDARY_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
