"""User-terminal-only V2 static verifier for Assembly Coordination Network v1."""
from pathlib import Path
def root():
 for p in (Path.cwd(),Path(__file__).absolute().parents[3],Path(__file__).resolve().parents[3]):
  if (p/"docs/architecture/cognitive_flow").is_dir(): return p
 raise RuntimeError("Luna workspace root unavailable")
F=root()/"docs/architecture/cognitive_flow"
N=("cognitive_assembly_temporal_profile_model_v1.md","cognitive_resonance_layer_architecture_v1.md","cognitive_assembly_inter_relationship_model_v1.md","cognitive_workspace_visibility_model_v1.md","cognitive_assembly_coordination_window_model_v1.md","cognitive_assembly_state_signal_model_v1.md","cognitive_assembly_resource_coordination_model_v1.md","cognitive_assembly_coordination_network_whitebox_v1.md","cognitive_assembly_coordination_network_go_no_go_v1.md")
def main():
 x=[]; c=0
 for n in N:
  c+=1
  if not (F/n).is_file(): x.append(f"missing required file: {n}")
 for n,t in ((N[1],"not a communications bus"),(N[3],"Restricted Context"),(N[8],"sole cognitive coordination layer")):
  c+=1
  if t not in (F/n).read_text(): x.append(f"missing contract term {t} in {n}")
 q=len(x); print(f"CHECKS: {c}"); print(f"FAILED_CHECKS: {x}"); print(f"PASSED_CHECK_COUNT: {c-q}"); print(f"FAILED_CHECK_COUNT: {q}"); print(f"BLOCKER_COUNT: {q}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not q else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not q else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return q
if __name__=="__main__": raise SystemExit(main())
