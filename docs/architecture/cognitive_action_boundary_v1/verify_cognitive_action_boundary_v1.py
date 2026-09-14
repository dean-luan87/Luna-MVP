#!/usr/bin/env python3
"""V2 static verifier for Cognitive Action Boundary architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_action_boundary_model_v1.md": [
        "Action Boundary", "Brain Decision Candidate", "Action Intent", "Action Request", "Action Permission Candidate",
        "Execution Boundary", "Outcome Evidence", "Decision is not Execution", "Action Command", "required capability",
        "Brain retains Goal", "Value", "Decision", "authorization judgment", "cannot modify Goal", "modify Decision",
        "modify Reality", "Action Failure", "Cause Attribution Candidate", "Environment Change", "Capability Gap",
        "Execution Gap", "Information Gap", "Understanding Gap", "Random Event", "Unknown Factor", "Low-risk",
        "High-risk", "payment", "data deletion", "movement", "Neural Fast Path", "Safety Action Candidate",
        "No real Action Runtime", "hardware control", "robot movement", "automatic execution"
    ],
    "action_permission_boundary_v1.md": [
        "Permission classes", "Low-risk candidate", "query weather", "adjust observation frequency", "Medium-risk candidate",
        "navigation support", "High-risk candidate", "payment", "delete data", "change environment", "movement",
        "Safety candidate", "Neural Fast Path candidate", "Permission is a candidate", "Action Request", "authorization candidate",
        "Provider", "Capability", "Runtime", "Neural", "control hardware", "send external commands", "move a robot",
        "make payment", "delete data", "external system", "sole State mutation authority"
    ],
    "action_failure_attribution_v1.md": [
        "Action Failure", "Outcome Evidence", "Difference Analysis", "Cause Attribution Candidate", "Adaptation Candidate",
        "Decision Failure", "Environment Change", "Capability Gap", "Execution Gap", "Information Gap", "Understanding Gap",
        "Random Event", "Decision Factor", "Unknown Factor", "multiple factors", "Goal", "Self Model", "Decision Policy",
        "Reality", "Action Policy", "not blame", "responsibility assignment", "sole State mutation authority"
    ],
    "action_brain_boundary_v1.md": [
        "Decision Candidate", "Action Intent Candidate", "Action Request Candidate", "Brain / User Authorization Candidate",
        "Execution Boundary", "Brain owns Intent", "Goal", "Value", "Decision", "authorization judgment",
        "permission", "capability", "risk", "constraint", "Runtime owns only execution mechanics", "cannot modify Goal",
        "Decision", "Reality", "Self Identity", "Capability Identity", "issue a command", "execute", "make a payment",
        "move a robot", "delete data", "change the environment", "bypass Brain", "Neural Fast Path", "Safety Action Candidate",
        "does not grant permission"
    ],
    "action_whitebox_v1.md": [
        "Decision Candidate", "Action Intent", "Action Request", "Permission", "Risk", "Capability Validation",
        "Execution Boundary Candidate", "Outcome Evidence", "Reality Update Candidate", "Reducer", "Decision Reference",
        "Target", "Constraints", "Confidence", "Required Capability", "Authorization Level", "Risk Classification",
        "Unknowns", "Permission Candidate", "Action Command", "no real execution", "no direct Reality mutation",
        "Action Failure", "Cause Attribution Candidate", "Decision Failure", "Neural Safety Action Candidate",
        "candidate-only", "sole State mutation authority", "No real Action Runtime", "No hardware control", "No robot movement",
        "No payment", "No external system operation", "No automatic execution", "No Emotion Runtime", "No Role Runtime",
        "No Social Runtime", "No B Runtime"
    ],
    "action_go_no_go_v1.md": [
        "Decision Candidate", "Action Intent", "Action Request", "Action Command", "decision_reference", "intent", "target",
        "constraints", "confidence", "required_capability", "authorization_level", "low-risk", "medium-risk", "high-risk",
        "Safety Action Candidate", "Brain/User", "External World Change", "Evidence", "Reality Update Candidate", "Reducer",
        "Action Failure", "Cause Attribution Candidate", "Decision Failure", "Capability Governance", "cannot directly call a model",
        "Provider", "Attention does not execute Action", "Goal", "Decision", "Value", "authorization authority",
        "sole State mutation authority", "No real Action Runtime", "No hardware control", "No automatic execution", "No robot movement",
        "No payment", "No external system operation", "No Emotion", "No Role", "No Social Runtime", "No B", "No real model",
        "No OCR", "No SLAM", "No Camera", "No Hardware Runtime", "No Action execution", "No direct Reality mutation",
        "No direct Goal mutation", "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "action_intent_schema_v1.json": [
        "Action Intent Schema", "intent_id", "decision_reference", "intent", "target", "constraints", "confidence",
        "required_capability", "authorization_level", "risk_classification", "unknowns", "provenance",
        "action_intent_is_not_decision", "action_intent_is_not_action_command", "action_intent_is_not_execution",
        "action_intent_does_not_modify_goal", "action_intent_does_not_modify_reality", "action_intent_does_not_execute",
        "brain_authorization_required", "unknowns_are_preserved"
    ],
    "action_request_contract_v1.json": [
        "Action Request Contract", "request_id", "decision_reference", "intent", "target", "constraints", "confidence",
        "required_capability", "authorization_level", "risk_classification", "provenance", "expiry", "Created", "Validated",
        "Authorized Candidate", "Rejected", "Expired", "Feedback Pending", "action_request_is_not_action_command",
        "action_request_is_not_execution", "action_request_requires_validation", "action_request_requires_permission_candidate",
        "action_request_cannot_modify_goal", "action_request_cannot_modify_decision", "action_request_cannot_modify_reality",
        "action_request_cannot_execute", "provider_is_not_action_authority", "brain_retains_authorization_authority"
    ],
    "action_reality_feedback_contract_v1.json": [
        "Action Reality Feedback Contract", "Action Request Candidate", "Execution Boundary", "External World Change",
        "Outcome Evidence", "Reality Update Candidate", "Reducer", "request_reference", "expected_change_candidate",
        "observed_change_evidence", "difference", "provenance", "confidence", "unknowns", "timestamp",
        "action_does_not_directly_modify_reality", "evidence_gateway_required", "reality_update_candidate_required",
        "outcome_is_not_decision_failure", "external_change_is_not_assumed", "reducer_is_sole_state_mutation_authority"
    ],
    "action_attention_interface_v1.json": [
        "Action Attention Interface", "action_intent", "execution_state_candidate", "risk_context", "capability_context",
        "new_observation_requirement_candidate", "attention_adjustment_candidate", "monitoring_priority_candidate",
        "execution_feedback_candidate", "crossing", "navigation", "completion", "failure", "action_does_not_modify_attention_directly",
        "attention_does_not_execute_action", "attention_does_not_modify_goal", "attention_does_not_modify_decision",
        "candidate_only", "no_automatic_frequency_adjustment"
    ],
    "action_capability_interface_v1.json": [
        "Action Capability Interface", "action_intent", "required_capability", "resource_requirement", "authorization_level",
        "constraints", "provenance", "Decision", "Action Intent", "Capability Requirement", "Capability Governance",
        "Provider Candidate", "Execution Boundary", "action_does_not_directly_call_model", "capability_governance_required",
        "provider_is_not_decision_authority", "provider_is_not_action_authority", "hardware_control_is_out_of_scope",
        "execution_is_out_of_scope", "capability_failure_returns_candidate"
    ]
}


def main():
    failures = []
    checks = 0
    for name, terms in MD_REQ.items():
        checks += 1
        path = BASE / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
    for name, terms in JSON_REQ.items():
        checks += 1
        path = BASE / name
        try:
            text = path.read_text()
            json.loads(text)
        except Exception as exc:
            failures.append(f"JSON parse failure: {name}: {type(exc).__name__}")
            text = ""
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required JSON contract term: {term} in {name}")
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
