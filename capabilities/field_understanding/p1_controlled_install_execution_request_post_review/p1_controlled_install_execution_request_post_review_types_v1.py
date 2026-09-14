# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Request Post-Review — types v1.

Pure post-review of Phase-P1-Controlled-Install-Execution-Request-v1-001. It
audits the install-execution REQUEST package for compliance:

  Request != Owner Approval
  Request != Install Execution
  Request != Inference / Runtime / Output Adapter / Semantic Layer

This phase mutates nothing, generates no owner approval, performs no approval
issuance, executes no pip install, installs no dependency, downloads no
model/weight/dataset, runs no inference, enters no runtime / semantic layer. It
only re-checks the request package, requested asset scope, excluded asset
disclosure, owner approval request record, command template references, the
snapshot / rollback / probe REQUESTS, risk disclosure, permission boundary, the
upstream test board planning records, and the non-execution boundaries.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_RECORD_TYPES,
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001"
SCOPE = "p1_controlled_install_execution_request_post_review"
SOURCE_CHAIN = "p1_controlled_install_execution_request_post_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Execution-Request-v1-001，执行纯事后复核。Request ≠ Owner Approval，"
    "Request ≠ Install Execution，Request ≠ Inference/Runtime/Output Adapter/Semantic Layer。该阶段不修改 request "
    "package、不生成 owner approval、不进入 approval issuance、不执行 pip install、不安装依赖、不下载模型/权重/数据集、"
    "不执行 inference、不进入 runtime、不进入语义层。只复核 request package、requested asset scope、excluded asset "
    "disclosure、owner approval request record、command template references、snapshot/rollback/probe request、risk "
    "disclosure、permission boundary、上一阶段测试板块（planning）记录与 non-execution 边界。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_request_post_review_is_review_only_no_mutation_no_approval_no_issuance_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
REQUEST_PACKAGE_MUTATION_ALLOWED = False
OWNER_APPROVAL_GENERATION_ALLOWED = False
APPROVAL_ISSUANCE_ALLOWED = False
INSTALL_EXECUTION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Install-Execution-Request-v1-001"
EXECUTION_PLANNING_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001"
EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001"

UPSTREAM_REQUEST_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "post_review"

# Upstream request artifact (read for the artifact audit; sealed-ref fallback).
UPSTREAM_REQUEST_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_execution_request_v1_smoke_v0/"
    "p1_controlled_install_execution_request_review_v1.json"
)

# Upstream request test board (planning mode) directory, searched across roots.
UPSTREAM_REQUEST_TEST_BOARD_REL = (
    "capabilities/test_board/recognition_models/"
    "phase_p1_controlled_install_execution_request_v1_001"
)
UPSTREAM_REQUEST_TEST_BOARD_EXPECTED_MODE = "planning"

# --------------------------------------------------------------------------- #
# Scope (locked, must match request phase).
# --------------------------------------------------------------------------- #
EXPECTED_REQUESTED_ASSETS: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)
EXPECTED_EXCLUDED_ASSETS: Tuple[Dict[str, str], ...] = (
    {"asset_id": "fast_sam", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    {"asset_id": "yolov8n", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    {"asset_id": "pyannote", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    {"asset_id": "sam2", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "depth_anything", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "zoe_depth", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "grounding_dino", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "scene_relation_vlm", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "open_vocab_vlm", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "sense_voice", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "emotion_multimodal_bridge", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "rt_detr", "exclusion_bucket": "PARTIAL_OR_NON_INSTALL_REQUIRED"},
)

REQUIRED_SNAPSHOT_ITEMS: Tuple[str, ...] = (
    "python_version_capture",
    "pip_freeze_capture",
    "package_list_capture",
    "path_env_capture",
    "registry_snapshot",
    "test_board_snapshot",
    "rollback_snapshot",
    "snapshot_artifact_protected",
    "snapshot_non_deletable",
)

REQUIRED_PERMISSION_BOUNDARIES: Tuple[str, ...] = (
    "request_success_not_owner_approval",
    "request_success_not_install_execution_approval",
    "request_success_not_inference_approval",
    "request_success_not_runtime_approval",
    "request_success_not_output_adapter_approval",
    "request_success_not_semantic_layer_approval",
    "commercial_runtime_approved",
)

# Non-execution boundary items (>= 18).
NON_EXECUTION_BOUNDARY_ITEMS: Tuple[str, ...] = (
    "owner_approval_granted",
    "approval_issuance_allowed",
    "install_execution_allowed",
    "real_install_performed",
    "dependency_install_performed",
    "pip_install_performed",
    "model_download_performed",
    "weight_download_performed",
    "dataset_download_performed",
    "real_inference_performed",
    "runtime_execution_allowed",
    "runtime_activation_allowed",
    "navigation_runtime_allowed",
    "action_runtime_allowed",
    "speech_runtime_allowed",
    "fact_write_runtime_allowed",
    "semantic_promotion_allowed",
    "vla_action_chain_allowed",
    "commercial_runtime_approved",
)

# Upstream test board planning records that must exist (6 + manifest).
UPSTREAM_TEST_BOARD_RECORDS: Tuple[str, ...] = REQUIRED_RECORD_TYPES + ("test_board_manifest",)

# --------------------------------------------------------------------------- #
# Sealed expected metrics (fallback when upstream artifact is missing).
# --------------------------------------------------------------------------- #
SEALED_EXPECTED_METRICS: Dict[str, Any] = {
    "final_decision": UPSTREAM_REQUEST_EXPECTED_GO,
    "blocker_count": 0,
    "install_execution_request_package_count": 1,
    "requested_asset_count": 5,
    "excluded_asset_disclosure_count": 12,
    "owner_approval_request_record_count": 1,
    "command_template_reference_record_count": 5,
    "pre_install_snapshot_request_count": 1,
    "rollback_requirement_request_count": 5,
    "post_install_probe_requirement_request_count": 5,
    "risk_disclosure_record_count": 5,
    "request_audit_record_count": 10,
    "request_permission_boundary_count": 7,
    "negative_guard_passed": 27,
    "test_board_record_count": 6,
}

# Artifact audit spec: (field, comparator, expected). comparator in {eq, gte}.
ARTIFACT_AUDIT_SPEC: Tuple[Tuple[str, str, Any], ...] = (
    ("final_decision", "eq", UPSTREAM_REQUEST_EXPECTED_GO),
    ("blocker_count", "eq", 0),
    ("install_execution_request_package_count", "eq", 1),
    ("requested_asset_count", "eq", 5),
    ("excluded_asset_disclosure_count", "eq", 12),
    ("owner_approval_request_record_count", "gte", 1),
    ("command_template_reference_record_count", "eq", 5),
    ("pre_install_snapshot_request_count", "gte", 1),
    ("rollback_requirement_request_count", "eq", 5),
    ("post_install_probe_requirement_request_count", "eq", 5),
    ("risk_disclosure_record_count", "eq", 5),
    ("request_audit_record_count", "gte", 8),
    ("request_permission_boundary_count", "gte", 6),
    ("negative_guard_passed", "eq", 27),
    ("test_board_record_count", "gte", 6),
)

# --------------------------------------------------------------------------- #
# Negative post-review guards (31: A..Z, AA, AB, AC, AD, AE).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_final_decision_not_go", "go_key": "upstream_final_decision_go_verified", "depends_on": "upstream_final_decision_go"},
    {"guard_id": "invalid_b_upstream_blocker_count_nonzero", "go_key": "upstream_blocker_count_zero_verified", "depends_on": "upstream_blocker_count_zero"},
    {"guard_id": "invalid_c_request_package_missing", "go_key": "request_package_verified", "depends_on": "request_package_present"},
    {"guard_id": "invalid_d_request_as_owner_approval", "go_key": "request_success_not_owner_approval", "depends_on": "request_success_not_owner_approval"},
    {"guard_id": "invalid_e_request_as_install_execution_approval", "go_key": "request_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_f_request_as_inference_approval", "go_key": "request_success_not_inference_approval", "depends_on": "not_inference_approval"},
    {"guard_id": "invalid_g_request_as_runtime_approval", "go_key": "request_success_not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_h_request_as_output_adapter_approval", "go_key": "request_success_not_output_adapter_approval", "depends_on": "not_output_adapter_approval"},
    {"guard_id": "invalid_i_request_as_semantic_layer_approval", "go_key": "request_success_not_semantic_layer_approval", "depends_on": "not_semantic_layer_approval"},
    {"guard_id": "invalid_j_approval_granted_true", "go_key": "owner_approval_not_granted", "depends_on": "owner_approval_not_granted"},
    {"guard_id": "invalid_k_approval_issuance_allowed_this_phase", "go_key": "approval_issuance_blocked", "depends_on": "approval_issuance_blocked"},
    {"guard_id": "invalid_l_request_scope_not_five_assets", "go_key": "requested_asset_count_verified", "depends_on": "requested_asset_count_five"},
    {"guard_id": "invalid_m_excluded_assets_in_request_scope", "go_key": "excluded_assets_not_in_request_scope", "depends_on": "excluded_assets_not_in_request_scope"},
    {"guard_id": "invalid_n_request_scope_includes_runtime_inference_semantic", "go_key": "request_scope_excludes_runtime_inference_semantic", "depends_on": "request_scope_excludes_runtime_inference_semantic"},
    {"guard_id": "invalid_o_request_scope_includes_unapproved_weight_download", "go_key": "request_scope_excludes_weight_download", "depends_on": "request_scope_excludes_weight_download"},
    {"guard_id": "invalid_p_new_install_command_generated", "go_key": "no_new_install_command", "depends_on": "no_new_install_command"},
    {"guard_id": "invalid_q_install_command_executed", "go_key": "request_does_not_execute_command", "depends_on": "request_does_not_execute_command"},
    {"guard_id": "invalid_r_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_s_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_t_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_u_pre_install_snapshot_request_missing", "go_key": "pre_install_snapshot_requested", "depends_on": "pre_install_snapshot_requested"},
    {"guard_id": "invalid_v_rollback_requirement_request_missing", "go_key": "rollback_requirement_requested", "depends_on": "rollback_requirement_requested"},
    {"guard_id": "invalid_w_post_install_probe_request_missing", "go_key": "post_install_probe_requested", "depends_on": "post_install_probe_requested"},
    {"guard_id": "invalid_x_probe_allows_import_load_inference_runtime_adapter", "go_key": "post_install_probe_find_spec_only_strict", "depends_on": "post_install_probe_find_spec_only_strict"},
    {"guard_id": "invalid_y_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_z_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_aa_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_ab_upstream_test_board_planning_missing_or_mode_mismatch", "go_key": "upstream_test_board_planning_record_verified", "depends_on": "upstream_test_board_planning_verified"},
    {"guard_id": "invalid_ac_current_post_review_test_board_not_written", "go_key": "current_post_review_test_board_written", "depends_on": "current_post_review_test_board_written"},
    {"guard_id": "invalid_ad_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_ae_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (42 phase + 6 test board = 48).
# --------------------------------------------------------------------------- #
POST_REVIEW_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_install_execution_request_post_review_only",
    "no_request_package_mutation_is_allowed",
    "no_owner_approval_is_generated",
    "approval_issuance_is_not_allowed",
    "request_is_not_owner_approval",
    "request_is_not_install_execution_approval",
    "request_is_not_inference_approval",
    "request_is_not_runtime_approval",
    "request_is_not_real_output_adapter_approval",
    "request_is_not_semantic_layer_approval",
    "owner_approval_remains_not_granted",
    "install_execution_is_not_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "requested_scope_must_remain_limited_to_approved_install_candidates",
    "excluded_assets_must_not_enter_request_scope",
    "no_new_install_command_may_be_generated",
    "command_template_refs_must_remain_non_executed",
    "pre_install_snapshot_request_audit_is_required",
    "rollback_requirement_request_audit_is_required",
    "post_install_probe_request_audit_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "post_install_probe_is_not_output_adapter",
    "future_approval_issuance_requires_separate_phase",
    "future_install_execution_requires_separate_owner_approval",
    "future_approval_must_exclude_inference_unless_separately_approved",
    "future_approval_must_exclude_runtime_unless_separately_approved",
    "future_approval_must_exclude_weight_download_unless_separately_approved",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "upstream_request_test_board_audit_is_required",
    "current_post_review_test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    POST_REVIEW_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionRequestPostReviewProfile",
    "InstallExecutionRequestArtifactAudit",
    "RequestPackageAudit",
    "RequestedAssetScopeAudit",
    "ExcludedAssetDisclosureAudit",
    "OwnerApprovalRequestAudit",
    "CommandTemplateReferenceAudit",
    "PreInstallSnapshotRequestAudit",
    "RollbackRequirementRequestAudit",
    "PostInstallProbeRequirementAudit",
    "RiskDisclosureAudit",
    "RequestPermissionBoundaryAudit",
    "UpstreamTestBoardPlanningRecordAudit",
    "NonExecutionBoundaryAudit",
    "NegativeInstallExecutionRequestPostReviewGuard",
    "OwnerApprovalIssuanceHandoffReadiness",
    "P1ControlledInstallExecutionRequestPostReviewDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_owner_approval_issuance_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "post_review_test_mode_reused": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "request_package_mutation_allowed": False,
    "owner_approval_generation_allowed": False,
    "approval_issuance_allowed": False,
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
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "semantic_promotion_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class P1ControlledInstallExecutionRequestPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    request_package_mutation_allowed: bool
    owner_approval_generation_allowed: bool
    approval_issuance_allowed: bool
    install_execution_allowed: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    upstream_request_ref: str
    execution_planning_post_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    expected_requested_assets: Tuple[str, ...]
    expected_excluded_assets: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class InstallExecutionRequestArtifactAudit:
    artifact_ref: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    checks_total: int
    checks_passed: int
    field_results: Tuple[Dict[str, Any], ...]
    audit_holds: bool


@dataclass(frozen=True)
class RequestPackageAudit:
    request_id_exists: bool
    request_type_ok: bool
    request_package_complete: bool
    request_only: bool
    owner_approval_required: bool
    owner_approval_granted: bool
    install_execution_allowed: bool
    request_success_not_owner_approval: bool
    request_success_not_install_execution_approval: bool
    request_success_not_inference_approval: bool
    request_success_not_runtime_approval: bool
    request_success_not_output_adapter_approval: bool
    request_success_not_semantic_layer_approval: bool
    audit_holds: bool


@dataclass(frozen=True)
class RequestedAssetScopeAudit:
    asset_id: str
    in_requested_scope: bool
    not_excluded: bool
    not_runtime: bool
    not_inference: bool
    not_weight_download_unless_separately_approved: bool
    not_semantic_layer: bool
    audit_holds: bool


@dataclass(frozen=True)
class ExcludedAssetDisclosureAudit:
    asset_id: str
    exclusion_bucket: str
    disclosed: bool
    cannot_enter_request_scope: bool
    cannot_enter_install_execution: bool
    cannot_enter_runtime: bool
    cannot_enter_real_output_adapter: bool
    audit_holds: bool


@dataclass(frozen=True)
class OwnerApprovalRequestAudit:
    approval_request_created: bool
    approval_granted: bool
    approval_scope_requested_ok: bool
    approval_excludes_inference: bool
    approval_excludes_runtime: bool
    approval_excludes_real_output_adapter: bool
    approval_excludes_semantic_layer: bool
    approval_excludes_commercial_runtime: bool
    approval_excludes_weight_download_unless_separately_approved: bool
    owner_review_required: bool
    owner_explicit_go_required_for_next_phase: bool
    approval_expiry_required: bool
    approval_revocation_supported: bool
    post_review_success_not_owner_approval: bool
    request_post_review_success_not_approval_issuance: bool
    audit_holds: bool


@dataclass(frozen=True)
class CommandTemplateReferenceAudit:
    asset_id: str
    command_template_ref_exists: bool
    template_only: bool
    command_not_executed: bool
    new_command_generated: bool
    whitelist_ref_exists: bool
    command_requires_future_approval: bool
    command_requires_pre_snapshot: bool
    command_requires_rollback_plan: bool
    audit_holds: bool


@dataclass(frozen=True)
class PreInstallSnapshotRequestAudit:
    pre_install_snapshot_requested: bool
    requested_items_present: Tuple[str, ...]
    missing_items: Tuple[str, ...]
    snapshot_not_executed_in_this_phase: bool
    audit_holds: bool


@dataclass(frozen=True)
class RollbackRequirementRequestAudit:
    asset_id: str
    rollback_plan_required: bool
    rollback_trigger_conditions_ref_exists: bool
    rollback_command_template_ref_exists: bool
    rollback_command_not_executed: bool
    rollback_preserve_test_board: bool
    rollback_preserve_registry: bool
    rollback_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool
    audit_holds: bool


@dataclass(frozen=True)
class PostInstallProbeRequirementAudit:
    asset_id: str
    post_install_probe_required: bool
    probe_uses_find_spec_only: bool
    real_import_allowed: bool
    no_model_load_on_probe: bool
    no_inference_on_probe: bool
    no_runtime_on_probe: bool
    no_output_adapter_on_probe: bool
    installed_version_record_required: bool
    dependency_gap_recheck_required: bool
    license_recheck_required: bool
    test_board_probe_record_required: bool
    audit_holds: bool


@dataclass(frozen=True)
class RiskDisclosureAudit:
    asset_id: str
    dependency_risk_exists: bool
    license_risk_exists: bool
    weight_risk_exists: bool
    environment_risk_exists: bool
    rollback_risk_exists: bool
    owner_ack_required: bool
    install_execution_allowed: bool
    can_enter_install_execution_after_approval: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_real_output_adapter: bool
    audit_holds: bool


@dataclass(frozen=True)
class RequestPermissionBoundaryAudit:
    boundary_id: str
    holds: bool


@dataclass(frozen=True)
class UpstreamTestBoardPlanningRecordAudit:
    record_id: str
    exists: bool
    protected: bool
    non_deletable: bool
    deletion_forbidden: bool
    test_mode_planning: bool
    audit_holds: bool


@dataclass(frozen=True)
class NonExecutionBoundaryAudit:
    boundary_id: str
    expected_false: bool
    actual_false: bool
    holds: bool


@dataclass
class NegativeInstallExecutionRequestPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class OwnerApprovalIssuanceHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool
    approval_issuance_allowed_this_phase: bool


@dataclass(frozen=True)
class P1ControlledInstallExecutionRequestPostReviewDecision:
    decision_ref: str
    install_execution_request_post_review_profile_count: int
    install_execution_request_artifact_audit_count: int
    request_package_audit_count: int
    requested_asset_scope_audit_count: int
    excluded_asset_disclosure_audit_count: int
    owner_approval_request_audit_count: int
    command_template_reference_audit_count: int
    pre_install_snapshot_request_audit_count: int
    rollback_requirement_request_audit_count: int
    post_install_probe_requirement_audit_count: int
    risk_disclosure_audit_count: int
    request_permission_boundary_audit_count: int
    upstream_test_board_planning_record_audit_count: int
    non_execution_boundary_audit_count: int
    negative_post_review_guard_count: int
    negative_post_review_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
