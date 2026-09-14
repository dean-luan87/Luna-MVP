# -*- coding: utf-8 -*-
"""Text-first target proposal validation — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformTextFirstTargetProposalValidationPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_DUAL_ROUTE_PERCEPTION_VALIDATION_EXECUTION_GO",
    "P1_MIDPLATFORM_SCENE_AWARE_SEGMENTATION_PROMPT_POLICY_EXECUTION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO",
)

PLANNING_ENDPOINT = "target_proposal_comparison_candidate"

CANDIDATE_TYPES = (
    "region_proposal_candidate",
    "text_region_candidate",
    "text_line_candidate",
    "text_block_candidate",
    "semantic_target_candidate",
    "target_proposal_comparison_candidate",
)

TEXT_FIRST_CHAIN_STAGES = (
    "input_image",
    "text_detector_stub",
    "text_region_candidate",
    "text_line_candidate",
    "text_block_candidate",
    "midplatform_target_selection",
    "target_proposal_comparison_candidate",
    "ocr_task_candidate",
)

FUSION_INPUT_TYPES = (
    "region_proposal_candidate",
    "text_region_candidate",
    "semantic_target_candidate",
)

SMOKE_CASE_IDS = (
    "case_a_subway_direction_sign_text",
    "case_b_shop_sign_text_block",
    "case_c_no_obvious_text",
    "case_d_sam_text_misalignment",
)

SUBWAY_IMAGE_REF = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png"
)
SHOP_SIGN_IMAGE_REF = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_shop_sign_nostalgic_flavor_v1_001.png"
)

FORBIDDEN_OPERATIONS = (
    "no_ocr_recognition",
    "no_text_fact_generation",
    "text_region_candidate_not_fact",
    "no_fact_write",
    "no_navigation_decision",
    "sam_not_primary_text_detector",
    "no_slam_text_detection",
    "text_detector_stub_not_ocr_result",
    "target_proposal_comparison_not_fact",
    "no_prompt_label_fact_upgrade",
    "no_human_correction_ground_truth",
)

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "no_ocr_recognition": True,
    "text_region_candidate_not_fact": True,
    "sam_not_primary_text_detector": True,
    "text_detector_stub_not_ocr_result": True,
    "target_proposal_comparison_not_fact": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "candidate_only_preserved": True,
}
