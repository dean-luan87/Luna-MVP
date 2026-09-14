#!/usr/bin/env python3
"""User-terminal V2 verifier for Brain Perspective Context Interface v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_perspective_context_contract_v1.md": (
        "Perspective Source", "Role Reference", "Relationship Reference",
        "Emotional Weight Candidate", "Responsibility Weight Candidate",
        "Attention Bias Candidate", "Decision Preference Candidate", "Boundary Constraint",
    ),
    "cognitive_emotion_influence_boundary_v1.md": (
        "does not modify Reality", "does not directly create an Action",
        "does not override Survival Constitution", "value weights", "possibility space",
    ),
    "cognitive_role_reference_placeholder_v1.md": (
        "unknown_social_role", "future_emotional_engine", "Placeholder only",
        "Role selection and Perspective Management remain Brain-level",
    ),
    "cognitive_brain_a_perspective_decision_interface_v1.md": (
        "does not enter World Understanding", "Situation Candidate",
        "Perspective Context Candidate", "Decision Evaluation Weight Candidates", "Brain Evaluation",
    ),
    "cognitive_perspective_reality_emotion_dual_boundary_v1.md": (
        "Reality Cognition / A", "Emotional Cognition", "Perspective Context",
        "Reality fact and emotional meaning remain separate",
    ),
    "cognitive_brain_perspective_context_interface_go_no_go_v1.md": (
        "does not enter World Understanding", "does not modify Reality",
        "Role Reference is a placeholder only", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
