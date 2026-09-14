#!/usr/bin/env python3
"""V2 static verifier for Goal/Task/Temporal Continuity architecture.

This file is executed by User Terminal for the final phase verification. The
Agent only performs equivalent V0 parsing and compilation checks.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_goal_model_v1.md": [
        "Goal", "Long Term Goal", "Current Goal", "Task Goal", "Brain Goal",
        "Cognitive Goal", "Goal hierarchy", "Intent", "Value", "Goal authority",
        "Field transition", "Goal Reassessment Candidate", "completion condition",
        "Abandonment", "Suspension", "unknowns", "automatic planning",
        "autonomous Goal creation", "Goal mutation", "Action execution",
        "does not modify Reality", "does not modify Self Identity"
    ],
    "cognitive_task_model_v1.md": [
        "Task as a cognitive process", "Cognitive Process", "Todo List", "Action Command",
        "second cognitive subject", "origin_field_reference", "goal_reference",
        "lifecycle_state", "constraints", "progress evidence", "completion condition",
        "pending_information", "next_requirement_candidate", "interruption context",
        "resume conditions", "Background", "Suspended", "Resumed", "Completed",
        "Abandoned", "Expired", "Reducer remains the sole State mutation authority",
        "Task state does not directly mutate Reality", "automatic planning", "automatic execution",
        "Provider Goal mutation"
    ],
    "temporal_continuity_model_v1.md": [
        "Temporal Continuity", "Active", "Suspended", "Resumed", "Completed", "Abandoned",
        "Expired", "scheduler", "planner", "Action Runtime", "identity", "constraints",
        "pending information", "unknowns", "Reality", "Evidence", "Field", "Cross-day",
        "cross-field", "Temporal memory boundary", "unfinished Goals and Tasks",
        "validity intervals", "completion/outcome evidence", "validated Experience candidates",
        "Unknown remains Unknown", "automatic planning", "automatic execution", "online learning"
    ],
    "task_brain_boundary_v1.md": [
        "Brain owns Intent", "Value", "long-term Goal", "current Goal", "final judgment",
        "authorization", "Task manages continuity", "lifecycle state", "progress evidence",
        "pending information", "resume candidates", "second Brain", "modify Goal", "modify Value",
        "modify Decision", "modify Reality", "Self Identity", "Action Policy", "execute Action",
        "authorize external operations", "Task candidate", "Conflict Candidate", "Field transition",
        "Runtime owns only lifecycle mechanics", "Reducer remains the sole State mutation authority",
        "Provider", "Capability", "Goal authority", "Task authority", "Decision authority",
        "No automatic planning", "No automatic execution", "No Emotion", "No Role", "No B Route"
    ],
    "task_experience_boundary_v1.md": [
        "Experience Candidate", "task context", "Decision reference", "Action Boundary reference",
        "Outcome Evidence", "Cause Attribution", "adaptation candidate", "Reality",
        "One failed task", "Goal", "Self Identity", "Capability", "Decision Policy",
        "Repeated outcomes", "Pattern Candidate", "validation", "provenance", "confidence",
        "time decay", "successful outcome", "risky strategy", "Attention", "Option",
        "Capability awareness", "Unknowns", "automatic learning", "model training",
        "automatic planning"
    ],
    "temporal_continuity_whitebox_v1.md": [
        "Brain Intent / Goal", "Goal Hierarchy", "Field-bound Task Process", "Task Lifecycle State",
        "Attention", "Situation", "Decision", "Action Boundary", "Outcome Evidence",
        "Experience Candidate", "Suspend", "Resume", "Complete", "goal_reference", "task_id",
        "field_reference", "lifecycle state", "pending_information", "next_requirement",
        "completion_condition", "interruption context", "resume evidence", "provenance",
        "confidence", "unknowns", "Reality", "Reducer", "sole State mutation authority",
        "not a Scheduler", "not automatic planning", "not automatic execution", "No Runtime",
        "No hardware control", "No external system operation", "No B Route", "No online learning"
    ],
    "temporal_continuity_go_no_go_v1.md": [
        "Goal hierarchy", "Long Term", "Current", "Task Goal", "Field-bound Cognitive Process",
        "not a Todo List", "Created", "Active", "Background", "Suspended", "Resumed",
        "Completed", "Abandoned", "Expired", "cross-day continuity", "Field transitions",
        "Goal mutation", "context pollution", "Reality confirmation", "Field confirmation",
        "Self State reassessment", "outcome evidence", "Attention", "Brain retains Goal",
        "Experience", "current Reality", "Reducer remains the sole State mutation authority",
        "No automatic planning", "No automatic execution", "No Action Runtime", "No hardware",
        "No external system operation", "No Emotion Runtime", "No Role Runtime", "No Social Runtime",
        "No B Route", "No Simulation", "No online learning", "No direct Reality mutation",
        "No direct Goal mutation", "No direct Decision mutation", "No second cognitive subject",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "goal_hierarchy_schema_v1.json": [
        "Goal Hierarchy Schema v1", "goal_id", "goal_type", "Long Term", "Current", "Task",
        "parent_goal_reference", "origin", "intent_reference", "field_reference", "constraints",
        "priority_candidate", "validity_interval", "status", "completion_condition", "provenance",
        "unknowns", "goal_is_not_task", "goal_is_not_action", "goal_does_not_modify_reality",
        "goal_does_not_execute", "brain_retains_goal_authority", "goal_revision_requires_review",
        "unknowns_are_preserved"
    ],
    "task_field_binding_contract_v1.json": [
        "Task Field Binding Contract v1", "task_id", "origin_field_reference", "current_field_reference",
        "goal_reference", "binding_mode", "Bound", "Following Transition", "Background", "Suspended",
        "field_transition_reference", "context_update_candidate", "confidentiality_boundary",
        "task_does_not_modify_reality", "field_does_not_modify_goal", "field_transition_does_not_delete_task",
        "reality_over_experience", "reducer_is_sole_state_mutation_authority", "unknowns_are_preserved"
    ],
    "task_lifecycle_schema_v1.json": [
        "Cognitive Task Lifecycle Schema v1", "Created", "Active", "Background", "Suspended", "Resumed",
        "Completed", "Abandoned", "Expired", "allowed_transitions", "transition_requires_candidate",
        "resume_requires_identity_continuity", "completion_requires_evidence", "abandonment_requires_review",
        "task_state_is_not_action_execution", "task_state_does_not_modify_goal", "task_state_does_not_modify_reality",
        "reducer_is_sole_state_mutation_authority"
    ],
    "task_resume_contract_v1.json": [
        "Task Resume Contract v1", "task_id", "prior_state", "resume_candidate", "resume_time",
        "preserved_goal_reference", "preserved_constraints", "pending_information", "unknowns",
        "current_reality_confirmation_required", "current_field_confirmation_required",
        "self_state_reassessment_required", "attention_allocation_candidate_required",
        "resume_does_not_execute_action", "resume_does_not_modify_goal", "resume_does_not_modify_reality",
        "reality_over_experience", "reducer_is_sole_state_mutation_authority"
    ],
    "task_attention_interface_v1.json": [
        "Task Attention Interface v1", "task_reference", "attention_request_candidate",
        "attention_resource_candidate", "suspension_candidate", "resume_candidate", "maintenance_candidate",
        "task_does_not_control_attention", "attention_does_not_modify_goal", "attention_does_not_decide_task",
        "attention_does_not_execute_action", "allocation_is_candidate_only", "resource_cost_is_explicit",
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
