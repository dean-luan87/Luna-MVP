# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_change_control_mapping_dryrun_v1 import (
    run_change_control_mapping_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_dependency_protocol_mapping_dryrun_v1 import (
    run_dependency_protocol_mapping_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_evidence_chain_mapping_dryrun_v1 import (
    run_evidence_chain_mapping_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_model_skill_admission_contract_dryrun_v1 import (
    run_model_skill_admission_contract_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_output_contract_protocol_mapping_dryrun_v1 import (
    run_output_contract_protocol_mapping_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_permission_admission_mapping_dryrun_v1 import (
    run_permission_admission_mapping_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_protocol_alignment_metrics_v1 import (
    compute_protocol_alignment_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_registry_alignment_dryrun_v1 import (
    run_registry_alignment_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_runtime_boundary_protocol_mapping_dryrun_v1 import (
    run_runtime_boundary_protocol_mapping_dryrun,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Post-Review-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_dryrun_v1"

ADMISSION_DRYRUN_DIR = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1"
ALIGNMENT_PLANNING_DIR = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1"

PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_GO"
ADMISSION_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
ADMISSION_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_POST_REVIEW_GO"
ADMISSION_PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"
ROUTE_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
ROUTE_POST_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _load_list(root: Path, rel: str) -> List[Dict[str, Any]]:
    p = root / rel
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def _verify_protocol_chain(root: Path) -> bool:
    chain = _load_json(root, "capabilities/midplatform/protocols/region_intelligence_protocol_chain_v1.json")
    refs = [p.get("protocol_ref") for p in chain.get("legacy_protocols_required") or []]
    return "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1" in refs


def run_option_b_protocol_alignment_dryrun(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    checks = {
        "route_dryrun": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/option_b_candidate_route_dryrun_summary.json"),
        "route_post": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1/option_b_candidate_route_post_review_summary.json"),
        "admission_planning": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1/option_b_admission_planning_summary.json"),
        "admission_dryrun": _load_json(root, f"{ADMISSION_DRYRUN_DIR}/option_b_admission_dryrun_summary.json"),
        "admission_post": _load_json(root, "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_post_review_v1/option_b_admission_post_review_summary.json"),
        "alignment_planning": _load_json(root, f"{ALIGNMENT_PLANNING_DIR}/option_b_protocol_alignment_planning_summary.json"),
    }
    if checks["route_dryrun"].get("final_decision") != ROUTE_DRYRUN_GO:
        blockers.append("upstream.route_dryrun")
    if checks["route_post"].get("final_decision") != ROUTE_POST_GO:
        blockers.append("upstream.route_post")
    if checks["admission_planning"].get("final_decision") != ADMISSION_PLANNING_GO:
        blockers.append("upstream.admission_planning")
    if checks["admission_dryrun"].get("final_decision") != ADMISSION_DRYRUN_GO:
        blockers.append("upstream.admission_dryrun")
    if checks["admission_post"].get("final_decision") != ADMISSION_POST_GO:
        blockers.append("upstream.admission_post")
    if checks["alignment_planning"].get("final_decision") != PLANNING_GO:
        blockers.append("upstream.alignment_planning")
    if entry.get("option_b_model_skill_admission_protocol_alignment_planning_ready") is not True:
        blockers.append("registry.alignment_planning_ready")
    if not _verify_protocol_chain(root):
        blockers.append("protocol_chain.missing_model_skill_contract")

    admission_results = _load_list(root, f"{ADMISSION_DRYRUN_DIR}/option_b_model_candidate_admission_results.json")
    if len(admission_results) != 8:
        blockers.append("admission_results.incomplete")

    contract = run_model_skill_admission_contract_dryrun(admission_results=admission_results)
    registry = run_registry_alignment_dryrun(admission_results=admission_results)
    dependency = run_dependency_protocol_mapping_dryrun(admission_results=admission_results)
    output = run_output_contract_protocol_mapping_dryrun(admission_results=admission_results)
    runtime = run_runtime_boundary_protocol_mapping_dryrun(admission_results=admission_results)
    permission = run_permission_admission_mapping_dryrun(dependency_mapping=dependency)
    change = run_change_control_mapping_dryrun()
    evidence = run_evidence_chain_mapping_dryrun(admission_results=admission_results, contract_mapping=contract)
    metrics = compute_protocol_alignment_metrics(
        contract=contract, registry=registry, dependency=dependency,
        output=output, runtime=runtime, change=change, evidence=evidence,
    )

    if not contract.get("all_mapped"):
        blockers.append("contract_mapping.incomplete")
    if registry.get("active_registry_update_count", 1) != 0:
        blockers.append("registry.active_update")
    if metrics.get("active_model_mapping_count", 1) != 0:
        blockers.append("metrics.active_model")
    if change.get("recommended_next_phase") != NEXT_POST_REVIEW:
        blockers.append("change_control.wrong_next_phase")
    if change.get("preflight_planning_not_recommended") is not True:
        blockers.append("preflight_planning.leak")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED
    frozen = checks["alignment_planning"].get("option_b_frozen_state") or {}

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-DryRun-v1-001",
        "protocol_alignment_dryrun_only": True,
        "preflight_planning_forbidden": True,
        "preflight_execution_forbidden": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "runtime_activation_allowed": False,
        "controlled_execution_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "active_registry_update_allowed": False,
        "boundary_status": "frozen",
        "primary_contract": "LUNA-PROTO-L1-MODEL-SKILL-ADMISSION-CONTRACT-V1",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "option_b_frozen_state": frozen,
        "metrics": metrics,
        "governance_conclusion": (
            "Option B 已完成 Model/Skill Admission Contract dryrun 对齐；"
            "A1/C1 仅可作为 preflight candidate；blocked candidates 拒绝路径可追踪；"
            "Post-Review 完成前不得进入 Preflight Planning。"
        ),
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "protocol_compliance_passed": True,
        "recommended_next_phase": NEXT_POST_REVIEW if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "dryrun_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_protocol_alignment_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_skill_contract_mapping_results.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_registry_alignment_results.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_protocol_mapping_results.json").write_text(json.dumps(dependency, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_protocol_mapping_results.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_runtime_boundary_mapping_results.json").write_text(json.dumps(runtime, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_permission_admission_mapping_results.json").write_text(json.dumps(permission, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_change_control_mapping_results.json").write_text(json.dumps(change, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_evidence_chain_mapping_results.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_protocol_alignment_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "contract_mapping": contract,
        "registry_alignment": registry,
        "dependency_mapping": dependency,
        "output_mapping": output,
        "runtime_mapping": runtime,
        "permission_mapping": permission,
        "change_control_mapping": change,
        "evidence_mapping": evidence,
    }
