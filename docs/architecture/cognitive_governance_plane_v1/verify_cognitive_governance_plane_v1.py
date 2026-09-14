#!/usr/bin/env python3
"""V2 static verifier for Cognitive Governance Plane architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_governance_plane_architecture_v1.md": [
        "Cognitive Governance Plane", "autonomous nervous-system-like", "Constitution", "Protocol Governance",
        "Registry Plane", "Admission Governance", "Authority Governance", "Diagnostics Governance", "Resource Governance",
        "Runtime Governance", "Change Governance", "highest constraint", "Protocol Manager", "lifecycle", "version",
        "compatibility", "deprecation", "migration", "Capability Registry", "Model Registry", "Hardware Registry",
        "Field Registry", "Authority Registry", "what exists", "Admission", "who may", "Diagnostic Candidate",
        "Process", "Tick", "Wake-up", "scheduling mechanics", "Draft", "Review", "Active", "Deprecated", "Archived",
        "does not modify Reality", "does not create Goals", "does not make Decisions", "No Model Runtime", "No Provider Runtime",
        "No OCR", "No SLAM", "No Hardware", "No Action", "No B", "No Emotion", "No Role"
    ],
    "governance_layer_boundary_model_v1.md": [
        "Constitution", "Governance Plane", "Runtime Plane", "Capability Plane", "policy", "lifecycle governance",
        "Reality", "Goal", "Value", "Decision", "Self Identity", "Action", "Reducer", "sole State mutation authority",
        "Registry Plane", "Admission", "Authority Governance", "Diagnostics", "Resource Governance", "Runtime Governance",
        "what exists", "may it enter", "under what authority", "how mechanics run", "what should Luna want",
        "second cognitive subject"
    ],
    "constitution_governance_relation_v1.md": [
        "highest constraint", "Governance Plane", "Evidence", "Reality", "Field", "Attention", "Situation", "Decision",
        "Reducer", "sole State mutation authority", "Unknown Preservation", "Reality > Experience", "Self Identity Continuity",
        "Provider", "Capability", "Protocol", "Registry", "Admission", "Authority", "Resource", "Runtime", "Change Proposal",
        "Governance Blocker", "does not register objects", "does not schedule Processes", "does not run Providers",
        "does not execute Actions", "does not become Brain", "Model Manager Runtime"
    ],
    "protocol_manager_governance_manual_v1.md": [
        "Protocol Manager", "protocol creation", "registration", "versioning", "compatibility", "deprecation", "migration",
        "archival", "Change Proposal", "Compatibility Review", "Version Candidate", "Admission", "Active", "Deprecated",
        "Archived", "new Protocol", "owner", "consumers", "schema", "provenance", "failure behavior", "security boundary",
        "breaking change", "new version", "rollback", "does not interpret Reality", "does not create a Goal",
        "does not make a Decision", "does not call a Provider", "does not execute an Action"
    ],
    "registry_plane_architecture_v1.md": [
        "Registry Plane", "what exists", "Capability Registry", "Model Registry", "Hardware Registry", "Field Registry",
        "Authority Registry", "capability identity", "Evidence contract", "limitations", "Model asset", "version",
        "provider mapping", "resource profile", "sensor/actuator identity", "health", "Field identity", "lifecycle",
        "permission", "Draft", "Review", "Admission", "Active", "Deprecated", "Archived", "does not decide",
        "does not execute", "does not create a Goal", "cannot control hardware"
    ],
    "admission_governance_model_v1.md": [
        "Admission", "controlled entry gate", "Protocol", "Capability", "Model", "Hardware", "Field", "Authority",
        "Identity and provenance", "Constitution compatibility", "Protocol compatibility", "Declared capability",
        "limitation", "Authority", "permission scope", "Resource profile", "health", "Evidence/output contract",
        "Risk", "failure namespace", "Admitted", "Deferred", "Rejected", "Expired", "Blocked", "not Runtime enablement",
        "not Provider execution", "cannot create a Goal", "cannot make a Decision", "Provider cannot admit itself",
        "Model cannot admit itself", "Governance Blocker"
    ],
    "authority_governance_model_v1.md": [
        "Who creates", "Who approves", "Who modifies", "Who runs", "Who observes", "Who can revoke", "Brain",
        "Constitution", "Registry", "Admission", "Provider", "Evidence", "Reality Write", "Diagnostics", "Diagnostic Candidate",
        "Reducer remains the sole State mutation authority", "Authority Proposal", "Constitution Check", "Risk Review",
        "Compatibility Review", "Approval Candidate", "revocation path", "registration", "model replacement"
    ],
    "diagnostics_governance_model_v1.md": [
        "Diagnostics", "observability", "classification", "not a control plane", "anomaly", "health degradation", "drift",
        "protocol errors", "resource drift", "Evidence quality", "Capability confidence", "Diagnostic Candidate",
        "Failure Classification Candidate", "Fallback Candidate", "Capability Update Candidate", "Governance Blocker Candidate",
        "not Action", "not Goal", "not Decision", "not Reality Write", "automatic repair", "Failure", "Classification",
        "Fallback Candidate", "correlation", "unknowns", "cannot hide a failure", "cannot weaken Constitution", "second Brain"
    ],
    "resource_governance_model_v1.md": [
        "Resource Governance", "compute", "energy", "memory", "time", "network", "storage", "sensor", "Attention",
        "Runtime Governance", "Need", "Capability Request", "Resource Requirement", "Budget Review", "Allocation Candidate",
        "Denial Candidate", "Information Value", "Resource Cost", "risk", "urgency", "quota", "reservation", "health",
        "throttling", "deferment", "release", "fallback", "cannot directly execute", "cannot change Goal", "cannot change Decision",
        "Capability Degraded Candidate", "Attention Adjustment Candidate", "sole State mutation authority"
    ],
    "runtime_governance_model_v1.md": [
        "Runtime Governance", "Process lifecycle", "Tick", "Wake-up", "Scheduling", "pause/resume", "health observation",
        "Intent", "Goal", "Value", "Situation", "Decision", "Reality interpretation", "Provider selection", "Action execution",
        "cognitive need", "Brain", "Admission", "Authority", "Protocol", "Resource", "Diagnostics", "Process Request",
        "Resource Candidate", "Wake-up Candidate", "Scheduler", "Runtime", "Model Manager Runtime", "Provider Runtime",
        "Hardware Runtime", "Action Runtime"
    ],
    "governance_operation_manual_v1.md": [
        "New Capability integration", "Capability Definition", "Registry Registration", "Protocol Binding", "Admission Review",
        "Provider Binding", "Evidence Validation", "Runtime Enable Candidate", "New Model integration", "Model Registry",
        "Capability Mapping", "Resource Profile", "Benchmark Candidate", "Controlled Enable Candidate", "Model Manager",
        "New Protocol", "Change Proposal", "Version Upgrade", "Migration Plan", "Activation Candidate", "Authority change",
        "Authority Proposal", "Constitution Check", "Risk Review", "Approval Candidate", "Failure handling", "Diagnostics",
        "Classification", "Fallback Candidate", "Change management", "rollback", "user-terminal verification command",
        "Passed assets", "not weakened", "not deleted"
    ],
    "governance_whitebox_v1.md": [
        "Constitution Check", "Change Proposal", "Object Draft", "Protocol", "Registry", "Admission", "Authority",
        "Resource", "Diagnostics Baseline", "Active Candidate", "Runtime Governance", "Who creates", "Who approves",
        "Who modifies", "Who runs", "Who observes", "Who can revoke", "Registry says what exists", "Admission says whether",
        "Authority says who", "Diagnostics says what is abnormal", "Resource Governance says", "Runtime Governance says",
        "Brain remains final cognitive authority", "Reducer remains the sole State mutation authority", "Diagnostic Candidate",
        "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation", "second Brain"
    ],
    "governance_go_no_go_v1.md": [
        "highest constraint", "Protocol Manager", "Registry Plane", "Capability", "Model", "Hardware", "Field", "Authority",
        "Admission", "entry gate", "Authority Governance", "create", "approve", "modify", "run", "observe", "revoke",
        "Diagnostics", "Resource Governance", "compute", "energy", "memory", "time", "network", "storage", "sensor",
        "Runtime Governance", "Process", "Tick", "Wake-up", "Draft", "Review", "Active", "Deprecated", "Archived",
        "Governance Operation Manual", "Whitebox", "who creates", "who approves", "who modifies", "who runs", "who observes",
        "who revokes", "sole State mutation authority", "final cognitive authority", "No Model Runtime", "No real Provider",
        "No OCR", "No SLAM", "No Hardware", "No Action", "No B", "No Emotion", "No Role", "No Social Runtime",
        "No automatic execution", "No direct Reality mutation", "No direct Goal mutation", "No direct Decision mutation",
        "second Brain", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ]
}

JSON_REQ = {
    "governance_lifecycle_contract_v1.json": [
        "Governance Lifecycle Contract v1", "Protocol", "Model", "Capability", "Hardware", "Field", "Authority",
        "Draft", "Review", "Admission", "Active", "Deprecated", "Archived", "draft_requires_owner",
        "review_requires_constitution_check", "admission_requires_protocol_compatibility", "active_requires_admission",
        "deprecated_requires_replacement_or_migration", "archived_is_not_runtime_active", "protocol_manager_owns_versioning",
        "registry_plane_owns_inventory", "admission_owns_entry_review", "authority_governance_owns_permission",
        "diagnostics_emits_candidates", "resource_governance_emits_allocation_candidates", "runtime_governance_owns_mechanics_only",
        "lifecycle_does_not_execute", "lifecycle_does_not_modify_reality", "reducer_is_sole_state_mutation_authority",
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
