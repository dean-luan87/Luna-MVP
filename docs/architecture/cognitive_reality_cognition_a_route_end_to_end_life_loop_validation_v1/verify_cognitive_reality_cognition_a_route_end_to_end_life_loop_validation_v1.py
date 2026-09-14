#!/usr/bin/env python3
"""V2 final verifier for A-Route end-to-end life-loop validation."""

from __future__ import annotations

import json
from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
DOC_TERMS = {
    "cognitive_a_route_e2e_validation_model_v1.md": [
        "Survival Drive",
        "Intent Preservation",
        "Attention Requirement",
        "Situated Outcome Evaluation",
        "Experience Candidate",
        "Evidence never skips Reality/World/Situation",
        "B Reflection has no current A-route control authority",
    ],
    "a_route_complete_trace_contract_v1.md": [
        "structured provenance contract",
        "private chain-of-thought",
        "Decision Trace",
        "Outcome Trace",
        "handoff-only",
    ],
    "a_route_e2e_metrics_v1.md": [
        "Loop Integrity",
        "Trace Completeness",
        "Reality Alignment",
        "Self Alignment",
        "Decision Quality",
        "Experience Quality",
    ],
    "a_route_failure_analysis_validation_v1.md": [
        "Difference Candidate",
        "Cause Attribution Candidate",
        "Capability Gap",
        "pattern candidate pending Validation",
    ],
    "a_route_e2e_go_no_go_v1.md": [
        "no trace skips from Evidence to Decision Candidate",
        "No real Hardware",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}
REGISTRY_TERMS = [
    "life_loop_01_daily_pharmacy_task",
    "life_loop_02_unfamiliar_mall_exit",
    "life_loop_03_degraded_visual_capability",
    "life_loop_04_speed_safety_goal_conflict",
    "life_loop_05_repeated_map_data_failure",
    "life_loop_06_long_duration_travel",
    "full_chain_present",
    "Experience Candidate"
]


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

    name = "a_route_life_loop_scenario_registry_v1.json"
    path = root / FLOW / name
    checks += 1
    if not path.is_file():
        failures.append(f"missing required file: {name}")
    else:
        try:
            text = path.read_text(encoding="utf-8")
            registry = json.loads(text)
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"scenario registry parse failure: {type(exc).__name__}")
        else:
            checks += 1
            if registry.get("fixture_type") != "deterministic_a_route_e2e_validation":
                failures.append("wrong scenario registry fixture type")
            for term in REGISTRY_TERMS:
                checks += 1
                if term not in text:
                    failures.append(f"missing required scenario contract: {term} in {name}")

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
