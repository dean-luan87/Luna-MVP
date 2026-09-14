#!/usr/bin/env python3
"""User-terminal V2 verifier for Reality Cognition System Encapsulation v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_cognition_system_encapsulation_model_v1.md": (
        "Reality Cognition System", "World Understanding", "Self Understanding",
        "Decision Formation", "Action Feedback", "Adaptation Feedback",
    ),
    "cognitive_reality_cognition_system_interface_contract_v1.md": (
        "Reality Evidence", "Self State / Self Capability Context", "Goal Context",
        "Situation Candidate", "Decision Candidate", "Outcome Reference", "Experience Candidate",
    ),
    "cognitive_reality_cognition_system_internal_boundary_contract_v1.md": (
        "World Model", "Self Model", "Situation Understanding", "Decision Formation",
        "cannot implement an Action", "cannot modify Self, Strategy, or State directly",
    ),
    "cognitive_reality_cognition_system_reflection_interface_v1.md": (
        "B Reflective Cognition", "Validation → Reality Feasibility → Adoption Candidate",
        "cannot directly access or modify internal A modules", "in real time",
    ),
    "cognitive_reality_cognition_system_whitebox_v1.md": (
        "```mermaid", "Reality Evidence", "Decision Formation", "Experience Candidate",
        "external A-to-B interface only",
    ),
    "cognitive_reality_cognition_system_authority_matrix_v1.md": (
        "not a", "direct internal A access", "sole State mutation authority",
        "does not transfer Brain",
    ),
    "cognitive_reality_cognition_system_encapsulation_go_no_go_v1.md": (
        "not a", "Only Reality Evidence", "cannot directly access internal",
        "Existing A Route Constitution is reused", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
