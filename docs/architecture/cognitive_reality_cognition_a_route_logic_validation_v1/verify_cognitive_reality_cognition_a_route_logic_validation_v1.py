#!/usr/bin/env python3
"""V2 final verifier for A-Route Level 1 cognitive logic validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_logic_validation_model_v1.md": [
        "Evidence → World Representation",
        "Self–World Coupling",
        "Capability Boundary",
        "Unknown Preservation",
        "Reality Grounding",
        "Situation Re-evaluation",
        "private chain-of-thought",
    ],
    "cognitive_logic_metrics_v1.md": [
        "Self Awareness",
        "Reality Grounding",
        "Unknown Management",
        "Situation Adaptability",
        "Confidence Calibration",
    ],
    "cognitive_logic_validation_go_no_go_v1.md": [
        "no Decision, Action, Outcome, Experience",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
JSON_FIXTURES = {
    "self_world_coupling_test_cases_v1.json": [
        "world_state_is_constant",
        "situation_difference_follows_self_difference",
        "self_world_child",
        "self_world_adult",
        "self_world_large_animal",
    ],
    "capability_boundary_test_cases_v1.json": [
        "capability_to_false_confidence",
        "unsupported_identity_is_not_a_fact",
        "distant_sign_low_light_occlusion",
    ],
    "unknown_handling_test_cases_v1.json": [
        "unknown_preservation",
        "absence_of_evidence_is_not_absence_claim",
        "ambiguous_dark_moving_object",
    ],
    "reality_grounding_test_cases_v1.json": [
        "fact_hypothesis_and_risk_are_separated",
        "evidence_does_not_directly_become_reality_truth",
        "person_rapidly_approaching",
    ],
    "situation_reassessment_test_cases_v1.json": [
        "new_material_evidence_reassesses_situation",
        "reassessment_is_not_a_decision",
        "road_construction_reassessment",
    ],
}


def find_root() -> Path:
    for candidate in [Path.cwd(), *Path(__file__).absolute().parents]:
        if (candidate / FLOW).is_dir():
            return candidate
    return Path.cwd()


def main() -> int:
    root = find_root()
    failures: list[str] = []
    checks = 0

    for name, terms in DOC_TERMS.items():
        checks += 1
        path = root / FLOW / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")

    for name, terms in JSON_FIXTURES.items():
        checks += 1
        path = root / FLOW / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
            fixture = json.loads(text)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"fixture parse failure: {name}: {type(exc).__name__}")
            continue
        checks += 1
        if fixture.get("fixture_type") != "deterministic_logic_validation":
            failures.append(f"wrong fixture type: {name}")
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required fixture contract: {term} in {name}")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
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
