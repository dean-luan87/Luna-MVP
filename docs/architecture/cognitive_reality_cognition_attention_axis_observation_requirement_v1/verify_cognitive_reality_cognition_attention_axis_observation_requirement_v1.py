#!/usr/bin/env python3
"""User-terminal V2 verifier for Attention Axis and Observation Requirement v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_attention_intent_contract_v1.md": (
        "Purpose",
        "Cognitive Direction",
        "Required Context",
        "Time Requirement",
        "Confidence Requirement",
        "Priority Candidate",
        "cannot create a Goal, Survival Drive, Decision, or Action",
    ),
    "cognitive_attention_requirement_model_v1.md": (
        "Target Domain",
        "Observation Scope",
        "Region Candidate",
        "Object Candidate",
        "Information Need",
        "Evidence Type",
        "Unknown Requirement",
        "not a detection specification",
    ),
    "cognitive_attention_refinement_model_v1.md": (
        "Current Situation Candidate",
        "Available Capability Context",
        "Experience Reference",
        "Capability Observation Candidate",
        "does not select YOLO, SAM, OCR",
    ),
    "cognitive_attention_axis_model_v1.md": (
        "Direction",
        "Region",
        "Entity",
        "Attribute",
        "Relationship",
        "does not assert that an entity exists",
    ),
    "cognitive_attention_feedback_contract_v1.md": (
        "Coverage Candidate",
        "Evidence Obtained Reference",
        "Missing Information Candidate",
        "Failure Reason Candidate",
        "does not correct evidence",
    ),
    "cognitive_attention_trace_model_v1.md": (
        "Attention Intent",
        "Attention Requirement",
        "Capability Observation Candidate",
        "Situation Impact Candidate",
        "why did Luna look here?",
    ),
    "cognitive_attention_axis_system_boundary_v1.md": (
        "Capability Observation Request Candidate",
        "Attention Requirement != Automatic Frequency Adjustment",
        "does not own device frequency",
    ),
    "cognitive_attention_axis_storage_experience_boundary_v1.md": (
        "Working Attention Context Candidate",
        "Attention Pattern Candidate",
        "does not preserve all attention history",
        "No candidate in this phase automatically modifies Attention strategy",
    ),
    "cognitive_attention_axis_scenario_registry_v1.md": (
        "multi_object_competition",
        "goal_change_axis_shift",
        "constrained_observation",
        "observation_failure",
        "self_difference",
        "No Attention Runtime",
    ),
    "cognitive_attention_axis_observation_requirement_go_no_go_v1.md": (
        "Planning Only",
        "Attention Requirement != Automatic Frequency Adjustment",
        "No automatic model call",
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
