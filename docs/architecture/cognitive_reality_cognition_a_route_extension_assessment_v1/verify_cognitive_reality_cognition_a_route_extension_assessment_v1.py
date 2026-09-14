#!/usr/bin/env python3
"""User-terminal V2 verifier for A-Route Extension Assessment v1."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_reality_a_route_extension_taxonomy_v1.md": (
        "Temporal Extension", "Spatial Extension", "Attention Extension", "Social Extension",
        "Multi-Agent Extension", "Uncertainty Extension", "assess only",
    ),
    "cognitive_reality_extension_boundary_model_v1.md": (
        "Brain Perspective Management", "Cognitive Process Ecology / Assembly",
        "B Reflective Cognition / Emotional Cognition", "No extension may alter",
    ),
    "cognitive_reality_extension_priority_model_v1.md": (
        "A Core impact", "First-person life value", "Decision quality gain",
        "Engineering complexity", "Priority Candidate",
    ),
    "cognitive_reality_extension_interface_contract_v1.md": (
        "Evidence Extension", "Situation Enhancement Candidate", "Decision Support Candidate",
        "cannot directly modify", "simulation-baseline regression requirements",
    ),
    "cognitive_reality_extension_review_matrix_v1.md": (
        "Brain Perspective Management", "Process Ecology / Assembly", "B Reflection",
        "future Context Integration", "must not be implemented through A internals",
    ),
    "cognitive_reality_a_route_extension_assessment_go_no_go_v1.md": (
        "Role Perspective", "Multi-A coordination", "No Role Model",
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
