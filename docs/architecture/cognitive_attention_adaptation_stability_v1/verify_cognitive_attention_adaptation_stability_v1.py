#!/usr/bin/env python3
"""V2 static verifier for Attention Adaptation and Stability architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_attention_adaptation_model_v1.md": [
        "Attention Pattern Candidate", "Experience", "Validation", "Future Allocation Candidate",
        "One event cannot change", "Unknown", "Attention high", "Attention cost reduction",
        "Deviation Detection", "Attention Increase Candidate", "Experience does not directly control Attention",
        "No online learning", "No automatic strategy modification", "No Emotion Runtime", "No Role Runtime",
        "No B Route", "No Decision", "No Action", "No Runtime"
    ],
    "attention_familiarity_model_v1.md": [
        "Unknown high", "new Field", "Attention high", "Stable Reality Pattern", "confidence",
        "Attention cost reduction candidate", "New Evidence", "Deviation Detection",
        "Attention Increase Candidate", "Current Evidence has priority", "cannot suppress Unknown",
        "cannot make a Decision", "cannot issue an Action", "automatically change an Attention Policy"
    ],
    "attention_drift_detection_model_v1.md": [
        "Attention Drift Candidate", "Attraction Drift", "Persistence Drift", "Narrowing Drift",
        "Omission Drift", "Overgeneralization Drift", "Resource Drift", "Current Field",
        "Reality", "Goal", "Validation", "Future Allocation Candidate", "does not directly correct",
        "cannot modify Brain", "cannot modify Goal", "cannot modify Reality", "single event is not enough"
    ],
    "attention_experience_boundary_v1.md": [
        "Outcome", "Experience Candidate", "Attention Pattern Candidate", "Validation",
        "Future Allocation Candidate", "Experience is a reference", "Current Reality overrides stale Experience",
        "not automatic learning", "No single event", "cannot modify Brain", "cannot modify Goal",
        "cannot modify Self Identity", "B Route", "Reflection"
    ],
    "attention_adaptation_whitebox_v1.md": [
        "Outcome", "Experience Candidate", "Attention Pattern Candidate", "Validation",
        "Future Allocation Candidate", "Unknown high", "Attention high", "Stable Reality Pattern",
        "New Evidence", "Deviation Detection", "Attention Increase Candidate", "Capability Change",
        "Attention Requirement Adjustment Candidate", "Attention Drift Candidate", "No online learning",
        "No automatic strategy modification", "No Decision", "No Action", "No Runtime"
    ],
    "attention_adaptation_go_no_go_v1.md": [
        "Attention Baseline", "Field Pattern", "Expected Attention Requirement", "Normal Observation Cost",
        "Attention Pattern Candidate", "Validation", "Future Allocation Candidate", "single event",
        "Unknown high", "new Field", "stable confidence", "cost reduction candidate", "New Evidence",
        "Deviation Detection", "Attention Increase Candidate", "Attention Drift Candidate", "attraction",
        "persistence", "narrowing", "omission", "overgeneralization", "resource drift",
        "Experience does not directly control Attention", "Capability Change",
        "Attention Requirement Adjustment Candidate", "No online learning", "No automatic strategy modification",
        "No automatic policy update", "No Brain modification", "No Goal modification", "No Decision",
        "No Action", "No Emotion Runtime", "No Role Runtime", "No B Route", "No Runtime",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "attention_baseline_contract_v1.json": [
        "Attention Baseline Contract", "field_pattern", "expected_attention_requirement",
        "normal_observation_cost", "familiarity", "uncertainty", "supporting_experience",
        "validation_status", "review_condition", "automatic_strategy_change", "single_event_adoption",
        "reality_override"
    ],
    "attention_reactivation_contract_v1.json": [
        "Attention Anomaly Reactivation Contract", "new evidence", "deviation detected",
        "risk increase candidate", "confidence decline", "capability change", "stable_pattern",
        "new_evidence", "deviation_candidate", "Attention Increase Candidate", "automatic_attention_change",
        "automatic_decision", "automatic_action", "reality_mutation"
    ],
    "attention_pattern_candidate_schema_v1.json": [
        "Attention Pattern Candidate Schema", "base_field_reference", "attention_axis_candidate",
        "expected_requirement", "normal_cost_candidate", "supporting_experience", "support_count",
        "confidence", "uncertainty", "exceptions", "validation_status", "adoption_requires_validation",
        "single_event_is_insufficient", "automatic_policy_update"
    ],
    "attention_capability_feedback_contract_v1.json": [
        "Attention Capability Feedback Contract", "capability_change", "self_capability_context",
        "field_context", "current_requirement", "visual capability decline", "audio observation",
        "Attention Requirement Adjustment Candidate", "compensation_candidate",
        "automatic_requirement_change", "automatic_strategy_change", "self_model_mutation",
        "decision_authority"
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
