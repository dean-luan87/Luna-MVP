# -*- coding: utf-8 -*-
"""P1 Model Weight Download Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only).

First REAL weight-download execution phase. It downloads ONLY the readiness-approved
mobile_sam checkpoint (weights/mobile_sam.pt at the pinned MobileSAM commit) into the
controlled storage root, then performs a same-phase post-review: file-exists check,
exact size check (40728226 bytes), sha256 record, storage-path verification, network
log, rollback/deletion readiness, and a model-load/inference/runtime exclusion record.
byte_track weight download is NOT in scope (source unresolved). It does NOT model
load / real import / inference / runtime / output adapter / semantic promotion /
registry mutation / commercial runtime, and NO download outside the mobile_sam scope.
A successful download is NOT model-ready / load / inference / runtime approval.
Protected, non-deletable test board records are written in `real_test` mode.
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

PHASE_ID = "Phase-P1-Model-Weight-Download-Execution-And-Post-Review-v1-001"
SCOPE = "p1_model_weight_download_execution_and_post_review"
WEIGHT_CHAIN = "p1_model_weight_download_execution_and_post_review_v1"

WEIGHT_PRINCIPLE_ZH = (
    "首个真实权重下载执行阶段，scope=mobile_sam_only。仅下载 readiness 已批准的 mobile_sam 权重（pinned MobileSAM commit 的 "
    "weights/mobile_sam.pt，期望 40728226B），并在同阶段完成 post-review：存在性、精确大小、sha256、存储路径校验、network log、"
    "rollback/deletion readiness。byte_track 权重来源 unresolved，不进入本阶段。下载后仍禁止 model load/真实 import/inference/"
    "runtime/output adapter/语义层/registry mutation/商业 runtime，且不得下载 scope 外任何外部文件。下载成功 ≠ model ready / "
    "model load / inference / runtime 批准。测试板块写 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "weight_download_execution_mobile_sam_only_no_model_load_no_inference_no_runtime_download_is_not_readiness"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
WEIGHT_DOWNLOAD_EXECUTION = True
POST_REVIEW_INCLUDED = True
EXECUTION_SCOPE = "mobile_sam_only"
BYTE_TRACK_DOWNLOAD_ALLOWED = False
MOBILE_SAM_DOWNLOAD_ALLOWED = True
MODEL_LOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REQUEST_APPROVAL_READINESS_REF = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001"
UPSTREAM_REQUEST_APPROVAL_READINESS_EXPECTED_GO = "P1_MODEL_WEIGHT_DOWNLOAD_REQUEST_APPROVAL_AND_READINESS_GO"
UPSTREAM_PATCH_EXECUTION_REF = "Phase-P1-Source-Code-Only-Install-Registry-Patch-Execution-And-Post-Review-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routing.
NEXT_PHASE_REGISTRY_PATCH_MODEL_LOAD_READINESS = (
    "Phase-P1-MobileSAM-Weight-Registry-Patch-And-Model-Load-Readiness-Planning-v1-001"
)
OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE = "Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Download target (mobile_sam only). Pinned, evidence-backed raw file URL.
# --------------------------------------------------------------------------- #
MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_EXPECTED_FILENAME = "mobile_sam.pt"
MOBILE_SAM_EXPECTED_SIZE_BYTES = 40728226
MOBILE_SAM_SOURCE_REPOSITORY = "https://github.com/ChaoningZhang/MobileSAM"
MOBILE_SAM_SOURCE_COMMIT = "f706ad9c4eb7f219c00d9050e46328518ffb65d2"
MOBILE_SAM_SOURCE_FILE = "weights/mobile_sam.pt"
MOBILE_SAM_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/ChaoningZhang/MobileSAM/"
    "f706ad9c4eb7f219c00d9050e46328518ffb65d2/weights/mobile_sam.pt"
)
MOBILE_SAM_TARGET_DOMAIN = "raw.githubusercontent.com"
WEIGHT_STORAGE_ROOT = "capabilities/model_weights/p1/"
MOBILE_SAM_DESTINATION_REL = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
HASH_ALGORITHM = "sha256"
EXPECTED_FILE_EXTENSION = ".pt"

# Forbidden download targets (must remain false / absent).
FORBIDDEN_DOWNLOAD_TARGETS: Tuple[str, ...] = (
    "byte_track_weight",
    "any_detector_or_tracker_weight",
    "any_other_model_weight",
    "dataset",
    "example_asset",
    "code_repository",
    "non_whitelisted_external_file",
)

# --------------------------------------------------------------------------- #
# Negative guards (17: Invalid A..Q).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_download_without_pre_download_snapshot", "go_key": "pre_download_snapshot_present", "depends_on": "pre_download_snapshot_present"},
    {"guard_id": "invalid_b_scope_includes_byte_track", "go_key": "scope_mobile_sam_only", "depends_on": "scope_mobile_sam_only"},
    {"guard_id": "invalid_c_downloaded_non_mobile_sam_pt_file", "go_key": "only_mobile_sam_pt_downloaded", "depends_on": "only_mobile_sam_pt_downloaded"},
    {"guard_id": "invalid_d_download_url_not_pinned_or_unreviewed", "go_key": "download_url_pinned_evidence_backed", "depends_on": "download_url_pinned_evidence_backed"},
    {"guard_id": "invalid_e_download_to_uncontrolled_path", "go_key": "download_to_controlled_path", "depends_on": "download_to_controlled_path"},
    {"guard_id": "invalid_f_size_mismatch_but_go", "go_key": "size_matches_expected", "depends_on": "size_matches_expected"},
    {"guard_id": "invalid_g_sha256_not_recorded_but_go", "go_key": "sha256_recorded", "depends_on": "sha256_recorded"},
    {"guard_id": "invalid_h_extra_weight_model_dataset_example_files", "go_key": "no_extra_files_created", "depends_on": "no_extra_files_created"},
    {"guard_id": "invalid_i_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_j_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_k_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_l_download_marked_as_model_inference_runtime_ready", "go_key": "download_not_marked_ready", "depends_on": "download_not_marked_ready"},
    {"guard_id": "invalid_m_rollback_deletion_policy_missing", "go_key": "rollback_deletion_present", "depends_on": "rollback_deletion_present"},
    {"guard_id": "invalid_n_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_o_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (34 phase + 6 test board = 40).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_weight_download_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "byte_track_weight_download_is_not_allowed",
    "pre_download_snapshot_is_required",
    "download_source_must_be_pinned_evidence_backed",
    "download_destination_must_be_controlled",
    "file_size_check_is_required",
    "sha256_hash_record_is_required",
    "storage_path_verification_is_required",
    "extra_downloads_are_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "weight_download_success_is_not_model_readiness",
    "weight_download_success_is_not_model_load_approval",
    "weight_download_success_is_not_inference_approval",
    "weight_download_success_is_not_runtime_approval",
    "weight_download_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "rollback_deletion_policy_is_required",
    "post_review_is_required",
    "candidate_only_boundary_is_preserved",
    "no_download_outside_mobile_sam_scope",
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
    "weight_pre_download_snapshot_record",
    "weight_download_execution_record",
    "weight_file_integrity_record",
    "weight_hash_record",
    "weight_storage_record",
    "weight_download_post_review_record",
    "weight_rollback_deletion_record",
    "model_load_inference_runtime_exclusion_record",
    "followup_model_load_trial_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ModelWeightDownloadExecutionPostReviewProfile",
    "WeightPreDownloadSnapshotRecord",
    "WeightDownloadExecutionScope",
    "WeightDownloadExecutionRecord",
    "WeightFileIntegrityRecord",
    "WeightHashRecord",
    "WeightStorageRecord",
    "WeightDownloadNetworkLogRecord",
    "WeightDownloadPostReviewAudit",
    "WeightRollbackDeletionRecord",
    "ModelLoadInferenceRuntimeExclusionRecord",
    "WeightDownloadFollowupRouteRecord",
    "NegativeWeightDownloadExecutionPostReviewGuard",
    "P1ModelWeightDownloadExecutionPostReviewDecision",
)

FINAL_DECISION_GO = "P1_MODEL_WEIGHT_DOWNLOAD_EXECUTION_AND_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_MODEL_WEIGHT_DOWNLOAD_EXECUTION_AND_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "upstream_readiness_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1ModelWeightDownloadExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    weight_download_execution: bool
    post_review_included: bool
    execution_scope: str
    byte_track_download_allowed: bool
    mobile_sam_download_allowed: bool
    model_load_allowed: bool
    real_import_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    upstream_request_approval_readiness_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class WeightPreDownloadSnapshotRecord:
    snapshot_id: str
    storage_root: str
    destination_path: str
    existing_file_status: str
    existing_file_size: Optional[int]
    existing_file_sha256: Optional[str]
    free_disk_space_bytes: Optional[int]
    upstream_readiness_ref: str
    download_command_whitelist_ref: str
    rollback_policy_ref: str
    timestamp: str
    test_board_ref: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class WeightDownloadExecutionScope:
    scope_id: str
    execution_scope: str
    allowed_asset_ids: Tuple[str, ...]
    forbidden_download_targets: Tuple[str, ...]
    byte_track_in_scope: bool
    mobile_sam_in_scope: bool


@dataclass(frozen=True)
class WeightDownloadExecutionRecord:
    asset_id: str
    download_url: str
    source_repository: str
    source_commit: str
    source_file: str
    destination_path: str
    download_attempted: bool
    download_status: str
    download_return_ok: bool
    overwrote_existing: bool
    downloaded_to_controlled_path: bool
    url_pinned_to_commit: bool
    timestamp: str


@dataclass(frozen=True)
class WeightFileIntegrityRecord:
    asset_id: str
    file_exists: bool
    actual_size_bytes: int
    expected_size_bytes: int
    size_matches_expected: bool
    sha256_computed: bool
    storage_path_matches_plan: bool
    file_not_empty: bool
    file_extension: str
    file_extension_ok: bool
    no_extra_weight_files_created: bool
    no_dataset_files_created: bool
    no_example_asset_files_created: bool
    integrity_ok: bool


@dataclass(frozen=True)
class WeightHashRecord:
    asset_id: str
    hash_algorithm: str
    sha256_value: str
    sha256_recorded: bool
    hash_computed_after_download: bool


@dataclass(frozen=True)
class WeightStorageRecord:
    asset_id: str
    storage_root: str
    storage_path: str
    storage_path_matches_plan: bool
    file_present_at_storage_path: bool
    storage_verified: bool


@dataclass(frozen=True)
class WeightDownloadNetworkLogRecord:
    asset_id: str
    download_url: str
    target_domain: str
    expected_file: str
    destination_path: str
    timestamp: str
    download_status: str
    network_boundary_compliant: bool
    unapproved_network_access: bool


@dataclass(frozen=True)
class WeightDownloadPostReviewAudit:
    audit_id: str
    only_mobile_sam_downloaded: bool
    byte_track_not_downloaded: bool
    file_exists: bool
    expected_size_matches: bool
    sha256_recorded: bool
    storage_path_valid: bool
    no_extra_downloads: bool
    no_model_load: bool
    no_real_import: bool
    no_inference: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_registry_mutation: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class WeightRollbackDeletionRecord:
    record_id: str
    rollback_available: bool
    deletion_policy_available: bool
    hash_mismatch_deletes_or_quarantines_file: bool
    partial_download_cleanup_done: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool


@dataclass(frozen=True)
class ModelLoadInferenceRuntimeExclusionRecord:
    record_id: str
    mobile_sam_weight_downloaded: bool
    mobile_sam_weight_file_present: bool
    mobile_sam_weight_sha256_recorded: bool
    mobile_sam_weight_storage_verified: bool
    model_load_ready: bool
    model_ready: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_ready: bool
    weight_download_success_not_model_load_approval: bool
    weight_download_success_not_model_ready: bool
    weight_download_success_not_inference_approval: bool
    weight_download_success_not_runtime_approval: bool
    weight_download_success_not_output_adapter_approval: bool
    weight_download_success_not_semantic_layer_approval: bool


@dataclass(frozen=True)
class WeightDownloadFollowupRouteRecord:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    optional_followup_phase: Optional[str]
    next_phase_allows_registry_overlay_weight_patch_planning: bool
    next_phase_allows_model_load_trial_request: bool
    next_phase_still_no_direct_inference: bool
    next_phase_still_no_direct_runtime: bool


@dataclass
class NegativeWeightDownloadExecutionPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ModelWeightDownloadExecutionPostReviewDecision:
    decision_ref: str
    model_weight_download_execution_post_review_profile_count: int
    weight_pre_download_snapshot_record_count: int
    weight_download_execution_scope_count: int
    weight_download_execution_record_count: int
    weight_file_integrity_record_count: int
    weight_hash_record_count: int
    weight_storage_record_count: int
    weight_download_network_log_record_count: int
    weight_download_post_review_audit_count: int
    weight_rollback_deletion_record_count: int
    model_load_inference_runtime_exclusion_record_count: int
    weight_download_followup_route_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
