#!/usr/bin/env python3
"""V2 final verifier for A-Route Level 4 behavior robustness validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_behavior_robustness_validation_model_v1.md": [
        "Information noise",
        "Capability degradation",
        "Goal conflict",
        "Repeated failure",
        "Identity Stable",
        "feedback loop self-degradation",
        "Robustness Score Candidate",
    ],
    "robustness_metrics_v1.md": [
        "Reality Stability",
        "Self Stability",
        "Decision Stability",
        "Adaptation Quality",
        "Unknown Handling",
        "Recovery Capability",
    ],
    "behavior_robustness_go_no_go_v1.md": [
        "Information noise remains governed Evidence",
        "No real model",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
JSON_FIXTURES = {
    "information_noise_test_cases_v1.json": [
        "single_false_obstacle_observation",
        "single_error_becomes_reality",
        "evidence_not_reality",
    ],
    "capability_degradation_test_cases_v1.json": [
        "camera_contamination_visual_degradation",
        "dark_environment_confidence_under_stress",
        "Identity Stable",
        "confidence_inflation",
        "self_identity_stability_preserved",
    ],
    "goal_conflict_test_cases_v1.json": [
        "fast_arrival_conflicts_with_hazardous_road",
        "shopping_mall_closes_after_initial_plan",
        "Survival Impact",
        "unexpected_environment_shift_reopens_cognitive_chain",
    ],
    "repeated_failure_test_cases_v1.json": [
        "navigation_failures_map_data_attribution",
        "feedback_loop_anti_oscillation",
        "automatic_self_identity_change",
        "feedback_loop_self_degradation",
        "correction_safety_preserved",
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
        if fixture.get("fixture_type") != "deterministic_behavior_robustness_validation":
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
