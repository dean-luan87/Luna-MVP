#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field Capability Integration architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

MD_REQ = {
    "cognitive_field_capability_integration_model_v1.md": [
        "Observation Requirement", "Capability Registry", "Capability Admission",
        "Model Manager", "Provider", "Evidence Gateway", "Reality Workspace",
        "Field Update", "Provider replacement", "Human Feedback", "Capability Failure",
        "Diagnostics", "Self Capability Candidate", "does not perform real model execution",
        "real OCR", "real SLAM", "Hardware Runtime", "Action Runtime"
    ],
    "capability_selection_boundary_v1.md": [
        "Observation Requirement", "Capability Registry", "Capability Admission",
        "Object Evidence", "Text Evidence", "Spatial Evidence", "provider-neutral",
        "create a Field", "modify Reality State", "trigger Action", "Provider Replacement"
    ],
    "model_provider_boundary_v1.md": [
        "Model Manager", "Provider Candidate", "Provider Execution Boundary",
        "Evidence Gateway", "Provider Replacement", "not a Fact", "not Reality",
        "not a Decision", "cannot bypass the Evidence Gateway", "No real OCR",
        "no real SLAM", "No Hardware Runtime", "No Action Runtime"
    ],
    "capability_failure_feedback_v1.md": [
        "Provider unavailable", "low-quality Evidence", "capability protocol error",
        "Capability Failure", "Diagnostics", "Self Capability Candidate", "Human Feedback",
        "Evidence Gateway", "Unknown candidate", "No automatic", "automatic Action"
    ],
    "field_capability_whitebox_v1.md": [
        "Cognitive Field", "Observation Requirement", "Capability Registry",
        "Capability Admission", "Model Manager", "Provider Candidate", "Evidence Gateway",
        "Evidence Candidate", "Reality Workspace", "Capability Failure", "Diagnostics",
        "Self Capability Candidate", "real model execution", "real OCR", "real SLAM",
        "Hardware Runtime", "Action Runtime"
    ],
    "field_capability_go_no_go_v1.md": [
        "Observation Requirement", "Capability Registry", "Model Manager", "Provider",
        "Evidence Gateway", "Provider replacement", "Human Feedback", "Capability Failure",
        "Diagnostics", "Self Capability Candidate", "No real model execution", "No real OCR",
        "No real SLAM", "No Hardware Runtime", "No Action Runtime", "No B Simulation Runtime",
        "no online learning", "no automatic model switching", "no automatic Reality mutation",
        "no direct model call", "WAITING_FOR_USER_TERMINAL_VERIFICATION"
    ],
}

JSON_REQ = {
    "field_observation_requirement_contract_v1.json": [
        "Observation Requirement", "Cognitive Field", "required_evidence",
        "provider_neutral", "no_direct_model_call", "no_action_authority",
        "no_reality_mutation", "admission_required"
    ],
    "evidence_gateway_field_interface_v1.json": [
        "observation_requirement", "provider_output", "human_feedback", "provenance",
        "evidence_candidate", "Reality Workspace", "Reducer only", "direct_decision",
        "direct_action", "provider_bypass"
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
