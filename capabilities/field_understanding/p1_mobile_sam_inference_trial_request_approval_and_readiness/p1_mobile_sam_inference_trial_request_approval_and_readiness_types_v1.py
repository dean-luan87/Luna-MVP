# -*- coding: utf-8 -*-
"""P1 MobileSAM Inference Trial Request Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only).

Prepares the NEXT inference execution: trial request, narrow owner approval issuance,
local test image manifest planning (no image read/create), candidate-only output boundary,
command whitelist template, memory/timeout, rollback/cleanup, readiness review.
Does NOT execute inference, read images, import/load, runtime, registry mutation, or download.
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

PHASE_ID = "Phase-P1-MobileSAM-Inference-Trial-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_inference_trial_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_inference_trial_request_approval_and_readiness_v1"

INFERENCE_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only。为下一次 inference trial execution 准备：trial request、"
    "窄范围 owner approval（仅 preparation + execution-next）、local test image manifest 规划（不创建/不读取图片）、"
    "candidate-only output boundary、TEMPLATE-ONLY command whitelist、memory/timeout、rollback/cleanup、readiness review。"
    "不执行 inference、不读图、不 segmentation/prediction、不 runtime/output adapter/语义层、不写 fact、"
    "不 navigation/action/speech、不改 registry、不额外下载。inference approval ≠ runtime/output/semantic/fact 批准。"
    "测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "inference_trial_request_approval_readiness_only_no_inference_no_runtime_approval_is_not_runtime"
)

COMPRESSED_PHASE = True
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
INFERENCE_TRIAL_REQUEST_INCLUDED = True
INFERENCE_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
INFERENCE_TRIAL_READINESS_REVIEW_INCLUDED = True
MODEL_LOAD_VERIFIED_REQUIRED = True
INFERENCE_EXECUTION_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
SEGMENTATION_ALLOWED = False
PREDICTION_ALLOWED = False
IMAGE_INPUT_ALLOWED = False
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
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
UPSTREAM_REGISTRY_PATCH_EXECUTION_REF = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001"
)
UPSTREAM_REGISTRY_PATCH_EXECUTION_EXPECTED_GO = "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_EXECUTION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_INFERENCE_EXECUTION = "Phase-P1-MobileSAM-Inference-Trial-Execution-And-Post-Review-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Inference-Trial-Request-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)
MOBILE_SAM_ASSET_ID = "mobile_sam"
EXPECTED_READINESS_LEVEL = "model_load_verified"
MOBILE_SAM_WEIGHT_SHA256 = (
    "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
)
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226

OVERLAY_EXPECTED_TRUE: Tuple[str, ...] = (
    "model_load_verified",
    "checkpoint_load_verified",
    "dependency_gap_resolved",
    "dependency_repair_applied",
    "weight_downloaded",
    "weight_integrity_verified",
    "storage_verified",
)
OVERLAY_EXPECTED_FALSE: Tuple[str, ...] = (
    "inference_ready",
    "runtime_ready",
    "output_adapter_ready",
    "semantic_layer_ready",
    "commercial_runtime_approved",
)

PLANNED_MEMORY_LIMIT_MB = 4096
PLANNED_TIMEOUT_SECONDS = 300

PLANNED_TEST_IMAGE_MANIFEST_ENTRY: Dict[str, Any] = {
    "test_image_id": "mobile_sam_tiny_static_test_image_v1",
    "local_path": "capabilities/test_assets/p1/mobile_sam/planned_tiny_static_test_image_v1.png",
    "sha256": "pending_verification_in_execution_phase",
    "width": 0,
    "height": 0,
    "file_size_bytes": 0,
    "source_type": "tiny_static_local_test_image",
    "personal_data_absent": True,
    "live_camera_frame": False,
    "external_url_source": False,
    "dataset_source": False,
    "navigation_runtime_frame": False,
    "fact_layer_source": False,
    "semantic_layer_source": False,
    "allowed_for_single_inference_trial": True,
    "must_not_enter_fact_layer": True,
    "must_not_enter_navigation_runtime": True,
    "manifest_status": "planned_not_created",
}

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_registry_not_model_load_verified", "go_key": "overlay_model_load_verified", "depends_on": "overlay_model_load_verified"},
    {"guard_id": "invalid_b_model_load_fields_missing", "go_key": "model_load_fields_verified", "depends_on": "model_load_fields_verified"},
    {"guard_id": "invalid_c_real_inference_executed", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_d_image_input", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_e_real_import_model_load", "go_key": "no_real_import_load", "depends_on": "no_real_import_load"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_fact_navigation_speech", "go_key": "no_fact_navigation_speech", "depends_on": "no_fact_navigation_speech"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_j_approval_as_runtime_semantic_fact", "go_key": "approval_not_downstream", "depends_on": "approval_not_downstream"},
    {"guard_id": "invalid_k_image_manifest_allows_forbidden_source", "go_key": "image_manifest_strict", "depends_on": "image_manifest_strict"},
    {"guard_id": "invalid_l_candidate_boundary_missing", "go_key": "candidate_boundary_present", "depends_on": "candidate_boundary_present"},
    {"guard_id": "invalid_m_whitelist_allows_forbidden", "go_key": "whitelist_strict", "depends_on": "whitelist_strict"},
    {"guard_id": "invalid_n_rollback_missing", "go_key": "rollback_present", "depends_on": "rollback_present"},
    {"guard_id": "invalid_o_test_board_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_deletes_test_board", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_inference_trial_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "upstream_registry_must_be_model_load_verified",
    "model_load_verified_must_be_true_before_inference_request",
    "checkpoint_load_verified_must_be_true_before_inference_request",
    "inference_execution_is_not_allowed_in_this_phase",
    "image_input_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed_in_this_phase",
    "model_load_is_not_allowed_in_this_phase",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "additional_download_is_not_allowed",
    "future_image_input_must_be_local_test_asset_only",
    "future_image_input_must_have_manifest",
    "future_image_input_must_not_contain_personal_data",
    "future_image_input_must_not_use_live_camera",
    "future_image_input_must_not_use_external_url",
    "future_image_input_must_not_use_uncontrolled_dataset",
    "future_inference_output_must_be_candidate_only",
    "future_inference_output_must_not_enter_fact_layer",
    "future_inference_output_must_not_enter_runtime",
    "future_inference_output_must_not_enter_output_adapter",
    "future_inference_output_must_not_enter_semantic_layer",
    "future_inference_output_must_not_trigger_navigation_action_speech",
    "inference_approval_is_not_runtime_approval",
    "inference_approval_is_not_output_adapter_approval",
    "inference_approval_is_not_semantic_layer_approval",
    "inference_approval_is_not_fact_write_approval",
    "inference_approval_is_not_commercial_runtime_approval",
    "commercial_runtime_is_not_approved",
    "rollback_plan_is_required",
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
    "mobile_sam_model_load_verified_registry_audit_record",
    "mobile_sam_inference_trial_request_record",
    "mobile_sam_inference_owner_approval_issuance_record",
    "mobile_sam_local_test_image_manifest_plan_record",
    "mobile_sam_inference_candidate_output_boundary_record",
    "mobile_sam_inference_command_whitelist_record",
    "mobile_sam_inference_memory_timeout_boundary_record",
    "mobile_sam_inference_rollback_cleanup_record",
    "mobile_sam_inference_readiness_review_record",
    "mobile_sam_followup_inference_execution_route_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_INFERENCE_TRIAL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "model_load_verified_registry_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMInferenceTrialRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    planning_only: bool
    mobile_sam_only: bool
    inference_trial_request_included: bool
    inference_owner_approval_issuance_included: bool
    inference_trial_readiness_review_included: bool
    model_load_verified_required: bool
    inference_execution_allowed: bool
    real_inference_allowed: bool
    segmentation_allowed: bool
    prediction_allowed: bool
    image_input_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_registry_patch_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMModelLoadVerifiedRegistryAudit:
    audit_id: str
    registry_overlay_ref: str
    readiness_level: str
    model_load_verified: bool
    checkpoint_load_verified: bool
    dependency_gap_resolved: bool
    dependency_repair_applied: bool
    dependency_repair_dependency: str
    dependency_repair_dependency_version: str
    dependency_repair_method: str
    model_type_name: str
    model_load_trial_result: str
    torch_version_observed: str
    torchvision_version_observed: str
    weight_downloaded: bool
    weight_sha256: str
    weight_file_size_bytes: int
    weight_integrity_verified: bool
    storage_verified: bool
    inference_ready: bool
    runtime_ready: bool
    output_adapter_ready: bool
    semantic_layer_ready: bool
    commercial_runtime_approved: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMInferenceTrialRequestRecord:
    request_id: str
    asset_id: str
    request_scope: str
    inference_trial_requested: bool
    inference_execution_requested_next: bool
    model_load_verified_required: bool
    local_test_image_required: bool
    candidate_output_required: bool
    request_is_not_inference_execution: bool
    request_is_not_runtime_approval: bool
    request_is_not_output_adapter_approval: bool
    request_is_not_semantic_layer_approval: bool
    request_is_not_fact_write_approval: bool
    request_is_not_navigation_action_speech_approval: bool
    request_is_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMInferenceOwnerApprovalIssuanceRecord:
    record_id: str
    owner_approval_granted_for_inference_trial_preparation: bool
    owner_approval_granted_for_inference_trial_execution_next: bool
    runtime_approved: bool
    output_adapter_approved: bool
    semantic_layer_approved: bool
    fact_write_approved: bool
    navigation_action_speech_approved: bool
    commercial_runtime_approved: bool
    registry_mutation_approved: bool
    additional_download_approved: bool
    inference_trial_approval_not_runtime_approval: bool
    inference_trial_approval_not_output_adapter_approval: bool
    inference_trial_approval_not_semantic_layer_approval: bool
    inference_trial_approval_not_fact_write_approval: bool
    inference_trial_approval_not_navigation_action_speech_approval: bool
    inference_trial_approval_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMLocalTestImageManifestPlanningRecord:
    record_id: str
    allowed_future_sources: Tuple[str, ...]
    forbidden_sources: Tuple[str, ...]
    planned_manifest_entries: Tuple[Dict[str, Any], ...]
    image_created_this_phase: bool
    image_read_this_phase: bool


@dataclass(frozen=True)
class MobileSAMInferenceCandidateOutputBoundaryRecord:
    record_id: str
    inference_output_candidate_only: bool
    output_must_not_enter_fact_layer: bool
    output_must_not_enter_runtime: bool
    output_must_not_enter_output_adapter: bool
    output_must_not_enter_semantic_layer: bool
    output_must_not_trigger_navigation_action_speech: bool
    output_must_not_be_user_visible_runtime_output: bool
    output_must_be_written_only_to_eval_artifacts: bool
    output_must_be_marked_candidate: bool
    output_requires_post_review: bool


@dataclass(frozen=True)
class MobileSAMInferenceCommandWhitelistRecord:
    record_id: str
    allowed_future_steps: Tuple[str, ...]
    forbidden_future_steps: Tuple[str, ...]
    command_template_only: bool
    command_not_executed: bool
    inference_command_requires_next_phase: bool


@dataclass(frozen=True)
class MobileSAMInferenceMemoryTimeoutBoundaryRecord:
    record_id: str
    memory_limit_mb: int
    timeout_seconds: int
    oom_handling_required: bool
    timeout_failure_records_required: bool
    candidate_output_cleanup_required: bool
    no_persistent_runtime_process_allowed: bool


@dataclass(frozen=True)
class MobileSAMInferenceRollbackCleanupRecord:
    record_id: str
    pre_inference_snapshot_required: bool
    rollback_required: bool
    rollback_preserves_registry: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    candidate_output_cleanup_required: bool
    no_fact_write_on_failure: bool
    no_registry_mutation_on_failure: bool


@dataclass(frozen=True)
class MobileSAMInferenceReadinessReview:
    review_id: str
    can_enter_inference_trial_execution_next: bool
    inference_trial_execution_scope: str
    inference_execution_requires_test_image_manifest: bool
    inference_execution_requires_sha256_recheck: bool
    inference_execution_requires_model_load_verified: bool
    inference_execution_requires_candidate_output_boundary: bool
    inference_execution_requires_post_review: bool
    can_enter_runtime_after_this_phase: bool
    can_enter_output_adapter_after_this_phase: bool
    can_enter_semantic_layer_after_this_phase: bool
    can_write_fact_after_this_phase: bool


@dataclass(frozen=True)
class MobileSAMFollowupInferenceExecutionRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_allows_single_controlled_inference: bool
    next_phase_still_no_runtime: bool


@dataclass
class NegativeMobileSAMInferenceTrialRequestApprovalGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMInferenceTrialRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_inference_trial_request_approval_readiness_profile_count: int
    mobile_sam_model_load_verified_registry_audit_count: int
    mobile_sam_inference_trial_request_record_count: int
    mobile_sam_inference_owner_approval_issuance_record_count: int
    mobile_sam_local_test_image_manifest_plan_count: int
    mobile_sam_inference_candidate_output_boundary_count: int
    mobile_sam_inference_command_whitelist_count: int
    mobile_sam_inference_memory_timeout_boundary_count: int
    mobile_sam_inference_rollback_cleanup_count: int
    mobile_sam_inference_readiness_review_count: int
    mobile_sam_followup_inference_execution_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
