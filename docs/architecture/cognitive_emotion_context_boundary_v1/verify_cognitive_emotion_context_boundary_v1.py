#!/usr/bin/env python3
"""V2 final verifier for Emotion Context Boundary contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_emotion_context_boundary_v1.md": [
        "Emotion Context Boundary", "Emotion Context Interface", "previously verified Emotion Engine", "future reference", "does not activate",
        "Field", "Role", "Relationship", "Memory", "Emotion Context Candidate", "Future Emotion Engine", "metadata", "not emotion classification",
        "not emotion inference", "not emotion generation", "expression", "relationship calculation", "decision signal", "Attention", "Drive",
        "Memory Retrieval", "Field Emotion Attachment Candidate", "Role Emotion Context Candidate", "Relationship Emotion Context Candidate",
        "Memory Emotion Metadata Placeholder", "Provenance", "Confidence", "Unknown", "revocability", "Facts remain in Reality", "Relationship Judgment",
        "Attention Interface", "Drive Interface", "Memory Interface", "Brain Interface", "Goal", "Value", "final Decision authority",
        "No emotion classification", "No emotion reasoning", "No emotion generation", "No personality change", "No relationship calculation",
        "No emotion expression", "No emotion decision", "No Emotion Runtime", "No B Simulation", "No Action Runtime", "does not compute"
    ],
    "emotion_context_whitebox_v1.md": [
        "Field + Role + Relationship + Memory Metadata", "Emotion Context Candidate", "Attention", "Drive", "Memory", "Brain Interfaces",
        "Future Emotion Engine only", "Who creates a Field Emotion Attachment Candidate", "Field history interface", "Who creates a Role Emotion Context Candidate",
        "Role context interface", "Who creates a Relationship Emotion Context Candidate", "Relationship context interface", "Who stores Emotion Metadata",
        "Memory metadata interface", "separate from facts", "Who owns factual truth", "Reality Workspace", "Who owns Goal, Value, and final Decision",
        "Who may later compute emotion", "separately authorized Future Emotion Engine", "Emotion Context → classification", "Emotion Context → reasoning",
        "Emotion Context → generation", "Emotion Context → expression", "Emotion Context → relationship calculation", "Emotion Context → Decision",
        "Emotion Context → Goal mutation", "Emotion Context → Value mutation", "Emotion Context → Identity mutation", "Emotion Context → Action",
        "Emotion Context → B Simulation", "Planning Only", "Emotion Engine Runtime"
    ],
    "emotion_context_go_no_go_v1.md": [
        "Emotion Context Interface", "not Emotion Engine", "Emotion Context Candidate", "Field", "Role", "Relationship", "Memory metadata",
        "evidence", "provenance", "confidence", "unknowns", "time", "revocability", "Fact", "Experience", "Emotion Metadata", "Relationship Judgment",
        "Attention", "Drive", "Memory Retrieval", "Brain", "Goal", "Value", "final Decision authority", "Future Emotion Engine",
        "No emotion classification", "No emotion reasoning", "No emotion generation", "No personality change", "No relationship calculation",
        "No emotion expression", "No emotion decision", "No Emotion Runtime", "No B Simulation", "No Action Runtime", "cannot modify Reality",
        "Decision", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "emotion_context_schema_v1.json": [
        "Emotion Context Schema v1", "context_candidate_id", "field_reference", "role_reference", "relationship_reference", "memory_metadata_reference",
        "time_scope", "evidence", "provenance", "confidence", "unknowns", "revocable", "placeholder_only", "does_not_compute_emotion",
        "unknowns_are_preserved"
    ],
    "field_emotion_attachment_placeholder_v1.json": [
        "Field Emotion Attachment Placeholder v1", "field_reference", "field_history", "emotion_context_candidate", "evidence", "provenance",
        "confidence", "unknowns", "field_emotion_attachment_candidate", "does_not_calculate_emotion", "does_not_make_relationship_judgment",
        "unknowns_are_preserved"
    ],
    "role_emotion_context_placeholder_v1.json": [
        "Role Emotion Context Placeholder v1", "role_reference", "active_role", "field_context", "responsibility_context", "emotion_context_candidate",
        "evidence", "confidence", "unknowns", "role_emotion_context_candidate", "does_not_modify_identity", "does_not_compute_emotion",
        "unknowns_are_preserved"
    ],
    "relationship_emotion_context_placeholder_v1.json": [
        "Relationship Emotion Context Placeholder v1", "participant_a", "participant_b", "relationship_reference", "relationship_context", "time",
        "boundary", "emotion_context_candidate", "relationship_emotion_context_candidate", "relationship_calculation", "relationship_judgment",
        "unknowns_are_preserved"
    ],
    "memory_emotion_metadata_placeholder_v1.json": [
        "Memory Emotion Metadata Placeholder v1", "event_fact_reference", "experience_reference", "emotion_metadata", "field_reference", "role_reference",
        "relationship_reference", "provenance", "unknowns", "metadata_is_separate_from_fact", "memory_is_not_rewritten", "does_not_compute_emotion",
        "unknowns_are_preserved"
    ],
    "emotion_interface_contract_v1.json": [
        "Emotion Context Interface Contract v1", "emotion_context_candidate", "Future Emotion Engine", "Placeholder Only", "Context Reference Only",
        "no_emotion_calculation", "no_emotion_inference", "no_emotion_generation", "no_emotion_expression", "no_emotion_decision",
        "unknowns_are_preserved"
    ],
    "emotion_brain_attention_drive_boundary_v1.json": [
        "Emotion Brain Attention Drive Boundary v1", "emotion_context_candidate", "attention_influence_candidate", "drive_modulation_candidate",
        "memory_retrieval_candidate", "brain_context_reference", "attention_allocation", "drive_ownership", "brain_goal_authority",
        "brain_value_authority", "brain_final_decision_authority", "candidate_only", "unknowns_are_preserved"
    ],
    "emotion_context_future_engine_placeholder_v1.json": [
        "Future Emotion Engine Placeholder v1", "Emotion Context Boundary", "Future Emotion Engine", "Not Authorized", "future_computation",
        "future_personality_growth", "future_emotional_regulation", "future_expression_strategy", "future_relationship_model",
        "requires_new_phase_authorization", "placeholder_only", "unknowns_are_preserved"
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
