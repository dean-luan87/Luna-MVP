# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Request, Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only, target = timm).

Prepares the NEXT controlled dependency-repair install for the `timm` gap exposed by the
MobileSAM model-load trial. It produces a timm install request, a package/version review,
a license/dependency review, a torch-compatibility review, a NARROW owner approval
(install preparation + execution-next only), a TEMPLATE-ONLY install command whitelist
(never executed; no global install; find_spec-only post-install probe), a rollback plan,
a readiness review, and a model-load retry gate. It does NOT pip install / install timm /
install any dependency, does NOT real import / model load / retry / inference / runtime /
output adapter / semantic promotion, does NOT mutate the registry, and downloads NOTHING
extra. Version pins and license/dependency reviews must NOT be fabricated. timm install
approval is NOT model-load-retry / inference / runtime / commercial-runtime approval.
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

PHASE_ID = "Phase-P1-MobileSAM-Dependency-Repair-Install-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_dependency_repair_install_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_dependency_repair_install_request_approval_and_readiness_v1"

REPAIR_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only，target=timm。为下一次受控依赖修复安装做准备：timm install request、package/version "
    "review、license/dependency review、torch 兼容性 review、窄范围 owner approval（仅 install preparation + execution-next）、"
    "TEMPLATE-ONLY install command whitelist（不执行、不全局安装、find_spec-only 探针）、rollback plan、readiness review、"
    "model-load retry gate。不 pip install、不装 timm、不装任何依赖、不真实 import、不 model load、不 retry、不 inference、"
    "不 runtime、不 output adapter、不语义层、不改 registry、不额外下载。version pin 与 license/dependency review 不得伪造。"
    "timm 安装批准 ≠ model-load retry / inference / runtime / 商业 runtime 批准。测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "dependency_repair_request_approval_readiness_only_no_install_no_load_install_approval_is_not_model_load_retry"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
MOBILE_SAM_ONLY = True
DEPENDENCY_REPAIR_REQUEST_INCLUDED = True
DEPENDENCY_REPAIR_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
DEPENDENCY_REPAIR_READINESS_REVIEW_INCLUDED = True
TARGET_DEPENDENCY = "timm"
DEPENDENCY_INSTALL_EXECUTION_ALLOWED = False
PIP_INSTALL_ALLOWED = False
TIMM_INSTALL_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
MODEL_LOAD_RETRY_ALLOWED = False
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

UPSTREAM_FAILURE_REPAIR_PLANNING_REF = "Phase-P1-MobileSAM-Model-Load-Failure-Review-And-Repair-Planning-v1-001"
UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO = "P1_MOBILE_SAM_MODEL_LOAD_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Upstream failure-repair-planning artifact (read for dependency-gap evidence).
UPSTREAM_OUTPUT_DIR_REL = "_tmp_eval_out/p1_mobile_sam_model_load_failure_review_and_repair_planning_v1_smoke_v0"
UPSTREAM_REVIEW_FILE = "p1_mobile_sam_model_load_failure_review_and_repair_planning_review_v1.json"

# Follow-up phases.
NEXT_PHASE_INSTALL_EXECUTION = "Phase-P1-MobileSAM-Dependency-Repair-Install-Execution-And-Post-Review-v1-001"
SUGGESTED_RETRY_PHASE = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Failure / dependency facts (carried from upstream).
# --------------------------------------------------------------------------- #
MOBILE_SAM_ASSET_ID = "mobile_sam"
EXPECTED_FAILURE_CATEGORY = "dependency_gap"
EXPECTED_MISSING_DEPENDENCY = "timm"
EXPECTED_ERROR_CLASS = "ModuleNotFoundError"
CONTROLLED_INSTALL_SCOPE = "controlled_model_load_env"
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
FALLBACK_TORCH_VERSION = "2.8.0"

# --------------------------------------------------------------------------- #
# Negative guards (17: Invalid A..Q).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_dependency_gap_timm_but_approval", "go_key": "upstream_dependency_gap_timm", "depends_on": "upstream_dependency_gap_timm"},
    {"guard_id": "invalid_b_pip_install_or_timm_install_executed", "go_key": "no_install_executed", "depends_on": "no_install_executed"},
    {"guard_id": "invalid_c_real_import_timm_or_mobile_sam", "go_key": "no_real_import", "depends_on": "no_real_import"},
    {"guard_id": "invalid_d_model_load_or_retry", "go_key": "no_model_load_retry", "depends_on": "no_model_load_retry"},
    {"guard_id": "invalid_e_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_f_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_version_unresolved_but_marked_pinned", "go_key": "version_not_falsely_pinned", "depends_on": "version_not_falsely_pinned"},
    {"guard_id": "invalid_j_review_not_done_but_marked_completed", "go_key": "reviews_not_falsely_completed", "depends_on": "reviews_not_falsely_completed"},
    {"guard_id": "invalid_k_install_approval_treated_as_model_load_retry_approval", "go_key": "approval_not_model_load_retry", "depends_on": "approval_not_model_load_retry"},
    {"guard_id": "invalid_l_install_approval_treated_as_inference_runtime_approval", "go_key": "approval_not_inference_runtime", "depends_on": "approval_not_inference_runtime"},
    {"guard_id": "invalid_m_command_whitelist_missing_or_executed", "go_key": "command_template_only_not_executed", "depends_on": "command_template_only_not_executed"},
    {"guard_id": "invalid_n_rollback_plan_missing", "go_key": "rollback_plan_present", "depends_on": "rollback_plan_present"},
    {"guard_id": "invalid_o_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (33 phase + 6 test board = 39).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_dependency_repair_install_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "target_dependency_is_timm",
    "upstream_failure_must_be_dependency_gap_timm",
    "pip_install_is_not_allowed_in_this_phase",
    "timm_install_is_not_allowed_in_this_phase",
    "dependency_install_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "model_load_retry_is_not_allowed",
    "inference_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "version_pin_must_not_be_fabricated",
    "license_dependency_review_must_not_be_fabricated",
    "timm_install_approval_is_not_model_load_retry_approval",
    "timm_install_approval_is_not_inference_approval",
    "timm_install_approval_is_not_runtime_approval",
    "commercial_runtime_is_not_approved",
    "install_command_whitelist_is_template_only",
    "rollback_plan_is_required",
    "post_install_find_spec_probe_is_required",
    "candidate_only_boundary_is_preserved",
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
    "timm_dependency_gap_audit_record",
    "timm_install_request_record",
    "timm_owner_approval_issuance_record",
    "timm_package_version_review_record",
    "timm_torch_compatibility_review_record",
    "timm_install_command_whitelist_record",
    "timm_rollback_plan_record",
    "timm_install_readiness_review_record",
    "mobile_sam_model_load_retry_gate_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMDependencyRepairInstallRequestApprovalReadinessProfile",
    "MobileSAMTimmDependencyGapAudit",
    "TimmInstallRequestRecord",
    "TimmOwnerApprovalIssuanceRecord",
    "TimmPackageVersionReviewRecord",
    "TimmLicenseDependencyReviewRecord",
    "TimmTorchCompatibilityReviewRecord",
    "TimmInstallCommandWhitelistRecord",
    "TimmRollbackPlanRecord",
    "TimmInstallReadinessReview",
    "MobileSAMModelLoadRetryGateAfterDependencyRepair",
    "NegativeTimmDependencyRepairRequestApprovalGuard",
    "P1MobileSAMDependencyRepairInstallRequestApprovalReadinessDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "upstream_failure_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMDependencyRepairInstallRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    mobile_sam_only: bool
    dependency_repair_request_included: bool
    dependency_repair_owner_approval_issuance_included: bool
    dependency_repair_readiness_review_included: bool
    target_dependency: str
    dependency_install_execution_allowed: bool
    pip_install_allowed: bool
    timm_install_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    model_load_retry_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_failure_repair_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMTimmDependencyGapAudit:
    audit_id: str
    upstream_review_file_ref: str
    upstream_review_exists: bool
    final_decision_observed: str
    final_decision_ok: bool
    blocker_count_observed: int
    failure_category_observed: str
    missing_dependency_observed: str
    error_class_observed: str
    weight_integrity_related_observed: bool
    checkpoint_corruption_related_observed: bool
    environment_dependency_related_observed: bool
    timm_package_install_required_observed: bool
    timm_install_requires_separate_request_observed: bool
    model_load_retry_allowed_now_observed: bool
    audit_passed: bool


@dataclass(frozen=True)
class TimmInstallRequestRecord:
    request_id: str
    asset_id: str
    target_dependency: str
    dependency_role: str
    request_scope: str
    install_execution_requested_next: bool
    controlled_install_scope: str
    global_install_requested: bool
    request_is_not_install_execution: bool
    request_is_not_model_load_retry: bool
    request_is_not_inference_approval: bool
    request_is_not_runtime_approval: bool


@dataclass(frozen=True)
class TimmOwnerApprovalIssuanceRecord:
    approval_id: str
    owner_approval_granted_for_timm_install_preparation: bool
    owner_approval_granted_for_timm_install_execution_next: bool
    model_load_retry_not_approved: bool
    inference_not_approved: bool
    runtime_not_approved: bool
    output_adapter_not_approved: bool
    semantic_layer_not_approved: bool
    registry_mutation_not_approved: bool
    additional_weight_download_not_approved: bool
    commercial_runtime_not_approved: bool
    timm_install_approval_not_model_load_retry_approval: bool
    timm_install_approval_not_inference_approval: bool
    timm_install_approval_not_runtime_approval: bool
    timm_install_approval_not_commercial_runtime_approval: bool


@dataclass(frozen=True)
class TimmPackageVersionReviewRecord:
    record_id: str
    package_name_candidate: str
    import_root_candidate: str
    clean_pypi_candidate: bool
    version_status: str
    version_resolution_required: bool
    version_pin_required: bool
    version_pinned_value: str
    version_falsely_pinned: bool
    package_source_review_required: bool
    hash_or_lockfile_recommended: bool
    dependency_conflict_review_required: bool
    transitive_dependency_review_required: bool
    license_review_required: bool
    local_available_candidate: bool


@dataclass(frozen=True)
class TimmLicenseDependencyReviewRecord:
    record_id: str
    license_review_required: bool
    license_review_status: str
    license_candidate: str
    dependency_review_required: bool
    dependency_review_status: str
    transitive_dependency_review_status: str
    review_falsely_marked_completed: bool


@dataclass(frozen=True)
class TimmTorchCompatibilityReviewRecord:
    record_id: str
    current_torch_available: bool
    current_torch_version_observed: str
    torch_compatibility_review_required: bool
    timm_torch_compatibility_status: str
    compatibility_must_be_validated_after_install: bool
    compatibility_failure_blocks_model_load_retry: bool


@dataclass(frozen=True)
class TimmInstallCommandWhitelistRecord:
    record_id: str
    install_target: str
    package: str
    version_pin_required: bool
    no_global_install: bool
    no_model_load_during_install: bool
    no_import_during_install: bool
    no_inference_during_install: bool
    no_runtime_during_install: bool
    command_template: str
    command_template_only: bool
    command_not_executed: bool
    command_template_success_not_install_execution: bool
    install_execution_requires_separate_phase: bool
    post_install_probe_required: bool
    probe_method: str
    probe_target: str
    real_import_after_install_allowed: bool
    model_load_after_install_allowed: bool
    timm_find_spec_required_before_model_load_retry: bool


@dataclass(frozen=True)
class TimmRollbackPlanRecord:
    record_id: str
    pre_install_snapshot_required: bool
    rollback_required: bool
    rollback_removes_timm_if_failed: bool
    rollback_preserves_mobile_sam_code: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_registry: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    global_env_contamination_check_required: bool


@dataclass(frozen=True)
class TimmInstallReadinessReview:
    review_id: str
    can_enter_timm_install_execution_next: bool
    timm_install_execution_scope: str
    can_enter_model_load_retry_after_this_phase: bool
    model_load_retry_requires_timm_install_execution_go: bool
    model_load_retry_requires_timm_find_spec_verified: bool
    model_load_retry_requires_sha256_recheck: bool
    model_load_retry_requires_code_and_weight_ready_still_valid: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRetryGateAfterDependencyRepair:
    record_id: str
    model_load_retry_allowed_now: bool
    requires_timm_install_request_go: bool
    requires_timm_owner_approval_granted: bool
    requires_timm_install_execution_go: bool
    requires_timm_find_spec_verified: bool
    requires_no_global_env_contamination: bool
    requires_sha256_recheck: bool
    requires_code_and_weight_ready_still_valid: bool
    requires_model_load_retry_command_whitelist_updated: bool
    requires_test_board_ready: bool
    suggested_retry_phase: str


@dataclass
class NegativeTimmDependencyRepairRequestApprovalGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMDependencyRepairInstallRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_dependency_repair_install_request_approval_readiness_profile_count: int
    mobile_sam_timm_dependency_gap_audit_count: int
    timm_install_request_record_count: int
    timm_owner_approval_issuance_record_count: int
    timm_package_version_review_record_count: int
    timm_license_dependency_review_record_count: int
    timm_torch_compatibility_review_record_count: int
    timm_install_command_whitelist_record_count: int
    timm_rollback_plan_record_count: int
    timm_install_readiness_review_count: int
    mobile_sam_model_load_retry_gate_after_dependency_repair_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
