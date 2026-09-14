#!/usr/bin/env python3
"""V2 final verifier for Cognitive System Integration Readiness architecture.

This verifier only checks the declared planning contracts. It does not execute
Runtime, models, devices, network calls, or Action.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "luna_cognitive_operating_model_v1.md": [
        "planning-only integration blueprint", "Cognitive Constitution", "Brain owns Goal", "final Judgment",
        "Runtime owns cycle progression", "Runtime is not a cognitive subject", "Global Cognitive Loop",
        "External World", "Reality Update", "Field Update", "Attention Allocation", "Situation Update",
        "Goal / Task Check", "Decision Candidate", "Action Boundary", "Outcome", "Experience", "Future Adaptation",
        "Evidence", "Reality Reducer", "does not interpret goals", "global resource bus", "Reality Observation",
        "Brain Escalation", "Capability Usage", "Situation Candidate", "Goal and Task continuity", "A Route",
        "Options", "Evaluation Candidates", "Brain retains final cognitive judgment", "Action Request",
        "Action Runtime", "Outcome Evidence", "Cause Attribution", "Capability Governance", "Need to Capability",
        "Model Manager", "Hardware Registry", "Provider output is Raw Evidence Candidate", "Evidence Gateway",
        "Protocol", "Authority", "Admission", "Resource", "Diagnostics", "Created", "Activated", "Running",
        "Background", "Suspended", "Completed", "Archived", "24 hours", "7 days", "30 days", "Unknown",
        "No real Model", "No Camera", "No OCR", "No SLAM", "No Hardware Runtime", "No Action Runtime",
        "No Emotion Runtime", "No Social Runtime", "No B Runtime", "No Scheduler implementation", "No automatic execution",
        "No automatic model switching", "No automatic learning"
    ],
    "long_term_stability_validation_v1.md": [
        "24 hours", "7 days", "30 days", "Runtime Execution", "Day 1", "Day 7", "Day 30", "Unknown",
        "Identity", "Constitution", "core Capability", "Field", "Attention", "Task", "Self State",
        "Experience Candidates", "anomaly reactivation", "State growth is bounded", "No long-running implementation",
        "No Scheduler", "No model call", "No hardware call", "No action"
    ],
    "failure_recovery_model_v1.md": [
        "Model Unavailable", "Hardware Degraded", "Network Disconnected", "Information Conflict", "Invalid Evidence",
        "Timeout", "Resource Denied", "Protocol Error", "Unknown Failure", "Failure", "Diagnostics", "Classification",
        "Fallback Candidate", "Capability Update", "does not directly change Goal", "does not directly change Decision",
        "does not directly change Reality", "does not directly change Identity", "Evidence Gateway", "Conflict Candidate",
        "automatic model switching", "No real recovery Runtime", "No Scheduler", "No Provider", "No Camera", "No OCR",
        "No SLAM", "No Hardware", "No Action", "No Emotion", "No Social", "No B"
    ],
    "luna_system_whitebox_v1.md": [
        "External World", "Evidence", "Reality Workspace", "Reducer", "Cognitive Field", "Attention Global Bus",
        "Situation", "Goal / Task Check", "A Route", "Option", "Decision Candidate", "Brain Review", "Action Boundary",
        "Outcome Evidence", "Experience Candidate", "Who creates a Field", "Brain Intent", "Neural Detection",
        "User Request", "External Event", "never a Provider", "Who approves activation", "Governance Admission",
        "Who modifies Reality", "Reality Reducer", "Who owns Goal and final Decision", "Who allocates finite resources",
        "Who observes health", "Who may revoke", "Capability → Model / Hardware → Evidence", "Model → Decision",
        "Model → Goal", "Model → Action", "Provider → Brain", "Runtime → Judgment", "Planning Only architecture artifact",
        "No Runtime", "No Scheduler", "No Model", "No Hardware", "No Camera", "No OCR", "No SLAM", "No Action",
        "No Emotion", "No Social", "No B"
    ],
    "luna_system_go_no_go_v1.md": [
        "Global Cognitive Loop", "External World", "Reality Update", "Field Update", "Attention Allocation",
        "Situation Update", "Goal / Task Check", "Decision Candidate", "Action Boundary", "Outcome", "Experience",
        "Future Adaptation", "Cognitive Process lifecycle", "Created", "Activated", "Running", "Background",
        "Suspended", "Completed", "Archived", "Attention Global Bus", "Reality Observation", "Brain Escalation",
        "Capability Usage", "Need → Capability → Model / Hardware → Evidence", "Protocol", "Authority", "Admission",
        "Resource", "Runtime", "Diagnostics", "24 hours", "7 days", "30 days", "Model Unavailable", "Hardware Degraded",
        "Network Disconnected", "Information Conflict", "Reality Reducer remains the sole Reality mutation authority",
        "Brain retains Goal and final Decision authority", "No real models", "No Camera", "No OCR", "No SLAM",
        "No Hardware Runtime", "No Action Runtime", "No Emotion Runtime", "No Social Runtime", "No B Runtime",
        "No Scheduler implementation", "No automatic execution", "Provider-to-Decision", "Model-to-Goal", "Model-to-Action",
        "direct Reality mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "global_cognitive_loop_contract_v1.json": [
        "Global Cognitive Loop Contract v1", "Planning Only", "External World", "Reality Update", "Field Update",
        "Attention Allocation", "Situation Update", "Goal / Task Check", "Decision Candidate", "Action Boundary",
        "Outcome", "Experience", "Future Adaptation", "external_world_enters_as_evidence", "reality_reducer_required",
        "decision_is_candidate_until_brain_review", "action_boundary_is_not_action_runtime", "outcome_returns_as_evidence",
        "future_adaptation_requires_validation", "unknown_preserved", "no_direct_model_to_decision", "no_direct_model_to_goal",
        "no_direct_model_to_action", "no_direct_provider_to_brain", "no_direct_reality_mutation", "no_runtime_implementation",
        "no_scheduler_implementation", "no_automatic_execution"
    ],
    "module_interaction_matrix_v1.json": [
        "Module Interaction Matrix v1", "Reality Workspace", "facts", "provenance", "Unknown", "Cognitive Field",
        "relevant context", "Attention", "global resource allocation candidates", "Reality Observation", "Field Update",
        "Brain Escalation", "Capability Usage", "Situation", "Situation Candidate", "Goal / Task", "Task continuity",
        "A Route", "Option", "Decision Candidate", "Brain", "final Judgment", "Capability Governance", "Evidence",
        "Experience", "Experience Candidate", "Governance", "Protocol", "Authority", "Admission", "Resource", "Runtime",
        "Diagnostics", "reality_reducer_is_sole_reality_mutation_authority", "brain_retains_final_decision_authority",
        "provider_cannot_create_field", "model_cannot_modify_goal", "unknowns_are_preserved"
    ],
    "attention_global_bus_contract_v1.json": [
        "Attention Global Bus Contract v1", "global finite cognitive resource allocation", "Reality Observation",
        "Field Update", "Task", "Brain Escalation", "Capability Usage", "Attention Allocation Candidate",
        "Observation Requirement", "Brain Escalation Candidate", "Resource Reallocation Candidate", "source", "Field",
        "Goal", "Task", "risk", "information value", "uncertainty", "resource cost", "provenance",
        "integrates_reality_observation", "integrates_field_update", "integrates_task", "integrates_brain_escalation",
        "integrates_capability_usage", "attention_does_not_own_goal", "attention_does_not_own_decision",
        "attention_does_not_mutate_reality", "attention_does_not_execute_action", "preemption_requires_arbitration",
        "release_requires_lifecycle_evidence", "unknowns_are_preserved"
    ],
    "runtime_process_lifecycle_v1.json": [
        "Runtime Process Lifecycle v1", "Created", "Activated", "Running", "Background", "Suspended", "Completed",
        "Archived", "Survival", "Foreground", "Maintenance", "process reference", "Field reference", "Goal reference",
        "Task reference", "resource candidate", "authority reference", "provenance", "runtime_kernel_owns_tick",
        "runtime_kernel_does_not_reason", "runtime_kernel_does_not_decide", "not_a_scheduler", "no_scheduler_implementation",
        "no_runtime_implementation", "no_automatic_execution", "unknowns_are_preserved"
    ],
    "capability_execution_flow_v1.json": [
        "Capability Execution Flow v1", "Need", "Capability", "Model/Hardware", "Evidence", "Field", "Attention",
        "Observation Requirement", "Task", "Situation", "Capability Governance", "Model Manager", "Hardware Registry",
        "Human Input", "Raw Evidence Candidate", "evidence_gateway_required", "reality_update_candidate_required",
        "reducer_required", "human_input_is_evidence_source", "model_is_not_cognitive_subject", "provider_cannot_create_field",
        "provider_cannot_create_decision", "provider_cannot_modify_reality", "capability_failure_returns_diagnostic_candidate",
        "hardware_degradation_returns_self_capability_candidate", "automatic_model_switching", "no_real_model", "no_camera",
        "no_ocr", "no_slam", "no_hardware_runtime", "no_action_runtime", "unknowns_are_preserved"
    ],
    "governance_interception_points_v1.json": [
        "Governance Interception Points v1", "Protocol", "Authority", "Admission", "Resource", "Runtime", "Diagnostics",
        "schema", "version", "compatibility", "owner", "permission", "scope", "identity", "capability", "boundary",
        "health", "compute", "energy", "memory", "latency", "network", "process lifecycle", "tick", "wake-up",
        "state synchronization", "failure classification", "provenance", "degradation", "unknown",
        "protocol_interception_required", "authority_interception_required", "admission_interception_required",
        "resource_interception_required", "runtime_interception_required", "diagnostics_interception_required",
        "diagnostics_emits_candidate_not_action", "governance_does_not_make_decision", "governance_does_not_modify_reality",
        "Draft", "Review", "Active", "Deprecated", "Archived", "unknowns_are_preserved"
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
