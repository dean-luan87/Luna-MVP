#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field Continuous Flow validation."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_continuous_flow_validation_model_v1.md": ["continuous cognitive flow", "24-hour", "Reality Change", "Reality Neural Operating Space", "Reality Field", "Cognitive Field", "Field State / Continuity", "A Route Input", "Decision Candidate", "does not execute a Decision or Action", "deterministic fixture"],
    "field_persistence_validation_model_v1.md": ["Stable Layer", "Adaptive Layer", "Transient Layer", "Home", "Commute", "Office", "Commercial", "Unknown", "Identity Drift", "cross-field leakage", "not Memory"],
    "long_running_field_metrics_v1.md": ["Field Existence Continuity", "Transition Fidelity", "Stable Layer Stability", "Adaptive Layer Responsiveness", "Transient Cleanup", "Event Stream Integrity", "Unknown Persistence", "Pollution Isolation", "Parallel Structure Integrity", "Action Boundary"],
    "continuous_flow_whitebox_v1.md": ["08:00 Home Field Active", "09:00 Commute Field Active", "10:00 Office Field Active", "18:00 Commercial Field Active", "20:00 Home Field Active", "Stable Layer Continuity", "Adaptive Layer Update", "Transient Layer Create / Release", "Decision Candidate boundary", "does not execute Action"],
    "go_no_go_v1.md": ["24-hour timeline", "Stable Layer", "Adaptive Layer", "Transient Layer", "Multi-event stream", "Unknown remains Unknown", "one Field does not rewrite another Field", "Self Identity remains continuous", "Active/Background parallel fields", "Decision Candidate", "No Emotion Engine", "No Social Field Runtime", "No Role System", "No Multi-A", "No B", "No Prediction", "No Action", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "continuous_field_transition_scenarios_v1.json": ["24h", "08:00", "home_field", "commute_field", "office_field", "commercial_field", "stable_layer", "adaptive_layer_changes", "transient_layer_policy", "identity_drift", "action_execution"],
    "multi_event_field_stream_fixture_v1.json": ["multi_event_field_stream", "user_enters_meeting_room", "message_received", "battery_decreases", "network_changes", "context_preserved", "state_pollution", "decision_output"],
    "field_pollution_boundary_test_cases_v1.json": ["work_context_isolated_from_home_reality", "no_reality_state_pollution", "experience_candidate_allowed", "unknown_person_persists", "auto_resolved", "invented_relationship"],
    "self_continuity_stream_test_cases_v1.json": ["identity_across_daily_fields", "identity_drift", "stable_layer", "resource_change_without_identity_change", "adaptive_self_resource_constraint"],
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
