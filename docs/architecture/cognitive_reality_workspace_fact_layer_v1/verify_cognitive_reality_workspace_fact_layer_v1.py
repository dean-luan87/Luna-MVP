#!/usr/bin/env python3
"""V2 static verifier for the Reality Workspace fact layer phase."""
import json
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
MD_REQ = {
    "reality_workspace_architecture_v1.md": ["Evidence ≠ Fact", "Fact ≠ Reality", "Reality State ≠ Situation", "Reality State Reducer", "Evidence Intake", "Evidence Assembly", "Current World State", "No real model"],
    "evidence_assembly_model_v1.md": ["Entity Binding", "Temporal Alignment", "Spatial Association", "Reality Candidate", "Conflict Preservation"],
    "reality_state_reducer_boundary_v1.md": ["sole State mutation authority", "temporal freshness", "provenance", "confidence", "expiry", "withdrawal", "Latest evidence is not automatically correct", "Unknown"],
    "unknown_management_contract_v1.md": ["Unknown", "Unknown Preservation", "does not manufacture certainty", "Conflicted Candidate"],
    "reality_workspace_whitebox_v1.md": ["Evidence Intake Layer", "Evidence Assembly Layer", "Reality State Reducer (sole State authority)", "Current World State", "Self Reality State", "Situation Candidate"],
    "reality_workspace_go_no_go_v1.md": ["Evidence ≠ Fact", "Reality State ≠ Situation", "sole State mutation authority", "Self State ≠ Personality", "No real model", "No OCR Runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "evidence_intake_contract_v1.json": ["evidence_id", "source", "timestamp", "confidence", "capability_reference", "provenance", "uncertainty", "direct_world_state_write"],
    "reality_candidate_schema_v1.json": ["candidate_id", "supporting_evidence", "unknowns", "not_fact", "not_situation", "not_decision"],
    "world_state_schema_v1.json": ["entities", "events", "relations", "unknowns", "validity", "provenance", "absolute_truth_claim"],
    "self_reality_state_schema_v1.json": ["Identity", "Capability", "Resource", "Limitation", "Current Condition", "personality", "Reducer only"],
    "situated_context_interface_v1.json": ["current_world_state", "self_state", "goal", "resource", "situation_candidate", "candidate_only", "brain_bypass"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in MD_REQ.items():
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
