#!/usr/bin/env python3
"""V2 final verifier for Cognitive Emotion Engine architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_emotion_engine_architecture_v1.md": [
        "Emotion Engine", "internal state feedback layer", "Field", "Role", "Relationship", "Expectation", "Memory", "Value", "Drive",
        "Reality Feedback", "Self State", "Emotion State Candidate", "Decision", "Goal", "Action controller", "Emotion Input Package",
        "Field Context", "Role Context", "Relationship Context", "Evidence", "Provenance", "Confidence", "Unknown", "Valence", "Arousal",
        "Stability", "Attachment", "Field Emotion Attachment", "Role Emotion", "Relationship Emotion Context", "work Field", "friend Field",
        "family Field", "Event Memory", "Experience Memory", "Emotion Attachment", "Emotion Experience Candidate", "Attention Influence Candidate",
        "Drive Modulation Candidate", "Emotion Reference", "Goal authority", "Value authority", "final Decision authority",
        "Triggered → Active → Decay → Integrated → Archived", "Reality priority", "revocability", "No emotion recognition runtime",
        "No automatic emotional expression", "personality-switching Runtime", "No automatic Value change", "No automatic Identity change",
        "No Social Judgment", "No B Simulation", "No Action Runtime"
    ],
    "emotion_whitebox_v1.md": [
        "Field / Role / Relationship / Expectation / Reality Feedback", "Memory / Self State / Drive / Value", "Emotion Input Package",
        "Emotion State Candidate", "Attention", "Drive", "Memory", "Learning", "Brain Reference", "Who supplies Emotion inputs",
        "Who creates the state", "Who owns factual truth", "Reality Workspace", "Evidence Gateway", "Who stores historical feeling",
        "Emotion Attachment", "Who receives attention influence", "Who receives drive modulation", "Who owns Goal, Value, and final Decision",
        "Who can revoke an incorrect attachment", "Emotion Governance", "Emotion → Attention Influence Candidate", "Emotion → Drive Modulation Candidate",
        "Emotion → Memory Candidate", "Emotion → Learning Candidate", "Emotion → Decision", "Emotion → Goal Mutation", "Emotion → Value Mutation",
        "Emotion → Identity Mutation", "Emotion → Action", "Emotion → Social Judgment", "Emotion → automatic expression", "context-bound",
        "multidimensional", "uncertain", "revocable", "Planning Only", "Emotion Runtime"
    ],
    "emotion_go_no_go_v1.md": [
        "internal state feedback layer", "not Decision", "Goal", "Value", "Action authority", "Emotion Input Package", "Field", "Role",
        "Relationship", "Expectation", "Reality Feedback", "Memory", "Self State", "Valence", "Arousal", "Stability", "Attachment", "Confidence",
        "Field Emotion Attachment", "Role Emotion", "Relationship Emotion Context", "context", "history", "Memory", "Learning", "Attention", "Drive",
        "candidate only", "Brain", "Goal", "Value", "final Decision authority", "Triggered", "Active", "Decay", "Integrated", "Archived",
        "Reality priority", "Unknown preservation", "provenance", "revocability", "No emotion recognition runtime", "No automatic emotional expression",
        "No automatic Value change", "No automatic Identity change", "No Social Judgment", "No B Simulation", "No Action Runtime", "cannot modify Reality",
        "Decision", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "emotion_state_schema_v1.json": [
        "Emotion State Schema v1", "emotion_state_id", "valence", "arousal", "stability", "attachment", "confidence", "intensity", "duration",
        "field_context", "role_context", "relationship_context", "unknowns", "emotion_state_candidate", "does_not_make_decision", "unknowns_are_preserved"
    ],
    "emotion_input_contract_v1.json": [
        "Emotion Input Contract v1", "field_context", "role_context", "relationship_context", "expectation", "reality_feedback", "memory",
        "self_state", "evidence", "provenance", "confidence", "unknowns", "stimulus_alone_is_insufficient", "emotion_input_is_candidate",
        "unknowns_are_preserved"
    ],
    "field_emotion_binding_v1.json": [
        "Field Emotion Binding v1", "field_reference", "field_context", "field_history", "emotion_state_candidate", "evidence", "confidence", "unknowns",
        "field_emotion_attachment", "emotion_is_context_bound", "field_does_not_make_emotion_judgment", "unknowns_are_preserved"
    ],
    "role_emotion_binding_v1.json": [
        "Role Emotion Binding v1", "role_reference", "active_role", "field_context", "responsibility", "expectation", "emotion_state_candidate",
        "role_emotion_candidate", "role_does_not_modify_identity", "unknowns_are_preserved"
    ],
    "relationship_emotion_context_v1.json": [
        "Relationship Emotion Context v1", "participant_a", "participant_b", "relationship_reference", "field_context", "relationship_history", "boundary",
        "confidence", "emotion_state_candidate", "relationship_emotion_is_not_judgment", "social_judgment", "unknowns_are_preserved"
    ],
    "emotion_memory_interface_v1.json": [
        "Emotion Memory Interface v1", "event_memory", "experience_memory", "emotion_attachment", "field_context", "role_context", "relationship_context",
        "provenance", "emotion_is_separate_from_fact", "memory_candidate_only", "memory_does_not_override_reality", "unknowns_are_preserved"
    ],
    "emotion_learning_interface_v1.json": [
        "Emotion Learning Interface v1", "emotion_experience_candidate", "pattern_candidate", "attention_change_candidate", "strategy_modification",
        "validation_required", "revocation_supported", "emotion_does_not_directly_modify_strategy", "emotion_does_not_auto_learn", "unknowns_are_preserved"
    ],
    "emotion_attention_interface_v1.json": [
        "Emotion Attention Interface v1", "emotion_state_reference", "attention_influence_candidate", "field_context", "role_context", "arousal", "risk",
        "emotion_does_not_allocate_attention", "attention_candidate_only", "unknowns_are_preserved"
    ],
    "emotion_drive_interface_v1.json": [
        "Emotion Drive Interface v1", "emotion_state_reference", "drive_modulation_candidate", "drive_reference", "valence", "arousal",
        "modulation_is_candidate_only", "emotion_does_not_own_drive", "unknowns_are_preserved"
    ],
    "emotion_brain_interface_v1.json": [
        "Emotion Brain Interface v1", "emotion_reference", "emotion_state_candidate", "field_context", "role_context", "relationship_context",
        "brain_receives_emotion_reference", "brain_retains_goal_authority", "brain_retains_value_authority", "brain_retains_final_decision_authority",
        "emotion_does_not_make_decision", "unknowns_are_preserved"
    ],
    "emotion_lifecycle_contract_v1.json": [
        "Emotion Lifecycle Contract v1", "Triggered", "Active", "Decay", "Integrated", "Archived", "Triggered → Active", "Active → Decay",
        "Decay → Integrated", "Integrated → Archived", "decay_is_context_and_evidence_aware", "integration_creates_memory_candidate",
        "integration_creates_learning_candidate", "lifecycle_does_not_make_decision", "unknowns_are_preserved"
    ],
    "emotion_governance_contract_v1.json": [
        "Emotion Governance Contract v1", "reality_priority", "unknowns_are_preserved", "provenance_required", "confidence_required",
        "context_binding_required", "revocability_required", "emotion_recognition_runtime", "automatic_emotional_expression", "personality_switching_runtime",
        "automatic_value_change", "automatic_identity_change", "social_judgment", "b_simulation", "action_runtime", "emotion_does_not_modify_reality",
        "emotion_does_not_modify_goal", "emotion_does_not_modify_value", "emotion_does_not_modify_identity", "emotion_does_not_modify_decision"
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
