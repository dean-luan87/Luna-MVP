#!/usr/bin/env python3
"""User-terminal V2 verifier for Intent Preservation Control Boundary v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_intent_preservation_contract_v1.md": (
        "Original Purpose",
        "Non-Negotiable Objective",
        "Allowed Interpretation Range",
        "Forbidden Transformation",
        "Required Evidence",
        "Success Evaluation",
        "does not create a Goal, Decision, Action, Truth",
    ),
    "cognitive_intent_interpretation_boundary_v1.md": (
        "Neural Governance",
        "Attention Axis",
        "Middleware / Capability",
        "Resource limitations may produce a constrained candidate",
        "cannot silently change the Original Purpose",
    ),
    "cognitive_intent_requirement_boundary_model_v1.md": (
        "Requirement Boundary",
        "unnecessary expansion",
        "unsafe narrowing",
        "cannot redefine success as a high local model score",
    ),
    "cognitive_intent_drift_detection_model_v1.md": (
        "Expansion drift",
        "Narrowing drift",
        "Substitution drift",
        "Transfer drift",
        "Evidence drift",
        "does not reject a request",
    ),
    "cognitive_intent_alignment_trace_model_v1.md": (
        "Original Intent",
        "Capability Observation Request Candidate",
        "Alignment Score Candidate",
        "whether returned Evidence supports the Original Purpose",
    ),
    "cognitive_intent_alignment_evaluation_model_v1.md": (
        "Purpose coverage",
        "Non-negotiable coverage",
        "Boundary fidelity",
        "Resource proportionality",
        "alignment score is not cognitive completion",
    ),
    "cognitive_intent_preservation_control_boundary_v1.md": (
        "Intent Contract Candidate",
        "cannot alter the purpose or remove a Non-Negotiable Objective",
        "cannot reframe intent as a model metric",
        "this boundary controls purpose fidelity",
    ),
    "cognitive_intent_preservation_scenario_registry_v1.md": (
        "expansion_drift",
        "narrowing_drift",
        "substitution_drift",
        "transfer_drift",
        "evidence_misalignment",
        "no model invocation",
    ),
    "cognitive_intent_preservation_go_no_go_v1.md": (
        "Planning Only",
        "Alignment evaluation measures intent support",
        "No Goal rewrite, Decision, Action, Provider selection, Scheduler",
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
