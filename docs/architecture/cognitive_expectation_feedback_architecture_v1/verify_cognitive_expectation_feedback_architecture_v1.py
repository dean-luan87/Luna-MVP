#!/usr/bin/env python3
"""V2 final verifier for Expectation and Feedback architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_expectation_feedback_architecture_v1.md": [
        "Cognitive Expectation and Feedback Architecture v1", "Expectation Candidate", "Reality Feedback",
        "Reality", "Evidence", "Hypothesis", "Belief Candidate", "Expectation", "Experience", "Learning",
        "Future Understanding", "Prediction is a future-event estimate", "Expectation is not Prediction",
        "Prediction Runtime", "World Model", "expected_state", "expected_evidence", "time_context", "confidence",
        "validation_condition", "feedback_status", "lifecycle_state", "Hypothesis Driven", "Belief Driven",
        "Field Rule Driven", "Task Driven", "Hypothesis explains current uncertainty", "Expectation specifies",
        "Field Context", "Situation", "Belief or Hypothesis source", "Time", "Reality Observation", "Compare",
        "Feedback Candidate", "Update Candidate", "Confirmed", "Partially Confirmed", "Contradicted", "Unknown", "Expired",
        "Expectation Difference", "not Prediction Error", "Feedback has priority over stale Belief",
        "Observation Requirement", "Attention Request", "Attention owns resource allocation", "Memory records what occurred",
        "Learning receives Feedback", "Brain receives an Expectation Package", "Brain retains final judgment authority",
        "Expectation does not make a Decision", "Created → Active → Validated → Updated → Contradicted →",
        "Deprecated", "Archived", "Simulation Expectation Candidate", "B Simulation Runtime", "automatic future reasoning",
        "automatic Belief modification", "automatic Reality modification", "automatic Decision", "Action Runtime",
        "model training", "hardware execution", "Provenance", "Unknown is preserved"
    ],
    "expectation_whitebox_v1.md": [
        "Who creates an Expectation Candidate", "Who owns current Reality", "Who compares expected and observed state",
        "Who owns the Hypothesis/Expectation boundary", "Who allocates observation resources", "Who receives Feedback",
        "Who evaluates material contradiction", "Who owns Task continuity", "Hypothesis / Belief / Field Rule / Task",
        "Expectation Candidate", "Validation Requirement + Context", "Attention Request", "Reality Observation",
        "Feedback / Difference", "Experience + Learning Candidate", "Brain Context Package", "Expectation → Prediction Runtime",
        "Expectation → World Model", "Expectation → Reality write", "Expectation → automatic Belief modification",
        "Expectation → automatic Decision", "Expectation → Action Runtime", "Attention → Expectation selection",
        "Learning → automatic Expectation update", "Feedback → silent Unknown completion", "B Route Snapshot → live Expectation mutation",
        "Expected State", "Expected Evidence", "Reality Observation", "Feedback Status", "Difference", "Unknown", "Risk",
        "Field Context", "Situation", "Time Context", "Lifecycle State", "Provenance"
    ],
    "expectation_go_no_go_v1.md": [
        "Expectation Candidate", "Prediction", "Hypothesis/Belief", "Field", "Situation", "Time", "Expected Evidence",
        "Feedback Status", "Difference", "Unknown", "Confidence", "Provenance", "Confirmed", "Partially Confirmed",
        "Contradicted", "Feedback has priority over stale Belief", "multiple Expectation Candidates", "Attention only receives validation requirements",
        "Learning receives Feedback", "Expectation Package", "Brain retains final judgment authority", "B Route is a placeholder only",
        "No Prediction Runtime", "No World Model", "No automatic future reasoning", "No automatic Belief modification",
        "No automatic Reality modification", "No automatic Decision", "No Action Runtime", "No B Simulation Runtime",
        "No model training", "No hardware execution", "no silent Unknown completion", "V0 static checks", "V1",
        "V2 Final Phase Verification", "User Terminal Only", "V3", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "expectation_schema_v1.json": [
        "Expectation Schema v1", "Expectation Candidate", "expectation_id", "source_hypothesis", "source_belief",
        "related_field", "related_situation", "expected_state", "expected_evidence", "time_context", "confidence",
        "validation_condition", "feedback_status", "lifecycle_state", "Hypothesis Driven", "Belief Driven", "Field Rule Driven",
        "Task Driven", "supporting_evidence", "unknowns", "risk", "difference_reference", "provenance",
        "expectation_is_not_prediction", "expectation_does_not_modify_reality", "expectation_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "expectation_source_contract_v1.json": [
        "Expectation Source Contract v1", "Expectation Source Governance", "Hypothesis Driven", "Belief Driven",
        "Field Rule Driven", "Task Driven", "source_id", "source_type", "hypothesis_reference", "belief_reference",
        "field_rule_reference", "task_reference", "field_reference", "situation_reference", "confidence", "provenance", "unknowns",
        "source_does_not_make_decision", "source_does_not_modify_reality", "source_does_not_modify_belief_automatically",
        "unknowns_are_preserved"
    ],
    "expectation_hypothesis_interface_v1.json": [
        "Expectation Hypothesis Interface v1", "Hypothesis to Expectation Candidate", "hypothesis_reference",
        "hypothesis_explanation", "supporting_evidence", "contradicting_evidence", "field_context", "situation_context",
        "confidence", "unknowns", "provenance", "expectation_candidate", "expected_evidence", "validation_condition",
        "difference_basis", "hypothesis_is_not_expectation", "expectation_is_not_prediction", "hypothesis_does_not_create_reality",
        "expectation_does_not_make_decision", "unknowns_are_preserved"
    ],
    "expectation_belief_interface_v1.json": [
        "Expectation Belief Interface v1", "Belief to Expectation Candidate", "belief_reference", "validated_pattern_reference",
        "field_context", "situation_context", "confidence", "decay_state", "unknowns", "provenance", "expectation_candidate",
        "expected_state", "expected_evidence", "revalidation_requirement", "belief_is_not_reality",
        "belief_does_not_override_current_feedback", "belief_does_not_create_expectation_as_fact", "expectation_is_revocable",
        "unknowns_are_preserved"
    ],
    "expectation_field_binding_v1.json": [
        "Expectation Field Binding v1", "Expectation Field Context Binding", "expectation_reference", "field_reference",
        "field_state", "field_rule_context", "situation_reference", "time_context", "provenance", "unknowns",
        "expectation_is_field_bound", "expectation_references_existing_field", "binding_does_not_create_field",
        "binding_does_not_mutate_field", "expectation_does_not_cross_field_silently", "same_state_can_have_different_field_expectation",
        "unknowns_are_preserved"
    ],
    "expectation_situation_interface_v1.json": [
        "Expectation Situation Interface v1", "Situation to Expectation Context", "situation_reference", "current_understanding",
        "hypothesis_candidates", "belief_candidates", "field_context", "intent_context", "goal_context", "task_context", "unknowns",
        "provenance", "expectation_candidates", "validation_conditions", "feedback_status", "situation_does_not_create_prediction",
        "expectation_does_not_modify_situation_automatically", "reality_feedback_updates_situation_candidate", "unknowns_are_preserved"
    ],
    "expectation_feedback_contract_v1.json": [
        "Expectation Feedback Contract v1", "Expectation to Reality Feedback", "expectation_reference", "expected_state",
        "expected_evidence", "reality_observation", "evidence_references", "field_context", "situation_context", "time_context",
        "provenance", "unknowns", "Confirmed", "Partially Confirmed", "Contradicted", "Expired", "comparison_basis",
        "expectation_difference", "confidence_update_candidate", "feedback_candidate", "experience_record", "learning_candidate",
        "feedback_has_priority_over_stale_belief", "feedback_does_not_modify_reality", "feedback_does_not_modify_belief_automatically",
        "feedback_does_not_make_decision", "unknowns_are_preserved"
    ],
    "expectation_difference_schema_v1.json": [
        "Expectation Difference Schema v1", "Expectation Difference", "difference_id", "expectation_reference", "expected_state",
        "observed_reality", "comparison_basis", "difference_category", "difference_magnitude", "feedback_status", "learning_signal",
        "unknowns", "risk", "provenance", "difference_is_not_prediction_error", "difference_does_not_modify_belief_automatically",
        "difference_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "expectation_attention_interface_v1.json": [
        "Expectation Attention Interface v1", "Expectation Validation Attention Request", "expectation_reference",
        "validation_condition", "expected_evidence", "risk", "unknowns", "field_context", "provenance", "attention_request",
        "observation_targets", "priority_candidate", "persistence_candidate", "resource_cost_candidate",
        "expectation_produces_observation_requirement", "expectation_does_not_allocate_attention", "attention_owns_resource_allocation",
        "attention_only_supports_validation", "unknowns_are_preserved"
    ],
    "expectation_memory_interface_v1.json": [
        "Expectation Memory Interface v1", "Expectation and Memory Separation", "expectation_reference", "feedback_reference",
        "experience_record", "field_context", "time_context", "provenance", "unknowns", "observed_event", "expectation_at_time",
        "feedback_status", "difference_reference", "experience_candidate", "memory_records_what_occurred",
        "expectation_records_what_was_expected", "memory_does_not_override_reality", "memory_does_not_modify_expectation_automatically",
        "unknowns_are_preserved"
    ],
    "expectation_learning_interface_v1.json": [
        "Expectation Learning Interface v1", "Feedback to Learning Candidate", "expectation_reference", "feedback_status",
        "expectation_difference", "experience_record", "evidence_references", "field_reference", "provenance", "unknowns",
        "learning_candidate", "future_adjustment_candidate", "pattern_candidate", "learning_receives_feedback",
        "learning_does_not_modify_expectation_automatically", "learning_does_not_modify_belief_automatically",
        "learning_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "expectation_brain_interface_v1.json": [
        "Expectation Brain Interface v1", "Expectation Package for Brain", "current_understanding", "expectation_candidates",
        "supporting_evidence", "feedback_status", "expectation_difference", "unknown", "risk", "conflict", "field_context",
        "situation_context", "provenance", "accept_feedback", "request_more_observation", "keep_expectations_separate",
        "request_clarification", "final_judgment", "brain_receives_expectation_package", "expectation_does_not_make_decision",
        "brain_retains_final_decision_authority", "brain_does_not_receive_prediction_runtime", "unknowns_are_preserved"
    ],
    "expectation_lifecycle_contract_v1.json": [
        "Expectation Lifecycle Contract v1", "Expectation Candidate Lifecycle", "Created", "Active", "Validated", "Updated",
        "Contradicted", "Deprecated", "Archived", "Created → Active", "Active → Validated", "Validated → Updated",
        "Active → Contradicted", "Updated → Contradicted", "Contradicted → Deprecated", "Deprecated → Archived", "candidate_based",
        "feedback_status_required", "time_context_required", "provenance_preserved", "contradiction_does_not_delete_history",
        "lifecycle_does_not_make_decision", "lifecycle_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "expectation_governance_contract_v1.json": [
        "Expectation Governance Contract v1", "Expectation Admission and Feedback Governance", "source permission",
        "Hypothesis or Belief compatibility", "Field binding", "Situation binding", "Task compatibility", "expected Evidence",
        "validation condition", "time context", "confidence", "Unknown", "Risk", "Provenance", "Reality observation",
        "comparison basis", "Difference", "Feedback Status", "current Field", "current Time", "expectation", "attention",
        "observation", "feedback", "memory", "learning", "brain", "reality", "no_prediction_runtime", "no_world_model",
        "no_automatic_future_reasoning", "no_automatic_belief_modification", "no_automatic_reality_modification",
        "no_automatic_decision", "no_action_runtime", "no_b_simulation_runtime", "no_model_training", "no_hardware_execution",
        "no_silent_unknown_completion", "unknowns_are_preserved", "constitution_review_required", "protocol_version_required",
        "field_scope_review_required", "brain_boundary_review_required"
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
