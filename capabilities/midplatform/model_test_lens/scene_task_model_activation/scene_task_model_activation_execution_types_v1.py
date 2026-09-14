# -*- coding: utf-8
"""Scene-Task Model Activation — execution types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Scene-Task-Model-Activation-Execution-v1-001"
SYSTEM_ID = "LunaMidplatformSceneTaskModelActivationExecutionV1"
EXECUTION_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_PLANNING_GO",
    "P1_MIDPLATFORM_TEXT_FIRST_TARGET_PROPOSAL_VALIDATION_PLANNING_GO",
    "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO",
)

PLANNING_ENDPOINT = "model_activation_plan_candidate"

SMOKE_CASE_IDS = (
    "case_a_shopfront_sign",
    "case_b_subway_direction_sign",
    "case_c_street_crossing",
    "case_d_spatial_navigation",
    "case_e_unknown_scene",
    "case_ui_static_audit",
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

FINAL_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_BLOCKED"
SMOKE_GO = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_SMOKE_GO"
SMOKE_BLOCKED = "P1_MIDPLATFORM_SCENE_TASK_MODEL_ACTIVATION_EXECUTION_SMOKE_BLOCKED"

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Text-First-Target-Proposal-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "execution_only": True,
    "model_activation_candidate_not_fact": True,
    "no_blanket_model_activation": True,
    "noop_record_required_for_inactive_models": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "no_runner_execution_in_activation_execution": True,
    "no_boundary_clone": True,
    "human_correction_not_ground_truth": True,
}
