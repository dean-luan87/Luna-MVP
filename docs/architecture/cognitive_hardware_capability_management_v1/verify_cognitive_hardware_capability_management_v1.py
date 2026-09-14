#!/usr/bin/env python3
"""V2 static verifier for Hardware Capability Management architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_hardware_capability_management_model_v1.md": [
        "Hardware Capability Management", "body/self-awareness foundation", "Hardware Identity", "Hardware Capability Profile",
        "Resource", "Health", "Calibration", "Limitation", "Self Capability Awareness", "Attention", "Runtime",
        "Model Requirement", "Identity", "Specification", "Capability Profile", "Resource Profile", "Health State",
        "Calibration State", "Vision Sensor Capability", "resolution", "FOV", "low-light", "Hardware Capability",
        "Hardware State", "Available", "Degraded", "Limited", "Failed", "Unknown", "Hardware Issue", "Diagnostics",
        "Hardware State Candidate", "Self Capability Update Candidate", "Adaptation Candidate", "low battery", "GPU temperature",
        "lower observation frequency", "smaller Model", "defer background", "another Evidence source", "does not close a Task",
        "does not change a Goal", "does not choose a Decision", "Hardware Resource Profile", "Model Admission", "No hardware control",
        "No driver development", "No Camera", "No Sensor", "No Model Runtime", "No Provider Runtime", "No Action Runtime",
        "No Emotion", "No Role", "No Social Runtime", "automatic adaptation"
    ],
    "hardware_state_model_v1.md": [
        "Hardware Capability", "Hardware State", "what could", "current condition", "Available", "Degraded", "Limited",
        "Failed", "Unknown", "Camera Capability", "lens obstructed", "GPU Capability", "thermal throttling", "Battery Capability",
        "low charge", "Storage Capability", "capacity constrained", "Hardware Identity", "Self Identity", "Goal", "Reality",
        "Hardware Evidence", "State Update Candidate", "Reducer", "Self Capability", "Self State", "resource insufficient",
        "vision reliability degraded", "does not close a Task", "does not stop a Process", "does not choose a Decision"
    ],
    "hardware_whitebox_v1.md": [
        "Hardware Registry Entry", "Hardware Capability Profile", "Resource", "Health", "Calibration", "Limitation",
        "Diagnostics Candidate", "Hardware State Candidate", "Self Capability", "Confidence Candidate", "Attention", "Runtime",
        "Model Requirement Candidate", "Hardware identity", "Hardware Capability", "Hardware State", "Capability Contribution",
        "Evidence support", "Understanding", "Decision", "Available", "Degraded", "Limited", "Failed", "Unknown",
        "Hardware Manager reports body state", "Runtime owns execution mechanics", "Attention may reallocate observation",
        "Model Manager manages implementation assets", "Adaptation", "lower frequency", "smaller model", "defer background",
        "alternative evidence", "Reducer remains the sole State mutation authority", "No hardware control", "No driver", "No Camera",
        "No Sensor", "No Model Runtime", "No Action Runtime", "No Emotion", "No Role", "No Social", "No B"
    ],
    "hardware_go_no_go_v1.md": [
        "Hardware Registry Extension", "Identity", "Specification", "Capability Profile", "Resource Profile", "Health State",
        "Calibration State", "Limitation", "Hardware Capability", "Hardware State", "Self Identity", "Capability Contribution",
        "output Evidence", "confidence boundary", "Available", "Degraded", "Limited", "Failed", "Unknown", "Hardware Diagnostics",
        "Hardware Issue", "Self Capability Update Candidate", "Hardware Adaptation", "Attention", "Runtime", "Model Requirement",
        "Model Manager", "implementation assets", "Hardware replacement", "No hardware control", "No driver development",
        "No Camera connection", "No sensor connection", "No Model Runtime", "No Provider Runtime", "No Action Runtime", "No Emotion",
        "No Role", "No Social Runtime", "No automatic adaptation", "No direct Reality mutation", "No direct Goal mutation",
        "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "hardware_registry_extension_schema_v1.json": [
        "Hardware Registry Extension Schema v1", "hardware_id", "hardware_type", "Camera", "Microphone", "IMU", "GPS",
        "Display", "Battery", "Storage", "Network", "identity", "specification", "resolution", "fov", "range", "capacity",
        "capability_profile_reference", "resource_profile_reference", "health_state_reference", "calibration_state_reference",
        "limitation", "registry_state", "Draft", "Review", "Admission", "Active", "Deprecated", "Archived",
        "admission_required", "hardware_manager_does_not_control", "hardware_does_not_modify_reality", "hardware_does_not_modify_goal",
        "hardware_does_not_execute_action", "unknowns_are_preserved"
    ],
    "hardware_capability_profile_v1.json": [
        "Hardware Capability Profile v1", "hardware_id", "capability_id", "capability_contribution", "Object Observation",
        "OCR Input", "Scene Evidence", "input_boundary", "output_boundary", "Evidence Candidate", "resource_profile",
        "energy", "compute", "memory", "latency", "confidence_boundary", "low_light", "occlusion", "motion_blur",
        "limitations", "provider_mapping_candidate", "capability_is_not_understanding", "capability_is_not_decision",
        "capability_is_not_reality", "evidence_gateway_required", "unknowns_are_preserved"
    ],
    "hardware_health_contract_v1.json": [
        "Hardware Health Contract v1", "hardware_id", "health_state", "Available", "Degraded", "Limited", "Failed", "Unknown",
        "health_evidence", "diagnostics_reference", "confidence", "provenance", "timestamp", "calibration_state", "Calibrated",
        "Drifted", "Required", "limitation", "health_update_candidate", "self_capability_update_candidate",
        "health_does_not_modify_identity", "health_does_not_modify_goal", "health_does_not_modify_decision",
        "health_does_not_execute_action", "reducer_is_sole_state_mutation_authority", "unknowns_are_preserved"
    ],
    "hardware_diagnostics_interface_v1.json": [
        "Hardware Diagnostics Interface v1", "hardware_reference", "issue_class", "blocked_sensor", "thermal", "power", "memory",
        "calibration", "connectivity", "unknown", "diagnostic_candidate", "severity", "confidence", "hardware_state_candidate",
        "capability_confidence_candidate", "self_capability_update_candidate", "attention_reallocation_candidate",
        "resource_adaptation_candidate", "diagnostics_does_not_control_hardware", "diagnostics_does_not_modify_reality",
        "diagnostics_does_not_modify_goal", "diagnostics_does_not_execute_action", "unknowns_are_preserved"
    ],
    "hardware_adaptation_candidate_contract_v1.json": [
        "Hardware Adaptation Candidate Contract v1", "hardware_reference", "low_battery", "thermal_pressure", "memory_pressure",
        "sensor_degradation", "network_loss", "unknown", "adaptation_candidate", "lower_observation_frequency",
        "smaller_model_requirement", "defer_background_work", "alternative_evidence_source", "resource_context",
        "capability_confidence_context", "attention_adjustment_candidate", "runtime_adjustment_candidate", "model_requirement_candidate",
        "hardware_manager_does_not_decide", "adaptation_is_candidate_only", "adaptation_does_not_modify_goal",
        "adaptation_does_not_modify_decision", "adaptation_does_not_execute", "unknowns_are_preserved"
    ],
    "hardware_attention_interface_v1.json": [
        "Hardware Attention Interface v1", "hardware_reference", "capability_state", "capability_confidence_candidate",
        "observation_cost", "attention_reallocation_candidate", "reduce", "increase", "alternative", "information_value",
        "resource_cost", "attention_does_not_modify_hardware", "attention_does_not_modify_goal", "attention_does_not_modify_decision",
        "attention_does_not_execute_action", "candidate_only", "unknowns_are_preserved"
    ],
    "hardware_runtime_interface_v1.json": [
        "Hardware Runtime Interface v1", "hardware_reference", "runtime_request_candidate", "state_observation_candidate",
        "resource_status_candidate", "runtime_owns_execution_mechanics", "hardware_manager_owns_body_state",
        "hardware_manager_does_not_control_hardware", "hardware_manager_does_not_close_task", "hardware_manager_does_not_modify_goal",
        "hardware_manager_does_not_modify_decision", "no_runtime_implementation_in_this_phase", "unknowns_are_preserved"
    ],
    "hardware_model_manager_interface_v1.json": [
        "Hardware Model Manager Interface v1", "hardware_reference", "resource_profile_reference", "model_requirement_candidate",
        "capability", "resource_constraints", "scale", "model_admission_candidate", "health_constraint_candidate",
        "hardware_contributes_resource_profile", "model_manager_manages_implementation_assets", "hardware_manager_manages_body_state",
        "model_manager_does_not_manage_cognition", "hardware_does_not_select_model", "no_model_runtime_in_this_phase",
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
