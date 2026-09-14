#!/usr/bin/env python3
"""User-terminal V2 verifier for A-Route Reality Cognition Foundation Closure v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_cognition_constitution_v1.md": (
        "Reality First", "Self Situated Understanding", "Candidate Only", "Feedback Driven",
        "Situation is not Decision", "sole State mutation authority",
    ),
    "cognitive_reality_route_layer_architecture_v1.md": (
        "L0 Survival Constitution", "L1 Brain Cognitive Layer", "L2 Neural Governance Layer",
        "L3 Reality Understanding Layer", "L4 Capability Boundary Layer", "L5 Outcome Feedback Layer",
    ),
    "cognitive_reality_reflection_interface_boundary_v2.md": (
        "Experience Candidate", "Strategy Improvement Candidate", "B cannot affect Current Decision",
        "without sharing responsibility or control authority",
    ),
    "cognitive_reality_loop_health_model_v1.md": (
        "Perception Health", "Understanding Health", "Decision Health", "Feedback Health",
        "not a health Runtime",
    ),
    "cognitive_reality_loop_failure_boundary_v1.md": (
        "Perception Failure Candidate", "Situation Failure Candidate", "Outcome Deviation Candidate",
        "Adaptation Failure Candidate", "Unknown Cause",
    ),
    "cognitive_reality_route_whitebox_v1.md": (
        "```mermaid", "Execution Boundary", "Value Feedback Candidate", "A-to-B governed interface",
    ),
    "cognitive_reality_route_authority_matrix_v1.md": (
        "L0 Survival Constitution", "L5 Feedback / Experience", "B Reflection", "sole State mutation authority",
    ),
    "cognitive_reality_route_foundation_closure_go_no_go_v1.md": (
        "architecture foundation closure", "not a claim that a real", "No B deep-design expansion",
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
