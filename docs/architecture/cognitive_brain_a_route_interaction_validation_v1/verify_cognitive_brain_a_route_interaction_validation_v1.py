#!/usr/bin/env python3
"""V2 final verifier for Brain–A Route interaction validation."""
from __future__ import annotations
import json
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
DOCS = {
 "cognitive_brain_a_route_interaction_validation_model_v1.md": ["Brain Original Purpose", "Intent expansion", "Brain supplies Attention direction", "A returns Reality/Situation/Risk/Capability/Decision candidates only"],
 "brain_intent_trace_contract_v1.md": ["structured provenance", "expansion drift", "attraction drift"],
 "brain_a_authority_boundary_validation_v1.md": ["final cognitive judgment", "Goal mutation", "sole State mutation authority"],
 "brain_feedback_alignment_metrics_v1.md": ["Intent Preservation", "Brain Authority Integrity", "A Autonomy Boundary", "Feedback Quality"],
 "brain_a_interaction_go_no_go_v1.md": ["Brain controls attention direction", "No model", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}
TERMS = ["safe_route_intent_injection", "pharmacy_intent_drift_detection", "exit_attention_governance", "a_route_risk_feedback_boundary", "brain_decision_review", "capability_constraint_upward_feedback", "outcome_feedback_quality"]

def main() -> int:
 root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
 failures=[]; checks=0
 for name, terms in DOCS.items():
  checks += 1; path=root/FLOW/name
  if not path.is_file(): failures.append(f"missing required file: {name}"); continue
  text=path.read_text(encoding="utf-8")
  for term in terms:
   checks += 1
   if term not in text: failures.append(f"missing required contract term: {term} in {name}")
 path=root/FLOW/"brain_attention_governance_test_cases_v1.json"; checks += 1
 if not path.is_file(): failures.append("missing required file: brain_attention_governance_test_cases_v1.json")
 else:
  try: text=path.read_text(encoding="utf-8"); data=json.loads(text)
  except (OSError,json.JSONDecodeError) as exc: failures.append(f"fixture parse failure: {type(exc).__name__}")
  else:
   checks += 1
   if data.get("fixture_type") != "deterministic_brain_a_route_interaction_validation": failures.append("wrong fixture type")
   for term in TERMS:
    checks += 1
    if term not in text: failures.append(f"missing required fixture contract: {term}")
 passed=checks-len(failures)
 print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {failures}"); print(f"PASSED_CHECK_COUNT: {passed}"); print(f"FAILED_CHECK_COUNT: {len(failures)}"); print(f"BLOCKER_COUNT: {len(failures)}")
 if failures: print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE"); print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 1
 print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"); return 0
if __name__ == "__main__": raise SystemExit(main())
