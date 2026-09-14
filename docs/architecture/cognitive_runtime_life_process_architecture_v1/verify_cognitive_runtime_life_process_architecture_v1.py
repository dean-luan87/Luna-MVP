#!/usr/bin/env python3
"""V2 final verifier for Cognitive Runtime Life Process architecture contracts."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_runtime_life_process_architecture_v1.md": [
        "Cognitive Runtime", "lifecycle plane", "Cognitive Core", "Tick", "Wake-up", "process states", "Workspace refresh", "resource allocation",
        "escalation", "not Brain", "does not own Goal", "Reasoning", "Decision", "Action", "External Change → Tick → Wake-up Evaluation",
        "Process Scheduling", "Field / Workspace / Attention Refresh", "Brain Invocation Boundary", "State Synchronization", "Lifecycle Manager",
        "Tick Manager", "Wake-up Manager", "Process Scheduler", "Workspace Manager", "Attention Scheduler", "Memory Maintenance", "Learning Scheduler",
        "Reflex Monitor", "Survival", "Foreground", "Background", "Maintenance", "Reality Change", "Field Change", "Attention Trigger", "Reflex Signal",
        "Task Deadline", "Cognitive Tick", "High Frequency", "Normal Cadence", "Low Frequency", "Memory Maintenance", "Learning evaluation",
        "compute", "energy", "memory", "time", "sensor availability", "State Synchronization", "Unknown", "conflict", "high-risk", "high-cost",
        "Failure → Diagnostics → Fallback Candidate → Escalation", "No real Scheduler", "Runtime loop", "model call", "Hardware Runtime",
        "Action Runtime", "B Simulation", "automatic Learning execution"
    ],
    "runtime_whitebox_v1.md": [
        "Tick / Wake-up Sources", "Lifecycle Manager", "Process Scheduler", "Workspace Manager", "Attention Scheduler", "State Synchronization",
        "Brain Invocation Candidate", "Diagnostics", "Fallback", "Escalation", "Who advances time", "Tick Manager", "logical tick candidate",
        "Who wakes processes", "Wake-up Manager", "Who schedules processes", "Process Scheduler", "Who maintains Workspaces", "Who allocates scarce resources",
        "Attention and Resource Governance", "Who maintains Memory and Learning", "Who monitors Reflex", "Reflex Monitor", "Who invokes Brain",
        "Who owns final judgment", "Who owns Reality mutation", "Runtime → State Update Candidate", "Runtime → Wake-up Candidate", "Runtime → Allocation Candidate",
        "Runtime → Brain Invocation Candidate", "Runtime → Goal Mutation", "Runtime → Decision", "Runtime → Action", "Runtime → Model Call", "Runtime → Hardware Call",
        "Runtime → Automatic Learning", "Scheduler → Value Resolution", "Planning Only", "real Scheduler", "Runtime loop"
    ],
    "runtime_go_no_go_v1.md": [
        "lifecycle plane", "not Brain", "not Decision", "Tick", "Wake-up", "Process Scheduler", "Workspace Manager", "Attention Scheduler", "Maintenance",
        "Reflex Monitor", "Brain Invocation Boundary", "Reality Change", "Field Change", "Attention Trigger", "Reflex Signal", "Task Deadline",
        "Created", "Activated", "Running", "Background", "Suspended", "Completed", "Archived", "Resource constraints", "State Synchronization",
        "Unknown", "Conflict", "Risk", "high cost", "Diagnostics", "Fallback Candidate", "Escalation", "No real Scheduler", "No Runtime loop",
        "No model call", "No Hardware Runtime", "No Action Runtime", "No B Simulation", "No automatic Learning execution", "cannot modify Goal",
        "Decision", "Value", "Reality", "Identity", "Action", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "runtime_lifecycle_manager_contract_v1.json": [
        "Runtime Lifecycle Manager Contract v1", "Created", "Activated", "Running", "Background", "Suspended", "Completed", "Archived",
        "lifecycle_candidate", "Cognitive Runtime", "does_not_make_decision", "does_not_modify_goal", "unknowns_are_preserved"
    ],
    "runtime_tick_manager_contract_v1.json": [
        "Runtime Tick Manager Contract v1", "Logical State Advance", "High Frequency", "Normal Cadence", "Low Frequency", "Safety", "Reflex",
        "Attention", "Field Refresh", "Memory Maintenance", "Learning Evaluation", "tick_is_not_wall_clock_promise", "tick_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "runtime_wakeup_manager_contract_v1.json": [
        "Runtime Wake-up Manager Contract v1", "Reality Change", "Field Change", "Attention Trigger", "Reflex Signal", "Task Deadline",
        "wake_up_candidate", "target_process", "priority_candidate", "wake_up_does_not_make_decision", "wake_up_does_not_execute_action",
        "unknowns_are_preserved"
    ],
    "runtime_process_scheduler_contract_v1.json": [
        "Runtime Process Scheduler Contract v1", "Survival", "Foreground", "Background", "Maintenance", "process_request", "allocation_candidate",
        "suspension_candidate", "resume_candidate", "scheduler_does_not_choose_goal", "scheduler_does_not_resolve_value_conflict",
        "scheduler_does_not_make_decision", "unknowns_are_preserved"
    ],
    "runtime_workspace_manager_contract_v1.json": [
        "Runtime Workspace Manager Contract v1", "primary_workspace", "background_workspaces", "refresh_candidate", "field_context", "attention_state",
        "workspace_manager_only_refreshes_context", "workspace_manager_does_not_become_brain", "workspace_manager_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "runtime_attention_scheduler_contract_v1.json": [
        "Runtime Attention Scheduler Contract v1", "attention_request", "attention_allocation_candidate", "resource_constraint", "field_context",
        "task_context", "risk", "attention_governance_owns_policy", "runtime_does_not_allocate_attention_directly", "unknowns_are_preserved"
    ],
    "runtime_memory_maintenance_contract_v1.json": [
        "Runtime Memory Maintenance Contract v1", "maintenance_request", "retrieval_candidate", "consolidation_candidate", "decay_review_candidate",
        "memory_reference", "maintenance_does_not_rewrite_memory", "maintenance_does_not_override_reality", "unknowns_are_preserved"
    ],
    "runtime_learning_scheduler_contract_v1.json": [
        "Runtime Learning Scheduler Contract v1", "learning_request", "experience_reference", "pattern_evaluation_candidate", "adaptation_candidate",
        "Low Frequency", "learning_scheduler_does_not_execute_automatic_learning", "learning_scheduler_does_not_modify_model", "unknowns_are_preserved"
    ],
    "runtime_reflex_monitor_contract_v1.json": [
        "Runtime Reflex Monitor Contract v1", "reflex_signal", "safety_candidate", "attention_boost_candidate", "brain_escalation_candidate",
        "High Frequency", "reflex_monitor_does_not_execute_action", "reflex_monitor_does_not_modify_safety_rules", "unknowns_are_preserved"
    ],
    "runtime_brain_invocation_boundary_v1.json": [
        "Runtime Brain Invocation Boundary v1", "invocation_candidate", "unknown_condition", "conflict_condition", "risk_condition", "high_cost_condition",
        "brain_input_package", "brain_retains_goal_authority", "brain_retains_value_authority", "brain_retains_reasoning_authority",
        "brain_retains_final_decision_authority", "runtime_does_not_say_what_to_choose", "unknowns_are_preserved"
    ],
    "runtime_resource_governance_contract_v1.json": [
        "Runtime Resource Governance Contract v1", "Compute", "Energy", "Memory", "Time", "Sensor Availability", "resource_request",
        "allocation_candidate", "degradation_candidate", "attention_owns_resource_policy", "governance_owns_permission", "runtime_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "runtime_state_sync_contract_v1.json": [
        "Runtime State Synchronization Contract v1", "Field", "Self", "Workspace", "Task", "Attention", "Memory", "Learning", "Reflex", "Emotion Context",
        "state_update_candidate", "source_provenance", "temporal_scope", "sync_preserves_boundaries", "sync_does_not_modify_identity",
        "sync_does_not_make_decision", "unknowns_are_preserved"
    ],
    "runtime_failure_escalation_contract_v1.json": [
        "Runtime Failure Escalation Contract v1", "Failure", "Diagnostics", "Fallback Candidate", "Escalation", "Capability Failure", "Stale State",
        "Resource Denial", "Malformed Context", "Process Starvation", "diagnostic_candidate", "fallback_candidate", "escalation_candidate",
        "failure_does_not_execute_action", "failure_does_not_make_decision", "unknowns_are_preserved"
    ],
    "runtime_scope_boundary_contract_v1.json": [
        "Runtime Scope Boundary Contract v1", "real_scheduler", "runtime_loop", "model_call", "hardware_runtime", "action_runtime", "b_simulation",
        "automatic_learning_execution", "runtime_does_not_modify_goal", "runtime_does_not_modify_decision", "runtime_does_not_modify_reality",
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
