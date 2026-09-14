#!/usr/bin/env python3
"""V2 static verifier for Self Capability Awareness architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_self_capability_awareness_model_v1.md": [
        "Self Awareness Infrastructure", "Capability Identity", "Capability State",
        "Capability Confidence Candidate", "Self Capability Awareness",
        "Attention Reallocation Candidate", "A Route Confidence", "Brain Awareness Candidate",
        "Capability is not a Provider", "not Understanding", "not Reality", "not a Goal",
        "not a Decision", "not an Action", "Available", "Degraded", "Limited", "Unavailable", "Unknown",
        "Capability Confidence is confidence", "not confidence that", "provenance", "uncertainty",
        "Evidence Gateway", "cannot modify Reality", "Goal", "Decision", "Action", "Identity",
        "Personality", "Reducer remains the sole State mutation authority", "baseline is not ordinary Runtime input",
        "No real model", "No OCR", "No SLAM", "No Camera", "No Hardware Runtime", "No Action", "No Emotion",
        "No Role", "No Social Runtime", "No B Runtime", "No online learning"
    ],
    "capability_state_model_v1.md": [
        "Capability State", "Available", "Degraded", "Limited", "Unavailable", "Unknown",
        "Provider diagnostics", "Hardware diagnostics", "resource availability", "evidence quality",
        "Capability State Update Candidate", "Diagnostics", "Self Capability Awareness",
        "Provider Replacement", "Capability Identity", "Self Identity", "Goal", "Decision", "Reality",
        "not a Decision", "not Reality State", "Reducer remains the sole State mutation authority",
        "No automatic state mutation", "online learning", "model training", "hardware control", "action execution"
    ],
    "self_capability_whitebox_v1.md": [
        "Capability Registry", "Provider Diagnostics", "Capability Failure", "Diagnostics Candidate",
        "Capability State Update Candidate", "Capability Confidence Candidate", "Self Capability Context",
        "capability identity", "current state", "limitations", "uncertainty", "provenance",
        "Attention Reallocation Candidate", "A Route Confidence Input", "Brain Awareness Candidate",
        "Provider Replacement", "Capability Identity", "Self Identity", "Goal", "Decision", "Reality",
        "Capability State ≠ Reality State", "Capability Confidence ≠ Fact", "Failure Feedback ≠ Self Identity Rewrite",
        "Self Capability Awareness ≠ Brain Decision", "Reducer remains the sole State mutation authority",
        "no real model", "OCR", "SLAM", "Camera", "Hardware Runtime", "Action", "Emotion", "Role",
        "Social Runtime", "B Runtime"
    ],
    "self_capability_go_no_go_v1.md": [
        "Capability Identity", "Provider Identity", "Capability State", "Available", "Degraded", "Limited",
        "Unavailable", "Unknown", "Capability Confidence", "not Fact", "not Reality", "Self Capability State",
        "Diagnostics", "Capability State Update Candidate", "Observation Cost", "Attention Reallocation Candidate",
        "Brain", "Goal", "Decision authority", "Provider Replacement", "cognitive subject",
        "Reducer remains the sole State mutation authority", "No real model", "No OCR", "No SLAM", "No Camera",
        "No Hardware Runtime", "No Action", "No Emotion", "No Role", "No Social Runtime", "No B Runtime",
        "No online learning", "No automatic Self Model rewrite", "No direct Reality mutation",
        "No automatic frequency adjustment", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "capability_identity_contract_v1.json": [
        "Capability Identity Contract", "capability_identity", "capability_type", "semantic_boundary",
        "input_contract", "output_evidence_contract", "provider_references", "known_limitations",
        "Capability Confidence Candidate", "capability_is_not_provider", "capability_is_not_understanding",
        "capability_is_not_reality", "capability_is_not_goal", "capability_is_not_decision",
        "capability_is_not_action", "provider_cannot_define_self_identity", "capability_cannot_modify_reality",
        "capability_cannot_modify_goal", "capability_cannot_modify_decision", "capability_cannot_issue_action",
        "registry_is_not_cognitive_subject", "evidence_gateway", "sole State mutation authority"
    ],
    "capability_confidence_contract_v1.json": [
        "Capability Confidence Contract", "Capability Confidence Candidate", "confidence_scope",
        "capability evidence production only", "provenance", "timestamp", "uncertainty", "known_limitations",
        "calibration_reference", "confidence_is_not_fact", "confidence_is_not_reality",
        "confidence_requires_provenance", "confidence_requires_uncertainty", "evidence_gateway_required",
        "low_confidence_requires_caution_candidate", "confidence_cannot_modify_reality",
        "confidence_cannot_modify_goal", "confidence_cannot_modify_decision", "confidence_cannot_modify_identity",
        "no_false_certainty"
    ],
    "self_capability_state_schema_v1.json": [
        "Self Capability State Schema", "identity", "capability_states", "resource_context", "limitations",
        "health_context", "confidence_context", "provenance", "Available", "Degraded", "Limited",
        "Unavailable", "Unknown", "identity_is_stable", "capability_is_dynamic", "experience_is_reference_only",
        "personality_is_out_of_scope", "self_state_is_not_reality", "reducer_is_sole_state_mutation_authority",
        "does_not_modify_goal", "does_not_modify_decision", "does_not_modify_action", "does_not_modify_reality"
    ],
    "capability_failure_feedback_contract_v1.json": [
        "Capability Failure Feedback", "Capability Failure", "Diagnostics", "Capability State Update Candidate",
        "Self Capability Awareness", "Attention Reallocation Candidate", "Brain Awareness Candidate",
        "provider_unavailable", "protocol_error", "low_quality_evidence", "resource_exhaustion",
        "hardware_degradation", "capability_boundary_exceeded", "unknown_failure", "failure_reason",
        "diagnostic_reference", "confidence_impact", "limitation_candidate", "alternative_capability_candidate",
        "failure_does_not_modify_identity", "failure_does_not_modify_goal", "failure_does_not_modify_decision",
        "failure_does_not_modify_reality", "failure_does_not_trigger_action", "failure_does_not_trigger_online_learning",
        "diagnostics_is_not_brain", "self_awareness_is_not_decision"
    ],
    "capability_attention_interface_v1.json": [
        "Capability Attention Interface", "capability_state", "capability_confidence", "limitation",
        "observation_cost_change_candidate", "attention_reallocation_candidate", "alternative_observation_candidate",
        "uncertainty_increase_candidate", "brain_awareness_candidate", "capability_degradation",
        "Observation Cost", "Attention Reallocation Candidate", "attention_does_not_modify_capability_state",
        "capability_does_not_select_goal", "capability_does_not_select_decision", "no_automatic_frequency_adjustment",
        "no_hardware_control", "no_direct_reality_update", "evidence_gateway_required"
    ],
    "capability_brain_interface_v1.json": [
        "Capability Brain Interface", "capability_boundary", "capability_state", "capability_confidence",
        "limitations", "unknowns", "resource_constraints", "alternative_capability_candidates",
        "brain_retains_goal", "brain_retains_decision", "brain_retains_value_evaluation",
        "brain_retains_action_authority", "provider_internal_details_are_not_required",
        "capability_does_not_command_brain", "capability_does_not_modify_goal", "capability_does_not_modify_decision",
        "capability_does_not_define_reality", "capability_does_not_define_identity",
        "brain_receives_boundary_not_raw_provider_control"
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
