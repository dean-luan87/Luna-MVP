#!/usr/bin/env python3
"""User-terminal V2 verifier for Temporal Understanding Extension v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_temporal_context_contract_v1.md": (
        "Past Reference",
        "Current State Reference",
        "Change Evidence",
        "Transition Pattern Candidate",
        "Trend Candidate",
        "Future Possibility Candidate",
        "Temporal Uncertainty",
        "Prediction != Reality",
    ),
    "cognitive_temporal_world_state_model_v1.md": (
        "Temporal World State Candidate",
        "does not modify Reality",
        "not causality",
        "not a forecast",
        "sole State mutation authority",
    ),
    "cognitive_temporal_self_coupling_model_v1.md": (
        "Self Capability Context",
        "Goal Context",
        "Resource Context",
        "Temporal Situation Enhancement Candidate",
        "does not change Self Model",
    ),
    "cognitive_temporal_situation_enhancement_model_v1.md": (
        "Situation Candidate",
        "Decision Support Candidate",
        "does not decide to reroute",
        "does not decide",
    ),
    "cognitive_temporal_experience_extension_model_v1.md": (
        "Temporal Experience Extension Candidate",
        "turning_point_candidate",
        "validation is required",
        "does not enter B Reflection",
    ),
    "cognitive_temporal_boundary_model_v1.md": (
        "does not perform time planning",
        "Scheduler",
        "automatic frequency adjustment",
        "does not connect Field assets",
    ),
    "cognitive_temporal_understanding_integration_model_v1.md": (
        "A-Route Extension Interface Contract",
        "not a parallel Reality Cognition loop",
        "Temporal order is not causal proof",
        "Reducer remains the sole State mutation authority",
    ),
    "cognitive_temporal_understanding_simulation_case_design_v1.md": (
        "Static vs dynamic",
        "Trend change",
        "Cyclic change",
        "Abrupt change",
        "Self difference",
        "no real Action",
    ),
    "cognitive_temporal_understanding_go_no_go_v1.md": (
        "Planning Only",
        "does not introduce Scheduler",
        "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ),
}


def repository_root() -> Path:
    for candidate in [Path.cwd(), *Path(__file__).absolute().parents]:
        if (candidate / FLOW).is_dir():
            return candidate
    raise FileNotFoundError("repository root with docs/architecture/cognitive_flow was not found")


def main() -> int:
    root = repository_root()
    failures: list[str] = []
    checks = 0
    for filename, terms in REQUIRED.items():
        target = root / FLOW / filename
        checks += 1
        if not target.is_file():
            failures.append(f"missing required file: {target.relative_to(root)}")
            continue
        content = target.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in content:
                failures.append(f"missing required contract term: {term} in {filename}")

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
