# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Planning — types v1.

Controlled install EXECUTION PLANNING (NOT install execution). It normalizes the
approval gate, pre-install environment snapshot, install command whitelist,
execution order lock, stop conditions, rollback execution plan, post-install
probe plan, execution audit plan, risk matrix and permission boundary that any
FUTURE real controlled install must satisfy.

It does NOT run pip install, NOT install dependencies, NOT download
models/weights/datasets, NOT run inference, NOT enter runtime, NOT enter the
semantic layer, NOT trigger navigation / action / speech / fact_write. Execution
planning success is NOT install-execution / inference / runtime / output-adapter
/ semantic-layer approval.
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
SCOPE = "p1_controlled_install_execution_planning"
SOURCE_CHAIN = "p1_controlled_install_execution_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001，规划未来 controlled install "
    "execution 的审批门、环境快照、命令白名单、执行顺序锁、回滚触发、post-install probe、审计记录和测试板块证据。"
    "该阶段是 execution planning，不是 install execution。不执行 pip install、不安装依赖、不下载模型/权重/数据集、"
    "不执行 inference、不进入 runtime、不进入语义层、不触发 navigation/action/speech/fact_write。"
    "execution planning 成功不等于 install execution / inference / runtime / output adapter / semantic layer 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_planning_is_plan_only_no_install_no_download_no_inference_no_runtime_no_approval_granted"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
EXECUTION_PLANNING_ONLY = True
INSTALL_EXECUTION_ALLOWED = False
OWNER_APPROVAL_REQUIRED = True
OWNER_APPROVAL_NOT_GRANTED_IN_THIS_PHASE = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

CONTROLLED_INSTALL_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"
CONTROLLED_INSTALL_PLANNING_REF = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"
RECONCILIATION_POST_REVIEW_REF = (
    "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
)
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001"

CONTROLLED_INSTALL_POST_REVIEW_EXPECTED_GO = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_POST_REVIEW_GO"
CONTROLLED_INSTALL_PLANNING_EXPECTED_GO = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding.
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Upstream artifact (controlled-install-planning) used for per-asset detail.
# --------------------------------------------------------------------------- #
CONTROLLED_INSTALL_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_planning_dryrun_v1_smoke_v0/"
    "p1_controlled_install_planning_dryrun_review_v1.json"
)

# --------------------------------------------------------------------------- #
# Candidate / excluded scope (locked; must match post-review).
# --------------------------------------------------------------------------- #
CANDIDATE_ASSET_IDS: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)

# Locked execution order (asset_id, order_index, reason).
EXECUTION_ORDER_LOCK: Tuple[Tuple[str, int, str], ...] = (
    ("supervision", 1, "utility_wrapper_first_no_model_weight_low_risk_shared_cv_core"),
    ("byte_track", 2, "tracking_core_depends_on_detector_output_after_utility"),
    ("deep_sort", 3, "tracking_with_optional_reid_after_byte_track"),
    ("midas", 4, "depth_hint_after_tracking_stack_before_segmentation"),
    ("mobile_sam", 5, "segmentation_last_heaviest_optional_weight_gated"),
)

EXCLUDED_ASSET_IDS: Tuple[str, ...] = (
    "fast_sam",
    "yolov8n",
    "pyannote",
    "sam2",
    "depth_anything",
    "zoe_depth",
    "grounding_dino",
    "scene_relation_vlm",
    "open_vocab_vlm",
    "sense_voice",
    "emotion_multimodal_bridge",
    "rt_detr",
)

# Assets that do not require a model weight (per upstream weight plans).
NO_WEIGHT_ASSETS: Tuple[str, ...] = ("supervision", "byte_track")
WEIGHT_HANDLED_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

# --------------------------------------------------------------------------- #
# Stop conditions (>= 12; 14 specified).
# --------------------------------------------------------------------------- #
STOP_CONDITIONS: Tuple[Dict[str, str], ...] = (
    {"condition_id": "owner_approval_missing", "severity": "blocker"},
    {"condition_id": "pre_install_snapshot_missing", "severity": "blocker"},
    {"condition_id": "command_not_whitelisted", "severity": "blocker"},
    {"condition_id": "dependency_conflict_detected", "severity": "blocker"},
    {"condition_id": "unexpected_package_overwrite_risk", "severity": "blocker"},
    {"condition_id": "license_mismatch", "severity": "blocker"},
    {"condition_id": "version_drift", "severity": "blocker"},
    {"condition_id": "import_side_effect_risk", "severity": "blocker"},
    {"condition_id": "test_board_write_failure", "severity": "blocker"},
    {"condition_id": "rollback_plan_missing", "severity": "blocker"},
    {"condition_id": "post_install_probe_plan_missing", "severity": "blocker"},
    {"condition_id": "runtime_or_inference_flag_accidentally_enabled", "severity": "blocker"},
    {"condition_id": "network_download_attempted_without_approval", "severity": "blocker"},
    {"condition_id": "weight_download_attempted_without_approval", "severity": "blocker"},
)

# --------------------------------------------------------------------------- #
# Rollback trigger conditions.
# --------------------------------------------------------------------------- #
ROLLBACK_TRIGGER_CONDITIONS: Tuple[str, ...] = (
    "dependency_conflict",
    "import_probe_still_missing_after_future_install",
    "version_drift",
    "package_import_side_effect_risk",
    "license_mismatch",
    "environment_corruption",
    "unexpected_package_overwrite",
    "test_board_write_failure",
    "post_install_probe_failure",
    "weight_visibility_failure",
)

# --------------------------------------------------------------------------- #
# Execution audit trace items (>= 10).
# --------------------------------------------------------------------------- #
AUDIT_TRACE_ITEMS: Tuple[str, ...] = (
    "approval_trace",
    "pre_snapshot_trace",
    "command_whitelist_trace",
    "execution_order_trace",
    "stop_condition_trace",
    "rollback_trace",
    "post_install_probe_trace",
    "test_board_trace",
    "no_runtime_trace",
    "no_inference_trace",
)

# --------------------------------------------------------------------------- #
# Permission boundary statements (>= 5; 6 specified).
# --------------------------------------------------------------------------- #
PERMISSION_BOUNDARY_STATEMENTS: Tuple[Dict[str, Any], ...] = (
    {"boundary_id": "execution_planning_success_not_install_execution_approval", "value_is_true": True},
    {"boundary_id": "execution_planning_success_not_inference_approval", "value_is_true": True},
    {"boundary_id": "execution_planning_success_not_runtime_approval", "value_is_true": True},
    {"boundary_id": "execution_planning_success_not_output_adapter_approval", "value_is_true": True},
    {"boundary_id": "execution_planning_success_not_semantic_layer_approval", "value_is_true": True},
    {"boundary_id": "commercial_runtime_approved", "value_is_true": False},
)

# --------------------------------------------------------------------------- #
# Negative guards (22: A..V).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_b_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_c_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_d_whitelist_as_execution_approval", "go_key": "command_whitelist_not_execution_approval", "depends_on": "command_whitelist_not_execution_approval"},
    {"guard_id": "invalid_e_owner_approval_gate_missing", "go_key": "owner_approval_gate_present", "depends_on": "owner_approval_gate_present"},
    {"guard_id": "invalid_f_pre_install_snapshot_plan_missing", "go_key": "pre_install_snapshot_planned", "depends_on": "pre_install_snapshot_planned"},
    {"guard_id": "invalid_g_rollback_execution_plan_missing", "go_key": "rollback_execution_planned", "depends_on": "rollback_execution_planned"},
    {"guard_id": "invalid_h_post_install_probe_plan_missing", "go_key": "post_install_probe_planned", "depends_on": "post_install_probe_planned"},
    {"guard_id": "invalid_i_execution_order_not_locked", "go_key": "execution_order_locked", "depends_on": "execution_order_locked"},
    {"guard_id": "invalid_j_failure_allows_downstream_continue", "go_key": "execution_must_stop_on_failure", "depends_on": "execution_must_stop_on_failure"},
    {"guard_id": "invalid_k_excluded_asset_in_execution_planning", "go_key": "excluded_assets_not_in_execution_planning", "depends_on": "excluded_assets_not_in_execution_planning"},
    {"guard_id": "invalid_l_planning_as_install_execution_approval", "go_key": "execution_planning_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_m_planning_as_inference_approval", "go_key": "execution_planning_success_not_inference_approval", "depends_on": "not_inference_approval"},
    {"guard_id": "invalid_n_planning_as_runtime_approval", "go_key": "execution_planning_success_not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_o_planning_as_real_output_adapter_approval", "go_key": "execution_planning_success_not_output_adapter_approval", "depends_on": "not_output_adapter_approval"},
    {"guard_id": "invalid_p_planning_as_semantic_layer_approval", "go_key": "execution_planning_success_not_semantic_layer_approval", "depends_on": "not_semantic_layer_approval"},
    {"guard_id": "invalid_q_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_r_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_s_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_t_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_u_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_v_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (41 phase + 6 test board = 47).
# --------------------------------------------------------------------------- #
EXECUTION_PLANNING_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_install_execution_planning_only",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "install_execution_is_not_allowed_in_this_phase",
    "owner_approval_gate_is_required",
    "owner_approval_is_not_granted_in_this_phase",
    "pre_install_snapshot_plan_is_required",
    "install_command_whitelist_plan_is_required",
    "command_whitelist_is_not_execution_approval",
    "install_execution_order_lock_is_required",
    "failed_step_must_stop_downstream_execution",
    "rollback_execution_plan_is_required",
    "rollback_template_must_not_be_executed",
    "post_install_probe_plan_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "future_install_execution_requires_separate_approval",
    "execution_planning_success_is_not_install_execution_approval",
    "execution_planning_success_is_not_inference_approval",
    "execution_planning_success_is_not_runtime_approval",
    "execution_planning_success_is_not_real_output_adapter_approval",
    "execution_planning_success_is_not_semantic_layer_approval",
    "excluded_assets_must_not_enter_execution_planning",
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
    EXECUTION_PLANNING_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionPlanningProfile",
    "OwnerApprovalGatePlan",
    "PreInstallEnvironmentSnapshotPlan",
    "InstallCommandWhitelistPlan",
    "InstallExecutionOrderLock",
    "InstallExecutionStopCondition",
    "RollbackExecutionPlan",
    "PostInstallProbePlan",
    "InstallExecutionAuditPlan",
    "InstallExecutionRiskMatrix",
    "InstallExecutionPermissionBoundary",
    "ControlledInstallExecutionReadinessRecord",
    "NegativeInstallExecutionPlanningGuard",
    "P1ControlledInstallExecutionPlanningDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_execution_planning_post_review_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}

PLANNING_TRUE_INVARIANTS: Dict[str, bool] = {
    "execution_planning_only": True,
    "owner_approval_required": True,
    "owner_approval_not_granted_in_this_phase": True,
    "pre_install_snapshot_planned": True,
    "install_command_whitelist_planned": True,
    "command_whitelist_not_execution_approval": True,
    "execution_order_locked": True,
    "order_change_requires_review": True,
    "execution_must_stop_on_failure": True,
    "rollback_execution_planned": True,
    "rollback_template_not_executed": True,
    "post_install_probe_planned": True,
    "post_install_probe_find_spec_only": True,
    "post_install_probe_not_inference": True,
    "post_install_probe_not_runtime": True,
    "excluded_assets_not_in_execution_planning": True,
    "future_install_execution_requires_separate_approval": True,
    "execution_planning_success_not_install_execution_approval": True,
    "execution_planning_success_not_inference_approval": True,
    "execution_planning_success_not_runtime_approval": True,
    "execution_planning_success_not_output_adapter_approval": True,
    "execution_planning_success_not_semantic_layer_approval": True,
    "candidate_only_boundary_preserved": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
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
class P1ControlledInstallExecutionPlanningProfile:
    profile_ref: str
    phase_id: str
    execution_planning_only: bool
    install_execution_allowed: bool
    owner_approval_required: bool
    owner_approval_not_granted_in_this_phase: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    controlled_install_post_review_ref: str
    controlled_install_planning_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    candidate_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class OwnerApprovalGatePlan:
    gate_ref: str
    owner_approval_required: bool
    owner_approval_record_required: bool
    owner_approval_granted_in_this_phase: bool
    approval_scope: str
    approval_does_not_allow_inference: bool
    approval_does_not_allow_runtime: bool
    approval_does_not_allow_weight_download_unless_separately_approved: bool
    approval_expiry_policy: str
    approval_revocation_policy: str
    approval_trace_ref_required: bool


@dataclass(frozen=True)
class PreInstallEnvironmentSnapshotPlan:
    plan_ref: str
    pre_install_snapshot_required: bool
    target_env_label: str
    python_version_capture_required: bool
    pip_freeze_capture_required: bool
    package_list_capture_required: bool
    path_env_capture_required: bool
    registry_snapshot_required: bool
    test_board_snapshot_required: bool
    rollback_snapshot_required: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool
    snapshot_must_not_overwrite_test_board: bool
    snapshot_must_not_overwrite_registry: bool
    snapshot_executed_in_this_phase: bool


@dataclass(frozen=True)
class InstallCommandWhitelistPlan:
    command_template_id: str
    asset_id: str
    command_template: str
    template_only: bool
    command_not_executed: bool
    whitelist_required_before_execution: bool
    shell_execution_allowed_now: bool
    subprocess_execution_allowed_now: bool
    pip_install_allowed_now: bool
    command_requires_owner_approval: bool
    command_requires_pre_snapshot: bool
    command_requires_rollback_plan: bool
    contains_install_or_download_token: bool
    allowed_now: bool


@dataclass(frozen=True)
class InstallExecutionOrderLock:
    asset_id: str
    locked_order_index: int
    order_lock_reason: str
    order_change_requires_review: bool
    order_change_requires_owner_approval: bool
    execution_must_stop_on_failure: bool
    downstream_steps_blocked_on_failure: bool
    parallel_install_allowed: bool


@dataclass(frozen=True)
class InstallExecutionStopCondition:
    condition_id: str
    severity: str
    halts_execution: bool
    requires_owner_review: bool


@dataclass(frozen=True)
class RollbackExecutionPlan:
    asset_id: str
    rollback_plan_required: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_command_template: str
    rollback_command_not_executed: bool
    rollback_requires_owner_acknowledgement: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool


@dataclass(frozen=True)
class PostInstallProbePlan:
    asset_id: str
    post_install_probe_required: bool
    probe_uses_find_spec_only: bool
    real_import_allowed: bool
    no_model_load_on_probe: bool
    no_inference_on_probe: bool
    installed_version_record_required: bool
    dependency_gap_recheck_required: bool
    license_recheck_required: bool
    weight_visibility_recheck_required: bool
    test_board_probe_record_required: bool


@dataclass(frozen=True)
class InstallExecutionAuditPlan:
    trace_id: str
    trace_required: bool
    writes_to_test_board_protected_record: bool


@dataclass(frozen=True)
class InstallExecutionRiskMatrix:
    asset_id: str
    risk_level: str
    risk_reason: str
    dependency_risk: str
    license_risk: str
    weight_risk: str
    environment_risk: str
    rollback_risk: str
    install_execution_allowed: bool
    can_enter_future_install_execution_request: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    can_enter_inference: bool


@dataclass(frozen=True)
class InstallExecutionPermissionBoundary:
    boundary_id: str
    holds: bool


@dataclass(frozen=True)
class ControlledInstallExecutionReadinessRecord:
    asset_id: str
    owner_approval_gate_ready: bool
    snapshot_plan_ready: bool
    command_whitelist_ready: bool
    order_lock_ready: bool
    rollback_plan_ready: bool
    post_install_probe_ready: bool
    install_execution_allowed: bool
    can_enter_future_install_execution_request: bool


@dataclass
class NegativeInstallExecutionPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallExecutionPlanningDecision:
    decision_ref: str
    execution_planning_profile_count: int
    owner_approval_gate_plan_count: int
    pre_install_environment_snapshot_plan_count: int
    install_command_whitelist_plan_count: int
    install_execution_order_lock_count: int
    install_execution_stop_condition_count: int
    rollback_execution_plan_count: int
    post_install_probe_plan_count: int
    install_execution_audit_plan_count: int
    install_execution_risk_matrix_count: int
    install_execution_permission_boundary_count: int
    controlled_install_execution_readiness_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
