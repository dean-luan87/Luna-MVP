# -*- coding: utf-8 -*-
"""P1 Model Weight Download Request, Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY).

Compressed phase that merges the weight-download request, owner approval issuance,
weight source review, hash/size/storage planning, download command whitelist,
rollback/deletion policy, and readiness review for P1 model weights. It plans and
approves PREPARATION ONLY — it does NOT download any weight / model / checkpoint /
dataset / example asset, does NOT install / pip / resolve dependencies, and does NOT
do real import, model load, inference, runtime, output adapter, or semantic
promotion. Honest source state drives readiness: mobile_sam's weight source is known
(committed weights/mobile_sam.pt at the pinned MobileSAM commit) → ready for a
download-execution next phase; byte_track's weight source is UNRESOLVED → must NOT be
approved for download execution (no fabricated URL). Weight approval is NOT model
load / inference / runtime / output adapter / semantic / commercial-runtime approval.
Protected, non-deletable test board records are written in `planning` mode.
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

PHASE_ID = "Phase-P1-Model-Weight-Download-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_model_weight_download_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_model_weight_download_request_approval_and_readiness_v1"

WEIGHT_PRINCIPLE_ZH = (
    "压缩阶段：合并权重下载 request、owner approval issuance、source review、hash/size/storage planning、download command "
    "whitelist、rollback/deletion policy 与 readiness review。只生成准备与审批，绝不真正下载权重/模型/checkpoint/数据集/示例，"
    "不安装、不 pip、不装依赖、不真实 import、不 model load、不 inference、不 runtime、不 output adapter、不语义层。诚实来源："
    "mobile_sam 权重来源已知（pinned MobileSAM commit 的 weights/mobile_sam.pt，40728226B）→ ready 进入下载执行阶段；"
    "byte_track 权重来源 UNRESOLVED → 不得批准下载执行（不得伪造 URL）。权重 approval 不等于 model load/inference/runtime/"
    "output adapter/语义/商业 runtime 批准。下载后仍不允许 inference/runtime。真正下载在下一阶段且建议 scope=mobile_sam_only。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "weight_download_request_approval_readiness_only_no_download_no_model_load_no_inference_no_runtime_ready_only_scope"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
WEIGHT_DOWNLOAD_REQUEST_INCLUDED = True
WEIGHT_DOWNLOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
WEIGHT_SOURCE_REVIEW_INCLUDED = True
WEIGHT_HASH_STORAGE_PLANNING_INCLUDED = True
WEIGHT_DOWNLOAD_READINESS_REVIEW_INCLUDED = True

WEIGHT_DOWNLOAD_EXECUTION_ALLOWED = False
MODEL_DOWNLOAD_EXECUTION_ALLOWED = False
CHECKPOINT_DOWNLOAD_EXECUTION_ALLOWED = False
DATASET_DOWNLOAD_EXECUTION_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_EXECUTION_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PATCH_EXECUTION_REF = "Phase-P1-Source-Code-Only-Install-Registry-Patch-Execution-And-Post-Review-v1-001"
UPSTREAM_PATCH_EXECUTION_EXPECTED_GO = "P1_SOURCE_CODE_ONLY_INSTALL_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO"
UPSTREAM_PLANNING_REF = "Phase-P1-Source-Code-Only-Install-Registry-Patch-And-Readiness-Planning-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routing.
NEXT_PHASE_DOWNLOAD_EXECUTION = "Phase-P1-Model-Weight-Download-Execution-And-Post-Review-v1-001"
OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE = "Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001"
FALLBACK_PHASE_WEIGHT_SOURCE_RESOLUTION = "Phase-P1-Model-Weight-Source-Resolution-Planning-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# Upstream registry overlay (must be verified before any weight approval).
REGISTRY_OVERLAY_REL = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
WEIGHT_STORAGE_ROOT = "capabilities/model_weights/p1/"

IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("mobile_sam", "byte_track")
HASH_ALGORITHM = "sha256"

# Expected overlay field values (validated against the actual overlay at runtime).
OVERLAY_EXPECTED: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "readiness_level": "code_only_ready",
        "model_weight_status": "not_downloaded",
        "model_ready": False,
        "inference_ready": False,
        "runtime_ready": False,
    },
    "mobile_sam": {
        "readiness_level": "code_only_ready",
        "model_weight_status": "not_downloaded",
        "checkpoint_weight_status": "not_downloaded",
        "committed_weight_file": "weights/mobile_sam.pt",
        "committed_weight_file_downloaded": False,
        "model_ready": False,
        "inference_ready": False,
        "runtime_ready": False,
    },
}

# --------------------------------------------------------------------------- #
# Weight download candidate plan (planning content; no download).
# --------------------------------------------------------------------------- #
WEIGHT_CANDIDATES: Dict[str, Dict[str, Any]] = {
    "mobile_sam": {
        "asset_id": "mobile_sam",
        "weight_type": "checkpoint",
        "known_committed_weight_file": "weights/mobile_sam.pt",
        "known_size_bytes": 40728226,
        "source_repository": "https://github.com/ChaoningZhang/MobileSAM",
        "source_commit": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "download_source_candidate": "repository_committed_weight_blob_or_release_if_verified",
        "weight_source_known": True,
        "hash_required": True,
        "storage_required": True,
        "download_execution_allowed_next": True,
        "expected_filename": "mobile_sam.pt",
        "storage_path": "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt",
        "source_license": "Apache-2.0",
    },
    "byte_track": {
        "asset_id": "byte_track",
        "weight_type": "detector_or_tracker_weight_to_be_determined",
        "known_committed_weight_file": None,
        "known_size_bytes": 0,
        "source_repository": "https://github.com/FoundationVision/ByteTrack",
        "source_commit": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "download_source_candidate": "unresolved",
        "weight_source_known": False,
        "weight_source_currently_unknown": True,
        "hash_required": True,
        "storage_required": True,
        "download_execution_allowed_next": False,
        "expected_filename": None,
        "storage_path": "capabilities/model_weights/p1/byte_track/",
        "source_license": "MIT",
    },
}

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_registry_overlay_missing_but_weight_approval_generated", "go_key": "overlay_verified", "depends_on": "overlay_verified"},
    {"guard_id": "invalid_b_code_only_ready_unconfirmed_but_weight_approval_generated", "go_key": "code_only_ready_verified", "depends_on": "code_only_ready_verified"},
    {"guard_id": "invalid_c_real_weight_model_checkpoint_download_executed", "go_key": "no_download_execution", "depends_on": "no_download_execution"},
    {"guard_id": "invalid_d_install_pip_dependency_executed", "go_key": "no_install", "depends_on": "no_install"},
    {"guard_id": "invalid_e_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_mobile_sam_source_unreviewed_but_download_allowed", "go_key": "mobile_sam_source_reviewed_before_exec", "depends_on": "mobile_sam_source_reviewed_before_exec"},
    {"guard_id": "invalid_h_byte_track_unresolved_but_download_allowed", "go_key": "byte_track_unresolved_not_exec_approved", "depends_on": "byte_track_unresolved_not_exec_approved"},
    {"guard_id": "invalid_i_weight_approval_treated_as_model_load_approval", "go_key": "approval_not_model_load", "depends_on": "approval_not_model_load"},
    {"guard_id": "invalid_j_weight_approval_treated_as_inference_runtime_approval", "go_key": "approval_not_inference_runtime", "depends_on": "approval_not_inference_runtime"},
    {"guard_id": "invalid_k_hash_plan_missing", "go_key": "hash_plan_present", "depends_on": "hash_plan_present"},
    {"guard_id": "invalid_l_storage_plan_missing", "go_key": "storage_plan_present", "depends_on": "storage_plan_present"},
    {"guard_id": "invalid_m_rollback_deletion_policy_missing", "go_key": "rollback_deletion_policy_present", "depends_on": "rollback_deletion_policy_present"},
    {"guard_id": "invalid_n_command_whitelist_missing_or_executed", "go_key": "command_whitelist_present_not_executed", "depends_on": "command_whitelist_present_not_executed"},
    {"guard_id": "invalid_o_commercial_runtime_approved", "go_key": "commercial_runtime_not_approved", "depends_on": "commercial_runtime_not_approved"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (36 phase + 6 test board = 42).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_weight_download_request_approval_and_readiness_only",
    "registry_overlay_must_be_verified_before_weight_approval",
    "code_only_readiness_must_be_verified_before_weight_approval",
    "weight_download_execution_is_not_allowed_in_this_phase",
    "model_download_execution_is_not_allowed_in_this_phase",
    "checkpoint_download_execution_is_not_allowed_in_this_phase",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "no_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "mobile_sam_weight_source_must_be_reviewed",
    "byte_track_unresolved_weight_source_must_not_be_approved_for_execution",
    "weight_approval_is_not_model_load_approval",
    "weight_approval_is_not_inference_approval",
    "weight_approval_is_not_runtime_approval",
    "weight_approval_is_not_output_adapter_approval",
    "weight_approval_is_not_semantic_layer_approval",
    "hash_plan_is_required",
    "storage_plan_is_required",
    "rollback_deletion_policy_is_required",
    "download_command_whitelist_is_required_and_must_not_execute",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "no_fabricated_weight_url",
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
    "weight_download_request_record",
    "weight_owner_approval_issuance_record",
    "weight_source_review_record",
    "weight_hash_storage_plan_record",
    "weight_download_command_whitelist_record",
    "weight_download_boundary_record",
    "weight_download_readiness_review_record",
    "followup_weight_download_execution_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ModelWeightDownloadRequestApprovalReadinessProfile",
    "CodeOnlyRegistryOverlayAudit",
    "WeightDownloadCandidateRecord",
    "WeightDownloadRequestRecord",
    "WeightSourceReviewRecord",
    "WeightLicenseUsageBoundaryRecord",
    "WeightHashStoragePlanRecord",
    "WeightDownloadCommandWhitelistRecord",
    "WeightOwnerApprovalIssuanceRecord",
    "WeightDownloadRollbackDeletionPolicy",
    "WeightDownloadReadinessReview",
    "WeightDownloadExecutionHandoffRecord",
    "NegativeWeightDownloadRequestApprovalReadinessGuard",
    "P1ModelWeightDownloadRequestApprovalReadinessDecision",
)

FINAL_DECISION_GO = "P1_MODEL_WEIGHT_DOWNLOAD_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MODEL_WEIGHT_DOWNLOAD_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "registry_overlay_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1ModelWeightDownloadRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    weight_download_request_included: bool
    weight_download_owner_approval_issuance_included: bool
    weight_source_review_included: bool
    weight_hash_storage_planning_included: bool
    weight_download_readiness_review_included: bool
    weight_download_execution_allowed: bool
    model_download_execution_allowed: bool
    checkpoint_download_execution_allowed: bool
    dataset_download_execution_allowed: bool
    example_asset_download_execution_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_patch_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class CodeOnlyRegistryOverlayAudit:
    audit_id: str
    overlay_file_ref: str
    overlay_exists: bool
    byte_track_checks: Dict[str, bool]
    mobile_sam_checks: Dict[str, bool]
    code_only_registry_patch_go_verified: bool
    overlay_audit_passed: bool


@dataclass(frozen=True)
class WeightDownloadCandidateRecord:
    asset_id: str
    weight_type: str
    weight_source_known: bool
    source_repository: str
    source_commit: str
    download_source_candidate: str
    known_committed_weight_file: Optional[str]
    known_size_bytes: int
    hash_required: bool
    storage_required: bool
    download_execution_allowed_next: bool


@dataclass(frozen=True)
class WeightDownloadRequestRecord:
    request_id: str
    requested_assets: Tuple[str, ...]
    mobile_sam_weight_request_included: bool
    byte_track_weight_request_included_as_unresolved_candidate: bool
    request_package_created: bool
    request_package_is_not_download_execution: bool
    request_package_is_not_model_load_approval: bool
    request_package_is_not_inference_approval: bool
    request_package_is_not_runtime_approval: bool


@dataclass(frozen=True)
class WeightSourceReviewRecord:
    asset_id: str
    weight_source_known: bool
    weight_source_ref: Optional[str]
    weight_source_review_completed: bool
    expected_size_bytes: int
    hash_currently_known: bool
    hash_must_be_computed_after_download: bool
    source_license_ref: str
    weight_download_ready_candidate: bool
    requires_separate_weight_source_resolution: bool


@dataclass(frozen=True)
class WeightLicenseUsageBoundaryRecord:
    record_id: str
    weight_download_approval_does_not_approve_commercial_runtime: bool
    weight_download_approval_does_not_approve_model_load: bool
    weight_download_approval_does_not_approve_inference: bool
    weight_download_approval_does_not_approve_runtime: bool
    weight_license_must_be_bound_to_source_asset: bool
    usage_boundary_internal_p1_evaluation_only: bool
    redistribution_not_approved: bool
    commercial_deployment_not_approved: bool
    per_asset_license: Dict[str, str]


@dataclass(frozen=True)
class WeightHashStoragePlanRecord:
    asset_id: str
    expected_filename: Optional[str]
    expected_size_bytes: int
    hash_algorithm: str
    hash_required_after_download: bool
    hash_record_required: bool
    storage_root: str
    asset_specific_storage_path: str
    no_overwrite_without_snapshot: bool
    existing_file_policy: str
    deletion_policy: str
    rollback_policy: str
    test_board_weight_record_required: bool
    execution_ready: bool


@dataclass(frozen=True)
class WeightDownloadCommandWhitelistRecord:
    asset_id: str
    command_template: str
    template_only_do_not_execute: bool
    command_not_executed: bool
    expected_output_path: str
    hash_after_download_required: bool
    command_execution_readiness: bool
    source_pinned_to_verified_commit_or_release: bool


@dataclass(frozen=True)
class WeightOwnerApprovalIssuanceRecord:
    approval_id: str
    owner_approval_granted_for_weight_download_preparation: bool
    owner_approval_granted_for_mobile_sam_weight_download_execution_next: bool
    owner_approval_granted_for_byte_track_weight_download_execution_next: bool
    weight_approval_success_not_model_load_approval: bool
    weight_approval_success_not_inference_approval: bool
    weight_approval_success_not_runtime_approval: bool
    weight_approval_success_not_output_adapter_approval: bool
    weight_approval_success_not_semantic_layer_approval: bool
    model_load_not_approved: bool
    inference_not_approved: bool
    runtime_not_approved: bool
    output_adapter_not_approved: bool
    semantic_layer_not_approved: bool
    commercial_runtime_not_approved: bool
    byte_track_unresolved_weight_download_not_approved: bool


@dataclass(frozen=True)
class WeightDownloadRollbackDeletionPolicy:
    policy_id: str
    pre_download_snapshot_required: bool
    rollback_required: bool
    rollback_deletes_downloaded_weight_if_failed: bool
    rollback_preserves_test_board: bool
    rollback_preserves_registry: bool
    rollback_preserves_review_artifacts: bool
    failed_hash_mismatch_deletes_file_or_quarantines: bool
    partial_download_cleanup_required: bool
    deletion_must_be_recorded: bool


@dataclass(frozen=True)
class WeightDownloadReadinessReview:
    asset_id: str
    can_enter_weight_download_execution_next: bool
    weight_source_resolved: bool
    requires_weight_source_resolution: bool
    can_model_load_after_download: bool
    can_inference_after_download: bool
    can_runtime_after_download: bool
    can_output_adapter_after_download: bool
    can_semantic_layer_after_download: bool


@dataclass(frozen=True)
class WeightDownloadExecutionHandoffRecord:
    handoff_id: str
    recommended_next_phase: str
    allowed_weight_download_execution_scope: str
    ready_assets: Tuple[str, ...]
    unresolved_assets: Tuple[str, ...]
    ready_asset_count: int
    unresolved_asset_count: int
    optional_followup_phase: Optional[str]
    no_model_load_after_download: bool
    no_inference_after_download: bool
    no_runtime_after_download: bool
    no_output_adapter_after_download: bool
    no_semantic_layer_after_download: bool


@dataclass
class NegativeWeightDownloadRequestApprovalReadinessGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ModelWeightDownloadRequestApprovalReadinessDecision:
    decision_ref: str
    model_weight_download_request_approval_readiness_profile_count: int
    code_only_registry_overlay_audit_count: int
    weight_download_candidate_record_count: int
    weight_download_request_record_count: int
    weight_source_review_record_count: int
    weight_license_usage_boundary_record_count: int
    weight_hash_storage_plan_record_count: int
    weight_download_command_whitelist_record_count: int
    weight_owner_approval_issuance_record_count: int
    weight_download_rollback_deletion_policy_count: int
    weight_download_readiness_review_count: int
    weight_download_execution_handoff_record_count: int
    ready_asset_count: int
    unresolved_asset_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
