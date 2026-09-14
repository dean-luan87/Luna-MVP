#!/usr/bin/env python3
"""V2 static verifier for Cognitive System Runtime Orchestration."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_runtime_kernel_model_v1.md": [
        "Cognitive Runtime Kernel", "not Brain", "not a Scheduler", "World Event", "Reality Update Candidate",
        "Field Update Candidate", "Attention Allocation Candidate", "Observation", "Brain Evaluation",
        "Experience Update Candidate", "Cognitive Tick", "module wake-up", "state synchronization",
        "resource boundaries", "Reducer remains the sole State mutation authority", "does not modify Reality",
        "does not modify Goal", "No real Runtime", "No Scheduler implementation", "No Hardware Runtime", "No Action"
    ],
    "cognitive_process_lifecycle_model_v1.md": [
        "Cognitive Process", "Survival Process", "Foreground Process", "Background Process", "Maintenance Process",
        "Created", "Active", "Background", "Suspended", "Completed", "Archived", "intent reference",
        "resource request", "priority candidate", "not a person", "not Brain", "not a Decision", "not an Action"
    ],
    "module_wakeup_policy_v1.md": [
        "Reality Workspace", "resident", "Attention", "continuous governance", "Brain", "event-driven escalation",
        "Experience", "background", "Capability", "on-demand", "Neural", "fast stimulus", "Wake-up condition",
        "Execution Candidate", "not a Scheduler", "does not implement a Scheduler", "does not call models",
        "does not control Hardware", "does not execute Action"
    ],
    "background_cognitive_process_model_v1.md": [
        "Field Stability Monitor", "Capability Health", "Memory/Experience Maintenance", "Unknown Tracking",
        "Self Resource Awareness", "Diagnostic Candidate", "Stability Candidate", "Unknown Update Candidate",
        "Brain Escalation Candidate", "cannot choose a Goal", "cannot interpret Reality", "cannot execute Action",
        "cannot erase Unknown", "automatically learn"
    ],
    "brain_activation_boundary_v1.md": [
        "Brain Activation Candidate", "unresolved conflict", "high or persistent Unknown", "survival/risk escalation",
        "Intent drift", "Goal conflict", "resource trade-off", "repeated failure", "capability limitation",
        "Field transition", "Routine state refresh", "Brain Evaluation", "not a Decision", "Goal authority",
        "final Decision authority", "cannot activate Brain by changing its Goal"
    ],
    "runtime_resource_governance_model_v1.md": [
        "compute", "battery/energy", "time", "storage", "attention", "sensor/capability", "network", "memory",
        "Process Request", "Attention Priority", "Resource Allocation Candidate", "Execution Candidate",
        "Resource Constraint Candidate", "not a Scheduler", "does not implement a Scheduler", "does not call a model",
        "does not control Hardware", "does not execute Action", "preserves Unknown"
    ],
    "runtime_failure_escalation_model_v1.md": [
        "Failure", "Diagnostics", "Fallback Candidate", "Escalation Candidate", "Brain Evaluation",
        "Capability failure", "state synchronization conflict", "resource exhaustion", "stale Evidence",
        "process timeout", "wake-up rejection", "does not stop the entire cognitive system", "does not choose the fallback",
        "does not alter Goal", "does not modify Reality", "does not execute Action", "does not automatically learn"
    ],
    "runtime_whitebox_v1.md": [
        "World Event", "Reality Update", "Field Update", "Attention Reallocation", "Observation Candidate",
        "Cognition Candidate", "Brain Activation Candidate", "Brain Evaluation Candidate", "Experience Update Candidate",
        "Next Cognitive Tick", "Process Request", "Attention Priority", "Resource Allocation", "Neural Response Candidate",
        "Diagnostics", "Fallback Candidate", "Escalation Candidate", "Brain owns judgement", "Reducer remains the sole State mutation authority",
        "No Runtime", "No Scheduler implementation", "No Hardware", "No Action", "No Model", "No Emotion", "No Role", "No Social", "No B Simulation"
    ],
    "runtime_go_no_go_v1.md": [
        "Cognitive Runtime Kernel", "cycle references", "wake-up candidates", "state synchronization", "process lifecycle",
        "resource boundaries", "Survival", "Foreground", "Background", "Maintenance", "Created", "Active",
        "Suspended", "Completed", "Archived", "Cognitive Tick", "multi-frequency", "without implementing a Scheduler",
        "Module Wake-up Policy", "Field Stability", "Capability Health", "Unknown Tracking", "Brain Activation Candidate",
        "Conflict", "Unknown High", "Risk", "Intent/Goal conflict", "repeated failure", "Neural Fast Path",
        "Stimulus", "Neural Response Candidate", "Feedback", "State Synchronization", "Failure Escalation",
        "Reducer", "does not own cognition", "No real Runtime", "No Scheduler implementation", "No Hardware Runtime",
        "No Action", "No model call", "No Emotion", "No Role", "No Social Runtime", "No B Simulation",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "cognitive_runtime_tick_contract_v1.json": [
        "Cognitive Runtime Tick Contract", "tick_reference", "time_reference", "world_event", "reality_update_candidate",
        "Reality Update", "Field Update", "Attention Reallocation", "Observation Candidate", "Cognition Candidate",
        "Brain Evaluation Candidate", "Experience Update Candidate", "Next Cycle", "multi_frequency",
        "scheduler_implementation", "runtime_execution", "Reducer remains the sole State mutation authority"
    ],
    "neural_fast_path_contract_v1.json": [
        "Neural Fast Path Contract", "Stimulus", "Neural Response Candidate", "Feedback", "rapid risk signal",
        "health anomaly", "resource protection", "brain_required_for_fast_path", "fast_path_is_decision",
        "fast_path_is_action", "neural_changes_goal", "neural_modifies_reality", "hardware_runtime", "action_runtime"
    ],
    "cognitive_state_sync_contract_v1.json": [
        "Cognitive State Synchronization Contract", "Reality Update", "Field Update", "Attention Reallocation",
        "A Route Re-evaluation", "Brain Awareness Candidate", "state_version", "provenance", "timestamp",
        "confidence", "Conflict Candidate", "Stale Candidate", "cross_module_direct_mutation", "Reducer authority",
        "reality_over_experience"
    ],
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
