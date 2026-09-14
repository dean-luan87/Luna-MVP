#!/usr/bin/env python3
"""V2 final verifier for A-Route Level 2 decision logic validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_decision_logic_validation_model_v1.md": [
        "Decision ≠ Action",
        "Situation dependency",
        "Unknown visibility",
        "Reconsideration",
        "Brain authority",
        "Survival Impact",
        "Experience Reference",
    ],
    "decision_trace_validation_model_v1.md": [
        "structured decision basis",
        "private chain-of-thought",
        "final cognitive judgment boundary",
    ],
    "decision_logic_metrics_v1.md": [
        "Situation Dependency",
        "Option Diversity",
        "Decision Stability",
        "Decision Adaptability",
    ],
    "decision_logic_validation_go_no_go_v1.md": [
        "No Action Execution",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
JSON_FIXTURES = {
    "decision_option_generation_test_cases_v1.json": [
        "flooded_road_option_generation",
        "option_diversity_present",
        "option_is_not_recommendation",
    ],
    "decision_evaluation_test_cases_v1.json": [
        "small_horse_crossing_capability_fit",
        "risk_resource_route_tradeoff",
        "low_resource_navigation",
        "self_capability_changes_option_evaluation",
        "brain_evaluation_required",
    ],
    "decision_uncertainty_test_cases_v1.json": [
        "occluded_area_uncertainty",
        "environment_change_decision_reconsideration",
        "capability_decline_decision_confidence",
        "unknown_enters_decision_evaluation",
        "old_decision_is_not_immutable",
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
        if fixture.get("fixture_type") != "deterministic_decision_logic_validation":
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
