#!/usr/bin/env python3
"""V2 static verifier for Cognitive Governance Registry and Resource architecture."""
import json
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
MD_REQ = {
    "cognitive_governance_registry_resource_architecture_v1.md": ["Cognitive Governance Layer", "Cognitive Process Manager", "Resource Manager", "Authority Manager", "Self Awareness Infrastructure", "Capability Registry", "Model Registry", "Hardware Registry", "Diagnostics", "Reducer remains the sole State mutation authority"],
    "cognitive_process_model_v1.md": ["intent", "context", "state", "resource", "priority", "authority", "lifecycle", "Brain", "Neural", "User", "External Event"],
    "cognitive_process_priority_model_v1.md": ["Survival", "Safety", "Critical Goal", "Information Value", "Resource Cost", "not a Scheduler"],
    "cognitive_resource_budget_model_v1.md": ["compute", "battery", "attention", "memory", "network", "Expected Value", "Resource Cost", "Allocation Candidate", "not a Scheduler"],
    "attention_resource_allocation_contract_v1.md": ["Attention Requirement", "Information Value", "Attention Cost", "Allocation Candidate", "Brain retains final judgment"],
    "cognitive_escalation_policy_v2.md": ["Escalation Candidate", "risk increase", "unknown growth", "evidence conflict", "capability degradation", "resource stress", "Brain Review Candidate"],
    "background_process_management_model_v1.md": ["Background Process Management", "Promotion Candidate", "Suspension", "not a Scheduler", "Action Runtime"],
    "reality_workspace_lifecycle_contract_v1.md": ["Candidate", "Active", "Stale", "Expired", "Immediate State", "Working Reality", "Stable Reality Pattern", "Reality Compression"],
    "cognitive_process_whitebox_v1.md": ["Process Candidate Creation", "Need → Value → Cost → Allocation Candidate", "Self Awareness Infrastructure", "Self Capability Context", "not a Runtime trace"],
    "self_awareness_infrastructure_model_v1.md": ["Self Awareness Infrastructure", "Hardware Registry", "Model Registry", "Capability Registry", "Diagnostics", "Self Capability", "Hardware Capability", "Software Capability", "Model Capability", "Resource Availability"],
    "diagnostics_self_awareness_interface_v1.md": ["hardware_failure", "Capability State Candidate", "Self Capability Context Candidate", "cannot decide", "Reducer"],
    "registry_self_model_coupling_v1.md": ["Registry Asset", "Capability / Health State", "Self Capability Context", "Identity", "does not become a second cognitive subject"],
    "governance_registry_resource_whitebox_v1.md": ["Authority Manager", "Registry System", "Capability Registry", "Model Registry", "Hardware Registry", "Diagnostics", "Self Capability Context", "do not interpret"],
    "governance_registry_resource_go_no_go_v1.md": ["Cognitive Process", "Resource Management is not a Scheduler", "Authority Registry", "Self Awareness Infrastructure", "Reducer remains the sole State mutation authority", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "cognitive_process_lifecycle_contract_v1.json": ["Created", "Active", "Background", "Suspended", "Completed", "Archived", "reducer_is_sole_state_mutation_authority"],
    "capability_registry_contract_v1.json": ["Capability Registry", "text_evidence_extraction", "output_evidence_contract", "world_understanding", "registry_is_not_cognitive_subject"],
    "model_registry_contract_v1.json": ["Model Registry", "provider_identity", "supported_capability", "understand_world", "direct_brain_access"],
    "hardware_registry_contract_v1.json": ["Hardware Registry", "health_state", "capability_reference", "hardware_manager_direct_control", "hardware_manager_decision_authority"],
    "authority_registry_contract_v1.json": ["Permission / Authority Registry", "allowed_operations", "forbidden_operations", "authority_registry_is_not_decision_system", "reducer_sole_state_mutation_authority"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in MD_REQ.items():
        checks += 1
        path = root / FLOW / name
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
        path = root / FLOW / name
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
