# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Trial Request, Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only).

Prepares the NEXT model-load execution: it produces a model-load trial request, a
narrow owner approval issuance (preparation + execution-next only), a TEMPLATE-ONLY
model-load command whitelist (never executed, no inference/segmentation/prediction),
a sha256 recheck plan, a controlled env/code/weight path plan, a memory/timeout
boundary, a rollback/cleanup plan, and a readiness review. It does NOT real import /
model load / inference / segmentation / runtime / output adapter / semantic promotion /
registry mutation, and downloads NO extra weight. byte_track is out of scope. Model-
load approval is NOT inference / runtime / output adapter / semantic / commercial-
runtime approval. Protected, non-deletable test board records are written in `planning`
mode.
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

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Trial-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_model_load_trial_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_trial_request_approval_and_readiness_v1"

MODEL_LOAD_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only。为下一次 model-load execution 准备：trial request、窄范围 owner approval"
    "（仅 preparation + execution-next）、TEMPLATE-ONLY command whitelist（不执行、无 inference/segmentation/prediction）、"
    "sha256 recheck plan、受控 env/code/weight path plan、memory/timeout boundary、rollback/cleanup plan、readiness review。"
    "不真实 import、不 load model、不 inference、不 segmentation、不 runtime、不 output adapter、不语义层、不改 registry、不额外下载。"
    "byte_track 不在 scope。model-load approval ≠ inference/runtime/output adapter/语义/商业 runtime 批准。测试板块 planning 模式，"
    "protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_load_trial_request_approval_readiness_only_no_load_no_inference_no_runtime_approval_is_not_inference"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
MOBILE_SAM_ONLY = True
MODEL_LOAD_TRIAL_REQUEST_INCLUDED = True
MODEL_LOAD_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
MODEL_LOAD_READINESS_REVIEW_INCLUDED = True
MODEL_LOAD_EXECUTION_ALLOWED = False
REAL_IMPORT_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
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

UPSTREAM_PATCH_EXECUTION_REF = "Phase-P1-MobileSAM-Weight-Registry-Patch-Execution-And-Post-Review-v1-001"
UPSTREAM_PATCH_EXECUTION_EXPECTED_GO = "P1_MOBILE_SAM_WEIGHT_REGISTRY_PATCH_EXECUTION_AND_POST_REVIEW_GO"
UPSTREAM_PLANNING_REF = "Phase-P1-MobileSAM-Weight-Registry-Patch-And-Model-Load-Readiness-Planning-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_MODEL_LOAD_EXECUTION = "Phase-P1-MobileSAM-Model-Load-Trial-Execution-And-Post-Review-v1-001"
OPTIONAL_FOLLOWUP_BYTE_TRACK_SOURCE = "Phase-P1-ByteTrack-Weight-Source-Resolution-Planning-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Registry overlay (must show code_and_weight_ready before approval).
# --------------------------------------------------------------------------- #
REGISTRY_OVERLAY_REL = "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_IMPORT_ROOT = "mobile_sam"
MOBILE_SAM_WEIGHT_FILE_NAME = "mobile_sam.pt"
MOBILE_SAM_WEIGHT_FILE_PATH = "capabilities/model_weights/p1/mobile_sam/mobile_sam.pt"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
MOBILE_SAM_CODE_INSTALL_EVIDENCE_REF = (
    "_tmp_eval_out/p1_controlled_source_install_execution_retry_and_post_review_v1_smoke_v0/"
    "source_retry_code_install_execution_records_v1.json"
)
EXPECTED_READINESS_LEVEL = "code_and_weight_ready"

# Overlay fields that must hold before approval.
OVERLAY_EXPECTED_TRUE: Tuple[str, ...] = (
    "code_only_install_verified",
    "find_spec_verified",
    "weight_downloaded",
    "weight_integrity_verified",
    "storage_verified",
)
OVERLAY_EXPECTED_FALSE: Tuple[str, ...] = (
    "model_load_ready",
    "model_ready",
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
)

# Planned model-load memory/timeout boundary defaults.
PLANNED_MAX_RUNTIME_SECONDS = 300
PLANNED_MEMORY_LIMIT_MB = 4096

# --------------------------------------------------------------------------- #
# Negative guards (16: Invalid A..P).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_overlay_missing_or_not_code_and_weight_ready_but_approval", "go_key": "overlay_code_and_weight_ready", "depends_on": "overlay_code_and_weight_ready"},
    {"guard_id": "invalid_b_weight_sha256_size_storage_unverified_but_approval", "go_key": "weight_integrity_verified", "depends_on": "weight_integrity_verified"},
    {"guard_id": "invalid_c_byte_track_in_scope", "go_key": "byte_track_out_of_scope", "depends_on": "byte_track_out_of_scope"},
    {"guard_id": "invalid_d_real_import_or_model_load", "go_key": "no_real_import_or_model_load", "depends_on": "no_real_import_or_model_load"},
    {"guard_id": "invalid_e_inference_segmentation_prediction", "go_key": "no_inference_segmentation_prediction", "depends_on": "no_inference_segmentation_prediction"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_model_load_approval_treated_as_inference_runtime_approval", "go_key": "approval_not_inference_runtime", "depends_on": "approval_not_inference_runtime"},
    {"guard_id": "invalid_j_command_template_executed", "go_key": "command_template_not_executed", "depends_on": "command_template_not_executed"},
    {"guard_id": "invalid_k_sha256_recheck_plan_missing", "go_key": "sha256_recheck_plan_present", "depends_on": "sha256_recheck_plan_present"},
    {"guard_id": "invalid_l_memory_timeout_boundary_missing", "go_key": "memory_timeout_boundary_present", "depends_on": "memory_timeout_boundary_present"},
    {"guard_id": "invalid_m_rollback_cleanup_plan_missing", "go_key": "rollback_cleanup_plan_present", "depends_on": "rollback_cleanup_plan_present"},
    {"guard_id": "invalid_n_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_o_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_p_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (33 phase + 6 test board = 39).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_model_load_trial_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "byte_track_is_out_of_scope",
    "registry_overlay_must_show_code_and_weight_ready_before_approval",
    "weight_sha256_must_be_verified_before_approval",
    "weight_size_must_be_verified_before_approval",
    "weight_storage_path_must_be_verified_before_approval",
    "model_load_execution_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed",
    "inference_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "model_load_approval_is_not_inference_approval",
    "model_load_approval_is_not_runtime_approval",
    "model_load_approval_is_not_output_adapter_approval",
    "model_load_approval_is_not_semantic_layer_approval",
    "commercial_runtime_is_not_approved",
    "command_whitelist_is_template_only_and_must_not_execute",
    "sha256_recheck_is_required_before_model_load_execution",
    "memory_limit_is_required",
    "timeout_is_required",
    "rollback_cleanup_planning_is_required",
    "candidate_only_boundary_is_preserved",
    "no_fabricated_command",
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
    "mobile_sam_code_and_weight_registry_audit_record",
    "mobile_sam_model_load_trial_request_record",
    "mobile_sam_owner_approval_issuance_record",
    "mobile_sam_model_load_command_whitelist_record",
    "mobile_sam_sha256_recheck_plan_record",
    "mobile_sam_memory_timeout_boundary_record",
    "mobile_sam_model_load_rollback_cleanup_record",
    "mobile_sam_model_load_readiness_review_record",
    "mobile_sam_followup_execution_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMModelLoadTrialRequestApprovalReadinessProfile",
    "MobileSAMCodeAndWeightRegistryAudit",
    "MobileSAMModelLoadTrialRequestRecord",
    "MobileSAMModelLoadOwnerApprovalIssuanceRecord",
    "MobileSAMModelLoadCommandWhitelistRecord",
    "MobileSAMModelLoadSha256RecheckPlan",
    "MobileSAMModelLoadEnvPathPlan",
    "MobileSAMModelLoadMemoryTimeoutBoundary",
    "MobileSAMModelLoadRollbackCleanupPlan",
    "MobileSAMModelLoadReadinessReview",
    "MobileSAMModelLoadExecutionHandoffRecord",
    "NegativeMobileSAMModelLoadRequestApprovalReadinessGuard",
    "P1MobileSAMModelLoadRequestApprovalReadinessDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "registry_overlay_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMModelLoadTrialRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    mobile_sam_only: bool
    model_load_trial_request_included: bool
    model_load_owner_approval_issuance_included: bool
    model_load_readiness_review_included: bool
    model_load_execution_allowed: bool
    real_import_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_patch_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMCodeAndWeightRegistryAudit:
    audit_id: str
    overlay_file_ref: str
    overlay_exists: bool
    readiness_level: str
    readiness_level_ok: bool
    true_field_checks: Dict[str, bool]
    false_field_checks: Dict[str, bool]
    weight_file_path_ok: bool
    weight_size_ok: bool
    weight_sha256_ok: bool
    byte_track_weight_downloaded: bool
    byte_track_out_of_scope: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMModelLoadTrialRequestRecord:
    request_id: str
    asset_id: str
    request_scope: str
    model_load_trial_requested: bool
    model_load_execution_requested_next: bool
    no_inference_requested: bool
    no_runtime_requested: bool
    no_output_adapter_requested: bool
    no_semantic_layer_requested: bool
    request_is_not_execution: bool
    request_is_not_inference_approval: bool
    request_is_not_runtime_approval: bool
    request_is_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMModelLoadOwnerApprovalIssuanceRecord:
    approval_id: str
    owner_approval_granted_for_model_load_preparation: bool
    owner_approval_granted_for_model_load_execution_next: bool
    inference_not_approved: bool
    runtime_not_approved: bool
    output_adapter_not_approved: bool
    semantic_layer_not_approved: bool
    commercial_runtime_not_approved: bool
    registry_mutation_not_approved: bool
    additional_weight_download_not_approved: bool
    model_load_approval_success_not_inference_approval: bool
    model_load_approval_success_not_runtime_approval: bool
    model_load_approval_success_not_output_adapter_approval: bool
    model_load_approval_success_not_semantic_layer_approval: bool
    model_load_approval_success_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMModelLoadCommandWhitelistRecord:
    record_id: str
    controlled_python_executable: str
    controlled_env_path: str
    source_code_path_ref: str
    weight_path: str
    import_target: str
    checkpoint_load_target: str
    command_template: str
    no_inference_command_allowed: bool
    no_image_input_allowed: bool
    no_segmentation_prediction_call_allowed: bool
    no_runtime_server_allowed: bool
    command_template_only: bool
    command_not_executed: bool
    model_load_command_template_success_not_model_load_execution: bool


@dataclass(frozen=True)
class MobileSAMModelLoadSha256RecheckPlan:
    plan_id: str
    sha256_recheck_required_before_model_load: bool
    expected_sha256: str
    expected_size_bytes: int
    storage_path: str
    sha256_mismatch_blocks_model_load: bool
    size_mismatch_blocks_model_load: bool


@dataclass(frozen=True)
class MobileSAMModelLoadEnvPathPlan:
    plan_id: str
    controlled_model_load_env_required: bool
    model_load_env_path: str
    code_path_ref_required: bool
    weight_path_ref_required: bool
    no_global_env_mutation_allowed: bool
    no_install_during_model_load_trial: bool
    no_download_during_model_load_trial: bool


@dataclass(frozen=True)
class MobileSAMModelLoadMemoryTimeoutBoundary:
    boundary_id: str
    memory_usage_limit_required: bool
    memory_limit_mb_planned: int
    timeout_required: bool
    max_runtime_seconds_planned: int
    oom_handling_required: bool
    timeout_failure_records_required: bool
    partial_model_object_cleanup_required: bool
    no_persistent_runtime_process_allowed: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRollbackCleanupPlan:
    plan_id: str
    pre_model_load_snapshot_required: bool
    rollback_required: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_registry: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    failed_model_load_cleanup_required: bool
    partial_model_object_cleanup_required: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class MobileSAMModelLoadReadinessReview:
    review_id: str
    can_enter_model_load_execution_next: bool
    model_load_execution_scope: str
    can_inference_after_model_load: bool
    can_runtime_after_model_load: bool
    can_output_adapter_after_model_load: bool
    can_semantic_layer_after_model_load: bool
    inference_requires_separate_trial: bool
    runtime_requires_separate_trial: bool
    output_adapter_requires_separate_review: bool
    semantic_layer_requires_separate_promotion: bool


@dataclass(frozen=True)
class MobileSAMModelLoadExecutionHandoffRecord:
    handoff_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_controlled_import: bool
    next_phase_allows_controlled_model_load: bool
    next_phase_allows_sha256_recheck: bool
    next_phase_allows_memory_timeout_monitoring: bool
    next_phase_still_no_inference: bool
    next_phase_still_no_segmentation_prediction: bool
    next_phase_still_no_runtime: bool
    optional_followup_phase: Optional[str]


@dataclass
class NegativeMobileSAMModelLoadRequestApprovalReadinessGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_model_load_request_approval_readiness_profile_count: int
    mobile_sam_code_and_weight_registry_audit_count: int
    mobile_sam_model_load_trial_request_record_count: int
    mobile_sam_owner_approval_issuance_record_count: int
    mobile_sam_model_load_command_whitelist_record_count: int
    mobile_sam_sha256_recheck_plan_record_count: int
    mobile_sam_model_load_env_path_plan_count: int
    mobile_sam_memory_timeout_boundary_count: int
    mobile_sam_model_load_rollback_cleanup_count: int
    mobile_sam_model_load_readiness_review_count: int
    mobile_sam_model_load_execution_handoff_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
