# -*- coding: utf-8 -*-
"""Scene-Task Model Activation — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Scene-Task-Model-Activation-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformSceneTaskModelActivationPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO",
    "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
)

PLANNING_ENDPOINT = "model_activation_plan_candidate"

SCENE_TYPES = (
    "text_signage_scene",
    "subway_platform",
    "shopfront_sign",
    "outdoor_street_crossing",
    "indoor_navigation",
    "corridor",
    "unknown_scene",
)

TASK_INTENTS = (
    "read_text",
    "find_direction",
    "identify_object",
    "assess_walkable_area",
    "track_dynamic_target",
    "understand_scene",
    "locate_place",
    "manual_review",
)

MODELS = (
    "ocr_text_detector",
    "ocr_recognizer",
    "detection",
    "depth",
    "tracking",
    "slam",
    "vlm_route_enhancer",
    "mobile_sam_region_proposal",
)

SMOKE_CASE_IDS = (
    "case_a_shopfront_sign",
    "case_b_subway_direction_sign",
    "case_c_street_crossing",
    "case_d_spatial_navigation",
    "case_e_unknown_scene",
)

SHOP_SIGN_IMAGE_REF = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png"
)
SUBWAY_IMAGE_REF = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png"
)
STREET_IMAGE_REF = (
    "capabilities/test_assets/p1/mobile_sam/multi/mobile_sam_multi_real_image_street_scene_v1_001.png"
)

FINAL_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "model_activation_candidate_not_fact": True,
    "no_blanket_model_activation": True,
    "noop_record_required_for_inactive_models": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "no_runner_execution_in_planning": True,
    "no_boundary_clone": True,
    "human_correction_not_ground_truth": True,
}
