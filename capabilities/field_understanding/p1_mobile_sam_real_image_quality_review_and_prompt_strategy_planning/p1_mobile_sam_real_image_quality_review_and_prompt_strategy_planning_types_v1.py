# -*- coding: utf-8 -*-
"""P1 MobileSAM Real Image Quality Review And Prompt Strategy Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-MobileSAM-Real-Image-Quality-Review-And-Prompt-Strategy-Planning-v1-001"
SCOPE = "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning"
WEIGHT_CHAIN = "p1_mobile_sam_real_image_quality_review_and_prompt_strategy_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "仅 real image quality review + prompt strategy planning，scope=mobile_sam_only。"
    "读取上一阶段 candidate mask metadata、quality summary、post-review 产物与 mask 文件引用，"
    "审查 5 个 prompt 质量、沉淀 prompt 策略、failure mode、detector/OCR/semantic 辅助需求、多图测试路线。"
    "不再次 inference、不读新图、不 import/model load、不 runtime/output/semantic/fact/navigation、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "quality_review_is_not_runtime_approval_masks_are_not_facts"
)

PLANNING_ONLY = True
QUALITY_REVIEW_PLANNING = True
PROMPT_STRATEGY_PLANNING = True
MOBILE_SAM_ONLY = True
CANDIDATE_MASK_METADATA_REVIEW_ALLOWED = True
CANDIDATE_MASK_FILE_REFERENCE_ALLOWED = True
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
NEW_IMAGE_READ_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
DATASET_BATCH_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_EXECUTION_REF = (
    "Phase-P1-MobileSAM-Real-Local-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)
UPSTREAM_EXECUTION_EXPECTED_GO = "P1_MOBILE_SAM_REAL_LOCAL_IMAGE_INFERENCE_TRIAL_EXECUTION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_EXECUTION_ROOT_REL = (
    "_tmp_eval_out/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_v1_smoke_v0"
)
UPSTREAM_REVIEW_REL = f"{UPSTREAM_EXECUTION_ROOT_REL}/p1_mobile_sam_real_local_image_inference_trial_execution_and_post_review_review_v1.json"
UPSTREAM_MASKS_REL = f"{UPSTREAM_EXECUTION_ROOT_REL}/real_local_image_candidate_masks_v1.json"
UPSTREAM_QUALITY_REL = f"{UPSTREAM_EXECUTION_ROOT_REL}/real_local_image_quality_summary_v1.json"
UPSTREAM_POST_REVIEW_REL = f"{UPSTREAM_EXECUTION_ROOT_REL}/real_local_image_post_review_audit_v1.json"
UPSTREAM_MASKS_DIR_REL = f"{UPSTREAM_EXECUTION_ROOT_REL}/candidate_masks"

CANONICAL_TEST_ASSET_PATH = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/capabilities/test_assets/p1/mobile_sam/"
    "mobile_sam_real_local_image_street_scene_v1.png"
)
IMAGE_WIDTH = 767
IMAGE_HEIGHT = 1024
SCENE_TYPE = "dusk_urban_street_scene"
PROMPT_COUNT = 5

ROUTE_A = "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
ROUTE_B = "Phase-P1-MobileSAM-Detector-Assisted-Prompt-Planning-v1-001"
ROUTE_C = "Phase-P1-MobileSAM-Real-Image-Quality-Review-Post-Review-Closure-v1-001"
RECOMMENDED_ROUTE = ROUTE_A

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

PER_PROMPT_QUALITY_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "prompt_id": "left_building",
        "stability": "high",
        "quality_tier": "best",
        "prompt_strategy": "box_prompt_preferred",
        "reason": "large_structured_object_with_clear_edges",
        "risk": "repeated_window_patterns_glass_reflection",
    },
    {
        "prompt_id": "crosswalk_or_road_region",
        "stability": "medium_high",
        "quality_tier": "good_but_may_overexpand",
        "prompt_strategy": "box_plus_negative_or_multi_point_recommended",
        "reason": "large_flat_region_easy_to_expand",
        "risk": "over_segmentation_road_marking_boundary_ambiguity",
    },
    {
        "prompt_id": "center_advertisement_screen",
        "stability": "medium",
        "quality_tier": "medium",
        "prompt_strategy": "box_prompt_preferred_with_tighter_box",
        "reason": "bright_rectangle_object",
        "risk": "glow_screen_reflection_adjacent_building_merge",
    },
    {
        "prompt_id": "road_sign",
        "stability": "medium",
        "quality_tier": "medium_small_region",
        "prompt_strategy": "detector_or_ocr_assisted_box_recommended",
        "reason": "small_sign_with_text_and_poles",
        "risk": "small_object_text_region_fragmentation",
    },
    {
        "prompt_id": "front_vehicle",
        "stability": "low_to_medium",
        "quality_tier": "weakest",
        "prompt_strategy": "detector_assisted_box_or_multi_point_recommended",
        "reason": "small_dark_vehicle_shadow_road_merge",
        "risk": "weak_boundary_small_area_vehicle_background_merge",
    },
)

FAILURE_MODES: Tuple[Dict[str, Any], ...] = (
    {
        "mode_id": "low_light_boundary_loss",
        "symptom": "object_edges_blur_into_background",
        "likely_cause": "dusk_low_contrast_lighting",
        "mitigation": "exposure_normalization_or_detector_assisted_box",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "medium",
    },
    {
        "mode_id": "glare_and_reflection_merge",
        "symptom": "mask_bleeds_into_reflection_or_glow",
        "likely_cause": "glass_screen_headlight_reflection",
        "mitigation": "tighter_box_negative_points",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "medium",
    },
    {
        "mode_id": "small_object_under_segmentation",
        "symptom": "tiny_mask_area_low_score",
        "likely_cause": "small_prompt_target_vehicle_or_sign",
        "mitigation": "detector_assisted_box_multi_point",
        "requires_detector_or_ocr": True,
        "runtime_admission_risk": "high",
    },
    {
        "mode_id": "large_plane_over_segmentation",
        "symptom": "road_mask_expands_beyond_intended_region",
        "likely_cause": "uniform_asphalt_texture",
        "mitigation": "negative_points_road_boundary_prior",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "high",
    },
    {
        "mode_id": "repeated_pattern_confusion",
        "symptom": "building_windows_merge_across_facade",
        "likely_cause": "repetitive_architectural_pattern",
        "mitigation": "tighter_vertical_box",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "low",
    },
    {
        "mode_id": "shadow_vehicle_merge",
        "symptom": "vehicle_mask_includes_shadow_or_road",
        "likely_cause": "dark_vehicle_on_dark_road",
        "mitigation": "detector_box_plus_negative_points",
        "requires_detector_or_ocr": True,
        "runtime_admission_risk": "high",
    },
    {
        "mode_id": "text_region_fragmentation",
        "symptom": "sign_mask_splits_or_misses_text_panel",
        "likely_cause": "fine_text_and_pole_structure",
        "mitigation": "ocr_detector_localized_box",
        "requires_detector_or_ocr": True,
        "runtime_admission_risk": "medium",
    },
    {
        "mode_id": "prompt_box_too_loose",
        "symptom": "mask_includes_adjacent_objects",
        "likely_cause": "normalized_box_covers_multiple_objects",
        "mitigation": "tighter_box_or_multi_point_refinement",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "medium",
    },
    {
        "mode_id": "prompt_point_ambiguous",
        "symptom": "unstable_mask_when_point_used",
        "likely_cause": "ambiguous_click_region",
        "mitigation": "prefer_box_or_multi_point",
        "requires_detector_or_ocr": False,
        "runtime_admission_risk": "medium",
    },
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "upstream_execution_go", "depends_on": "upstream_execution_go"},
    {"guard_id": "invalid_b_re_inference", "go_key": "no_re_inference", "depends_on": "no_re_inference"},
    {"guard_id": "invalid_c_new_image_or_non_upstream", "go_key": "upstream_artifacts_only", "depends_on": "upstream_artifacts_only"},
    {"guard_id": "invalid_d_import_model_load", "go_key": "no_import_load", "depends_on": "no_import_load"},
    {"guard_id": "invalid_e_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_prompt_label_as_fact", "go_key": "prompt_labels_not_facts", "depends_on": "prompt_labels_not_facts"},
    {"guard_id": "invalid_h_quality_summary_as_fact", "go_key": "quality_summary_not_fact", "depends_on": "quality_summary_not_fact"},
    {"guard_id": "invalid_i_runtime_ready_interpretation", "go_key": "no_runtime_ready_granted", "depends_on": "no_runtime_ready_granted"},
    {"guard_id": "invalid_j_missing_per_prompt", "go_key": "per_prompt_assessment_complete", "depends_on": "per_prompt_assessment_complete"},
    {"guard_id": "invalid_k_missing_prompt_strategy", "go_key": "prompt_strategy_defined", "depends_on": "prompt_strategy_defined"},
    {"guard_id": "invalid_l_missing_failure_taxonomy", "go_key": "failure_mode_taxonomy_defined", "depends_on": "failure_mode_taxonomy_defined"},
    {"guard_id": "invalid_m_missing_detector_need", "go_key": "detector_need_assessed", "depends_on": "detector_need_assessed"},
    {"guard_id": "invalid_n_missing_runtime_boundary", "go_key": "runtime_boundary_preserved", "depends_on": "runtime_boundary_preserved"},
    {"guard_id": "invalid_o_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_real_image_quality_review_and_prompt_strategy_planning_only",
    "no_new_inference_is_allowed",
    "no_new_image_input_is_allowed",
    "no_import_is_allowed",
    "no_model_load_is_allowed",
    "no_runtime_execution_is_allowed",
    "no_output_adapter_is_allowed",
    "no_semantic_layer_is_allowed",
    "no_fact_write_is_allowed",
    "no_navigation_action_speech_is_allowed",
    "no_registry_mutation_is_allowed",
    "prompt_labels_are_test_descriptions_only",
    "prompt_labels_are_not_semantic_facts",
    "candidate_masks_remain_candidate_artifacts",
    "quality_summary_is_not_fact",
    "runtime_readiness_is_not_granted",
    "output_adapter_readiness_is_not_granted",
    "semantic_fact_navigation_readiness_is_not_granted",
    "detector_ocr_semantic_prompt_generation_requires_separate_governance",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "real_image_quality_review_scope_record",
    "real_image_candidate_mask_quality_assessment_record",
    "per_prompt_quality_assessment_record",
    "prompt_strategy_recommendation_record",
    "failure_mode_taxonomy_record",
    "detector_ocr_semantic_prompt_generation_need_record",
    "multi_image_trial_route_record",
    "runtime_boundary_preservation_record",
    "followup_phase_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_REAL_IMAGE_QUALITY_REVIEW_PROMPT_STRATEGY_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_REAL_IMAGE_QUALITY_REVIEW_PROMPT_STRATEGY_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "upstream_execution_artifacts_reused": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMRealImageQualityReviewPromptStrategyPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    quality_review_planning: bool
    prompt_strategy_planning: bool
    mobile_sam_only: bool
    candidate_mask_metadata_review_allowed: bool
    candidate_mask_file_reference_allowed: bool
    real_inference_allowed: bool
    new_image_read_allowed: bool
    runtime_execution_allowed: bool
    registry_mutation_allowed: bool
    upstream_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RealImageQualityReviewScopeRecord:
    record_id: str
    upstream_execution_ref: str
    upstream_execution_go: str
    canonical_test_asset_path: str
    image_width: int
    image_height: int
    scene_type: str
    prompt_count: int
    prompt_success_count: int
    candidate_masks_written: bool
    review_reads_upstream_metadata_only: bool
    new_inference_executed: bool
    new_image_read: bool


@dataclass(frozen=True)
class RealImageCandidateMaskQualityAssessmentRecord:
    record_id: str
    overall_quality_observation_available: bool
    all_prompts_produced_masks: bool
    candidate_only: bool
    not_semantic_fact: bool
    human_review_required: bool
    suitable_for_runtime_admission: bool


@dataclass(frozen=True)
class PerPromptQualityAssessmentRecord:
    record_id: str
    assessments: Tuple[Dict[str, Any], ...]
    assessment_count: int
    prompt_labels_are_test_descriptions_only: bool


@dataclass(frozen=True)
class PromptStrategyRecommendationRecord:
    record_id: str
    large_object_building_strategy: str
    road_crosswalk_strategy: str
    sign_advertisement_strategy: str
    vehicle_strategy: str
    mobile_sam_role: str
    object_labels_are_not_facts: bool


@dataclass(frozen=True)
class FailureModeTaxonomyRecord:
    record_id: str
    failure_modes: Tuple[Dict[str, Any], ...]
    failure_mode_count: int


@dataclass(frozen=True)
class DetectorOCRSemanticPromptGenerationNeedRecord:
    record_id: str
    road_sign: str
    advertisement_screen: str
    vehicle: str
    building: str
    road_crosswalk: str
    mobile_sam_is_boundary_refinement_only: bool
    auto_prompt_requires_separate_governance: bool


@dataclass(frozen=True)
class MultiImageTrialRouteRecord:
    record_id: str
    route_a: str
    route_a_purpose: str
    route_b: str
    route_b_purpose: str
    route_c: str
    route_c_purpose: str
    recommended_route: str


@dataclass(frozen=True)
class RuntimeBoundaryPreservationRecord:
    record_id: str
    runtime_ready_granted: bool
    output_adapter_ready_granted: bool
    semantic_layer_ready_granted: bool
    fact_write_ready_granted: bool
    navigation_action_speech_ready_granted: bool
    candidate_masks_remain_eval_artifacts: bool
    human_review_summary_is_not_fact: bool


@dataclass(frozen=True)
class FollowupPhaseRouteRecord:
    record_id: str
    recommended_next_phase: str
    can_enter_multi_real_image_trial_request_next: bool
    can_enter_detector_assisted_prompt_planning_next: bool
    can_enter_runtime_now: bool


@dataclass
class NegativeRealImageQualityReviewPromptStrategyGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMRealImageQualityReviewPromptStrategyDecision:
    decision_ref: str
    mobile_sam_real_image_quality_review_prompt_strategy_profile_count: int
    real_image_quality_review_scope_record_count: int
    real_image_candidate_mask_quality_assessment_record_count: int
    per_prompt_quality_assessment_record_count: int
    prompt_strategy_recommendation_record_count: int
    failure_mode_taxonomy_record_count: int
    detector_ocr_semantic_prompt_generation_need_record_count: int
    multi_image_trial_route_record_count: int
    runtime_boundary_preservation_record_count: int
    followup_phase_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
