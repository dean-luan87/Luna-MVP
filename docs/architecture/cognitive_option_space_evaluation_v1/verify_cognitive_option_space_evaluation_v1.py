#!/usr/bin/env python3
"""V2 static verifier for Cognitive Option Space and Evaluation architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_option_space_model_v1.md": [
        "Option Space", "Situation", "Self Capability", "Self State", "Goal", "Constraint", "Unknown",
        "Option Candidate Space", "Evaluation Candidate", "Decision Candidate Package", "Brain Evaluation",
        "candidate space, not an answer", "recommendation", "Decision", "Action", "execution plan", "Prediction",
        "Expected Benefit Candidate", "Resource Cost", "Risk Candidate", "Capability Requirement", "Dependency",
        "Option Evaluation", "Survival Impact", "Goal Alignment", "Capability Fit", "Uncertainty",
        "Experience Reference", "Provider cannot", "No Action", "No Execution Runtime", "No automatic execution"
    ],
    "option_generation_boundary_v1.md": [
        "Option Candidate", "A Route", "Brain Request", "Capability Feedback", "Situation", "Self Capability",
        "Self State", "Goal Context", "Rules", "Survival constraints", "Experience Reference", "Unknown Context",
        "Option Generation Candidate Set", "Provider is not", "Provider cannot generate behavior", "Capability cannot decide",
        "Decision", "Action", "Prediction", "Value Judgment", "No automatic execution", "sole State mutation authority"
    ],
    "option_constraint_model_v1.md": [
        "Option dimensions", "Expected Benefit Candidate", "Resource Cost", "Risk Candidate", "Capability Requirement",
        "Unknown", "Dependency", "Self Capability", "Self State", "Resource State", "Goal Context",
        "authority boundaries", "Field Context", "Constraint Fit", "final value judgment", "Option Confidence",
        "does not execute", "modify Reality", "modify Goal", "modify Decision", "issue Action", "Brain retains final"
    ],
    "option_unknown_management_v1.md": [
        "Unknown", "Situation", "Option Candidate", "Unknown road closure extent", "Unknown water depth",
        "Unknown resource duration", "Unknown Capability availability", "Option Confidence Adjustment Candidate",
        "Information Request", "Waiting", "Alternative Option Candidate", "fact", "assumption", "certainty",
        "automatic prohibition", "Option Evaluation", "New Evidence", "regenerate", "Decision", "Action", "Prediction"
    ],
    "option_experience_boundary_v1.md": [
        "Experience Reference", "Option Prior Candidate", "Current Situation", "Current Reality", "Current Self Capability",
        "Current Self State", "Option Candidate Space", "not a recommendation", "Decision", "Action",
        "automatic strategy override", "Current Reality > Experience", "New Evidence", "regenerate options",
        "automatic learning", "online learning", "Goal mutation", "Decision mutation", "Action execution"
    ],
    "option_whitebox_v1.md": [
        "Situation Candidate", "Self Capability", "Self State", "Goal", "Constraint", "Unknown", "Option Candidate Space",
        "Expected Benefit", "Cost", "Risk", "Capability", "Option Evaluation Candidate", "Decision Candidate Package",
        "Brain Evaluation", "Option List", "Tradeoff", "Experience Reference", "private chain-of-thought",
        "Provider cannot create an Option", "Decision", "Action", "feasibility candidates", "Reducer remains the sole State mutation authority",
        "No Action", "No Execution Runtime", "No automatic execution", "No Provider Decision", "No Emotion Runtime",
        "No Role Runtime", "No Social Runtime", "No B Runtime", "No Prediction"
    ],
    "option_go_no_go_v1.md": [
        "Option Candidate Space", "Self Capability", "Self State", "Goal", "Constraint", "Unknown", "Recommendation",
        "Decision", "Action", "Execution Plan", "Prediction", "Expected Benefit Candidate", "Resource Cost",
        "Risk Candidate", "Capability Requirement", "Dependency", "Self Capability Filter", "Capability Fit",
        "Feasibility Candidates", "Option Confidence", "Survival Impact", "Goal Alignment", "Uncertainty",
        "Experience Reference", "Brain", "Option List", "final Decision authority", "Provider cannot",
        "Current Reality", "Reducer remains the sole State mutation authority", "No Action", "No Execution Runtime",
        "No automatic execution", "No Provider Decision", "No Emotion", "No Role", "No Social Runtime", "No B",
        "No Prediction", "No automatic learning", "No online learning", "No real model", "No OCR", "No SLAM",
        "No Camera", "No Hardware Runtime", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "option_candidate_schema_v1.json": [
        "Option Candidate Schema", "option_id", "description", "situation_reference", "expected_benefit_candidate",
        "resource_cost", "risk_candidate", "capability_requirement", "unknowns", "dependencies", "provenance",
        "confidence", "constraint_status", "experience_reference", "option_is_not_decision", "option_is_not_action",
        "option_is_not_execution", "option_is_not_prediction", "provider_cannot_select_option", "option_cannot_modify_reality",
        "option_cannot_modify_goal", "option_cannot_execute", "unknowns_are_preserved", "brain_retains_decision_authority"
    ],
    "option_self_capability_interface_v1.json": [
        "Option Self Capability Interface", "self_capability_state", "self_state", "capability_requirements",
        "resource_constraints", "limitations", "capability_fit_candidate", "feasibility_candidate",
        "capability_gap_candidate", "alternative_option_candidate", "option_confidence_adjustment_candidate",
        "child_crossing", "adult_crossing", "degraded_capability", "self_capability_does_not_select_option",
        "self_capability_does_not_select_decision", "self_capability_does_not_modify_goal", "capability_fit_is_candidate_only",
        "unknown_is_preserved"
    ],
    "option_evaluation_contract_v1.json": [
        "Option Evaluation Contract", "Option Evaluation Candidate", "survival_impact", "goal_alignment",
        "capability_fit", "resource_cost", "risk", "uncertainty", "experience_reference", "confidence", "unknowns",
        "constraint_fit", "evaluation_is_candidate_only", "evaluation_is_not_final_value_judgment", "evaluation_is_not_decision",
        "evaluation_is_not_action", "evaluation_is_not_prediction", "unknowns_remain_visible", "risk_must_be_visible",
        "resource_cost_must_be_visible", "capability_fit_must_be_visible", "brain_retains_final_evaluation",
        "provider_cannot_evaluate_value", "experience_cannot_override_reality"
    ],
    "option_brain_interface_v1.json": [
        "Option Brain Interface", "Decision Candidate Package", "situation_reference", "option_list", "tradeoff", "risk",
        "unknown", "confidence", "constraint", "provenance", "accept_candidate", "modify_candidate", "reject_candidate",
        "request_more_information", "retains_goal_authority", "retains_decision_authority", "option_layer_does_not_command_brain",
        "option_layer_does_not_create_goal", "option_layer_does_not_create_decision", "option_layer_does_not_issue_action",
        "brain_evaluation_is_final_boundary", "no_direct_execution"
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
