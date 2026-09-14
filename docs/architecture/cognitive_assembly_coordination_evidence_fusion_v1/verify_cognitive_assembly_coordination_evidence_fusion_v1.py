"""User-terminal-only V2 static verifier for Assembly Coordination and Evidence Fusion v1."""
from __future__ import annotations
from pathlib import Path
def root() -> Path:
    for p in (Path.cwd(),Path(__file__).absolute().parents[3],Path(__file__).resolve().parents[3]):
        if (p/"docs/architecture/cognitive_flow").is_dir(): return p
    raise RuntimeError("Luna workspace root unavailable")
FLOW=root()/"docs/architecture/cognitive_flow"
FILES=("cognitive_assembly_member_model_v1.md","cognitive_assembly_coordination_model_v1.md","cognitive_assembly_member_relationship_model_v1.md","cognitive_assembly_evidence_fusion_model_v1.md","cognitive_assembly_completion_evaluation_model_v1.md","cognitive_assembly_failure_and_partial_completion_model_v1.md","cognitive_assembly_template_reuse_model_v2.md","cognitive_assembly_coordination_whitebox_architecture_v1.md","cognitive_assembly_coordination_go_no_go_v1.md")
def main() -> int:
    fails=[]; checks=0
    for f in FILES:
        checks+=1
        if not (FLOW/f).is_file(): fails.append(f"missing required file: docs/architecture/cognitive_flow/{f}")
    for f,t in (("cognitive_assembly_member_model_v1.md","not an Agent"),("cognitive_assembly_coordination_model_v1.md","not an Agent"),("cognitive_assembly_evidence_fusion_model_v1.md","not an answer or Truth claim"),("cognitive_assembly_completion_evaluation_model_v1.md","cannot declare cognitive completion"),("cognitive_assembly_coordination_go_no_go_v1.md","No Runtime")):
        checks+=1
        if t not in (FLOW/f).read_text(): fails.append(f"missing contract term {t} in {f}")
    n=len(fails); print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {fails}"); print(f"PASSED_CHECK_COUNT: {checks-n}"); print(f"FAILED_CHECK_COUNT: {n}"); print(f"BLOCKER_COUNT: {n}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not n else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not n else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 0 if not n else 1
if __name__ == "__main__": raise SystemExit(main())
