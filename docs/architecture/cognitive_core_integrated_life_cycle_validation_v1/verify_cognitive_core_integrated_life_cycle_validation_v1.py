#!/usr/bin/env python3
"""V2 final verifier for Cognitive Core integrated lifecycle validation assets."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_core_integrated_lifecycle_model_v1.md": [
        "Integrated Life Cycle Validation", "architecture-level integration", "continuous time", "Field", "Role", "Relationship", "Self",
        "Attention", "Workspace", "Drive", "Value", "Brain", "Decision", "Action Boundary", "Experience", "Learning", "Reflex",
        "Emotion Context", "Reality Change → Field Update → Role Projection → Relationship Context", "Workspace Update", "Attention Arbitration",
        "Drive / Value Influence", "Brain Input Package", "Decision Candidate", "Experience Record", "Learning Candidate", "Future Adaptation",
        "Constitution", "Governance", "Field switch", "Home/Office", "Transit", "Multi-role composition", "Employee", "Organizer", "Friend",
        "Experience-to-attention", "Safety interruption", "Innate", "Emotion Context placeholder", "Unknown", "Conflict", "Confidence", "Provenance",
        "Self Identity", "Failure injection", "24-hour", "7-day", "30-day", "No fixture authorizes real Action", "model invocation", "hardware access",
        "automatic learning"
    ],
    "core_whitebox_v1.md": [
        "Reality Change", "Field / Role / Relationship", "Self Context", "Attention", "Workspace", "Drive / Value", "Brain Input Package",
        "Decision Candidate", "Action Boundary", "Experience", "Learning Candidate", "Future Attention", "Reflex Candidate", "Evidence", "Reducer",
        "Identity is continuous", "Goal and Decision", "Action remains an Action Boundary request", "Emotion Context remains metadata", "Unknown",
        "Conflict", "Model → Decision", "Emotion → Decision", "Learning → automatic strategy", "Reflex → automatic Action", "Workspace → Reality Write",
        "Field → Goal Mutation", "Role → Identity Mutation", "fixture → external side effect"
    ],
    "core_go_no_go_v1.md": [
        "Full Reality → Field → Role → Relationship → Workspace → Attention", "Drive/Value", "Brain", "Decision Candidate", "Action Boundary",
        "Outcome/Experience", "Learning Candidate", "Future Adaptation", "Field switch", "multi-role", "Learning→Attention", "Reflex interruption",
        "Emotion Context placeholder", "24-hour", "7-day", "30-day", "Failure injection", "Evidence", "Capability", "Task", "Goal", "Experience",
        "Reflex", "Emotion Context faults", "Unknown", "Conflict", "Confidence", "Provenance", "Self Identity continuity", "static",
        "No Emotion Runtime", "No B Runtime", "No automatic personality change", "No automatic Value modification", "No automatic learning", "No real Action",
        "No model call", "No hardware call", "No external side effect", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "cognitive_core_module_dependency_matrix_v1.json": [
        "Cognitive Core Module Dependency Matrix v1", "Reality", "Field", "Role", "Relationship", "Self", "Attention", "Workspace", "Drive",
        "Value", "Brain", "Decision", "Action Boundary", "Experience", "Learning", "Reflex", "Emotion Context", "no_reverse_authority",
        "Field→Decision", "Learning→Goal", "Emotion Context→Decision", "Model→Brain", "unknowns_are_preserved"
    ],
    "cognitive_core_information_flow_contract_v1.json": [
        "Cognitive Core Information Flow Contract v1", "Reality Change", "Field Update", "Role Projection", "Relationship Context", "Workspace Update",
        "Attention Arbitration", "Drive / Value Influence", "Brain Input Package", "Decision Candidate", "Action Boundary", "Experience Record",
        "Learning Candidate", "Future Adaptation", "Reality→Field", "Field→Role", "Role→Workspace", "Attention→Workspace", "Workspace→Brain",
        "Brain→Decision Candidate", "Action Boundary→Experience", "Experience→Learning", "Learning→Attention Candidate", "Model→Decision", "Emotion→Decision",
        "Learning→automatic strategy", "Reflex→automatic Action", "Workspace→Reality Write", "unknowns_are_preserved", "provenance_is_preserved"
    ],
    "cognitive_core_lifecycle_fixture_v1.json": [
        "Cognitive Core Lifecycle Fixture v1", "24-hour", "7-day", "30-day", "Reality Change", "Field Update", "Role Projection", "Relationship Context",
        "Workspace Update", "Attention Arbitration", "Drive / Value Influence", "Brain Input Package", "Decision Candidate", "Action Boundary",
        "Experience Record", "Learning Candidate", "Future Adaptation", "Family Field", "Family Member", "User Reminder", "Work Field", "Assistant",
        "Transit Field", "Navigation Assistant", "Social Field", "Friend", "static_fixture_only", "no_runtime", "unknowns_are_preserved"
    ],
    "field_role_workspace_trace_fixture_v1.json": [
        "Field Role Workspace Trace Fixture v1", "Office → Transit", "Office Field", "Transit Field", "Employee", "Navigation Assistant", "role_stack",
        "Organizer", "Friend", "workspace_refresh", "attention_shift", "identity_continuity", "action_boundary_only", "unknowns_are_preserved"
    ],
    "attention_learning_trace_fixture_v1.json": [
        "Attention Learning Trace Fixture v1", "Metro Field", "Exit direction", "High", "repeat_visit", "Exit sign location", "Field Pattern",
        "Prioritize exit signage", "validation", "learning_does_not_auto_update", "reality_priority", "unknowns_are_preserved"
    ],
    "reflex_interrupt_fixture_v1.json": [
        "Reflex Interrupt Fixture v1", "Navigation Field", "Route Support", "Active", "Reflex", "Sudden Danger", "Attention Boost", "Innate Reflex",
        "Brain Review Candidate", "action_execution", "Suspend Candidate", "unknowns_are_preserved"
    ],
    "emotion_context_boundary_fixture_v1.json": [
        "Emotion Context Boundary Fixture v1", "Historically Significant Field", "Companion", "Family Context", "memory_metadata", "Important Event",
        "emotion_metadata", "emotion_context_candidate", "decision_change", "emotion_computation", "emotion_expression", "unknowns_are_preserved"
    ],
    "brain_input_package_fixture_v1.json": [
        "Brain Input Package Fixture v1", "field_context", "role_context", "relationship_context", "self_context", "workspace_context", "attention_state",
        "drive_influence", "value_constraints", "unknowns", "risks", "memory_candidates", "emotion_context_candidate", "brain_retains_goal_authority",
        "brain_retains_final_decision_authority", "unknowns_are_preserved"
    ],
    "core_failure_injection_cases_v1.json": [
        "Core Failure Injection Cases v1", "Wrong Evidence", "Reality Conflict Candidate", "Capability Degradation", "Self Capability Candidate",
        "Task Interrupted", "Task Suspend / Resume Candidate", "Goal Conflict", "Brain Review Candidate", "Stale Experience", "Reality Priority",
        "Revocation Candidate", "Reflex Uncertainty", "Brain Escalation Candidate", "Malformed Emotion Context", "Placeholder Rejection Candidate",
        "no_real_action", "no_model_call", "no_hardware_call", "unknowns_are_preserved"
    ],
    "core_validation_metrics_v1.json": [
        "Core Validation Metrics v1", "information_flow_integrity", "authority_boundary_integrity", "field_role_continuity", "workspace_refresh_integrity",
        "attention_learning_linkage", "reflex_interrupt_integrity", "emotion_context_isolation", "unknown_retention", "provenance_retention",
        "self_identity_continuity", "failure_isolation", "longitudinal_stability", "Static Fixture Review", "runtime_execution", "model_execution",
        "action_execution", "unknowns_are_preserved"
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
