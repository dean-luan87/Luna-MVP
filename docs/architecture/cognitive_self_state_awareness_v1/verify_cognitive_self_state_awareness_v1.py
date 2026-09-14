#!/usr/bin/env python3
"""V2 static verifier for Cognitive Self State Awareness architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_self_state_model_v1.md": [
        "Self State Awareness", "Self Identity", "Self Capability", "Self State",
        "how Luna is currently doing", "not Self Identity", "not Personality", "not Emotion",
        "not a Goal", "not a Decision", "not Reality", "Physical State", "Cognitive State",
        "Capability State", "Resource State", "battery", "temperature", "sensor health", "storage",
        "network", "current load", "active Field count", "Attention consumption", "Unknown accumulation",
        "compute", "memory", "time", "Self State Update Candidate", "Reducer validation",
        "Attention Adjustment Candidate", "Brain Awareness Candidate", "Resource Protection Candidate",
        "Alternative Observation Candidate", "cannot directly modify Reality", "Goal", "Decision", "Action",
        "Self Identity", "Capability Identity", "Personality", "Emotion", "Reducer remains the sole State mutation authority",
        "No Emotion Runtime", "No Role Runtime", "No Social Runtime", "No B Runtime", "No Action Runtime"
    ],
    "self_identity_capability_state_boundary_v1.md": [
        "Three-layer Self model", "Identity", "Capability", "State", "stable Luna subject reference",
        "ability boundary", "current physical", "Self State is not Self Identity", "Self Capability is not Self State",
        "low battery", "high temperature", "high cognitive load", "network loss", "Authority table",
        "Reducer", "does not modify Reality", "Goal", "Decision", "Action", "Capability Identity",
        "Personality", "Emotion", "sole State mutation authority", "not ordinary Runtime input"
    ],
    "self_state_experience_boundary_v1.md": [
        "Self State Context", "Decision Context", "Outcome Evidence", "Situated Outcome Evaluation",
        "Experience Candidate", "low battery", "high load", "degraded network", "Resource Management Candidate",
        "Attention Pattern Candidate", "cannot directly modify Identity", "Capability", "Goal", "Decision",
        "Reality", "Self State", "One event cannot permanently change", "Self State Pattern Candidate",
        "current evidence", "expiry", "not automatic learning", "not online learning", "personality update",
        "Recovery Candidate", "stale Experience"
    ],
    "self_state_whitebox_v1.md": [
        "Reality / Runtime / Diagnostics Evidence", "Self State Domain Mapping", "Physical", "Cognitive",
        "Capability", "Resource", "Self State Update Candidate", "Reducer validation", "Self Awareness Context",
        "Attention Adjustment Candidate", "Field Constraint Candidate", "Brain Awareness Candidate",
        "Experience Reference", "Self State ≠ Self Identity", "Self State ≠ Self Capability", "Self State ≠ Reality",
        "State Candidate ≠ Decision", "State Recovery ≠ Personality Change", "Low battery", "High load",
        "Recovery", "does not directly modifies Reality", "Goal", "Decision", "Action", "Identity",
        "Capability Identity", "Personality", "Emotion", "sole State mutation authority", "No Emotion Runtime",
        "Role Runtime", "Social Runtime", "B Runtime", "Action Runtime", "real model", "OCR", "SLAM",
        "Camera", "Hardware Runtime"
    ],
    "self_state_go_no_go_v1.md": [
        "Identity", "Capability", "State", "Physical State", "Cognitive State", "Capability State",
        "Resource State", "dynamic", "Self Identity", "Self State Update Candidate", "Reducer remains the sole State mutation authority",
        "Low battery", "high load", "high risk", "state recovery", "Attention", "Goal", "Decision",
        "Brain", "Experience", "Current evidence", "No Emotion State", "No Personality Change", "No Role",
        "No Social Runtime", "No B", "No automatic learning", "No online learning", "No Action", "No Action Runtime",
        "No real model", "No OCR", "No SLAM", "No Camera", "No Hardware Runtime", "No direct Reality mutation",
        "No direct Goal mutation", "No direct Decision mutation", "No automatic frequency adjustment",
        "No Scheduler implementation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "self_state_schema_v1.json": [
        "Self State Schema", "identity_reference", "physical_state", "cognitive_state", "capability_state_reference",
        "resource_state", "validity", "provenance", "battery", "temperature", "sensor_health", "storage",
        "network", "current_load", "active_field_count", "attention_consumption", "unknown_accumulation",
        "compute", "memory", "time", "self_state_is_not_self_identity", "self_state_is_not_capability_identity",
        "self_state_is_not_reality", "self_state_is_not_personality", "self_state_is_not_emotion",
        "does_not_modify_identity", "does_not_modify_goal", "does_not_modify_decision", "does_not_modify_action",
        "does_not_modify_reality", "reducer_is_sole_state_mutation_authority"
    ],
    "self_state_update_contract_v1.json": [
        "Self State Update Contract", "Self State Update Candidate", "Runtime Evidence", "Diagnostics Candidate",
        "Capability State Reference", "Resource Evidence", "Field Load Context", "Temporal Context",
        "Physical State", "Cognitive State", "Capability State", "Resource State", "previous_state",
        "proposed_state", "trigger", "confidence", "provenance", "uncertainty", "recovery_condition",
        "expiry_condition", "Reducer validation", "Self Awareness", "Attention Adjustment Candidate",
        "Brain Awareness Candidate", "automatic_state_mutation", "reducer_is_sole_state_mutation_authority",
        "does_not_modify_identity", "does_not_modify_capability_identity", "does_not_modify_reality",
        "does_not_modify_goal", "does_not_modify_decision", "does_not_trigger_action", "does_not_trigger_online_learning"
    ],
    "self_state_attention_interface_v1.json": [
        "Self State Attention Interface", "current Self State", "resource_state", "compute", "memory", "time",
        "battery", "network", "cognitive_load", "active Field count", "capability_state", "attention_adjustment_candidate",
        "resource_protection_candidate", "observation_scope_reduction_candidate", "alternative_observation_candidate",
        "attention_recovery_candidate", "low_battery", "high_load", "high_risk", "state_recovery",
        "attention_does_not_modify_self_state", "self_state_does_not_select_goal", "self_state_does_not_select_decision",
        "no_automatic_frequency_adjustment", "no_hardware_control", "candidate_only"
    ],
    "self_state_brain_interface_v1.json": [
        "Self State Brain Interface", "state_summary", "constraint_candidate", "confidence_adjustment_candidate",
        "unknowns", "provenance", "validity", "recovery_candidate", "brain_retains_goal", "brain_retains_decision",
        "brain_retains_value_evaluation", "brain_retains_action_authority", "brain_retains_identity_authority",
        "self_state_does_not_command_brain", "self_state_does_not_modify_goal", "self_state_does_not_modify_decision",
        "self_state_does_not_modify_identity", "self_state_does_not_issue_action", "brain_receives_summary_not_raw_hardware_control"
    ],
    "self_state_runtime_interface_v1.json": [
        "Self State Runtime Interface", "tick_context", "health_evidence", "resource_evidence",
        "capability_state_reference", "field_load_reference", "attention_load_reference", "Self State Update Candidate",
        "diagnostic_candidate", "recovery_candidate", "escalation_candidate", "runtime_does_not_modify_state_directly",
        "reducer_is_sole_state_mutation_authority", "runtime_does_not_replace_brain", "runtime_does_not_execute_action",
        "runtime_does_not_control_hardware", "no_scheduler_implementation", "no_runtime_execution"
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
