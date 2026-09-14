#!/usr/bin/env python3
"""V2 final verifier for Cognitive Brain architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_brain_architecture_v1.md": [
        "Cognitive Brain Architecture v1", "Global Cognitive State", "Brain", "Decision Candidate", "Decision Boundary",
        "Action Boundary", "not a Large Language Model", "not Memory", "not Planner", "not an Action Executor",
        "not a Prediction Engine", "State Interpretation", "Current Cognitive Interpretation Candidate", "Situation Evaluation",
        "Situation Evaluation Candidate", "Intent Alignment", "Option Evaluation", "Conflict Evaluation", "Intent Conflict",
        "Goal Conflict", "Role Conflict", "Value Conflict", "Field Conflict", "Resource Conflict", "Decision Candidate Generation",
        "Brain Context Package", "Relevant Evidence", "Hypothesis Candidates", "Expectation Feedback", "Option Candidates",
        "Constraint Candidates", "does not directly access Camera", "Model", "Hardware", "Database", "State Understanding",
        "Intent Alignment", "Option Evaluation", "Conflict Analysis", "Decision Trace", "Attention does not belong to Brain",
        "Attention Requirement", "Need More Evidence", "Attention retains resource allocation", "Brain evaluates Hypothesis Candidates",
        "Expectation Feedback", "Value supplies constraints", "Brain does not create Value", "Drive supplies motivation influence",
        "Learning supplies Experience Candidate", "Strategy Candidate", "Pattern Candidate", "Decision Trace", "Unknown",
        "Provenance", "Created", "Context Loaded", "Evaluation", "Candidate Generated", "Reviewed", "Completed", "Archived",
        "Alternative Evaluation", "B Simulation Runtime", "LLM integration", "automatic reasoning Runtime", "Action execution",
        "automatic planning", "Prediction", "World Model", "automatic learning", "model training", "hardware calls",
        "Action Runtime", "does not mutate any source state"
    ],
    "brain_whitebox_v1.md": [
        "Who supplies Brain input", "Who owns Reality", "Who owns Field, Self, Memory, Goal, and Attention", "Who evaluates Situation and Options",
        "Who owns Value", "Who owns Drive", "Who owns final Decision authority", "Who executes Action", "Global Cognitive State + Evidence + Hypothesis + Expectation Feedback",
        "Brain Context Package", "State Interpretation", "Situation Evaluation", "Intent Alignment", "Option Evaluation", "Conflict Analysis",
        "Decision Candidate", "Decision Trace", "Brain → Reality mutation", "Brain → Field mutation", "Brain → Memory ownership",
        "Brain → Goal mutation", "Brain → Attention allocation", "Brain → Hypothesis or Belief resolution", "Brain → Expectation update",
        "Brain → Decision", "Brain → Action", "Brain → Prediction Runtime", "Brain → World Model", "Brain → B Simulation Runtime",
        "Brain → automatic learning", "Value remains a constraint", "Unknown", "Risk", "Constraint", "Confidence", "Provenance"
    ],
    "brain_go_no_go_v1.md": [
        "Brain", "cognitive evaluation center", "Brain Context Package", "State Interpretation", "Situation Evaluation", "Intent Alignment",
        "Option Evaluation", "Conflict Analysis", "Decision Candidate Generation", "Decision Trace", "Value remains a constraint",
        "Drive remains an influence", "Learning and Memory provide candidates", "Attention retains resource allocation", "Unknown",
        "Risk", "Conflict", "Confidence", "Provenance", "Decision Candidate", "Action Boundary", "B Route", "interface placeholder",
        "No LLM integration", "No automatic reasoning Runtime", "No Action execution", "No automatic planning", "No Prediction",
        "No World Model", "No B Simulation Runtime", "No automatic learning", "No model training", "No hardware calls", "No Action Runtime",
        "No Reality", "Field", "Memory", "Goal", "Identity", "Attention", "Value mutation", "V0 static checks", "V1",
        "V2 Final Phase Verification", "User Terminal Only", "V3", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "brain_context_package_schema_v1.json": [
        "Brain Context Package Schema v1", "Brain Context Package", "global_cognitive_state", "relevant_evidence", "hypothesis_candidates",
        "expectation_feedback", "option_candidates", "constraint_candidates", "intent_context", "goal_context", "task_context", "risk",
        "unknowns", "conflicts", "confidence", "provenance", "brain_does_not_access_camera", "brain_does_not_access_model",
        "brain_does_not_access_hardware", "brain_does_not_access_database", "brain_does_not_make_action", "unknowns_are_preserved"
    ],
    "brain_processing_flow_v1.json": [
        "Brain Processing Flow v1", "Brain Cognitive Flow", "State Understanding", "Situation Evaluation", "Intent Alignment",
        "Option Evaluation", "Conflict Analysis", "Decision Candidate", "Decision Trace", "Current Cognitive Interpretation Candidate",
        "Situation Evaluation Candidate", "Intent Alignment Candidate", "Option Evaluation Candidate", "Conflict Evaluation Candidate",
        "candidate_based", "unknowns_are_preserved", "flow_does_not_execute_action", "flow_does_not_make_reality"
    ],
    "brain_state_interpretation_contract_v1.json": [
        "Brain State Interpretation Contract v1", "State Interpretation", "global_cognitive_state", "relevant_evidence", "hypothesis_candidates",
        "belief_candidates", "expectation_feedback", "unknowns", "provenance", "current_cognitive_interpretation_candidate", "field_summary",
        "self_summary", "task_summary", "risk_summary", "unknown_summary", "interpretation_does_not_modify_reality",
        "interpretation_does_not_modify_field", "interpretation_does_not_modify_self", "interpretation_does_not_make_decision", "unknowns_are_preserved"
    ],
    "brain_situation_evaluation_contract_v1.json": [
        "Brain Situation Evaluation Contract v1", "Situation Evaluation Candidate", "situation_reference", "global_cognitive_state",
        "interpretation_candidate", "evidence", "hypothesis_candidates", "expectation_feedback", "risk", "unknowns", "provenance",
        "situation_evaluation_candidate", "relevance", "risk_assessment", "confidence", "information_gap", "evaluation_does_not_replace_situation",
        "evaluation_does_not_modify_reality", "evaluation_does_not_make_decision", "unknowns_are_preserved"
    ],
    "brain_intent_alignment_contract_v1.json": [
        "Brain Intent Alignment Contract v1", "Intent Alignment Candidate", "intent_state", "goal_state", "task_state", "option_candidate",
        "global_cognitive_state", "drive_influence", "value_constraints", "unknowns", "provenance", "alignment_status", "alignment_candidate",
        "deviation_reason", "clarification_request", "intent_is_not_decision", "alignment_does_not_modify_intent", "alignment_does_not_modify_goal",
        "alignment_does_not_modify_value", "unknowns_are_preserved"
    ],
    "brain_option_evaluation_contract_v1.json": [
        "Brain Option Evaluation Contract v1", "Option Evaluation Candidate", "option_candidates", "global_cognitive_state", "situation_evaluation",
        "intent_alignment", "value_constraints", "drive_influence", "capability_state", "unknowns", "provenance", "option_evaluation_candidates",
        "tradeoffs", "risk_candidates", "resource_cost_candidates", "confidence", "constraint_fit", "evaluation_is_not_action",
        "evaluation_does_not_execute", "evaluation_does_not_modify_option_owner", "evaluation_does_not_make_final_decision", "unknowns_are_preserved"
    ],
    "brain_conflict_evaluation_contract_v1.json": [
        "Brain Conflict Evaluation Contract v1", "Conflict Evaluation Candidate", "Intent Conflict", "Goal Conflict", "Role Conflict",
        "Value Conflict", "Field Conflict", "Resource Conflict", "global_cognitive_state", "conflicts", "options", "value_constraints",
        "risk", "unknowns", "provenance", "conflict_evaluation_candidate", "tradeoffs", "priority_candidate", "more_information_request",
        "defer_candidate", "conflict_is_not_automatically_resolved", "conflict_does_not_make_decision", "conflict_does_not_modify_value",
        "conflict_does_not_modify_goal", "unknowns_are_preserved"
    ],
    "brain_decision_candidate_schema_v1.json": [
        "Brain Decision Candidate Schema v1", "Decision Candidate", "decision_candidate_id", "brain_context_reference", "global_state_snapshot_reference",
        "situation_evaluation", "intent_alignment", "option_evaluation", "selected_option_candidate", "alternative_options", "value_constraints",
        "drive_influence", "risk", "unknowns", "conflicts", "confidence", "required_capability_candidate", "decision_trace_reference",
        "provenance", "status", "decision_candidate_is_not_action", "decision_candidate_is_not_command", "decision_candidate_does_not_execute",
        "decision_boundary_retains_authority", "unknowns_are_preserved"
    ],
    "brain_decision_trace_schema_v1.json": [
        "Brain Decision Trace Schema v1", "Decision Trace", "trace_id", "global_cognitive_state_snapshot", "relevant_evidence", "field_context",
        "role_context", "relationship_context", "self_context", "intent_context", "goal_context", "task_context", "option_candidates", "tradeoffs",
        "value_constraints", "drive_influence", "hypothesis_candidates", "belief_candidates", "expectation_feedback", "unknowns", "risks",
        "conflicts", "confidence", "rationale_candidate", "rejected_alternatives", "provenance", "trace_is_explanation_not_command",
        "trace_does_not_modify_reality", "unknowns_are_preserved"
    ],
    "brain_attention_interface_v1.json": [
        "Brain Attention Interface v1", "Brain Attention Requirement", "brain_context", "information_gap", "unknowns", "risk", "provenance",
        "attention_requirement", "need_more_evidence", "observation_requirement", "discriminating_targets", "resource_cost_candidate",
        "brain_does_not_allocate_attention", "brain_does_not_arbitrate_attention", "attention_retains_resource_management",
        "brain_request_is_candidate_only", "unknowns_are_preserved"
    ],
    "brain_hypothesis_interface_v1.json": [
        "Brain Hypothesis Interface v1", "Brain Hypothesis Evaluation", "hypothesis_candidates", "supporting_evidence", "contradicting_evidence",
        "field_context", "situation_context", "confidence", "unknowns", "provenance", "hypothesis_evaluation_candidate", "validation_requirement",
        "more_evidence_request", "conflict_reference", "brain_does_not_create_fact", "brain_does_not_solidify_belief_automatically",
        "hypothesis_remains_candidate", "reality_and_evidence_remain_authoritative", "unknowns_are_preserved"
    ],
    "brain_expectation_interface_v1.json": [
        "Brain Expectation Interface v1", "Brain Expectation Feedback Evaluation", "expectation_candidates", "feedback_status", "expectation_differences",
        "current_reality", "hypothesis_context", "belief_context", "unknowns", "provenance", "expectation_evaluation_candidate",
        "option_weight_adjustment_candidate", "more_observation_request", "learning_input_candidate", "feedback_informs_brain",
        "brain_does_not_modify_expectation_automatically", "brain_does_not_modify_belief_automatically", "current_reality_overrides_stale_belief",
        "unknowns_are_preserved"
    ],
    "brain_memory_interface_v1.json": [
        "Brain Memory Interface v1", "Brain Relevant Memory Context", "memory_candidates", "current_field", "current_situation", "current_task",
        "attention_context", "provenance", "unknowns", "memory_context", "experience_relevance_candidate", "pattern_reference", "memory_conflict_candidate",
        "brain_does_not_own_memory", "memory_is_context_not_fact_override", "memory_does_not_make_decision", "brain_does_not_modify_memory_automatically",
        "unknowns_are_preserved"
    ],
    "brain_learning_interface_v1.json": [
        "Brain Learning Interface v1", "Brain Learning Candidate Input", "experience_candidates", "strategy_candidates", "pattern_candidates",
        "feedback_candidates", "capability_learning_candidates", "global_cognitive_state", "provenance", "unknowns", "learning_relevance_candidate",
        "strategy_evaluation_candidate", "future_adjustment_candidate", "brain_review_reference", "learning_does_not_modify_brain",
        "learning_does_not_make_decision", "learning_does_not_change_goal_automatically", "learning_is_input_candidate", "unknowns_are_preserved"
    ],
    "brain_value_constraint_interface_v1.json": [
        "Brain Value Constraint Interface v1", "Value Constraint for Brain Evaluation", "value_state", "value_constraints", "priority_candidates",
        "global_cognitive_state", "unknowns", "provenance", "constraint_package", "option_constraint_fit_candidate", "value_conflict_candidate",
        "value_is_constraint", "brain_does_not_create_value", "brain_does_not_modify_value", "value_does_not_make_decision", "unknowns_are_preserved"
    ],
    "brain_b_route_placeholder_v1.json": [
        "Brain B Route Placeholder v1", "Alternative Evaluation Interface Placeholder", "global_cognitive_state_snapshot", "decision_candidate",
        "alternative_variable_candidate", "provenance", "alternative_evaluation_candidate", "simulation_state_reference", "comparison_candidate",
        "b_route_is_interface_placeholder", "no_b_simulation_runtime", "placeholder_does_not_mutate_live_state", "placeholder_does_not_make_decision",
        "placeholder_does_not_execute_action", "unknowns_are_preserved"
    ],
    "brain_lifecycle_contract_v1.json": [
        "Brain Lifecycle Contract v1", "Brain Cognitive Evaluation Lifecycle", "Created", "Context Loaded", "Evaluation", "Candidate Generated",
        "Reviewed", "Completed", "Archived", "Created → Context Loaded", "Context Loaded → Evaluation", "Evaluation → Candidate Generated",
        "Candidate Generated → Reviewed", "Reviewed → Completed", "Completed → Archived", "candidate_based", "context_package_required",
        "decision_trace_required", "provenance_preserved", "lifecycle_does_not_execute_action", "lifecycle_does_not_modify_reality",
        "unknowns_are_preserved"
    ],
    "brain_governance_contract_v1.json": [
        "Brain Governance Contract v1", "Brain Admission and Authority Governance", "Global Cognitive State package", "Relevant Evidence",
        "Hypothesis Candidates", "Expectation Feedback", "Option Candidates", "Constraint Candidates", "Intent alignment", "Value constraints",
        "Drive influence", "Unknown", "Risk", "Conflict", "Confidence", "Provenance", "reality", "field", "self", "memory", "attention",
        "value", "drive", "learning", "brain", "decision_boundary", "action_boundary", "brain_does_not_replace_reality",
        "brain_does_not_modify_field", "brain_does_not_own_memory", "brain_does_not_own_goal", "brain_does_not_execute_action",
        "brain_does_not_access_camera", "brain_does_not_access_model", "brain_does_not_access_hardware", "brain_does_not_access_database",
        "brain_does_not_run_prediction", "brain_does_not_run_world_model", "brain_does_not_run_b_simulation", "brain_does_not_run_automatic_learning",
        "brain_does_not_bypass_attention", "brain_does_not_bypass_governance", "decision_candidate_is_not_action", "unknowns_are_preserved",
        "constitution_review_required", "protocol_version_required", "decision_boundary_review_required", "action_boundary_review_required"
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
