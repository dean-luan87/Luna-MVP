#!/usr/bin/env python3
"""Static contract verifier for Decision Commitment architecture.

This verifier is intentionally suitable for the repository's V0/V2 contract
workflow. It validates presence and JSON syntax only; it does not execute any
runtime, capability, model, hardware, planning, or action path.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_decision_commitment_architecture_v1.md": [
        "Cognitive Decision Commitment Architecture v1", "Decision Candidate", "Decision Commitment",
        "Action Request Candidate", "Action Boundary", "not an Action", "not a Plan",
        "Reality Freshness Check", "Evidence Sufficiency Check", "Constraint Check", "Intent Alignment Check",
        "Capability Availability Check", "Constitution", "Value", "Safety", "Governance",
        "Executing Preparation", "Invalidated", "Expired", "Validation Requirement", "Attention Request",
        "Expected Outcome", "Maintain / Revise / Invalidate", "Evidence has priority",
        "Memory stores selected Decision Transitions", "Learning receives Decision Outcome",
        "Intent Conflict", "Goal Conflict", "Value Conflict", "Role Conflict", "Resource Conflict", "Time Conflict",
        "Revision Candidate", "New Commitment", "Human Override", "Action Boundary receives an Action Request Candidate",
        "Action Execution", "Hardware Control", "Model Runtime", "automatic planning", "automatic execution",
        "automatic Value or Goal modification", "B Simulation Runtime", "Prediction Runtime", "model or hardware call"
    ],
    "decision_whitebox_v1.md": [
        "Who creates a Decision Commitment Candidate", "Who validates freshness and constraints",
        "Who owns Capability status", "Who owns Attention", "Who owns Expected Outcome",
        "Who owns Goal and Intent", "Who owns Action permission and execution", "Who can override",
        "Who owns revision", "Brain Decision Candidate", "Decision Commitment Candidate",
        "Reality Freshness + Evidence Sufficiency + Constraint Check",
        "Intent Alignment + Capability Availability Check", "Expected Outcome / Validation Requirement",
        "Action Request Candidate → Action Boundary", "Brain → Action Execution",
        "Decision Candidate → direct Action Request", "Commitment → Reality mutation",
        "Commitment → Goal mutation", "Commitment → Value mutation", "Commitment → Capability invocation",
        "Commitment → Model Runtime or Hardware Control", "Commitment → automatic planning",
        "Commitment → automatic execution", "Commitment → Prediction Runtime or B Simulation Runtime",
        "Learning → automatic strategy modification", "Conflict → silent selection", "Provenance"
    ],
    "decision_go_no_go_v1.md": [
        "Decision Candidate", "Decision Commitment", "Action Request Candidate", "Reality Freshness",
        "Evidence Sufficiency", "Constraint", "Intent Alignment", "Capability Availability",
        "Capability Availability is state-only", "Commitment lifecycle", "expiration", "Expected Outcome",
        "Feedback", "Maintain / Revise / Invalidate", "Evidence has priority", "Value remains a constraint",
        "Learning remains an input candidate", "Human Override", "Action Boundary", "No Action Execution",
        "No Hardware Control", "No Model Runtime", "No automatic planning", "No automatic execution",
        "No automatic Value modification", "No automatic Goal modification", "No B Simulation Runtime",
        "No Prediction Runtime", "No Capability invocation", "No model or hardware calls",
        "No silent conflict resolution", "V0 static checks", "V1", "V2 Final Phase Verification",
        "User Terminal Only", "V3", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "decision_candidate_contract_v1.json": [
        "Decision Candidate Contract v1", "Decision Candidate", "decision_candidate_id", "source_brain_trace",
        "related_field", "related_intent", "related_goal", "related_task", "options", "constraints", "risk",
        "unknowns", "confidence", "provenance", "candidate_status", "candidate_is_not_commitment",
        "candidate_is_not_action", "candidate_does_not_execute", "unknowns_are_preserved"
    ],
    "decision_commitment_schema_v1.json": [
        "Decision Commitment Schema v1", "Decision Commitment Candidate", "decision_commitment_id",
        "source_decision_candidate", "related_field", "related_task", "related_intent", "supporting_evidence",
        "confidence", "risk_level", "constraint_check", "resource_requirement", "expiration_condition",
        "commitment_status", "review_trace", "reality_freshness", "evidence_sufficiency", "intent_alignment",
        "capability_availability", "expected_outcome", "validation_requirement", "human_override", "unknowns",
        "conflicts", "provenance", "commitment_is_not_action", "commitment_does_not_execute",
        "commitment_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "decision_validation_contract_v1.json": [
        "Decision Validation Contract v1", "Decision Commitment Validation", "decision_candidate", "current_reality",
        "supporting_evidence", "field_context", "intent_context", "task_context", "capability_state",
        "value_constraints", "risk", "unknowns", "provenance", "Reality Freshness Check", "Evidence Sufficiency Check",
        "Constraint Check", "Intent Alignment Check", "Capability Availability Check", "validation_status",
        "decision_commitment_candidate", "validation_requirement", "review_trace", "validation_does_not_invoke_capability",
        "validation_does_not_execute_action", "validation_does_not_modify_reality", "evidence_has_priority",
        "unknowns_are_preserved"
    ],
    "decision_evidence_requirement_v1.json": [
        "Decision Evidence Requirement v1", "Commitment Evidence Requirement", "decision_candidate",
        "commitment_candidate", "supporting_evidence", "unknowns", "risk_level", "expected_outcome",
        "evidence_sufficiency_check", "missing_evidence", "validation_condition", "more_evidence_request",
        "evidence_requirement_does_not_make_decision", "evidence_requirement_does_not_invoke_capability",
        "evidence_requirement_does_not_execute_action", "unknowns_are_preserved"
    ],
    "decision_constraint_check_contract_v1.json": [
        "Decision Constraint Check Contract v1", "Commitment Constraint Check", "decision_candidate",
        "constitution_constraints", "value_constraints", "safety_constraints", "governance_constraints", "risk",
        "unknowns", "provenance", "constraint_check", "violations", "review_requirement", "commitment_status_candidate",
        "value_is_constraint", "constraint_check_does_not_modify_value", "constraint_check_does_not_modify_goal",
        "constraint_check_does_not_execute", "unknowns_are_preserved"
    ],
    "decision_intent_alignment_contract_v1.json": [
        "Decision Intent Alignment Contract v1", "Commitment Intent Alignment Check", "decision_candidate",
        "intent_reference", "goal_reference", "task_reference", "field_reference", "alignment_context", "unknowns",
        "provenance", "intent_alignment_check", "deviation_candidate", "clarification_request",
        "commitment_review_requirement", "alignment_does_not_modify_intent", "alignment_does_not_modify_goal",
        "alignment_does_not_modify_task", "alignment_does_not_make_decision", "unknowns_are_preserved"
    ],
    "decision_capability_check_contract_v1.json": [
        "Decision Capability Check Contract v1", "Capability Availability Check", "decision_candidate",
        "required_capability", "capability_state", "self_capability_state", "hardware_state", "resource_requirement",
        "unknowns", "provenance", "capability_availability_check", "capability_constraint_candidate",
        "fallback_review_requirement", "commitment_status_candidate", "capability_check_is_state_only",
        "capability_check_does_not_invoke_capability", "capability_check_does_not_select_provider",
        "capability_check_does_not_execute_action", "unknowns_are_preserved"
    ],
    "decision_expectation_interface_v1.json": [
        "Decision Expectation Interface v1", "Commitment Expected Outcome and Feedback", "commitment_reference",
        "expected_outcome", "expectation_reference", "validation_condition", "field_context", "task_context", "unknowns",
        "provenance", "feedback_status", "maintain_candidate", "revision_candidate", "invalidation_candidate",
        "commitment_binds_expected_outcome", "feedback_can_maintain_revise_or_invalidate", "expectation_does_not_make_decision",
        "feedback_does_not_execute_action", "unknowns_are_preserved"
    ],
    "decision_attention_interface_v1.json": [
        "Decision Attention Interface v1", "Commitment Validation Attention Request", "commitment_reference",
        "validation_requirement", "missing_evidence", "risk", "unknowns", "field_context", "provenance",
        "attention_request", "observation_requirement", "validation_targets", "priority_candidate", "resource_cost_candidate",
        "commitment_produces_validation_requirement", "commitment_does_not_allocate_attention",
        "attention_retains_resource_management", "attention_request_is_candidate_only", "unknowns_are_preserved"
    ],
    "decision_memory_interface_v1.json": [
        "Decision Memory Interface v1", "Decision Transition Memory Reference", "commitment_reference", "decision_outcome",
        "outcome_evidence", "field_context", "task_context", "provenance", "unknowns", "decision_transition_record",
        "experience_candidate", "memory_admission_candidate", "memory_stores_selected_decision_transitions",
        "memory_does_not_store_all_decisions", "memory_does_not_modify_commitment", "memory_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "decision_learning_interface_v1.json": [
        "Decision Learning Interface v1", "Decision Outcome to Learning Candidate", "decision_outcome",
        "commitment_reference", "outcome_evidence", "experience_candidate", "field_context", "strategy_reference",
        "provenance", "unknowns", "decision_quality_candidate", "pattern_candidate", "strategy_effect_candidate", "future_candidate",
        "learning_does_not_modify_decision", "learning_does_not_modify_strategy_automatically", "learning_does_not_modify_value",
        "learning_does_not_modify_goal", "unknowns_are_preserved"
    ],
    "decision_action_boundary_interface_v1.json": [
        "Decision Action Boundary Interface v1", "Action Request Candidate Boundary", "decision_commitment", "commitment_status",
        "intent", "target", "constraints", "risk", "required_capability", "authorization_level", "expiration_condition",
        "provenance", "action_request_candidate", "permission_candidate", "risk_review_candidate", "Action Boundary only",
        "commitment_output_is_action_request_candidate", "commitment_does_not_execute", "action_boundary_retains_permission",
        "action_boundary_retains_execution", "action_request_is_not_action_command", "unknowns_are_preserved"
    ],
    "decision_conflict_contract_v1.json": [
        "Decision Conflict Contract v1", "Decision Commitment Conflict Candidate", "Intent Conflict", "Goal Conflict",
        "Value Conflict", "Role Conflict", "Resource Conflict", "Time Conflict", "commitment_candidates", "decision_candidates",
        "field_context", "intent_context", "goal_context", "value_constraints", "resource_constraints", "time_constraints",
        "unknowns", "provenance", "conflict_candidate", "brain_review_requirement", "human_override_requirement", "resolution_status",
        "conflict_is_preserved", "conflict_is_not_silently_resolved", "conflict_does_not_make_decision",
        "conflict_does_not_execute_action", "unknowns_are_preserved"
    ],
    "decision_revision_contract_v1.json": [
        "Decision Revision Contract v1", "Decision Commitment Revision Loop", "decision_candidate", "commitment_reference", "feedback",
        "outcome_evidence", "reality_change", "expectation_difference", "capability_constraint", "unknowns", "provenance",
        "Decision Candidate", "Commitment", "Feedback", "Revision Candidate", "New Commitment", "revision_candidate",
        "new_decision_candidate", "new_commitment_candidate", "invalidated_commitment", "revision_is_candidate_based",
        "revision_does_not_execute_action", "revision_does_not_modify_value", "revision_does_not_modify_goal", "unknowns_are_preserved"
    ],
    "decision_lifecycle_contract_v1.json": [
        "Decision Lifecycle Contract v1", "Decision Commitment Lifecycle", "Created", "Candidate", "Reviewing", "Committed",
        "Executing Preparation", "Invalidated", "Expired", "Archived", "Created → Candidate", "Candidate → Reviewing",
        "Reviewing → Committed", "Committed → Executing Preparation", "Reviewing → Invalidated", "Committed → Invalidated",
        "Executing Preparation → Invalidated", "Committed → Expired", "Invalidated → Archived", "Expired → Archived",
        "candidate_based", "reality_freshness_required", "evidence_sufficiency_required", "constraint_check_required",
        "intent_alignment_required", "capability_availability_check_required", "human_override_supported", "provenance_preserved",
        "lifecycle_does_not_execute_action", "lifecycle_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "decision_governance_contract_v1.json": [
        "Decision Governance Contract v1", "Decision Commitment Admission and Authority Governance", "Reality Freshness Check",
        "Evidence Sufficiency Check", "Constraint Check", "Intent Alignment Check", "Capability Availability Check", "Constitution",
        "Value", "Safety", "Governance", "Expectation", "Expiration", "Human Override", "Unknown", "Risk", "Provenance", "brain",
        "commitment", "attention", "capability", "expectation", "memory", "learning", "action_boundary", "commitment_is_not_action",
        "commitment_does_not_execute", "no_action_execution", "no_hardware_control", "no_model_runtime", "no_automatic_planning",
        "no_automatic_execution", "no_automatic_value_modification", "no_automatic_goal_modification", "no_b_simulation_runtime",
        "no_prediction_runtime", "no_capability_invocation", "no_model_calls", "no_hardware_calls", "no_silent_conflict_resolution",
        "unknowns_are_preserved", "constitution_review_required", "protocol_version_required", "action_boundary_review_required"
    ]
}


def main() -> int:
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
