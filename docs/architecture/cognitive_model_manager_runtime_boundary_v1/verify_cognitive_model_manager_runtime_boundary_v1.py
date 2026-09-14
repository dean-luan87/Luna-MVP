#!/usr/bin/env python3
"""V2 static verifier for Model Manager Runtime Boundary architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_model_manager_positioning_v1.md": [
        "Model Manager", "asset", "implementation governance", "not a Brain", "reasoning center", "Task scheduler",
        "Decision maker", "cognitive subject", "Cognitive Requirement", "Capability", "Model / Provider Candidate",
        "Evidence Gateway", "Text Evidence", "Scene Evidence", "Spatial Evidence", "Audio Evidence", "Model Registry",
        "version", "Provider mapping", "Capability binding", "resource profile", "Hardware Compatibility", "health",
        "permission", "does not create a Goal", "does not receive full Self", "does not make a Decision", "does not create a Field",
        "does not modify Reality", "does not execute Action", "Model cognitive scope", "local feature", "possible vehicle",
        "you should go there", "Evidence Quality Candidate", "No real model", "No GPT", "No VLM", "No OCR", "No SLAM",
        "No ASR", "No Provider Runtime", "No automatic model switching", "No automatic learning", "No B", "No Emotion", "No Role"
    ],
    "model_runtime_boundary_v1.md": [
        "Model Runtime", "Capability Request", "Raw Evidence Candidate", "Goal", "full Self", "full Field", "Decision",
        "Authority", "complete cognitive state", "Situation Requirement", "Vision", "OCR", "Spatial", "Audio", "Scene",
        "Text", "Evidence Candidate", "Model Cognitive Scope", "Possible vehicle", "you should go there", "Controlled Available",
        "Registry", "Capability Binding", "Admission", "Permission", "Hardware Compatibility", "Resource Profile", "Health Baseline",
        "Evidence Output Contract", "does not automatically switch", "Model Capability Degradation Candidate", "Diagnostics",
        "No real Model Runtime", "No Provider Runtime", "No GPT", "No VLM", "No OCR", "No SLAM", "No ASR", "No Action Runtime"
    ],
    "model_provider_isolation_contract_v1.md": [
        "Input isolation", "model_reference", "capability_request_reference", "scoped input Evidence", "resource envelope",
        "deadline", "output schema", "Goal", "Brain Intent", "full Field", "full Self", "Identity", "Value", "Decision",
        "Authority", "Task list", "Action Request", "Raw Evidence Candidate", "Model Failure Candidate", "source", "confidence",
        "limitation", "Unknown", "provenance", "timestamp", "capability reference", "Evidence Gateway", "Provider is not Brain",
        "Provider replacement", "Self Identity", "Provider-to-Brain", "Provider-to-Decision", "Provider-to-Goal",
        "Provider-to-Reality", "Provider-to-Action"
    ],
    "model_whitebox_v1.md": [
        "Cognitive Requirement", "Capability Requirement", "Capability Governance", "Model Registry", "Capability Binding",
        "Model Admission", "Hardware Compatibility", "Resource Profile", "Health", "Provider Candidate", "Raw Evidence Candidate",
        "Evidence Gateway", "Reality Workspace", "Capability is abstract", "Model is an implementation option", "version",
        "Model Cognitive Scope", "local feature", "full Goal", "full Self", "full Field", "Authority", "Decision", "Task",
        "Source", "Confidence", "Limitation", "Unknown", "Provenance", "Model Replacement", "automatic model switching",
        "No real model", "No GPT", "No VLM", "No OCR", "No SLAM", "No ASR", "No Provider Runtime", "No Action Runtime",
        "No Hardware Runtime", "No automatic learning", "No B", "No Emotion", "No Role"
    ],
    "model_go_no_go_v1.md": [
        "Model Manager", "asset governance manager", "not Brain", "reasoning center", "Task scheduler", "Decision maker",
        "Model Registry", "Identity", "Version", "Provider", "Capability Binding", "Resource Requirement", "Hardware Compatibility",
        "Performance Profile", "Health", "Permission", "Capability → Implementation Options → Models", "Model Admission",
        "capability declaration", "boundaries", "Evidence output", "Model Runtime", "Capability Request", "Evidence Candidate",
        "Model Cognitive Scope", "Goal", "Decision", "Action", "Value", "Authority", "Source", "Confidence", "Limitation",
        "Unknown", "Provenance", "Evidence Gateway", "Model Replacement", "Identity", "Field", "Task", "Hardware limitation",
        "Model Unavailable", "Model Degradation Candidate", "Attention selects Capability", "implementation options",
        "automatic model switching", "No real model", "No GPT", "No VLM", "No OCR", "No SLAM", "No ASR", "No Provider Runtime",
        "No automatic learning", "No Action", "No B", "No Emotion", "No Role", "No direct Reality mutation", "No direct Goal mutation",
        "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "model_registry_schema_v1.json": [
        "Model Registry Schema v1", "model_id", "model_identity", "name", "vendor", "version", "provider_reference",
        "capability_bindings", "Text Recognition Capability", "resource_requirement_reference", "hardware_compatibility_reference",
        "performance_profile", "latency", "quality", "throughput", "health_state", "permission_reference", "cognitive_scope",
        "known_limitations", "registry_state", "Draft", "Review", "Admission", "Active", "Deprecated", "Archived",
        "model_is_not_brain", "model_is_not_decision_authority", "model_is_not_goal_authority", "model_does_not_modify_reality",
        "model_does_not_execute_action", "unknowns_are_preserved"
    ],
    "model_capability_binding_contract_v1.json": [
        "Model Capability Binding Contract v1", "model_reference", "capability_id", "capability_scope", "Evidence Provision",
        "input_contract", "full_goal", "full_self", "full_field", "decision", "output_contract", "Text Evidence",
        "known_limitations", "confidence_boundary", "provenance_requirement", "cognitive_scope_is_local", "model_cannot_create_goal",
        "model_cannot_create_decision", "model_cannot_create_field", "model_cannot_modify_reality", "evidence_gateway_required",
        "unknowns_are_preserved"
    ],
    "model_admission_contract_v1.json": [
        "Model Admission Contract v1", "model_candidate_reference", "registry_check", "capability_declaration_check",
        "boundary_declaration_check", "resource_requirement_check", "evidence_output_check", "hardware_compatibility_check",
        "permission_check", "health_baseline_check", "protocol_compatibility_check", "admission_state", "Draft", "Review",
        "Admitted Candidate", "Rejected", "Deferred", "Deprecated", "admission_is_not_runtime_execution",
        "admission_does_not_enable_automatic_switching", "admission_does_not_modify_goal", "admission_does_not_modify_decision",
        "provider_cannot_admit_itself", "unknowns_are_preserved"
    ],
    "model_evidence_output_contract_v1.json": [
        "Model Evidence Output Contract v1", "model_reference", "capability_reference", "raw_output_candidate", "evidence_type",
        "Text", "Scene", "Spatial", "Audio", "source", "confidence", "limitation", "unknowns", "provenance", "timestamp",
        "schema_validation", "evidence_gateway_required", "reality_update_candidate_required", "output_is_not_reality",
        "output_is_not_situation", "output_is_not_decision", "output_is_not_goal", "output_is_not_action", "unknowns_are_preserved"
    ],
    "model_health_monitoring_contract_v1.json": [
        "Model Health Monitoring Contract v1", "model_reference", "health_state", "Available", "Degraded", "Limited", "Failed",
        "Unknown", "health_evidence", "quality_signal", "latency_signal", "resource_signal", "diagnostics_candidate",
        "model_capability_degradation_candidate", "fallback_candidate", "automatic_model_switching", "health_does_not_modify_identity",
        "health_does_not_modify_goal", "health_does_not_modify_decision", "health_does_not_execute_action", "unknowns_are_preserved"
    ],
    "model_resource_profile_schema_v1.json": [
        "Model Resource Profile Schema v1", "model_reference", "hardware_compatibility_reference", "gpu_cpu", "memory", "latency",
        "energy", "network", "bandwidth", "storage", "performance_profile", "quality", "throughput", "resource_cost",
        "admission_resource_check_required", "resource_profile_does_not_select_goal", "resource_profile_does_not_make_decision",
        "unknowns_are_preserved"
    ],
    "model_hardware_compatibility_contract_v1.json": [
        "Model Hardware Compatibility Contract v1", "model_reference", "hardware_reference", "capability_reference",
        "compatibility_state", "Compatible Candidate", "Limited Candidate", "Incompatible Candidate", "Unknown",
        "required_hardware_capability", "required_driver_reference", "resource_constraints", "health_constraints",
        "calibration_constraints", "limitation", "compatibility_is_not_admission", "compatibility_is_not_runtime_execution",
        "hardware_state_is_authoritative", "model_does_not_control_hardware", "unknowns_are_preserved"
    ],
    "model_attention_interface_v1.json": [
        "Model Attention Interface v1", "capability_requirement_reference", "attention_priority_candidate", "information_value",
        "risk_context", "resource_cost", "model_option_candidates", "quality_latency_tradeoff", "attention_selects_capability_not_model",
        "model_manager_provides_options", "model_does_not_trigger_attention", "model_does_not_modify_goal", "model_does_not_modify_decision",
        "automatic_model_switching", "unknowns_are_preserved"
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
