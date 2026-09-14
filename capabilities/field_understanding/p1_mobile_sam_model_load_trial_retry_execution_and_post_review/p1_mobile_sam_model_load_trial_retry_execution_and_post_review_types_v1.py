# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Retry Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

Model-load RETRY after timm no-deps controlled install GO. Allows sha256/size recheck,
code_and_weight_ready reverification, timm find_spec recheck, torch/torchvision reuse
boundary observation, REAL import, REAL model load retry, checkpoint load retry, and
same-phase post-review. Does NOT read images / construct image input / call segmentation
/ prediction / inference, does NOT start runtime / output adapter / semantic layer,
does NOT mutate registry, and downloads NOTHING extra. Three honest outcomes: GO,
FAILED_NO_BOUNDARY_VIOLATION, or BLOCKED. Model-load retry success is NOT inference /
runtime / output-adapter / semantic / commercial-runtime approval.
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

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_model_load_trial_retry_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1"

MODEL_LOAD_RETRY_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。timm no-deps 安装 GO 后的 MobileSAM model-load retry："
    "允许 sha256/size 复校、code_and_weight_ready 复核、timm find_spec 复核、torch/torchvision "
    "复用边界观察、真实 import、真实 model load retry、checkpoint load retry，同阶段 post-review。"
    "不读取图片、不构造 image input、不 segmentation/prediction/inference、不启动 runtime/output "
    "adapter/语义层、不改 registry、不额外下载。三种诚实结局：GO、FAILED_NO_BOUNDARY_VIOLATION、"
    "BLOCKED。model-load retry 成功 ≠ inference/runtime/output adapter/语义/商业 runtime 批准。"
    "测试板块 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_load_retry_after_timm_nodeps_no_image_no_segmentation_no_prediction_no_inference_"
    "load_success_is_not_inference"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
MODEL_LOAD_RETRY_EXECUTION = True
POST_REVIEW_INCLUDED = True
REAL_IMPORT_ALLOWED = True
MODEL_LOAD_ALLOWED = True
CHECKPOINT_LOAD_ALLOWED = True
TORCH_TORCHVISION_REUSE_OBSERVATION_ALLOWED = True
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

UPSTREAM_NODEPS_INSTALL_REF = (
    "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Execution-And-Post-Review-v1-001"
)
UPSTREAM_NODEPS_INSTALL_EXPECTED_GO = (
    "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_EXECUTION_GO"
)
UPSTREAM_MODEL_LOAD_RETRY_GATE_REF = UPSTREAM_NODEPS_INSTALL_REF
UPSTREAM_REGISTRY_OVERLAY_REF = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_GO = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Planning-v1-001"
)
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Model-Load-Retry-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Model-Load-Retry-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Weight + code-path + timm constants.
# --------------------------------------------------------------------------- #
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
TIMM_INSTALLED_VERSION_EXPECTED = "1.0.27"
EXPECTED_TORCH_VERSION = "2.8.0"

MEMORY_LIMIT_MB = 4096
TIMEOUT_SECONDS = 300

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
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_snapshot_but_import_load", "go_key": "pre_snapshot_present", "depends_on": "pre_snapshot_present"},
    {"guard_id": "invalid_b_code_and_weight_ready_not_reverified", "go_key": "upstream_readiness_verified", "depends_on": "upstream_readiness_verified"},
    {"guard_id": "invalid_c_timm_nodeps_go_not_reverified", "go_key": "timm_nodeps_go_reverified", "depends_on": "timm_nodeps_go_reverified"},
    {"guard_id": "invalid_d_no_sha256_size_recheck_but_import_load", "go_key": "sha256_size_rechecked", "depends_on": "sha256_size_rechecked"},
    {"guard_id": "invalid_e_load_proceeded_on_sha256_size_mismatch", "go_key": "no_load_on_mismatch", "depends_on": "no_load_on_mismatch"},
    {"guard_id": "invalid_f_scope_includes_byte_track_or_other_asset", "go_key": "scope_mobile_sam_only", "depends_on": "scope_mobile_sam_only"},
    {"guard_id": "invalid_g_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_h_image_read_or_image_input_constructed", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_i_segmentation_prediction_inference_called", "go_key": "no_seg_pred_inference", "depends_on": "no_seg_pred_inference"},
    {"guard_id": "invalid_j_runtime_output_adapter_semantic_layer_started", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_k_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_l_model_load_retry_success_marked_downstream_ready", "go_key": "success_not_downstream_ready", "depends_on": "success_not_downstream_ready"},
    {"guard_id": "invalid_m_timeout_memory_not_recorded", "go_key": "memory_timeout_recorded", "depends_on": "memory_timeout_recorded"},
    {"guard_id": "invalid_n_cleanup_rollback_record_missing", "go_key": "cleanup_rollback_recorded", "depends_on": "cleanup_rollback_recorded"},
    {"guard_id": "invalid_o_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (36 phase + 6 test board = 42).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_model_load_retry_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "byte_track_is_out_of_scope",
    "mobile_sam_code_and_weight_ready_must_be_reverified",
    "timm_no_deps_install_go_must_be_reverified",
    "sha256_recheck_is_required_before_import_load",
    "size_recheck_is_required_before_import_load",
    "real_import_is_allowed",
    "model_load_is_allowed",
    "checkpoint_load_is_allowed",
    "image_input_is_not_allowed",
    "segmentation_is_not_allowed",
    "prediction_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "torch_torchvision_reinstall_is_not_allowed",
    "memory_limit_is_required",
    "timeout_is_required",
    "cleanup_rollback_record_is_required",
    "post_review_is_required",
    "model_load_retry_success_is_not_inference_approval",
    "model_load_retry_success_is_not_runtime_approval",
    "model_load_retry_success_is_not_output_adapter_approval",
    "model_load_retry_success_is_not_semantic_layer_approval",
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

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "mobile_sam_retry_pre_model_load_snapshot_record",
    "mobile_sam_retry_sha256_recheck_record",
    "mobile_sam_retry_dependency_availability_record",
    "mobile_sam_retry_torch_torchvision_boundary_record",
    "mobile_sam_retry_import_record",
    "mobile_sam_retry_model_load_execution_record",
    "mobile_sam_retry_memory_timeout_monitor_record",
    "mobile_sam_retry_post_review_record",
    "mobile_sam_retry_inference_runtime_exclusion_record",
    "mobile_sam_retry_followup_registry_patch_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMModelLoadRetryExecutionPostReviewProfile",
    "MobileSAMRetryPreModelLoadSnapshotRecord",
    "MobileSAMRetrySha256RecheckRecord",
    "MobileSAMRetryCodeAndWeightRegistryAudit",
    "MobileSAMRetryDependencyAvailabilityRecord",
    "MobileSAMRetryTorchTorchvisionBoundaryRecord",
    "MobileSAMRetryImportExecutionRecord",
    "MobileSAMRetryModelLoadExecutionRecord",
    "MobileSAMRetryMemoryTimeoutMonitorRecord",
    "MobileSAMRetryPostReviewAudit",
    "MobileSAMRetryRollbackCleanupRecord",
    "MobileSAMRetryInferenceRuntimeExclusionRecord",
    "MobileSAMRetryFollowupRegistryPatchRoute",
    "NegativeMobileSAMModelLoadRetryExecutionGuard",
    "P1MobileSAMModelLoadRetryExecutionDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "registry_overlay_evidence_locked_and_reused": True,
    "timm_nodeps_install_evidence_reused": True,
    "code_only_source_install_evidence_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMModelLoadRetryExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    model_load_retry_execution: bool
    post_review_included: bool
    real_import_allowed: bool
    model_load_allowed: bool
    checkpoint_load_allowed: bool
    torch_torchvision_reuse_observation_allowed: bool
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
    upstream_nodeps_install_ref: str
    upstream_registry_overlay_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMRetryPreModelLoadSnapshotRecord:
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
    pip_freeze_before_count: int
    pip_freeze_before_digest: str
    process_id: int
    memory_limit_mb: int
    timeout_seconds: int
    upstream_timm_nodeps_install_ref: str
    upstream_model_load_retry_gate_ref: str
    upstream_registry_overlay_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MobileSAMRetrySha256RecheckRecord:
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
class MobileSAMRetryCodeAndWeightRegistryAudit:
    audit_id: str
    registry_overlay_ref: str
    readiness_level: str
    code_only_install_verified: bool
    find_spec_verified: bool
    weight_downloaded: bool
    weight_integrity_verified: bool
    storage_verified: bool
    weight_sha256: str
    model_load_ready: bool
    inference_ready: bool
    runtime_ready: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMRetryDependencyAvailabilityRecord:
    record_id: str
    probe_method: str
    timm_find_spec_result: bool
    mobile_sam_find_spec_result: bool
    timm_target_path_used: bool
    mobile_sam_code_path_used: bool
    real_import_used_for_probe: bool


@dataclass(frozen=True)
class MobileSAMRetryTorchTorchvisionBoundaryRecord:
    record_id: str
    torch_reuse_expected: bool
    expected_torch_version: str
    torchvision_reuse_expected: bool
    torch_reinstall_allowed: bool
    torchvision_reinstall_allowed: bool
    torch_files_installed_in_timm_target: bool
    torchvision_files_installed_in_timm_target: bool
    torch_observed_during_load: bool
    torch_version_observed_if_available: str
    torchvision_observed_during_load: bool
    torchvision_version_observed_if_available: str
    torch_reinstall_performed: bool
    torchvision_reinstall_performed: bool


@dataclass(frozen=True)
class MobileSAMRetryImportExecutionRecord:
    record_id: str
    import_target: str
    mobile_sam_code_path_added: str
    timm_target_path_added: str
    import_attempted: bool
    import_success: bool
    import_error: str
    imported_module_file: str
    dependency_gap_resolved: bool


@dataclass(frozen=True)
class MobileSAMRetryModelLoadExecutionRecord:
    record_id: str
    build_key: str
    checkpoint_path: str
    command_purpose: str
    checkpoint_load_attempted: bool
    model_object_created: bool
    model_type_name: str
    checkpoint_load_success: bool
    checkpoint_load_error: str
    model_object_released: bool
    model_load_retry_success: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool


@dataclass(frozen=True)
class MobileSAMRetryMemoryTimeoutMonitorRecord:
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
class MobileSAMRetryPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    upstream_readiness_verified: bool
    sha256_rechecked: bool
    sha256_matches: bool
    size_matches: bool
    timm_find_spec_verified: bool
    mobile_sam_find_spec_verified: bool
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
class MobileSAMRetryRollbackCleanupRecord:
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
class MobileSAMRetryInferenceRuntimeExclusionRecord:
    record_id: str
    no_image_input: bool
    no_segmentation: bool
    no_prediction: bool
    no_inference: bool
    no_runtime_server: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    model_load_retry_success_not_inference_approval: bool
    model_load_retry_success_not_runtime_approval: bool
    model_load_retry_success_not_output_adapter_approval: bool
    model_load_retry_success_not_semantic_layer_approval: bool
    model_load_retry_success_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMRetryFollowupRegistryPatchRoute:
    route_id: str
    decision_branch: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_purpose: str


@dataclass
class NegativeMobileSAMModelLoadRetryExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadRetryExecutionDecision:
    decision_ref: str
    mobile_sam_model_load_retry_execution_profile_count: int
    mobile_sam_retry_pre_model_load_snapshot_record_count: int
    mobile_sam_retry_sha256_recheck_record_count: int
    mobile_sam_retry_code_and_weight_registry_audit_count: int
    mobile_sam_retry_dependency_availability_record_count: int
    mobile_sam_retry_torch_torchvision_boundary_record_count: int
    mobile_sam_retry_import_execution_record_count: int
    mobile_sam_retry_model_load_execution_record_count: int
    mobile_sam_retry_memory_timeout_monitor_record_count: int
    mobile_sam_retry_post_review_audit_count: int
    mobile_sam_retry_rollback_cleanup_record_count: int
    mobile_sam_retry_inference_runtime_exclusion_record_count: int
    mobile_sam_retry_followup_registry_patch_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    import_success: bool
    dependency_gap_resolved: bool
    checkpoint_load_success: bool
    model_load_retry_success: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
