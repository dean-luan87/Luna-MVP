#!/usr/bin/env python3
"""V2 static verifier for Cognitive Situation Understanding architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_situation_model_v1.md": [
        "Situation Understanding", "Reality Evidence", "Reality State", "Cognitive Field State",
        "Self State", "Self Capability State", "Goal Context", "Attention Context", "Situation Candidate",
        "Environment Context", "Self Context", "Constraint Context", "Risk Context", "Unknown Context",
        "Reality is not Situation", "Situation is not Reality", "Evidence Support", "provenance",
        "Unknown", "not a Decision", "Action", "Prediction", "Personality", "Emotion", "cannot issue a Decision",
        "cannot issue an Action", "Reducer remains the sole State mutation authority", "Situation Reassessment Candidate"
    ],
    "situation_reality_boundary_v1.md": [
        "Fact and interpretation", "Reality Evidence", "Reality Representation", "Situation Candidate",
        "Decision Candidate", "facts", "hypotheses", "Risk", "Evidence Provenance", "Self Capability",
        "Self State", "Reality is not Situation", "Situation Candidate", "does not directly generate Decision",
        "Action", "Prediction", "Value Judgment", "Emotion Judgment", "Goal", "Unknown",
        "sole State mutation authority"
    ],
    "situation_update_loop_v1.md": [
        "New Evidence", "Reality Update Candidate", "Cognitive Field Update Candidate",
        "Situation Reassessment Candidate", "Situation Confidence", "A Route Input", "material change",
        "location", "entity", "relation", "Self State", "Capability State", "Goal Context", "Unknown",
        "stale Situation", "Reality Evidence has priority", "Experience Reference", "does not execute Action",
        "make Decision", "alter Goal", "mutate Reality directly"
    ],
    "situation_experience_boundary_v1.md": [
        "Experience Reference", "Situation Prior Candidate", "Current Reality Evidence", "Current Self",
        "Current Field", "Current Goal", "Situation Candidate", "cannot override Current Reality Evidence",
        "hypothesis", "Fact", "Reality > Experience", "Situation Reassessment Candidate", "not automatic learning",
        "online learning", "Unknown"
    ],
    "situation_whitebox_v1.md": [
        "Reality Evidence", "Reality State", "Field State", "Self State", "Capability State", "Goal Context",
        "Attention Context", "Situation Candidate", "Environment", "Self", "Risk", "Unknown",
        "Situation Confidence Candidate", "A Route Input", "New Evidence", "Reality Update Candidate",
        "Field Update Candidate", "Situation Reassessment Candidate", "Brain Awareness Input", "Reality Facts",
        "hypotheses", "Evidence Support", "no Decision", "Action", "Prediction", "private chain-of-thought",
        "Reducer remains the sole State mutation authority", "No real model", "No OCR", "No SLAM", "No Camera",
        "No Hardware Runtime", "No Emotion", "No Role", "No Social Runtime", "No B Runtime"
    ],
    "situation_go_no_go_v1.md": [
        "Situation Model", "Reality", "Cognitive Field", "Self State", "Self Capability", "Goal Context",
        "Attention Context", "Environment Context", "Self Context", "Constraint Context", "Risk Context",
        "Unknown Context", "Evidence Support", "provenance", "confidence", "same Reality", "different Self",
        "Situation Reassessment Candidates", "lower Situation Confidence", "cannot create Decision", "Action",
        "Goal", "Prediction", "Value Judgment", "Experience", "current Reality Evidence", "Brain",
        "re-observation", "Decision authority", "Reducer remains the sole State mutation authority", "No Decision",
        "No Action", "No Prediction", "No Emotion", "No Role", "No Social Runtime", "No B", "No automatic learning",
        "No online learning", "No real model", "No OCR", "No SLAM", "No Camera", "No Hardware Runtime",
        "No Runtime execution", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "situation_context_schema_v1.json": [
        "Situation Context Schema", "environment_context", "self_context", "goal_context", "constraint_context",
        "risk_context", "unknown_context", "evidence_support", "confidence", "provenance",
        "situation_candidate", "reassessment_candidate", "reality_is_not_situation", "situation_is_not_reality",
        "situation_is_not_decision", "situation_is_not_action", "situation_is_not_prediction", "does_not_modify_reality",
        "does_not_modify_goal", "does_not_modify_decision", "does_not_issue_action", "unknown_must_be_preserved",
        "reducer_is_sole_state_mutation_authority"
    ],
    "situation_confidence_contract_v1.json": [
        "Situation Confidence", "evidence_support", "provenance", "uncertainty", "unknowns", "self_context",
        "field_context", "goal_context", "validity", "situation_confidence_is_not_fact",
        "situation_confidence_is_not_reality", "hypothesis_is_not_fact", "unknown_reduces_confidence",
        "evidence_support_required", "provenance_required", "confidence_cannot_create_decision",
        "confidence_cannot_create_action", "confidence_cannot_modify_reality", "confidence_cannot_modify_goal",
        "confidence_cannot_modify_identity"
    ],
    "situation_attention_interface_v1.json": [
        "Situation Attention Interface", "situation_candidate", "unknown_context", "risk_context", "confidence",
        "field_context", "goal_context", "attention_relevance_candidate", "observation_requirement_candidate",
        "uncertainty_reduction_candidate", "reassessment_attention_candidate", "unknown_increase", "risk_candidate",
        "stable_situation", "confidence_decline", "situation_does_not_modify_attention_directly",
        "attention_does_not_modify_situation_directly", "attention_does_not_select_goal",
        "attention_does_not_select_decision", "candidate_only", "unknown_is_preserved"
    ],
    "situation_brain_interface_v1.json": [
        "Situation Brain Interface", "situation_candidate", "environment_context", "self_context", "goal_context",
        "constraint_context", "risk_context", "unknown_context", "confidence", "evidence_support", "provenance",
        "may_request_reobservation", "may_evaluate_situation", "retains_goal_authority", "retains_decision_authority",
        "retains_value_authority", "brain_does_not_receive_raw_world_by_default", "situation_does_not_command_brain",
        "situation_does_not_create_goal", "situation_does_not_create_decision", "situation_does_not_issue_action",
        "brain_can_request_reobservation"
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
