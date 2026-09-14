# -*- coding: utf-8 -*-
"""Dual route perception validation — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformDualRoutePerceptionValidationPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_PLANNING_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_GO",
)

FROZEN_CHAIN_STAGES = (
    "input_image",
    "route_a_grounding_detection",
    "route_a_bbox_candidate",
    "route_a_sam_refine",
    "route_a_mask_candidate",
    "route_b_vlm_observation",
    "route_b_scene_profile",
    "route_b_attention_route",
    "midplatform_dual_route_comparison",
    "dual_route_comparison_candidate",
    "next_task_candidate",
)

PLANNING_ENDPOINT = "dual_route_comparison_candidate"

ROUTE_A_ID = "route_a_detector_grounding_sam"
ROUTE_B_ID = "route_b_vlm_route_candidate"

ROUTE_A_OUTPUT_TYPES = (
    "grounding_detection_candidate",
    "detected_region_candidate",
    "bbox_candidate",
    "sam_refine_mask_candidate",
)

ROUTE_B_OUTPUT_TYPES = (
    "vlm_scene_candidate",
    "vlm_attention_candidate",
    "vlm_route_candidate",
)

ROUTE_A_SUITABLE_TARGETS = (
    "direction_sign",
    "station_name_board",
    "advertisement_panel",
    "screen_door",
    "door_area",
    "person_candidate",
    "vehicle_candidate",
    "warning_line_candidate",
)

SLAM_ALLOWED_ROLES = (
    "spatial_reference_candidate",
    "walkable_area_reference",
    "structure_reference",
    "pose_map_geometry_support",
)

SLAM_FORBIDDEN_TEXT_ROLES = (
    "text_detection",
    "text_recognition",
    "sign_identification",
    "ocr_route_direct_generation",
    "fact_text_generation",
)

COMPARISON_DIMENSIONS = (
    "region_overlap",
    "text_likelihood",
    "route_agreement",
    "route_conflict",
    "trace_completeness",
    "uncertainty",
    "recommended_next_task",
)

SMOKE_CASE_IDS = (
    "case_a_subway_direction_sign",
    "case_b_outdoor_street",
    "case_c_route_a_miss_route_b_hit",
    "case_d_route_conflict",
)

SMOKE_CASE_A_IMAGE = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png"
)

FORBIDDEN_OPERATIONS = (
    "no_slam_text_detection",
    "no_slam_text_recognition",
    "no_slam_ocr_route_direct_generation",
    "no_fact_write",
    "no_navigation_decision",
    "no_ocr_execution",
    "no_detection_execution",
    "no_vlm_fact_generation",
    "no_grounding_label_fact_upgrade",
    "no_sam_mask_fact_upgrade",
    "no_prompt_label_fact_upgrade",
    "no_mobile_sam_direct_to_ocr",
    "no_bypass_midplatform",
    "no_visual_expression_mutation",
    "no_boundary_clone",
    "human_correction_not_ground_truth",
)

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "route_a_candidate_only": True,
    "route_b_candidate_only": True,
    "dual_route_comparison_not_fact": True,
    "dual_route_conflict_not_auto_fact": True,
    "no_slam_for_text": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "no_ocr_execution": True,
    "no_detection_execution": True,
    "no_vlm_fact_generation": True,
}
