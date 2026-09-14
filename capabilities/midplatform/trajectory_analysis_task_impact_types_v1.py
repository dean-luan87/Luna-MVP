# -*- coding: utf-8 -*-
"""Trajectory Analysis & Task Impact — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

TRAJECTORY_FIELDS: Tuple[str, ...] = (
    "trajectory_candidate_id", "field_session_ref", "dynamic_track_ref", "target_label",
    "previous_position", "current_position", "position_delta", "motion_pattern",
    "trajectory_confidence", "trajectory_reliability_reasons", "tracker_hint_id",
    "tracker_id_is_hint_not_fact", "source_refs", "evidence_refs", "reason_codes", "candidate_only",
)

TASK_IMPACT_ANALYSIS_FIELDS: Tuple[str, ...] = (
    "task_impact_analysis_id", "target_ref", "trajectory_ref", "static_lock_ref", "task_goal_ref",
    "target_label", "field_zone", "motion_pattern", "task_impact_type", "task_impact_priority",
    "task_relevance_score_discrete", "safety_relevant", "task_relevant", "background_only",
    "reason_codes", "missing_information", "candidate_only",
)

RISK_PROJECTION_FIELDS: Tuple[str, ...] = (
    "risk_projection_id", "target_ref", "trajectory_ref", "risk_type", "risk_level",
    "time_horizon_hint", "risk_zone_hint", "affects_user_path_candidate", "requires_recheck",
    "reason_codes", "candidate_only",
)

MISSING_INFO_FIELDS: Tuple[str, ...] = (
    "missing_info_id", "target_ref", "missing_type", "affects_analysis",
    "recommended_recheck", "reason_codes", "candidate_only",
)

ANALYSIS_RESULT_FIELDS: Tuple[str, ...] = (
    "analysis_result_id", "field_session_ref", "trajectory_candidates", "task_impact_analysis_candidates",
    "risk_projection_candidates", "missing_information_candidates", "tracking_allowed", "tracking_frozen",
    "tracking_reset", "reason_codes", "non_execution_flags",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_runtime_execution": True,
    "no_real_tracking_execution": True,
    "no_trajectory_prediction": True,
    "no_task_execution": True,
    "no_final_action_output": True,
    "tracker_id_is_hint_not_fact": True,
}

SAFETY_LABELS: Tuple[str, ...] = ("person", "vehicle", "bicycle", "scooter", "moving_obstacle")
STATIC_IMPACT_LABELS: Dict[str, str] = {
    "door": "door_state_relevant",
    "elevator": "elevator_state_relevant",
    "traffic_light": "traffic_light_relevant",
    "sign": "static_anchor_relevant",
    "text_region": "reading_blocker",
    "obstacle": "route_blocker",
}
