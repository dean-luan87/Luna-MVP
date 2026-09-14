#!/usr/bin/env python3
"""User-terminal V2 verifier for Situated World Understanding architecture v1."""

from __future__ import annotations

import argparse
from pathlib import Path


PHASE = "cognitive_situated_world_understanding_v1"
FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_world_self_coupling_model_v1.md": [
        "World State + Self Model + Goal Context + Resource Context",
        "Situation Candidate",
        "does not establish truth",
    ],
    "cognitive_self_situated_position_model_v1.md": [
        "Physical", "Capability", "Resource", "Cognitive",
    ],
    "cognitive_situation_assessment_model_v1.md": [
        "Situation Candidate", "Reality is not Situation", "Experience",
    ],
    "cognitive_action_feasibility_interface_v1.md": [
        "Feasibility Candidate", "Currently Impossible", "does not execute",
    ],
    "cognitive_dual_cognition_boundary_model_v1.md": [
        "Reality Cognition", "Emotional Cognition", "cannot convert",
    ],
    "cognitive_situated_understanding_authority_matrix_v1.md": [
        "Evidence Gateway", "Middleware", "sole State mutation authority",
    ],
    "cognitive_situated_understanding_whitebox_v1.md": [
        "```mermaid", "Situation Candidate", "Brain Context",
    ],
    "cognitive_situated_world_understanding_go_no_go_v1.md": [
        "No Runtime", "automatic action", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}


def repository_root() -> Path:
    here = Path(__file__).absolute()
    candidates = [Path.cwd(), *here.parents]
    for candidate in candidates:
        if (candidate / FLOW).is_dir():
            return candidate
    raise FileNotFoundError("repository root with docs/architecture/cognitive_flow was not found")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="/private/tmp/luna-situated-world-understanding-v1")
    parser.parse_args()

    root = repository_root()
    failures: list[str] = []
    checks = 0
    for name, terms in REQUIRED.items():
        target = root / FLOW / name
        checks += 1
        if not target.is_file():
            failures.append(f"missing required file: {target.relative_to(root)}")
            continue
        text = target.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")

    passed = checks - len(failures)
    blocked = len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {blocked}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
