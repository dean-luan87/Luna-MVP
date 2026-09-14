"""User-terminal-only V2 static verifier for Process Ecology and Experience Consolidation v1."""
from __future__ import annotations
import json
from pathlib import Path
def root() -> Path:
    for p in (Path.cwd(), Path(__file__).absolute().parents[3], Path(__file__).resolve().parents[3]):
        if (p / "docs/architecture/cognitive_flow").is_dir(): return p
    raise RuntimeError("Luna workspace root unavailable")
ROOT=root(); FLOW=ROOT/"docs/architecture/cognitive_flow"
FILES=("cognitive_process_ecology_architecture_v1.md","cognitive_reflex_process_model_v1.md","cognitive_background_process_model_v1.md","cognitive_active_cognitive_assembly_model_v1.md","cognitive_multi_process_coordination_model_v1.md","cognitive_process_lifecycle_model_v1.md","cognitive_process_resource_budget_model_v1.md","cognitive_process_interrupt_candidate_model_v1.md","cognitive_experience_consolidation_architecture_v1.md","cognitive_experience_layering_model_v1.md","cognitive_process_template_model_v1.md","cognitive_process_ecology_whitebox_architecture_v1.md","cognitive_process_ecology_experience_go_no_go_v1.md","cognitive_process_ecology_contract_schema_v1.json")
def main() -> int:
    fails=[]; checks=0
    for name in FILES:
        checks+=1
        if not (FLOW/name).is_file(): fails.append(f"missing required file: docs/architecture/cognitive_flow/{name}")
    checks+=1
    try: json.loads((FLOW/"cognitive_process_ecology_contract_schema_v1.json").read_text())
    except Exception as exc: fails.append(f"schema parse failure: {type(exc).__name__}")
    for name,term in (("cognitive_process_ecology_architecture_v1.md","```mermaid"),("cognitive_multi_process_coordination_model_v1.md","Neural Governance"),("cognitive_process_lifecycle_model_v1.md","Dormant"),("cognitive_experience_consolidation_architecture_v1.md","Candidate → Validation → Adoption"),("cognitive_process_ecology_experience_go_no_go_v1.md","automatic learning")):
        checks+=1
        if term not in (FLOW/name).read_text(): fails.append(f"missing contract term {term} in {name}")
    n=len(fails); print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {fails}"); print(f"PASSED_CHECK_COUNT: {checks-n}"); print(f"FAILED_CHECK_COUNT: {n}"); print(f"BLOCKER_COUNT: {n}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not n else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not n else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 0 if not n else 1
if __name__ == "__main__": raise SystemExit(main())
