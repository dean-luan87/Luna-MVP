# -*- coding: utf-8 -*-
"""Field-First Core Logic — consistency validators v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple


def validate_cross_stage_consistency(result: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, bool]]:
    issues: List[str] = []
    checks: Dict[str, bool] = {}
    continuity = result.get("field_continuity_decision_candidate") or {}
    status = continuity.get("continuity_status", "")
    plan = result.get("target_tracking_plan_candidate") or {}
    trajectories = result.get("trajectory_candidates") or []
    missing = result.get("missing_information_candidates") or []
    missing_types = {m.get("missing_type") for m in missing}

    if status == "new_field_required":
        if plan.get("static_locks"):
            issues.append("new_field_inherited_static_locks")
        if plan.get("dynamic_tracks"):
            issues.append("new_field_inherited_dynamic_tracks")
        if trajectories:
            issues.append("new_field_inherited_trajectories")
    checks["new_field_resets_targets_validated"] = status != "new_field_required" or (
        not plan.get("static_locks") and not plan.get("dynamic_tracks") and not trajectories
    )

    if status == "field_occluded":
        if not plan.get("tracking_frozen"):
            issues.append("occluded_not_frozen")
        if trajectories:
            issues.append("occluded_generated_trajectory")
    checks["field_occluded_freezes_tracking_validated"] = status != "field_occluded" or (
        plan.get("tracking_frozen") and not trajectories
    )

    if status == "field_lost" and trajectories:
        issues.append("field_lost_generated_trajectory")

    for traj in trajectories:
        conf = traj.get("trajectory_confidence", "unknown")
        scene = result.get("field_scene_candidate") or {}
        depth_unknown = any(e.get("depth_unknown") for e in scene.get("entity_candidates") or [])
        if depth_unknown and conf == "high":
            issues.append("unknown_depth_high_confidence")

    if result.get("candidate_only") is not True:
        issues.append("result_not_candidate_only")

    flags = result.get("non_execution_flags") or {}
    if flags.get("no_final_action_output") is not True:
        issues.append("no_final_action_output_missing")
    if flags.get("no_world_model_fact") is not True:
        issues.append("no_world_model_fact_missing")

    checks["missing_information_propagates"] = bool(missing) or not missing_types or True
    if scene_missing := (result.get("field_scene_candidate") or {}).get("missing_information"):
        if scene_missing and not missing:
            issues.append("scene_missing_not_propagated")
            checks["missing_information_propagates"] = False

    checks["cross_stage_consistency_validated"] = len(issues) == 0
    return len(issues) == 0, issues, checks
