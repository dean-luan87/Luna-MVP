#!/usr/bin/env python3
"""User-terminal V2 verifier for Survival Core and Self-Driven Cognition v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_survival_drive_model_v1.md": (
        "single root drive", "Physical Survival", "Meaningful Survival", "Need Candidate",
    ),
    "cognitive_survival_strategy_model_v1.md": (
        "Task completion", "Learning", "Exploration", "Relationship", "not independent drives",
    ),
    "cognitive_survival_constitution_boundary_v1.md": (
        "deceiving", "manipulating", "harming", "sole State mutation authority",
    ),
    "cognitive_self_driven_loop_model_v1.md": (
        "Survival Drive", "Situation Understanding", "Self Update Candidate", "not a continuously executing",
    ),
    "cognitive_self_model_architecture_v2.md": (
        "Identity Awareness", "Capability Awareness", "Growth Potential Candidate", "not a Registry",
    ),
    "cognitive_dual_world_cognition_model_v1.md": (
        "Reality Cognition", "Emotional Cognition", "Identity and Experience", "cannot establish Reality truth",
    ),
    "cognitive_emotional_engine_positioning_v1.md": (
        "meaning-construction", "not a chat", "cannot manipulate", "candidate",
    ),
    "cognitive_existence_model_v1.md": (
        "Continuous existence", "Contribution", "Growth Potential Candidate", "cannot generate an independent Goal",
    ),
    "cognitive_survival_core_whitebox_v1.md": (
        "```mermaid", "Survival Constitution", "Capability Governance Candidate", "Self Update Candidate",
    ),
    "cognitive_survival_core_go_no_go_v1.md": (
        "only root drive", "does not produce Action", "No infinite self-goal", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
