# -*- coding: utf-8 -*-
"""Field-First Core Logic — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

INPUT_PACKAGE_FIELDS: Tuple[str, ...] = (
    "input_package_id", "current_observation_candidates", "previous_field_scene_candidate",
    "previous_field_session_state", "previous_target_tracking_plan_candidate",
    "camera_state_candidate", "user_state_candidate", "task_goal_ref", "timestamp",
    "source_refs", "traceability_refs", "candidate_only",
)

RESULT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "result_candidate_id", "input_package_ref", "field_scene_candidate",
    "field_continuity_decision_candidate", "target_tracking_plan_candidate",
    "static_target_lock_candidates", "dynamic_target_track_candidates",
    "trajectory_candidates", "task_impact_analysis_candidates", "risk_projection_candidates",
    "missing_information_candidates", "warning_summary", "decision_readiness_summary",
    "pipeline_stage_results", "traceability_refs", "non_execution_flags", "candidate_only",
)

PIPELINE_STAGES: Tuple[str, ...] = (
    "step_1_build_small_range_field_scene",
    "step_2_detect_field_continuity",
    "step_3_build_static_dynamic_target_tracking",
    "step_4_build_trajectory_analysis_task_impact",
    "step_5_assemble_core_logic_result",
)

DECISION_READINESS_FLAGS: Tuple[str, ...] = (
    "ready_for_field_simulation_candidate",
    "need_more_observation",
    "blocked_by_missing_depth",
    "blocked_by_field_uncertainty",
    "blocked_by_tracking_frozen",
    "blocked_by_new_field_reset",
    "unsafe_to_infer_motion",
    "candidate_only_no_action",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_memory_write": True,
    "no_runtime_execution": True,
    "no_model_execution": True,
    "no_real_tracking_execution": True,
    "no_trajectory_prediction": True,
    "no_task_execution": True,
    "no_final_action_output": True,
    "no_field_simulation": True,
    "tracker_id_is_hint_not_fact": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_FIRST_CORE_LOGIC_FORMAL_IMPLEMENTATION_READY_FOR_FIELD_SIMULATION_PLANNING"
)
