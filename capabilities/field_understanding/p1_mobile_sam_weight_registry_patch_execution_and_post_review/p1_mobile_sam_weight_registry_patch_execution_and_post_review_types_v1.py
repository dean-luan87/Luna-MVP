# -*- coding: utf-8 -*-
"""P1 MobileSAM Weight Registry Patch Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

Executes the REAL registry-overlay patch for mobile_sam ONLY: writes the verified
weight-download metadata (weight_downloaded / sha256 / storage_path / size / source
commit / source file / source url / license / integrity_verified / storage_verified)
and lifts readiness_level to `code_and_weight_ready`, while keeping model_load_ready /
model_ready / inference_ready / runtime_ready / output_adapter_ready /
semantic_layer_ready / commercial_runtime_approved ALL false. byte_track and every
other asset are left UNCHANGED. It does NOT model load / real import / inference /
runtime / output adapter / semantic promotion, and downloads NO extra weight. A
successful registry patch is NOT model-load / inference / runtime approval. A pre-patch
snapshot + diff + post-review run in the same phase. Protected, non-deletable test
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

PHASE_ID = "Phase-P1-MobileSAM-Weight-Registry-Patch-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_weight_registry_patch_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_weight_registry_patch_execution_and_post_review_v1"

PATCH_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only。对 registry overlay 只修改 mobile_sam：写入已验证的权重下载元数据"
    "（weight_downloaded/sha256/storage_path/size/source_commit/source_file/source_url/license/integrity_verified/"
    "storage_verified），并把 readiness_level 提升为 code_and_weight_ready；同时保持 model_load_ready/model_ready/"
    "inference_ready/runtime_ready/output_adapter_ready/semantic_layer_ready/commercial_runtime_approved 全部 false。"
    "byte_track 及其余资产保持不变。不 model load、不真实 import、不 inference、不 runtime、不 output adapter、不语义层、"
    "不额外下载权重。registry patch 成功 ≠ model load/inference/runtime 批准。同阶段含 pre-patch snapshot + diff + post-review。"
    "测试板块 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "registry_weight_patch_mobile_sam_only_code_and_weight_ready_not_model_loaded_not_inference_not_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
WEIGHT_REGISTRY_PATCH_EXECUTION = True
POST_REVIEW_INCLUDED = True
REGISTRY_MUTATION_ALLOWED = True
REGISTRY_FILE_WRITE_ALLOWED = True
ALLOWED_REGISTRY_PATCH_SCOPE = "mobile_sam_weight_download_metadata"
ADDITIONAL_WEIGHT_DOWNLOAD_ALLOWED = False
BYTE_TRACK_WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PLANNING_REF = "Phase-P1-MobileSAM-Weight-Registry-Patch-And-Model-Load-Readiness-Planning-v1-001"
UPSTREAM_PLANNING_EXPECTED_GO = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_AND_MODEL_LOAD_READINESS_PLANNING_GO"
UPSTREAM_DOWNLOAD_EXECUTION_REF = "Phase-P1-Model-Weight-Download-Execution-And-Post-Review-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_MODEL_LOAD_TRIAL = "Phase-P1-MobileSAM-Model-Load-Trial-Request-Approval-And-Readiness-v1-001"
OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE = "Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Registry overlay target.
# --------------------------------------------------------------------------- #
REGISTRY_OVERLAY_REL = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
PATCH_ASSET_ID = "mobile_sam"
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

# Verified mobile_sam weight facts (from the real download + planning GO).
MOBILE_SAM_WEIGHT_FILE_NAME = "mobile_sam.pt"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
MOBILE_SAM_WEIGHT_SOURCE_URL = (
    "https://raw.githubusercontent.com/ChaoningZhang/MobileSAM/"
    "f706ad9c4eb7f219c00d9050e46328518ffb65d2/weights/mobile_sam.pt"
)
MOBILE_SAM_WEIGHT_SOURCE_COMMIT = "f706ad9c4eb7f219c00d9050e46328518ffb65d2"
MOBILE_SAM_WEIGHT_SOURCE_FILE = "weights/mobile_sam.pt"
MOBILE_SAM_WEIGHT_LICENSE_REF = "Apache-2.0 repository license"
PLANNED_READINESS_LEVEL = "code_and_weight_ready"

# The exact fields the patch writes onto the mobile_sam overlay entry.
PATCH_AFTER_VALUES: Dict[str, Any] = {
    "weight_downloaded": True,
    "model_weight_status": "downloaded",
    "checkpoint_weight_status": "downloaded",
    "committed_weight_file_downloaded": True,
    "weight_file_path": MOBILE_SAM_WEIGHT_FILE_PATH,
    "weight_file_name": MOBILE_SAM_WEIGHT_FILE_NAME,
    "weight_file_size_bytes": MOBILE_SAM_WEIGHT_SIZE_BYTES,
    "weight_sha256": MOBILE_SAM_WEIGHT_SHA256,
    "weight_source_commit": MOBILE_SAM_WEIGHT_SOURCE_COMMIT,
    "weight_source_file": MOBILE_SAM_WEIGHT_SOURCE_FILE,
    "weight_source_url": MOBILE_SAM_WEIGHT_SOURCE_URL,
    "weight_license_ref": MOBILE_SAM_WEIGHT_LICENSE_REF,
    "weight_integrity_verified": True,
    "storage_verified": True,
    "weight_download_required_before_model_ready": False,
    "weight_download_evidence_ref": (
        "_tmp_eval_out/p1_model_weight_download_execution_and_post_review_v1_smoke_v0/"
        "p1_model_weight_download_execution_and_post_review_review_v1.json"
    ),
    "readiness_level": PLANNED_READINESS_LEVEL,
    "model_load_ready": False,
    "model_ready": False,
    "inference_ready": False,
    "runtime_ready": False,
    "output_adapter_ready": False,
    "semantic_layer_ready": False,
    "commercial_runtime_approved": False,
}

# Fields that must remain present/unchanged after patch (code-only facts).
PATCH_MUST_PRESERVE: Dict[str, Any] = {
    "code_only_install_verified": True,
    "find_spec_verified": True,
    "import_root": "mobile_sam",
    "full_clone_allowed": False,
    "weight_excluding_checkout_required": True,
}

# Readiness flags that MUST be false after patch.
READINESS_FLAGS_MUST_BE_FALSE: Tuple[str, ...] = (
    "model_load_ready",
    "model_ready",
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
)

# --------------------------------------------------------------------------- #
# Negative guards (16: Invalid A..P).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_overlay_written_without_pre_patch_snapshot", "go_key": "pre_patch_snapshot_present", "depends_on": "pre_patch_snapshot_present"},
    {"guard_id": "invalid_b_non_mobile_sam_asset_modified", "go_key": "only_mobile_sam_modified", "depends_on": "only_mobile_sam_modified"},
    {"guard_id": "invalid_c_byte_track_modified", "go_key": "byte_track_unchanged", "depends_on": "byte_track_unchanged"},
    {"guard_id": "invalid_d_field_out_of_weight_metadata_scope", "go_key": "patch_scope_valid", "depends_on": "patch_scope_valid"},
    {"guard_id": "invalid_e_model_inference_runtime_ready_set_true", "go_key": "readiness_flags_remain_false", "depends_on": "readiness_flags_remain_false"},
    {"guard_id": "invalid_f_output_semantic_commercial_set_true", "go_key": "output_semantic_commercial_false", "depends_on": "output_semantic_commercial_false"},
    {"guard_id": "invalid_g_extra_weight_model_checkpoint_dataset_example_downloaded", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_h_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_i_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_j_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_k_diff_missing", "go_key": "diff_present", "depends_on": "diff_present"},
    {"guard_id": "invalid_l_patch_go_treated_as_model_load_approval", "go_key": "patch_not_model_load_approval", "depends_on": "patch_not_model_load_approval"},
    {"guard_id": "invalid_m_patch_go_treated_as_inference_runtime_approval", "go_key": "patch_not_inference_runtime_approval", "depends_on": "patch_not_inference_runtime_approval"},
    {"guard_id": "invalid_n_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_o_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_p_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (33 phase + 6 test board = 39).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_weight_registry_patch_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "only_mobile_sam_may_be_modified",
    "byte_track_must_not_be_modified",
    "registry_pre_patch_snapshot_is_required",
    "registry_diff_is_required",
    "registry_post_review_is_required",
    "only_mobile_sam_weight_metadata_may_be_patched",
    "readiness_level_may_be_set_to_code_and_weight_ready",
    "model_load_ready_must_remain_false",
    "model_ready_must_remain_false",
    "inference_ready_must_remain_false",
    "runtime_ready_must_remain_false",
    "output_adapter_ready_must_remain_false",
    "semantic_layer_ready_must_remain_false",
    "commercial_runtime_approved_must_remain_false",
    "additional_weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "checkpoint_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "weight_registry_patch_success_is_not_model_load_approval",
    "weight_registry_patch_success_is_not_inference_approval",
    "weight_registry_patch_success_is_not_runtime_approval",
    "model_load_requires_separate_request_and_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "mobile_sam_weight_registry_patch_snapshot_record",
    "mobile_sam_weight_registry_patch_execution_record",
    "mobile_sam_weight_registry_patch_diff_record",
    "mobile_sam_weight_registry_patch_post_review_record",
    "mobile_sam_model_load_boundary_record",
    "mobile_sam_followup_model_load_trial_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMWeightRegistryPatchExecutionPostReviewProfile",
    "MobileSAMWeightRegistryPrePatchSnapshotRecord",
    "MobileSAMWeightRegistryPatchExecutionRecord",
    "MobileSAMWeightRegistryPatchDiffRecord",
    "MobileSAMWeightRegistryPostReviewAudit",
    "MobileSAMWeightRegistryRollbackReadinessRecord",
    "MobileSAMCodeAndWeightReadinessRecord",
    "MobileSAMModelLoadBoundaryRecord",
    "MobileSAMFollowupModelLoadTrialRoute",
    "NegativeMobileSAMWeightRegistryPatchExecutionGuard",
    "P1MobileSAMWeightRegistryPatchExecutionDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "registry_overlay_reused_and_extended": True,
    "planned_patch_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMWeightRegistryPatchExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    weight_registry_patch_execution: bool
    post_review_included: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
    allowed_registry_patch_scope: str
    additional_weight_download_allowed: bool
    byte_track_weight_download_allowed: bool
    model_load_allowed: bool
    real_import_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    upstream_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMWeightRegistryPrePatchSnapshotRecord:
    snapshot_id: str
    overlay_file_ref: str
    overlay_exists: bool
    mobile_sam_registry_before: Dict[str, Any]
    byte_track_registry_before: Dict[str, Any]
    timestamp: str
    upstream_planning_ref: str
    rollback_snapshot_ref: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class MobileSAMWeightRegistryPatchExecutionRecord:
    execution_id: str
    overlay_file_ref: str
    patch_asset_id: str
    patch_applied: bool
    overlay_written: bool
    patched_fields: Tuple[str, ...]
    patched_by_phase: str
    patched_at_utc: str
    out_of_scope_assets_untouched: bool


@dataclass(frozen=True)
class MobileSAMWeightRegistryPatchDiffRecord:
    diff_id: str
    changed_asset_count: int
    changed_assets: Tuple[str, ...]
    byte_track_changed: bool
    changed_field_paths: Tuple[str, ...]
    before_values: Dict[str, Any]
    after_values: Dict[str, Any]
    no_unscoped_asset_changed: bool
    no_model_load_ready_field_set_true: bool
    no_model_ready_field_set_true: bool
    no_inference_ready_field_set_true: bool
    no_runtime_ready_field_set_true: bool
    no_output_adapter_ready_field_set_true: bool
    no_semantic_layer_ready_field_set_true: bool


@dataclass(frozen=True)
class MobileSAMWeightRegistryPostReviewAudit:
    audit_id: str
    registry_patch_applied: bool
    registry_patch_scope_valid: bool
    changed_asset_count: int
    only_mobile_sam_changed: bool
    byte_track_unchanged: bool
    weight_downloaded_written: bool
    weight_sha256_written: bool
    weight_storage_path_written: bool
    weight_size_written: bool
    weight_source_commit_written: bool
    weight_integrity_verified_written: bool
    storage_verified_written: bool
    readiness_level_code_and_weight_ready_written: bool
    model_load_ready_false_written: bool
    model_ready_false_written: bool
    inference_ready_false_written: bool
    runtime_ready_false_written: bool
    output_adapter_ready_false_written: bool
    semantic_layer_ready_false_written: bool
    commercial_runtime_false_written: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class MobileSAMWeightRegistryRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_snapshot_ref: str
    rollback_not_executed_by_default: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_must_preserve_weight_file: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class MobileSAMCodeAndWeightReadinessRecord:
    asset_id: str
    readiness_level: str
    code_only_install_verified: bool
    find_spec_verified: bool
    weight_downloaded: bool
    weight_integrity_verified: bool
    storage_verified: bool
    model_load_ready: bool
    model_ready: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool
    code_and_weight_ready_not_model_loaded: bool
    code_and_weight_ready_not_model_ready: bool
    code_and_weight_ready_not_inference_ready: bool
    code_and_weight_ready_not_runtime_ready: bool


@dataclass(frozen=True)
class MobileSAMModelLoadBoundaryRecord:
    record_id: str
    weight_registry_patch_success_not_model_load_approval: bool
    code_and_weight_ready_not_model_loaded: bool
    code_and_weight_ready_not_model_ready: bool
    code_and_weight_ready_not_inference_ready: bool
    code_and_weight_ready_not_runtime_ready: bool
    model_load_requires_separate_request: bool
    model_load_requires_owner_approval: bool
    model_load_trial_requires_separate_phase: bool
    inference_requires_separate_trial: bool
    runtime_requires_separate_trial: bool
    output_adapter_requires_separate_review: bool
    semantic_layer_requires_separate_promotion: bool
    commercial_runtime_not_approved: bool


@dataclass(frozen=True)
class MobileSAMFollowupModelLoadTrialRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_model_load_trial_request: bool
    next_phase_allows_owner_approval_issuance_for_model_load: bool
    next_phase_allows_model_load_command_whitelist_planning: bool
    next_phase_still_no_direct_model_load: bool
    next_phase_still_no_inference: bool
    next_phase_still_no_runtime: bool
    optional_followup_phase: Optional[str]


@dataclass
class NegativeMobileSAMWeightRegistryPatchExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMWeightRegistryPatchExecutionDecision:
    decision_ref: str
    mobile_sam_weight_registry_patch_execution_profile_count: int
    mobile_sam_weight_registry_pre_patch_snapshot_record_count: int
    mobile_sam_weight_registry_patch_execution_record_count: int
    mobile_sam_weight_registry_patch_diff_record_count: int
    mobile_sam_weight_registry_post_review_audit_count: int
    mobile_sam_weight_registry_rollback_readiness_record_count: int
    mobile_sam_code_and_weight_readiness_record_count: int
    mobile_sam_model_load_boundary_record_count: int
    mobile_sam_followup_model_load_trial_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
