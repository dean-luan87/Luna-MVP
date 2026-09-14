#!/usr/bin/env python3
"""V2 final verifier for Cognitive Drive and Value Core contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_drive_and_value_core_model_v1.md": [
        "Drive and Value", "internal motivational", "evaluative context", "not Emotion", "not Goal", "not Decision", "not Action",
        "Survival Constitution", "highest safety constraint", "Value Constitution", "Cognitive Drive", "Attention", "Situation",
        "Option Evaluation", "Brain Judgment", "Survival Drive", "Task Drive", "Self Continuity Drive", "Exploration Drive", "Social Drive",
        "Value Constitution", "Survival Value", "Self Integrity Value", "User Goal Value", "Social Value", "Learning Value",
        "Value Weight Candidate", "Tradeoff Candidate", "Goal/Task", "Outcome", "Drive State Candidate", "low battery", "priority candidate",
        "Drive Conflict Candidate", "Value Conflict Candidate", "Attention Candidate", "Option Evaluation Candidate", "Learning Candidate",
        "Reflex Candidate", "No Emotion Runtime", "automatic learning", "Model Training", "B Route", "Prediction", "Action Runtime",
        "Social Decision", "Personality Switching", "Value Manager"
    ],
    "value_conflict_model_v1.md": [
        "Value Conflict Candidate", "Survival Value", "Self Integrity Value", "User Goal Value", "Social Value", "Learning Value",
        "context", "constraints", "confidence", "Unknown", "provenance", "Tradeoff Candidate", "does not produce a Decision",
        "Option Evaluation", "Brain Review", "Survival Constitution", "hard constraints", "fast route", "safe route", "choose the safe route"
    ],
    "drive_state_lifecycle_model_v1.md": [
        "Drive State", "Reality", "Self State", "Field", "Goal/Task", "Outcome", "Resource State", "intensity candidate", "trigger evidence",
        "scope", "duration", "confidence", "Unknown", "provenance", "Detected", "Elevated", "Sustained", "Decaying", "Released",
        "Archived Candidate", "Attention Reallocation Candidate", "Brain Escalation Candidate", "Reflex", "modify Goal", "make Decision",
        "Emotion", "low-battery Survival Drive", "not fear"
    ],
    "drive_value_whitebox_v1.md": [
        "Reality", "Self State", "Field", "Goal", "Outcome", "Drive State Candidate", "Value Weight Candidate", "Attention",
        "Option Evaluation", "Learning", "Reflex", "Brain Review", "hard safety limits", "Survival Constitution", "Governance",
        "Value Constitution", "Value Manager", "Evidence-backed", "Drive/Value conflict", "Brain Review", "Goal and final Decision",
        "Social Action", "Action Runtime", "Drive → Attention Candidate", "Value → Option Evaluation Candidate", "Drive → Emotion",
        "Drive → Goal", "Drive → Decision", "Drive → Action", "Value → Reality Mutation", "Value → Identity Mutation", "Value → Model Training",
        "Planning Only", "No Emotion Runtime", "automatic learning", "Model Training", "B Route", "Prediction", "Action Runtime",
        "Social Decision", "Personality Switching", "Value Manager"
    ],
    "drive_value_go_no_go_v1.md": [
        "Survival Drive", "Task Drive", "Self Continuity Drive", "Exploration Drive", "Social Drive", "Survival Value", "Self Integrity Value",
        "User Goal Value", "Social Value", "Learning Value", "Survival Constitution", "highest safety constraint", "priority", "salience",
        "weight", "trade-off", "Brain retains Goal", "final Decision authority", "Detected", "Elevated", "Sustained", "Decaying", "Released",
        "Archived Candidate", "Drive Conflict Candidate", "Value Conflict Candidate", "Unknown", "provenance", "Attention", "Option Evaluation",
        "Learning", "Reflex", "No Emotion Runtime", "No automatic learning", "No Model Training", "No B Route", "No Prediction",
        "No Action Runtime", "No Social Decision", "No Personality Switching", "No Value Manager", "directly modify Reality", "Identity", "Goal",
        "Decision", "Action", "Model parameters", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "drive_schema_v1.json": [
        "Cognitive Drive Schema v1", "drive_id", "drive_type", "Survival", "Task", "Self Continuity", "Exploration", "Social",
        "source_reality", "self_state_reference", "field_reference", "goal_reference", "outcome_reference", "intensity_candidate",
        "trigger_evidence", "scope", "duration", "confidence", "unknowns", "provenance", "lifecycle_state", "Detected", "Elevated",
        "Sustained", "Decaying", "Released", "Archived Candidate", "drive_is_not_emotion", "drive_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "value_constitution_v1.json": [
        "Value Constitution v1", "constitution_reference", "survival_value", "self_integrity_value", "user_goal_value", "social_value",
        "learning_value", "rank", "hard_constraint", "survival_constitution_precedence", "value_weight_candidate", "tradeoff_candidate",
        "value_is_not_decision_authority", "value_is_not_goal_authority", "value_does_not_override_safety", "unknowns_are_preserved"
    ],
    "drive_value_interaction_contract_v1.json": [
        "Drive Value Interaction Contract v1", "drive_reference", "value_constitution_reference", "reality_reference", "field_reference",
        "self_state_reference", "goal_reference", "outcome_reference", "drive_state_candidate", "value_weight_candidate", "priority_candidate",
        "tradeoff_candidate", "drive_conflict_candidate", "value_conflict_candidate", "survival_constitution_precedence", "brain_review_required",
        "drive_does_not_make_decision", "value_does_not_make_decision", "unknowns_are_preserved"
    ],
    "drive_attention_interface_v1.json": [
        "Drive Attention Interface v1", "drive_reference", "field_reference", "attention_candidate", "priority_candidate", "salience_candidate",
        "resource_cost", "risk_context", "information_value", "attention_reallocation_candidate", "drive_provides_attention_candidate",
        "drive_does_not_allocate_attention_directly", "drive_does_not_modify_goal", "drive_does_not_modify_decision", "unknowns_are_preserved"
    ],
    "drive_brain_interface_v1.json": [
        "Drive Brain Interface v1", "drive_state_candidate", "value_weight_candidate", "drive_conflict_candidate", "value_conflict_candidate",
        "tradeoff_candidate", "goal_reference", "decision_candidate_reference", "brain_review_required", "brain_retains_goal_authority",
        "brain_retains_final_decision_authority", "drive_does_not_make_decision", "value_does_not_make_decision", "unknowns_are_preserved"
    ],
    "drive_learning_interface_v1.json": [
        "Drive Learning Interface v1", "drive_reference", "experience_reference", "pattern_candidate", "strategy_candidate",
        "feedback_reference", "drive_adjustment_candidate", "validation_required", "candidate_only", "automatic_learning", "model_training",
        "drive_does_not_modify_model_parameters", "drive_does_not_modify_goal", "unknowns_are_preserved"
    ],
    "drive_reflex_interface_v1.json": [
        "Drive Reflex Interface v1", "drive_reference", "reflex_candidate", "Innate Reflex Placeholder", "Learned Reflex Placeholder",
        "safety_context", "experience_reference", "governance_reference", "candidate_only", "reflex_does_not_execute_action",
        "reflex_does_not_make_decision", "reflex_does_not_modify_goal", "unknowns_are_preserved"
    ],
    "value_conflict_contract_v1.json": [
        "Value Conflict Contract v1", "Survival Value", "Self Integrity Value", "User Goal Value", "Social Value", "Learning Value",
        "Survival Drive", "Task Drive", "Self Continuity Drive", "Exploration Drive", "Social Drive", "tradeoff_candidate", "constraints",
        "unknowns", "provenance", "survival_constitution_is_highest", "conflict_is_not_decision", "automatic_resolution", "brain_review_required",
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
