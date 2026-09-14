# -*- coding: utf-8 -*-
"""Document Surface — Option B protocol alignment planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_change_control_freeze_mapping_v1 import (
    build_change_control_freeze_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_dependency_admission_protocol_mapping_v1 import (
    build_dependency_admission_protocol_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_model_candidate_registry_alignment_v1 import (
    build_model_candidate_registry_alignment,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_model_skill_admission_contract_mapping_v1 import (
    build_model_skill_admission_contract_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_output_contract_protocol_mapping_v1 import (
    build_output_contract_protocol_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_permission_runtime_boundary_mapping_v1 import (
    build_permission_runtime_boundary_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_protocol_alignment_review_v1 import (
    build_protocol_alignment_review,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_MODEL_SKILL_ADMISSION_PROTOCOL_ALIGNMENT_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-DryRun-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_model_skill_admission_protocol_alignment_planning_v1"

POST_REVIEW_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_post_review_v1/"
    "option_b_admission_post_review_summary.json"
)
POST_REVIEW_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_POST_REVIEW_GO"
DRYRUN_DIR = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def _load_list(root: Path, rel: str) -> List[Dict[str, Any]]:
    p = root / rel
    if not p.is_file():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def run_option_b_protocol_alignment_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    post_review = _load_json(root, POST_REVIEW_REL)
    if post_review.get("final_decision") != POST_REVIEW_GO:
        blockers.append(f"upstream.admission_post_review.not_go={post_review.get('final_decision')}")
    if entry.get("option_b_dependency_and_model_candidate_admission_post_review_ready") is not True:
        blockers.append("registry.admission_post_review_ready")

    dryrun_registry = _load_json(root, f"{DRYRUN_DIR}/option_b_candidate_fixture_registry.json")
    dep_results = _load_list(root, f"{DRYRUN_DIR}/option_b_dependency_admission_results.json")
    contract_results = _load_list(root, f"{DRYRUN_DIR}/option_b_output_contract_results.json")

    contract_mapping = build_model_skill_admission_contract_mapping()
    registry_alignment = build_model_candidate_registry_alignment(dryrun_registry=dryrun_registry)
    dependency_mapping = build_dependency_admission_protocol_mapping(dependency_results=dep_results)
    output_mapping = build_output_contract_protocol_mapping(contract_results=contract_results)
    boundary_mapping = build_permission_runtime_boundary_mapping()
    change_control_mapping = build_change_control_freeze_mapping()

    mappings = {
        "contract_mapping": contract_mapping,
        "registry_alignment": registry_alignment,
        "dependency_mapping": dependency_mapping,
        "output_mapping": output_mapping,
        "boundary_mapping": boundary_mapping,
        "change_control_mapping": change_control_mapping,
    }
    alignment_review = build_protocol_alignment_review(mappings=mappings)
    if not alignment_review.get("passed"):
        blockers.append("protocol_alignment_review.failed")

    if registry_alignment.get("fixture_count", 0) < 8:
        blockers.append("registry.fixture_count")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Model-Skill-Admission-Protocol-Alignment-Planning-v1-001",
        "protocol_alignment_planning_only": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "preflight_execution_forbidden": True,
        "controlled_execution_forbidden": True,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "active_registry_update_allowed": False,
        "boundary_status": "frozen",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "primary_contract": contract_mapping.get("primary_contract"),
        "option_b_frozen_state": boundary_mapping.get("option_b_frozen_state"),
        "governance_conclusion": (
            "Option B local admission 已挂载至 Model/Skill Admission Contract；"
            "A1/C1 admitted_for_preflight_candidate ≠ model/skill/runtime admitted ≠ active registry update。"
        ),
        "adjusted_pipeline": change_control_mapping.get("adjusted_pipeline"),
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "alignment_review_passed": alignment_review.get("passed"),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "planned_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_protocol_alignment_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_skill_admission_contract_mapping_v1.json").write_text(json.dumps(contract_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_candidate_registry_alignment_v1.json").write_text(json.dumps(registry_alignment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_admission_protocol_mapping_v1.json").write_text(json.dumps(dependency_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_protocol_mapping_v1.json").write_text(json.dumps(output_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_permission_runtime_boundary_mapping_v1.json").write_text(json.dumps(boundary_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_change_control_freeze_mapping_v1.json").write_text(json.dumps(change_control_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_protocol_alignment_review_v1.json").write_text(json.dumps(alignment_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        plan_src = root / "capabilities/midplatform/model_manager/runtime/document_surface/option_b_protocol_alignment_planning/document_surface_option_b_model_skill_admission_protocol_alignment_plan_v1.md"
        if plan_src.is_file():
            (out_dir / "option_b_model_skill_admission_protocol_alignment_plan_v1.md").write_text(plan_src.read_text(encoding="utf-8"), encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {**summary, **mappings, "alignment_review": alignment_review}
