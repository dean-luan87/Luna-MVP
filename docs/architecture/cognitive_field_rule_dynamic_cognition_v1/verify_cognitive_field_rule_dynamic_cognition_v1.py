#!/usr/bin/env python3
"""V2 static verifier for Field Rule and Dynamic Cognition architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_field_rule_layer_model_v1.md": [
        "Cognitive Field", "Physical Layer", "Entity Layer", "Spatial Layer", "Rule Layer", "Dynamic Layer",
        "Physical Rule", "Functional Rule", "Social Rule", "Legal Rule", "Temporary Rule", "Reality",
        "Rule Candidate", "Evidence", "confidence", "provenance", "validity", "Unknowns", "not Facts",
        "Density", "Direction", "Flow Pattern", "entry", "exit", "queue", "gathering", "evacuation",
        "Attention Bias Candidate", "Capability Requirement Candidate", "Field + Task", "Model never decides",
        "No Role", "No Emotion", "No Social Relationship", "No B Route", "No Prediction", "No automatic planning",
        "No Action Runtime", "No OCR Runtime", "No SLAM Runtime", "No Camera", "No Hardware", "automatic execution"
    ],
    "field_dynamic_behavior_model_v1.md": [
        "Dynamic Layer", "Density", "Direction", "Flow Pattern", "sparse", "normal", "dense", "unknown", "entering",
        "leaving", "crossing", "stationary", "queue", "gathering", "dispersal", "evacuation", "circulation", "Change",
        "Evidence Frames", "Entity / Flow Assembly", "Dynamic Candidate", "Rule Candidate", "Field Update Candidate",
        "Attention", "Capability Requirement Candidate", "group/environment patterns", "person identification", "motive",
        "emotion", "Role", "Social Relationship", "Unknown is high", "Information Source Candidate", "low-risk route",
        "acquire more Evidence", "No prediction", "No automatic planning", "No Action Runtime", "No real model"
    ],
    "crowd_following_strategy_v1.md": [
        "Crowd Following", "low-information", "risk-reduction strategy", "not blind following", "not a Decision",
        "not a Goal", "not a prediction", "not an Action", "Unknown High", "Information Source Candidate",
        "Crowd Density", "Direction", "Flow Pattern", "Low Risk Path Candidate", "Acquire More Evidence",
        "alternative sources", "flow uncertainty", "rule confidence", "Capability limits", "OCR", "spatial Evidence",
        "human confirmation", "does not directly follow", "does not execute", "No automatic planning", "No Prediction",
        "No Action Runtime", "No Role", "No Emotion", "No Social Relationship", "No B"
    ],
    "information_seeking_behavior_model_v1.md": [
        "Field Understanding Confidence", "Information Source Candidate", "service desk", "staffed information point",
        "signs", "maps", "exit markers", "verified user input", "visible entrance/exit structure", "stable crowd-flow boundary",
        "Capability source", "expected information value", "access uncertainty", "resource cost", "risk", "provenance",
        "expiry", "Evidence Gateway", "Reducer", "Attention Priority Candidate", "Capability Requirement Candidate",
        "Field + Task + Unknown", "Provider cannot choose", "Brain", "No automatic planning", "No Prediction", "No Action",
        "No Role", "No Emotion", "No Social Relationship", "No B Route", "Runtime execution"
    ],
    "field_rule_whitebox_v1.md": [
        "Reality Evidence", "Physical / Entity / Spatial Field", "Rule Candidate", "Confidence", "Unknown", "Dynamic Density",
        "Dynamic Direction", "Dynamic Flow Pattern", "Field Understanding Candidate", "Attention Bias Candidate",
        "Capability Requirement Candidate", "Situation Enhancement", "people are queued", "queue norm may apply",
        "Physical", "Functional", "Social", "Legal", "Temporary", "Human Flow", "Crowd Following", "Unknown High",
        "Information Source Candidate", "Field + Task + Unknown", "Model does not", "Reducer remains the sole State mutation authority",
        "No Prediction", "No automatic planning", "No Action Runtime", "No real model", "No OCR", "No SLAM", "No Camera",
        "No Hardware", "No Social Relationship", "No Role", "No Emotion", "No B Runtime"
    ],
    "field_rule_go_no_go_v1.md": [
        "Physical", "Entity", "Spatial", "Rule", "Dynamic", "Physical Rule", "Functional Rule", "Social Rule",
        "Legal Rule", "Temporary Rule", "Rule Candidate", "Reality Fact", "Evidence", "Confidence", "Provenance", "Validity",
        "Scope", "Unknown", "Human Flow", "Density", "Direction", "Flow Pattern", "entry", "exit", "queue", "gathering",
        "dispersal", "evacuation", "Crowd Following Strategy", "risk-reduction", "blind following", "Prediction", "Decision",
        "Action", "Information Source Candidate", "service desks", "signs", "maps", "people", "Capability Requirement Candidate",
        "Model", "Provider", "Attention", "No Role", "No Emotion", "No Social Relationship", "No B Route", "No Prediction",
        "No automatic planning", "No Action Runtime", "No real model", "No OCR", "No SLAM", "No Camera", "No Hardware",
        "No automatic execution", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "field_rule_schema_v1.json": [
        "Field Rule Schema v1", "rule_id", "field_reference", "rule_type", "Physical", "Functional", "Social", "Legal",
        "Temporary", "statement_candidate", "supporting_evidence", "confidence", "provenance", "validity_interval", "scope",
        "unknowns", "observed_reality_reference", "rule_is_not_fact", "rule_is_not_situation", "rule_is_not_decision",
        "rule_does_not_modify_reality", "rule_does_not_modify_goal", "rule_does_not_execute_action", "unknowns_are_preserved"
    ],
    "field_rule_confidence_contract_v1.json": [
        "Field Rule Confidence Contract v1", "rule_reference", "evidence_references", "confidence", "provenance", "validity",
        "scope", "unknowns", "reality_reference", "rule_candidate_status", "Observed Candidate", "Supported Candidate",
        "Conflicted Candidate", "Stale Candidate", "Rejected Candidate", "rule_is_not_reality", "rule_is_not_fact",
        "confidence_does_not_create_decision", "new_evidence_can_update_rule", "temporary_rule_can_expire",
        "unknowns_are_preserved", "reducer_is_sole_state_mutation_authority"
    ],
    "human_flow_understanding_contract_v1.json": [
        "Human Flow Understanding Contract v1", "field_reference", "density_candidate", "sparse", "normal", "dense",
        "direction_candidate", "entering", "leaving", "crossing", "stationary", "flow_pattern_candidate", "queue",
        "gathering", "dispersal", "evacuation", "circulation", "supporting_evidence", "confidence", "provenance",
        "uncertainty", "unknowns", "group_pattern_only", "does_not_identify_motive", "does_not_identify_emotion",
        "does_not_infer_social_relationship", "does_not_create_role", "does_not_predict", "does_not_execute_action",
        "reality_update_requires_reducer"
    ],
    "field_attention_rule_interface_v1.json": [
        "Field Attention Rule Interface v1", "field_reference", "rule_reference", "dynamic_reference", "attention_bias_candidate",
        "exit", "sign", "flow", "information_value", "uncertainty", "risk_context", "resource_cost", "reactivation_candidate",
        "release_candidate", "attention_does_not_modify_reality", "attention_does_not_modify_goal",
        "attention_does_not_modify_decision", "attention_does_not_execute_action", "candidate_only", "unknowns_are_preserved"
    ],
    "field_capability_requirement_interface_v1.json": [
        "Field Capability Requirement Interface v1", "field_reference", "task_reference", "rule_context", "dynamic_context",
        "unknown_context", "capability_requirement_candidate", "OCR", "spatial", "human-flow", "user-confirmation", "reason",
        "Field + Task + Unknown", "information_value", "resource_cost", "risk", "provenance", "model_is_not_requirement_authority",
        "provider_is_not_requirement_authority", "field_does_not_select_model", "capability_governance_required",
        "unknowns_are_preserved", "candidate_only"
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
