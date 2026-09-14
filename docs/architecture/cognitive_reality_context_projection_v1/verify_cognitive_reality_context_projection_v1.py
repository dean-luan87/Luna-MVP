#!/usr/bin/env python3
"""V2 static verifier for the Reality Context Projection bridge."""
import json
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
MD_REQ = {
    "reality_context_projection_model_v1.md": ["Reality Context Projection", "not a Situation Engine", "Observable State", "State Change", "Relevant Constraints", "Unknowns", "Provenance", "does not add risk", "user_is_sad"],
    "fact_relevance_boundary_v1.md": ["declared read scope", "Observable State", "State Change", "Relevant Constraints", "does not add a Goal", "does not add a Decision", "water_depth: 60cm", "risk: dangerous"],
    "unknown_propagation_contract_v1.md": ["Unknown Propagation", "Reality Unknown", "Context Unknown", "flow_speed: unknown", "does not authorize an Action"],
    "context_provenance_model_v1.md": ["source", "Evidence reference", "Reality State reference", "timestamp", "confidence", "uncertainty", "transform trace", "auditable read model", "not a Situation Engine"],
    "reality_context_whitebox_v1.md": ["Reality Neural Operating Space", "Reality Context Projection", "Observable State", "State Change", "Relevant Constraints", "Unknowns", "Provenance", "Situation Understanding", "read-only"],
    "go_no_go_v1.md": ["not a Situation Engine", "Observable State", "State Change", "Relevant Constraints", "Unknowns", "Provenance", "does not interpret facts", "Unknown Propagation", "No Situation Engine", "No raw model-to-A-Route path", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "reality_to_cognition_interface_contract_v1.json": ["Reality Neural Operating Space", "Reality Context Package", "observable_state", "state_change", "relevant_constraints", "unknowns", "provenance", "recommendation", "prediction", "decision", "creates_situation"],
    "context_package_schema_v1.json": ["reality_context_package", "observable_state", "state_change", "relevant_constraints", "unknowns", "provenance", "recommendation", "prediction", "emotion", "decision", "situation_engine"],
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
