#!/usr/bin/env python3
"""V2 final verifier for Hypothesis and Belief architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_hypothesis_belief_architecture_v1.md": [
        "Cognitive Hypothesis and Belief Architecture v1", "Hypothesis Candidate", "Belief Candidate",
        "Reality", "Evidence", "Hypothesis", "Field Understanding", "Situation", "Intent", "Goal", "Task",
        "Decision Boundary", "Reality > Evidence > Hypothesis > Belief Candidate > Decision Context",
        "Hypothesis is not Prediction", "Prediction Runtime", "Unknown", "hypothesis_id", "source_evidence",
        "related_field", "related_situation", "candidate_explanation", "confidence", "uncertainty",
        "supporting_evidence", "contradicting_evidence", "validation_status", "lifecycle_state",
        "Evidence Driven", "Field Rule Driven", "Experience Driven", "Human Feedback Driven",
        "Hypothesis is always bound to an existing Field and Situation", "Hypothesis = Evidence + Field Context + Situation Context",
        "Confidence is a candidate assessment", "Hypothesis Conflict", "multiple candidates", "Brain Evaluation",
        "Validation Requirement", "Attention Request", "Evidence Update", "Attention owns resource allocation",
        "Validated Pattern", "Experience Reference", "Reality always overrides Belief Candidate",
        "Validation Result", "Memory stores", "Brain retains final judgment authority", "Created → Candidate → Validated → Active Reference → Contradicted →",
        "Deprecated", "Archived", "B Route", "Simulation Hypothesis Candidate", "B Simulation Runtime",
        "World Model", "automatic belief solidification", "Reality mutation", "automatic Decision", "Action Runtime",
        "model training", "hardware execution", "Provenance", "Unknown is first-class"
    ],
    "hypothesis_whitebox_v1.md": [
        "Who creates a Hypothesis Candidate", "Who owns Reality", "Who owns the Field binding", "Who qualifies confidence",
        "Who allocates validation resources", "Who executes Observation", "Who receives Validation Result",
        "Who admits a Belief Candidate", "Who resolves material conflicts", "Who owns final judgment",
        "Evidence / Field Rule / Experience / Human Feedback", "Hypothesis Candidate", "Field + Situation + Confidence + Unknown",
        "Validation Requirement", "Attention Request", "Evidence Update", "Belief Candidate (admitted)", "Brain Context Package",
        "Hypothesis → Reality write", "Belief → Evidence override", "Hypothesis → Decision", "Belief → automatic Decision",
        "Attention → Hypothesis selection", "Learning → automatic belief solidification", "Provider/Model → Belief",
        "Hypothesis → Prediction Runtime", "Hypothesis → B Simulation Runtime", "Hypothesis → Action Runtime",
        "Unknown", "Confidence", "Uncertainty", "Supporting Evidence", "Contradicting Evidence", "Validation Status",
        "Lifecycle State", "Field Context", "Situation Context", "Provenance", "Hypothesis Conflict"
    ],
    "hypothesis_go_no_go_v1.md": [
        "Hypothesis Candidate", "Reality", "Prediction", "Belief Candidate", "Evidence", "Unknown",
        "Reality > Evidence > Hypothesis > Belief Candidate", "Evidence Driven", "Field Rule Driven", "Experience Driven",
        "Human Feedback Driven", "Field and Situation", "Confidence", "support", "contradiction", "Provenance",
        "multiple Hypothesis Candidates", "Hypothesis Conflict", "Brain Evaluation", "validation requirements",
        "Attention", "Learning", "Validation Result", "validated-pattern admission", "B Route", "Simulation Placeholder",
        "No Prediction Runtime", "No World Model construction", "No automatic belief solidification", "No automatic Reality mutation",
        "No automatic Decision", "No Action Runtime", "No B Simulation Runtime", "No model training", "No hardware execution",
        "no silent Unknown completion", "no forced conflict resolution", "V0 static checks", "V1", "V2 Final Phase Verification",
        "User Terminal Only", "V3", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "hypothesis_schema_v1.json": [
        "Hypothesis Schema v1", "Hypothesis Candidate", "hypothesis_id", "source_evidence", "related_field",
        "related_situation", "candidate_explanation", "confidence", "uncertainty", "supporting_evidence",
        "contradicting_evidence", "validation_status", "lifecycle_state", "Evidence Driven", "Field Rule Driven",
        "Experience Driven", "Human Feedback Driven", "field_context", "situation_context", "attention_request_reference",
        "validation_requirement", "risk", "constraints", "time_validity", "provenance", "unknowns",
        "hypothesis_is_not_reality", "hypothesis_is_not_prediction", "hypothesis_does_not_make_decision",
        "hypothesis_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "belief_candidate_schema_v1.json": [
        "Belief Candidate Schema v1", "Belief Candidate", "belief_id", "validated_pattern_reference", "hypothesis_references",
        "related_field", "related_situation_class", "belief_expression", "validation_count", "confidence",
        "supporting_evidence", "contradicting_evidence", "uncertainty", "lifecycle_state", "admission_status",
        "decay_policy", "provenance", "unknowns", "belief_is_not_reality", "belief_does_not_override_evidence",
        "belief_does_not_make_decision", "belief_is_revocable", "unknowns_are_preserved"
    ],
    "evidence_hypothesis_contract_v1.json": [
        "Evidence Hypothesis Contract v1", "Evidence to Hypothesis Candidate", "evidence_reference", "evidence_type",
        "related_field", "related_situation", "confidence", "provenance", "unknowns", "hypothesis_candidate",
        "candidate_explanation", "supporting_evidence", "contradicting_evidence", "validation_requirement",
        "evidence_does_not_become_reality_automatically", "hypothesis_is_not_reality", "hypothesis_is_not_prediction",
        "hypothesis_does_not_make_decision", "hypothesis_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "hypothesis_confidence_contract_v1.json": [
        "Hypothesis Confidence Contract v1", "Hypothesis Confidence Candidate", "hypothesis_reference", "basis",
        "uncertainty", "source_reliability", "field_validity", "calibration_history", "supporting_evidence",
        "contradicting_evidence", "unknowns", "confidence_update", "confidence_is_not_truth", "confidence_does_not_override_reality",
        "confidence_does_not_make_decision", "unknowns_are_preserved"
    ],
    "hypothesis_validation_contract_v1.json": [
        "Hypothesis Validation Contract v1", "Hypothesis Validation Requirement and Result", "hypothesis_reference",
        "discriminating_observations", "field_reference", "situation_reference", "unknowns", "provenance",
        "attention_request", "capability_requirement", "evidence_expectation", "resource_cost", "validation_result",
        "Supported", "Weakened", "Contradicted", "Inconclusive", "experience_candidate", "belief_admission_candidate",
        "attention_only_validates", "validation_does_not_make_decision", "validation_does_not_modify_reality",
        "unknowns_are_preserved"
    ],
    "hypothesis_conflict_contract_v1.json": [
        "Hypothesis Conflict Contract v1", "Hypothesis Conflict", "conflict_id", "hypothesis_candidates", "shared_evidence",
        "field_context", "situation_context", "confidence_comparison", "supporting_evidence", "contradicting_evidence",
        "risk", "unknowns", "tradeoffs", "provenance", "resolution_status", "conflict_is_preserved",
        "conflict_does_not_auto_select", "conflict_requires_brain_evaluation", "conflict_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "hypothesis_field_interface_v1.json": [
        "Hypothesis Field Interface v1", "Hypothesis Field Context Binding", "hypothesis_reference", "field_reference",
        "field_state", "field_rule_context", "situation_reference", "time_validity", "provenance", "unknowns",
        "hypothesis_is_field_bound", "hypothesis_references_existing_field", "hypothesis_does_not_create_field",
        "hypothesis_does_not_mutate_field", "hypothesis_does_not_cross_field_silently",
        "same_evidence_can_have_different_field_meaning", "unknowns_are_preserved"
    ],
    "hypothesis_attention_interface_v1.json": [
        "Hypothesis Attention Interface v1", "Hypothesis Validation Attention Request", "hypothesis_reference",
        "validation_requirement", "discriminating_observations", "risk", "unknowns", "field_context", "provenance",
        "attention_request", "observation_targets", "priority_candidate", "resource_cost_candidate",
        "hypothesis_produces_validation_requirement", "hypothesis_does_not_allocate_attention",
        "attention_owns_resource_allocation", "attention_only_validates", "unknowns_are_preserved"
    ],
    "hypothesis_learning_interface_v1.json": [
        "Hypothesis Learning Interface v1", "Hypothesis Validation to Learning", "hypothesis_reference", "validation_result",
        "evidence_references", "field_reference", "experience_reference", "provenance", "unknowns", "pattern_candidate",
        "future_candidate", "belief_admission_candidate", "learning_receives_validation_result",
        "learning_does_not_solidify_belief_automatically", "learning_does_not_modify_reality", "experience_is_not_reality",
        "unknowns_are_preserved"
    ],
    "hypothesis_brain_interface_v1.json": [
        "Hypothesis Brain Interface v1", "Hypothesis Decision Context Package", "reality", "evidence", "hypothesis_candidates",
        "belief_candidates", "confidence", "unknown", "risk", "conflict", "field_context", "situation_context", "provenance",
        "adopt_candidate", "reject_candidate", "keep_multiple", "request_more_evidence", "defer", "final_judgment",
        "hypothesis_is_context_not_decision", "belief_is_context_not_decision", "brain_retains_final_decision_authority",
        "brain_receives_reality_and_evidence", "unknowns_are_preserved"
    ],
    "belief_lifecycle_contract_v1.json": [
        "Belief Lifecycle Contract v1", "Belief Candidate Lifecycle", "Created", "Candidate", "Validated", "Active Reference",
        "Contradicted", "Deprecated", "Archived", "Created → Candidate", "Candidate → Validated", "Validated → Active Reference",
        "Active Reference → Contradicted", "Contradicted → Deprecated", "Deprecated → Archived", "validated_pattern_required",
        "repeated_or_high_impact_validation", "field_compatibility_review", "contradiction_review", "governance_admission_required",
        "belief_is_not_reality", "belief_does_not_override_evidence", "belief_is_revocable", "contradiction_preserves_history",
        "lifecycle_does_not_make_decision", "unknowns_are_preserved"
    ],
    "belief_governance_contract_v1.json": [
        "Belief Governance Contract v1", "Belief Candidate Admission and Governance", "validated pattern", "supporting evidence",
        "contradicting evidence", "confidence calibration", "Field compatibility", "Situation compatibility", "uncertainty", "risk",
        "provenance", "decay and expiry", "hypothesis", "learning", "memory", "governance", "attention", "brain", "reality", "evidence",
        "no_automatic_belief_solidification", "no_reality_mutation", "no_evidence_override", "no_automatic_decision",
        "no_action_runtime", "no_prediction_runtime", "no_world_model", "no_b_simulation_runtime", "no_model_training",
        "no_hardware_execution", "no_silent_unknown_completion", "no_forced_conflict_resolution", "unknowns_are_preserved",
        "constitution_review_required", "protocol_version_required", "field_scope_review_required", "brain_boundary_review_required"
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
