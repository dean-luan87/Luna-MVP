# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Registry Patch And Inference Trial Readiness Planning — types v1
(PLANNING ONLY, scope = mobile_sam_only).

Translates model-load retry GO into (a) registry overlay patch PLAN (model_load_verified,
NOT written) and (b) inference trial request/approval/readiness PLAN. Does NOT write
registry, import, model load, read images, inference, runtime, output adapter, semantic
layer, or download extra assets. Planning is NOT execution approval.
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

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Planning-v1-001"
SCOPE = "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_registry_patch_and_inference_trial_readiness_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "仅规划，scope=mobile_sam_only。基于 model-load retry GO，规划 registry overlay 写入 "
    "model_load_verified / checkpoint_load_verified / dependency_gap_resolved（不写 registry），"
    "并规划 inference trial request、owner approval、readiness、image input boundary、command "
    "whitelist、memory/timeout、rollback 与 post-review 要求。不修改 registry、不 import、不 model "
    "load、不读取图片、不 inference/segmentation/prediction、不 runtime/output adapter/语义层、"
    "不额外下载。registry patch planning ≠ registry mutation；inference request planning ≠ "
    "inference execution approval。测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_load_verified_is_not_inference_not_runtime_planning_is_not_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
MODEL_LOAD_REGISTRY_PATCH_PLANNING = True
INFERENCE_TRIAL_REQUEST_PLANNING = True
INFERENCE_TRIAL_READINESS_PLANNING = True
REGISTRY_MUTATION_ALLOWED = False
REGISTRY_FILE_WRITE_ALLOWED = False
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

UPSTREAM_MODEL_LOAD_RETRY_REF = (
    "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"
)
UPSTREAM_MODEL_LOAD_RETRY_EXPECTED_GO = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_RETRY_EXECUTION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_PHASE_REGISTRY_PATCH_EXECUTION = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-Execution-And-Post-Review-v1-001"
)
NEXT_PHASE_INFERENCE_TRIAL_REQUEST = (
    "Phase-P1-MobileSAM-Inference-Trial-Request-Approval-And-Readiness-v1-001"
)
NEXT_PHASE_BLOCKED = (
    "Phase-P1-MobileSAM-Model-Load-Registry-Patch-And-Inference-Trial-Readiness-Blocker-Review-v1-001"
)

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Upstream model-load retry evidence (read-only).
# --------------------------------------------------------------------------- #
UPSTREAM_RETRY_OUTPUT_DIR_REL = (
    "_tmp_eval_out/p1_mobile_sam_model_load_trial_retry_execution_and_post_review_v1_smoke_v0"
)
UPSTREAM_RETRY_REVIEW_FILE_REL = (
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/"
    "p1_mobile_sam_model_load_trial_retry_execution_and_post_review_review_v1.json"
)
UPSTREAM_RETRY_ARTIFACT_REFS: Tuple[str, ...] = (
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_pre_model_load_snapshot_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_sha256_recheck_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_dependency_availability_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_torch_torchvision_boundary_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_import_record_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_model_load_execution_record_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_memory_timeout_monitor_v1.json",
    f"{UPSTREAM_RETRY_OUTPUT_DIR_REL}/mobile_sam_retry_post_review_audit_v1.json",
)

MOBILE_SAM_ASSET_ID = "mobile_sam"
MOBILE_SAM_WEIGHT_SHA256 = (
    "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
)
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226
PLANNED_READINESS_LEVEL = "model_load_verified"
REGISTRY_OVERLAY_REL = (
    "capabilities/midplatform/model_registry/code_only_source_install_registry_overlay_v1.json"
)

UPSTREAM_EXPECTED: Dict[str, Any] = {
    "final_decision": UPSTREAM_MODEL_LOAD_RETRY_EXPECTED_GO,
    "blocker_count": 0,
    "negative_guard_passed": 18,
    "import_success": True,
    "dependency_gap_resolved": True,
    "checkpoint_load_success": True,
    "model_load_retry_success": True,
    "model_type_name": "Sam",
}

PLANNED_REGISTRY_PATCH: Dict[str, Any] = {
    "asset_id": MOBILE_SAM_ASSET_ID,
    "model_load_verified": True,
    "checkpoint_load_verified": True,
    "dependency_gap_resolved": True,
    "dependency_repair_applied": True,
    "dependency_repair_dependency": "timm",
    "dependency_repair_dependency_version": "1.0.27",
    "model_type_name": "Sam",
    "model_load_trial_phase_ref": UPSTREAM_MODEL_LOAD_RETRY_REF,
    "model_load_trial_result": "GO",
    "model_load_peak_memory_mb": 359,
    "model_load_elapsed_seconds": 1.75,
    "torch_version_observed": "2.8.0",
    "torchvision_version_observed": "0.23.0",
    "readiness_level": PLANNED_READINESS_LEVEL,
    "inference_ready": False,
    "runtime_ready": False,
    "output_adapter_ready": False,
    "semantic_layer_ready": False,
    "commercial_runtime_approved": False,
    "weight_downloaded": True,
    "weight_sha256": MOBILE_SAM_WEIGHT_SHA256,
    "weight_file_size_bytes": MOBILE_SAM_WEIGHT_SIZE_BYTES,
    "weight_integrity_verified": True,
    "storage_verified": True,
    "code_only_install_verified": True,
    "find_spec_verified": True,
    "import_root": "mobile_sam",
    "full_clone_allowed": False,
    "weight_excluding_checkout_required": True,
}

# --------------------------------------------------------------------------- #
# Negative guards (16: Invalid A..P).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_retry_not_go_but_patch_planned", "go_key": "upstream_retry_go_verified", "depends_on": "upstream_retry_go_verified"},
    {"guard_id": "invalid_b_upstream_boundary_violation_but_inference_planned", "go_key": "upstream_boundary_clean", "depends_on": "upstream_boundary_clean"},
    {"guard_id": "invalid_c_registry_mutated_this_phase", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_d_real_import_or_model_load", "go_key": "no_real_import_load", "depends_on": "no_real_import_load"},
    {"guard_id": "invalid_e_image_input_this_phase", "go_key": "no_image_input", "depends_on": "no_image_input"},
    {"guard_id": "invalid_f_segmentation_prediction_inference", "go_key": "no_seg_pred_inference", "depends_on": "no_seg_pred_inference"},
    {"guard_id": "invalid_g_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_h_extra_download", "go_key": "no_extra_download", "depends_on": "no_extra_download"},
    {"guard_id": "invalid_i_patch_sets_inference_runtime_ready", "go_key": "patch_not_downstream_ready", "depends_on": "patch_not_downstream_ready"},
    {"guard_id": "invalid_j_inference_request_treated_as_execution_approval", "go_key": "request_not_execution_approval", "depends_on": "request_not_execution_approval"},
    {"guard_id": "invalid_k_image_boundary_allows_live_camera_personal", "go_key": "image_boundary_strict", "depends_on": "image_boundary_strict"},
    {"guard_id": "invalid_l_future_output_not_candidate_only", "go_key": "future_output_candidate_only", "depends_on": "future_output_candidate_only"},
    {"guard_id": "invalid_m_runtime_output_semantic_in_future_trial", "go_key": "future_trial_no_runtime_semantic", "depends_on": "future_trial_no_runtime_semantic"},
    {"guard_id": "invalid_n_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_o_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_p_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (37 phase + 6 test board = 43).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_load_registry_patch_and_inference_trial_readiness_planning_only",
    "scope_is_mobile_sam_only",
    "upstream_model_load_retry_must_be_go",
    "upstream_boundary_must_be_clean",
    "registry_mutation_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "image_input_is_not_allowed",
    "segmentation_is_not_allowed",
    "prediction_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "fact_write_is_not_allowed",
    "navigation_action_speech_is_not_allowed",
    "additional_download_is_not_allowed",
    "registry_patch_planning_must_not_set_inference_ready_true",
    "registry_patch_planning_must_not_set_runtime_ready_true",
    "registry_patch_planning_must_not_set_output_adapter_ready_true",
    "registry_patch_planning_must_not_set_semantic_layer_ready_true",
    "commercial_runtime_is_not_approved",
    "inference_trial_request_planning_is_not_inference_execution_approval",
    "future_image_input_must_be_local_test_asset_only",
    "future_image_input_must_have_manifest",
    "future_image_input_must_not_contain_personal_data",
    "future_inference_output_must_be_candidate_only",
    "future_inference_output_must_not_enter_fact_layer",
    "future_inference_output_must_not_enter_runtime",
    "future_inference_output_must_not_enter_output_adapter",
    "future_inference_output_must_not_enter_semantic_layer",
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
    "mobile_sam_model_load_success_audit_record",
    "mobile_sam_model_load_registry_patch_plan_record",
    "mobile_sam_inference_trial_request_plan_record",
    "mobile_sam_inference_owner_approval_plan_record",
    "mobile_sam_image_input_boundary_plan_record",
    "mobile_sam_inference_command_whitelist_plan_record",
    "mobile_sam_inference_memory_timeout_boundary_record",
    "mobile_sam_inference_rollback_cleanup_plan_record",
    "mobile_sam_inference_readiness_review_record",
    "mobile_sam_followup_registry_patch_execution_route_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningProfile",
    "MobileSAMModelLoadSuccessAudit",
    "MobileSAMModelLoadRegistryPatchPlanningRecord",
    "MobileSAMInferenceTrialRequestPlanningRecord",
    "MobileSAMInferenceOwnerApprovalPlanningRecord",
    "MobileSAMImageInputBoundaryPlanningRecord",
    "MobileSAMInferenceCommandWhitelistPlanningRecord",
    "MobileSAMInferenceMemoryTimeoutBoundaryRecord",
    "MobileSAMInferenceRollbackCleanupPlanningRecord",
    "MobileSAMInferenceReadinessReview",
    "MobileSAMFollowupRegistryPatchExecutionRoute",
    "NegativeMobileSAMModelLoadRegistryPatchInferenceReadinessPlanningGuard",
    "P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningDecision",
)

FINAL_DECISION_GO = (
    "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_AND_INFERENCE_TRIAL_READINESS_PLANNING_GO"
)
FINAL_DECISION_BLOCKED = (
    "P1_MOBILE_SAM_MODEL_LOAD_REGISTRY_PATCH_AND_INFERENCE_TRIAL_READINESS_PLANNING_BLOCKED"
)

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "model_load_retry_evidence_locked_and_reused": True,
}

MEMORY_LIMIT_MB = 4096
TIMEOUT_SECONDS = 300


@dataclass(frozen=True)
class P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    mobile_sam_only: bool
    model_load_registry_patch_planning: bool
    inference_trial_request_planning: bool
    inference_trial_readiness_planning: bool
    registry_mutation_allowed: bool
    registry_file_write_allowed: bool
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
    upstream_model_load_retry_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMModelLoadSuccessAudit:
    audit_id: str
    upstream_review_file_ref: str
    final_decision_ok: bool
    blocker_count_ok: bool
    negative_guard_ok: bool
    import_success: bool
    dependency_gap_resolved: bool
    checkpoint_load_success: bool
    model_load_retry_success: bool
    model_type_name: str
    size_matches: bool
    sha256_matches: bool
    timm_find_spec_verified: bool
    mobile_sam_find_spec_verified: bool
    torch_observed_during_load: bool
    torch_version_observed: str
    torchvision_observed_during_load: bool
    torchvision_version_observed: str
    peak_memory_mb: float
    elapsed_seconds: float
    no_image_input: bool
    no_segmentation: bool
    no_prediction: bool
    no_inference: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_registry_mutation: bool
    no_extra_download: bool
    registry_mutation_performed: bool
    real_import_performed: bool
    model_load_performed: bool
    inference_performed: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRegistryPatchPlanningRecord:
    record_id: str
    registry_overlay_ref: str
    patch_is_plan_only: bool
    patch_is_not_registry_mutation: bool
    planned_patch_values: Dict[str, Any]
    planned_readiness_level: str
    planned_inference_ready: bool
    planned_runtime_ready: bool
    planned_output_adapter_ready: bool
    planned_semantic_layer_ready: bool
    planned_commercial_runtime_approved: bool


@dataclass(frozen=True)
class MobileSAMInferenceTrialRequestPlanningRecord:
    request_id: str
    asset_id: str
    request_scope: str
    inference_trial_requested: bool
    inference_execution_requested_later: bool
    image_input_required_for_future_trial: bool
    segmentation_or_prediction_required_for_future_trial: bool
    request_is_not_inference_execution: bool
    request_is_not_runtime_approval: bool
    request_is_not_output_adapter_approval: bool
    request_is_not_semantic_layer_approval: bool
    request_is_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class MobileSAMInferenceOwnerApprovalPlanningRecord:
    record_id: str
    owner_approval_required_for_inference_trial: bool
    owner_approval_granted_now: bool
    inference_trial_execution_requires_separate_request_or_issuance: bool
    inference_trial_execution_requires_separate_phase: bool
    runtime_approved: bool
    output_adapter_approved: bool
    semantic_layer_approved: bool
    commercial_runtime_approved: bool
    fact_write_approved: bool
    navigation_action_speech_approved: bool


@dataclass(frozen=True)
class MobileSAMImageInputBoundaryPlanningRecord:
    record_id: str
    allowed_candidates: Tuple[str, ...]
    forbidden_sources: Tuple[str, ...]
    image_input_must_be_local: bool
    image_input_must_be_test_asset: bool
    image_input_must_have_manifest: bool
    image_input_must_not_contain_personal_data: bool
    image_input_must_not_enter_fact_layer: bool
    image_input_must_not_enter_navigation_runtime: bool


@dataclass(frozen=True)
class MobileSAMInferenceCommandWhitelistPlanningRecord:
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
class MobileSAMInferenceRollbackCleanupPlanningRecord:
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
    can_enter_model_load_registry_patch_execution_next: bool
    can_enter_inference_trial_request_approval_next: bool
    can_enter_inference_execution_now: bool
    inference_execution_requires_registry_patch_go: bool
    inference_execution_requires_owner_approval: bool
    inference_execution_requires_test_image_manifest: bool
    inference_execution_requires_candidate_output_boundary: bool
    inference_success_not_runtime_approval: bool
    inference_success_not_output_adapter_approval: bool
    inference_success_not_semantic_layer_approval: bool


@dataclass(frozen=True)
class MobileSAMFollowupRegistryPatchExecutionRoute:
    route_id: str
    recommended_next_phase: str
    subsequent_inference_trial_phase: str
    next_phase_scope: str
    next_phase_allows_registry_overlay_write: bool
    next_phase_still_no_inference: bool


@dataclass
class NegativeMobileSAMModelLoadRegistryPatchInferenceReadinessPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadRegistryPatchInferenceReadinessPlanningDecision:
    decision_ref: str
    mobile_sam_model_load_registry_patch_inference_readiness_planning_profile_count: int
    mobile_sam_model_load_success_audit_count: int
    mobile_sam_model_load_registry_patch_plan_record_count: int
    mobile_sam_inference_trial_request_plan_record_count: int
    mobile_sam_inference_owner_approval_plan_record_count: int
    mobile_sam_image_input_boundary_plan_record_count: int
    mobile_sam_inference_command_whitelist_plan_record_count: int
    mobile_sam_inference_memory_timeout_boundary_count: int
    mobile_sam_inference_rollback_cleanup_plan_count: int
    mobile_sam_inference_readiness_review_count: int
    mobile_sam_followup_registry_patch_execution_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    registry_patch_planned: bool
    planned_readiness_level: str
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
