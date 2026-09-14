#!/usr/bin/env python3
"""User-terminal V2 verifier for Reality Cognition System Readiness Review v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_cognition_system_readiness_review_model_v1.md": (
        "Input completeness", "Output completeness", "Closed-loop continuity",
        "Traceability", "Failure locality", "Simulation boundary",
    ),
    "cognitive_reality_loop_completeness_review_v1.md": (
        "Reality Evidence", "Situation Candidate", "Decision Candidate", "Outcome Reference",
        "Experience Candidate", "Completeness does not mean correctness",
    ),
    "cognitive_reality_decision_trace_contract_v1.md": (
        "Available Option Candidates", "Evaluation Factors", "Expected Outcome Candidate",
        "confidence_and_unknowns", "must not fabricate a selected action",
    ),
    "cognitive_reality_outcome_trace_contract_v1.md": (
        "Goal Result", "Risk Change", "Resource Cost", "Environment Change",
        "User Feedback", "Unexpected Event", "Unknown / Missing Observation",
    ),
    "cognitive_reality_failure_trace_review_v1.md": (
        "Perception", "Understanding", "Situation", "Decision", "Execution",
        "Environment", "Resource", "Unknown Cause",
    ),
    "cognitive_reality_experience_interface_readiness_v1.md": (
        "context_ref", "decision_trace_ref", "outcome_ref", "difference_ref",
        "failure_type_candidates", "value_impact_ref", "confidence_and_unknowns",
    ),
    "cognitive_reality_simulation_scenario_registry_model_v1.md": (
        "Basic", "Complex", "Extreme", "not a runtime registry", "does not test whether an AI is generally intelligent",
    ),
    "cognitive_reality_simulation_test_boundary_v1.md": (
        "Controlled Scenario Input", "Injected Outcome Reference", "does not prove general intelligence",
        "does not execute a real Action",
    ),
    "cognitive_reality_cognition_system_readiness_go_no_go_v1.md": (
        "A loop is complete", "Experience interface", "do not implement a simulation Runtime",
        "No B deepening", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
        text = target.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in text:
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
