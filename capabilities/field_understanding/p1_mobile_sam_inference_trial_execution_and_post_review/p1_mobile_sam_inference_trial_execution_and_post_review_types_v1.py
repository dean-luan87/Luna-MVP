# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

Single local test image candidate-only inference trial with pre-snapshot, sha256/registry
recheck, real import/load, one controlled inference call, candidate output, post-review.
Does NOT runtime/output adapter/semantic/fact/navigation, registry mutation, or extra download.
"""

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

PHASE_ID = "Phase-P1-MobileSAM-Inference-Trial-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_inference_trial_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_inference_trial_execution_and_post_review_v1"

INFERENCE_EXECUTION_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。单次 local test image candidate-only inference trial："
    "pre-snapshot、sha256/registry 复核、真实 import/load、读取 manifest 单张图、一次受控 inference、"
    "candidate 输出、post-review。不 runtime/output adapter/语义层/fact/navigation、不改 registry、不额外下载。"
    "inference 成功 ≠ runtime/output/semantic/fact 批准。测试板块 real_test，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "single_local_test_image_candidate_inference_only_success_is_not_runtime"
)

REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
INFERENCE_TRIAL_EXECUTION = True
SINGLE_LOCAL_TEST_IMAGE_ONLY = True
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
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXTERNAL_IMAGE_DOWNLOAD_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
PERSONAL_IMAGE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_INFERENCE_APPROVAL_REF = (
    "Phase-P1-MobileSAM-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
UPSTREAM_INFERENCE_APPROVAL_EXPECTED_GO = (
    "P1_MOBILE_SAM_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
)
UPSTREAM_REGISTRY_OVERLAY_REF = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_GO = "Phase-P1-MobileSAM-Inference-Trial-Registry-Patch-And-Runtime-Boundary-Planning-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Inference-Trial-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Inference-Trial-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_IMPORT_ROOT = "mobile_sam"
TIMM_IMPORT_ROOT = "timm"
MOBILE_SAM_BUILD_KEY = "vit_t"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = (
    "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
)
MOBILE_SAM_CODE_PATH_REL = "_tmp_eval_out/p1_source_retry_workspace/install_target/mobile_sam"
TIMM_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"
EXPECTED_READINESS_LEVEL = "model_load_verified"
MEMORY_LIMIT_MB = 4096
TIMEOUT_SECONDS = 300
SYNTHETIC_IMAGE_WIDTH = 128
SYNTHETIC_IMAGE_HEIGHT = 128
TEST_IMAGE_ID = "mobile_sam_synthetic_tiny_test_image_v1"

OUT_OF_SCOPE_ASSET_IDS: Tuple[str, ...] = (
    "byte_track", "supervision", "deep_sort", "midas", "fast_sam", "yolov8n",
    "pyannote", "sam2", "depth_anything", "zoe_depth", "grounding_dino",
    "scene_relation_vlm", "open_vocab_vlm", "sense_voice", "emotion_multimodal_bridge",
    "rt_detr",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go_but_inference", "go_key": "upstream_approval_verified", "depends_on": "upstream_approval_verified"},
    {"guard_id": "invalid_b_registry_not_model_load_verified", "go_key": "registry_model_load_verified", "depends_on": "registry_model_load_verified"},
    {"guard_id": "invalid_c_sha256_not_rechecked", "go_key": "sha256_rechecked", "depends_on": "sha256_rechecked"},
    {"guard_id": "invalid_d_manifest_missing_but_image_read", "go_key": "manifest_before_image", "depends_on": "manifest_before_image"},
    {"guard_id": "invalid_e_non_manifest_image", "go_key": "only_manifest_image", "depends_on": "only_manifest_image"},
    {"guard_id": "invalid_f_live_camera", "go_key": "no_live_camera", "depends_on": "no_live_camera"},
    {"guard_id": "invalid_g_personal_image", "go_key": "no_personal_image", "depends_on": "no_personal_image"},
    {"guard_id": "invalid_h_external_url_image", "go_key": "no_external_url", "depends_on": "no_external_url"},
    {"guard_id": "invalid_i_uncontrolled_dataset", "go_key": "no_uncontrolled_dataset", "depends_on": "no_uncontrolled_dataset"},
    {"guard_id": "invalid_j_candidate_not_marked", "go_key": "candidate_output_only", "depends_on": "candidate_output_only"},
    {"guard_id": "invalid_k_candidate_entered_downstream", "go_key": "no_downstream_output", "depends_on": "no_downstream_output"},
    {"guard_id": "invalid_l_navigation_action_speech", "go_key": "no_navigation_speech", "depends_on": "no_navigation_speech"},
    {"guard_id": "invalid_m_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_n_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_o_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_p_success_marked_downstream_ready", "go_key": "success_not_downstream_ready", "depends_on": "success_not_downstream_ready"},
    {"guard_id": "invalid_q_memory_timeout_not_recorded", "go_key": "memory_timeout_recorded", "depends_on": "memory_timeout_recorded"},
    {"guard_id": "invalid_r_cleanup_missing", "go_key": "cleanup_recorded", "depends_on": "cleanup_recorded"},
    {"guard_id": "invalid_s_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_t_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_u_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_v_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_inference_trial_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "upstream_inference_request_approval_readiness_must_be_go",
    "registry_must_be_model_load_verified",
    "sha256_recheck_is_required_before_inference",
    "size_recheck_is_required_before_inference",
    "test_image_manifest_is_required",
    "only_one_local_test_image_may_be_used",
    "synthetic_tiny_local_scoped_test_image_only",
    "live_camera_is_not_allowed",
    "personal_image_is_not_allowed",
    "external_url_image_is_not_allowed",
    "uncontrolled_dataset_is_not_allowed",
    "batch_dataset_run_is_not_allowed",
    "inference_is_allowed_only_as_controlled_trial",
    "candidate_output_only",
    "candidate_output_must_not_enter_fact_layer",
    "candidate_output_must_not_enter_runtime",
    "candidate_output_must_not_enter_output_adapter",
    "candidate_output_must_not_enter_semantic_layer",
    "candidate_output_must_not_trigger_navigation_action_speech",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "inference_success_is_not_runtime_approval",
    "inference_success_is_not_output_adapter_approval",
    "inference_success_is_not_semantic_layer_approval",
    "inference_success_is_not_fact_write_approval",
    "inference_success_is_not_navigation_action_speech_approval",
    "commercial_runtime_is_not_approved",
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
    "mobile_sam_pre_inference_snapshot_record",
    "mobile_sam_test_image_manifest_record",
    "mobile_sam_inference_sha256_registry_recheck_record",
    "mobile_sam_inference_model_load_record",
    "mobile_sam_single_inference_execution_record",
    "mobile_sam_candidate_output_record",
    "mobile_sam_inference_memory_timeout_monitor_record",
    "mobile_sam_inference_post_review_record",
    "mobile_sam_runtime_semantic_fact_exclusion_record",
    "mobile_sam_followup_inference_registry_patch_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_INFERENCE_TRIAL_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_INFERENCE_TRIAL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_INFERENCE_TRIAL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "inference_approval_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMInferenceTrialExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    inference_trial_execution: bool
    single_local_test_image_only: bool
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
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_inference_approval_ref: str
    upstream_registry_overlay_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMPreInferenceSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    env_path: str
    working_directory: str
    mobile_sam_code_path_ref: str
    timm_install_target_path_ref: str
    weight_path: str
    weight_file_exists: bool
    weight_file_size: int
    weight_sha256_before: str
    registry_overlay_path: str
    registry_mobile_sam_readiness_level: str
    pip_freeze_before_count: int
    pip_freeze_before_digest: str
    process_id: int
    memory_limit_mb: int
    timeout_seconds: int
    upstream_inference_request_approval_ref: str
    upstream_model_load_registry_patch_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MobileSAMLocalTestImageManifestRecord:
    manifest_id: str
    test_image_id: str
    local_path: str
    sha256: str
    width: int
    height: int
    file_size_bytes: int
    source_type: str
    personal_data_absent: bool
    live_camera_frame: bool
    external_url_source: bool
    dataset_source: bool
    navigation_runtime_frame: bool
    fact_layer_source: bool
    semantic_layer_source: bool
    allowed_for_single_inference_trial: bool
    must_not_enter_fact_layer: bool
    must_not_enter_navigation_runtime: bool
    manifest_valid: bool


@dataclass(frozen=True)
class MobileSAMInferenceSha256RegistryRecheckRecord:
    recheck_id: str
    registry_readiness_level: str
    model_load_verified: bool
    checkpoint_load_verified: bool
    dependency_gap_resolved: bool
    dependency_repair_dependency: str
    dependency_repair_dependency_version: str
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool
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
class MobileSAMInferenceModelLoadRecord:
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
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool


@dataclass(frozen=True)
class MobileSAMSingleInferenceExecutionRecord:
    record_id: str
    command_purpose: str
    manifest_path_used: str
    test_image_id: str
    inference_attempted: bool
    inference_success: bool
    inference_error: str
    output_type: str
    mask_count: int
    result_shape_summary: str
    elapsed_seconds: float
    peak_memory_mb: float


@dataclass(frozen=True)
class MobileSAMCandidateOutputRecord:
    candidate_id: str
    asset_id: str
    test_image_id: str
    inference_attempted: bool
    inference_success: bool
    output_type: str
    mask_count: int
    result_shape_summary: str
    elapsed_seconds: float
    peak_memory_mb: float
    candidate_only: bool
    not_fact: bool
    not_runtime_output: bool
    not_output_adapter_output: bool
    not_semantic_output: bool
    not_user_visible_runtime_output: bool
    post_review_required: bool
    candidate_output_written: bool


@dataclass(frozen=True)
class MobileSAMInferenceMemoryTimeoutMonitorRecord:
    monitor_id: str
    memory_limit_mb: int
    timeout_seconds: int
    started_at: str
    ended_at: str
    elapsed_seconds: float
    peak_memory_mb: float
    timeout_occurred: bool
    oom_occurred: bool
    candidate_output_cleanup_attempted_if_failed: bool
    model_object_cleanup_attempted: bool
    persistent_process_left: bool


@dataclass(frozen=True)
class MobileSAMInferencePostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    registry_model_load_verified_rechecked: bool
    sha256_rechecked: bool
    sha256_matches: bool
    local_test_image_manifest_exists: bool
    local_test_image_manifest_valid: bool
    image_source_allowed: bool
    real_import_performed: bool
    model_load_performed: bool
    inference_attempted: bool
    inference_success: bool
    candidate_output_written: bool
    candidate_output_only: bool
    no_live_camera: bool
    no_personal_image: bool
    no_external_url_image: bool
    no_uncontrolled_dataset: bool
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
class MobileSAMInferenceRollbackCleanupRecord:
    record_id: str
    pre_inference_snapshot_required: bool
    rollback_available: bool
    candidate_output_cleanup_attempted: bool
    model_object_cleanup_attempted: bool
    rollback_preserves_registry: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    no_fact_write_on_failure: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class MobileSAMRuntimeSemanticFactExclusionRecord:
    record_id: str
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    fact_write_ready: bool
    navigation_action_speech_ready: bool
    commercial_runtime_ready: bool
    inference_trial_success_not_runtime_approval: bool
    inference_trial_success_not_output_adapter_approval: bool
    inference_trial_success_not_semantic_layer_approval: bool
    inference_trial_success_not_fact_write_approval: bool
    inference_trial_success_not_navigation_action_speech_approval: bool
    inference_trial_success_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMFollowupInferenceRegistryPatchRoute:
    route_id: str
    decision_branch: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_purpose: str


@dataclass
class NegativeMobileSAMInferenceTrialExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMInferenceTrialExecutionDecision:
    decision_ref: str
    mobile_sam_inference_trial_execution_profile_count: int
    mobile_sam_pre_inference_snapshot_record_count: int
    mobile_sam_test_image_manifest_record_count: int
    mobile_sam_inference_sha256_registry_recheck_record_count: int
    mobile_sam_inference_model_load_record_count: int
    mobile_sam_single_inference_execution_record_count: int
    mobile_sam_candidate_output_record_count: int
    mobile_sam_inference_memory_timeout_monitor_record_count: int
    mobile_sam_inference_post_review_audit_count: int
    mobile_sam_inference_rollback_cleanup_record_count: int
    mobile_sam_runtime_semantic_fact_exclusion_record_count: int
    mobile_sam_followup_inference_registry_patch_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    inference_attempted: bool
    inference_success: bool
    candidate_output_written: bool
    candidate_output_only: bool
    single_local_test_image_inference_verified: bool
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
