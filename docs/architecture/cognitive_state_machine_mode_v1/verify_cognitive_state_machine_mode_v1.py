#!/usr/bin/env python3
"""V2 static verifier for Cognitive State Machine and Mode architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_runtime_state_model_v1.md": [
        "Cognitive Runtime State", "Idle", "Observe", "Engage", "Analyze", "Escalated", "Recover", "Maintain",
        "runtime states", "not Tasks", "not Goals", "not Decisions", "not Actions", "Runtime State Candidate",
        "entry", "maintenance", "exit", "timeout", "Reducer remains the sole State mutation authority",
        "does not modify Reality", "does not modify Goal", "does not modify Decision"
    ],
    "cognitive_mode_brain_boundary_v1.md": [
        "Runtime State / Mode Candidate", "Brain Evaluation", "Goal or Decision Candidate", "does not replace Brain",
        "change Goal", "Decision", "Identity", "Reality", "Action", "Attention cannot decide Mode",
        "Survival Mode Candidate", "Emergency Candidate", "not an Action"
    ],
    "cognitive_mode_neural_boundary_v1.md": [
        "Stimulus", "Neural Response Candidate", "Runtime State Candidate", "Attention Reallocation Candidate",
        "Brain Escalation if needed", "Emergency Candidate", "Risk Increase Candidate", "Resource Protection Candidate",
        "does not decide", "alter Goal", "modify Reality", "execute Action", "cannot lock Survival Mode",
        "cannot control hardware frequency"
    ],
    "cognitive_mode_experience_boundary_v1.md": [
        "Experience", "Mode Transition Candidate", "Survival Mode", "Current Reality Evidence", "Cognitive Mode Candidate",
        "One event cannot permanently alter", "Identity", "Goal", "Decision", "Attention Policy",
        "not an automatic mode switch"
    ],
    "cognitive_mode_stability_model_v1.md": [
        "entry threshold", "maintenance evidence", "exit threshold", "minimum dwell", "timeout", "hysteresis",
        "cooldown", "recovery", "Normal Mode", "Survival Mode", "oscillation", "false trigger", "Diagnostic Candidate",
        "Focus Mode", "Recovery Mode", "Maintenance Mode", "does not modify Goal", "does not modify Decision",
        "does not modify Identity", "does not modify Reality", "does not modify Action"
    ],
    "cognitive_mode_whitebox_v1.md": [
        "Reality Change", "Runtime State Evaluation", "Cognitive Mode Candidate", "Attention / Process Allocation Candidate",
        "Observation / Capability Candidate", "Evidence", "A Route", "Brain Evaluation", "Experience Reference",
        "Runtime Update Candidate", "Survival Mode", "Normal Mode", "Focus Mode", "Recovery Mode", "Maintenance Mode",
        "Stimulus", "Neural Response Candidate", "Attention Reallocation Candidate", "Brain Escalation if needed",
        "not Brain", "not a Decision Engine", "not an Action Runtime", "No OCR", "No SLAM", "No Hardware", "No B Runtime"
    ],
    "cognitive_mode_go_no_go_v1.md": [
        "Runtime states", "Idle", "Observe", "Engage", "Analyze", "Escalated", "Recover", "Maintain", "Survival Mode",
        "Normal Mode", "Focus Mode", "Recovery Mode", "Maintenance Mode", "Mode Transition Contract", "Reality change",
        "Risk", "Resource", "Field", "Experience", "Attention Budget Candidate", "Attention does not select Mode",
        "does not replace Brain", "Goal", "Decision authority", "Neural Fast Path", "Stimulus", "Neural Response Candidate",
        "Runtime State Candidate", "Attention Reallocation Candidate", "Brain Escalation if needed", "thresholds", "hysteresis",
        "cooldown", "oscillation", "No real model", "No OCR", "No SLAM", "No Hardware Runtime", "No Action",
        "No Emotion", "No Role", "No Social Runtime", "No B Runtime", "no automatic mode change",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "cognitive_mode_registry_v1.json": [
        "Cognitive Mode Registry", "Survival Mode", "Normal Mode", "Focus Mode", "Recovery Mode", "Maintenance Mode",
        "mode_is_not_goal", "mode_is_not_decision", "mode_is_not_action", "automatic_mode_change", "role_runtime",
        "emotion_runtime", "b_runtime"
    ],
    "cognitive_mode_transition_contract_v1.json": [
        "Cognitive Mode Transition Contract", "reality_change", "risk_candidate", "resource_state", "field_state",
        "experience_reference", "Cognitive Mode Transition Candidate", "Normal Mode", "Risk Increase",
        "Survival Mode Candidate", "requires_confidence", "requires_exit_condition", "automatic_transition",
        "direct_brain_command", "direct_attention_command", "direct_action"
    ],
    "cognitive_mode_attention_interface_v1.json": [
        "Cognitive Mode Attention Interface", "Cognitive Mode Candidate", "Attention Budget Adjustment Candidate",
        "Survival Mode", "Normal Mode", "Focus Mode", "Recovery Mode", "Maintenance Mode",
        "attention_does_not_select_mode", "direct_attention_mutation", "automatic_frequency_adjustment",
        "decision_authority"
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
