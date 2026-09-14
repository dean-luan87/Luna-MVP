# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair NoDeps Install Request, Approval And Readiness — types v1
(COMPRESSED PLANNING / APPROVAL ONLY, scope = mobile_sam_only, target = timm, route = no-deps).

Prepares the NEXT controlled no-deps timm install (Route A) after the full isolated install
timeout failure. It produces a no-deps route audit, a timm no-deps install request, a NARROW
owner approval (no-deps install preparation + execution-next only), a torch/torchvision reuse
boundary record, a TEMPLATE-ONLY `--no-deps` command whitelist (never executed; no global
install; no transitive deps; find_spec-only post-install probe), a rollback plan, a readiness
review, and a model-load retry gate. It does NOT pip install / install timm / real import
torch/torchvision/mobile_sam / model load / retry / inference / runtime / output adapter /
semantic promotion / registry mutation / extra downloads. no-deps approval is NOT install
execution now, NOT model-load-retry / inference / runtime / commercial-runtime approval.
Protected, non-deletable test board records are written in `planning` mode.
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

PHASE_ID = "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Request-Approval-And-Readiness-v1-001"
SCOPE = "p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness"
WEIGHT_CHAIN = "p1_mobile_sam_dependency_repair_nodeps_install_request_approval_and_readiness_v1"

REPAIR_PRINCIPLE_ZH = (
    "压缩规划/审批，scope=mobile_sam_only，target=timm，route=timm_no_deps_controlled_install。"
    "为下一次受控 no-deps timm 安装做准备：no-deps route audit、timm no-deps install request、"
    "窄范围 owner approval（仅 no-deps install preparation + execution-next）、torch/torchvision "
    "复用边界、TEMPLATE-ONLY --no-deps command whitelist（不执行、不全局安装、不拉传递依赖、"
    "find_spec-only 探针）、rollback plan、readiness review、model-load retry gate。不 pip install、"
    "不装 timm、不真实 import torch/torchvision/mobile_sam、不 model load、不 retry、不 inference、"
    "不 runtime、不 output adapter、不语义层、不改 registry、不额外下载。no-deps 批准 ≠ 立即执行安装 ≠ "
    "model-load retry / inference / runtime / 商业 runtime 批准。测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "nodeps_timm_install_request_approval_readiness_only_reuse_torch_no_transitive_deps_no_install_now"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
MOBILE_SAM_ONLY = True
TARGET_DEPENDENCY = "timm"
SELECTED_ROUTE = "timm_no_deps_controlled_install"
NODEPS_INSTALL_REQUEST_INCLUDED = True
NODEPS_OWNER_APPROVAL_ISSUANCE_INCLUDED = True
NODEPS_INSTALL_READINESS_REVIEW_INCLUDED = True
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

UPSTREAM_FAILURE_REPAIR_PLANNING_REF = (
    "Phase-P1-MobileSAM-Dependency-Repair-Install-Failure-Review-And-Repair-Planning-v1-001"
)
UPSTREAM_FAILURE_REPAIR_PLANNING_EXPECTED_GO = (
    "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_OUTPUT_DIR_REL = (
    "_tmp_eval_out/p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1_smoke_v0"
)
UPSTREAM_REVIEW_FILE = (
    "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_review_v1.json"
)

CONTROLLED_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"
FALLBACK_TORCH_VERSION = "2.8.0"
EXPECTED_FAILURE_CATEGORY = "dependency_install_timeout"

NEXT_PHASE_NODEPS_INSTALL_EXECUTION = (
    "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Execution-And-Post-Review-v1-001"
)
SUGGESTED_RETRY_PHASE = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

MOBILE_SAM_ASSET_ID = "mobile_sam"
TIMM_PACKAGE_NAME = "timm"
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_no_deps_route", "go_key": "upstream_no_deps_route_selected", "depends_on": "upstream_no_deps_route_selected"},
    {"guard_id": "invalid_b_pip_install_or_timm_install_executed", "go_key": "no_install_executed", "depends_on": "no_install_executed"},
    {"guard_id": "invalid_c_real_import_timm_torch_torchvision_mobile_sam", "go_key": "no_real_import", "depends_on": "no_real_import"},
    {"guard_id": "invalid_d_model_load_or_retry", "go_key": "no_model_load_retry", "depends_on": "no_model_load_retry"},
    {"guard_id": "invalid_e_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_f_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_h_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_i_command_whitelist_missing_no_deps", "go_key": "whitelist_has_no_deps_flag", "depends_on": "whitelist_has_no_deps_flag"},
    {"guard_id": "invalid_j_command_whitelist_allows_global_install", "go_key": "whitelist_no_global_install", "depends_on": "whitelist_no_global_install"},
    {"guard_id": "invalid_k_torch_torchvision_reuse_boundary_missing", "go_key": "torch_torchvision_reuse_boundary_present", "depends_on": "torch_torchvision_reuse_boundary_present"},
    {"guard_id": "invalid_l_nodeps_approval_treated_as_install_execution_now", "go_key": "nodeps_approval_not_install_execution_now", "depends_on": "nodeps_approval_not_install_execution_now"},
    {"guard_id": "invalid_m_nodeps_approval_treated_as_model_load_retry_approval", "go_key": "nodeps_approval_not_model_load_retry_approval", "depends_on": "nodeps_approval_not_model_load_retry_approval"},
    {"guard_id": "invalid_n_nodeps_approval_treated_as_inference_runtime_approval", "go_key": "nodeps_approval_not_inference_runtime_approval", "depends_on": "nodeps_approval_not_inference_runtime_approval"},
    {"guard_id": "invalid_o_rollback_plan_missing", "go_key": "rollback_plan_present", "depends_on": "rollback_plan_present"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (31 phase + 1 cleanup + 6 test board = 38).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_nodeps_timm_install_request_approval_and_readiness_only",
    "scope_is_mobile_sam_only",
    "target_dependency_is_timm",
    "selected_route_must_be_timm_no_deps_controlled_install",
    "pip_install_is_not_allowed_in_this_phase",
    "timm_install_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed",
    "torch_torchvision_import_is_not_allowed",
    "mobile_sam_import_is_not_allowed",
    "model_load_is_not_allowed",
    "model_load_retry_is_not_allowed",
    "inference_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "command_whitelist_must_include_no_deps",
    "global_install_is_not_allowed",
    "transitive_dependency_install_is_not_allowed_by_route",
    "torch_reuse_does_not_allow_torch_reinstall",
    "torchvision_reuse_boundary_is_required",
    "nodeps_approval_is_not_install_execution_now",
    "nodeps_approval_is_not_model_load_retry_approval",
    "nodeps_approval_is_not_inference_approval",
    "nodeps_approval_is_not_runtime_approval",
    "commercial_runtime_is_not_approved",
    "rollback_plan_is_required",
    "post_install_find_spec_probe_is_required",
    "candidate_only_boundary_is_preserved",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    PHASE_GOVERNANCE_RULES + ("cleanup_must_not_delete_test_board_artifacts",) + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "timm_nodeps_route_audit_record",
    "timm_nodeps_install_request_record",
    "timm_nodeps_owner_approval_issuance_record",
    "timm_torch_torchvision_reuse_boundary_record",
    "timm_nodeps_command_whitelist_record",
    "timm_nodeps_probe_plan_record",
    "timm_nodeps_rollback_plan_record",
    "timm_nodeps_install_readiness_review_record",
    "mobile_sam_model_load_retry_gate_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessProfile",
    "TimmNoDepsRouteAudit",
    "TimmNoDepsInstallRequestRecord",
    "TimmNoDepsOwnerApprovalIssuanceRecord",
    "TimmTorchTorchvisionReuseBoundaryRecord",
    "TimmNoDepsCommandWhitelistRecord",
    "TimmNoDepsProbePlanRecord",
    "TimmNoDepsRollbackPlanRecord",
    "TimmNoDepsInstallReadinessReview",
    "MobileSAMModelLoadRetryGateAfterNoDepsTimm",
    "NegativeTimmNoDepsInstallRequestApprovalGuard",
    "P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_REQUEST_APPROVAL_AND_READINESS_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_REQUEST_APPROVAL_AND_READINESS_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "upstream_failure_repair_planning_reused": True,
    "torch_torchvision_reuse_boundary_planned": True,
}


@dataclass(frozen=True)
class P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    mobile_sam_only: bool
    target_dependency: str
    selected_route: str
    nodeps_install_request_included: bool
    nodeps_owner_approval_issuance_included: bool
    nodeps_install_readiness_review_included: bool
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
class TimmNoDepsRouteAudit:
    audit_id: str
    upstream_review_file_ref: str
    upstream_review_exists: bool
    final_decision_observed: str
    final_decision_ok: bool
    blocker_count_observed: int
    failure_category_observed: str
    selected_route_observed: str
    same_full_isolated_install_retry_not_recommended_observed: bool
    model_load_retry_allowed_now_observed: bool
    no_deps_install_missing_transitive_dependency_risk_recorded: bool
    torch_timm_compatibility_risk_recorded: bool
    route_a_selected: bool
    audit_passed: bool


@dataclass(frozen=True)
class TimmNoDepsInstallRequestRecord:
    request_id: str
    asset_id: str
    target_dependency: str
    request_scope: str
    selected_route: str
    install_execution_requested_next: bool
    command_strategy: str
    controlled_install_scope: str
    global_install_requested: bool
    request_is_not_install_execution: bool
    request_is_not_model_load_retry: bool
    request_is_not_inference_approval: bool
    request_is_not_runtime_approval: bool


@dataclass(frozen=True)
class TimmNoDepsOwnerApprovalIssuanceRecord:
    approval_id: str
    owner_approval_granted_for_timm_nodeps_install_preparation: bool
    owner_approval_granted_for_timm_nodeps_install_execution_next: bool
    model_load_retry_not_approved: bool
    inference_not_approved: bool
    runtime_not_approved: bool
    output_adapter_not_approved: bool
    semantic_layer_not_approved: bool
    registry_mutation_not_approved: bool
    additional_weight_download_not_approved: bool
    commercial_runtime_not_approved: bool
    nodeps_install_approval_not_install_execution_now: bool
    nodeps_install_approval_not_model_load_retry_approval: bool
    nodeps_install_approval_not_inference_approval: bool
    nodeps_install_approval_not_runtime_approval: bool


@dataclass(frozen=True)
class TimmTorchTorchvisionReuseBoundaryRecord:
    record_id: str
    existing_torch_reuse_allowed: bool
    existing_torch_version_expected: str
    existing_torch_reuse_does_not_allow_global_mutation: bool
    existing_torch_reuse_does_not_allow_reinstall: bool
    existing_torch_reinstall_allowed: bool
    torchvision_status_check_required_before_execution: bool
    torchvision_reinstall_allowed: bool
    torch_compatibility_must_be_observed_after_model_load_retry: bool
    if_torchvision_missing_then_enter_dependency_repair_loop: bool
    torchvision_observed_available: bool
    torchvision_observed_version: str


@dataclass(frozen=True)
class TimmNoDepsCommandWhitelistRecord:
    record_id: str
    command_template: str
    command_template_only: bool
    command_not_executed: bool
    no_deps_flag_required: bool
    no_global_install: bool
    no_transitive_dependency_install: bool
    no_model_load_during_install: bool
    no_import_during_install: bool
    no_inference_during_install: bool
    no_runtime_during_install: bool
    no_registry_mutation_during_install: bool


@dataclass(frozen=True)
class TimmNoDepsProbePlanRecord:
    record_id: str
    post_install_probe_required: bool
    probe_method: str
    probe_target: str
    real_import_after_install_allowed: bool
    model_load_after_install_allowed: bool
    timm_find_spec_required_before_model_load_retry: bool


@dataclass(frozen=True)
class TimmNoDepsRollbackPlanRecord:
    record_id: str
    pre_install_snapshot_required: bool
    rollback_required: bool
    rollback_removes_timm_if_failed: bool
    rollback_preserves_mobile_sam_code: bool
    rollback_preserves_mobile_sam_weight_file: bool
    rollback_preserves_registry: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    global_env_contamination_check_required: bool
    controlled_target_cleanup_required_on_failure: bool


@dataclass(frozen=True)
class TimmNoDepsInstallReadinessReview:
    review_id: str
    can_enter_timm_nodeps_install_execution_next: bool
    timm_nodeps_install_execution_scope: str
    can_enter_model_load_retry_after_this_phase: bool
    model_load_retry_requires_nodeps_timm_install_go: bool
    model_load_retry_requires_timm_find_spec_verified: bool
    model_load_retry_requires_mobile_sam_weight_sha256_recheck: bool
    model_load_retry_requires_code_and_weight_ready_still_valid: bool
    model_load_retry_requires_torch_torchvision_reuse_boundary_check: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRetryGateAfterNoDepsTimm:
    record_id: str
    model_load_retry_allowed_now: bool
    requires_nodeps_timm_install_request_go: bool
    requires_nodeps_owner_approval_granted: bool
    requires_nodeps_timm_install_execution_go: bool
    requires_timm_find_spec_verified: bool
    requires_no_global_env_contamination: bool
    requires_sha256_recheck: bool
    requires_code_and_weight_ready_still_valid: bool
    requires_torch_torchvision_reuse_boundary_check: bool
    suggested_retry_phase: str


@dataclass
class NegativeTimmNoDepsInstallRequestApprovalGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMNoDepsTimmInstallRequestApprovalReadinessDecision:
    decision_ref: str
    mobile_sam_nodeps_timm_install_request_approval_readiness_profile_count: int
    timm_nodeps_route_audit_count: int
    timm_nodeps_install_request_record_count: int
    timm_nodeps_owner_approval_issuance_record_count: int
    timm_torch_torchvision_reuse_boundary_record_count: int
    timm_nodeps_command_whitelist_record_count: int
    timm_nodeps_probe_plan_record_count: int
    timm_nodeps_rollback_plan_record_count: int
    timm_nodeps_install_readiness_review_count: int
    mobile_sam_model_load_retry_gate_after_nodeps_timm_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
