#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field Governance and Orchestration."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_governance_model_v1.md": ["Field Governance", "Field Registry", "Field Admission", "Resource Governance", "Information Boundary", "Health Monitoring", "Orchestration", "does not make a Decision", "not a cognitive subject"],
    "cognitive_field_resource_governance_model_v1.md": ["Attention", "Memory", "Compute", "Sensor", "Energy", "Field Resource Request", "Resource Evaluation", "Allocation Candidate", "Monitoring", "not a Scheduler", "does not execute Action"],
    "cognitive_field_information_boundary_v1.md": ["Field Data Boundary", "shared", "scoped", "restricted", "unknown", "Battery Low", "Work Confidential File", "Family Field", "permission context", "does not create a Decision"],
    "cognitive_field_health_monitoring_model_v1.md": ["Health Monitoring", "abnormal lifecycle", "information inflation", "Unknown accumulation", "Field State drift", "Diagnostic Candidate", "does not repair", "does not execute Action"],
    "cognitive_field_orchestration_boundary_v1.md": ["coexist", "pause", "suspend", "resume", "share a declared resource", "remain isolated", "parent / child", "Field Relationship Candidate", "not Multi-Agent", "not Multi-A Coordination", "does not resolve value conflicts"],
    "cognitive_field_governance_whitebox_v1.md": ["Field Request", "Field Registry", "Field Admission", "Activation Candidate", "Resource Evaluation", "Information Boundary Check", "Health Monitoring", "Diagnostic Candidate", "Orchestration", "A Route Input", "Brain Interface"],
    "cognitive_field_governance_go_no_go_v1.md": ["Field Registry", "Field Admission", "Field Request", "Validation", "Activation Candidate", "External models cannot directly create a Field", "Resource Governance", "Attention", "Memory", "Compute", "Sensor", "Energy", "Information Boundary", "Diagnostic Candidate", "Orchestration", "A Route", "Brain", "Registry is not a cognitive subject", "Governance does not modify Reality", "Orchestration does not execute Decision", "No Role System", "No Emotion Engine", "No Social Runtime", "No Multi-Agent", "No Multi-A", "No B", "No Prediction", "No Decision", "No Action Runtime", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "cognitive_field_registry_contract_v1.json": ["Cognitive Field Registry", "field_id", "field_type", "lifecycle_state", "activation_source", "owner_reference", "resource_requirement", "boundary_policy", "registry_is_not_memory", "registry_is_not_cognitive_subject"],
    "cognitive_field_admission_contract_v1.json": ["Brain Intent", "Neural Detection", "External Event", "User Request", "Field Request", "Validation", "Admission", "Activation Candidate", "external_model_direct_creation", "make_decision"],
    "cognitive_field_brain_interface_v1.json": ["field_state", "resource_state", "conflict_candidate", "diagnostic_candidate", "field_relationship_candidate", "goal", "final_decision", "make_decision", "interpret_reality", "raw_reality_access"],
    "cognitive_field_a_route_interface_v1.json": ["current_field", "relevant_facts", "unknowns", "constraints", "provenance", "situation", "decision_candidate", "make_decision", "recommend_action"],
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
