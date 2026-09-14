# -*- coding: utf-8 -*-
"""Field Simulation — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

SIMULATION_MODES: Tuple[str, ...] = (
    "current_state_simulation",
    "short_horizon_motion_projection",
    "occlusion_and_missing_info_simulation",
    "task_relevance_field_projection",
    "safety_risk_projection",
    "field_quality_projection",
)

SIMULATION_STATUSES: Tuple[str, ...] = (
    "generated",
    "generated_degraded",
    "blocked_insufficient_input",
    "blocked_no_scene",
    "blocked_no_entity",
    "blocked_quality_insufficient",
)

INPUT_VIEW_FIELDS: Tuple[str, ...] = (
    "simulation_input_id", "enhanced_field_scene_ref", "source_case_type",
    "frame_ref", "timestamp", "entity_candidates", "zone_summary",
    "traceability_refs", "candidate_only",
)

ELIGIBILITY_FIELDS: Tuple[str, ...] = (
    "eligibility_id", "simulation_input_ref", "eligible_modes", "blocked_modes",
    "eligibility_status", "eligibility_reasons", "limitations", "candidate_only",
)

PLAN_FIELDS: Tuple[str, ...] = (
    "simulation_plan_id", "simulation_input_ref", "selected_modes", "deferred_modes",
    "blocked_modes", "simulation_scope", "assumptions", "limitations",
    "warning_codes", "readiness_for_simulation_result_generation", "candidate_only",
)

SIMULATION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "simulation_candidate_id", "simulation_plan_ref", "mode", "input_scene_ref",
    "confidence_level", "simulation_status", "no_action_output", "no_fact_output",
    "source_refs", "traceability_refs", "candidate_only",
)

READINESS_FIELDS: Tuple[str, ...] = (
    "readiness_id", "simulation_plan_ref",
    "readiness_for_current_state_simulation",
    "readiness_for_short_horizon_projection",
    "readiness_for_occlusion_missing_info_simulation",
    "readiness_for_task_relevance_projection",
    "readiness_for_safety_risk_projection",
    "readiness_for_field_quality_projection",
    "readiness_for_task_reasoning_planning",
    "blockers", "warnings", "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_task_reasoning": True,
    "no_navigation_action": True,
    "no_action_output": True,
    "no_fact_output": True,
    "no_fact_admission": True,
    "no_scene_graph": True,
    "no_slam": True,
    "no_real_yolo_rerun": True,
    "no_real_depth_rerun": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "skeleton_only_no_runtime": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = "MIDPLATFORM_FIELD_SIMULATION_SKELETON_READY_FOR_TASK_REASONING_PLANNING"
