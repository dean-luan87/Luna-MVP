# -*- coding: utf-8 -*-
"""P1 Controlled Install Owner Approval Issuance — types v1.

Generates an owner approval ISSUANCE record for the P1 controlled install
execution request. The approval scope is intentionally very narrow:

  Approval Issuance != Install Execution

This phase MAY generate an approval issuance record, but the issued approval
only permits entering the subsequent controlled install execution PREPARATION /
execution planning chain. It does NOT approve real install, pip install,
dependency install, model/weight/dataset download, inference, runtime, real
output adapter, or the semantic layer. It executes none of those either.

A local Owner / Record Approval protocol module is referenced as a
`governance_ref` (non-mutating); this phase only writes its own issuance record.
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

PHASE_ID = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001"
SCOPE = "p1_controlled_install_owner_approval_issuance"
SOURCE_CHAIN = "p1_controlled_install_owner_approval_issuance_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001，生成 P1 受控安装执行请求的 owner "
    "approval issuance。Approval Issuance ≠ Install Execution。本阶段允许生成审批发行记录，但审批范围仅限于“允许进入后续 "
    "controlled install execution preparation / execution planning chain”。不执行安装、不执行 pip install、不安装依赖、"
    "不下载模型/权重/数据集、不执行 inference、不进入 runtime、不进入 output adapter、不进入语义层。审批发行成功不等于 "
    "install execution / inference / runtime / output adapter / semantic layer 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_owner_approval_issuance_is_execution_preparation_scope_only_not_install_execution_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
APPROVAL_ISSUANCE_ONLY = True
OWNER_APPROVAL_ISSUANCE_CREATED = True
OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION_PREPARATION = True
OWNER_APPROVAL_GRANTED_FOR_INSTALL_EXECUTION = False
INSTALL_EXECUTION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True
OLD_APPROVAL_SYSTEM_MUTATED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REQUEST_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001"
UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Install-Execution-Request-v1-001"
EXECUTION_PLANNING_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001"
EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
CONTROLLED_INSTALL_PLANNING_REF = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"
CONTROLLED_INSTALL_PLANNING_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"
REGISTRY_PROBE_RECONCILIATION_REF = (
    "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-Post-Review-v1-001"
EXECUTION_PREPARATION_REF = "Phase-P1-Controlled-Install-Execution-Preparation-v1-001"

# Local Owner / Record Approval protocol module referenced as governance_ref.
OWNER_APPROVAL_PROTOCOL_GOVERNANCE_REF = "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"
GOVERNANCE_REFS: Tuple[str, ...] = (OWNER_APPROVAL_PROTOCOL_GOVERNANCE_REF,)

UPSTREAM_REQUEST_POST_REVIEW_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_POST_REVIEW_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

APPROVAL_SCOPE = "install_execution_preparation_only"

# --------------------------------------------------------------------------- #
# Scope (locked).
# --------------------------------------------------------------------------- #
APPROVED_ASSET_IDS: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)
EXCLUDED_ASSETS: Tuple[Dict[str, str], ...] = (
    {"asset_id": "fast_sam", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "yolov8n", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "pyannote", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "sam2", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "depth_anything", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "zoe_depth", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "grounding_dino", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "scene_relation_vlm", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "open_vocab_vlm", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "sense_voice", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "emotion_multimodal_bridge", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "rt_detr", "exclusion_reason": "PARTIAL_OR_NON_INSTALL_REQUIRED"},
)

# Approval conditions (>= 8).
APPROVAL_CONDITIONS: Tuple[str, ...] = (
    "pre_install_snapshot_required",
    "command_whitelist_required",
    "execution_order_lock_required",
    "stop_condition_enforcement_required",
    "rollback_plan_required",
    "post_install_probe_required",
    "test_board_write_required",
    "owner_revocation_supported",
    "approval_expiry_required",
    "next_phase_required_before_execution",
)

# Approval boundary statements (>= 6).
APPROVAL_BOUNDARY_STATEMENTS: Tuple[Dict[str, Any], ...] = (
    {"boundary_id": "approval_issuance_success_not_install_execution_approval", "value_is_true": True},
    {"boundary_id": "approval_issuance_success_not_inference_approval", "value_is_true": True},
    {"boundary_id": "approval_issuance_success_not_runtime_approval", "value_is_true": True},
    {"boundary_id": "approval_issuance_success_not_output_adapter_approval", "value_is_true": True},
    {"boundary_id": "approval_issuance_success_not_semantic_layer_approval", "value_is_true": True},
    {"boundary_id": "owner_approval_granted_for_install_execution", "value_is_true": False},
    {"boundary_id": "commercial_runtime_approved", "value_is_true": False},
)

# Expiry policy.
APPROVAL_EXPIRY_POLICY = (
    "approval_expires_on_first_of:fixed_window_or_registry_drift_or_dependency_drift_or_scope_change"
)

# Revocation policy.
APPROVAL_REVOCATION_POLICY = "owner_initiated_revocation_recorded_protected_and_blocks_use"

# Traceability refs (>= 8).
TRACEABILITY_REFS: Tuple[Tuple[str, str], ...] = (
    ("request_ref", UPSTREAM_REQUEST_REF),
    ("request_post_review_ref", UPSTREAM_REQUEST_POST_REVIEW_REF),
    ("execution_planning_ref", EXECUTION_PLANNING_REF),
    ("execution_planning_post_review_ref", EXECUTION_PLANNING_POST_REVIEW_REF),
    ("controlled_install_planning_ref", CONTROLLED_INSTALL_PLANNING_REF),
    ("controlled_install_planning_post_review_ref", CONTROLLED_INSTALL_PLANNING_POST_REVIEW_REF),
    ("registry_probe_reconciliation_ref", REGISTRY_PROBE_RECONCILIATION_REF),
    ("test_board_ref", "capabilities/test_board/recognition_models/phase_p1_controlled_install_owner_approval_issuance_v1_001"),
    ("approval_issuance_trace_id", "p1_controlled_install_owner_approval_issuance_trace_v1"),
)

# Per-asset weight handling (for approved asset scope).
NO_WEIGHT_ASSETS: Tuple[str, ...] = ("supervision", "byte_track")
WEIGHT_HANDLED_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

# --------------------------------------------------------------------------- #
# Negative guards (25: A..Y).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_issuance_as_install_execution_approval", "go_key": "approval_issuance_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_b_issuance_as_pip_or_dependency_install_approval", "go_key": "issuance_not_install_approval", "depends_on": "not_install_approval"},
    {"guard_id": "invalid_c_issuance_as_download_approval", "go_key": "issuance_not_download_approval", "depends_on": "not_download_approval"},
    {"guard_id": "invalid_d_issuance_as_inference_approval", "go_key": "approval_issuance_success_not_inference_approval", "depends_on": "not_inference_approval"},
    {"guard_id": "invalid_e_issuance_as_runtime_approval", "go_key": "approval_issuance_success_not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_f_issuance_as_output_adapter_approval", "go_key": "approval_issuance_success_not_output_adapter_approval", "depends_on": "not_output_adapter_approval"},
    {"guard_id": "invalid_g_issuance_as_semantic_layer_approval", "go_key": "approval_issuance_success_not_semantic_layer_approval", "depends_on": "not_semantic_layer_approval"},
    {"guard_id": "invalid_h_approval_scope_includes_excluded", "go_key": "excluded_assets_remain_excluded", "depends_on": "excluded_assets_remain_excluded"},
    {"guard_id": "invalid_i_approval_scope_includes_unapproved_weight_download", "go_key": "weight_download_requires_separate_approval", "depends_on": "weight_download_requires_separate_approval"},
    {"guard_id": "invalid_j_approval_no_expiry", "go_key": "approval_expiry_required", "depends_on": "approval_expiry_present"},
    {"guard_id": "invalid_k_approval_no_revocation", "go_key": "approval_revocation_required", "depends_on": "approval_revocation_present"},
    {"guard_id": "invalid_l_approval_missing_source_chain_traceability", "go_key": "source_chain_complete", "depends_on": "source_chain_complete"},
    {"guard_id": "invalid_m_approval_missing_rollback_condition", "go_key": "rollback_condition_required", "depends_on": "rollback_condition_present"},
    {"guard_id": "invalid_n_approval_missing_post_install_probe_condition", "go_key": "post_install_probe_condition_required", "depends_on": "post_install_probe_condition_present"},
    {"guard_id": "invalid_o_approval_allows_skip_execution_preparation", "go_key": "direct_install_execution_not_allowed_after_this_phase", "depends_on": "execution_preparation_required_before_execution"},
    {"guard_id": "invalid_p_real_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_q_model_weight_dataset_download_executed", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_r_real_inference_executed", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_s_runtime_execution_allowed", "go_key": "runtime_execution_blocked", "depends_on": "runtime_not_allowed"},
    {"guard_id": "invalid_t_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_u_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_v_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_w_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_x_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_y_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (36 phase + 6 test board = 42).
# --------------------------------------------------------------------------- #
ISSUANCE_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_owner_approval_issuance_only",
    "approval_issuance_is_limited_to_install_execution_preparation",
    "approval_issuance_is_not_install_execution_approval",
    "approval_issuance_is_not_pip_install_approval",
    "approval_issuance_is_not_dependency_install_approval",
    "approval_issuance_is_not_model_download_approval",
    "approval_issuance_is_not_weight_download_approval",
    "approval_issuance_is_not_dataset_download_approval",
    "approval_issuance_is_not_inference_approval",
    "approval_issuance_is_not_runtime_approval",
    "approval_issuance_is_not_real_output_adapter_approval",
    "approval_issuance_is_not_semantic_layer_approval",
    "approved_asset_scope_is_limited_to_requested_assets",
    "excluded_assets_must_remain_excluded",
    "weight_download_requires_separate_approval",
    "approval_expiry_is_required",
    "approval_revocation_is_required",
    "source_chain_traceability_is_required",
    "rollback_condition_is_required",
    "post_install_probe_condition_is_required",
    "execution_preparation_phase_is_required_before_any_install_execution",
    "direct_install_execution_is_not_allowed_after_this_phase",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    ISSUANCE_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallOwnerApprovalIssuanceProfile",
    "OwnerApprovalIssuanceRecord",
    "ApprovalScopeRecord",
    "ApprovedAssetScopeRecord",
    "ExcludedAssetScopeRecord",
    "ApprovalConditionRecord",
    "ApprovalExpiryRecord",
    "ApprovalRevocationRecord",
    "ApprovalBoundaryRecord",
    "ApprovalTraceabilityRecord",
    "ApprovalRiskAcknowledgementRecord",
    "ApprovalHandoffReadiness",
    "NegativeOwnerApprovalIssuanceGuard",
    "P1ControlledInstallOwnerApprovalIssuanceDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, Any], ...] = (
    {
        "target_ref": EXECUTION_PREPARATION_REF,
        "go_key": "p1_controlled_install_execution_preparation_readiness_recorded",
        "can_enter": True,
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_OWNER_APPROVAL_ISSUANCE_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_OWNER_APPROVAL_ISSUANCE_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "owner_approval_protocol_referenced_as_governance_ref": True,
    "old_approval_system_mutated": False,
    "planning_test_mode_reused": True,
}

# Capability boundaries reachable / not reachable after this phase.
CAN_ENTER_FLAGS: Dict[str, bool] = {
    "can_enter_execution_preparation": True,
    "can_enter_install_execution": False,
    "can_enter_inference": False,
    "can_enter_runtime": False,
    "can_enter_output_adapter": False,
    "can_enter_semantic_layer": False,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "install_execution_allowed": False,
    "real_install_performed": False,
    "dependency_install_performed": False,
    "pip_install_performed": False,
    "model_download_performed": False,
    "weight_download_performed": False,
    "dataset_download_performed": False,
    "real_inference_performed": False,
    "runtime_execution_allowed": False,
    "runtime_activation_allowed": False,
    "real_output_adapter_allowed": False,
    "semantic_promotion_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class P1ControlledInstallOwnerApprovalIssuanceProfile:
    profile_ref: str
    phase_id: str
    approval_issuance_only: bool
    owner_approval_issuance_created: bool
    owner_approval_granted_for_install_execution_preparation: bool
    owner_approval_granted_for_install_execution: bool
    install_execution_allowed: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    old_approval_system_mutated: bool
    upstream_request_post_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    governance_refs: Tuple[str, ...]
    luna_core_principle: str
    approved_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class OwnerApprovalIssuanceRecord:
    issuance_id: str
    phase_id: str
    owner_approval_issuance_created: bool
    owner_approval_granted_for_install_execution_preparation: bool
    owner_approval_granted_for_install_execution: bool
    approval_scope: str
    approval_issuance_success_not_install_execution_approval: bool
    approval_issuance_success_not_inference_approval: bool
    approval_issuance_success_not_runtime_approval: bool
    approval_issuance_success_not_output_adapter_approval: bool
    approval_issuance_success_not_semantic_layer_approval: bool
    issuance_complete: bool


@dataclass(frozen=True)
class ApprovalScopeRecord:
    approval_scope: str
    approved_for_install_execution_preparation: bool
    approved_for_install_execution: bool
    approved_for_pip_install: bool
    approved_for_dependency_install: bool
    approved_for_model_download: bool
    approved_for_weight_download: bool
    approved_for_dataset_download: bool
    approved_for_inference: bool
    approved_for_runtime: bool
    approved_for_real_output_adapter: bool
    approved_for_semantic_layer: bool
    approved_for_commercial_runtime: bool
    approved_for_vla_action_chain: bool
    approved_for_navigation_action_speech_fact_write: bool


@dataclass(frozen=True)
class ApprovedAssetScopeRecord:
    asset_id: str
    included_in_approval_scope: bool
    approval_scope: str
    install_execution_allowed: bool
    inference_allowed: bool
    runtime_allowed: bool
    output_adapter_allowed: bool
    semantic_layer_allowed: bool
    weight_download_allowed: bool
    requires_next_phase_execution_preparation: bool


@dataclass(frozen=True)
class ExcludedAssetScopeRecord:
    asset_id: str
    excluded_from_approval_scope: bool
    exclusion_reason: str
    cannot_enter_install_execution: bool
    cannot_enter_inference: bool
    cannot_enter_runtime: bool
    cannot_enter_output_adapter: bool


@dataclass(frozen=True)
class ApprovalConditionRecord:
    condition_id: str
    required: bool
    enforced_in_future_phase: bool


@dataclass(frozen=True)
class ApprovalExpiryRecord:
    approval_has_expiry: bool
    expiry_policy: str
    expired_approval_cannot_be_used: bool
    approval_use_after_registry_drift_blocked: bool
    approval_use_after_dependency_drift_blocked: bool
    approval_use_after_scope_change_blocked: bool


@dataclass(frozen=True)
class ApprovalRevocationRecord:
    approval_revocation_supported: bool
    revocation_reason_required: bool
    revoked_approval_cannot_be_used: bool
    revocation_must_be_recorded: bool
    revocation_record_protected: bool
    revocation_policy: str


@dataclass(frozen=True)
class ApprovalBoundaryRecord:
    boundary_id: str
    holds: bool


@dataclass(frozen=True)
class ApprovalTraceabilityRecord:
    ref_id: str
    ref_value: str
    present: bool


@dataclass(frozen=True)
class ApprovalRiskAcknowledgementRecord:
    asset_id: str
    dependency_risk_acknowledged: bool
    license_risk_acknowledged: bool
    weight_risk_acknowledged: bool
    environment_risk_acknowledged: bool
    rollback_risk_acknowledged: bool
    owner_ack_required_for_next_phase: bool


@dataclass(frozen=True)
class ApprovalHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    can_enter_execution_preparation: bool
    can_enter_install_execution: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_output_adapter: bool
    can_enter_semantic_layer: bool


@dataclass
class NegativeOwnerApprovalIssuanceGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallOwnerApprovalIssuanceDecision:
    decision_ref: str
    owner_approval_issuance_profile_count: int
    owner_approval_issuance_record_count: int
    approval_scope_record_count: int
    approved_asset_scope_record_count: int
    excluded_asset_scope_record_count: int
    approval_condition_record_count: int
    approval_expiry_record_count: int
    approval_revocation_record_count: int
    approval_boundary_record_count: int
    approval_traceability_record_count: int
    approval_risk_acknowledgement_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
