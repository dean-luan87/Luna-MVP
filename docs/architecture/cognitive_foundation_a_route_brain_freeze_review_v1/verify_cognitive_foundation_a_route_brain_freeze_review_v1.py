#!/usr/bin/env python3
"""V2 final verifier for cognitive foundation freeze review."""
from pathlib import Path
FLOW="docs/architecture/cognitive_flow"
REQ={
"cognitive_foundation_freeze_contract_v1.md":["Survival Drive","Brain owns Intent","Reducer remains sole State mutation authority"],
"a_route_brain_final_authority_matrix_v1.md":["Decision Acceptance","Goal/Value/Self-definition mutation","sole State mutation authority"],
"cognitive_information_flow_final_boundary_v1.md":["Evidence → Reality Representation","Model Evidence","Reality Confirmation"],
"self_model_continuity_freeze_contract_v1.md":["Identity Layer","Capability Layer","Experience Layer","Validation → Adoption"],
"a_b_future_extension_boundary_v1.md":["Experience Candidate","B cannot control A in real time","Capability extensions cannot change the cognitive subject"],
"cognitive_failure_diagnosis_boundary_v1.md":["Evidence Failure","Experience Governance Failure"],
"cognitive_foundation_regression_baseline_v1.md":["Level 1 Situation Formation","Brain Interaction"],
"a_route_brain_freeze_review_go_no_go_v1.md":["No Model Manager","WAITING_FOR_USER_TERMINAL_VERIFICATION"]}
def main():
 root=next((p for p in [Path.cwd(),*Path(__file__).absolute().parents] if (p/FLOW).is_dir()),Path.cwd()); failures=[]; checks=0
 for n,ts in REQ.items():
  checks+=1; p=root/FLOW/n
  if not p.is_file(): failures.append(f"missing required file: {n}"); continue
  s=p.read_text()
  for t in ts:
   checks+=1
   if t not in s: failures.append(f"missing required contract term: {t} in {n}")
 print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {failures}"); print(f"PASSED_CHECK_COUNT: {checks-len(failures)}"); print(f"FAILED_CHECK_COUNT: {len(failures)}"); print(f"BLOCKER_COUNT: {len(failures)}")
 if failures: print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE"); print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 1
 print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"); return 0
if __name__=="__main__": raise SystemExit(main())
