"""User-terminal-only V2 static verifier for Cognitive Assembly governance v1."""
from __future__ import annotations
from pathlib import Path
def root() -> Path:
    for p in (Path.cwd(),Path(__file__).absolute().parents[3],Path(__file__).resolve().parents[3]):
        if (p/"docs/architecture/cognitive_flow").is_dir(): return p
    raise RuntimeError("Luna workspace root unavailable")
FLOW=root()/"docs/architecture/cognitive_flow"
FILES=("cognitive_assembly_contract_model_v1.md","cognitive_assembly_creation_model_v1.md","cognitive_assembly_classification_model_v1.md","cognitive_assembly_lifecycle_model_v1.md","cognitive_assembly_identity_model_v1.md","cognitive_assembly_capacity_governance_model_v1.md","cognitive_assembly_admission_model_v1.md","cognitive_assembly_resource_budget_model_v1.md","cognitive_assembly_template_reuse_model_v1.md","cognitive_assembly_whitebox_architecture_v1.md","cognitive_assembly_go_no_go_v1.md")
def main() -> int:
    fails=[]; checks=0
    for f in FILES:
        checks+=1
        if not (FLOW/f).is_file(): fails.append(f"missing required file: docs/architecture/cognitive_flow/{f}")
    for f,term in (("cognitive_assembly_contract_model_v1.md","Assembly is not an Agent"),("cognitive_assembly_creation_model_v1.md","sole Assembly creation coordinator"),("cognitive_assembly_lifecycle_model_v1.md","```mermaid"),("cognitive_assembly_go_no_go_v1.md","No Scheduler")):
        checks+=1
        if term not in (FLOW/f).read_text(): fails.append(f"missing contract term {term} in {f}")
    n=len(fails); print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {fails}"); print(f"PASSED_CHECK_COUNT: {checks-n}"); print(f"FAILED_CHECK_COUNT: {n}"); print(f"BLOCKER_COUNT: {n}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not n else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not n else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 0 if not n else 1
if __name__ == "__main__": raise SystemExit(main())
