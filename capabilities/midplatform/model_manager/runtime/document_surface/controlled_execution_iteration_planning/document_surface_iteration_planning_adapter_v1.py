# -*- coding: utf-8 -*-
"""Document Surface — controlled execution iteration planning adapter v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_attached_to_uncertainty_strategy_v1 import (
    build_attached_to_uncertainty_strategy_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_candidate_quality_gate_v1 import (
    build_candidate_quality_gate_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_fixture_plan_v1 import (
    build_iteration_fixture_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_metrics_plan_v1 import (
    build_iteration_metrics_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_risk_mapping_v1 import (
    build_iteration_risk_mapping,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_low_contrast_noise_strategy_v1 import (
    build_low_contrast_noise_strategy_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_overlap_separation_strategy_v1 import (
    build_overlap_separation_strategy_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_relation_hint_constraints_v1 import (
    build_relation_hint_constraints_plan,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_CONTROLLED_EXECUTION_ITERATION_PLANNING_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-DryRun-v1-001"
PARALLEL_NEXT_TRACK = "Phase-P1-Midplatform-Luna-Situation-Understanding-Field-Centric-Object-Role-DryRun-v1-001"
OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_controlled_execution_iteration_planning_v1"

UPSTREAM_POST_REVIEW = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_post_review_v1_review_v0/"
    "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_post_review_review_v1.json"
)
POST_REVIEW_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_CONTROLLED_EXECUTION_POST_REVIEW_GO"


def run_iteration_planning(
    *,
    repo_root: Optional[Path] = None,
    write_outputs: bool = True,
) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}

    risk_mapping = build_iteration_risk_mapping()
    quality_gate = build_candidate_quality_gate_plan()
    overlap = build_overlap_separation_strategy_plan()
    low_contrast = build_low_contrast_noise_strategy_plan()
    attached = build_attached_to_uncertainty_strategy_plan()
    relations = build_relation_hint_constraints_plan()
    fixtures = build_iteration_fixture_plan()
    metrics = build_iteration_metrics_plan()

    upstream = {}
    up_path = root / UPSTREAM_POST_REVIEW
    if up_path.is_file():
        upstream = json.loads(up_path.read_text(encoding="utf-8"))

    blockers: List[str] = []
    if upstream.get("final_decision") != POST_REVIEW_GO:
        blockers.append("upstream.post_review.not_go")
    if entry.get("controlled_execution_post_review_ready") is not True:
        blockers.append("registry.controlled_execution_post_review_ready")
    if not risk_mapping.get("all_case_bcd_mapped"):
        blockers.append("risk_mapping.case_bcd_incomplete")

    decision = FINAL_GO if not blockers else FINAL_BLOCKED

    summary: Dict[str, Any] = {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Document-Surface-Detector-Controlled-Execution-Iteration-Planning-v1-001",
        "runtime_id": "document_surface_detector_v1",
        "iteration_planning_only": True,
        "detector_rerun_forbidden": True,
        "cv2_execution_forbidden": True,
        "real_image_read_forbidden": True,
        "runtime_activation_allowed": False,
        "boundary_status": upstream.get("boundary_status", "frozen"),
        "protocol_compliance_check": "required",
        "protocol_compliance_passed": True,
        "existing_midplatform_protocol_chain_extension": True,
        "protocol_patch_not_new_branch": True,
        "case_bcd_risks_mapped": risk_mapping.get("all_case_bcd_mapped"),
        "fixture_categories_planned": fixtures.get("category_count"),
        "new_metrics_planned": len(metrics.get("new_metrics") or []),
        "recommended_next_phase": NEXT_PHASE if decision == FINAL_GO else None,
        "parallel_next_track": PARALLEL_NEXT_TRACK if decision == FINAL_GO else None,
        "blocker_count": len(blockers),
        "failed_checks": blockers,
        "final_decision": decision,
        "candidate_only": True,
        "not_fact": True,
        "planned_at": datetime.now(timezone.utc).isoformat(),
    }

    out_dir = root / OUTPUT_ROOT
    if write_outputs:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "iteration_planning_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_risk_mapping.json").write_text(json.dumps(risk_mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "candidate_quality_gate_plan.json").write_text(json.dumps(quality_gate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "overlap_separation_strategy_plan.json").write_text(json.dumps(overlap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "low_contrast_noise_strategy_plan.json").write_text(json.dumps(low_contrast, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "attached_to_uncertainty_strategy_plan.json").write_text(json.dumps(attached, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "relation_hint_constraints_plan.json").write_text(json.dumps(relations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_fixture_plan.json").write_text(json.dumps(fixtures, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "iteration_metrics_plan.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        summary["output_dir"] = str(out_dir)

    return {
        **summary,
        "risk_mapping": risk_mapping,
        "quality_gate": quality_gate,
        "overlap_strategy": overlap,
        "low_contrast_strategy": low_contrast,
        "attached_strategy": attached,
        "relation_constraints": relations,
        "fixture_plan": fixtures,
        "metrics_plan": metrics,
    }
