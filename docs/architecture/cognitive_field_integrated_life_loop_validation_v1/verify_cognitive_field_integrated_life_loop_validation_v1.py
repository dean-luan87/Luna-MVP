#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field integrated life-loop validation."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_integrated_validation_model_v1.md": ["Reality Change", "Reality Neural Operating Space", "Reality Field", "Cognitive Field Formation", "Field State Update", "Context / Observation Requirement", "A Route Input", "Decision Candidate", "does not execute Action", "deterministic fixture"],
    "field_validation_metrics_v1.md": ["Field Transition Fidelity", "Goal-Conditioned Field Separation", "Reality Fidelity", "Self Stability", "Continuity Quality", "Unknown Preservation", "Feedback Integrity", "Parallel Isolation", "Decision Boundary"],
    "field_validation_whitebox_v1.md": ["Reality Change", "Reality Neural Operating Space", "Reality Field", "Cognitive Field Formation", "Field State Update", "Context / Observation Requirement", "A Route Input", "Decision Candidate", "no Action"],
    "field_validation_go_no_go_v1.md": ["Reality Change → Reality Neural Operating Space → Reality Field → Cognitive Field Formation → Field State Update → Context / Observation Requirement → A Route Input → Decision Candidate", "Office → Transit", "different Goal", "Fire alarm", "Self Layer", "Stable Layer", "Adaptive Layer", "Transient Layer", "Unknown", "Parallel fields", "Decision Candidate", "No Role System", "No Emotion Engine", "No Social Field Runtime", "No Multi-A Coordination", "No Prediction", "No Action", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "field_transition_test_cases_v1.json": ["space_transition_office_to_transit", "office_field", "transit_field", "fire_alarm_candidate", "field_change_only_no_action", "stable_invariants"],
    "field_continuity_test_cases_v1.json": ["home_to_office_continuity", "stable_layer_preserved", "adaptive_layer_changed", "transient_layer_released", "identity_changed", "self_layer_only"],
    "field_context_generation_test_cases_v1.json": ["same_space_different_goal", "work_task_field", "social_interaction_field", "reality_same", "field_different", "cognitive_field_package", "recommendation", "decision", "action"],
    "field_reality_feedback_test_cases_v1.json": ["reality_field", "cognitive_field", "observation_requirement", "reality_update_candidate", "evidence_and_reducer_governed_update", "unknown_preserved", "direct_reality_write"],
    "field_parallel_placeholder_test_cases_v1.json": ["navigation_field", "self_maintenance_field", "Active", "Background", "parallel_structure_only", "mutual_contamination", "multi_a_coordination", "decision_competition"],
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
