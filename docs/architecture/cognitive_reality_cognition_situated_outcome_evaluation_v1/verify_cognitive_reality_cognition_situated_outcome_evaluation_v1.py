#!/usr/bin/env python3
from pathlib import Path
FLOW='docs/architecture/cognitive_flow'
FILES=['cognitive_situated_outcome_interpretation_model_v1.md','cognitive_prediction_reality_difference_extension_v1.md','cognitive_outcome_cause_attribution_model_v1.md','cognitive_outcome_adaptive_correction_boundary_v1.md','cognitive_outcome_self_capability_feedback_interface_v1.md','cognitive_situated_outcome_experience_interface_v1.md','cognitive_situated_outcome_scenario_registry_v1.md','cognitive_situated_outcome_evaluation_go_no_go_v1.md']
TERMS=['Past Available Context','Capability Gap','Cause Attribution is cognitive explanation','candidates only','Self Capability Limitation Candidate','not a log, Memory write, B','correct_decision_bad_outcome','WAITING_FOR_USER_TERMINAL_VERIFICATION']
def main():
 root=Path.cwd(); failures=[]; checks=0
 for p in [root,*Path(__file__).absolute().parents]:
  if (p/FLOW).is_dir(): root=p; break
 for f,t in zip(FILES,TERMS):
  checks+=1; q=root/FLOW/f
  if not q.is_file(): failures.append(f'missing required file: {f}'); continue
  checks+=1
  if t not in q.read_text(): failures.append(f'missing required contract term: {t} in {f}')
 print(f'CHECKS: {checks}'); print(f'FAILED_CHECKS: {failures}'); print(f'PASSED_CHECK_COUNT: {checks-len(failures)}'); print(f'FAILED_CHECK_COUNT: {len(failures)}'); print(f'BLOCKER_COUNT: {len(failures)}')
 if failures: print('FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE'); print('NEXT: REMEDIATE_REPORTED_FAILURES_ONLY'); return 1
 print('FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED'); print('NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT'); return 0
if __name__=='__main__': raise SystemExit(main())
