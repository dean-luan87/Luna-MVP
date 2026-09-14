# -*- coding: utf-8 -*-
"""Trajectory Analysis & Task Impact Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

TRAJECTORY_MOTION_PATTERNS: Tuple[str, ...] = (
    "static", "likely_static", "moving_left", "moving_right", "moving_forward", "moving_away",
    "approaching_user", "moving_across_field", "crossing_user_path_candidate", "blocking_route_candidate",
    "leaving_risk_zone", "entering_risk_zone", "uncertain_motion", "unknown",
)

TRAJECTORY_CONFIDENCE_LEVELS: Tuple[str, ...] = ("high", "medium", "low", "unknown")

TRAJECTORY_RELIABILITY_REASONS: Tuple[str, ...] = (
    "sufficient_position_delta", "weak_position_delta", "missing_depth", "missing_previous_position",
    "frozen_tracking", "new_field_reset", "occlusion_present", "low_confidence_track",
    "tracker_hint_present", "tracker_hint_absent",
)

TASK_IMPACT_TYPES: Tuple[str, ...] = (
    "safety_risk", "navigation_risk", "route_blocker", "crossing_risk", "collision_candidate",
    "reading_blocker", "find_object_occluder", "elevator_state_relevant", "door_state_relevant",
    "traffic_light_relevant", "static_anchor_relevant", "background_only", "unknown",
)

TASK_IMPACT_PRIORITIES: Tuple[str, ...] = (
    "P0_safety_critical", "P1_task_relevant", "P2_context_anchor", "P3_background", "unknown",
)

TRAJECTORY_CANDIDATE_MODEL: Dict[str, Any] = {
    "model_id": "trajectory_candidate_model_v1",
    "output_type": "TrajectoryCandidate",
    "candidate_only": True,
    "tracker_id_is_hint_not_fact": True,
    "fields": (
        "trajectory_candidate_id", "field_session_ref", "dynamic_track_ref", "target_label",
        "previous_position", "current_position", "position_delta", "motion_pattern",
        "trajectory_confidence", "trajectory_reliability_reasons", "tracker_hint_id",
        "tracker_id_is_hint_not_fact", "source_refs", "evidence_refs", "reason_codes", "candidate_only",
    ),
}

TASK_IMPACT_ANALYSIS_MODEL: Dict[str, Any] = {
    "model_id": "task_impact_analysis_candidate_model_v1",
    "output_type": "TaskImpactAnalysisCandidate",
    "candidate_only": True,
    "fields": (
        "task_impact_analysis_id", "target_ref", "trajectory_ref", "static_lock_ref", "task_goal_ref",
        "target_label", "field_zone", "motion_pattern", "task_impact_type", "task_impact_priority",
        "task_relevance_score_discrete", "safety_relevant", "task_relevant", "background_only",
        "reason_codes", "missing_information", "candidate_only",
    ),
}

RISK_PROJECTION_MODEL: Dict[str, Any] = {
    "model_id": "risk_projection_candidate_model_v1",
    "output_type": "RiskProjectionCandidate",
    "candidate_only": True,
    "fields": (
        "risk_projection_id", "target_ref", "trajectory_ref", "risk_type", "risk_level",
        "time_horizon_hint", "risk_zone_hint", "affects_user_path_candidate", "requires_recheck",
        "reason_codes", "candidate_only",
    ),
}

MISSING_INFORMATION_MODEL: Dict[str, Any] = {
    "model_id": "missing_information_candidate_model_v1",
    "output_type": "MissingInformationCandidate",
    "candidate_only": True,
    "fields": (
        "missing_info_id", "target_ref", "missing_type", "affects_analysis",
        "recommended_recheck", "reason_codes", "candidate_only",
    ),
}

TRAJECTORY_TASK_IMPACT_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "dynamic_trajectory_rule", "desc": "tracking_allowed with positions enables TrajectoryCandidate"},
    {"rule_id": "frozen_tracking_rule", "desc": "tracking_frozen blocks new motion trend"},
    {"rule_id": "new_field_reset_rule", "desc": "tracking_reset no trajectory inheritance"},
    {"rule_id": "position_delta_rule", "desc": "position delta derives motion_pattern"},
    {"rule_id": "depth_uncertainty_rule", "desc": "estimated/unknown depth caps confidence at medium/low"},
    {"rule_id": "safety_priority_rule", "desc": "vehicle/person/obstacle inner_zone P0"},
    {"rule_id": "static_impact_rule", "desc": "static targets can yield TaskImpactAnalysis without trajectory"},
    {"rule_id": "missing_info_rule", "desc": "missing depth/position/task_goal explicit MissingInformation"},
    {"rule_id": "no_execution_rule", "desc": "no final action output"},
)

INPUT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "trajectory_task_impact_input_output_contract_v1",
    "inputs": (
        "TargetTrackingPlanCandidate", "StaticTargetLockCandidate", "DynamicTargetTrackCandidate",
        "FieldContinuityDecisionCandidate", "optional task_goal_ref",
    ),
    "outputs": (
        "TrajectoryCandidate", "TaskImpactAnalysisCandidate", "RiskProjectionCandidate", "MissingInformationCandidate",
    ),
    "candidate_only": True,
    "no_final_action_output": True,
}

NEXT_IMPLEMENTATION_PLAN: Dict[str, Any] = {
    "recommended_next": "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001",
    "deferred_to_skeleton": ("trajectory_builder", "task_impact_analyzer", "risk_projection_builder", "mock_dryrun"),
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_trajectory_prediction", "real_tracking", "bytetrack", "yolo", "supervision",
        "model_download", "real_inference", "field_simulation", "task_execution",
        "navigation_instruction_output", "world_model_fact", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_trajectory_prediction", "task_impact_not_final_action",
    "risk_projection_not_world_model_fact", "planning_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Controlled-Skeleton-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Trajectory Analysis Task Impact Controlled Skeleton Implementation"


def _case(
    case_id: str, traj: Tuple[str, ...], impact: Tuple[str, ...], risk: Tuple[str, ...],
    missing: Tuple[str, ...], prohibited: Tuple[str, ...], pass_cond: str,
    tracking_summary: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "input_tracking_plan_summary": tracking_summary or {"mock": True},
        "expected_trajectory_candidates": list(traj),
        "expected_task_impact_candidates": list(impact),
        "expected_risk_projection_candidates": list(risk),
        "expected_missing_information": list(missing),
        "expected_prohibited_behavior": list(prohibited),
        "pass_condition": pass_cond,
    }


MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    _case("person_approaching_user", ("person:approaching_user",), ("person:safety_risk",), ("person:collision_candidate",), (), ("final_action",), "approaching_trajectory"),
    _case("vehicle_crossing_user_path_candidate", ("vehicle:crossing_user_path_candidate",), ("vehicle:crossing_risk",), ("vehicle:safety_risk",), (), ("navigation_instruction",), "crossing_path"),
    _case("obstacle_static_inner_zone_route_blocker", (), ("obstacle:route_blocker",), ("obstacle:navigation_risk",), (), (), "static_inner_zone"),
    _case("traffic_light_static_task_relevant", (), ("traffic_light:traffic_light_relevant",), (), (), (), "static_traffic_light"),
    _case("elevator_door_state_relevant_static", (), ("elevator:elevator_state_relevant",), (), (), (), "static_elevator"),
    _case("moving_target_missing_depth_low_confidence", ("person:uncertain_motion",), ("person:safety_risk",), (), ("depth:missing_depth",), ("high_confidence_despite_unknown_depth",), "depth_caps_confidence"),
    _case("moving_target_without_previous_position_missing_info", (), (), (), ("position:missing_previous_position",), ("infer_trajectory_without_position",), "missing_prev_position"),
    _case("field_occluded_freezes_trajectory", (), (), (), ("tracking:frozen_tracking",), ("new_motion_trend",), "frozen_no_trajectory", {"tracking_frozen": True}),
    _case("new_field_resets_trajectory", (), (), (), ("tracking:new_field_reset",), ("inherit_old_trajectory",), "reset_no_inherit", {"tracking_reset": True}),
    _case("person_moving_away_lower_risk", ("person:moving_away",), ("person:background_only",), (), (), (), "moving_away"),
    _case("text_region_reading_blocked_by_person", ("person:blocking_route_candidate",), ("text_region:reading_blocker", "person:reading_blocker",), ("person:navigation_risk",), (), (), "reading_blocked"),
    _case("duplicate_dynamic_targets_separate_trajectories", ("person:approaching_user", "person:moving_across_field",), ("person:safety_risk", "person:safety_risk",), ("person:collision_candidate", "person:crossing_risk",), (), ("merge_duplicate_tracks",), "separate_trajectories"),
)
