#!/usr/bin/env python3
"""V2 final verifier for Experience and Adaptation architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_experience_system_model_v1.md": [
        "long-term compression", "Reality", "Field", "Self", "Behavior", "not a storage-only Memory",
        "not a Knowledge", "not a Rule", "not a Decision", "Current Reality > Recent Experience > Old Experience",
        "Current Reality always overrides", "Outcome", "Cause Attribution", "Experience Candidate", "Experience Evaluation",
        "Experience Memory", "Pattern Candidate", "Adaptation Candidate", "Future Attention / Behavior Adjustment",
        "Episodic Experience", "Field Experience", "Behavioral Experience", "Self Experience", "Interaction Experience",
        "Field Rule", "Action command", "Social Relationship", "Experience Value Assessment", "Repeatability", "Reliability",
        "Relevance", "Impact", "Conflict", "Experience Retention Candidate", "Unknown", "unconfirmed information",
        "one-off noise", "Model guesses", "Field Pattern Candidate", "Behavior Pattern Candidate", "Attention Pattern Candidate",
        "Self Capability Adjustment Candidate", "Increase attention to exits", "Always avoid this place",
        "Attention Pattern Candidate", "Behavior Pattern Candidate", "Self Capability Adjustment Candidate", "Current Reality",
        "Recent Experience", "Old Experience", "Conflict Candidate", "No online learning", "Model Training",
        "parameter update", "automatic policy rewrite", "automatic action", "No Emotion Runtime", "No Role System",
        "No Social Relationship", "No B Route", "No Prediction", "No Action Runtime"
    ],
    "experience_classification_model_v1.md": [
        "Episodic Experience", "Field Experience", "Behavioral Experience", "Self Experience", "Interaction Experience",
        "bounded event", "Outcome", "Field context", "repeated pattern", "Field Pattern Candidate", "not a Rule",
        "Behavior Candidate", "Behavior Pattern Candidate", "Capability/State evidence", "Self Capability Adjustment Candidate",
        "interaction outcome", "Social Relationship", "experience_id", "field_reference", "self_reference", "outcome_reference",
        "evidence_reference", "timestamp", "confidence", "unknowns", "provenance", "Classification", "Evaluation",
        "Retention Candidate", "unconfirmed Model guess", "one-off noise", "Reality", "Knowledge", "Rule", "Decision"
    ],
    "experience_memory_boundary_v1.md": [
        "Short-term Experience Candidate", "Mid-term Experience Pattern Candidate", "Long-term Experience Reference",
        "Outcome", "Cause Attribution", "Field", "Behavior", "Attention", "Self", "provenance", "confidence",
        "recency", "decay", "compression", "Current Reality > Experience", "Unknown", "source provenance",
        "high-frequency regularity", "high-impact events", "important Field changes", "validated Self Capability changes",
        "one-off noise", "unconfirmed information", "Model guesses", "Pattern strength decays", "Archived Experience",
        "historical candidate", "No database implementation", "No Memory Runtime", "No automatic learning", "No Action"
    ],
    "experience_whitebox_v1.md": [
        "Outcome", "Cause Attribution", "Experience Candidate", "Experience Evaluation", "Experience Memory",
        "Pattern Candidate", "Adaptation Candidate", "Future Attention / Behavior Adjustment", "Who creates Experience Candidate",
        "Outcome and Cause Attribution", "not a Model directly", "Who evaluates retention", "Repeatability", "Reliability",
        "Relevance", "Impact", "Conflict", "Who may promote a pattern", "single unconfirmed event", "Who wins conflicts",
        "Current Reality", "Recent Experience", "Old Experience", "Who owns Goal and final Decision", "Who may modify Reality",
        "Reality Reducer", "Who observes adaptation health", "Diagnostic Candidate", "Experience → Attention Pattern Candidate",
        "Experience → Behavior Pattern Candidate", "Experience → Self Capability Adjustment Candidate", "Experience → Action",
        "Experience → Goal", "Experience → Decision", "Experience → Identity", "Model Parameter Mutation", "automatic learning",
        "Model Training", "Memory Runtime", "Emotion Runtime", "Role System", "Social Relationship", "B Route", "Prediction",
        "Action Runtime"
    ],
    "experience_go_no_go_v1.md": [
        "long-term compression", "Reality", "Field", "Self", "Behavior", "storage-only Memory", "Outcome", "Cause Attribution",
        "Experience Candidate", "Experience Evaluation", "Experience Memory", "Pattern Candidate", "Adaptation Candidate",
        "Episodic Experience", "Field Experience", "Behavioral Experience", "Self Experience", "Interaction Experience",
        "Repeatability", "Reliability", "Relevance", "Impact", "Conflict", "one-off noise", "unconfirmed information",
        "Model guesses", "Current Reality > Recent Experience > Old Experience", "Attention", "Behavior", "Self Capability",
        "Unknown", "provenance", "conflict", "decay", "compression", "release", "No automatic learning", "No Model Training",
        "No parameter update", "No Emotion Runtime", "No Role System", "No Social Relationship", "No B Route", "No Prediction",
        "No Action Runtime", "directly modify Reality", "directly modify Goal", "directly modify Decision", "directly modify Identity",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "experience_schema_v1.json": [
        "Experience Schema v1", "experience_id", "experience_class", "Episodic", "Field", "Behavioral", "Self", "Interaction",
        "field_reference", "self_reference", "outcome_reference", "evidence_reference", "timestamp", "confidence", "unknowns",
        "provenance", "repeatability", "reliability", "relevance", "impact", "conflict", "retention_state", "Candidate",
        "Short-term", "Mid-term", "Long-term", "Archived", "Rejected", "pattern_candidate", "adaptation_candidate",
        "is_reality", "is_rule", "is_decision", "unknowns_are_preserved", "current_reality_precedence"
    ],
    "experience_evaluation_contract_v1.json": [
        "Experience Evaluation Contract v1", "experience_candidate_reference", "repeatability", "reliability", "relevance",
        "impact", "conflict", "evidence_support", "unknowns", "provenance", "Experience Retention Candidate",
        "one_off_noise_not_promoted", "unconfirmed_information_not_promoted", "model_guess_not_promoted", "current_reality_overrides",
        "evaluation_does_not_modify_reality", "evaluation_does_not_modify_goal", "evaluation_does_not_modify_decision",
        "evaluation_does_not_execute_action", "unknowns_are_preserved"
    ],
    "field_experience_memory_contract_v1.json": [
        "Field Experience Memory Contract v1", "field_reference", "context", "observed_pattern", "supporting_experiences",
        "repeatability", "reliability", "relevance", "impact", "conflict", "field_pattern_candidate", "pattern_is_not_rule",
        "pattern_is_not_reality", "current_reality_precedence", "unknowns_are_preserved", "provenance_required", "decay_required",
        "compression_boundary_required"
    ],
    "behavior_experience_adaptation_contract_v1.json": [
        "Behavior Experience Adaptation Contract v1", "experience_reference", "behavior_pattern_candidate", "current_field_validation",
        "goal_context", "self_capability_context", "constraints", "unknowns", "behavior_candidate_output",
        "experience_does_not_control_action", "experience_does_not_modify_goal", "experience_does_not_make_decision",
        "reality_overrides_experience", "unknowns_are_preserved"
    ],
    "attention_experience_adaptation_interface_v1.json": [
        "Attention Experience Adaptation Interface v1", "experience_reference", "field_context", "attention_pattern_candidate",
        "information_value", "risk_context", "uncertainty", "resource_cost", "future_attention_candidate",
        "attention_governance_review_required", "experience_does_not_directly_allocate_attention", "experience_does_not_modify_goal",
        "experience_does_not_modify_decision", "anomaly_reactivation_preserved", "decay_required", "unknowns_are_preserved"
    ],
    "self_experience_adaptation_interface_v1.json": [
        "Self Experience Adaptation Interface v1", "experience_reference", "capability_reference", "self_state_reference",
        "evidence_reference", "capability_adjustment_candidate", "self_state_adjustment_candidate", "identity_reference",
        "identity_continuity_required", "experience_does_not_modify_identity", "experience_does_not_claim_capability_without_evidence",
        "current_reality_precedence", "diagnostics_candidate_allowed", "unknowns_are_preserved"
    ],
    "experience_conflict_resolution_contract_v1.json": [
        "Experience Conflict Resolution Contract v1", "Current Reality > Recent Experience > Old Experience", "current_reality",
        "recent_experience", "old_experience", "conflict_candidate", "supporting_evidence", "recency", "reliability", "unknowns",
        "conflict_is_not_silently_erased", "reducer_or_governed_review_required", "experience_does_not_overwrite_reality",
        "experience_does_not_make_decision", "unknowns_are_preserved"
    ],
    "adaptation_candidate_contract_v1.json": [
        "Adaptation Candidate Contract v1", "source_experience_reference", "candidate_type", "Attention Pattern", "Behavior Pattern",
        "Self Capability Adjustment", "Field Observation", "scope", "condition", "expected_effect", "confidence", "unknowns",
        "provenance", "validation_state", "Candidate", "Review", "Accepted Candidate", "Rejected", "Expired",
        "increase_attention_to_exits", "always_avoid_this_place", "candidate_only", "no_automatic_learning",
        "no_model_parameter_update", "no_direct_action", "no_goal_mutation", "no_decision_mutation", "no_identity_mutation",
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
