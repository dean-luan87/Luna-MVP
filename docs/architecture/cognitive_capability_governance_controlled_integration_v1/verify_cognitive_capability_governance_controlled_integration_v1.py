#!/usr/bin/env python3
"""V2 static verifier for controlled capability integration."""
import json
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
REQ = {
    "capability_governance_controlled_integration_plan_v1.md": [
        "Capability ≠ Understanding", "Capability Registry", "Evidence Gateway", "Provider Replacement", "No real model call"
    ],
    "provider_boundary_contract_v1.md": ["Provider Candidate", "no Truth", "no Decision", "no Reality", "no Brain"],
    "evidence_gateway_validation_model_v1.md": ["Evidence Candidate", "Evidence Validation", "confidence", "provenance", "uncertainty", "Reality Cognition"],
    "self_capability_feedback_interface_v1.md": ["Capability State Changed", "Self Capability Context Candidate", "Brain Awareness", "not “Luna cannot read”"],
    "controlled_capability_integration_go_no_go_v1.md": ["Capability Isolation", "Evidence Integrity", "Provider Replaceability", "Cognitive Independence", "Failure Traceability", "No real model", "No real OCR", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "capability_registration_contract_v1.json": ["capability_id", "text_evidence_extraction", "output_evidence_contract", "world_understanding"],
    "capability_admission_contract_v1.json": ["provider_identity", "supported_capability", "known_limitation", "world_understanding_claim_forbidden"],
    "capability_failure_trace_schema_v1.json": ["provider_unavailable", "low_quality_output", "protocol_error", "diagnostics_required", "direct_self_update", "Reducer only"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in REQ.items():
        path = root / FLOW / name
        checks += 1
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
    for name, terms in JSON_REQ.items():
        path = root / FLOW / name
        checks += 1
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
