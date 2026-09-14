#!/usr/bin/env python3
"""V2 static verifier for Cognitive Observation Cycle Governance."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_observation_cycle_model_v1.md": [
        "Observation Requirement", "Observation Requirement ≠ Observation Execution",
        "Created", "Qualified", "Allocated", "Executing Candidate", "Evidence Received",
        "Evaluated", "Completed / Suspended", "Observation Priority", "Information Value",
        "Resource Cost", "Transient Observation", "Persistent Observation",
        "Background Observation", "Reality Update Candidate", "Field Reassessment",
        "Reducer remains the sole State mutation authority", "no real model call",
        "no Camera Runtime", "no OCR Runtime", "no SLAM Runtime", "no Hardware Runtime",
        "no Action Runtime"
    ],
    "observation_priority_model_v1.md": [
        "Observation Priority", "Survival Impact", "Goal Alignment", "Reality Uncertainty",
        "Temporal Urgency", "Information Value", "Resource Cost", "Allocation Candidate",
        "not a Scheduler", "does not implement a Scheduler", "Unknown"
    ],
    "observation_budget_governance_v1.md": [
        "camera/sensor", "microphone", "CPU/GPU", "battery/energy", "Information Value",
        "Resource Cost", "Budget Evaluation", "Allocation Candidate", "not a Scheduler",
        "does not implement a Scheduler", "Resource Constraint Candidate", "Unknown"
    ],
    "evidence_feedback_loop_v1.md": [
        "Observation", "Evidence", "Evidence Validation", "Reality Update Candidate",
        "Reality Workspace", "Reducer remains the sole State mutation authority",
        "Field Reassessment", "does not directly change the Field", "Human Feedback",
        "no automatic retry", "no automatic model switch", "no online learning"
    ],
    "observation_failure_boundary_v1.md": [
        "Capability Failure", "Evidence Quality Decline", "Observation Retry Candidate",
        "Alternative Capability Candidate", "Provider unavailable", "protocol error",
        "resource budget unavailable", "stale Evidence", "Unknown", "Self Capability Candidate",
        "does not directly modify the Self Model", "does not automatically execute a retry"
    ],
    "observation_cycle_whitebox_v1.md": [
        "Cognitive Field", "Observation Requirement", "Created", "Qualified", "Allocated",
        "Executing Candidate", "Evidence Received", "Evaluated", "Completed / Suspended",
        "Reality Update Candidate", "Field Reassessment", "Observation Priority Candidate",
        "Observation Budget", "Capability Failure", "Evidence Quality Decline",
        "Observation Retry Candidate", "Alternative Capability Candidate",
        "Observation Requirement ≠ Observation Execution", "Reducer remains the sole State mutation authority",
        "No Camera", "No OCR", "No SLAM", "No Hardware"
    ],
    "observation_cycle_go_no_go_v1.md": [
        "Observation lifecycle", "Observation Requirement is not Observation Execution",
        "Survival Impact", "Goal Alignment", "Reality Uncertainty", "Temporal Urgency",
        "Information Value", "Resource Cost", "Transient Observation", "Persistent Observation",
        "Background Observation", "release condition", "Observation → Evidence → Reality Update Candidate",
        "Field Reassessment", "Reducer remains the sole State mutation authority",
        "Capability Failure", "Evidence Quality Decline", "Observation Retry Candidate",
        "Alternative Capability Candidate", "No real model call", "No Camera Runtime", "No OCR Runtime",
        "No SLAM Runtime", "No Hardware Runtime", "No Action Runtime", "No Emotion Engine",
        "No Role System", "No B Route", "no Scheduler implementation", "no automatic retry",
        "no automatic model switching", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "observation_lifecycle_contract_v1.json": [
        "Observation Lifecycle Contract", "Created", "Qualified", "Allocated",
        "Executing Candidate", "Evidence Received", "Evaluated", "Completed", "Suspended",
        "observation_requirement_is_not_observation_execution", "direct_field_mutation",
        "direct_decision", "direct_action", "Reducer remains the sole State mutation authority"
    ],
    "observation_persistence_contract_v1.json": [
        "Transient Observation", "Persistent Observation", "Background Observation",
        "release", "requires_release_condition", "unbounded_stream", "automatic_frequency_adjustment",
        "hardware_control", "runtime_execution"
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
