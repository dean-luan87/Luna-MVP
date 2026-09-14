#!/usr/bin/env python3
"""User-terminal V2 verifier for Attention Alignment and Allocation v1."""
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
REQUIRED = {
    "cognitive_attention_allocation_model_v1.md": ("Intent Relevance Candidate", "Survival Impact Candidate", "Temporal Urgency Candidate", "Information Value Candidate", "Attention Allocation Candidate", "Complete Observation != Optimal Cognition"),
    "cognitive_attention_alignment_model_v1.md": ("Original Intent", "Attention Alignment Evaluation Candidate", "low alignment", "does not decide, act, retry a Provider"),
    "cognitive_attention_drift_model_v1.md": ("Expansion Drift", "Narrowing Drift", "Replacement Drift", "Attraction Drift", "Persistence Drift", "do not modify Goal"),
    "cognitive_attention_alignment_feedback_contract_v1.md": ("Intent Match Candidate", "Information Value Candidate", "Waste Candidate", "Improvement Candidate", "does not assert Truth"),
    "cognitive_attention_alignment_neural_boundary_v1.md": ("Neural Resource Evaluation Candidate", "Allowed Attention Allocation Candidate", "cannot allocate actual resources or modify frequency", "one cognitive objective only"),
    "cognitive_attention_alignment_scenario_registry_v1.md": ("goal_relevant_information", "high_attraction_distraction", "insufficient_information", "constrained_resource", "task_completed", "No multi-A coordination"),
    "cognitive_attention_alignment_allocation_go_no_go_v1.md": ("Planning Only", "Minimal sufficient information", "No runtime", "WAITING_FOR_USER_TERMINAL_VERIFICATION"),
}

def root() -> Path:
    for candidate in [Path.cwd(), *Path(__file__).absolute().parents]:
        if (candidate / FLOW).is_dir():
            return candidate
    raise FileNotFoundError("repository root not found")

def main() -> int:
    failures=[]; checks=0; repo=root()
    for filename, terms in REQUIRED.items():
        target=repo/FLOW/filename; checks += 1
        if not target.is_file():
            failures.append(f"missing required file: {target.relative_to(repo)}"); continue
        text=target.read_text(encoding="utf-8")
        for term in terms:
            checks += 1
            if term not in text: failures.append(f"missing required contract term: {term} in {filename}")
    print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks-len(failures)}"); print(f"FAILED_CHECK_COUNT: {len(failures)}"); print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE"); print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
