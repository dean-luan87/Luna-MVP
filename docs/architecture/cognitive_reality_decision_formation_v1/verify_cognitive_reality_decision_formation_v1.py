#!/usr/bin/env python3
"""User-terminal V2 verifier for Reality Decision Formation architecture v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_decision_formation_model_v1.md": (
        "Situation Candidate", "Option Generation Candidate Set", "Decision Candidate",
        "Future Execution Candidate Boundary", "Situation Understanding",
    ),
    "cognitive_decision_option_generation_model_v1.md": (
        "not a recommendation", "Self Capability", "Experience", "Survival Strategy", "no option is preferred",
    ),
    "cognitive_decision_evaluation_model_v1.md": (
        "Survival Impact", "Goal Alignment", "Capability Fit", "Resource Cost",
        "Risk and Uncertainty", "Experience Reference",
    ),
    "cognitive_decision_priority_model_v1.md": (
        "Survival Continuity", "Safety / Non-harm", "Critical Goal", "Efficiency", "Optimization",
    ),
    "cognitive_fast_decision_path_model_v1.md": (
        "Fast Path", "Normal Path", "Deep Evaluation Path", "not an Action", "No path creates a Scheduler",
    ),
    "cognitive_decision_confidence_model_v1.md": (
        "Decision Confidence Candidate", "Low confidence", "request user confirmation", "cannot force a decision",
    ),
    "cognitive_decision_survival_alignment_model_v1.md": (
        "Expected Outcome Candidate", "Survival Value Estimation Candidate", "not a Reward calculation", "Survival Constitution",
    ),
    "cognitive_decision_reflection_interface_model_v1.md": (
        "Reflection Candidate", "cannot modify the past", "current Decision Candidate in real time", "Adoption Candidate",
    ),
    "cognitive_reality_decision_whitebox_v1.md": (
        "```mermaid", "Decision Candidate", "Brain Evaluation / Approval Candidate", "Future Capability Execution Boundary",
    ),
    "cognitive_reality_decision_authority_matrix_v1.md": (
        "Brain", "Neural Governance", "Middleware", "B Reflection", "sole State mutation authority",
    ),
    "cognitive_reality_decision_formation_go_no_go_v1.md": (
        "Situation is not Decision", "Decision is not Action", "B Reflection cannot affect", "No Action execution",
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
