"""User-terminal-only V2 static verifier for Assembly Governance Finalization v1."""
from pathlib import Path
def root():
 for p in (Path.cwd(),Path(__file__).absolute().parents[3],Path(__file__).resolve().parents[3]):
  if (p/"docs/architecture/cognitive_flow").is_dir(): return p
 raise RuntimeError("Luna workspace root unavailable")
F=root()/"docs/architecture/cognitive_flow"; N=("cognitive_assembly_arbitration_model_v1.md","cognitive_assembly_working_state_model_v1.md","cognitive_assembly_process_capability_boundary_model_v1.md","cognitive_assembly_timing_alignment_model_v1.md","cognitive_assembly_resource_governance_model_v1.md","cognitive_assembly_authority_matrix_v1.md","cognitive_assembly_final_lifecycle_reconciliation_v1.md","cognitive_assembly_final_whitebox_architecture_v1.md","cognitive_assembly_go_no_go_final_v1.md")
def main():
 x=[]; c=0
 for n in N:
  c+=1
  if not (F/n).is_file(): x.append(f"missing required file: {n}")
 for n,t in ((N[0],"Neural Arbitration"),(N[1],"not Memory or Experience"),(N[5],"Reducer only"),(N[8],"No Scheduler")):
  c+=1
  if t not in (F/n).read_text(): x.append(f"missing contract term {t} in {n}")
 q=len(x); print(f"CHECKS: {c}"); print(f"FAILED_CHECKS: {x}"); print(f"PASSED_CHECK_COUNT: {c-q}"); print(f"FAILED_CHECK_COUNT: {q}"); print(f"BLOCKER_COUNT: {q}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not q else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not q else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return q
if __name__=="__main__": raise SystemExit(main())
