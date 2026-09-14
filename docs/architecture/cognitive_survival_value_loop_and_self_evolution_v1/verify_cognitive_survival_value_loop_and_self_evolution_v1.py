#!/usr/bin/env python3
"""User-terminal V2 verifier for Survival Value Loop and Self Evolution v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_survival_value_feedback_model_v1.md": (
        "Physical Survival Value", "Capability Survival Value", "Relationship Survival Value",
        "Meaning Survival Value", "Value ≠ Truth", "Value ≠ Reward",
    ),
    "cognitive_self_evaluation_model_v1.md": (
        "World adaptation", "Self understanding", "Existence effectiveness",
        "Self Evaluation Candidate", "cannot decide",
    ),
    "cognitive_survival_strategy_effectiveness_model_v1.md": (
        "strategy pattern", "single Action", "Strategy Effectiveness Candidate", "relationship friction",
    ),
    "cognitive_experience_self_update_model_v2.md": (
        "Pattern Extraction Candidate", "Validation", "Adoption Review",
        "A single event cannot change Self Model", "sole State mutation authority",
    ),
    "cognitive_cognitive_adaptation_model_v1.md": (
        "Strategy", "Capability Usage", "Resource Allocation", "Observation Preference",
        "does not automatically alter Attention",
    ),
    "cognitive_survival_intelligence_model_v1.md": (
        "what is worth noticing", "Survival Intelligence Guidance Candidate", "does not choose a", "Action",
    ),
    "cognitive_survival_value_loop_whitebox_v1.md": (
        "```mermaid", "Survival Value Feedback Candidate", "Self Evaluation Candidate",
        "Self Update Candidate", "Survival Constitution",
    ),
    "cognitive_survival_value_loop_authority_matrix_v1.md": (
        "Emotional Cognition", "Reality Cognition", "Middleware", "sole State mutation authority",
    ),
    "cognitive_survival_value_loop_go_no_go_v1.md": (
        "not Reward", "does not directly modify Strategy", "No online learning",
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
