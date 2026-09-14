#!/usr/bin/env python3
"""User-terminal V2 verifier for A-Route Attention Management Extension v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_reality_attention_context_model_v1.md": (
        "Target Candidate",
        "Relevance Candidate",
        "Risk Candidate",
        "Goal Alignment Candidate",
        "Temporal Change Candidate",
        "Uncertainty Candidate",
        "Resource Cost Candidate",
        "Attention Selection != Reality Judgment",
    ),
    "cognitive_reality_attention_source_model_v1.md": (
        "Survival Attention",
        "Goal Attention",
        "Temporal Attention",
        "Self Attention",
        "Social Attention Interface",
        "no relationship graph or Role System",
    ),
    "cognitive_reality_attention_observation_boundary_v1.md": (
        "Information Prioritization Candidate",
        "Observation Request Candidate",
        "does not invoke a model, camera, sensor, Provider",
        "does not decide cognitive goals, facts, situations, or actions",
    ),
    "cognitive_reality_attention_lifecycle_extension_v1.md": (
        "Activated Candidate",
        "Maintained Candidate",
        "Reduced Candidate",
        "Released Candidate",
        "not persistent State, Memory, a task queue, Scheduler, or Action",
    ),
    "cognitive_reality_attention_neural_resource_boundary_v1.md": (
        "Situation Importance Candidate",
        "Neural Resource Allocation Candidate",
        "does not set tempo",
        "does not turn attention selection into Reality",
    ),
    "cognitive_reality_attention_temporal_field_alignment_v1.md": (
        "Temporal Change Candidate",
        "Attention Axis Candidate",
        "not a filter that deletes unselected entities",
        "Field Kernel integration is explicitly not implemented",
    ),
    "cognitive_reality_attention_storage_experience_boundary_v1.md": (
        "Instant Attention Candidate",
        "Working Attention Context Candidate",
        "Attention Pattern Candidate",
        "Validation",
        "cannot directly modify attention strategy",
    ),
    "cognitive_reality_attention_management_integration_model_v1.md": (
        "A-Route Extension Interface Contract",
        "not a parallel decision loop",
        "Brain retains final Decision judgment",
        "Reducer remains the sole State mutation authority",
    ),
    "cognitive_reality_attention_scenario_registry_v1.md": (
        "multi_target_competition",
        "dynamic_hazard_change",
        "goal_shift",
        "constrained_resources",
        "self_capability_difference",
        "No case may introduce Attention Runtime",
    ),
    "cognitive_reality_attention_management_go_no_go_v1.md": (
        "Planning Only",
        "Attention Selection != Reality Judgment",
        "No Attention Runtime",
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
