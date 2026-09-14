# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Preparation And Readiness Review — types v1.

COMPRESSED phase merging three originally separate steps:
  1. Owner Approval Issuance Post-Review (confirm scope = preparation-only)
  2. Execution Preparation (snapshot plan, final command whitelist, order lock,
     rollback, post-install probe, package/weight install scope)
  3. Execution Readiness Review (decide whether the real Controlled Install
     Execution phase may be entered next)

It still executes NOTHING: no pip install, no dependency install, no
model/weight/dataset download, no inference, no runtime, no output adapter, no
semantic layer. It only emits an execution preparation package and an execution
readiness decision. If GO, the NEXT phase
(Phase-P1-Controlled-Install-Execution-v1-001) may begin — and the first
execution is recommended to be package-install-only (weight download deferred to
a separate sub-approval).
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Preparation-And-Readiness-Review-v1-001"
SCOPE = "p1_controlled_install_execution_preparation_and_readiness_review"
SOURCE_CHAIN = "p1_controlled_install_execution_preparation_and_readiness_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "压缩阶段：合并 Owner Approval Issuance Post-Review、Execution Preparation、Execution Readiness Review。基于已 GO 的 "
    "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001，复核 owner approval issuance 范围只限 install execution "
    "preparation，并完成真实安装执行前的准备与 readiness review。不执行 pip install、不安装依赖、不下载模型/权重/数据集、"
    "不执行 inference、不进入 runtime、不进入 output adapter、不进入语义层。只生成 execution preparation package 与 "
    "execution readiness decision。若本阶段 GO，下一阶段才允许进入 Phase-P1-Controlled-Install-Execution-v1-001。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_execution_preparation_and_readiness_review_is_preparation_only_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED = True
EXECUTION_PREPARATION_INCLUDED = True
EXECUTION_READINESS_REVIEW_INCLUDED = True
EXECUTION_PREPARATION_PACKAGE_CREATED = True
EXECUTION_READINESS_DECISION_CREATED = True
CAN_ENTER_CONTROLLED_INSTALL_EXECUTION_NEXT = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_REQUEST_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001"
UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Install-Execution-Request-v1-001"
EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-v1-001"

UPSTREAM_ISSUANCE_EXPECTED_GO = "P1_CONTROLLED_INSTALL_OWNER_APPROVAL_ISSUANCE_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

APPROVAL_SCOPE = "install_execution_preparation_only"

# Upstream issuance artifact (read for the approval issuance scope audit).
UPSTREAM_ISSUANCE_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_owner_approval_issuance_v1_smoke_v0/"
    "p1_controlled_install_owner_approval_issuance_review_v1.json"
)

# --------------------------------------------------------------------------- #
# Scope (locked).
# --------------------------------------------------------------------------- #
APPROVED_ASSET_ORDER: Tuple[Tuple[str, int], ...] = (
    ("supervision", 1),
    ("byte_track", 2),
    ("deep_sort", 3),
    ("midas", 4),
    ("mobile_sam", 5),
)
APPROVED_ASSET_IDS: Tuple[str, ...] = tuple(a for a, _ in APPROVED_ASSET_ORDER)
FINAL_EXECUTION_ORDER: Tuple[str, ...] = APPROVED_ASSET_IDS

NO_WEIGHT_ASSETS: Tuple[str, ...] = ("supervision", "byte_track")
WEIGHT_SUBAPPROVAL_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

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

# Command template text per asset (template-only; never executed here).
COMMAND_TEMPLATE_TEXT: Dict[str, str] = {
    "supervision": "TEMPLATE_ONLY_DO_NOT_EXECUTE: python -m pip install 'supervision==<pinned>'",
    "byte_track": "TEMPLATE_ONLY_DO_NOT_EXECUTE: python -m pip install 'bytetracker==<pinned>'",
    "deep_sort": "TEMPLATE_ONLY_DO_NOT_EXECUTE: python -m pip install 'deep-sort-realtime==<pinned>'",
    "midas": "TEMPLATE_ONLY_DO_NOT_EXECUTE: python -m pip install 'timm==<pinned>' 'midas==<pinned>'",
    "mobile_sam": "TEMPLATE_ONLY_DO_NOT_EXECUTE: python -m pip install 'mobile-sam @ git+<pinned-ref>'",
}

# Pre-execution snapshot requirement items.
PRE_EXECUTION_SNAPSHOT_ITEMS: Tuple[str, ...] = (
    "python_version_capture_required",
    "pip_freeze_capture_required",
    "package_list_capture_required",
    "path_env_capture_required",
    "registry_snapshot_required",
    "test_board_snapshot_required",
    "rollback_snapshot_required",
    "snapshot_must_be_written_before_first_install",
    "snapshot_artifact_protected",
    "snapshot_non_deletable",
)

# Final stop conditions (>= 18).
FINAL_STOP_CONDITIONS: Tuple[str, ...] = (
    "pre_snapshot_missing",
    "test_board_unwritable",
    "command_not_whitelisted",
    "command_scope_changed",
    "package_install_failure",
    "dependency_conflict",
    "unexpected_package_overwrite",
    "version_drift",
    "license_mismatch",
    "import_side_effect_risk",
    "rollback_unavailable",
    "post_probe_failure",
    "network_download_attempted_without_scope",
    "weight_download_attempted_without_scope",
    "runtime_flag_enabled",
    "inference_flag_enabled",
    "output_adapter_flag_enabled",
    "semantic_promotion_flag_enabled",
)

# Rollback trigger conditions reference.
ROLLBACK_TRIGGER_CONDITIONS: Tuple[str, ...] = (
    "package_install_failure",
    "dependency_conflict",
    "unexpected_package_overwrite",
    "version_drift",
    "license_mismatch",
    "import_side_effect_risk",
    "post_probe_failure",
    "test_board_write_failure",
)

# Approval issuance scope audit spec: (field, comparator, expected).
ISSUANCE_AUDIT_SPEC: Tuple[Tuple[str, str, Any], ...] = (
    ("final_decision", "eq", UPSTREAM_ISSUANCE_EXPECTED_GO),
    ("blocker_count", "eq", 0),
    ("owner_approval_issuance_created", "eq", True),
    ("owner_approval_granted_for_install_execution_preparation", "eq", True),
    ("owner_approval_granted_for_install_execution", "eq", False),
)
# Nested fields verified from owner_approval_issuance_record / go_conditions.
ISSUANCE_NESTED_BOOL_FIELDS: Tuple[str, ...] = (
    "approval_issuance_success_not_install_execution_approval",
    "approval_issuance_success_not_inference_approval",
    "approval_issuance_success_not_runtime_approval",
    "approval_issuance_success_not_output_adapter_approval",
    "approval_issuance_success_not_semantic_layer_approval",
)

SEALED_EXPECTED_ISSUANCE: Dict[str, Any] = {
    "final_decision": UPSTREAM_ISSUANCE_EXPECTED_GO,
    "blocker_count": 0,
    "owner_approval_issuance_created": True,
    "owner_approval_granted_for_install_execution_preparation": True,
    "owner_approval_granted_for_install_execution": False,
    "approval_scope": APPROVAL_SCOPE,
    "direct_install_execution_not_allowed_after_this_phase": True,
}

# --------------------------------------------------------------------------- #
# Negative guards (26: A..Z).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_issuance_as_install_execution_approval", "go_key": "approval_issuance_success_not_install_execution_approval", "depends_on": "approval_issuance_not_install_execution_approval"},
    {"guard_id": "invalid_b_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_c_model_weight_dataset_download_executed", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_d_inference_executed", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_e_runtime_output_adapter_semantic_entered", "go_key": "no_runtime_output_adapter_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_f_execution_preparation_package_missing", "go_key": "execution_preparation_package_present", "depends_on": "execution_preparation_package_present"},
    {"guard_id": "invalid_g_approval_scope_not_preparation_only", "go_key": "approval_scope_preparation_only", "depends_on": "approval_scope_preparation_only"},
    {"guard_id": "invalid_h_approved_assets_incomplete", "go_key": "approved_assets_complete", "depends_on": "approved_assets_complete"},
    {"guard_id": "invalid_i_excluded_assets_enter_scope", "go_key": "excluded_assets_remain_excluded", "depends_on": "excluded_assets_remain_excluded"},
    {"guard_id": "invalid_j_final_command_whitelist_missing", "go_key": "final_command_whitelist_present", "depends_on": "final_command_whitelist_present"},
    {"guard_id": "invalid_k_final_command_whitelist_executed", "go_key": "final_command_whitelist_not_executed", "depends_on": "final_command_whitelist_not_executed"},
    {"guard_id": "invalid_l_pre_execution_snapshot_requirement_missing", "go_key": "pre_execution_snapshot_required", "depends_on": "pre_execution_snapshot_required"},
    {"guard_id": "invalid_m_final_execution_order_not_locked", "go_key": "final_execution_order_locked", "depends_on": "final_execution_order_locked"},
    {"guard_id": "invalid_n_failure_does_not_stop_downstream", "go_key": "failure_stops_downstream", "depends_on": "failure_stops_downstream"},
    {"guard_id": "invalid_o_rollback_requirement_missing", "go_key": "final_rollback_ready", "depends_on": "rollback_requirement_present"},
    {"guard_id": "invalid_p_post_install_probe_requirement_missing", "go_key": "final_post_install_probe_ready", "depends_on": "post_install_probe_requirement_present"},
    {"guard_id": "invalid_q_probe_allows_import_load_inference_runtime_adapter", "go_key": "post_install_probe_find_spec_only_strict", "depends_on": "post_install_probe_find_spec_only_strict"},
    {"guard_id": "invalid_r_weight_download_approved_by_default", "go_key": "weight_download_not_approved_by_default", "depends_on": "weight_download_not_approved_by_default"},
    {"guard_id": "invalid_s_next_execution_package_and_weight_without_separate_approval", "go_key": "weight_download_requires_separate_approval", "depends_on": "weight_download_requires_separate_approval"},
    {"guard_id": "invalid_t_readiness_allows_inference_runtime_adapter_semantic", "go_key": "readiness_excludes_inference_runtime_adapter_semantic", "depends_on": "readiness_excludes_inference_runtime_adapter_semantic"},
    {"guard_id": "invalid_u_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_v_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_w_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_x_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_y_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_z_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (45 phase + 6 test board = 51).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_is_a_compressed_execution_preparation_and_readiness_review_phase",
    "owner_approval_issuance_post_review_is_included",
    "execution_preparation_is_included",
    "execution_readiness_review_is_included",
    "approval_issuance_remains_limited_to_execution_preparation",
    "approval_issuance_is_not_install_execution_approval",
    "no_pip_install_is_allowed_in_this_phase",
    "no_dependency_install_is_allowed_in_this_phase",
    "no_model_download_is_allowed_in_this_phase",
    "no_weight_download_is_allowed_in_this_phase",
    "no_dataset_download_is_allowed_in_this_phase",
    "no_real_inference_is_allowed_in_this_phase",
    "runtime_execution_is_not_allowed_in_this_phase",
    "output_adapter_is_not_allowed_in_this_phase",
    "semantic_layer_is_not_allowed_in_this_phase",
    "execution_preparation_package_is_required",
    "approved_asset_scope_is_limited_to_five_install_candidates",
    "excluded_assets_must_remain_excluded",
    "final_command_whitelist_is_required",
    "final_command_whitelist_must_not_be_executed_in_this_phase",
    "pre_execution_snapshot_is_required_before_next_execution_phase",
    "final_execution_order_is_locked",
    "failed_step_must_stop_downstream_execution",
    "final_rollback_requirement_is_required",
    "final_post_install_probe_requirement_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "post_install_probe_is_not_output_adapter",
    "package_install_execution_scope_may_be_prepared_for_next_phase",
    "weight_download_is_not_approved_by_default",
    "weight_download_requires_separate_approval",
    "next_execution_phase_may_install_packages_only_unless_separate_weight_approval_is_granted",
    "readiness_review_is_not_install_execution",
    "readiness_review_is_not_inference_approval",
    "readiness_review_is_not_runtime_approval",
    "readiness_review_is_not_output_adapter_approval",
    "readiness_review_is_not_semantic_layer_approval",
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

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionPreparationReadinessProfile",
    "ApprovalIssuanceScopeAudit",
    "ExecutionPreparationPackage",
    "PreExecutionSnapshotRequirement",
    "FinalCommandWhitelistRecord",
    "FinalExecutionOrderRecord",
    "FinalStopConditionRecord",
    "FinalRollbackRequirement",
    "FinalPostInstallProbeRequirement",
    "PackageInstallExecutionScope",
    "WeightDownloadExecutionScope",
    "ExecutionRiskReadinessRecord",
    "ExecutionReadinessReviewRecord",
    "ExecutionHandoffRecord",
    "NegativeExecutionPreparationReadinessGuard",
    "P1ControlledInstallExecutionPreparationReadinessDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PREPARATION_AND_READINESS_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_PREPARATION_AND_READINESS_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}

CAN_ENTER_FLAGS: Dict[str, bool] = {
    "can_enter_controlled_install_execution_next": True,
    "can_enter_weight_download_execution_next": False,
    "can_enter_inference": False,
    "can_enter_runtime": False,
    "can_enter_output_adapter": False,
    "can_enter_semantic_layer": False,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "install_execution_allowed_in_this_phase": False,
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
class P1ControlledInstallExecutionPreparationReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    approval_issuance_post_review_included: bool
    execution_preparation_included: bool
    execution_readiness_review_included: bool
    execution_preparation_package_created: bool
    execution_readiness_decision_created: bool
    can_enter_controlled_install_execution_next: bool
    install_execution_allowed_in_this_phase: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    upstream_issuance_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    approved_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ApprovalIssuanceScopeAudit:
    artifact_ref: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    approval_scope: str
    direct_install_execution_not_allowed_after_this_phase: bool
    checks_total: int
    checks_passed: int
    field_results: Tuple[Dict[str, Any], ...]
    audit_holds: bool


@dataclass(frozen=True)
class ExecutionPreparationPackage:
    preparation_package_id: str
    phase_id: str
    source_approval_issuance_ref: str
    source_request_ref: str
    approved_assets: Tuple[str, ...]
    excluded_assets: Tuple[str, ...]
    final_command_whitelist_refs: Tuple[str, ...]
    final_execution_order: Tuple[str, ...]
    final_stop_conditions: Tuple[str, ...]
    pre_execution_snapshot_required: bool
    rollback_required: bool
    post_install_probe_required: bool
    test_board_write_required: bool
    package_install_scope_defined: bool
    weight_download_scope_defined: bool
    execution_preparation_complete: bool
    install_execution_allowed_in_this_phase: bool


@dataclass(frozen=True)
class PreExecutionSnapshotRequirement:
    requirement_ref: str
    python_version_capture_required: bool
    pip_freeze_capture_required: bool
    package_list_capture_required: bool
    path_env_capture_required: bool
    registry_snapshot_required: bool
    test_board_snapshot_required: bool
    rollback_snapshot_required: bool
    snapshot_must_be_written_before_first_install: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool
    snapshot_executed_in_this_phase: bool


@dataclass(frozen=True)
class FinalCommandWhitelistRecord:
    asset_id: str
    command_template_ref: str
    command_template_text: str
    template_only_marker_present: bool
    command_not_executed_in_this_phase: bool
    command_allowed_only_in_next_execution_phase: bool
    command_requires_pre_snapshot: bool
    command_requires_stop_condition_check: bool
    command_requires_rollback_available: bool
    command_requires_post_probe: bool


@dataclass(frozen=True)
class FinalExecutionOrderRecord:
    asset_id: str
    order_index: int
    no_parallel_execution: bool
    failure_stops_downstream: bool
    order_change_requires_new_review: bool
    order_change_requires_owner_reapproval: bool


@dataclass(frozen=True)
class FinalStopConditionRecord:
    condition_id: str
    enforced_in_next_execution_phase: bool


@dataclass(frozen=True)
class FinalRollbackRequirement:
    asset_id: str
    rollback_required: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_template_ref: str
    rollback_command_not_executed_in_this_phase: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool


@dataclass(frozen=True)
class FinalPostInstallProbeRequirement:
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


@dataclass(frozen=True)
class PackageInstallExecutionScope:
    asset_id: str
    package_install_allowed_in_next_execution_phase: bool
    package_install_executed_in_this_phase: bool
    pip_install_executed_in_this_phase: bool
    dependency_install_executed_in_this_phase: bool


@dataclass(frozen=True)
class WeightDownloadExecutionScope:
    asset_id: str
    weight_download_required: bool
    weight_download_requires_separate_approval: bool
    weight_download_allowed_in_next_execution_phase: bool
    weight_download_subapproval_requested: bool
    weight_download_scope_not_approved: bool


@dataclass(frozen=True)
class ExecutionRiskReadinessRecord:
    asset_id: str
    dependency_risk_ready: bool
    license_risk_ready: bool
    weight_risk_ready: bool
    environment_risk_ready: bool
    rollback_risk_ready: bool
    owner_ack_required_for_next_phase: bool


@dataclass(frozen=True)
class ExecutionReadinessReviewRecord:
    review_ref: str
    approval_scope_valid: bool
    preparation_package_complete: bool
    approved_assets_verified: bool
    excluded_assets_verified: bool
    final_command_whitelist_ready: bool
    final_execution_order_ready: bool
    final_stop_conditions_ready: bool
    final_rollback_ready: bool
    final_post_install_probe_ready: bool
    package_install_scope_ready: bool
    weight_download_scope_not_approved: bool
    test_board_ready: bool
    non_execution_boundary_preserved: bool
    can_enter_controlled_install_execution_next: bool
    can_enter_weight_download_execution_next: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_output_adapter: bool
    can_enter_semantic_layer: bool
    readiness_holds: bool


@dataclass(frozen=True)
class ExecutionHandoffRecord:
    target_ref: str
    readiness_recorded: bool
    can_enter_controlled_install_execution_next: bool
    package_install_only_recommended_first: bool
    weight_download_deferred_to_subapproval: bool


@dataclass
class NegativeExecutionPreparationReadinessGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallExecutionPreparationReadinessDecision:
    decision_ref: str
    execution_preparation_readiness_profile_count: int
    approval_issuance_scope_audit_count: int
    execution_preparation_package_count: int
    approved_asset_preparation_count: int
    excluded_asset_preparation_count: int
    pre_execution_snapshot_requirement_count: int
    final_command_whitelist_count: int
    final_execution_order_count: int
    final_stop_condition_count: int
    final_rollback_requirement_count: int
    final_post_install_probe_requirement_count: int
    package_install_execution_scope_count: int
    weight_download_execution_scope_count: int
    execution_readiness_review_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
