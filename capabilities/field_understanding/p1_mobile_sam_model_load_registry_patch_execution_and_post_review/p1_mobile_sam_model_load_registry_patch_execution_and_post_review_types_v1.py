# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Registry Patch Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

Executes REAL registry overlay patch for mobile_sam ONLY: writes model_load_verified,
checkpoint_load_verified, dependency_gap_resolved, timm repair metadata, and lifts
readiness_level to model_load_verified while keeping inference/runtime/output/semantic/
commercial flags false. byte_track unchanged. No inference/import/load/download.
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

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_model_load_registry_patch_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_registry_patch_execution_and_post_review_v1"

PATCH_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。对 registry overlay 只修改 mobile_sam：写入 model_load_verified、"
    "checkpoint_load_verified、dependency_gap_resolved、timm 依赖修复元数据、model_type_name、性能摘要，"
    "readiness_level=model_load_verified；inference/runtime/output/semantic/commercial 保持 false。"
    "byte_track 及其余资产不变。不 inference、不读图、不 runtime、不额外下载。registry patch 成功 ≠ inference 批准。"
    "同阶段含 pre-patch snapshot + diff + post-review。测试板块 real_test，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "registry_model_load_verified_mobile_sam_only_not_inference_not_runtime"
)

REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
MODEL_LOAD_REGISTRY_PATCH_EXECUTION = True
POST_REVIEW_INCLUDED = True
REGISTRY_MUTATION_ALLOWED = True
REGISTRY_FILE_WRITE_ALLOWED = True
ALLOWED_REGISTRY_PATCH_SCOPE = "mobile_sam_model_load_verified_metadata"
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
MODEL_LOAD_RETRY_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_PLANNING_REF = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Planning-v1-001"
)
UPSTREAM_PLANNING_EXPECTED_GO = (
    "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_AND_INFERENCE_TRIAL_READINESS_PLANNING_GO"
)
UPSTREAM_MODEL_LOAD_RETRY_REF = (
    "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"
)
UPSTREAM_MODEL_LOAD_RETRY_EXPECTED_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_INFERENCE_TRIAL_REQUEST = (
    "Phase-P1-MobileSAM-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
NEXT_PHASE_BLOCKED = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Blocker-Review-v1-001"
)

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
PATCH_ASSET_ID = "mobile_sam"
PLANNED_READINESS_LEVEL = "model_load_verified"

MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = (
    "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
)

UPSTREAM_RETRY_REVIEW_REL = (
    "_tmp_eval_out/p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1_smoke_v0/"
    "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_review_v1.json"
)

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

ALLOWED_PATCH_FIELD_NAMES: Tuple[str, ...] = (
    "model_load_verified",
    "checkpoint_load_verified",
    "dependency_gap_resolved",
    "dependency_repair_applied",
    "dependency_repair_dependency",
    "dependency_repair_dependency_version",
    "dependency_repair_method",
    "model_type_name",
    "model_load_trial_phase_ref",
    "model_load_trial_result",
    "model_load_peak_memory_mb",
    "model_load_elapsed_seconds",
    "torch_version_observed",
    "torchvision_version_observed",
    "readiness_level",
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
    "weight_downloaded",
    "model_weight_status",
    "checkpoint_weight_status",
    "weight_file_path",
    "weight_file_size_bytes",
    "weight_sha256",
    "weight_integrity_verified",
    "storage_verified",
    "code_only_install_verified",
    "find_spec_verified",
    "import_root",
    "full_clone_allowed",
    "weight_excluding_checkout_required",
    "model_load_ready",
    "model_ready",
)

READINESS_FLAGS_MUST_BE_FALSE: Tuple[str, ...] = (
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
)

FORBIDDEN_INFERENCE_FIELDS: Tuple[str, ...] = (
    "inference_trial_executed",
    "inference_verified",
    "runtime_verified",
    "output_adapter_verified",
    "semantic_layer_promoted",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_snapshot_but_write", "go_key": "pre_patch_snapshot_present", "depends_on": "pre_patch_snapshot_present"},
    {"guard_id": "invalid_b_upstream_planning_not_go", "go_key": "upstream_planning_go_verified", "depends_on": "upstream_planning_go_verified"},
    {"guard_id": "invalid_c_upstream_retry_not_go", "go_key": "upstream_retry_go_verified", "depends_on": "upstream_retry_go_verified"},
    {"guard_id": "invalid_d_non_mobile_sam_modified", "go_key": "only_mobile_sam_modified", "depends_on": "only_mobile_sam_modified"},
    {"guard_id": "invalid_e_byte_track_modified", "go_key": "byte_track_unchanged", "depends_on": "byte_track_unchanged"},
    {"guard_id": "invalid_f_field_out_of_scope", "go_key": "patch_scope_valid", "depends_on": "patch_scope_valid"},
    {"guard_id": "invalid_g_downstream_ready_set_true", "go_key": "downstream_ready_remain_false", "depends_on": "downstream_ready_remain_false"},
    {"guard_id": "invalid_h_inference_seg_pred", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_i_image_input", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_j_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_k_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_l_patch_go_as_inference_approval", "go_key": "patch_not_inference_approval", "depends_on": "patch_not_inference_approval"},
    {"guard_id": "invalid_m_patch_go_as_runtime_semantic_approval", "go_key": "patch_not_runtime_semantic_approval", "depends_on": "patch_not_runtime_semantic_approval"},
    {"guard_id": "invalid_n_diff_missing", "go_key": "diff_present", "depends_on": "diff_present"},
    {"guard_id": "invalid_o_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_p_rollback_missing", "go_key": "rollback_present", "depends_on": "rollback_present"},
    {"guard_id": "invalid_q_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_r_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_s_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_model_load_registry_patch_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "pre_patch_snapshot_is_required",
    "upstream_planning_must_be_go",
    "upstream_model_load_retry_must_be_go",
    "registry_mutation_allowed_only_for_model_load_verified_metadata",
    "only_mobile_sam_may_be_changed",
    "byte_track_must_remain_unchanged",
    "out_of_scope_assets_must_remain_unchanged",
    "model_load_verified_may_be_written_true",
    "checkpoint_load_verified_may_be_written_true",
    "dependency_gap_resolved_may_be_written_true",
    "readiness_level_may_become_model_load_verified",
    "inference_ready_must_remain_false",
    "runtime_ready_must_remain_false",
    "output_adapter_ready_must_remain_false",
    "semantic_layer_ready_must_remain_false",
    "commercial_runtime_approved_must_remain_false",
    "inference_is_not_allowed",
    "image_input_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_download_is_not_allowed",
    "registry_patch_success_is_not_inference_approval",
    "registry_patch_success_is_not_runtime_approval",
    "registry_patch_success_is_not_output_adapter_approval",
    "registry_patch_success_is_not_semantic_layer_promotion",
    "diff_record_is_required",
    "post_review_is_required",
    "rollback_readiness_is_required",
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
    "mobile_sam_model_load_registry_pre_patch_snapshot_record",
    "mobile_sam_model_load_registry_patch_execution_record",
    "mobile_sam_model_load_registry_patch_diff_record",
    "mobile_sam_model_load_registry_patch_post_review_record",
    "mobile_sam_inference_boundary_preservation_record",
    "mobile_sam_followup_inference_trial_request_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "registry_overlay_reused_and_extended": True,
    "model_load_retry_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMModelLoadRegistryPatchExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    model_load_registry_patch_execution: bool
    post_review_included: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    allowed_registry_patch_scope: str
    real_inference_allowed: bool
    segmentation_allowed: bool
    prediction_allowed: bool
    image_input_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    model_load_retry_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_planning_ref: str
    upstream_model_load_retry_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryPrePatchSnapshotRecord:
    snapshot_id: str
    registry_overlay_path: str
    registry_overlay_exists: bool
    pre_patch_file_sha256: str
    pre_patch_file_size: int
    asset_count: int
    mobile_sam_pre_patch_entry: Dict[str, Any]
    byte_track_pre_patch_entry: Dict[str, Any]
    out_of_scope_assets_pre_patch_hashes: Dict[str, str]
    rollback_snapshot_path: str
    timestamp: str
    upstream_planning_ref: str
    upstream_model_load_retry_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryPatchExecutionRecord:
    record_id: str
    registry_patch_attempted: bool
    registry_patch_applied: bool
    changed_asset_ids: Tuple[str, ...]
    changed_field_names: Tuple[str, ...]
    changed_field_count: int
    write_timestamp: str
    pre_patch_sha256: str
    post_patch_sha256: str
    patch_scope: str
    no_inference_fields_promoted: bool
    no_runtime_fields_promoted: bool
    no_output_adapter_fields_promoted: bool
    no_semantic_fields_promoted: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryPatchDiffRecord:
    diff_id: str
    changed_asset_count: int
    changed_assets: Tuple[str, ...]
    byte_track_changed: bool
    out_of_scope_assets_changed: bool
    mobile_sam_changed_fields: Tuple[str, ...]
    readiness_level_changed_to: str
    inference_ready_remains_false: bool
    runtime_ready_remains_false: bool
    output_adapter_ready_remains_false: bool
    semantic_layer_ready_remains_false: bool
    commercial_runtime_approved_remains_false: bool
    before_values: Dict[str, Any]
    after_values: Dict[str, Any]


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    registry_patch_applied: bool
    registry_patch_scope_valid: bool
    only_mobile_sam_changed: bool
    byte_track_unchanged: bool
    out_of_scope_assets_unchanged: bool
    model_load_verified_written: bool
    checkpoint_load_verified_written: bool
    dependency_gap_resolved_written: bool
    dependency_repair_metadata_written: bool
    readiness_level_model_load_verified_written: bool
    inference_ready_false_written: bool
    runtime_ready_false_written: bool
    output_adapter_ready_false_written: bool
    semantic_layer_ready_false_written: bool
    commercial_runtime_false_written: bool
    no_inference_execution: bool
    no_image_input: bool
    no_prediction_or_segmentation: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_extra_download: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_snapshot_path: str
    rollback_not_executed_by_default: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    rollback_trigger_conditions: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMModelLoadVerifiedReadinessRecord:
    asset_id: str
    readiness_level: str
    model_load_verified: bool
    checkpoint_load_verified: bool
    dependency_gap_resolved: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool
    model_load_verified_not_inference_ready: bool
    model_load_verified_not_runtime_ready: bool


@dataclass(frozen=True)
class MobileSAMInferenceBoundaryPreservationRecord:
    record_id: str
    registry_patch_success_not_inference_approval: bool
    registry_patch_success_not_inference_execution: bool
    registry_patch_success_not_runtime_approval: bool
    registry_patch_success_not_output_adapter_approval: bool
    registry_patch_success_not_semantic_layer_promotion: bool
    inference_trial_requires_separate_request_approval: bool
    inference_trial_requires_separate_execution_phase: bool
    inference_output_candidate_only_required: bool


@dataclass(frozen=True)
class MobileSAMFollowupInferenceTrialRequestRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_inference_trial_request: bool
    next_phase_still_no_direct_inference: bool


@dataclass
class NegativeMobileSAMModelLoadRegistryPatchExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadRegistryPatchExecutionDecision:
    decision_ref: str
    mobile_sam_model_load_registry_patch_execution_profile_count: int
    mobile_sam_model_load_registry_pre_patch_snapshot_record_count: int
    mobile_sam_model_load_registry_patch_execution_record_count: int
    mobile_sam_model_load_registry_patch_diff_record_count: int
    mobile_sam_model_load_registry_post_review_audit_count: int
    mobile_sam_model_load_registry_rollback_readiness_record_count: int
    mobile_sam_model_load_verified_readiness_record_count: int
    mobile_sam_inference_boundary_preservation_record_count: int
    mobile_sam_followup_inference_trial_request_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    registry_patch_applied: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
