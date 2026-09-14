#!/usr/bin/env python3
"""V2 verifier for cognitive middleware integration readiness."""
import json
from pathlib import Path
FLOW="docs/architecture/cognitive_flow"
REQ={"cognitive_capability_requirement_contract_v1.md":["cognitive_need","required_evidence","no direct model call"],"cognitive_to_capability_mapping_model_v1.md":["Capability Registry","Provider Candidate","Model substitution"],"model_manager_cognitive_boundary_contract_v1.md":["Provider Management","not a cognitive subject","Evidence Gateway"],"protocol_manager_cognitive_request_contract_v1.md":["Observation Request","Capability Admission","Evidence Response"],"diagnostics_cognitive_failure_mapping_v1.md":["Provider failure","Evidence completeness","protocol error"],"middleware_integration_readiness_go_no_go_v1.md":["No real model","WAITING_FOR_USER_TERMINAL_VERIFICATION"]}
def main():
 root=next((p for p in [Path.cwd(),*Path(__file__).absolute().parents] if (p/FLOW).is_dir()),Path.cwd()); fails=[]; c=0
 for n,ts in REQ.items():
  c+=1;p=root/FLOW/n
  if not p.is_file():fails.append(f"missing required file: {n}");continue
  s=p.read_text()
  for t in ts:
   c+=1
   if t not in s:fails.append(f"missing required contract term: {t} in {n}")
 p=root/FLOW/"capability_registry_cognitive_interface_v1.json";c+=1
 try:s=p.read_text();json.loads(s)
 except Exception as e:fails.append(f"registry interface parse failure: {type(e).__name__}");s=""
 for t in ["cognitive_capability_mapping","no_model_name_in_cognitive_request","registry_does_not_decide"]:
  c+=1
  if t not in s:fails.append(f"missing required registry contract: {t}")
 print(f"CHECKS: {c}");print(f"FAILED_CHECKS: {fails}");print(f"PASSED_CHECK_COUNT: {c-len(fails)}");print(f"FAILED_CHECK_COUNT: {len(fails)}");print(f"BLOCKER_COUNT: {len(fails)}")
 if fails:print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE");print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY");return 1
 print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED");print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT");return 0
if __name__=="__main__":raise SystemExit(main())
