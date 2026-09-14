#!/usr/bin/env python3
"""User-terminal V2 verifier for Reality Action Feedback Loop v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_action_execution_boundary_model_v1.md": (
        "Execution Request Candidate", "Execution Status Candidate", "Outcome Evidence Candidate",
        "does not implement an Action",
    ),
    "cognitive_outcome_observation_model_v1.md": (
        "Goal progress", "Environment change", "User feedback", "Resource consumption",
        "Unexpected event", "not Evaluation",
    ),
    "cognitive_prediction_outcome_alignment_model_v1.md": (
        "Expected Outcome Candidate", "Difference Analysis Candidate", "Prediction Error Candidate",
        "does not immediately modify",
    ),
    "cognitive_reality_adaptation_interface_model_v1.md": (
        "Adaptive Correction Candidate Set", "strategy-adjustment candidate",
        "additional-observation candidate", "cannot automatically change",
    ),
    "cognitive_reality_failure_analysis_model_v1.md": (
        "Perception Failure", "Understanding Failure", "Decision Failure", "Execution Failure",
        "Environment Change", "Resource Constraint", "Unknown Cause",
    ),
    "cognitive_action_feedback_experience_boundary_v1.md": (
        "Experience Consolidation Candidate", "B Reflective Cognition", "does not become automatic learning",
    ),
    "cognitive_reality_action_feedback_whitebox_v1.md": (
        "```mermaid", "Execution Request Candidate", "Prediction–Outcome Alignment",
        "Adaptive Correction Candidate",
    ),
    "cognitive_reality_action_feedback_authority_matrix_v1.md": (
        "Action Execution Boundary", "Outcome Observation", "B Reflection", "sole State mutation authority",
    ),
    "cognitive_reality_action_feedback_loop_go_no_go_v1.md": (
        "Decision is not Action", "Outcome is not Evaluation", "No real Action Runtime",
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
