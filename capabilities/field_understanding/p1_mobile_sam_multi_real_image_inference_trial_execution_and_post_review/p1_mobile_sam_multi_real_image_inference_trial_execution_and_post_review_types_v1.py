# -*- coding: utf-8 -*-
"""P1 MobileSAM Multi Real Image Inference Trial Execution And Post Review — types v1."""

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

PHASE_ID = "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_multi_real_image_inference_trial_execution_and_post_review_v1"

EXECUTION_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。对已登记 4 张 scoped local test assets 执行 "
    "5 类 prompt × 4 图 = 20 次 candidate-only MobileSAM segmentation，含 pre-snapshot、"
    "registry/weight recheck、multi-image manifest、per-image/aggregate quality summary、post-review。"
    "不 runtime/output adapter/语义层/fact/navigation、不改 registry。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "multi_real_image_candidate_inference_only_success_is_not_runtime"
)

REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION = True
FOUR_SCOPED_LOCAL_IMAGES_ONLY = True
PLANNED_PROMPT_TARGETS_ONLY = True
EXPECTED_IMAGE_COUNT = 4
EXPECTED_PROMPT_CATEGORY_COUNT = 5
EXPECTED_PROMPT_TRIAL_COUNT = 20
CANDIDATE_OUTPUT_ONLY = True
POST_REVIEW_INCLUDED = True
REAL_IMPORT_ALLOWED = True
MODEL_LOAD_ALLOWED = True
CHECKPOINT_LOAD_ALLOWED = True
IMAGE_INPUT_ALLOWED = True
LOCAL_TEST_IMAGE_ALLOWED = True
REAL_INFERENCE_ALLOWED = True
SEGMENTATION_ALLOWED = True
PREDICTION_ALLOWED = True
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
UNCONTROLLED_DATASET_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_REQUEST_APPROVAL_REF = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO = (
    "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
)
UPSTREAM_QUALITY_REVIEW_REF = (
    "Phase-P1-MobileSAM-Real-Image-Quality-Review-And-Prompt-Strategy-Planning-v1-001"
)
UPSTREAM_RUNTIME_BOUNDARY_REF = (
    "Phase-P1-MobileSAM-Runtime-Boundary-Standardization-Planning-v1-001"
)
UPSTREAM_REGISTRY_OVERLAY_REF = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_GO = "Phase-P1-MobileSAM-Multi-Real-Image-Quality-Review-And-Automated-Test-Planning-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_IMPORT_ROOT = "mobile_sam"
TIMM_IMPORT_ROOT = "timm"
MOBILE_SAM_BUILD_KEY = "vit_t"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
MOBILE_SAM_CODE_PATH_REL = "_tmp_eval_out/p1_source_retry_workspace/install_target/mobile_sam"
TIMM_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"
EXPECTED_READINESS_LEVEL = "inference_trial_verified"
MEMORY_LIMIT_MB = 4096
TIMEOUT_SECONDS = 600

SOURCE_IMAGE_ROOT_REL = "capabilities/test_assets/p1/mobile_sam/multi"
SOURCE_TYPE = "user_supplied_scoped_local_test_asset"

MULTI_IMAGE_ASSET_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_001",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_001.png",
        "scene_type": "daytime_tree_lined_sidewalk_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_002",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_002.png",
        "scene_type": "daytime_hazy_urban_street_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_003",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_003.png",
        "scene_type": "daytime_street_vendor_stalls_scene",
    },
    {
        "test_asset_id": "mobile_sam_multi_real_image_street_scene_v1_004",
        "canonical_filename": "mobile_sam_multi_real_image_street_scene_v1_004.png",
        "scene_type": "daytime_sidewalk_scooters_scene",
    },
)

PROMPT_CATEGORY_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "prompt_id": "building_or_large_structure",
        "prompt_category": "building_or_large_structure",
        "prompt_target_label": "building_or_large_structure",
        "prompt_type_preferred": "box",
        "normalized_box_default": [0.03, 0.05, 0.38, 0.78],
        "strategy_note": "box_prompt_preferred; stable_large_object_mask",
    },
    {
        "prompt_id": "road_or_crosswalk_or_large_plane",
        "prompt_category": "road_or_crosswalk_or_large_plane",
        "prompt_target_label": "road_or_crosswalk_or_large_plane",
        "prompt_type_preferred": "box",
        "normalized_box_default": [0.35, 0.68, 0.98, 0.98],
        "strategy_note": "box_plus_negative_or_multi_point_recommended; large_plane_candidate_mask",
    },
    {
        "prompt_id": "sign_or_advertisement_screen",
        "prompt_category": "sign_or_advertisement_screen",
        "prompt_target_label": "sign_or_advertisement_screen",
        "prompt_type_preferred": "box",
        "normalized_box_default": [0.55, 0.30, 0.90, 0.62],
        "strategy_note": "manual_box_point_trial; future_detector_or_ocr_assisted_box",
    },
    {
        "prompt_id": "vehicle_or_small_dynamic_object",
        "prompt_category": "vehicle_or_small_dynamic_object",
        "prompt_target_label": "vehicle_or_small_dynamic_object",
        "prompt_type_preferred": "box",
        "normalized_box_default": [0.30, 0.62, 0.70, 0.85],
        "strategy_note": "manual_box_point_trial; future_detector_or_tracker_assisted_box",
    },
    {
        "prompt_id": "street_facility_or_pole_or_edge_object",
        "prompt_category": "street_facility_or_pole_or_edge_object",
        "prompt_target_label": "street_facility_or_pole_or_edge_object",
        "prompt_type_preferred": "box",
        "normalized_box_default": [0.45, 0.20, 0.65, 0.78],
        "strategy_note": "box_or_point_trial; thin_object_fragmentation_risk",
    },
)

BROAD_READINESS_MUST_BE_FALSE: Tuple[str, ...] = (
    "inference_ready", "runtime_ready", "output_adapter_ready", "semantic_layer_ready",
    "fact_write_ready", "navigation_action_speech_ready", "commercial_runtime_approved",
)
REQUIRED_REGISTRY_TRUE_FLAGS: Tuple[str, ...] = (
    "model_load_verified", "checkpoint_load_verified", "inference_trial_verified",
    "candidate_output_verified", "single_local_test_image_inference_verified",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "upstream_approval_verified", "depends_on": "upstream_approval_verified"},
    {"guard_id": "invalid_b_registry_not_inference_trial_verified", "go_key": "registry_inference_trial_verified", "depends_on": "registry_inference_trial_verified"},
    {"guard_id": "invalid_c_weight_not_rechecked", "go_key": "weight_rechecked", "depends_on": "weight_rechecked"},
    {"guard_id": "invalid_d_manifest_missing_or_bad_source", "go_key": "manifest_valid", "depends_on": "manifest_valid"},
    {"guard_id": "invalid_e_non_manifest_image", "go_key": "only_manifest_images", "depends_on": "only_manifest_images"},
    {"guard_id": "invalid_f_live_camera", "go_key": "no_live_camera", "depends_on": "no_live_camera"},
    {"guard_id": "invalid_g_external_url", "go_key": "no_external_url", "depends_on": "no_external_url"},
    {"guard_id": "invalid_h_uncontrolled_dataset", "go_key": "no_uncontrolled_dataset", "depends_on": "no_uncontrolled_dataset"},
    {"guard_id": "invalid_i_prompt_label_as_fact", "go_key": "prompt_labels_not_facts", "depends_on": "prompt_labels_not_facts"},
    {"guard_id": "invalid_j_candidate_entered_downstream", "go_key": "candidate_output_only", "depends_on": "candidate_output_only"},
    {"guard_id": "invalid_k_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_l_fact_navigation_speech", "go_key": "no_fact_navigation_speech", "depends_on": "no_fact_navigation_speech"},
    {"guard_id": "invalid_m_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_n_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_o_success_marked_downstream_ready", "go_key": "success_not_downstream_ready", "depends_on": "success_not_downstream_ready"},
    {"guard_id": "invalid_p_aggregate_quality_as_fact", "go_key": "aggregate_quality_not_fact", "depends_on": "aggregate_quality_not_fact"},
    {"guard_id": "invalid_q_memory_timeout_not_recorded", "go_key": "memory_timeout_recorded", "depends_on": "memory_timeout_recorded"},
    {"guard_id": "invalid_r_cleanup_missing", "go_key": "cleanup_recorded", "depends_on": "cleanup_recorded"},
    {"guard_id": "invalid_s_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_t_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_u_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_v_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_multi_real_image_inference_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "source_images_must_be_manifest_scoped_local_test_assets",
    "only_the_4_registered_scoped_local_images_may_be_used",
    "live_camera_is_not_allowed",
    "external_url_image_is_not_allowed",
    "uncontrolled_dataset_is_not_allowed",
    "dataset_batch_is_not_allowed",
    "registry_readiness_must_be_rechecked",
    "weight_sha256_and_size_must_be_rechecked",
    "prompt_labels_are_test_descriptions_only",
    "prompt_labels_are_not_semantic_facts",
    "candidate_masks_are_not_facts",
    "candidate_masks_must_not_enter_runtime",
    "candidate_masks_must_not_enter_output_adapter",
    "candidate_masks_must_not_enter_semantic_layer",
    "candidate_masks_must_not_trigger_navigation_action_speech",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "multi_image_inference_success_is_not_runtime_approval",
    "multi_image_inference_success_is_not_output_adapter_approval",
    "multi_image_inference_success_is_not_semantic_fact_navigation_approval",
    "aggregate_quality_summary_is_not_fact",
    "memory_limit_is_required",
    "timeout_is_required",
    "cleanup_rollback_record_is_required",
    "post_review_is_required",
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
    "multi_real_image_pre_inference_snapshot_record",
    "multi_real_image_manifest_record",
    "multi_real_image_registry_weight_recheck_record",
    "multi_real_image_model_load_record",
    "multi_real_image_prompt_execution_record",
    "multi_real_image_candidate_masks_record",
    "multi_real_image_per_image_quality_summary_record",
    "multi_real_image_aggregate_quality_summary_record",
    "multi_real_image_memory_timeout_monitor_record",
    "multi_real_image_post_review_record",
    "multi_real_image_runtime_semantic_fact_exclusion_record",
    "multi_real_image_followup_review_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MULTI_REAL_IMAGE_INFERENCE_TRIAL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "multi_real_image_request_approval_reused": True,
    "runtime_boundary_standardization_reused": True,
    "real_image_quality_review_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMMultiRealImageInferenceExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    multi_real_image_inference_trial_execution: bool
    four_scoped_local_images_only: bool
    planned_prompt_targets_only: bool
    expected_image_count: int
    expected_prompt_category_count: int
    expected_prompt_trial_count: int
    candidate_output_only: bool
    post_review_included: bool
    real_import_allowed: bool
    model_load_allowed: bool
    checkpoint_load_allowed: bool
    image_input_allowed: bool
    local_test_image_allowed: bool
    real_inference_allowed: bool
    segmentation_allowed: bool
    prediction_allowed: bool
    runtime_execution_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_request_approval_ref: str
    upstream_quality_review_ref: str
    upstream_runtime_boundary_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MultiRealImagePreInferenceSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    env_path: str
    working_directory: str
    mobile_sam_code_path_ref: str
    timm_install_target_path_ref: str
    weight_path: str
    weight_file_exists: bool
    registry_overlay_path: str
    source_image_root: str
    discovered_image_paths: Tuple[str, ...]
    process_id: int
    memory_limit_mb: int
    timeout_seconds: int
    upstream_request_approval_ref: str
    upstream_quality_review_ref: str
    upstream_runtime_boundary_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MultiRealImageManifestRecord:
    manifest_id: str
    image_count: int
    source_image_root: str
    images: Tuple[Dict[str, Any], ...]
    manifest_valid: bool


@dataclass(frozen=True)
class MultiRealImageRegistryWeightRecheckRecord:
    recheck_id: str
    registry_readiness_level: str
    inference_trial_verified: bool
    runtime_ready: bool
    registry_recheck_passed: bool
    expected_path: str
    expected_size_bytes: int
    expected_sha256: str
    actual_size_bytes: int
    actual_sha256: str
    size_matches: bool
    sha256_matches: bool
    mobile_sam_find_spec: bool
    timm_find_spec: bool
    recheck_passed: bool


@dataclass(frozen=True)
class MultiRealImageModelLoadRecord:
    record_id: str
    import_attempted: bool
    import_success: bool
    import_error: str
    checkpoint_load_attempted: bool
    model_object_created: bool
    model_type_name: str
    checkpoint_load_success: bool
    checkpoint_load_error: str
    model_object_released: bool


@dataclass(frozen=True)
class MultiRealImagePromptExecutionRecord:
    record_id: str
    expected_prompt_trial_count: int
    prompt_attempt_count: int
    prompt_success_count: int
    prompt_failure_count: int
    skipped_prompt_count: int
    inference_attempted: bool
    prompt_results: Tuple[Dict[str, Any], ...]


@dataclass(frozen=True)
class MultiRealImageCandidateMasksRecord:
    record_id: str
    candidate_masks_written: bool
    mask_output_dir: str
    prompt_mask_summaries: Tuple[Dict[str, Any], ...]
    candidate_only: bool
    not_fact: bool


@dataclass(frozen=True)
class MultiRealImagePerImageQualitySummaryRecord:
    record_id: str
    per_image_summaries: Tuple[Dict[str, Any], ...]
    human_review_required: bool
    suitable_for_runtime_admission: bool
    suitable_for_quality_observation: bool
    not_semantic_fact: bool


@dataclass(frozen=True)
class MultiRealImageAggregateQualitySummaryRecord:
    record_id: str
    image_count: int
    expected_prompt_trial_count: int
    prompt_attempt_count: int
    prompt_success_count: int
    prompt_failure_count: int
    skipped_prompt_count: int
    overall_success_rate: float
    per_category_success_rate: Dict[str, float]
    per_category_average_score: Dict[str, float]
    recurring_failure_modes: Tuple[str, ...]
    stable_categories: Tuple[str, ...]
    unstable_categories: Tuple[str, ...]
    prompt_strategy_implications: Tuple[str, ...]
    detector_ocr_tracker_prompt_need_update: bool
    human_review_required: bool
    suitable_for_runtime_admission: bool
    suitable_for_quality_observation: bool
    not_semantic_fact: bool


@dataclass(frozen=True)
class MultiRealImageMemoryTimeoutMonitorRecord:
    monitor_id: str
    memory_limit_mb: int
    timeout_seconds: int
    started_at: str
    ended_at: str
    elapsed_seconds: float
    peak_memory_mb: float
    timeout_occurred: bool
    oom_occurred: bool
    model_object_cleanup_attempted: bool
    persistent_process_left: bool


@dataclass(frozen=True)
class MultiRealImagePostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    registry_readiness_rechecked: bool
    weight_sha256_rechecked: bool
    multi_image_manifest_written: bool
    image_count: int
    image_sources_allowed: bool
    no_live_camera: bool
    no_external_url: bool
    no_uncontrolled_dataset_batch: bool
    real_import_performed: bool
    model_load_performed: bool
    expected_prompt_trial_count: int
    prompt_attempt_count: int
    inference_attempted: bool
    prompt_success_count: int
    candidate_masks_written: bool
    per_image_quality_summary_written: bool
    aggregate_quality_summary_written: bool
    candidate_output_only: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_fact_write: bool
    no_navigation_action_speech: bool
    no_registry_mutation: bool
    no_extra_download: bool
    memory_timeout_recorded: bool
    cleanup_recorded: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class MultiRealImageRollbackCleanupRecord:
    record_id: str
    pre_inference_snapshot_required: bool
    rollback_available: bool
    rollback_preserves_registry: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    rollback_preserves_source_uploaded_images: bool
    candidate_output_cleanup_attempted_if_failed: bool
    model_object_cleanup_attempted: bool
    no_fact_write_on_failure: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class MultiRealImageRuntimeSemanticFactExclusionRecord:
    record_id: str
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    fact_write_ready: bool
    navigation_action_speech_ready: bool
    commercial_runtime_ready: bool
    multi_real_image_trial_success_not_runtime_approval: bool
    multi_real_image_trial_success_not_output_adapter_approval: bool
    multi_real_image_trial_success_not_semantic_layer_approval: bool
    multi_real_image_trial_success_not_fact_write_approval: bool
    multi_real_image_trial_success_not_navigation_action_speech_approval: bool
    multi_real_image_trial_success_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MultiRealImageFollowupReviewRoute:
    route_id: str
    decision_branch: str
    recommended_next_phase: str
    next_phase_scope: str


@dataclass
class NegativeMultiRealImageInferenceExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMMultiRealImageInferenceExecutionDecision:
    decision_ref: str
    mobile_sam_multi_real_image_inference_execution_profile_count: int
    multi_real_image_pre_inference_snapshot_record_count: int
    multi_real_image_manifest_record_count: int
    multi_real_image_registry_weight_recheck_record_count: int
    multi_real_image_model_load_record_count: int
    multi_real_image_prompt_execution_record_count: int
    multi_real_image_candidate_masks_record_count: int
    multi_real_image_per_image_quality_summary_record_count: int
    multi_real_image_aggregate_quality_summary_record_count: int
    multi_real_image_memory_timeout_monitor_record_count: int
    multi_real_image_post_review_audit_count: int
    multi_real_image_rollback_cleanup_record_count: int
    multi_real_image_runtime_semantic_fact_exclusion_record_count: int
    multi_real_image_followup_review_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    image_count: int
    expected_prompt_trial_count: int
    prompt_attempt_count: int
    prompt_success_count: int
    inference_attempted: bool
    candidate_masks_written: bool
    multi_real_image_candidate_masks_verified: bool
    real_scene_multi_image_quality_observation_available: bool
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
