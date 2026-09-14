#!/usr/bin/env python3
"""V2 static verifier for Attention Competition and Arbitration architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_attention_architecture_v1.md": [
        "Attention Resource", "Attention Competition", "Attention Arbitration",
        "Attention Allocation", "Observation Requirement", "Survival Attention",
        "Goal Attention", "Field Attention", "Maintenance Attention", "Exploration Attention",
        "External Demand Attention", "Mandatory Attention", "Competitive Attention",
        "Opportunistic Attention", "Attention Interrupt Request", "Attention Priority Candidate",
        "Information Value", "Resource Cost", "Attention Lifecycle", "Created", "Allocated",
        "Maintained", "Decayed", "Released", "Archived", "No Emotion Runtime", "No Role Runtime",
        "No B Route", "No Decision", "No Action"
    ],
    "cognitive_attention_resource_model_v1.md": [
        "Available Capacity", "Current Allocation", "Reserved Capacity", "Recovery Capacity",
        "Attention Allocation Candidate", "Information Value", "Resource Cost", "Mandatory Attention",
        "does not implement a Scheduler", "automatic frequency adjustment", "hardware control"
    ],
    "cognitive_attention_priority_model_v1.md": [
        "Attention Priority Candidate", "Survival Impact", "Goal Relevance", "Field Relevance",
        "Temporal Urgency", "Information Value", "Uncertainty Reduction", "Resource Cost",
        "Allocation Candidate", "Priority does not equal Importance", "Attention Priority does not",
        "Decision", "Value Judgment"
    ],
    "cognitive_attention_competition_model_v1.md": [
        "Attention Request", "Attention Competition", "Arbitration Candidate", "Resource Allocation",
        "Coding Attention", "Threat Attention", "Mandatory Attention", "Preemption",
        "does not decide", "No multi-A coordination", "role competition", "emotion runtime"
    ],
    "cognitive_attention_preemption_model_v1.md": [
        "New Evidence", "Risk Candidate", "Attention Interrupt Request", "Attention Arbitration",
        "Resource Reallocation", "Mandatory Attention", "Preemption", "not a Decision",
        "not an Action", "cannot alter Reality", "cannot trigger Action", "Neural Fast Attention"
    ],
    "cognitive_attention_release_model_v1.md": [
        "Created", "Allocated", "Maintained", "Decayed", "Released", "Archived",
        "information is sufficiently covered", "risk is reduced", "task or Field is complete",
        "Attention Value", "prevents attention leakage", "not a Scheduler", "does not modify Goal"
    ],
    "cognitive_attention_persistence_model_v1.md": [
        "Attention Persistence", "Persistent", "Temporary", "Interruptive", "release condition",
        "resource cap", "restoration candidate", "cannot directly request hardware frequency",
        "cannot make a Decision", "cannot execute an Action", "Unknown remains visible"
    ],
    "cognitive_attention_brain_boundary_v1.md": [
        "Attention Candidate", "Brain Evaluation", "Decision Candidate", "final Goal",
        "Value", "Decision authority", "cannot issue an Action", "cannot change Reality",
        "Neural Fast Attention", "Attention Interrupt Request", "Role", "Emotion", "B Route"
    ],
    "cognitive_attention_whitebox_v1.md": [
        "Field State", "Self State", "Attention Source Registry", "Attention Competition",
        "Mandatory / Competitive / Opportunistic", "Observation Requirement", "New Evidence",
        "Risk Candidate", "Attention Interrupt Request", "Resource Reallocation", "Created",
        "Allocated", "Maintained", "Decayed", "Released", "Archived", "Value Judgment",
        "Reality mutation", "Camera", "OCR", "SLAM", "Hardware Runtime"
    ],
    "cognitive_attention_go_no_go_v1.md": [
        "Available Capacity", "Current Allocation", "Reserved Capacity", "Recovery Capacity",
        "Survival Attention", "Goal Attention", "Field Attention", "Maintenance Attention",
        "Exploration Attention", "External Demand Attention", "Survival Impact", "Goal Relevance",
        "Field Relevance", "Temporal Urgency", "Information Value", "Uncertainty Reduction",
        "Resource Cost", "Attention Requests", "Mandatory Attention", "Competitive Attention",
        "Opportunistic Attention", "Attention Interrupt Request", "Resource Reallocation Candidate",
        "Created", "Allocated", "Maintained", "Decayed", "Released", "Archived", "Persistent",
        "Temporary", "Interruptive", "Brain Evaluation", "No Emotion Runtime", "No Role Runtime",
        "No Social Field Runtime", "No B Route", "No Prediction", "No Decision", "No Action",
        "No real model call", "No Camera", "No OCR", "No SLAM", "No Hardware Runtime",
        "no automatic frequency adjustment", "no Scheduler implementation", "no online learning",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "cognitive_attention_source_registry_v1.json": [
        "Cognitive Attention Source Registry", "Survival Attention", "Goal Attention",
        "Field Attention", "Maintenance Attention", "Exploration Attention",
        "External Demand Attention", "Mandatory Attention", "Competitive Attention",
        "Opportunistic Attention", "source_is_not_decision", "source_is_not_action",
        "role_runtime", "emotion_runtime"
    ],
    "cognitive_attention_arbitration_contract_v1.json": [
        "Cognitive Attention Arbitration Contract", "Mandatory Attention", "Competitive Attention",
        "Opportunistic Attention", "may_request_preemption", "Arbitration Candidate",
        "Attention Allocation Candidate", "decision_authority", "action_authority",
        "value_judgment_authority", "automatic_action", "brain_final_evaluation"
    ],
    "cognitive_attention_field_interface_v1.json": [
        "Cognitive Attention Field Interface", "field_state", "self_state", "goal_reference",
        "risk_candidate", "resource_state", "attention_requests", "attention_competition",
        "arbitration_candidate", "attention_allocation_candidate", "observation_requirement",
        "field_update", "direct_reality_mutation", "direct_decision", "direct_action",
        "role_runtime", "emotion_runtime"
    ],
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
