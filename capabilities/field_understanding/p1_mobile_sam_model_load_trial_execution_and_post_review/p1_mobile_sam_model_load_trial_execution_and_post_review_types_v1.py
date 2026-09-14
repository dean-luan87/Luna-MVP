# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

The FIRST real model-load trial for MobileSAM. It allows a REAL import and a REAL
checkpoint load of mobile_sam.pt, preceded by a pre-load snapshot and a sha256/size
recheck, under a 4096MB / 300s memory+timeout boundary, followed by a same-phase post-
review. It does NOT read images / construct image input / call segmentation / prediction
/ inference, does NOT start a runtime server / output adapter / semantic layer, does NOT
mutate the registry, and downloads NOTHING extra. byte_track and every other asset are
out of scope. Three honest outcomes are possible: GO (import + checkpoint load succeed,
no boundary violation), FAILED_NO_BOUNDARY_VIOLATION (import/load fails but no boundary
violation — honest failure routed to repair planning), or BLOCKED (sha256/size mismatch,
unauthorized download, image/segmentation/prediction/inference, runtime/output/semantic,
registry mutation, or test-board failure). Model-load success is NOT inference / runtime
/ output-adapter / semantic / commercial-runtime approval. Protected, non-deletable test
board records are written in `real_test` mode.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Trial-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_model_load_trial_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_trial_execution_and_post_review_v1"

MODEL_LOAD_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。MobileSAM 的首次真实 model-load trial：允许真实 import 与真实加载 mobile_sam.pt "
    "checkpoint，前置 pre-load snapshot 与 sha256/size 复校，受 4096MB/300s 内存+超时边界约束，同阶段完成 post-review。"
    "不读取图片、不构造 image input、不 segmentation/prediction/inference、不启动 runtime/output adapter/语义层、不改 "
    "registry、不额外下载。byte_track 及其余资产不在 scope。三种诚实结局：GO（import+checkpoint load 成功且无边界违规）、"
    "FAILED_NO_BOUNDARY_VIOLATION（import/load 失败但无边界违规，转 repair planning）、BLOCKED（sha256/size 不匹配/越权下载/"
    "图像/分割/预测/推理/runtime/output/语义/registry mutation/test board 失败）。model-load 成功 ≠ inference/runtime/"
    "output adapter/语义/商业 runtime 批准。测试板块 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_load_trial_only_no_image_no_segmentation_no_prediction_no_inference_no_runtime_load_success_is_not_inference"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
MODEL_LOAD_TRIAL_EXECUTION = True
POST_REVIEW_INCLUDED = True
REAL_IMPORT_ALLOWED = True
MODEL_LOAD_ALLOWED = True
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REQUEST_APPROVAL_REF = "Phase-P1-MobileSAM-Model-Load-Trial-Request-Approval-And-Readiness-v1-001"
UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
UPSTREAM_REGISTRY_OVERLAY_REF = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routes (decision-dependent).
NEXT_PHASE_GO = "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Planning-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Model-Load-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Model-Load-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Weight + code-path constants.
# --------------------------------------------------------------------------- #
MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_IMPORT_ROOT = "mobile_sam"
MOBILE_SAM_BUILD_KEY = "vit_t"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
# Code-only source-install target (from the controlled source-install retry evidence).
MOBILE_SAM_CODE_PATH_REL = "_tmp_eval_out/p1_source_retry_workspace/install_target/mobile_sam"
MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF = (
    "_tmp_eval_out/p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0/"
    "p1_controlled_source_install_execution_retry_and_post_review_review_v1.json"
)

MEMORY_LIMIT_MB = 4096
TIMEOUT_SECONDS = 300

# Out-of-scope assets (must NOT be processed).
OUT_OF_SCOPE_ASSET_IDS: Tuple[str, ...] = (
    "byte_track",
    "supervision",
    "deep_sort",
    "midas",
    "fast_sam",
    "yolov8n",
    "pyannote",
    "sam2",
    "depth_anything",
    "zoe_depth",
    "grounding_dino",
    "scene_relation_vlm",
    "open_vocab_vlm",
    "sense_voice",
    "emotion_multimodal_bridge",
    "rt_detr",
)

# --------------------------------------------------------------------------- #
# Negative guards (16: Invalid A..P).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_snapshot_but_import_load", "go_key": "pre_snapshot_present", "depends_on": "pre_snapshot_present"},
    {"guard_id": "invalid_b_no_sha256_size_recheck_but_import_load", "go_key": "sha256_size_rechecked", "depends_on": "sha256_size_rechecked"},
    {"guard_id": "invalid_c_load_proceeded_on_sha256_size_mismatch", "go_key": "no_load_on_mismatch", "depends_on": "no_load_on_mismatch"},
    {"guard_id": "invalid_d_scope_includes_byte_track_or_other_asset", "go_key": "scope_mobile_sam_only", "depends_on": "scope_mobile_sam_only"},
    {"guard_id": "invalid_e_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_f_image_read_or_image_input_constructed", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_g_segmentation_prediction_inference_called", "go_key": "no_seg_pred_inference", "depends_on": "no_seg_pred_inference"},
    {"guard_id": "invalid_h_runtime_output_adapter_semantic_layer_started", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_i_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_j_model_load_success_marked_inference_runtime_output_semantic_ready", "go_key": "success_not_downstream_ready", "depends_on": "success_not_downstream_ready"},
    {"guard_id": "invalid_k_timeout_memory_not_recorded", "go_key": "memory_timeout_recorded", "depends_on": "memory_timeout_recorded"},
    {"guard_id": "invalid_l_cleanup_rollback_record_missing", "go_key": "cleanup_rollback_recorded", "depends_on": "cleanup_rollback_recorded"},
    {"guard_id": "invalid_m_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_n_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_o_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_p_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (33 phase + 6 test board = 39).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_model_load_trial_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "byte_track_is_out_of_scope",
    "pre_model_load_snapshot_is_required",
    "sha256_recheck_is_required_before_import_load",
    "size_recheck_is_required_before_import_load",
    "real_import_is_allowed",
    "model_load_is_allowed",
    "image_input_is_not_allowed",
    "segmentation_is_not_allowed",
    "prediction_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "memory_limit_is_required",
    "timeout_is_required",
    "cleanup_rollback_record_is_required",
    "post_review_is_required",
    "model_load_success_is_not_inference_approval",
    "model_load_success_is_not_runtime_approval",
    "model_load_success_is_not_output_adapter_approval",
    "model_load_success_is_not_semantic_layer_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "honest_failure_is_not_blocked_unless_boundary_violation",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "mobile_sam_pre_model_load_snapshot_record",
    "mobile_sam_sha256_recheck_record",
    "mobile_sam_model_import_record",
    "mobile_sam_model_load_execution_record",
    "mobile_sam_memory_timeout_monitor_record",
    "mobile_sam_model_load_post_review_record",
    "mobile_sam_inference_runtime_exclusion_record",
    "mobile_sam_followup_registry_patch_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMModelLoadTrialExecutionPostReviewProfile",
    "MobileSAMPreModelLoadSnapshotRecord",
    "MobileSAMSha256RecheckRecord",
    "MobileSAMModelImportExecutionRecord",
    "MobileSAMModelLoadExecutionRecord",
    "MobileSAMMemoryTimeoutMonitorRecord",
    "MobileSAMModelLoadPostReviewAudit",
    "MobileSAMModelLoadRollbackCleanupRecord",
    "MobileSAMInferenceRuntimeExclusionRecord",
    "MobileSAMModelLoadFollowupRouteRecord",
    "NegativeMobileSAMModelLoadExecutionGuard",
    "P1MobileSAMModelLoadExecutionDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "registry_overlay_evidence_locked_and_reused": True,
    "code_only_source_install_evidence_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMModelLoadTrialExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    model_load_trial_execution: bool
    post_review_included: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    segmentation_allowed: bool
    prediction_allowed: bool
    image_input_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_request_approval_ref: str
    upstream_registry_overlay_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMPreModelLoadSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    env_path: str
    working_directory: str
    code_path_ref: str
    weight_path: str
    weight_file_exists: bool
    weight_file_size: int
    weight_sha256_before: str
    pip_freeze_before_count: int
    pip_freeze_before_digest: str
    process_id: int
    memory_limit_mb: int
    timeout_seconds: int
    upstream_request_approval_ref: str
    upstream_registry_overlay_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MobileSAMSha256RecheckRecord:
    recheck_id: str
    expected_path: str
    expected_size_bytes: int
    expected_sha256: str
    actual_size_bytes: int
    actual_sha256: str
    size_matches: bool
    sha256_matches: bool
    recheck_passed: bool


@dataclass(frozen=True)
class MobileSAMModelImportExecutionRecord:
    record_id: str
    import_target: str
    code_path_added: str
    import_attempted: bool
    import_success: bool
    import_error: str
    imported_module_file: str


@dataclass(frozen=True)
class MobileSAMModelLoadExecutionRecord:
    record_id: str
    build_key: str
    checkpoint_path: str
    checkpoint_load_attempted: bool
    model_object_created: bool
    model_type_name: str
    checkpoint_load_success: bool
    checkpoint_load_error: str
    model_object_released: bool
    model_load_trial_success: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool


@dataclass(frozen=True)
class MobileSAMMemoryTimeoutMonitorRecord:
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
class MobileSAMModelLoadPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    sha256_rechecked: bool
    sha256_matches: bool
    size_matches: bool
    real_import_performed: bool
    model_load_performed: bool
    checkpoint_load_success: bool
    no_image_input: bool
    no_segmentation: bool
    no_prediction: bool
    no_inference: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_registry_mutation: bool
    no_extra_download: bool
    memory_timeout_recorded: bool
    cleanup_recorded: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRollbackCleanupRecord:
    record_id: str
    rollback_available: bool
    rollback_not_executed_by_default: bool
    model_object_cleanup_attempted: bool
    persistent_process_left: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_registry: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool


@dataclass(frozen=True)
class MobileSAMInferenceRuntimeExclusionRecord:
    record_id: str
    no_image_input: bool
    no_segmentation: bool
    no_prediction: bool
    no_inference: bool
    no_runtime_server: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    model_load_success_not_inference_approval: bool
    model_load_success_not_runtime_approval: bool
    model_load_success_not_output_adapter_approval: bool
    model_load_success_not_semantic_layer_approval: bool
    model_load_success_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMModelLoadFollowupRouteRecord:
    route_id: str
    decision_branch: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_purpose: str
    optional_followup_phase: Optional[str]


@dataclass
class NegativeMobileSAMModelLoadExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadExecutionDecision:
    decision_ref: str
    mobile_sam_model_load_trial_execution_profile_count: int
    mobile_sam_pre_model_load_snapshot_record_count: int
    mobile_sam_sha256_recheck_record_count: int
    mobile_sam_model_import_execution_record_count: int
    mobile_sam_model_load_execution_record_count: int
    mobile_sam_memory_timeout_monitor_record_count: int
    mobile_sam_model_load_post_review_audit_count: int
    mobile_sam_model_load_rollback_cleanup_record_count: int
    mobile_sam_inference_runtime_exclusion_record_count: int
    mobile_sam_model_load_followup_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    import_success: bool
    checkpoint_load_success: bool
    model_load_trial_success: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
