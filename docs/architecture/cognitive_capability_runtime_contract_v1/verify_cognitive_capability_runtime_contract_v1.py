#!/usr/bin/env python3
"""V2 static verifier for Capability Runtime Contract Architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_capability_runtime_contract_model_v1.md": [
        "Observation Requirement", "Capability Request", "Capability Admission", "Provider Invocation Candidate",
        "Provider Output", "Raw Evidence Candidate", "Evidence Gateway", "Reality Update Candidate", "Reducer",
        "not a Model Request", "not a Decision", "not an Action", "Attention", "Observation Cycle",
        "Situation Requirement", "Brain", "does not directly call a Provider", "Provider cannot create a request",
        "Runtime cannot create a need", "Requirement Match", "Permission", "Resource Budget", "Capability State",
        "Confidence", "Risk Level", "Evidence Expectation", "Admission is a candidate", "Provider sees only",
        "Goal", "Brain Intent", "full Field", "Identity", "Value", "Decision", "Resource Cost", "camera/sensor",
        "GPU/CPU", "memory", "latency", "energy", "network", "storage", "unavailable", "timeout",
        "low_confidence", "invalid_output", "resource_denied", "protocol_error", "provider_error",
        "Diagnostics", "Self Capability Update Candidate", "Attention Adjustment Candidate", "Alternative Capability Candidate",
        "No real model call", "No OCR", "No SLAM", "No Camera", "No Hardware", "No Provider Runtime",
        "No Action Runtime", "No automatic execution", "No automatic learning", "No B Route"
    ],
    "capability_invocation_boundary_v1.md": [
        "Attention", "Observation Cycle", "Situation Requirement", "Capability Requirement", "Capability Request",
        "Brain", "does not directly execute", "Provider and Model cannot submit", "Runtime cannot invent",
        "Need", "Admission Candidate", "Provider Invocation Candidate", "request_reference", "capability_id",
        "scoped input", "output Evidence schema", "resource envelope", "expiry", "provenance", "Provider cannot create a need",
        "trigger itself", "create a Field", "modify Reality", "modify Goal", "modify Decision", "reach Brain directly",
        "execute Action", "Capability Degraded Candidate", "Capability Unavailable Candidate", "Capability Failure Candidate",
        "No real Provider Runtime", "No Model call", "No OCR", "No SLAM", "No Camera", "No Hardware", "No Action"
    ],
    "provider_isolation_contract_v1.md": [
        "Least-privilege input", "request_reference", "capability_id", "scoped input Evidence", "capability parameters",
        "resource envelope", "deadline", "expected output Evidence schema", "Goal", "Brain Intent", "full Cognitive Field",
        "Identity", "Value", "Decision Candidate", "Action Request", "complete Self Model", "Raw Evidence Candidate",
        "Failure Candidate", "provenance", "confidence", "uncertainty", "timestamp", "capability reference",
        "Evidence Gateway", "Reducer remains the sole State mutation authority", "Provider replacement", "A Route logic",
        "Self Identity", "Provider-to-Brain", "Provider-to-Decision", "Provider-to-Goal", "Provider-to-Field",
        "Provider-to-Reality", "Provider-to-Action", "direct model call", "automatic external operation"
    ],
    "capability_runtime_whitebox_v1.md": [
        "Observation Requirement", "Capability Request", "Capability Admission", "Resource", "Permission", "State Review",
        "Provider Invocation Candidate", "Raw Evidence Candidate", "Evidence Gateway", "Reality Update Candidate", "Reducer",
        "Capability-level", "Model-level", "least-privilege", "Goal", "Brain Intent", "full", "Identity", "Value",
        "Decision", "Failure", "Diagnostics", "Self Capability", "Alternative Capability", "mandatory",
        "No real model call", "No OCR", "No SLAM", "No Camera", "No Hardware", "No Provider Runtime", "No Action Runtime",
        "No automatic execution", "No automatic learning", "No Provider-to-Brain", "No Provider-to-Decision", "No B"
    ],
    "capability_runtime_go_no_go_v1.md": [
        "Capability Request", "Model Request", "Attention", "Observation Cycle", "Situation Requirement", "Provider",
        "Runtime cannot create a need", "Requirement Match", "Permission", "Constitution Boundary", "Resource Budget",
        "Capability State", "Risk Level", "Evidence Expectation", "least-privilege", "Goal", "Brain Intent", "full Field",
        "Identity", "Value", "Decision", "complete Self Model", "Raw Evidence Candidate", "Evidence Gateway",
        "Reducer", "camera/sensor", "GPU/CPU", "memory", "latency", "energy", "network", "storage", "Resource Cost",
        "unavailable", "timeout", "low_confidence", "invalid_output", "resource_denied", "protocol_error", "provider_error",
        "Diagnostics", "Self Capability", "Attention", "Alternative Capability", "Provider replacement", "Self Identity",
        "No real model call", "No OCR", "No SLAM", "No Camera", "No Hardware", "No Provider Runtime", "No Action Runtime",
        "No automatic execution", "No automatic learning", "No Provider-to-Brain", "No Provider-to-Decision", "No Provider-to-Goal",
        "No B", "No Emotion", "No Role", "No Social Runtime", "No direct Reality mutation", "No direct Goal mutation",
        "No direct Decision mutation", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "capability_request_schema_v1.json": [
        "Capability Request Schema v1", "request_id", "observation_requirement_reference", "capability_id", "capability_type",
        "input_contract", "evidence_expectation", "priority_candidate", "permission_candidate", "resource_requirement_reference",
        "capability_state_reference", "risk_level", "expiry", "provenance", "unknowns", "request_is_not_model_request",
        "request_is_not_decision", "request_is_not_action", "request_does_not_create_need", "provider_does_not_create_request",
        "brain_does_not_directly_call_provider", "admission_required", "unknowns_are_preserved"
    ],
    "capability_admission_contract_v1.json": [
        "Capability Admission Contract v1", "request_reference", "requirement_match", "permission_check",
        "constitution_boundary_check", "resource_budget_check", "current_capability_state_check", "risk_level_check",
        "evidence_expectation_check", "provenance_check", "admission_state", "Created", "Qualified", "Admitted Candidate",
        "Deferred", "Rejected", "Expired", "provider_invocation_candidate", "admission_is_not_execution",
        "admission_does_not_modify_reality", "admission_does_not_modify_goal", "admission_does_not_modify_decision",
        "provider_is_not_admission_authority", "runtime_does_not_create_need", "resource_denial_returns_candidate",
        "unknowns_are_preserved"
    ],
    "capability_result_boundary_v1.json": [
        "Capability Result Boundary v1", "provider_output", "raw_evidence_candidate", "evidence_gateway_validation",
        "reality_update_candidate", "reducer_reference", "result_is_not_reality", "result_is_not_situation",
        "result_is_not_decision", "result_is_not_goal", "result_is_not_action", "evidence_gateway_required",
        "reality_update_candidate_required", "provider_cannot_modify_reality", "unknowns_are_preserved"
    ],
    "capability_resource_request_contract_v1.json": [
        "Capability Resource Request Contract v1", "request_reference", "capability_reference", "camera_or_sensor", "gpu_cpu",
        "memory", "latency", "energy", "network", "storage", "resource_budget", "attention_priority", "allocation_candidate",
        "resource_denied_candidate", "resource_request_is_not_execution", "resource_request_does_not_modify_goal",
        "resource_request_does_not_modify_decision", "resource_cost_is_explicit", "no_runtime_allocation_in_this_phase"
    ],
    "capability_failure_contract_v1.json": [
        "Capability Failure Contract v1", "unavailable", "timeout", "low_confidence", "invalid_output", "resource_denied",
        "protocol_error", "provider_error", "request_reference", "provider_reference", "diagnostics_candidate",
        "capability_state_update_candidate", "self_capability_update_candidate", "attention_adjustment_candidate",
        "alternative_capability_candidate", "failure_is_not_decision_failure", "failure_does_not_modify_reality",
        "failure_does_not_modify_goal", "failure_does_not_modify_decision", "failure_does_not_modify_identity",
        "unknowns_are_preserved", "reducer_is_sole_state_mutation_authority"
    ],
    "capability_attention_interface_v1.json": [
        "Capability Attention Interface v1", "observation_requirement_reference", "capability_request_reference",
        "attention_priority_candidate", "information_value", "uncertainty_reduction", "risk_context", "resource_cost",
        "persistence", "Transient", "Persistent", "Background", "release_candidate", "retry_candidate",
        "alternative_capability_candidate", "attention_does_not_execute_model", "attention_does_not_modify_goal",
        "attention_does_not_modify_decision", "attention_does_not_directly_call_provider", "allocation_is_candidate_only",
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
