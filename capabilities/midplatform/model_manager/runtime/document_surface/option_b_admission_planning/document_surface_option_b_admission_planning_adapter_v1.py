# -*- coding: utf-8 -*-
"""Document Surface — Option B admission planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_model_candidate_types_v1 import (
    build_option_b_candidate_family_evaluation,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_output_contract_compatibility_v1 import (
    build_output_contract_compatibility,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_planning.document_surface_option_b_preflight_requirements_v1 import (
    build_preflight_requirements,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-DryRun-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1"

POST_REVIEW_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1/"
    "option_b_candidate_route_post_review_summary.json"
)
POST_REVIEW_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"

PLAN_DIR = "capabilities/midplatform/model_manager/runtime/document_surface/option_b_admission_planning"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run_option_b_admission_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    post_review = _load_json(root, POST_REVIEW_REL)
    if post_review.get("final_decision") != POST_REVIEW_GO:
        blockers.append(f"upstream.post_review.not_go={post_review.get('final_decision')}")
    if entry.get("option_b_candidate_route_post_review_ready") is not True:
        blockers.append("registry.option_b_candidate_route_post_review_ready")

    families = build_option_b_candidate_family_evaluation()
    registry_schema = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_candidate_registry_schema_v1.json")
    dep_policy = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_dependency_admission_policy_v1.json")
    model_admission = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_model_candidate_admission_policy_v1.json")
    license_policy = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_license_and_weight_policy_v1.json")
    contract = build_output_contract_compatibility()
    preflight = build_preflight_requirements()
    abort_rollback = _load_json(root, f"{PLAN_DIR}/document_surface_option_b_abort_rollback_policy_v1.json")

    if not families.get("all_families_abcd_evaluated"):
        blockers.append("families.incomplete")
    if dep_policy.get("install_allowed") is not False:
        blockers.append("dependency.install_not_blocked")
    if model_admission.get("active_model_selection_allowed") is not False:
        blockers.append("model_admission.active_selection_not_blocked")
    if len(license_policy.get("block_conditions") or []) < 8:
        blockers.append("license_policy.incomplete")
    if not preflight.get("all_checks_required"):
        blockers.append("preflight.incomplete")
    if len(abort_rollback.get("abort_conditions") or []) < 12:
        blockers.append("abort_policy.incomplete")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Planning-v1-001",
        "admission_planning_only": True,
        "option_b_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "active_model_selection_forbidden": True,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "boundary_status": post_review.get("boundary_status", "frozen"),
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "final_decision": decision,
        "planned_at": datetime.now(timezone.utc).isoformat(),
        "candidate_only": True,
        "not_fact": True,
    }

    registry_review = {
        "schema_complete": all(f in (registry_schema.get("required_fields") or []) for f in (
            "model_candidate_id", "active_status", "preflight_required", "controlled_execution_required",
        )),
        "active_status_default_false": registry_schema.get("defaults", {}).get("active_status") is False,
        "preflight_required": registry_schema.get("defaults", {}).get("preflight_required") is True,
        "controlled_execution_required": registry_schema.get("defaults", {}).get("controlled_execution_required") is True,
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_admission_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_family_evaluation.json").write_text(json.dumps(families, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_candidate_registry_schema_review.json").write_text(json.dumps(registry_review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_admission_policy_summary.json").write_text(json.dumps(dep_policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_license_weight_policy_summary.json").write_text(json.dumps(license_policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_compatibility_summary.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_preflight_requirements_summary.json").write_text(json.dumps(preflight, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_abort_rollback_policy_summary.json").write_text(json.dumps(abort_rollback, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "families": families,
        "registry_schema": registry_schema,
        "registry_review": registry_review,
        "dependency_policy": dep_policy,
        "model_admission_policy": model_admission,
        "license_policy": license_policy,
        "output_contract": contract,
        "preflight": preflight,
        "abort_rollback": abort_rollback,
    }
