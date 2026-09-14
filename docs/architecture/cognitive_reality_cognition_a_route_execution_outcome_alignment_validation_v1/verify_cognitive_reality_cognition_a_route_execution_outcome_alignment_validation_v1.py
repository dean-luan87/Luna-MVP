#!/usr/bin/env python3
"""V2 final verifier for A-Route Level 3 execution-outcome alignment validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_execution_outcome_alignment_validation_model_v1.md": [
        "Decision ≠ Execution",
        "Outcome ≠ Failure",
        "Past Available Context",
        "Cause Attribution",
        "Correction Boundary",
        "Capability Gap",
        "Environment Change",
    ],
    "outcome_trace_validation_model_v1.md": [
        "structured provenance",
        "private chain-of-thought",
        "Past Available Context",
        "responsibility or blame",
    ],
    "failure_attribution_metrics_v1.md": [
        "Decision Outcome Separation",
        "Attribution Quality",
        "Correction Safety",
        "automatically update Strategy",
    ],
    "execution_outcome_validation_go_no_go_v1.md": [
        "good outcome after high-risk decision does not validate the strategy",
        "No real Action Runtime",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
JSON_FIXTURES = {
    "execution_boundary_test_cases_v1.json": [
        "decision_reasonable_environment_sudden_change",
        "execution_deviation_left_detour_not_realized",
        "Environment Change",
        "Execution Gap",
        "real_action_runtime_excluded",
    ],
    "outcome_attribution_test_cases_v1.json": [
        "high_risk_decision_accidental_good_outcome",
        "distant_text_failure_capability_gap",
        "unknown_cause_outcome",
        "Capability Gap",
        "Unknown",
        "attribution_is_not_blame",
    ],
    "prediction_outcome_alignment_test_cases_v1.json": [
        "prediction_reality_environment_difference",
        "information_gap_difference",
        "understanding_gap_difference",
        "repeated_failure_pattern_candidate",
        "requires_validation_before_adoption",
        "online_learning",
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
        if fixture.get("fixture_type") != "deterministic_execution_outcome_validation":
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
