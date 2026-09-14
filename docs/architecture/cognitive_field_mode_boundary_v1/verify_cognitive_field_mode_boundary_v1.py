#!/usr/bin/env python3
"""V2 static verifier for Cognitive Field Mode Boundary architecture."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
MD_REQ = {
    "cognitive_field_mode_boundary_model_v1.md": ["Field Mode", "Reality Mode", "Historical Reconstruction Mode", "Simulation Mode", "Creative Mode", "Only Reality Mode is allowed", "not a data cache", "Decision", "Planning", "Prediction", "Action"],
    "historical_reconstruction_mode_placeholder_v1.md": ["Historical Reconstruction Mode", "historical Evidence", "Historical Field Candidate", "time", "space", "relationships", "cannot rewrite Reality State", "not implemented"],
    "simulation_mode_placeholder_v1.md": ["Simulation Mode", "Reality Field", "Hypothesis Modification", "Simulation Field Candidate", "Possible Result Candidate", "not a Prediction Fact", "cannot modify A Reality", "placeholder only", "not implemented"],
    "creative_mode_placeholder_v1.md": ["Creative Mode", "hypothetical Field", "not Reality", "not a Prediction Fact", "cannot enter Reality State", "placeholder only", "not implemented"],
    "field_modification_boundary_v1.md": ["Hypothesis Modification", "Base Reality", "Non-Reality Field Candidate", "Simulation Result", "Brain Evaluation", "cannot directly modify A Reality", "not online learning", "not a Runtime"],
    "a_b_field_relationship_boundary_v1.md": ["Reality Field", "A Route", "B Route", "Reality Mode", "Simulation Field Candidate", "Strategy Candidate", "does not control current A Decision", "B Route is not implemented"],
    "simulation_result_brain_handoff_placeholder_v1.md": ["Simulation Result Candidate", "Brain Evaluation", "Validated Improvement", "Strategy Candidate", "does not directly enter Reality State", "No Simulation Runtime", "no automatic Decision"],
    "cognitive_field_mode_whitebox_v1.md": ["Reality Neural Operating Space", "Reality Field", "Reality Mode", "Historical Reconstruction Mode", "Simulation Mode", "Creative Mode", "Hypothesis Modification", "Brain Evaluation", "Only Reality Mode is active"],
    "cognitive_field_mode_go_no_go_v1.md": ["Field Mode", "Reality Mode", "Historical Reconstruction Mode", "Simulation Mode", "Creative Mode", "Only Reality Mode is allowed", "Hypothesis Modification", "Simulation Field Candidate", "cannot alter A Reality", "Simulation Result", "Brain Evaluation", "B Route", "No Simulation Runtime", "No Prediction Runtime", "No automatic Planning", "No automatic Decision", "No Action", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
JSON_REQ = {
    "reality_mode_contract_v1.json": ["Reality Mode", "allowed_current_mode", "current_reality_field", "current_self_state", "current_evidence", "hypothesis_modification", "Reducer only", "simulation_runtime"],
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
