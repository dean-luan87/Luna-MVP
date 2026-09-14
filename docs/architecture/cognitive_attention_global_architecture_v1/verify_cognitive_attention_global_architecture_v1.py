#!/usr/bin/env python3
"""V2 static verifier for Cognitive Attention Global Architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_attention_global_architecture_v1.md": [
        "Cognitive Attention Layer", "horizontal", "Attention Perception", "Attention Allocation",
        "Attention Arbitration", "Attention Memory", "Attention Adaptation", "Attention Governance",
        "Reality", "Cognitive Field", "Experience", "Brain", "Capability", "Neural",
        "Brain Awareness Candidate", "Attention Prior Candidate", "Observation Requirement",
        "does not modify Reality", "does not modify Goal", "does not modify Decision",
        "not a control center", "Reducer remains the sole State mutation authority", "No Runtime",
        "No real model call", "No Camera", "No OCR", "No SLAM", "No Hardware"
    ],
    "cognitive_attention_global_whitebox_v1.md": [
        "Reality Evidence", "Cognitive Field", "Experience", "Cognitive Attention Layer",
        "Attention Perception", "Attention Allocation", "Attention Arbitration", "Attention Memory",
        "Attention Adaptation", "Attention Governance", "Attention Requirement", "Capability Governance",
        "Evidence", "Reality Update Candidate", "Attention Prior Candidate", "Brain Awareness Candidate",
        "Brain Evaluation", "Decision", "horizontal layer", "not a control center", "does not modify Reality",
        "does not modify Goal", "does not modify Decision", "Reducer remains the sole State mutation authority",
        "No Runtime", "No model training", "No Emotion Runtime", "No Role Runtime", "No Social Field", "No B Runtime"
    ],
    "attention_global_authority_boundary_v1.md": [
        "Authority table", "Reality", "Cognitive Field", "Attention", "Capability", "Memory/Experience",
        "Neural", "Brain", "relevance", "allocation", "arbitration", "historical prior candidates",
        "fast interrupt", "Intent", "Goal", "final evaluation", "not a control center",
        "not a second cognitive subject"
    ],
    "cognitive_attention_global_go_no_go_v1.md": [
        "Cognitive Attention Layer", "horizontal", "Reality", "Cognitive Field", "Experience", "Brain",
        "Capability", "Memory", "Neural", "Attention Perception", "Attention Allocation", "Attention Arbitration",
        "Attention Memory", "Attention Adaptation", "Attention Governance", "Brain Awareness Candidate",
        "Decision authority", "candidate-only updates", "Attention Prior Candidate", "Evidence Candidate",
        "Fast Attention Candidate", "does not modify Reality", "does not modify Goal", "does not modify Decision",
        "No Runtime", "No real model call", "No Camera", "No OCR", "No SLAM", "No Hardware Runtime",
        "No model training", "No online learning", "No Emotion Runtime", "No Role Runtime", "No Social Field",
        "No B Runtime", "No Decision", "No Action", "not a control center", "cannot replace Brain",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
    "attention_global_authority_boundary_v1.md": [
        "Authority table", "Reality", "Cognitive Field", "Attention", "Capability",
        "Memory/Experience", "Neural", "Brain", "relevance", "allocation", "arbitration",
        "Intent", "Goal", "final evaluation", "not a control center", "not a second cognitive subject"
    ],
}

JSON_REQ = {
    "attention_brain_interface_contract_v1.json": [
        "Attention Brain Interface Contract", "intent", "goal", "value_context", "resource_context",
        "Brain Awareness Candidate", "relevance", "risk", "uncertainty", "provenance", "confidence",
        "brain_evaluation", "brain_retains_goal", "brain_retains_decision", "attention_modifies_brain",
        "attention_modifies_goal", "attention_modifies_decision", "attention_issues_action"
    ],
    "attention_field_interface_contract_v1.json": [
        "Attention Cognitive Field Interface Contract", "reality_field", "field_state", "self_state",
        "goal_context", "unknowns", "attention_relevance_candidate", "allocation_candidate",
        "observation_requirement_candidate", "field_update", "cross_field_isolation",
        "direct_reality_mutation", "direct_field_mutation", "direct_decision", "context_binding_required"
    ],
    "attention_memory_interface_contract_v1.json": [
        "Attention Memory Interface Contract", "experience_candidate", "attention_weight_candidate",
        "field_context", "outcome_feedback", "attention_prior_candidate", "attention_weight",
        "emotion_weight_placeholder", "survival_weight", "meaning_weight_placeholder", "validation_required",
        "time_decay_required", "memory_directly_controls_attention", "memory_modifies_reality",
        "online_learning", "raw_recording"
    ],
    "attention_capability_interface_contract_v1.json": [
        "Attention Capability Interface Contract", "observation_requirement_candidate", "evidence_candidate",
        "capability_registry", "model_manager", "provider", "evidence_gateway", "capability_is_not_cognition",
        "attention_selects_provider", "provider_direct_reality_update", "hardware_direct_control", "model_runtime"
    ],
    "attention_neural_interface_contract_v1.json": [
        "Attention Neural Interface Contract", "resource_state", "fast_stimulus", "interrupt_candidate",
        "health_state", "fast_attention_candidate", "attention_resource_constraint", "neural_makes_decision",
        "neural_changes_goal", "neural_modifies_reality", "automatic_frequency_adjustment", "hardware_runtime"
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
