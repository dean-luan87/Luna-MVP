# -*- coding: utf-8 -*-
"""Dual route perception validation — execution types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Dual-Route-Perception-Validation-Execution-v1-001"
SYSTEM_ID = "LunaMidplatformDualRoutePerceptionValidationExecutionV1"
EXECUTION_ONLY = True
PLANNING_ONLY = False
NO_MODEL_CALL = True

PLANNING_ENDPOINT = "dual_route_comparison_candidate"

ROUTE_A_ID = "route_a_detector_grounding_sam"
ROUTE_B_ID = "route_b_vlm_route_candidate"

SUBWAY_IMAGE_REF = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png"
)
STREET_IMAGE_REF = (
    "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_001.png"
)

SMOKE_CASE_IDS = (
    "case_a_subway_direction_sign",
    "case_b_outdoor_street",
    "case_c_route_a_miss_route_b_hit",
    "case_d_route_conflict",
)

FINAL_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_SMOKE_BLOCKED"

BOUNDARY_FLAGS = {
    "execution_only": True,
    "no_model_call": True,
    "route_a_candidate_only": True,
    "route_b_candidate_only": True,
    "dual_route_comparison_not_fact": True,
    "dual_route_conflict_not_auto_fact": True,
    "no_slam_for_text": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "no_ocr_execution": True,
    "no_detection_execution": True,
    "no_vlm_execution": True,
    "no_grounding_real_model_call": True,
    "no_vlm_real_model_call": True,
}
