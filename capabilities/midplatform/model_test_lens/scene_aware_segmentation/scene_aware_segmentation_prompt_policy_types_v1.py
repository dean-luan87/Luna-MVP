# -*- coding: utf-8 -*-
"""Scene-aware segmentation prompt policy — planning types v1."""

from __future__ import annotations

PHASE_REF = "Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Planning-v1-001"
SYSTEM_ID = "LunaMidplatformSceneAwareSegmentationPromptPolicyPlanningV1"
PLANNING_ONLY = True

UPSTREAM_GO = (
    "P1_MIDPLATFORM_MODEL_TEST_LENS_MOBILESAM_SINGLE_MODEL_EXECUTION_INTEGRATION_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_OBSERVATION_ATTENTION_LAYER_PLANNING_GO",
    "P1_MIDPLATFORM_MODEL_TEST_LENS_VISUAL_EXPRESSION_SYSTEM_PLANNING_GO",
    "P1_MIDPLATFORM_MULTI_MODEL_INTERACTION_MOBILE_SAM_OCR_RUNNER_SANDBOX_INTEGRATION_EXECUTION_GO",
)

FROZEN_CHAIN_STAGES = (
    "input_image",
    "scene_profile_candidate",
    "segmentation_prompt_policy",
    "mobilesam_prompt_set",
    "region_candidate",
    "observation_attention",
    "followup_route_candidate",
    "detection_ocr_depth_slam_review",
)

PLANNING_ENDPOINT = "segmentation_prompt_policy"

SCENE_PROFILE_TYPES = (
    "outdoor_street",
    "subway_platform",
    "indoor_station",
    "indoor_mall",
    "corridor",
    "store_front",
    "unknown_scene",
)

LEGACY_OUTDOOR_STREET_PROMPTS_FORBIDDEN_FOR_SUBWAY = (
    "road_sign",
    "left_building",
    "center_advertisement_screen",
    "front_vehicle",
    "crosswalk_or_road_region",
)

SUBWAY_PLATFORM_OCR_PROMPTS = (
    "station_direction_sign",
    "station_name_board",
    "route_map_or_line_info",
    "advertisement_panel",
)

SUBWAY_PLATFORM_PROMPT_SET = (
    "station_direction_sign",
    "station_name_board",
    "route_map_or_line_info",
    "platform_screen_door",
    "train_door_area",
    "advertisement_panel",
    "warning_line_or_platform_edge",
    "floor_walkable_area",
    "people_region",
    "large_static_structure",
)

OUTDOOR_STREET_PROMPT_SET = (
    "road_sign_candidate",
    "crosswalk_or_road_region",
    "vehicle_candidate",
    "advertisement_panel",
    "building_structure",
)

ALLOWED_MAIN_CANVAS_TASK_LABELS = (
    "P0 文字候选区",
    "P0 通行结构区",
    "P1 屏幕/标识候选",
    "P1 动态目标候选",
    "P2 大型结构候选",
    "P0 观察候选",
)

FORBIDDEN_MAIN_CANVAS_PROMPT_FACT_LABELS = (
    "路牌",
    "前方车辆",
    "广告屏",
    "道路区域",
    "左侧建筑",
    "车辆",
    "指示牌",
)

PROMPT_LABEL_DOWNGRADE_FIELDS = (
    "segmentation_prompt_id",
    "source_prompt_hint",
    "candidate_only",
    "prompt_is_not_fact",
    "semantic_label",
)

FORBIDDEN_OPERATIONS = (
    "no_model_call",
    "no_fact_write",
    "no_navigation_decision",
    "no_runner_architecture_mutation",
    "no_prompt_label_fact_upgrade",
    "no_mobilesam_semantic_fact_output",
    "no_fixed_outdoor_prompt_for_subway_profile",
)

SUBWAY_SMOKE_IMAGE_REL = (
    "capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png"
)

SUBWAY_SMOKE_EXPECTATIONS = (
    "subway_profile_uses_station_prompt_set",
    "station_direction_sign_covers_jiahuihu_or_ocr_route",
    "people_region_not_labeled_as_road_sign",
    "no_legacy_street_prompts_on_subway_profile",
)

RECOMMENDED_NEXT_PHASE = (
    "Phase-P1-Midplatform-Scene-Aware-Segmentation-Prompt-Policy-Execution-v1-001"
)

BOUNDARY_FLAGS = {
    "planning_only": True,
    "scene_profile_candidate_not_fact": True,
    "mobilesam_region_not_semantic_fact": True,
    "no_prompt_label_fact_upgrade": True,
    "prompt_label_display_not_fact": True,
    "ocr_route_requires_text_likely_candidate": True,
    "no_fact_write": True,
    "no_navigation_decision": True,
    "no_runner_architecture_mutation": True,
    "ui_marker_uses_task_semantics_not_prompt_label": True,
    "subway_profile_uses_station_prompt_set": True,
    "no_fixed_outdoor_prompt_for_subway_profile": True,
}
