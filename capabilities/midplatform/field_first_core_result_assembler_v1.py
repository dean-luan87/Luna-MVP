# -*- coding: utf-8 -*-
"""Field-First Core Logic — result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_first_core_logic_types_v1 import (
    DECISION_READINESS_FLAGS,
    NON_EXECUTION_FLAGS,
)


def build_decision_readiness_summary(
    *,
    continuity_status: str,
    tracking_plan: Dict[str, Any],
    missing_information: List[Dict[str, Any]],
    warnings: List[str],
    scene: Dict[str, Any],
) -> Dict[str, Any]:
    missing_types = {m.get("missing_type") for m in missing_information}
    depth_summary = scene.get("depth_quality_summary") or {}
    summary = {flag: False for flag in DECISION_READINESS_FLAGS}
    summary["candidate_only_no_action"] = True
    summary["ready_for_field_simulation_candidate"] = (
        continuity_status in ("same_field", "field_shift", "field_recovering")
        and tracking_plan.get("tracking_allowed")
        and not missing_types.intersection({"frozen_tracking", "new_field_reset"})
    )
    if depth_summary.get("unknown_count", 0) > 0 or "missing_depth" in missing_types:
        summary["blocked_by_missing_depth"] = True
    if continuity_status in ("uncertain_need_recheck", "field_lost"):
        summary["blocked_by_field_uncertainty"] = True
        summary["need_more_observation"] = True
    if tracking_plan.get("tracking_frozen"):
        summary["blocked_by_tracking_frozen"] = True
    if tracking_plan.get("tracking_reset"):
        summary["blocked_by_new_field_reset"] = True
    if continuity_status in ("field_occluded", "field_lost") or "frozen_tracking" in missing_types:
        summary["unsafe_to_infer_motion"] = True
    if warnings:
        summary["need_more_observation"] = summary["need_more_observation"] or bool(warnings)
    return summary


def assemble_field_first_core_logic_result(
    *,
    input_package: Dict[str, Any],
    field_scene: Dict[str, Any],
    continuity_decision: Dict[str, Any],
    tracking_plan: Dict[str, Any],
    trajectory_analysis: Dict[str, Any],
    pipeline_stage_results: List[Dict[str, Any]],
    warnings: List[str],
) -> Dict[str, Any]:
    missing = list(trajectory_analysis.get("missing_information_candidates") or [])
    scene_missing = field_scene.get("missing_information") or []
    for sm in scene_missing:
        missing.append({
            "missing_info_id": f"mi_{uuid.uuid4().hex[:12]}",
            "target_ref": None,
            "missing_type": sm if isinstance(sm, str) else sm.get("missing_type", "unknown"),
            "affects_analysis": True,
            "recommended_recheck": True,
            "reason_codes": ["from_field_scene_construction"],
            "candidate_only": True,
        })
    readiness = build_decision_readiness_summary(
        continuity_status=continuity_decision.get("continuity_status", "unknown"),
        tracking_plan=tracking_plan,
        missing_information=missing,
        warnings=warnings,
        scene=field_scene,
    )
    return {
        "result_candidate_id": f"ffcr_{uuid.uuid4().hex[:12]}",
        "input_package_ref": input_package.get("input_package_id"),
        "field_scene_candidate": field_scene,
        "field_continuity_decision_candidate": continuity_decision,
        "target_tracking_plan_candidate": tracking_plan,
        "static_target_lock_candidates": list(tracking_plan.get("static_locks") or []),
        "dynamic_target_track_candidates": list(tracking_plan.get("dynamic_tracks") or []),
        "trajectory_candidates": list(trajectory_analysis.get("trajectory_candidates") or []),
        "task_impact_analysis_candidates": list(trajectory_analysis.get("task_impact_analysis_candidates") or []),
        "risk_projection_candidates": list(trajectory_analysis.get("risk_projection_candidates") or []),
        "missing_information_candidates": missing,
        "warning_summary": {
            "warnings": warnings,
            "warning_count": len(warnings),
        },
        "decision_readiness_summary": readiness,
        "pipeline_stage_results": pipeline_stage_results,
        "traceability_refs": list(input_package.get("traceability_refs") or []) + [field_scene.get("field_scene_id")],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
