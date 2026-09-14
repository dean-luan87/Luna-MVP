# -*- coding: utf-8 -*-
"""Task impact analyzer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.trajectory_analysis_task_impact_types_v1 import (
    SAFETY_LABELS,
    STATIC_IMPACT_LABELS,
)


def _priority(label: str, impact_type: str, field_zone: str = "unknown") -> str:
    if label in SAFETY_LABELS or field_zone == "inner_zone" or impact_type in (
        "safety_risk", "collision_candidate", "crossing_risk",
    ):
        return "P0_safety_critical"
    if impact_type in ("route_blocker", "reading_blocker", "traffic_light_relevant", "door_state_relevant", "elevator_state_relevant"):
        return "P1_task_relevant"
    if impact_type == "background_only":
        return "P3_background"
    return "P2_context_anchor"


def _impact_from_motion(label: str, motion: Optional[str]) -> str:
    if motion in ("approaching_user", "entering_risk_zone"):
        return "safety_risk" if label in SAFETY_LABELS else "navigation_risk"
    if motion == "crossing_user_path_candidate":
        return "crossing_risk"
    if motion == "blocking_route_candidate":
        return "reading_blocker" if label == "person" else "route_blocker"
    if motion == "moving_away":
        return "background_only"
    if label in SAFETY_LABELS:
        return "safety_risk"
    return "unknown"


def analyze_static_task_impacts(
    *,
    tracking_plan: Dict[str, Any],
    task_goal_ref: Optional[str] = None,
) -> List[Dict[str, Any]]:
    analyses: List[Dict[str, Any]] = []
    for lock in tracking_plan.get("static_locks") or []:
        label = lock.get("label", "unknown")
        impact_type = STATIC_IMPACT_LABELS.get(label, "static_anchor_relevant")
        if lock.get("field_zone") == "inner_zone" and label == "obstacle":
            impact_type = "route_blocker"
        priority = _priority(label, impact_type, lock.get("field_zone", "unknown"))
        analyses.append({
            "task_impact_analysis_id": f"tia_{uuid.uuid4().hex[:12]}",
            "target_ref": lock.get("entity_candidate_ref"),
            "trajectory_ref": None,
            "static_lock_ref": lock.get("lock_candidate_id"),
            "task_goal_ref": task_goal_ref,
            "target_label": label,
            "field_zone": lock.get("field_zone", "unknown"),
            "motion_pattern": None,
            "task_impact_type": impact_type,
            "task_impact_priority": priority,
            "task_relevance_score_discrete": 3 if priority.startswith("P0") else 2,
            "safety_relevant": priority == "P0_safety_critical",
            "task_relevant": priority in ("P0_safety_critical", "P1_task_relevant"),
            "background_only": impact_type == "background_only",
            "reason_codes": [f"static_impact_{impact_type}"],
            "missing_information": [],
            "candidate_only": True,
        })
    return analyses


def analyze_dynamic_task_impacts(
    *,
    tracking_plan: Dict[str, Any],
    trajectories: List[Dict[str, Any]],
    task_goal_ref: Optional[str] = None,
) -> List[Dict[str, Any]]:
    analyses: List[Dict[str, Any]] = []
    traj_by_track = {t.get("dynamic_track_ref"): t for t in trajectories}
    for track in tracking_plan.get("dynamic_tracks") or []:
        traj = traj_by_track.get(track.get("track_candidate_id"))
        motion = traj.get("motion_pattern") if traj else None
        label = track.get("label", "unknown")
        impact_type = _impact_from_motion(label, motion)
        priority = _priority(label, impact_type)
        analyses.append({
            "task_impact_analysis_id": f"tia_{uuid.uuid4().hex[:12]}",
            "target_ref": track.get("current_entity_candidate_ref"),
            "trajectory_ref": traj.get("trajectory_candidate_id") if traj else None,
            "static_lock_ref": None,
            "task_goal_ref": task_goal_ref,
            "target_label": label,
            "field_zone": "unknown",
            "motion_pattern": motion,
            "task_impact_type": impact_type,
            "task_impact_priority": priority,
            "task_relevance_score_discrete": 3 if priority.startswith("P0") else 1,
            "safety_relevant": priority == "P0_safety_critical",
            "task_relevant": not (impact_type == "background_only"),
            "background_only": impact_type == "background_only",
            "reason_codes": [f"dynamic_impact_{impact_type}"],
            "missing_information": [],
            "candidate_only": True,
        })
    return analyses


def collect_missing_information(
    *,
    tracking_plan: Dict[str, Any],
    trajectories: List[Dict[str, Any]],
    depth_source: str = "estimated",
) -> List[Dict[str, Any]]:
    missing: List[Dict[str, Any]] = []
    if tracking_plan.get("tracking_frozen"):
        missing.append({
            "missing_info_id": f"mi_{uuid.uuid4().hex[:12]}",
            "target_ref": None,
            "missing_type": "frozen_tracking",
            "affects_analysis": True,
            "recommended_recheck": True,
            "reason_codes": ["frozen_tracking_rule"],
            "candidate_only": True,
        })
    if tracking_plan.get("tracking_reset"):
        missing.append({
            "missing_info_id": f"mi_{uuid.uuid4().hex[:12]}",
            "target_ref": None,
            "missing_type": "new_field_reset",
            "affects_analysis": True,
            "recommended_recheck": True,
            "reason_codes": ["new_field_reset_rule"],
            "candidate_only": True,
        })
    if depth_source == "unknown":
        for track in tracking_plan.get("dynamic_tracks") or []:
            missing.append({
                "missing_info_id": f"mi_{uuid.uuid4().hex[:12]}",
                "target_ref": track.get("current_entity_candidate_ref"),
                "missing_type": "missing_depth",
                "affects_analysis": True,
                "recommended_recheck": True,
                "reason_codes": ["depth_uncertainty_rule"],
                "candidate_only": True,
            })
    for track in tracking_plan.get("dynamic_tracks") or []:
        if not track.get("previous_pseudo_3d_position") and not track.get("previous_bbox"):
            missing.append({
                "missing_info_id": f"mi_{uuid.uuid4().hex[:12]}",
                "target_ref": track.get("current_entity_candidate_ref"),
                "missing_type": "missing_previous_position",
                "affects_analysis": True,
                "recommended_recheck": True,
                "reason_codes": ["missing_info_rule"],
                "candidate_only": True,
            })
    if not trajectories and (tracking_plan.get("dynamic_tracks") or []) and tracking_plan.get("tracking_allowed"):
        if not any(m.get("missing_type") == "missing_previous_position" for m in missing):
            pass
    return missing
