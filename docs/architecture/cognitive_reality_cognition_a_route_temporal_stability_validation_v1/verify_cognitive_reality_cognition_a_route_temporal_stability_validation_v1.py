#!/usr/bin/env python3
"""V2 final verifier for A-Route Level 5 temporal stability validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_temporal_stability_validation_model_v1.md": [
        "Self continuity",
        "Experience governance",
        "Reality priority",
        "Decision contextuality",
        "Long-term Unknown",
        "Temporal Stability Candidate",
    ],
    "temporal_stability_metrics_v1.md": [
        "Identity Stability",
        "Experience Quality",
        "Reality Adaptability",
        "Decision Consistency",
        "Adaptation Balance",
        "Drift Resistance",
    ],
    "temporal_stability_go_no_go_v1.md": [
        "Reality greater than Experience",
        "No clock Runtime",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
JSON_FIXTURES = {
    "self_continuity_test_cases_v1.json": [
        "day_1_to_day_30_visual_capability_change",
        "Identity Stable",
        "Capability Changed",
        "capability_change_is_not_identity_change",
    ],
    "experience_accumulation_test_cases_v1.json": [
        "one_week_repeated_construction_location",
        "experience_adds_judgment_basis",
        "experience_does_not_replace_current_evidence",
        "pattern_requires_validation",
    ],
    "experience_conflict_test_cases_v1.json": [
        "historically_open_road_currently_under_construction",
        "Reality_greater_than_Experience",
        "capability_upgrade_requires_validation",
        "new_asset_is_not_universal_capability_claim",
    ],
    "long_term_drift_test_cases_v1.json": [
        "scenario_a_one_day_life_flow",
        "scenario_b_one_week_change_flow",
        "scenario_c_one_month_change_flow",
        "long_term_conservative_route_drift",
        "prediction_stability_under_repeated_anomaly",
        "long_term_unresolved_region_unknown",
        "elapsed_time_is_not_evidence",
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
        if fixture.get("fixture_type") != "deterministic_temporal_stability_validation":
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
