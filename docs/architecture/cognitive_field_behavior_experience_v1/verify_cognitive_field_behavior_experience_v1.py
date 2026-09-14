#!/usr/bin/env python3
"""V2 static verifier for Field Behavior and Experience architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_field_behavior_model_v1.md": [
        "Field Behavior", "not an Action", "not a Decision", "not a Goal", "not a Personality", "not a Role",
        "not an Emotion Runtime", "Field Rules", "Self Capability", "Self State", "Experience", "Preference",
        "Behavior Candidate", "Behavior Pattern", "Personal Preference Candidate", "Historical Action Pattern Candidate",
        "Constraint", "Adaptation Candidate", "Reality", "Experience", "historical action", "Preference is not a Goal",
        "Attention Bias Candidate", "Task + Field + Goal", "Emotion Attachment Candidate", "Role Binding Placeholder",
        "Emotion Runtime", "Role System", "Social Relationship", "Personality Switching", "B Route", "Prediction",
        "Action Execution"
    ],
    "historical_action_pattern_model_v1.md": [
        "Historical Action", "Experience-derived", "Pattern Candidate", "not a rule", "not a preference", "Goal",
        "Decision", "Action command", "Outcome / Experience", "Current Field Validation", "Behavior Candidate",
        "mall", "inspect a map", "locate the target store", "pause", "frequency", "confidence", "context",
        "Self State", "Rule references", "outcome quality", "time decay", "Unknowns", "Reality", "Temporary Rule",
        "Revalidation Candidate", "No automatic learning", "automatic planning", "prediction", "Action execution",
        "Emotion Runtime", "Role System", "Social Relationship", "B Route", "personality switching"
    ],
    "behavior_experience_boundary_v1.md": [
        "Experience", "Historical Action Pattern Candidate", "Personal Preference Candidate", "Field Association Candidate",
        "Adaptation Candidate", "Behavior", "Rule", "Goal", "Decision", "Action", "Emotion", "Role", "Personality",
        "Outcome", "Current Reality", "Field Rule Validation", "Reality is higher priority", "One successful", "One failed",
        "provenance", "confidence", "context binding", "time decay", "Emotion Attachment Candidate", "Emotion Engine",
        "Role Binding Placeholder", "Role System", "Social Relationship runtime"
    ],
    "field_behavior_whitebox_v1.md": [
        "Field Rule / Dynamic", "Self", "Goal / Task", "Experience / Preference", "Behavior Pattern Candidate",
        "Current Field Reality Validation", "Behavior Candidate", "Attention Bias Candidate", "A Route Review",
        "Decision Candidate", "Action Boundary", "Behavior is a tendency", "Historical Action Pattern", "Experience-derived",
        "Preference is context-bound", "Emotion", "Personality", "Role", "Reality > Experience", "current Rule",
        "Evidence", "Task and Field constrain", "Emotion Attachment Candidate", "Role Binding Placeholder",
        "Reducer remains the sole State mutation authority", "No Emotion Runtime", "No Role System", "No Social Relationship",
        "No Personality Switching", "No B", "No Prediction", "No Action Execution", "No automatic planning"
    ],
    "field_behavior_go_no_go_v1.md": [
        "Field Behavior", "Action", "Decision", "Goal", "Personality", "Role", "Emotion", "Behavior Candidate",
        "Field", "Self", "Experience", "Rule", "Dynamic", "Capability", "Unknown", "Historical Action Pattern",
        "current Field validation", "Personal Preference", "context-bound", "Reality > Experience", "Attention Bias Candidate",
        "Task", "Field", "Task identity", "Emotion Attachment Candidate", "Role Binding Placeholder", "schema-only",
        "provenance", "confidence", "time decay", "A Route", "No Emotion Runtime", "No Role System", "No Social Relationship",
        "No Personality Switching", "No B", "No Prediction", "No Action Execution", "No automatic planning", "No automatic learning",
        "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "field_behavior_schema_v1.json": [
        "Field Behavior Schema v1", "behavior_id", "field_reference", "behavior_pattern_candidate",
        "personal_preference_candidate", "historical_action_pattern_candidate", "goal_reference", "task_reference",
        "constraints", "self_capability_reference", "self_state_reference", "rule_references", "experience_references",
        "adaptation_candidate", "confidence", "provenance", "unknowns", "behavior_is_not_action", "behavior_is_not_decision",
        "behavior_is_not_goal", "behavior_does_not_execute", "reality_over_experience", "unknowns_are_preserved"
    ],
    "field_preference_contract_v1.json": [
        "Field Preference Contract v1", "preference_id", "field_reference", "preference_candidate", "condition",
        "supporting_experience", "supporting_reality", "confidence", "provenance", "validity", "unknowns",
        "preference_is_not_emotion", "preference_is_not_personality", "preference_is_not_role", "preference_is_not_goal",
        "preference_is_not_decision", "preference_is_not_action", "current_reality_validation_required",
        "attention_bias_candidate_only", "unknowns_are_preserved"
    ],
    "behavior_candidate_generation_contract_v1.json": [
        "Behavior Candidate Generation Contract v1", "field_reference", "self_reference", "goal_reference", "task_reference",
        "rule_context", "dynamic_context", "experience_context", "preference_context", "capability_context", "unknowns",
        "behavior_candidate", "pattern", "constraints", "confidence", "adaptation_candidate", "reality_validation_required",
        "behavior_is_not_action", "behavior_is_not_decision", "behavior_is_not_goal", "behavior_does_not_execute",
        "a_route_review_required", "unknowns_are_preserved"
    ],
    "behavior_attention_interface_v1.json": [
        "Behavior Attention Interface v1", "behavior_reference", "field_reference", "preference_reference",
        "attention_bias_candidate", "information_value", "resource_cost", "risk_context", "persistence", "release_candidate",
        "attention_does_not_modify_behavior", "behavior_does_not_modify_attention_directly", "attention_does_not_modify_goal",
        "attention_does_not_modify_decision", "attention_does_not_execute_action", "candidate_only", "unknowns_are_preserved"
    ],
    "behavior_task_interface_v1.json": [
        "Behavior Task Interface v1", "behavior_reference", "task_reference", "field_reference", "goal_reference",
        "task_state", "Active", "Background", "Suspended", "Resumed", "task_constraint_candidates", "behavior_constraint_candidate",
        "task_does_not_execute_behavior", "behavior_does_not_modify_task_identity", "behavior_does_not_modify_goal",
        "behavior_does_not_modify_decision", "field_binding_required", "a_route_review_required", "unknowns_are_preserved"
    ],
    "behavior_emotion_placeholder_v1.json": [
        "Behavior Emotion Placeholder v1", "schema_only", "field_reference", "experience_reference", "emotion_attachment_candidate",
        "behavior_preference_candidate", "runtime_enabled", "does_not_modify_reality", "does_not_modify_goal",
        "does_not_modify_decision", "does_not_execute_action", "no_emotion_runtime", "no_personality_switching",
        "unknowns_are_preserved"
    ],
    "behavior_role_placeholder_v1.json": [
        "Behavior Role Placeholder v1", "schema_only", "field_reference", "role_binding_placeholder", "behavior_context_candidate",
        "runtime_enabled", "does_not_modify_identity", "does_not_modify_goal", "does_not_modify_decision",
        "does_not_execute_action", "no_role_system", "no_social_relationship_runtime", "no_personality_switching",
        "unknowns_are_preserved"
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
