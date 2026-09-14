#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field Dynamics and Process architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_dynamics_model_v1.md": ["Cognitive Field Dynamics", "Field Creation Source", "Brain Intent", "Neural Detection", "External Event", "User", "Field Lifecycle", "Attention Requirement", "Field Update", "Experience Candidate"],
    "cognitive_field_activation_policy_v1.md": ["Brain Intent", "Neural Detection", "External Event", "User", "Field Candidate", "does not perform Decision", "does not perform Prediction", "Attention does not create a Field"],
    "cognitive_field_priority_boundary_v1.md": ["Survival", "Goal Context", "Urgency", "Resource Cost", "Attention Demand", "Multi-A Coordination", "role competition", "Emotional Relationship Calculation", "Suspension Candidate", "Closure Candidate"],
    "cognitive_field_attention_interface_v1.md": ["Active Cognitive Field", "Attention Requirement", "Observation Candidate", "Field Update Candidate", "Attention does not create a Field", "Field does not decide a Goal", "does not perform Decision", "does not perform Planning", "does not perform Prediction"],
    "cognitive_field_process_binding_model_v1.md": ["Process ID", "Field ID", "Intent Reference", "Lifecycle Reference", "Resource Budget Candidate", "Priority Candidate", "Escalation Path", "Multi-A Coordination", "cannot create an independent Goal"],
    "cognitive_field_resource_boundary_v1.md": ["Allocation Candidate", "Attention", "compute", "memory", "energy", "network", "Expected Value", "Resource Cost", "not a Scheduler", "Escalation Candidate"],
    "cognitive_field_memory_boundary_v1.md": ["Field is not Memory", "Experience Candidate", "Candidate → Validation → Adoption", "Personality", "Identity", "Value System", "single field event"],
    "cognitive_field_whitebox_v1.md": ["Field Creation Source", "Created", "Active", "Background", "Suspended", "Closed", "Archived", "Attention Requirement", "Observation", "Field Update", "no Multi-A Coordination", "no Decision", "no Prediction"],
    "cognitive_field_go_no_go_v1.md": ["Field Creation Source", "Brain Intent", "Neural Detection", "External Event", "User", "Survival", "Goal", "Urgency", "Resource Cost", "Attention Demand", "Created", "Active", "Background", "Suspended", "Closed", "Archived", "Attention does not create a Field", "Field does not decide a Goal", "Experience Candidate", "does not accumulate Personality", "not a Scheduler", "No Multi-A Coordination", "no multi-role competition", "no emotional relationship calculation", "no Prediction", "no Decision", "no Action Runtime", "no real model", "no OCR", "no SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "cognitive_field_lifecycle_transition_v1.json": ["Created", "Active", "Background", "Suspended", "Closed", "Archived", "transition_is_not_decision", "transition_is_not_action", "lifecycle_is_not_runtime"],
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
