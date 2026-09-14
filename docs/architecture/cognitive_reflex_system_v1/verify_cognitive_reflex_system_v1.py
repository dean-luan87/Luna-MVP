#!/usr/bin/env python3
"""V2 final verifier for Cognitive Reflex System architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_reflex_architecture_v1.md": [
        "Reflex System", "fast response mechanism", "Decision", "Shortcut Brain", "low-level", "Agent", "Response Candidate",
        "Attention Adjustment Candidate", "Condition", "Field Context", "Active Role", "Risk", "Safety Constraint", "Brain Escalation",
        "Innate Reflex", "Constitution", "fixed", "high priority", "does not learn", "hardware over-temperature", "user-protection",
        "extreme-low-battery", "not an automatic action", "Learned Reflex", "Learning System", "Experience", "Pattern Candidates",
        "validation", "Governance Admission", "revocation", "one episode", "permanent reflex", "Reflex Trigger", "Attention", "Workspace Update",
        "Personality Switching", "Reflex Escalation Interface", "Brain Review", "Goal", "final Decision authority", "Candidate → Review → Active",
        "Triggered → Feedback → Adjusted → Deprecated", "Automatic Action", "automatic Value change", "automatic Personality change",
        "Emotion Runtime", "B Runtime", "Prediction Runtime", "model training", "Safety Rules", "Identity"
    ],
    "reflex_whitebox_v1.md": [
        "Constitution → Innate Reflex Candidate", "Learning Experience → Pattern → Learned Reflex Candidate", "Field + Role + Risk + Safety Constraint",
        "Reflex Governance", "Attention Candidate", "Response Candidate", "Brain Escalation", "Who defines Innate Reflex", "no learning",
        "rule mutation", "Who proposes Learned Reflex", "Learning System", "Who validates admission", "Who binds a trigger", "Who receives attention changes",
        "Who owns complex judgment", "Who owns external-world mutation", "Action Boundary", "Who revokes an incorrect reflex", "Governance",
        "Reflex → Attention Adjustment Candidate", "Reflex → Brain Escalation", "Reflex → automatic Action", "Reflex → Safety Rule Mutation",
        "Reflex → Value Mutation", "Reflex → Identity Mutation", "Reflex → Goal Mutation", "Reflex → Decision", "Reflex → Model Training",
        "Reflex → Prediction Runtime", "Innate Reflex", "Learned Reflex", "context-bound", "revocable", "Action Runtime", "Planning Only"
    ],
    "reflex_go_no_go_v1.md": [
        "Fast Response Mechanism", "not Decision", "Shortcut Brain", "Innate Reflex", "Constitution-sourced", "fixed", "high priority",
        "learning-forbidden", "Learned Reflex", "Experience/Pattern-sourced", "validated", "admitted", "feedback-enabled", "revocable",
        "Reflex Trigger", "Condition", "Field Context", "Risk", "Active Role", "Safety Constraint", "Attention Adjustment Candidate",
        "Workspace Update", "Reflex Escalation Interface", "Brain Review", "Candidate", "Review", "Active", "Triggered", "Feedback", "Adjusted",
        "Deprecated", "No automatic Action", "No automatic safety-rule modification", "No automatic Value change", "No automatic Personality change",
        "No Emotion Runtime", "No B Runtime", "No Prediction Runtime", "No model training", "cannot modify Safety Rules", "Value", "Identity",
        "Goal", "Decision", "Action", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "reflex_system_schema_v1.json": [
        "Reflex System Schema v1", "reflex_id", "Innate Reflex", "condition", "field_context", "active_role", "risk", "safety_constraint",
        "response_candidate", "attention_adjustment_candidate", "brain_escalation_candidate", "candidate_only", "does_not_make_decision",
        "does_not_execute_action", "unknowns_are_preserved"
    ],
    "innate_reflex_contract_v1.json": [
        "Innate Reflex Contract v1", "Constitution", "Innate Reflex", "fixed", "high_priority", "Forbidden", "constitution_mutation",
        "hardware_over_temperature", "Protection Candidate", "user_danger", "extreme_low_battery", "Energy Reduction Candidate",
        "candidate_only", "automatic_action", "unknowns_are_preserved"
    ],
    "learned_reflex_contract_v1.json": [
        "Learned Reflex Contract v1", "Learning System", "Learned Reflex", "experience_reference", "pattern_reference", "validation_required",
        "governance_admission_required", "context_binding_required", "feedback_required", "revocable", "one_episode_cannot_create_permanent_reflex",
        "candidate_only", "automatic_action", "unknowns_are_preserved"
    ],
    "reflex_trigger_schema_v1.json": [
        "Reflex Trigger Schema v1", "trigger_id", "condition", "field_context", "risk", "active_role", "safety_constraint", "evidence",
        "confidence", "unknowns", "trigger_formula", "trigger_does_not_make_decision", "unknowns_are_preserved"
    ],
    "reflex_field_binding_v1.json": [
        "Reflex Field Binding v1", "field_reference", "field_context", "field_rule_reference", "condition", "risk", "field_binding_required",
        "same_signal_can_differ_by_field", "reflex_does_not_modify_field", "unknowns_are_preserved"
    ],
    "reflex_role_binding_v1.json": [
        "Reflex Role Binding v1", "role_reference", "active_role", "field_context", "responsibility", "permission_boundary", "safety_constraint",
        "role_changes_response_candidate", "role_does_not_modify_identity", "personality_switching", "unknowns_are_preserved"
    ],
    "reflex_attention_interface_v1.json": [
        "Reflex Attention Interface v1", "reflex_reference", "attention_adjustment_candidate", "attention_boost_candidate", "workspace_update_candidate",
        "field_context", "risk", "reflex_does_not_allocate_attention", "reflex_does_not_make_decision", "unknowns_are_preserved"
    ],
    "reflex_learning_interface_v1.json": [
        "Reflex Learning Interface v1", "experience_reference", "pattern_reference", "learned_reflex_candidate", "validation_candidate", "feedback",
        "revocation_candidate", "governance_admission_required", "learning_does_not_auto_activate_reflex", "unknowns_are_preserved"
    ],
    "reflex_brain_escalation_v1.json": [
        "Reflex Brain Escalation Interface v1", "reflex_candidate", "complexity", "uncertainty", "risk", "brain_review_required", "goal_authority",
        "Brain", "final_decision_authority", "response_candidate", "escalation_does_not_execute_action", "unknowns_are_preserved"
    ],
    "reflex_lifecycle_contract_v1.json": [
        "Reflex Lifecycle Contract v1", "Candidate", "Review", "Active", "Triggered", "Feedback", "Adjusted", "Deprecated", "Candidate → Review",
        "Review → Active", "Active → Triggered", "Triggered → Feedback", "Feedback → Adjusted", "Adjusted → Active", "Active → Deprecated",
        "governance_admission_required", "learned_reflex_revocable", "lifecycle_does_not_make_decision", "unknowns_are_preserved"
    ],
    "reflex_governance_contract_v1.json": [
        "Reflex Governance Contract v1", "Constitution", "Learning System", "admission_required", "safety_boundary_required", "field_binding_required",
        "role_binding_required_when_relevant", "validation_required", "feedback_required", "revocation_supported", "automatic_action",
        "automatic_safety_rule_modification", "automatic_value_change", "automatic_personality_change", "emotion_runtime", "b_runtime",
        "prediction_runtime", "model_training", "reflex_does_not_modify_identity", "reflex_does_not_modify_goal", "reflex_does_not_modify_decision",
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
