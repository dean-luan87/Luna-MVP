#!/usr/bin/env python3
"""User-terminal V2 verifier for Reality–Reflection Dual Loop v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_reflection_dual_loop_model_v1.md": (
        "A: Reality Cognition", "B: Reflective Cognition", "do not share control authority",
    ),
    "cognitive_reflection_space_model_v1.md": (
        "Cognitive Reflection Space", "not a game world", "not a Simulation Runtime", "cannot execute a plan",
    ),
    "cognitive_imagination_space_boundary_model_v1.md": (
        "Engineering Simulation", "Cognitive Imagination Space", "Hypothesis → Validation → Reality Feasibility → Adoption Candidate",
    ),
    "cognitive_counterfactual_reflection_model_v1.md": (
        "Counterfactual Reflection", "does not rewrite what", "cannot recast history as fact",
    ),
    "cognitive_hypothetical_resource_model_v1.md": (
        "hypothetical_capability", "Hypothetical resources cannot enter Self Model", "Reality Decision Candidate",
    ),
    "cognitive_reflection_depth_model_v1.md": (
        "Event replay", "Capability analysis", "Identity analysis", "Future imagination",
    ),
    "cognitive_ab_reflection_boundary_contract_v1.md": (
        "B cannot directly modify A", "does not execute a B candidate", "sole State mutation authority",
    ),
    "cognitive_reflective_resource_budget_model_v1.md": (
        "Reflective Resource Budget Candidate", "not a Scheduler", "permission to preempt A",
    ),
    "cognitive_reflection_strategy_return_model_v1.md": (
        "Reality Feasibility Assessment", "Adoption Candidate", "No return automatically changes A",
    ),
    "cognitive_reality_reflection_whitebox_v1.md": (
        "```mermaid", "B Reflective Cognition", "future governed influence only", "direct B-to-A control path",
    ),
    "cognitive_reality_reflection_authority_matrix_v1.md": (
        "use hypothetical resource as fact", "direct A control", "sole State mutation authority",
    ),
    "cognitive_reality_reflection_dual_loop_go_no_go_v1.md": (
        "not a Simulation Runtime", "Hypothetical resources cannot enter", "No Simulation Runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
