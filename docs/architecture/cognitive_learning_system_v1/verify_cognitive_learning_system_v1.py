#!/usr/bin/env python3
"""V2 final verifier for Cognitive Learning System architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_learning_architecture_v1.md": [
        "Learning System", "life-experience adaptation layer", "Experience", "Memory", "Attention Adaptation", "Strategy Exploration",
        "Field Behavior", "Capability Feedback", "Event → Observation → Outcome → Experience Record", "Pattern Extraction Candidate",
        "Strategy Candidate", "Validation", "Adaptive Update Candidate", "Learning produces candidates", "does not modify Reality",
        "Identity", "Goal", "Decision", "model parameters", "Current Reality", "historical Experience", "Unknown", "revoked",
        "Survival Learning", "Field Pattern", "Attention Pattern", "Navigation Pattern", "Safety Pattern", "Interaction Pattern",
        "Skill Learning", "future placeholder", "Memory records what happened", "Learning extracts what may be useful",
        "Cause Attribution", "Prediction Error", "expectation-reality difference", "Prediction Runtime", "Expectation → Reality → Difference → Learning Signal",
        "Field Experience", "Role", "Task", "Evidence", "Provenance", "Confidence", "Conflict", "Pattern Candidate", "Rule",
        "Field Learning", "Attention Learning", "Memory Learning", "Capability Learning", "Performance Evidence",
        "Capability Confidence Update Candidate", "Learning Governance", "provenance", "context binding", "validation before activation",
        "revocability", "One anomalous episode", "Automatic strategy switching", "Online Learning Runtime", "model training",
        "parameter modification", "Emotion Runtime", "B Route", "Action Runtime", "Observed → Recorded → Evaluated → Pattern Candidate",
        "Validated → Adaptation Candidate → Accepted / Rejected / Revoked → Archived", "automatic activation"
    ],
    "learning_whitebox_v1.md": [
        "Reality / Field / Self / Attention / Memory / Outcome", "Experience Record", "Pattern Extraction Candidate", "Strategy Candidate",
        "Validation / Review", "Adaptive Update Candidate", "Who records experience", "Who extracts a pattern", "Who proposes a strategy",
        "Who validates adaptation", "Who owns Goal and final Decision", "Brain", "Reality Reducer", "Model parameters", "Learning has no training authority",
        "Prediction Error", "Prediction Runtime", "Experience → Pattern Candidate", "Pattern → Strategy Candidate", "Outcome → Learning Signal",
        "Learning → Reality Write", "Learning → Identity Mutation", "Learning → Goal Mutation", "Learning → Decision", "Learning → Action",
        "Learning → Model Training", "automatic strategy activation", "Current Reality outranks Experience", "Unknown", "Conflict", "Provenance",
        "Survival Learning", "Skill Learning", "placeholder only"
    ],
    "learning_go_no_go_v1.md": [
        "Experience → Pattern → Strategy → Feedback → Adaptation Candidate", "Survival Learning", "Field", "Attention", "Navigation",
        "Safety", "Interaction Patterns", "Skill Learning", "placeholder-only", "Prediction Error", "Expectation–Reality Difference",
        "not Prediction Runtime", "Field Learning", "Field, Role, Task", "Attention", "Memory", "Capability", "Learning Governance",
        "Reality priority", "Unknown preservation", "validation", "revocability", "Observed", "Recorded", "Evaluated", "Pattern Candidate",
        "Strategy Candidate", "Validated", "Adaptive Update Candidate", "Accepted", "Rejected", "Revoked", "Archived", "No automatic model training",
        "No parameter modification", "No Online Learning Runtime", "No automatic strategy switching", "No Emotion Runtime", "No B Route",
        "No Action Runtime", "cannot modify Reality", "Identity", "Goal", "Decision", "Action", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "learning_system_schema_v1.json": [
        "Learning System Schema v1", "learning_id", "Survival Learning", "experience_reference", "memory_reference", "field_pattern",
        "attention_pattern", "navigation_pattern", "safety_pattern", "interaction_pattern", "skill_learning_placeholder", "candidate_only",
        "reality_priority", "unknowns_are_preserved", "revocable"
    ],
    "experience_learning_pipeline_v1.json": [
        "Experience Learning Pipeline v1", "Event", "Observation", "Outcome", "Experience Record", "Pattern Extraction Candidate",
        "Strategy Candidate", "Validation", "Adaptive Update Candidate", "field_context", "role_context", "task_context", "self_context",
        "evidence", "provenance", "confidence", "unknowns", "candidate_only", "does_not_modify_reality", "does_not_modify_identity",
        "does_not_modify_goal", "does_not_modify_decision", "unknowns_are_preserved"
    ],
    "learning_signal_schema_v1.json": [
        "Learning Signal Schema v1", "signal_id", "Prediction Error", "expectation", "reality", "difference", "learning_signal", "evidence",
        "confidence", "unknowns", "attention_candidate", "field_observation_candidate", "signal_does_not_make_prediction",
        "signal_does_not_change_strategy_directly", "unknowns_are_preserved"
    ],
    "prediction_error_contract_v1.json": [
        "Prediction Error Contract v1", "Expectation → Reality → Difference → Learning Signal", "expectation_reference", "reality_reference",
        "difference_reference", "learning_signal_reference", "provenance", "confidence", "unknowns", "prediction_runtime",
        "does_not_modify_reality", "does_not_modify_goal", "does_not_modify_decision", "unknowns_are_preserved"
    ],
    "field_learning_contract_v1.json": [
        "Field Learning Contract v1", "field_reference", "role_reference", "task_reference", "field_experience", "field_pattern_candidate",
        "current_reality_check", "evidence", "confidence", "unknowns", "field_learning_is_context_bound", "pattern_is_not_rule",
        "field_learning_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "attention_learning_interface_v1.json": [
        "Attention Learning Interface v1", "experience_reference", "attention_pattern_candidate", "attention_evaluation_candidate",
        "field_context", "risk", "uncertainty_reduction", "validation_status", "attention_update_is_candidate_only",
        "does_not_allocate_attention_directly", "does_not_make_decision", "unknowns_are_preserved"
    ],
    "memory_learning_interface_v1.json": [
        "Memory Learning Interface v1", "memory_reference", "experience_record", "pattern_extraction_candidate", "retrieval_context",
        "retention_evidence", "provenance", "learning_extracts_does_not_rewrite_memory", "memory_does_not_become_reality", "candidate_only",
        "unknowns_are_preserved"
    ],
    "capability_learning_interface_v1.json": [
        "Capability Learning Interface v1", "capability_reference", "performance_evidence", "failure_attribution",
        "capability_confidence_update_candidate", "self_capability_profile_reference", "hardware_context", "model_training",
        "parameter_modification", "candidate_only", "unknowns_are_preserved"
    ],
    "strategy_candidate_schema_v1.json": [
        "Strategy Candidate Schema v1", "strategy_candidate_id", "field_context", "task_context", "goal_reference", "pattern_reference",
        "expected_benefit_candidate", "risk_candidate", "resource_cost", "capability_requirement", "unknowns", "validation_status",
        "activation_status", "automatic_strategy_switching", "candidate_only", "unknowns_are_preserved"
    ],
    "learning_governance_contract_v1.json": [
        "Learning Governance Contract v1", "reality_priority", "experience_is_not_fact", "unknowns_are_preserved", "candidate_requires_validation",
        "incorrect_experience_is_revocable", "strategy_requires_context_binding", "provenance_required", "confidence_required", "brain_review_candidate",
        "human_review_candidate", "automatic_model_training", "online_learning_runtime", "automatic_strategy_switching",
        "learning_does_not_modify_reality", "learning_does_not_modify_identity", "learning_does_not_modify_goal", "learning_does_not_modify_decision"
    ],
    "learning_lifecycle_contract_v1.json": [
        "Learning Lifecycle Contract v1", "Observed", "Recorded", "Evaluated", "Pattern Candidate", "Strategy Candidate", "Validated",
        "Adaptive Update Candidate", "Accepted", "Rejected", "Revoked", "Archived", "accepted_means_candidate_for_future_subsystem",
        "accepted_does_not_mean_automatic_activation", "revocation_supported", "unknowns_are_preserved", "lifecycle_does_not_make_decision"
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
