#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field State and Continuity architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_state_model_v1.md": ["Stable", "Adaptive", "Transient", "Field State", "Identity", "Unknown", "not a Decision"],
    "cognitive_field_continuity_contract_v1.md": ["Field Continuity", "Field change is not Identity change", "Stable Context", "Adaptive Context", "Transient Context", "Survival Constitution", "does not create a Role System", "cannot change Identity"],
    "cognitive_field_stable_adaptive_transient_model_v1.md": ["Stable Layer", "Adaptive Layer", "Transient Layer", "Survival Constitution", "Identity", "Core Capability", "temporary", "not three personalities"],
    "cognitive_field_hierarchy_model_v1.md": ["Reality Field: City", "Commercial District", "Building / Mall", "Room / Counter", "Task Context Field", "parent fields", "child fields", "not a command hierarchy", "Multi-A Coordination"],
    "cognitive_field_self_relation_boundary_v1.md": ["Self Presentation Candidate", "not a new Self", "Role System", "Stable Identity", "Capability", "Limitation", "No Emotional Relationship Calculation", "Personality Formation"],
    "cognitive_field_reality_feedback_contract_v1.md": ["Reality Field", "Cognitive Field", "Observation Requirement", "Reality Update Candidate", "Evidence", "Provenance", "Reducer", "does not execute Action"],
    "cognitive_field_parallel_state_placeholder_v1.md": ["Navigation Field", "Home Safety Field", "Maintenance Field", "Active", "Background", "Suspended", "structural only", "Multi-A Coordination", "does not decide who wins"],
    "cognitive_field_state_whitebox_v1.md": ["Stable", "Adaptive", "Transient", "Leaving", "Entering", "Shared", "Suspended", "Field Transition", "Observation Requirement", "Reality Update Candidate", "does not perform Decision", "Emotional Relationship Calculation"],
    "cognitive_field_state_go_no_go_v1.md": ["Stable Layer", "Adaptive Layer", "Transient Layer", "Leaving Context", "Entering Context", "Shared Context", "Suspended Context", "Field Continuity", "Self Presentation Candidate", "Reality Field → Cognitive Field → Observation Requirement → Reality Update Candidate", "structural placeholders only", "not Memory", "No Role System", "No Emotional Relationship Calculation", "No Multi-A Coordination", "No Brain Coordination", "No Prediction", "No Decision", "No Action Runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "cognitive_field_transition_package_v1.json": ["field_transition_package", "leaving_context", "entering_context", "shared_context", "suspended_context", "stable_context_reference", "adaptive_context_reference", "transient_context_reference", "transition_is_not_identity_change", "transition_is_not_decision"],
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
