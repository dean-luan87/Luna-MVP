#!/usr/bin/env python3
"""V2 static verifier for Attention Experience Adaptation and Stability."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_attention_experience_adaptation_model_v1.md": [
        "Field Experience", "Pattern Extraction", "Attention Prior Candidate",
        "Attention Allocation Adjustment Candidate", "Future Attention", "Experience Candidate",
        "Attention Pattern Candidate", "cannot directly modify Attention", "single event",
        "Field Context", "Outcome Feedback", "Unknown Field", "Learning Field", "Stable Field",
        "Changed Field", "Attention Reactivation Candidate", "Attention Drift Candidate",
        "Pattern Strength", "Experience Frequency", "Validation Confidence", "Time Decay",
        "Capability Change", "Attention Requirement Candidate", "Observation Strategy Candidate",
        "Historical Attention Pattern", "B Route is a placeholder", "No automatic learning",
        "No automatic attention policy change", "No Decision", "No Action", "No Model Training"
    ],
    "attention_prior_model_v1.md": [
        "Current Field", "Historical Pattern", "Self Capability", "Current Goal",
        "Attention Prior Candidate", "Prior is not Decision", "Prior is not Fact", "Attention Requirement Candidate",
        "Current Reality overrides Historical Pattern", "cannot hide Unknown", "cannot issue an Action",
        "not automatic learning", "not a model update"
    ],
    "attention_familiarity_model_v1.md": [
        "Unknown Field", "Learning Field", "Stable Field", "Changed Field", "high Unknown",
        "high initial Attention demand", "Stable does not mean closed", "Current Evidence has priority",
        "Attention Prior Candidate", "Reduced Observation Candidate", "cannot directly close observation",
        "make a Decision", "issue an Action", "modify an Attention Policy"
    ],
    "attention_reactivation_boundary_v1.md": [
        "Stable Pattern", "Reality Deviation", "Attention Reactivation Candidate",
        "Increase Observation Candidate", "New Evidence", "confidence decline", "risk increase",
        "Capability Change", "cannot suppress an anomaly", "cannot erase Unknown", "Reduced Observation Candidate",
        "does not directly modify Attention", "does not perform automatic learning"
    ],
    "attention_drift_detection_model_v1.md": [
        "Attention Drift Candidate", "Attraction Drift", "Persistence Drift", "Narrowing Drift",
        "Omission Drift", "Overgeneralization Drift", "Resource Drift", "Historical Attention Pattern",
        "Current Reality", "Validation", "Attention Allocation Adjustment Candidate", "cannot automatically correct",
        "cannot modify Brain", "cannot modify Goal", "cannot modify Reality", "single event is insufficient"
    ],
    "attention_decay_model_v1.md": [
        "Pattern Strength", "Experience Frequency", "Validation Confidence", "Time Decay",
        "Reduced Prior Candidate", "Review Candidate", "Expiry Candidate", "Revalidation Candidate",
        "ten-year-old accident", "cannot retain maximum alert priority", "cannot erase", "cannot suppress new Evidence",
        "not automatic learning"
    ],
    "attention_experience_boundary_v1.md": [
        "Outcome", "Experience Candidate", "Attention Pattern Candidate", "Validation",
        "Future Allocation Candidate", "Experience is a reference", "Current Reality overrides stale Experience",
        "not automatic learning", "No single event", "cannot modify Brain", "cannot modify Goal",
        "cannot modify Self Identity", "B Route", "Reflection"
    ],
    "attention_b_route_placeholder_v1.md": [
        "B Route is not implemented", "B Runtime is prohibited", "Simulation Field", "Historical Attention Pattern",
        "Simulation Observation", "Simulation cannot modify A Reality", "current Self", "Decision", "Action",
        "No Simulation Runtime", "Prediction", "Planning", "automatic attention", "model training",
        "Simulation Result Candidate"
    ],
    "attention_adaptation_whitebox_v1.md": [
        "Field Experience", "Pattern Extraction", "Attention Prior Candidate", "Attention Allocation Adjustment Candidate",
        "Field Context", "Condition", "Observed Pattern", "Attention Requirement", "Outcome Feedback",
        "Unknown Field", "Learning Field", "Stable Field", "Changed Field", "Reality Deviation",
        "Attention Reactivation Candidate", "Capability Change", "Simulation Field", "Historical Attention Pattern",
        "Simulation Observation", "does not directly control Attention", "No automatic learning", "No Action",
        "No Model Training"
    ],
    "attention_adaptation_go_no_go_v1.md": [
        "Pattern Extraction", "Attention Prior Candidate", "Field Attention Memory", "Field Context", "Condition",
        "Observed Pattern", "Attention Requirement", "Outcome Feedback", "Historical Pattern", "Self Capability",
        "Current Goal", "Unknown Field", "Learning Field", "Stable Field", "Changed Field", "Reality Deviation",
        "Attention Reactivation Candidate", "Increase Observation Candidate", "Attention Drift Candidate", "attraction",
        "persistence", "narrowing", "omission", "overgeneralization", "resource drift", "Pattern Strength",
        "Experience Frequency", "Validation Confidence", "Time Decay", "Capability Change", "Observation Strategy Candidate",
        "Simulation Field", "Simulation Observation", "B Route is not implemented", "No automatic learning",
        "No automatic strategy change", "No Brain modification", "No Goal modification", "No Decision", "No Action",
        "No Emotion Runtime", "No Role Runtime", "No Social Runtime", "No B Runtime", "No Model Training",
        "No Simulation Runtime", "No Runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "attention_experience_boundary_contract_v1.json": [
        "Attention Experience Boundary Contract", "experience_candidate", "field_context", "self_capability",
        "reality_stability", "outcome_feedback", "Attention Pattern Candidate", "single_event_insufficient",
        "provenance_required", "confidence_required", "scope_required", "Attention Prior Candidate",
        "direct_attention_control", "direct_brain_modification", "direct_goal_modification", "direct_decision",
        "direct_reality_mutation"
    ],
    "field_attention_memory_schema_v1.json": [
        "Field Attention Memory Schema", "field_context", "field_id", "field_type", "time_reference",
        "space_reference", "self_capability_reference", "condition", "observed_pattern", "attention_requirement",
        "outcome_feedback", "supporting_experience", "validation_confidence", "pattern_scope", "time_decay",
        "exceptions", "memory_is_not_raw_log", "memory_does_not_override_reality"
    ],
    "attention_adaptation_candidate_contract_v1.json": [
        "Attention Adaptation Candidate Contract", "current_attention", "historical_pattern", "self_capability",
        "reality_stability", "current_goal", "Attention Prior Candidate", "Attention Allocation Adjustment Candidate",
        "Reduced Observation Candidate", "Alternative Observation Candidate", "Attention Reactivation Candidate",
        "Attention Drift Candidate", "requires_validation", "single_event_adoption", "automatic_allocation_change",
        "automatic_strategy_change", "automatic_learning", "decision_authority", "action_authority"
    ],
    "attention_capability_feedback_contract_v1.json": [
        "Attention Capability Feedback Contract", "capability_change", "self_capability", "field_context",
        "current_requirement", "visual capability decline", "audio", "Human Feedback", "Attention Requirement Candidate",
        "Observation Strategy Candidate", "Alternative Observation Candidate", "automatic_requirement_change",
        "automatic_strategy_change", "self_model_mutation", "decision_authority", "action_authority"
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
