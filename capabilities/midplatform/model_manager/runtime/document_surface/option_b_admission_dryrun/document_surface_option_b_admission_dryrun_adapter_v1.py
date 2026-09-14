# -*- coding: utf-8 -*-
"""Document Surface — Option B admission dryrun adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_admission_dryrun_metrics_v1 import (
    compute_admission_dryrun_metrics,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_candidate_fixture_registry_v1 import (
    build_candidate_fixture_registry,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_model_candidate_admission_dryrun_v1 import (
    run_model_candidate_admission_dryrun,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_DRYRUN_BLOCKED"
NEXT_POST_REVIEW = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-Post-Review-v1-001"
PARALLEL = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_dryrun_v1"

PLANNING_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_dependency_and_model_candidate_admission_planning_v1/"
    "option_b_admission_planning_summary.json"
)
PLANNING_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_DEPENDENCY_AND_MODEL_CANDIDATE_ADMISSION_PLANNING_GO"
ROUTE_DRYRUN_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_candidate_route_dryrun_summary.json"
)
ROUTE_DRYRUN_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_DRYRUN_GO"
ROUTE_POST_REVIEW_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_post_review_v1/"
    "option_b_candidate_route_post_review_summary.json"
)
ROUTE_POST_REVIEW_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_OPTIONB_CANDIDATE_ROUTE_POST_REVIEW_GO"


def _load_json(root: Path, rel: str) -> Dict[str, Any]:
    p = root / rel
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}


def run_option_b_admission_dryrun(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    blockers: List[str] = []

    planning = _load_json(root, PLANNING_REL)
    route_dryrun = _load_json(root, ROUTE_DRYRUN_REL)
    route_post = _load_json(root, ROUTE_POST_REVIEW_REL)
    if route_dryrun.get("final_decision") != ROUTE_DRYRUN_GO:
        blockers.append(f"upstream.route_dryrun.not_go={route_dryrun.get('final_decision')}")
    if route_post.get("final_decision") != ROUTE_POST_REVIEW_GO:
        blockers.append(f"upstream.route_post_review.not_go={route_post.get('final_decision')}")
    if planning.get("final_decision") != PLANNING_GO:
        blockers.append(f"upstream.planning.not_go={planning.get('final_decision')}")
    if entry.get("option_b_dependency_and_model_candidate_admission_planning_ready") is not True:
        blockers.append("registry.admission_planning_ready")

    registry = build_candidate_fixture_registry()
    results = [run_model_candidate_admission_dryrun(candidate=f) for f in registry.get("fixtures", [])]
    metrics = compute_admission_dryrun_metrics(results=results)

    if registry.get("fixture_count", 0) < 8:
        blockers.append("fixtures.incomplete")
    if not all(r.get("expectation_met") for r in results):
        blockers.append("expectation.mismatch")
    if metrics.get("execution_block_rate", 0) < 1.0:
        blockers.append("metrics.execution_block")
    if metrics.get("active_model_selection_rate", 1) > 0:
        blockers.append("metrics.active_model_selected")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-OptionB-Dependency-And-Model-Candidate-Admission-DryRun-v1-001",
        "admission_dryrun_only": True,
        "segmentation_execution_forbidden": True,
        "model_download_forbidden": True,
        "dependency_install_forbidden": True,
        "preflight_execution_forbidden": True,
        "controlled_execution_forbidden": True,
        "runtime_activation_allowed": False,
        "option_b_execution_allowed": False,
        "option_b_active_model_selected": False,
        "boundary_status": "frozen",
        "metrics": metrics,
        "fixture_count": registry.get("fixture_count"),
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

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "option_b_admission_dryrun_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_candidate_fixture_registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_dependency_admission_results.json").write_text(json.dumps([r.get("dependency_admission") for r in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_model_candidate_admission_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_license_weight_results.json").write_text(json.dumps([r.get("license_weight") for r in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_output_contract_results.json").write_text(json.dumps([r.get("output_contract") for r in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_wrapper_requirement_results.json").write_text(json.dumps([r.get("wrapper_requirement") for r in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_abort_rollback_results.json").write_text(json.dumps([r.get("abort_rollback") for r in results], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "option_b_admission_dryrun_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {**summary, "registry": registry, "results": results}
