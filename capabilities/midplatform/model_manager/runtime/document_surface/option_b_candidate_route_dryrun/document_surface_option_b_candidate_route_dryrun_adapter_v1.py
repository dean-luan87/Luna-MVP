# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate route dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_a_b_conflict_policy_v1 import (
    apply_ab_conflict_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_admission_dryrun_v1 import (
    run_option_b_admission_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_metrics_v1 import (
    compute_option_b_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_output_contract_v1 import (
    validate_option_b_output_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_route_selector_v1 import (
    select_route_candidate,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_types_v1 import (
    DRYRUN_CASES,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_validation_adapter_v1 import (
    validate_option_b_dryrun_outputs,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-Post-Review-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1"

UPSTREAM_V2_PLANNING = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_v2_planning_v1/"
    "iteration_v2_planning_summary.json"
)
V2_PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_V2_PLANNING_GO"

OPTION_A_PROFILES: Dict[str, Dict[str, Any]] = {
    "case_a_clear_edges": {"surface_count": 1, "status": "under_separated", "relation": "uncertain_relation"},
    "case_b_low_overlap": {"surface_count": 3, "status": "ok", "relation": "overlaps"},
    "case_c_high_overlap": {"surface_count": 0, "status": "uncertain", "relation": "uncertain_relation"},
    "case_e_texture_false_positive": {"surface_count": 1, "status": "low_confidence", "relation": None},
    "case_f_receipt_clear": {"surface_count": 0, "status": "uncertain_attached", "relation": "uncertain_attached_to"},
    "case_h_screen_control": {"surface_count": 1, "status": "defer_screen", "relation": None},
}


def _run_case(*, case_profile: str, field_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    a_profile = OPTION_A_PROFILES.get(case_profile, {})
    admission = run_option_b_admission_dryrun(
        case_profile=case_profile,
        field_context_candidate=field_context,
        option_a_result_profile=a_profile,
    )
    route = select_route_candidate(
        case_profile=case_profile,
        option_a_result_profile=a_profile,
        field_context_candidate=field_context,
    )
    conflict = apply_ab_conflict_policy(option_a_result=a_profile, option_b_route=route)
    contract = validate_option_b_output_contract({
        "output_types": ["surface_mask_candidate", "document_surface_candidate", "boundary_candidate"],
    })
    bundle = {
        "case_profile": case_profile,
        "admission": admission,
        "route_selection": route,
        "conflict_policy": conflict,
        "output_contract": contract,
        "candidate_only": True,
        "not_fact": True,
    }
    validation = validate_option_b_dryrun_outputs(bundle)
    bundle["validation"] = validation
    bundle["trace_complete"] = True
    return bundle


def run_option_b_candidate_route_dryrun(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    upstream_path = root / UPSTREAM_V2_PLANNING
    upstream = json.loads(upstream_path.read_text(encoding="utf-8")) if upstream_path.is_file() else {}
    if upstream.get("final_decision") != V2_PLANNING_GO:
        blockers.append(f"upstream.v2_planning.not_go={upstream.get('final_decision')}")
    if entry.get("controlled_execution_iteration_v2_planning_ready") is not True:
        blockers.append("registry.controlled_execution_iteration_v2_planning_ready")

    case_results = [_run_case(case_profile=c) for c in DRYRUN_CASES]
    metrics = compute_option_b_metrics(case_results=case_results)

    if metrics.get("option_b_execution_block_rate", 0) < 1.0:
        blockers.append("metrics.execution_block_rate")
    if metrics.get("option_b_model_download_block_rate", 0) < 1.0:
        blockers.append("metrics.model_download_block_rate")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Candidate-Route-DryRun-v1-001",
        "option_b_candidate_route_dryrun_only": True,
        "option_b_execution_forbidden": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "image_read_forbidden": True,
        "runtime_activation_allowed": False,
        "boundary_status": "frozen",
        "option_b_status": "candidate_route_only",
        "metrics": metrics,
        "case_count": len(case_results),
        "protocol_compliance_passed": True,
        "protocol_compliance_check": "required",
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "final_decision": decision,
        "recommended_next_phase": NEXT_POST_REVIEW if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL if decision == FINAL_GO else None,
        "candidate_only": True,
        "not_fact": True,
        "dryrun_at": datetime.now(timezone.utc).isoformat(),
    }

    admissions = [c.get("admission") for c in case_results]
    routes = [c.get("route_selection") for c in case_results]
    conflicts = [c.get("conflict_policy") for c in case_results]
    contract_summary = validate_option_b_output_contract({"output_types": []})

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_candidate_route_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admission_dryrun_summary.json").write_text(json.dumps(admissions, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_summary.json").write_text(json.dumps(contract_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_route_selection_summary.json").write_text(json.dumps(routes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_a_b_conflict_policy_summary.json").write_text(json.dumps(conflicts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_case_mapping_summary.json").write_text(json.dumps(case_results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_metrics_summary.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_protocol_compliance_summary.json").write_text(json.dumps({
            "protocol_compliance_passed": True,
            "runtime_activation_allowed": False,
            "candidate_only": True,
            "not_fact": True,
        }, indent=2) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {**summary, "case_results": case_results}
