#!/usr/bin/env python3
"""V2 final verifier for Social Field architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_social_field_architecture_v1.md": [
        "Social Field", "social operating environment", "Participants", "Role Context", "Relationship Context", "Social Rules",
        "Interaction Patterns", "Social Position", "not a Contacts List", "Social Network", "Face Recognition Runtime",
        "Relationship Database", "Physical Field", "Reality", "Entity", "Spatial", "Rule", "Dynamic", "Behavior",
        "Identity Candidate", "Observation Evidence", "Confidence", "Field Presence", "Interaction History", "Identity Candidate",
        "not a confirmed identity", "Automatic identity confirmation", "permanent individual tracking", "Role belongs to Field",
        "not Identity", "Employee", "Family Member", "Resident", "Permission Boundary", "Responsibility", "Expected Behavior",
        "Relationship is a contextual", "Participant A", "Participant B", "Context", "History", "Boundary", "Colleague",
        "Friend", "Norm Rule", "Authority Rule", "Interaction Rule", "Cultural Rule", "Temporary Rule", "Evidence",
        "Social Rule Candidate", "not absolute Reality", "Interaction Pattern Candidate", "historical patterns", "not Prediction",
        "Social Position Candidate", "Identity Continuity", "Attention Candidate", "Behavior Candidate", "Social Field Memory Candidate",
        "Emotion State Candidate", "No Emotion Runtime", "No Personality Switching", "No Social Decision", "No Relationship Judgment",
        "No Human Identity Confirmation", "No Face Recognition Runtime", "No Multi-Agent", "No Hive", "No B Route", "No Prediction",
        "No Action Runtime", "No Social Runtime"
    ],
    "interaction_pattern_model_v1.md": [
        "Interaction Pattern Candidate", "bounded observation", "social interaction", "Field", "Time", "participants", "context",
        "observed sequence", "evidence", "confidence", "Unknown", "history", "provenance", "meeting host pattern",
        "repeated speaking order", "recurring handoff", "not Prediction", "not intention", "not emotion", "relationship judgment",
        "not Decision", "single observation", "Attention Candidate", "Behavior Candidate", "Social Field Memory Candidate", "Action",
        "Identity"
    ],
    "social_field_whitebox_v1.md": [
        "Physical Field", "Social Evidence", "Social Field", "Participants", "Role", "Relationship", "Social Rule",
        "Interaction Pattern", "Attention Candidate", "Behavior Candidate", "Memory Candidate", "Who creates a Participant",
        "Observation Evidence", "Identity Candidate", "never confirms Human Identity", "Who assigns a Role", "Field Context",
        "Role belongs to Field", "not Identity", "Who forms Relationship", "Interaction History", "Emotion", "Who validates Social Rule",
        "Evidence, Confidence, Unknown", "not absolute Reality", "Who owns Goal and Decision", "Social Decision", "Who modifies Reality",
        "Reality Reducer", "Social Field → Attention Candidate", "Social Field → Behavior Candidate", "Social Field → Social Field Memory Candidate",
        "Social Field → Emotion", "placeholder-only", "Social Field → Decision", "Relationship → Emotion Judgment", "Role → Identity Mutation",
        "Participant → Human Identity Confirmation", "Interaction Pattern → Prediction", "Unknown", "Confidence", "provenance", "Planning Only"
    ],
    "social_field_go_no_go_v1.md": [
        "Social Field", "contextual social operating environment", "contact list", "social network", "face recognition system",
        "relationship database", "Identity Candidate", "Observation Evidence", "Confidence", "Field Presence", "Interaction History",
        "Role belongs to Field", "not Identity", "permission", "responsibility", "expected behavior", "Relationship", "participants",
        "context", "time", "history", "boundary", "Norm", "Authority", "Interaction", "Cultural", "Temporary",
        "Evidence", "Unknown", "Interaction Pattern", "not Prediction", "Identity Continuity", "Memory does not override Reality",
        "Emotion is placeholder-only", "No Emotion Runtime", "No Personality Switching", "No Social Decision", "No Relationship Judgment",
        "No Human Identity Confirmation", "No Face Recognition Runtime", "No Multi-Agent", "No Hive", "No B Route", "No Prediction",
        "No Action Runtime", "No Social Runtime", "directly modify Reality", "Identity", "Goal", "Decision", "Action",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "social_field_schema_v1.json": [
        "Social Field Schema v1", "social_field_id", "physical_field_reference", "participants", "roles", "relationships",
        "social_rules", "interaction_patterns", "social_position_candidate", "field_context", "timestamp", "confidence", "unknowns",
        "provenance", "identity_continuity_required", "social_field_does_not_make_decision", "social_field_does_not_modify_reality",
        "unknowns_are_preserved"
    ],
    "social_participant_contract_v1.json": [
        "Social Participant Contract v1", "participant_id", "identity_candidate", "observation_evidence", "confidence", "field_presence",
        "interaction_history", "timestamp", "provenance", "unknowns", "identity_is_not_confirmed", "human_identity_confirmation",
        "face_recognition_runtime", "permanent_individual_tracking", "participant_does_not_make_decision", "unknowns_are_preserved"
    ],
    "role_context_model_v1.json": [
        "Role Context Model v1", "role_context_id", "field_context", "role_candidate", "Employee", "permission_boundary",
        "responsibility", "expected_behavior", "confidence", "unknowns", "role_belongs_to_field", "role_does_not_belong_to_identity",
        "role_does_not_modify_self_identity", "role_does_not_make_decision", "unknowns_are_preserved"
    ],
    "relationship_context_schema_v1.json": [
        "Relationship Context Schema v1", "relationship_id", "participant_a", "participant_b", "context", "history", "confidence",
        "boundary", "timestamp", "provenance", "unknowns", "relationship_is_contextual", "relationship_is_temporal",
        "direct_emotion_inference", "relationship_does_not_make_decision", "unknowns_are_preserved"
    ],
    "social_rule_contract_v1.json": [
        "Social Rule Contract v1", "rule_candidate_id", "rule_type", "Norm Rule", "Authority Rule", "Interaction Rule",
        "Cultural Rule", "Temporary Rule", "field_context", "evidence", "confidence", "unknowns", "provenance", "rule_is_candidate",
        "rule_is_not_absolute_reality", "rule_does_not_modify_reality", "rule_does_not_make_decision", "rule_does_not_infer_emotion",
        "unknowns_are_preserved"
    ],
    "interaction_pattern_model_v1.json": [
        "Interaction Pattern Model v1", "pattern_id", "participants", "field_context", "observed_sequence", "evidence", "confidence",
        "unknowns", "history", "provenance", "pattern_is_historical_observation", "pattern_is_not_prediction",
        "pattern_does_not_make_decision", "pattern_does_not_infer_emotion", "pattern_does_not_confirm_identity", "unknowns_are_preserved"
    ],
    "social_field_attention_interface_v1.json": [
        "Social Field Attention Interface v1", "social_field_reference", "participants", "role_context", "relationship_context",
        "social_rule_candidates", "interaction_pattern_candidates", "attention_candidate", "information_value", "risk_context", "unknowns",
        "social_field_provides_attention_candidate", "social_field_does_not_allocate_attention_directly", "social_field_does_not_modify_goal",
        "social_field_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "social_field_memory_interface_v1.json": [
        "Social Field Memory Interface v1", "social_field_reference", "social_field_memory_candidate", "interaction_history",
        "role_history", "relationship_history", "field_context", "timestamp", "provenance", "unknowns", "memory_is_candidate",
        "memory_does_not_override_reality", "memory_does_not_make_decision", "unknowns_are_preserved"
    ],
    "social_field_self_interface_v1.json": [
        "Social Field Self Interface v1", "social_field_reference", "self_reference", "role_context", "social_position_candidate",
        "attention_candidate", "behavior_candidate", "goal_context_candidate", "identity_continuity_required",
        "role_does_not_modify_identity", "social_field_does_not_make_decision", "unknowns_are_preserved"
    ],
    "social_emotion_placeholder_v1.json": [
        "Social Emotion Placeholder v1", "social_field_reference", "role_reference", "relationship_reference", "memory_reference",
        "emotion_state_candidate", "placeholder_only", "emotion_runtime", "emotion_does_not_modify_reality", "emotion_does_not_make_decision",
        "emotion_does_not_modify_identity", "unknowns_are_preserved"
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
