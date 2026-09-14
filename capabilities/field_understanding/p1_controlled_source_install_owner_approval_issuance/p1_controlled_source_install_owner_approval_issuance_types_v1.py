# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Owner Approval Issuance — types v1.

APPROVAL ISSUANCE ONLY for the two honestly-deferred assets byte_track and
mobile_sam.

It MAY generate a source-install owner approval issuance record, but the
approval scope is limited to "allowed to enter the subsequent controlled source
install preparation / readiness chain". It executes NOTHING and MUTATES NOTHING:
no git clone, no source checkout, no source install, no pip install, no
dependency install, no model/weight/dataset download, no real import, no model
load, no inference, no runtime, no output adapter, no semantic layer, NO registry
mutation.

Approval Issuance != Git Clone. Approval Issuance != Source Install. Approval
Issuance != Weight Download. Both assets REMAIN DEFERRED. Protected,
non-deletable test board records are written in planning mode.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
SCOPE = "p1_controlled_source_install_owner_approval_issuance"
SOURCE_CHAIN = "p1_controlled_source_install_owner_approval_issuance_v1"

PLANNING_PRINCIPLE_ZH = (
    "为 byte_track 与 mobile_sam 源码安装请求生成 owner approval issuance。可生成源码安装审批发行记录，但审批范围仅限"
    "“允许进入后续 controlled source install preparation / readiness chain”。不 git clone、不 source checkout、不源码"
    "安装、不 pip install、不安装依赖、不下载模型/权重/数据集、不真实 import / model load / inference、不进入 runtime "
    "/ output adapter / 语义层、不修改 registry。Approval Issuance ≠ Git Clone ≠ Source Install ≠ Weight Download；"
    "byte_track 与 mobile_sam 保持 DEFERRED。审批附带 expiry、revocation、source chain traceability，以及 repository "
    "验证 / commit pin / license / dependency expansion / network boundary / weight 独立审批等前置条件。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_install_owner_approval_issuance_is_preparation_scope_only_no_clone_no_install_no_weight_download"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
APPROVAL_ISSUANCE_ONLY = True
SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_CREATED = True
OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL_PREPARATION = True
OWNER_APPROVAL_GRANTED_FOR_GIT_CLONE = False
OWNER_APPROVAL_GRANTED_FOR_SOURCE_CHECKOUT = False
OWNER_APPROVAL_GRANTED_FOR_SOURCE_INSTALL = False
OWNER_APPROVAL_GRANTED_FOR_PIP_INSTALL = False
OWNER_APPROVAL_GRANTED_FOR_DEPENDENCY_INSTALL = False
OWNER_APPROVAL_GRANTED_FOR_MODEL_DOWNLOAD = False
OWNER_APPROVAL_GRANTED_FOR_WEIGHT_DOWNLOAD = False
OWNER_APPROVAL_GRANTED_FOR_DATASET_DOWNLOAD = False
OWNER_APPROVAL_GRANTED_FOR_INFERENCE = False
OWNER_APPROVAL_GRANTED_FOR_RUNTIME = False
OWNER_APPROVAL_GRANTED_FOR_OUTPUT_ADAPTER = False
OWNER_APPROVAL_GRANTED_FOR_SEMANTIC_LAYER = False

REGISTRY_MUTATION_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_CHECKOUT_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REQUEST_PLANNING_REF = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
UPSTREAM_RESOLUTION_PLANNING_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
UPSTREAM_REGISTRY_CORRECTION_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
UPSTREAM_PACKAGE_RESOLUTION_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
UPSTREAM_PROBE_RECONCILIATION_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
UPSTREAM_REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidate (this phase only routes; it does NOT create it).
PREPARATION_AND_READINESS_PHASE_REF = "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001"
NEXT_STEP_REF = PREPARATION_AND_READINESS_PHASE_REF

UPSTREAM_REQUEST_PLANNING_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_REQUEST_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Approved source asset scope (locked) — ONLY the two deferred assets.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}

# Approval conditions (>=12; here 16).
APPROVAL_CONDITIONS: Tuple[str, ...] = (
    "repository_verification_required",
    "repository_commit_pin_required",
    "repository_license_review_required",
    "dependency_expansion_review_required",
    "network_boundary_required",
    "pre_source_install_snapshot_required",
    "command_whitelist_required",
    "isolation_environment_required",
    "rollback_plan_required",
    "post_install_probe_find_spec_only_required",
    "test_board_write_required",
    "weight_download_separate_approval_required",
    "registry_patch_before_runtime_required",
    "owner_revocation_supported",
    "approval_expiry_required",
    "next_phase_required_before_source_execution",
)

# Approval boundary statements (>=8).
APPROVAL_BOUNDARY_STATEMENTS: Tuple[str, ...] = (
    "approval_issuance_success_not_git_clone_approval",
    "approval_issuance_success_not_source_checkout_approval",
    "approval_issuance_success_not_source_install_approval",
    "approval_issuance_success_not_weight_download_approval",
    "approval_issuance_success_not_inference_approval",
    "approval_issuance_success_not_runtime_approval",
    "approval_issuance_success_not_output_adapter_approval",
    "approval_issuance_success_not_semantic_layer_approval",
)

# Traceability refs (>=8; here 9).
TRACEABILITY_REFS: Tuple[Tuple[str, str], ...] = (
    ("source_install_request_ref", UPSTREAM_REQUEST_PLANNING_REF),
    ("source_install_resolution_ref", UPSTREAM_RESOLUTION_PLANNING_REF),
    ("registry_package_correction_planning_ref", UPSTREAM_REGISTRY_CORRECTION_REF),
    ("package_install_execution_post_review_ref", UPSTREAM_POST_REVIEW_REF),
    ("package_install_execution_ref", UPSTREAM_EXECUTION_REF),
    ("registry_probe_reconciliation_ref", UPSTREAM_PROBE_RECONCILIATION_REF),
    ("model_version_dependency_registry_ref", UPSTREAM_REGISTRY_PLANNING_REF),
    ("test_board_ref", "capabilities/test_board/recognition_models"),
    ("approval_issuance_trace_id", "p1_controlled_source_install_owner_approval_issuance_trace_v1"),
)

# Approval expiry policy.
APPROVAL_EXPIRY: Dict[str, Any] = {
    "approval_has_expiry": True,
    "expiry_policy": "single_use_for_preparation_handoff_then_reverify",
    "expired_approval_cannot_be_used": True,
    "approval_use_after_repository_change_blocked": True,
    "approval_use_after_dependency_drift_blocked": True,
    "approval_use_after_license_change_blocked": True,
    "approval_use_after_scope_change_blocked": True,
    "approval_use_after_registry_drift_blocked": True,
}

# Approval revocation policy.
APPROVAL_REVOCATION: Dict[str, Any] = {
    "approval_revocation_supported": True,
    "revocation_reason_required": True,
    "revoked_approval_cannot_be_used": True,
    "revocation_must_be_recorded": True,
    "revocation_record_protected": True,
}

RISK_ACK_DIMENSIONS: Tuple[str, ...] = (
    "dependency_expansion_risk_acknowledged",
    "license_risk_acknowledged",
    "source_setup_side_effect_risk_acknowledged",
    "build_compile_risk_acknowledged",
    "network_access_risk_acknowledged",
    "weight_download_risk_acknowledged",
    "environment_contamination_risk_acknowledged",
    "rollback_complexity_risk_acknowledged",
)

# --------------------------------------------------------------------------- #
# Negative guards (26: Invalid A..Z).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_issuance_as_git_clone_approval", "go_key": "not_git_clone_approval", "depends_on": "not_git_clone_approval"},
    {"guard_id": "invalid_b_issuance_as_source_checkout_approval", "go_key": "not_source_checkout_approval", "depends_on": "not_source_checkout_approval"},
    {"guard_id": "invalid_c_issuance_as_source_install_approval", "go_key": "not_source_install_approval", "depends_on": "not_source_install_approval"},
    {"guard_id": "invalid_d_issuance_as_pip_dependency_install_approval", "go_key": "not_pip_dependency_approval", "depends_on": "not_pip_dependency_approval"},
    {"guard_id": "invalid_e_issuance_as_model_weight_dataset_download_approval", "go_key": "not_download_approval", "depends_on": "not_download_approval"},
    {"guard_id": "invalid_f_issuance_as_inference_approval", "go_key": "not_inference_approval", "depends_on": "not_inference_approval"},
    {"guard_id": "invalid_g_issuance_as_runtime_approval", "go_key": "not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_h_issuance_as_output_adapter_semantic_approval", "go_key": "not_output_semantic_approval", "depends_on": "not_output_semantic_approval"},
    {"guard_id": "invalid_i_approval_scope_contains_other_asset", "go_key": "scope_limited_to_deferred", "depends_on": "scope_limited_to_deferred"},
    {"guard_id": "invalid_j_approval_no_expiry", "go_key": "approval_has_expiry", "depends_on": "approval_has_expiry"},
    {"guard_id": "invalid_k_approval_no_revocation", "go_key": "approval_has_revocation", "depends_on": "approval_has_revocation"},
    {"guard_id": "invalid_l_approval_missing_source_chain_traceability", "go_key": "source_chain_traceable", "depends_on": "source_chain_traceable"},
    {"guard_id": "invalid_m_missing_repository_verification_condition", "go_key": "repo_verification_condition_present", "depends_on": "repo_verification_condition_present"},
    {"guard_id": "invalid_n_missing_dependency_expansion_review_condition", "go_key": "dependency_review_condition_present", "depends_on": "dependency_review_condition_present"},
    {"guard_id": "invalid_o_missing_license_review_condition", "go_key": "license_review_condition_present", "depends_on": "license_review_condition_present"},
    {"guard_id": "invalid_p_missing_network_boundary_condition", "go_key": "network_boundary_condition_present", "depends_on": "network_boundary_condition_present"},
    {"guard_id": "invalid_q_missing_weight_separate_approval_condition", "go_key": "weight_separate_approval_condition_present", "depends_on": "weight_separate_approval_condition_present"},
    {"guard_id": "invalid_r_allows_skip_preparation_direct_execution", "go_key": "preparation_required_before_execution", "depends_on": "preparation_required_before_execution"},
    {"guard_id": "invalid_s_git_clone_checkout_install_pip_executed", "go_key": "no_clone_checkout_install", "depends_on": "no_clone_checkout_install"},
    {"guard_id": "invalid_t_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_u_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_v_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_w_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_x_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_y_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_z_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (50 phase + 6 test board = 56).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_source_install_owner_approval_issuance_only",
    "approval_issuance_is_limited_to_source_install_preparation",
    "approval_issuance_is_not_git_clone_approval",
    "approval_issuance_is_not_source_checkout_approval",
    "approval_issuance_is_not_source_install_approval",
    "approval_issuance_is_not_pip_install_approval",
    "approval_issuance_is_not_dependency_install_approval",
    "approval_issuance_is_not_model_download_approval",
    "approval_issuance_is_not_weight_download_approval",
    "approval_issuance_is_not_dataset_download_approval",
    "approval_issuance_is_not_inference_approval",
    "approval_issuance_is_not_runtime_approval",
    "approval_issuance_is_not_output_adapter_approval",
    "approval_issuance_is_not_semantic_layer_approval",
    "approved_source_scope_is_limited_to_byte_track_and_mobile_sam",
    "repository_verification_is_required_before_source_execution",
    "repository_commit_pin_is_required_before_source_execution",
    "repository_license_review_is_required_before_source_execution",
    "dependency_expansion_review_is_required_before_source_execution",
    "network_boundary_is_required_before_source_execution",
    "weight_download_requires_separate_approval",
    "registry_patch_before_runtime_is_required",
    "approval_expiry_is_required",
    "approval_revocation_is_required",
    "source_chain_traceability_is_required",
    "source_install_preparation_phase_is_required_before_source_execution",
    "direct_source_install_execution_is_not_allowed_after_this_phase",
    "no_git_clone_is_allowed",
    "no_source_checkout_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "commercial_runtime_is_not_approved",
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
    "source_owner_approval_issuance_record",
    "source_approval_scope_record",
    "source_approval_condition_record",
    "source_approval_boundary_record",
    "source_approval_traceability_record",
    "source_weight_exclusion_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallOwnerApprovalIssuanceProfile",
    "SourceOwnerApprovalIssuanceRecord",
    "SourceApprovalScopeRecord",
    "ApprovedSourceAssetScopeRecord",
    "SourceApprovalConditionRecord",
    "SourceApprovalExpiryRecord",
    "SourceApprovalRevocationRecord",
    "SourceApprovalBoundaryRecord",
    "SourceApprovalTraceabilityRecord",
    "SourceRiskAcknowledgementRecord",
    "SourceInstallPreparationHandoffReadiness",
    "NegativeSourceOwnerApprovalIssuanceGuard",
    "P1ControlledSourceInstallOwnerApprovalIssuanceDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallOwnerApprovalIssuanceProfile:
    profile_ref: str
    phase_id: str
    approval_issuance_only: bool
    source_install_owner_approval_issuance_created: bool
    owner_approval_granted_for_source_install_preparation: bool
    owner_approval_granted_for_git_clone: bool
    owner_approval_granted_for_source_checkout: bool
    owner_approval_granted_for_source_install: bool
    owner_approval_granted_for_pip_install: bool
    owner_approval_granted_for_dependency_install: bool
    owner_approval_granted_for_model_download: bool
    owner_approval_granted_for_weight_download: bool
    owner_approval_granted_for_dataset_download: bool
    owner_approval_granted_for_inference: bool
    owner_approval_granted_for_runtime: bool
    owner_approval_granted_for_output_adapter: bool
    owner_approval_granted_for_semantic_layer: bool
    registry_mutation_allowed: bool
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_request_planning_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceOwnerApprovalIssuanceRecord:
    issuance_id: str
    phase_id: str
    source_install_owner_approval_issuance_created: bool
    owner_approval_granted_for_source_install_preparation: bool
    approval_scope: str
    requested_assets: Tuple[str, ...]
    owner_approval_granted_for_git_clone: bool
    owner_approval_granted_for_source_checkout: bool
    owner_approval_granted_for_source_install: bool
    owner_approval_granted_for_weight_download: bool
    owner_approval_granted_for_inference: bool
    owner_approval_granted_for_runtime: bool
    next_phase_ref: str


@dataclass(frozen=True)
class SourceApprovalScopeRecord:
    scope_id: str
    approval_scope: str
    approved_asset_count: int
    scope_limited_to_source_install_preparation: bool
    scope_limited_to_deferred_assets: bool


@dataclass(frozen=True)
class ApprovedSourceAssetScopeRecord:
    asset_id: str
    included_in_approval_scope: bool
    approval_scope: str
    source_install_request_ref: str
    source_resolution_ref: str
    source_family: str
    current_status: str
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    inference_allowed: bool
    runtime_allowed: bool
    output_adapter_allowed: bool
    semantic_layer_allowed: bool
    requires_next_phase_source_install_preparation: bool


@dataclass(frozen=True)
class SourceApprovalConditionRecord:
    condition_id: str
    condition: str
    required: bool
    satisfied_now: bool


@dataclass(frozen=True)
class SourceApprovalExpiryRecord:
    expiry_id: str
    approval_has_expiry: bool
    expiry_policy: str
    expired_approval_cannot_be_used: bool
    approval_use_after_repository_change_blocked: bool
    approval_use_after_dependency_drift_blocked: bool
    approval_use_after_license_change_blocked: bool
    approval_use_after_scope_change_blocked: bool
    approval_use_after_registry_drift_blocked: bool


@dataclass(frozen=True)
class SourceApprovalRevocationRecord:
    revocation_id: str
    approval_revocation_supported: bool
    revocation_reason_required: bool
    revoked_approval_cannot_be_used: bool
    revocation_must_be_recorded: bool
    revocation_record_protected: bool


@dataclass(frozen=True)
class SourceApprovalBoundaryRecord:
    boundary_id: str
    statement: str
    holds: bool


@dataclass(frozen=True)
class SourceApprovalTraceabilityRecord:
    trace_key: str
    trace_ref: str
    present: bool


@dataclass(frozen=True)
class SourceRiskAcknowledgementRecord:
    asset_id: str
    risk_dimensions_acknowledged: Tuple[str, ...]
    owner_ack_required_for_next_phase: bool
    all_risk_dimensions_acknowledged: bool


@dataclass(frozen=True)
class SourceInstallPreparationHandoffReadiness:
    handoff_id: str
    next_phase_ref: str
    can_enter_source_install_preparation: bool
    can_enter_git_clone: bool
    can_enter_source_checkout: bool
    can_enter_source_install: bool
    can_enter_weight_download: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_output_adapter: bool
    can_enter_semantic_layer: bool
    direct_source_install_execution_blocked: bool


@dataclass
class NegativeSourceOwnerApprovalIssuanceGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallOwnerApprovalIssuanceDecision:
    decision_ref: str
    source_owner_approval_issuance_profile_count: int
    source_owner_approval_issuance_record_count: int
    source_approval_scope_record_count: int
    approved_source_asset_scope_record_count: int
    source_approval_condition_record_count: int
    source_approval_expiry_record_count: int
    source_approval_revocation_record_count: int
    source_approval_boundary_record_count: int
    source_approval_traceability_record_count: int
    source_risk_acknowledgement_record_count: int
    source_install_preparation_handoff_readiness_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
