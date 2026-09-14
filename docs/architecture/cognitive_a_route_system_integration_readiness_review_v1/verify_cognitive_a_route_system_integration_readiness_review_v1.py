#!/usr/bin/env python3
"""V2 static verifier for A Route system integration readiness review."""
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
REQ = {
    "a_route_system_integration_review_model_v1.md": ["system-level architecture review", "Brain", "A Route", "Reality Workspace", "Neural System", "Governance", "24-hour", "state inflation", "authority drift"],
    "cognitive_layer_authority_matrix_v2.md": ["Intent", "Goal", "final judgment", "direct hardware call", "Situation", "Decision Candidate", "Outcome Interpretation", "fast response", "risk escalation", "capability description", "sole State mutation authority"],
    "information_flow_integrity_review_v1.md": ["External Capability → Evidence → Reality Workspace → Situation → Decision Candidate → Outcome → Experience Candidate", "Model Output → Decision", "Model Output → Goal", "Emotion or Goal", "Reality Confirmation", "Evidence Candidate"],
    "self_awareness_loop_review_v1.md": ["Hardware State", "Capability State", "Self Capability Candidate", "A Route Evaluation", "Decision Constraint", "Camera health degraded", "visual reliability limited", "Identity remains stable", "Reducer remains the sole State mutation authority"],
    "resource_governance_review_v1.md": ["compute", "battery", "attention", "memory", "network", "Information Value", "Resource Cost", "Allocation Candidate", "not a Scheduler", "Unlimited-thinking guard"],
    "long_running_stability_review_v1.md": ["24-hour", "No state inflation", "No authority drift", "No experience contamination", "Unknown preservation", "Identity continuity", "Candidate, Active, Stale, and Expired"],
    "system_whitebox_v1.md": ["External Capability", "Evidence", "Reality Workspace", "Situation", "Decision Candidate", "Hardware State", "Self Capability Candidate", "Brain Final Judgment", "Model Output", "Reducer remains the sole State mutation authority"],
    "go_no_go_v1.md": ["Brain owns Intent", "A Route owns Situation", "Neural owns fast response", "Registry owns capability description", "External Capability → Evidence → Reality Workspace → Situation → Decision Candidate → Outcome → Experience Candidate", "Model output cannot directly change Emotion or Goal", "Resource Governance prevents unlimited thinking", "24-hour review", "No real model", "No OCR", "No SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in REQ.items():
        checks += 1
        path = root / FLOW / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
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
