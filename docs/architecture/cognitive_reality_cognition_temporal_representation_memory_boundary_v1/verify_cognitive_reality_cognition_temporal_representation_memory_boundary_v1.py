#!/usr/bin/env python3
"""User-terminal V2 verifier for Temporal Representation and Memory Boundary v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_temporal_evidence_boundary_v1.md": (
        "timestamp or ordering reference",
        "Temporal Candidate",
        "does not directly enter Decision, Action, Experience",
        "Raw continuous observation is not Temporal Memory",
    ),
    "cognitive_temporal_representation_model_v1.md": (
        "Current State Reference",
        "Previous Reference",
        "Change Delta Candidate",
        "Transition Pattern Candidate",
        "Stability Candidate",
        "Trend Candidate",
        "Confidence Candidate",
        "Trend Candidate != Future Fact",
    ),
    "cognitive_temporal_storage_hierarchy_v1.md": (
        "Level 0: Transient Temporal State",
        "Level 1: Working Temporal Context",
        "Level 2: Temporal Pattern Candidate",
        "not state mutation or Memory write",
        "Experience validation and Adoption",
    ),
    "cognitive_temporal_compression_policy_v1.md": (
        "not a time database",
        "Goal relevance",
        "Survival impact",
        "Change magnitude",
        "does not write Memory",
    ),
    "cognitive_temporal_experience_interface_v1.md": (
        "Temporal Context Candidate",
        "Validation",
        "Future Memory / Knowledge Candidate",
        "No temporal artifact directly enters B Reflection",
    ),
    "cognitive_temporal_self_coupling_model_v1.md": (
        "Self Capability Context",
        "Goal Context",
        "Resource Context",
        "does not change Self Model",
    ),
    "cognitive_temporal_neural_boundary_v1.md": (
        "Situation Risk Candidate",
        "Tempo Adjustment Candidate",
        "does not create a Tempo Adjustment Candidate",
        "Scheduler",
    ),
    "cognitive_temporal_world_memory_integration_boundary_v1.md": (
        "does not connect Field Kernel",
        "World Model Runtime",
        "Future Knowledge / Memory Candidate",
        "Reducer remains the sole State mutation authority",
    ),
    "cognitive_temporal_scenario_registry_v1.md": (
        "stable_environment",
        "gradual_resource_decline",
        "abrupt_obstacle_change",
        "cyclic_illumination",
        "subject_difference",
        "no full-history storage",
    ),
    "cognitive_temporal_representation_memory_boundary_go_no_go_v1.md": (
        "Planning Only",
        "No time database",
        "does not create Tempo Adjustment Candidate itself",
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
