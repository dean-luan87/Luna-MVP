#!/usr/bin/env python3
"""V2 static verifier for Reality Neural Operating Space architecture."""
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
REQ = {
    "reality_neural_operating_space_architecture_v1.md": ["Reality Neural Operating Space", "Reality State", "Self State", "Temporal State", "Entity State", "Relation State", "Attention Observation State", "Prediction Layer", "Outcome Prediction", "Decision Loop", "Planning", "Reasoning", "Evaluation", "Persistent Reality State"],
    "reality_state_runtime_concept_v1.md": ["Entity", "Event", "Relation", "State", "Location", "Change", "Current Reality State", "not a Prediction Layer", "Decision Loop", "Planning", "Reasoning"],
    "self_state_runtime_concept_v1.md": ["Capability", "Hardware", "Resource", "Health", "Limitation", "Current Condition", "not Personality", "Self State Candidate", "Identity remains continuous"],
    "temporal_reality_state_model_v1.md": ["current state", "previous reference", "change delta", "validity window", "temporal uncertainty", "not a Prediction", "not a Decision"],
    "entity_relation_management_model_v1.md": ["Entity Management", "Relation Management", "Event", "Change", "Current Entity / Relation State", "does not infer social meaning"],
    "evidence_memory_buffer_model_v1.md": ["Evidence Memory Buffer", "short-term cache", "provenance", "confidence", "uncertainty", "does not reason", "does not predict", "does not plan"],
    "reality_reducer_model_v1.md": ["sole State mutation authority", "Persistent Reality State", "Self State", "Temporal State", "Entity State", "Relation State", "Attention Observation State", "Latest evidence is not automatically correct", "Unknown"],
    "unknown_lifecycle_model_v1.md": ["Unknown Candidate", "Open Unknown", "Resolved", "Expired", "Conflicted", "Unknown is a first-class Reality State", "does not force completion"],
    "attention_observation_state_model_v1.md": ["Attention Observation State", "coverage", "freshness", "not Attention Decision", "does not decide"],
    "state_persistence_boundary_v1.md": ["Immediate State", "Working State", "Persistent Reality Pattern", "Persist only structured reality", "not Experience Consolidation", "not automatic learning"],
    "reality_neural_operating_space_whitebox_v1.md": ["Evidence Memory Buffer", "Reality Assembly / Alignment", "Reality Reducer (sole State mutation authority)", "Persistent Reality State", "Attention Observation", "A Route", "Brain"],
    "reality_neural_operating_space_go_no_go_v1.md": ["Reality Neural Operating Space", "Persistent Reality State", "Situation", "Decision", "Prediction", "Planning", "Reasoning", "Evaluation", "No Prediction Layer", "No Outcome Prediction", "No Decision Loop", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in REQ.items():
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
