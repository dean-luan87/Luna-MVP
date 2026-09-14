# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Request — types v1.

Generates an auditable owner-approval REQUEST package for P1 controlled install
execution. It only assembles request material (request scope, candidate assets,
command template references, snapshot requirements, risk summary, rollback
requirements, post-install probe requirements, test board evidence refs). It
does NOT grant approval and does NOT execute install.

Boundary chain enforced here:
  Request != Approval ; Approval != Execution ; Execution != Inference/Runtime.

No pip install, no dependency install, no model/weight/dataset download, no
inference, no runtime, no semantic layer, no navigation/action/speech/fact_write.
Request success is NOT owner / install-execution / inference / runtime /
output-adapter / semantic-layer approval.
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Request-v1-001"
SCOPE = "p1_controlled_install_execution_request"
SOURCE_CHAIN = "p1_controlled_install_execution_request_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001，生成 P1 受控安装执行的 owner "
    "approval request。Request ≠ Approval，Approval ≠ Execution，Execution ≠ Inference/Runtime。该阶段只生成请求材料、"
    "请求范围、候选资产、命令模板引用、快照要求、风险摘要、回滚要求、测试板块证据引用。不生成 approval、不执行 pip install、"
    "不安装依赖、不下载模型/权重/数据集、不执行 inference、不进入 runtime、不进入语义层。request 成功不等于 owner / install "
    "execution / inference / runtime / output adapter / semantic layer 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_request_is_request_material_only_no_approval_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
REQUEST_ONLY = True
OWNER_APPROVAL_REQUEST_CREATED = True
OWNER_APPROVAL_GRANTED = False
INSTALL_EXECUTION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

EXECUTION_PLANNING_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Planning-Post-Review-v1-001"
EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
CONTROLLED_INSTALL_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001"

EXECUTION_PLANNING_POST_REVIEW_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_POST_REVIEW_GO"
EXECUTION_PLANNING_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PLANNING_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding.
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Upstream artifacts used for request material (refs only, never executed).
# --------------------------------------------------------------------------- #
EXECUTION_PLANNING_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_execution_planning_v1_smoke_v0/"
    "p1_controlled_install_execution_planning_review_v1.json"
)

# Optional governance refs: if local Owner Approval / Record Approval GO
# artifacts exist they are recorded as optional context. This phase NEVER
# generates an approval, so these are non-gating.
OPTIONAL_GOVERNANCE_REFS: Tuple[Dict[str, str], ...] = (
    {
        "ref_id": "owner_approval_workflow",
        "artifact_rel": (
            "_tmp_eval_out/owner_approval_workflow_v1_smoke_v0/owner_approval_workflow_review_v1.json"
        ),
    },
    {
        "ref_id": "record_approval_governance",
        "artifact_rel": (
            "_tmp_eval_out/record_approval_governance_v1_smoke_v0/record_approval_governance_review_v1.json"
        ),
    },
)

# --------------------------------------------------------------------------- #
# Request scope (locked; must match execution planning).
# --------------------------------------------------------------------------- #
REQUESTED_ASSET_IDS: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)
REQUESTED_ORDER: Tuple[Tuple[str, int], ...] = (
    ("supervision", 1),
    ("byte_track", 2),
    ("deep_sort", 3),
    ("midas", 4),
    ("mobile_sam", 5),
)
NO_WEIGHT_ASSETS: Tuple[str, ...] = ("supervision", "byte_track")
WEIGHT_HANDLED_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

EXCLUDED_ASSETS: Tuple[Dict[str, str], ...] = (
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

# Pre-install snapshot request items.
PRE_INSTALL_SNAPSHOT_ITEMS: Tuple[str, ...] = (
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

# Rollback requirement reference triggers.
ROLLBACK_TRIGGER_REF_CONDITIONS: Tuple[str, ...] = (
    "dependency_conflict",
    "import_probe_still_missing_after_future_install",
    "version_drift",
    "package_import_side_effect_risk",
    "license_mismatch",
    "environment_corruption",
    "unexpected_package_overwrite",
    "test_board_write_failure",
)

# Request audit trace items (>= 8).
REQUEST_AUDIT_TRACE_ITEMS: Tuple[str, ...] = (
    "request_scope_trace",
    "command_template_ref_trace",
    "pre_install_snapshot_request_trace",
    "rollback_requirement_request_trace",
    "post_install_probe_requirement_request_trace",
    "risk_disclosure_trace",
    "excluded_asset_disclosure_trace",
    "owner_approval_request_trace",
    "permission_boundary_trace",
    "test_board_trace",
)

# Permission boundary statements (>= 6).
PERMISSION_BOUNDARY_STATEMENTS: Tuple[Dict[str, Any], ...] = (
    {"boundary_id": "request_success_not_owner_approval", "value_is_true": True},
    {"boundary_id": "request_success_not_install_execution_approval", "value_is_true": True},
    {"boundary_id": "request_success_not_inference_approval", "value_is_true": True},
    {"boundary_id": "request_success_not_runtime_approval", "value_is_true": True},
    {"boundary_id": "request_success_not_output_adapter_approval", "value_is_true": True},
    {"boundary_id": "request_success_not_semantic_layer_approval", "value_is_true": True},
    {"boundary_id": "commercial_runtime_approved", "value_is_true": False},
)

# --------------------------------------------------------------------------- #
# Negative guards (27: A..Z, AA).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_request_as_owner_approval", "go_key": "request_success_not_owner_approval", "depends_on": "request_success_not_owner_approval"},
    {"guard_id": "invalid_b_request_as_install_execution_approval", "go_key": "request_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_c_request_as_inference_approval", "go_key": "request_success_not_inference_approval", "depends_on": "not_inference_approval"},
    {"guard_id": "invalid_d_request_as_runtime_approval", "go_key": "request_success_not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_e_request_as_output_adapter_approval", "go_key": "request_success_not_output_adapter_approval", "depends_on": "not_output_adapter_approval"},
    {"guard_id": "invalid_f_request_as_semantic_layer_approval", "go_key": "request_success_not_semantic_layer_approval", "depends_on": "not_semantic_layer_approval"},
    {"guard_id": "invalid_g_no_request_package", "go_key": "request_package_complete", "depends_on": "request_package_complete"},
    {"guard_id": "invalid_h_owner_approval_request_record_missing", "go_key": "owner_approval_request_record_present", "depends_on": "owner_approval_request_record_present"},
    {"guard_id": "invalid_i_approval_granted_true", "go_key": "owner_approval_not_granted", "depends_on": "owner_approval_not_granted"},
    {"guard_id": "invalid_j_request_scope_includes_excluded", "go_key": "excluded_assets_not_in_request_scope", "depends_on": "excluded_assets_not_in_request_scope"},
    {"guard_id": "invalid_k_request_scope_includes_runtime_inference_semantic", "go_key": "request_scope_excludes_runtime_inference_semantic", "depends_on": "request_scope_excludes_runtime_inference_semantic"},
    {"guard_id": "invalid_l_request_scope_includes_unapproved_weight_download", "go_key": "request_scope_excludes_weight_download", "depends_on": "request_scope_excludes_weight_download"},
    {"guard_id": "invalid_m_new_install_command_generated", "go_key": "no_new_install_command", "depends_on": "no_new_install_command"},
    {"guard_id": "invalid_n_install_command_executed", "go_key": "request_does_not_execute_command", "depends_on": "request_does_not_execute_command"},
    {"guard_id": "invalid_o_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_p_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_q_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_r_pre_install_snapshot_request_missing", "go_key": "pre_install_snapshot_requested", "depends_on": "pre_install_snapshot_requested"},
    {"guard_id": "invalid_s_rollback_requirement_request_missing", "go_key": "rollback_requirement_requested", "depends_on": "rollback_requirement_requested"},
    {"guard_id": "invalid_t_post_install_probe_request_missing", "go_key": "post_install_probe_requested", "depends_on": "post_install_probe_requested"},
    {"guard_id": "invalid_u_probe_allows_import_load_inference_runtime_adapter", "go_key": "post_install_probe_find_spec_only_strict", "depends_on": "post_install_probe_find_spec_only_strict"},
    {"guard_id": "invalid_v_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_w_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_x_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_y_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_z_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_aa_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (43 phase + 6 test board = 49).
# --------------------------------------------------------------------------- #
REQUEST_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_install_execution_request_only",
    "request_is_not_owner_approval",
    "request_is_not_install_execution_approval",
    "request_is_not_inference_approval",
    "request_is_not_runtime_approval",
    "request_is_not_real_output_adapter_approval",
    "request_is_not_semantic_layer_approval",
    "owner_approval_is_not_granted_in_this_phase",
    "install_execution_is_not_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "requested_scope_is_limited_to_approved_install_candidates",
    "excluded_assets_must_not_enter_request_scope",
    "no_new_install_command_may_be_generated",
    "command_template_refs_must_remain_non_executed",
    "pre_install_snapshot_request_is_required",
    "rollback_requirement_request_is_required",
    "post_install_probe_request_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "post_install_probe_is_not_output_adapter",
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
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    REQUEST_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionRequestProfile",
    "InstallExecutionRequestPackage",
    "RequestedAssetScope",
    "OwnerApprovalRequestRecord",
    "RequestScopeBoundary",
    "CommandTemplateReferenceRecord",
    "PreInstallSnapshotRequest",
    "RollbackRequirementRequest",
    "PostInstallProbeRequirementRequest",
    "RiskDisclosureRecord",
    "ExcludedAssetDisclosureRecord",
    "RequestAuditRecord",
    "RequestPermissionBoundary",
    "NegativeInstallExecutionRequestGuard",
    "InstallExecutionApprovalHandoffReadiness",
    "P1ControlledInstallExecutionRequestDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_execution_request_post_review_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_REQUEST_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}

REQUEST_TRUE_INVARIANTS: Dict[str, bool] = {
    "request_only": True,
    "owner_approval_request_created": True,
    "request_success_not_owner_approval": True,
    "request_success_not_install_execution_approval": True,
    "request_success_not_inference_approval": True,
    "request_success_not_runtime_approval": True,
    "request_success_not_output_adapter_approval": True,
    "request_success_not_semantic_layer_approval": True,
    "request_scope_matches_execution_planning": True,
    "no_new_asset_added": True,
    "excluded_assets_not_in_request_scope": True,
    "request_scope_does_not_include_runtime": True,
    "request_scope_does_not_include_inference": True,
    "request_scope_does_not_include_weight_download_unless_separately_approved": True,
    "request_scope_does_not_include_semantic_layer": True,
    "new_install_command_generated_false": True,
    "request_does_not_execute_command": True,
    "pre_install_snapshot_requested": True,
    "rollback_requirement_requested": True,
    "post_install_probe_requested": True,
    "post_install_probe_find_spec_only": True,
    "post_install_probe_not_inference": True,
    "post_install_probe_not_runtime": True,
    "post_install_probe_not_output_adapter": True,
    "risk_disclosure_complete": True,
    "candidate_only_boundary_preserved": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
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
class P1ControlledInstallExecutionRequestProfile:
    profile_ref: str
    phase_id: str
    request_only: bool
    owner_approval_request_created: bool
    owner_approval_granted: bool
    install_execution_allowed: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    execution_planning_post_review_ref: str
    execution_planning_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    requested_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class InstallExecutionRequestPackage:
    request_id: str
    phase_id: str
    request_type: str
    requested_assets: Tuple[str, ...]
    requested_order: Tuple[Tuple[str, int], ...]
    command_template_refs: Tuple[str, ...]
    pre_install_snapshot_required: bool
    rollback_plan_required: bool
    post_install_probe_required: bool
    test_board_record_required: bool
    owner_approval_required: bool
    owner_approval_granted: bool
    install_execution_allowed: bool
    request_package_complete: bool


@dataclass(frozen=True)
class RequestedAssetScope:
    requested_asset_count: int
    excluded_asset_count: int
    no_new_asset_added: bool
    request_scope_matches_execution_planning: bool
    request_scope_does_not_include_runtime: bool
    request_scope_does_not_include_inference: bool
    request_scope_does_not_include_weight_download_unless_separately_approved: bool
    request_scope_does_not_include_semantic_layer: bool


@dataclass(frozen=True)
class OwnerApprovalRequestRecord:
    approval_request_created: bool
    approval_granted: bool
    approval_scope_requested: str
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
    request_success_not_owner_approval: bool


@dataclass(frozen=True)
class RequestScopeBoundary:
    boundary_id: str
    holds: bool


@dataclass(frozen=True)
class CommandTemplateReferenceRecord:
    asset_id: str
    command_template_ref: str
    template_only: bool
    command_not_executed: bool
    new_command_generated: bool
    whitelist_ref_exists: bool
    command_requires_future_approval: bool
    command_requires_pre_snapshot: bool
    command_requires_rollback_plan: bool


@dataclass(frozen=True)
class PreInstallSnapshotRequest:
    request_ref: str
    requested_items: Tuple[str, ...]
    snapshot_executed_in_this_phase: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool


@dataclass(frozen=True)
class RollbackRequirementRequest:
    asset_id: str
    rollback_plan_required: bool
    rollback_trigger_conditions_ref: Tuple[str, ...]
    rollback_command_template_ref: str
    rollback_command_not_executed: bool
    rollback_preserve_test_board: bool
    rollback_preserve_registry: bool
    rollback_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool


@dataclass(frozen=True)
class PostInstallProbeRequirementRequest:
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
class RiskDisclosureRecord:
    asset_id: str
    dependency_risk: str
    license_risk: str
    weight_risk: str
    environment_risk: str
    rollback_risk: str
    owner_ack_required: bool
    install_execution_allowed: bool
    can_enter_install_execution_after_approval: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_real_output_adapter: bool


@dataclass(frozen=True)
class ExcludedAssetDisclosureRecord:
    asset_id: str
    exclusion_bucket: str
    cannot_enter_request_scope: bool
    cannot_enter_install_execution: bool
    cannot_enter_runtime: bool
    cannot_enter_real_output_adapter: bool


@dataclass(frozen=True)
class RequestAuditRecord:
    trace_id: str
    trace_present: bool
    writes_to_test_board_protected_record: bool
    audit_only_in_this_phase: bool


@dataclass(frozen=True)
class RequestPermissionBoundary:
    boundary_id: str
    holds: bool


@dataclass
class NegativeInstallExecutionRequestGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class InstallExecutionApprovalHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ControlledInstallExecutionRequestDecision:
    decision_ref: str
    install_execution_request_profile_count: int
    install_execution_request_package_count: int
    requested_asset_count: int
    excluded_asset_disclosure_count: int
    owner_approval_request_record_count: int
    command_template_reference_record_count: int
    pre_install_snapshot_request_count: int
    rollback_requirement_request_count: int
    post_install_probe_requirement_request_count: int
    risk_disclosure_record_count: int
    request_audit_record_count: int
    request_permission_boundary_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
