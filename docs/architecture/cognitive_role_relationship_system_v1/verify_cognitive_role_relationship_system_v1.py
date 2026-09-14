#!/usr/bin/env python3
"""V2 final verifier for Role and Relationship System contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_role_system_model_v1.md": [
        "Identity ≠ Role", "Identity is long-term", "Role is a Field-bound", "Field", "Responsibility", "Permission", "Expectation",
        "Behavior Boundary", "Duration", "Social Field", "Role Assignment Candidate", "Relationship Context", "Social Position",
        "Behavior Candidate", "Emotion Interface", "Field Context", "Evidence", "Confidence", "Unknown", "Employee Candidate",
        "Family Member Candidate", "does not modify Identity", "Role Activation", "Created", "Active", "Background", "Suspended", "Closed",
        "Role Conflict Candidate", "does not automatically resolve", "Interaction Experience", "Relationship Memory", "Relationship Candidate",
        "Attention Candidate", "Social Position Candidate", "Emotion State Candidate", "No Emotion Runtime", "No Personality Switching",
        "No Relationship Judgment", "No Face Recognition", "No Social Action", "No Multi-Agent", "No Hive", "No B Route", "No Prediction",
        "No Action Runtime"
    ],
    "relationship_state_model_v1.md": [
        "Relationship is a contextual", "temporal candidate", "Participant A", "Participant B", "Context", "History", "Confidence",
        "Evidence", "Boundary", "Initial", "Developing", "Stable", "Changed", "Unknown", "Archived", "Colleague", "Friend Candidate",
        "Interaction Experience", "Relationship Memory", "Relationship Candidate", "Cooperation Candidate", "confirmed friendship",
        "emotional judgment", "Goal", "Decision", "Social Action", "Relationship Conflict Candidate", "Current Reality > Memory",
        "Emotion Runtime"
    ],
    "role_whitebox_v1.md": [
        "Social Field", "Role Assignment Candidate", "Relationship Context", "Social Position", "Behavior Candidate", "Emotion Interface Placeholder",
        "Who activates Role", "Field Context", "Role cannot mutate", "Identity", "Who owns Identity", "Who evolves Relationship",
        "Interaction Experience", "Relationship Memory", "Who resolves Role Conflict", "Role Conflict Candidate", "does not auto-resolve",
        "Who owns Goal and final Decision", "Brain", "Social Action", "Action Runtime", "relationship confidence", "Role Context → Attention Candidate",
        "Role Context → Behavior Candidate", "Relationship → Relationship Candidate", "Role/Relationship → Emotion State Candidate",
        "Role → Identity Mutation", "Relationship → Emotion Judgment", "Role → Decision", "Relationship → Social Action", "Model → Relationship Judgment",
        "Planning Only", "No Personality Switching", "No Face Recognition", "No Multi-Agent", "No Hive", "No B Route", "No Prediction",
        "No Emotion Runtime", "No Action Runtime"
    ],
    "role_go_no_go_v1.md": [
        "Identity ≠ Role", "Role belongs to Field", "not Identity", "Field Context", "Responsibility", "Permission", "Expectation",
        "Behavior Boundary", "Duration", "Role lifecycle", "Created", "Active", "Background", "Suspended", "Closed", "Role Activation",
        "Role Assignment Candidate", "Role Conflict Candidate", "automatic resolution", "Relationship states", "Initial", "Developing", "Stable",
        "Changed", "Unknown", "Archived", "Participant A", "Participant B", "Context", "History", "Confidence", "Evidence", "Boundary",
        "Interaction Experience", "Relationship Memory", "Attention", "Behavior", "Emotion", "candidate/placeholder-only", "No Emotion Runtime",
        "No Personality Switching", "No Relationship Judgment", "No Face Recognition", "No Social Action", "No Multi-Agent", "No Hive", "No B Route",
        "No Prediction", "No Action Runtime", "directly modify Identity", "directly modify Reality", "directly modify Goal", "directly modify Decision",
        "directly modify Action", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "role_schema_v1.json": [
        "Role Schema v1", "role_id", "field_context", "role_candidate", "Employee", "responsibility", "permission", "expectation",
        "behavior_boundary", "duration", "confidence", "evidence", "unknowns", "identity_reference", "identity_is_not_role",
        "role_belongs_to_field", "role_does_not_modify_identity", "unknowns_are_preserved"
    ],
    "role_activation_contract_v1.json": [
        "Role Activation Contract v1", "field_reference", "role_assignment_candidate", "Employee Candidate", "activation_source", "Field Context",
        "evidence", "confidence", "unknowns", "activation_state", "Created", "Active", "Background", "Suspended", "Closed",
        "activation_is_field_driven", "activation_does_not_modify_identity", "activation_does_not_make_decision",
        "activation_does_not_execute_social_action", "unknowns_are_preserved"
    ],
    "role_lifecycle_contract_v1.json": [
        "Role Lifecycle Contract v1", "states", "Created", "Active", "Background", "Suspended", "Closed", "role_reference", "field_context",
        "responsibility", "permission", "expectation", "behavior_boundary", "duration", "transition_requires_evidence",
        "transition_requires_confidence", "role_does_not_modify_identity", "role_does_not_make_decision", "unknowns_are_preserved"
    ],
    "role_conflict_candidate_schema_v1.json": [
        "Role Conflict Candidate Schema v1", "conflict_id", "role_candidates", "Employee Candidate", "Friend Candidate", "Parent Candidate",
        "field_context", "responsibility_conflict", "permission_conflict", "expectation_conflict", "evidence", "confidence", "unknowns",
        "conflict_is_candidate", "automatic_resolution", "does_not_modify_identity", "does_not_make_decision", "unknowns_are_preserved"
    ],
    "relationship_context_schema_v1.json": [
        "Relationship Context Schema v1", "relationship_id", "participant_a", "participant_b", "field_context", "state", "Initial",
        "Developing", "Stable", "Changed", "Unknown", "Archived", "history", "confidence", "evidence", "boundary", "timestamp",
        "unknowns", "relationship_is_contextual", "relationship_is_temporal", "relationship_does_not_make_decision", "unknowns_are_preserved"
    ],
    "relationship_evolution_contract_v1.json": [
        "Relationship Evolution Contract v1", "from_state", "to_state", "allowed_states", "Initial", "Developing", "Stable", "Changed",
        "Unknown", "Archived", "interaction_experience_reference", "relationship_memory_reference", "evidence", "confidence", "history",
        "unknowns", "relationship_candidate", "relationship_judgment", "emotion_inference", "does_not_make_decision", "unknowns_are_preserved"
    ],
    "relationship_memory_interface_v1.json": [
        "Relationship Memory Interface v1", "interaction_experience_reference", "relationship_memory_reference", "relationship_candidate",
        "field_context", "history", "confidence", "evidence", "unknowns", "memory_does_not_override_reality", "memory_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "role_attention_interface_v1.json": [
        "Role Attention Interface v1", "role_reference", "field_context", "responsibility", "expectation", "attention_candidate",
        "information_value", "risk_context", "unknowns", "role_provides_attention_candidate", "role_does_not_allocate_attention_directly",
        "role_does_not_modify_goal", "role_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "role_behavior_interface_v1.json": [
        "Role Behavior Interface v1", "role_reference", "field_context", "behavior_boundary", "expected_behavior", "behavior_candidate",
        "responsibility", "permission", "unknowns", "behavior_is_candidate", "role_does_not_execute_action", "role_does_not_make_decision",
        "role_does_not_modify_identity", "unknowns_are_preserved"
    ],
    "role_emotion_placeholder_v1.json": [
        "Role Emotion Placeholder v1", "role_reference", "relationship_reference", "field_reference", "memory_reference",
        "emotion_state_candidate", "placeholder_only", "emotion_runtime", "role_does_not_infer_emotion", "relationship_does_not_judge_emotion",
        "emotion_does_not_make_decision", "unknowns_are_preserved"
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
