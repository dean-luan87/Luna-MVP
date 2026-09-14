# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Planning Post-Review — types v1.

PURE post-review of Phase-P1-Controlled-Install-Execution-Planning-v1-001. Audits
the owner approval gate, pre-install snapshot plan, install command whitelist,
execution order lock, stop conditions, rollback execution plan, post-install
probe plan, execution audit plan, risk matrix, permission boundary, the upstream
test board planning records, and the non-execution boundary.

It mutates NO execution plan, generates NO new install command, generates NO
owner approval, runs NO pip install, installs NO dependency, downloads NO
model/weight/dataset, runs NO inference, enters NO runtime, enters NO semantic
layer. Post-review success is NOT owner / install-execution / inference / runtime
/ output-adapter / semantic-layer approval.
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001"
SCOPE = "p1_controlled_install_execution_planning_post_review"
SOURCE_CHAIN = "p1_controlled_install_execution_planning_post_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Execution-Planning-v1-001，执行纯事后复核。不修改 execution planning、"
    "不新增 install command、不生成 owner approval、不执行 pip install、不安装依赖、不下载模型/权重/数据集、"
    "不执行 inference、不进入 runtime、不进入语义层。只复核 owner approval gate、pre-install snapshot、command "
    "whitelist、execution order lock、stop conditions、rollback plan、post-install probe plan、audit plan、"
    "risk matrix、permission boundary、测试板块记录和 non-execution 边界。post-review 成功不等于 owner / install "
    "execution / inference / runtime / output adapter / semantic layer 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_planning_post_review_is_audit_only_no_mutation_no_command_no_approval_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
EXECUTION_PLANNING_MUTATION_ALLOWED = False
NEW_INSTALL_COMMAND_GENERATION_ALLOWED = False
OWNER_APPROVAL_GENERATION_ALLOWED = False
INSTALL_EXECUTION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
CONTROLLED_INSTALL_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"
CONTROLLED_INSTALL_PLANNING_REF = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-Request-v1-001"

EXECUTION_PLANNING_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding.
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "post_review"

# --------------------------------------------------------------------------- #
# Upstream artifact + upstream test board paths.
# --------------------------------------------------------------------------- #
UPSTREAM_REVIEW_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_execution_planning_v1_smoke_v0/"
    "p1_controlled_install_execution_planning_review_v1.json"
)
UPSTREAM_TEST_BOARD_REL = (
    "capabilities/test_board/recognition_models/"
    "phase_p1_controlled_install_execution_planning_v1_001"
)
UPSTREAM_TEST_BOARD_STANDIN_REL = (
    "_tmp_eval_out/board_standin/capabilities/test_board/recognition_models/"
    "phase_p1_controlled_install_execution_planning_v1_001"
)
UPSTREAM_TEST_BOARD_RECORD_FILES: Tuple[str, ...] = (
    "test_process_record",
    "test_result_summary",
    "test_conclusion_record",
    "test_artifact_refs",
    "protected_marker",
    "non_deletable_notice",
    "test_board_manifest",
)
UPSTREAM_TEST_BOARD_EXPECTED_MODE = "planning"

# --------------------------------------------------------------------------- #
# Candidate / excluded scope (locked).
# --------------------------------------------------------------------------- #
EXPECTED_CANDIDATES: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)
EXPECTED_ORDER: Tuple[Tuple[str, int], ...] = (
    ("supervision", 1),
    ("byte_track", 2),
    ("deep_sort", 3),
    ("midas", 4),
    ("mobile_sam", 5),
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

# Stop conditions that must be covered (>= 12).
REQUIRED_STOP_CONDITIONS: Tuple[str, ...] = (
    "owner_approval_missing",
    "pre_install_snapshot_missing",
    "command_not_whitelisted",
    "dependency_conflict_detected",
    "unexpected_package_overwrite_risk",
    "license_mismatch",
    "version_drift",
    "import_side_effect_risk",
    "test_board_write_failure",
    "rollback_plan_missing",
    "post_install_probe_plan_missing",
    "runtime_or_inference_flag_accidentally_enabled",
    "network_download_attempted_without_approval",
    "weight_download_attempted_without_approval",
)

# Execution audit trace items (>= 10).
REQUIRED_AUDIT_TRACE_ITEMS: Tuple[str, ...] = (
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

TEMPLATE_ONLY_MARKER = "TEMPLATE_ONLY_DO_NOT_EXECUTE"

# --------------------------------------------------------------------------- #
# Sealed expected metrics (used for sealed_ref_fallback when artifact missing).
# --------------------------------------------------------------------------- #
SEALED_EXPECTED_METRICS: Dict[str, int] = {
    "owner_approval_gate_plan_count": 1,
    "pre_install_environment_snapshot_plan_count": 1,
    "install_command_whitelist_plan_count": 5,
    "install_execution_order_lock_count": 5,
    "install_execution_stop_condition_count": 14,
    "rollback_execution_plan_count": 5,
    "post_install_probe_plan_count": 5,
    "install_execution_audit_plan_count": 10,
    "install_execution_risk_matrix_count": 5,
    "install_execution_permission_boundary_count": 6,
    "negative_guard_passed": 22,
    "test_board_record_count": 6,
}

# Artifact audit spec: (field, op, value).
ARTIFACT_AUDIT_SPEC: Tuple[Dict[str, Any], ...] = (
    {"field": "final_decision", "op": "eq", "value": EXECUTION_PLANNING_EXPECTED_GO},
    {"field": "blocker_count", "op": "eq", "value": 0},
    {"field": "owner_approval_gate_plan_count", "op": "gte", "value": 1},
    {"field": "pre_install_environment_snapshot_plan_count", "op": "gte", "value": 1},
    {"field": "install_command_whitelist_plan_count", "op": "eq", "value": 5},
    {"field": "install_execution_order_lock_count", "op": "eq", "value": 5},
    {"field": "install_execution_stop_condition_count", "op": "gte", "value": 12},
    {"field": "rollback_execution_plan_count", "op": "eq", "value": 5},
    {"field": "post_install_probe_plan_count", "op": "eq", "value": 5},
    {"field": "install_execution_audit_plan_count", "op": "gte", "value": 10},
    {"field": "install_execution_risk_matrix_count", "op": "eq", "value": 5},
    {"field": "install_execution_permission_boundary_count", "op": "gte", "value": 5},
    {"field": "negative_guard_passed", "op": "eq", "value": 22},
    {"field": "test_board_record_count", "op": "gte", "value": 6},
)

# Non-execution boundary audit items (>= 16).
NON_EXECUTION_BOUNDARY_AUDIT_ITEMS: Tuple[str, ...] = (
    "real_install_performed",
    "dependency_install_performed",
    "pip_install_performed",
    "model_download_performed",
    "weight_download_performed",
    "dataset_download_performed",
    "real_inference_performed",
    "install_execution_allowed",
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

# Permission boundary statements that must be audited (>= 6).
REQUIRED_PERMISSION_BOUNDARIES: Tuple[str, ...] = (
    "execution_planning_success_not_install_execution_approval",
    "execution_planning_success_not_inference_approval",
    "execution_planning_success_not_runtime_approval",
    "execution_planning_success_not_output_adapter_approval",
    "execution_planning_success_not_semantic_layer_approval",
    "commercial_runtime_approved",
)

# --------------------------------------------------------------------------- #
# Negative post-review guards (27: A..Z, AA).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "upstream_final_decision_go_verified", "depends_on": "upstream_final_decision_go"},
    {"guard_id": "invalid_b_upstream_blocker_nonzero", "go_key": "upstream_blocker_count_zero_verified", "depends_on": "upstream_blocker_count_zero"},
    {"guard_id": "invalid_c_owner_approval_gate_missing", "go_key": "owner_approval_gate_verified", "depends_on": "owner_approval_gate_present"},
    {"guard_id": "invalid_d_owner_approval_granted_in_this_phase", "go_key": "owner_approval_not_granted", "depends_on": "owner_approval_not_granted"},
    {"guard_id": "invalid_e_pre_install_snapshot_missing", "go_key": "pre_install_snapshot_verified", "depends_on": "pre_install_snapshot_present"},
    {"guard_id": "invalid_f_command_whitelist_missing_or_lt_5", "go_key": "command_whitelist_verified", "depends_on": "command_whitelist_count_5"},
    {"guard_id": "invalid_g_command_whitelist_as_execution_approval", "go_key": "command_whitelist_not_execution_approval", "depends_on": "command_whitelist_not_execution_approval"},
    {"guard_id": "invalid_h_install_template_executed", "go_key": "install_templates_not_executed", "depends_on": "install_templates_not_executed"},
    {"guard_id": "invalid_i_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_j_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_k_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_l_execution_order_not_locked", "go_key": "execution_order_locked", "depends_on": "execution_order_locked"},
    {"guard_id": "invalid_m_failure_allows_downstream_continue", "go_key": "execution_must_stop_on_failure", "depends_on": "execution_must_stop_on_failure"},
    {"guard_id": "invalid_n_rollback_execution_plan_missing", "go_key": "rollback_execution_verified", "depends_on": "rollback_execution_present"},
    {"guard_id": "invalid_o_rollback_template_executed", "go_key": "rollback_template_not_executed", "depends_on": "rollback_template_not_executed"},
    {"guard_id": "invalid_p_post_install_probe_plan_missing", "go_key": "post_install_probe_verified", "depends_on": "post_install_probe_present"},
    {"guard_id": "invalid_q_probe_allows_import_load_inference", "go_key": "post_install_probe_find_spec_only", "depends_on": "post_install_probe_find_spec_only"},
    {"guard_id": "invalid_r_planning_as_install_execution_approval", "go_key": "post_review_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_s_planning_as_inference_runtime_adapter_semantic_approval", "go_key": "post_review_success_not_downstream_approval", "depends_on": "not_inference_runtime_adapter_semantic_approval"},
    {"guard_id": "invalid_t_excluded_asset_in_execution_planning", "go_key": "excluded_assets_not_in_execution_planning", "depends_on": "excluded_assets_not_in_execution_planning"},
    {"guard_id": "invalid_u_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_v_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_w_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_x_upstream_test_board_missing_or_not_planning", "go_key": "upstream_test_board_planning_record_verified", "depends_on": "upstream_test_board_planning_verified"},
    {"guard_id": "invalid_y_phase_does_not_write_post_review_test_board", "go_key": "post_review_test_board_record_required", "depends_on": "post_review_test_board_write_planned"},
    {"guard_id": "invalid_z_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_aa_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (47 phase + 6 test board = 53).
# --------------------------------------------------------------------------- #
POST_REVIEW_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_install_execution_planning_post_review_only",
    "no_execution_planning_mutation_is_allowed",
    "no_new_install_command_generation_is_allowed",
    "no_owner_approval_is_generated",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "install_execution_remains_disallowed",
    "owner_approval_gate_audit_is_required",
    "owner_approval_must_not_be_granted_in_this_phase",
    "pre_install_snapshot_audit_is_required",
    "command_whitelist_audit_is_required",
    "command_whitelist_is_not_execution_approval",
    "install_command_templates_must_remain_non_executed",
    "execution_order_lock_audit_is_required",
    "failed_step_must_stop_downstream_execution",
    "rollback_execution_audit_is_required",
    "rollback_template_must_not_be_executed",
    "post_install_probe_audit_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "future_install_execution_requires_separate_owner_approval",
    "post_review_success_is_not_owner_approval",
    "post_review_success_is_not_install_execution_approval",
    "post_review_success_is_not_inference_approval",
    "post_review_success_is_not_runtime_approval",
    "post_review_success_is_not_real_output_adapter_approval",
    "post_review_success_is_not_semantic_layer_approval",
    "excluded_assets_must_not_enter_execution_planning",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "semantic_promotion_is_not_allowed",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "upstream_planning_test_board_audit_is_required",
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
    "P1ControlledInstallExecutionPlanningPostReviewProfile",
    "ExecutionPlanningArtifactAudit",
    "OwnerApprovalGateAudit",
    "PreInstallSnapshotAudit",
    "CommandWhitelistAudit",
    "ExecutionOrderLockAudit",
    "StopConditionAudit",
    "RollbackExecutionAudit",
    "PostInstallProbeAudit",
    "ExecutionAuditPlanAudit",
    "RiskMatrixAudit",
    "PermissionBoundaryAudit",
    "UpstreamTestBoardPlanningRecordAudit",
    "NonExecutionBoundaryAudit",
    "NegativeInstallExecutionPlanningPostReviewGuard",
    "InstallExecutionRequestHandoffReadiness",
    "P1ControlledInstallExecutionPlanningPostReviewDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_execution_request_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "post_review_test_mode_reused": True,
}

POST_REVIEW_TRUE_INVARIANTS: Dict[str, bool] = {
    "upstream_final_decision_go_verified": True,
    "upstream_blocker_count_zero_verified": True,
    "owner_approval_gate_verified": True,
    "owner_approval_not_granted": True,
    "post_review_success_not_owner_approval": True,
    "pre_install_snapshot_verified": True,
    "command_whitelist_verified": True,
    "command_whitelist_not_execution_approval": True,
    "install_templates_not_executed": True,
    "execution_order_locked": True,
    "execution_must_stop_on_failure": True,
    "rollback_execution_verified": True,
    "rollback_template_not_executed": True,
    "post_install_probe_verified": True,
    "post_install_probe_find_spec_only": True,
    "post_install_probe_not_inference": True,
    "post_install_probe_not_runtime": True,
    "post_install_probe_not_output_adapter": True,
    "risk_matrix_verified": True,
    "permission_boundary_verified": True,
    "excluded_assets_not_in_execution_planning": True,
    "future_install_execution_requires_separate_owner_approval": True,
    "post_review_success_not_install_execution_approval": True,
    "post_review_success_not_inference_approval": True,
    "post_review_success_not_runtime_approval": True,
    "post_review_success_not_output_adapter_approval": True,
    "post_review_success_not_semantic_layer_approval": True,
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
    "install_execution_allowed": False,
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
class P1ControlledInstallExecutionPlanningPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    execution_planning_mutation_allowed: bool
    new_install_command_generation_allowed: bool
    owner_approval_generation_allowed: bool
    install_execution_allowed: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    execution_planning_ref: str
    controlled_install_post_review_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    expected_candidates: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ExecutionPlanningArtifactAudit:
    artifact_rel: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    upstream_final_decision: str
    checks_passed: int
    checks_total: int
    passed: bool


@dataclass(frozen=True)
class OwnerApprovalGateAudit:
    owner_approval_required: bool
    owner_approval_record_required: bool
    approval_scope_ok: bool
    owner_approval_not_granted_in_this_phase: bool
    approval_does_not_allow_inference: bool
    approval_does_not_allow_runtime: bool
    approval_does_not_allow_weight_download_unless_separately_approved: bool
    approval_trace_ref_required: bool
    post_review_success_not_owner_approval: bool
    passed: bool


@dataclass(frozen=True)
class PreInstallSnapshotAudit:
    pre_install_snapshot_required: bool
    target_env_label_present: bool
    python_version_capture_required: bool
    pip_freeze_capture_required: bool
    package_list_capture_required: bool
    path_env_capture_required: bool
    registry_snapshot_required: bool
    test_board_snapshot_required: bool
    rollback_snapshot_required: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool
    snapshot_not_executed_in_this_phase: bool
    passed: bool


@dataclass(frozen=True)
class CommandWhitelistAudit:
    asset_id: str
    command_template_present: bool
    template_only_marker_present: bool
    template_only: bool
    command_not_executed: bool
    whitelist_required_before_execution: bool
    shell_execution_allowed_now: bool
    subprocess_execution_allowed_now: bool
    pip_install_allowed_now: bool
    command_requires_owner_approval: bool
    command_requires_pre_snapshot: bool
    command_requires_rollback_plan: bool
    passed: bool


@dataclass(frozen=True)
class ExecutionOrderLockAudit:
    asset_id: str
    locked_order_index: int
    order_index_correct: bool
    order_lock_reason_present: bool
    order_change_requires_review: bool
    order_change_requires_owner_approval: bool
    execution_must_stop_on_failure: bool
    downstream_steps_blocked_on_failure: bool
    no_parallel_install_without_separate_approval: bool
    passed: bool


@dataclass(frozen=True)
class StopConditionAudit:
    condition_id: str
    present: bool
    halts_execution: bool


@dataclass(frozen=True)
class RollbackExecutionAudit:
    asset_id: str
    rollback_plan_required: bool
    rollback_trigger_conditions_present: bool
    rollback_command_template_present: bool
    rollback_command_not_executed: bool
    rollback_requires_owner_acknowledgement: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool
    passed: bool


@dataclass(frozen=True)
class PostInstallProbeAudit:
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
    passed: bool


@dataclass(frozen=True)
class ExecutionAuditPlanAudit:
    trace_id: str
    present: bool
    protected_test_board_writable: bool
    audit_only_in_this_phase: bool


@dataclass(frozen=True)
class RiskMatrixAudit:
    asset_id: str
    risk_level_present: bool
    dependency_risk_present: bool
    license_risk_present: bool
    weight_risk_present: bool
    environment_risk_present: bool
    rollback_risk_present: bool
    install_execution_allowed: bool
    can_enter_future_install_execution_request_planned_only: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    can_enter_inference: bool
    passed: bool


@dataclass(frozen=True)
class PermissionBoundaryAudit:
    boundary_id: str
    holds: bool


@dataclass(frozen=True)
class UpstreamTestBoardPlanningRecordAudit:
    record_type: str
    present: bool
    protected: bool
    non_deletable: bool
    deletion_forbidden: bool
    mode_planning: bool


@dataclass(frozen=True)
class NonExecutionBoundaryAudit:
    audit_item: str
    is_false: bool


@dataclass
class NegativeInstallExecutionPlanningPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class InstallExecutionRequestHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ControlledInstallExecutionPlanningPostReviewDecision:
    decision_ref: str
    execution_planning_post_review_profile_count: int
    execution_planning_artifact_audit_count: int
    owner_approval_gate_audit_count: int
    pre_install_snapshot_audit_count: int
    command_whitelist_audit_count: int
    execution_order_lock_audit_count: int
    stop_condition_audit_count: int
    rollback_execution_audit_count: int
    post_install_probe_audit_count: int
    execution_audit_plan_audit_count: int
    risk_matrix_audit_count: int
    permission_boundary_audit_count: int
    upstream_test_board_planning_record_audit_count: int
    non_execution_boundary_audit_count: int
    negative_post_review_guard_count: int
    negative_post_review_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
