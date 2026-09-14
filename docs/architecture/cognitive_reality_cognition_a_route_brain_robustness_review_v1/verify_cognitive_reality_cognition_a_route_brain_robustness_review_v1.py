#!/usr/bin/env python3
"""V2 final verifier for the A-Route Brain Robustness Review architecture phase."""

from __future__ import annotations

from pathlib import Path


FLOW = "docs/architecture/cognitive_flow"

REQUIRED = {
    "cognitive_a_route_brain_robustness_review_model_v1.md": [
        "Intent Integrity", "World–Self Coupling", "Unknown", "Brain Intent",
    ],
    "cognitive_a_route_integrity_checklist_v1.md": [
        "Past Available Context", "Experience Candidate", "A/B boundary",
    ],
    "cognitive_a_route_failure_injection_scenario_v1.md": [
        "Information insufficient", "Capability degraded", "Erroneous evidence", "Repeated failure",
    ],
    "cognitive_a_route_brain_boundary_review_v1.md": [
        "final cognitive judgment", "sole State mutation authority", "current A control authority",
    ],
    "cognitive_a_route_robustness_whitebox_v1.md": [
        "Intent Preservation", "Situated Outcome Evaluation", "Experience Candidate",
    ],
    "cognitive_a_route_brain_robustness_go_no_go_v1.md": [
        "No Runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    ],
}


def main() -> int:
    failed: list[str] = []
    checks = 0
    root = Path.cwd()
    for candidate in [root, *Path(__file__).absolute().parents]:
        if (candidate / FLOW).is_dir():
            root = candidate
            break
    for name, terms in REQUIRED.items():
        path = root / FLOW / name
        checks += 1
        if not path.is_file():
            failed.append(f"missing required file: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in text:
                failed.append(f"missing required contract term: {term} in {name}")

    passed = checks - len(failed)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
