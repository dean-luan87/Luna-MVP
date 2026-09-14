#!/usr/bin/env python3
"""User-terminal V2 verifier for A-Route Closure and Handoff v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED: dict[str, tuple[str, ...]] = {
    "cognitive_reality_cognition_final_contract_v1.md": (
        "stable A-route foundation", "does not own Personality formation",
        "does not execute Actions", "sole State mutation authority",
    ),
    "cognitive_reality_cognition_final_architecture_map_v1.md": (
        "```mermaid", "World Understanding", "Self Understanding", "Decision Formation",
        "Action Feedback", "Experience Interface", "Reflection System B",
    ),
    "cognitive_reality_experience_handoff_contract_v1.md": (
        "Experience Package", "Situation Context", "Decision Trace", "Actual Outcome",
        "Failure Classification", "Unknown Factors", "delayed reflection",
    ),
    "cognitive_reality_simulation_baseline_contract_v1.md": (
        "level1_gully_child", "level3_capability_constraint", "Self Awareness",
        "deterministic replay", "not a Runtime input",
    ),
    "cognitive_reality_regression_boundary_v1.md": (
        "A Route Extension Capability", "Reality First", "Self Situated Understanding",
        "Candidate Only", "Decision ≠ Action ≠ Outcome", "baseline simulation revalidation",
    ),
    "cognitive_reality_authority_final_matrix_v1.md": (
        "Survival Constitution", "B Reflection", "sole State mutation authority",
        "No row creates a Runtime",
    ),
    "cognitive_reality_cognition_whitebox_final_v1.md": (
        "```mermaid", "Decision Candidate", "Outcome Evidence", "Experience Candidate",
        "delayed future candidate only",
    ),
    "cognitive_reality_cognition_a_route_closure_handoff_go_no_go_v1.md": (
        "seven scenario fixtures", "A Route Extension Capability", "B remains delayed",
        "No B deepening", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
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
