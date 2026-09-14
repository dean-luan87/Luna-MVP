# -*- coding: utf-8 -*-
"""P1 Controlled Install Planning DryRun Post-Review — types v1.

A PURE post-review of Phase-P1-Controlled-Install-Planning-DryRun-v1-001. It
audits the upstream controlled-install plan: the 5 INSTALL_REQUIRED candidates,
the 12 excluded assets, install order, dependency resolution, package install
templates (must remain template-only / non-executed), weight-acquisition plans,
environment isolation, version-pin plans, license boundary, rollback plans, the
readiness matrix, the upstream test board planning records, and the non-runtime
boundary.

It does NOT generate new install plans, NOT mutate candidates, NOT generate new
install command templates, NOT run pip install, NOT install dependencies, NOT
download models/weights/datasets, NOT run inference, NOT enter runtime, NOT enter
the semantic layer. Post-review success is NOT install-execution / runtime /
real-output-adapter approval.
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

PHASE_ID = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"
SCOPE = "p1_controlled_install_planning_dryrun_post_review"
SOURCE_CHAIN = "p1_controlled_install_planning_dryrun_post_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Controlled-Install-Planning-DryRun-v1-001，执行纯事后复核。不新增安装计划、不修改候选资产、"
    "不生成新的 install command template、不执行 pip install、不安装依赖、不下载模型/权重/数据集、不执行 inference、"
    "不进入 runtime、不进入语义层。只复核上游 controlled install planning dry-run 的 5 个候选、12 个排除资产、安装顺序、"
    "依赖解析、权重计划、环境隔离、版本锁、license 边界、rollback 计划、测试板块记录与 non-runtime 边界。"
    "post-review 成功不等于 install execution / runtime / real output adapter 批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_planning_post_review_is_audit_only_no_new_plan_no_mutation_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
NEW_INSTALL_PLAN_GENERATION_ALLOWED = False
INSTALL_CANDIDATE_MUTATION_ALLOWED = False
INSTALL_TEMPLATE_GENERATION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

CONTROLLED_INSTALL_PLANNING_REF = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"
RECONCILIATION_POST_REVIEW_REF = (
    "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
)
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"

CONTROLLED_INSTALL_PLANNING_EXPECTED_GO = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding.
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "post_review"

# --------------------------------------------------------------------------- #
# Upstream artifact + upstream test board paths.
# --------------------------------------------------------------------------- #
UPSTREAM_REVIEW_ARTIFACT_REL = (
    "_tmp_eval_out/p1_controlled_install_planning_dryrun_v1_smoke_v0/"
    "p1_controlled_install_planning_dryrun_review_v1.json"
)
UPSTREAM_TEST_BOARD_REL = (
    "capabilities/test_board/recognition_models/"
    "phase_p1_controlled_install_planning_dryrun_v1_001"
)
UPSTREAM_TEST_BOARD_STANDIN_REL = (
    "_tmp_eval_out/board_standin/capabilities/test_board/recognition_models/"
    "phase_p1_controlled_install_planning_dryrun_v1_001"
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
# Candidate / excluded scope (must match upstream).
# --------------------------------------------------------------------------- #
EXPECTED_CANDIDATES: Tuple[str, ...] = (
    "supervision",
    "byte_track",
    "deep_sort",
    "midas",
    "mobile_sam",
)

EXPECTED_EXCLUDED: Tuple[Dict[str, str], ...] = (
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
    {"asset_id": "rt_detr", "exclusion_bucket": "OTHER_NOT_INSTALL_REQUIRED"},
)

# Bucket aliases: the upstream controlled-install-planning phase labels the
# rt_detr "OTHER_NOT_INSTALL_REQUIRED" category as "PARTIAL_OR_NON_INSTALL_REQUIRED".
# Treat these as equivalent (cosmetic label difference, same governance meaning).
EXCLUSION_BUCKET_ALIASES: Dict[str, Tuple[str, ...]] = {
    "OTHER_NOT_INSTALL_REQUIRED": ("OTHER_NOT_INSTALL_REQUIRED", "PARTIAL_OR_NON_INSTALL_REQUIRED"),
}

EXPECTED_INSTALL_ORDER: Tuple[Tuple[str, int], ...] = (
    ("supervision", 1),
    ("byte_track", 2),
    ("deep_sort", 3),
    ("midas", 4),
    ("mobile_sam", 5),
)

# Assets that must record weight_required = false.
NO_WEIGHT_ASSETS: Tuple[str, ...] = ("supervision", "byte_track")
# Assets where weight_required handling must be present (true).
WEIGHT_HANDLED_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

# --------------------------------------------------------------------------- #
# Sealed expected metrics (used for sealed_ref_fallback when artifact missing).
# --------------------------------------------------------------------------- #
SEALED_EXPECTED_METRICS: Dict[str, int] = {
    "install_candidate_count": 5,
    "excluded_asset_count": 12,
    "install_order_plan_count": 5,
    "dependency_resolution_plan_count": 5,
    "package_install_plan_count": 5,
    "weight_acquisition_plan_count": 5,
    "version_pin_plan_count": 5,
    "license_install_boundary_check_count": 5,
    "rollback_plan_count": 5,
    "controlled_install_readiness_matrix_count": 5,
    "negative_guard_passed": 18,
    "test_board_record_count": 6,
}

# Artifact audit spec: (field, op, value).
ARTIFACT_AUDIT_SPEC: Tuple[Dict[str, Any], ...] = (
    {"field": "final_decision", "op": "eq", "value": CONTROLLED_INSTALL_PLANNING_EXPECTED_GO},
    {"field": "blocker_count", "op": "eq", "value": 0},
    {"field": "install_candidate_count", "op": "eq", "value": 5},
    {"field": "excluded_asset_count", "op": "eq", "value": 12},
    {"field": "install_order_plan_count", "op": "eq", "value": 5},
    {"field": "dependency_resolution_plan_count", "op": "eq", "value": 5},
    {"field": "package_install_plan_count", "op": "eq", "value": 5},
    {"field": "weight_acquisition_plan_count", "op": "eq", "value": 5},
    {"field": "version_pin_plan_count", "op": "eq", "value": 5},
    {"field": "license_install_boundary_check_count", "op": "eq", "value": 5},
    {"field": "rollback_plan_count", "op": "eq", "value": 5},
    {"field": "controlled_install_readiness_matrix_count", "op": "eq", "value": 5},
    {"field": "negative_guard_passed", "op": "eq", "value": 18},
    {"field": "test_board_record_count", "op": "gte", "value": 6},
)

# Non-runtime boundary audit items (>= 15).
NON_RUNTIME_BOUNDARY_AUDIT_ITEMS: Tuple[str, ...] = (
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

# Rollback triggers that must be covered.
REQUIRED_ROLLBACK_TRIGGERS: Tuple[str, ...] = (
    "dependency_conflict",
    "import_probe_still_missing_after_future_install",
    "version_drift",
    "package_import_side_effect_risk",
    "license_mismatch",
    "environment_corruption",
    "unexpected_package_overwrite",
    "test_board_write_failure",
)

# --------------------------------------------------------------------------- #
# Negative post-review guards (24: A..X)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "upstream_final_decision_go_verified", "depends_on": "upstream_final_decision_go"},
    {"guard_id": "invalid_b_upstream_blocker_nonzero", "go_key": "upstream_blocker_count_zero_verified", "depends_on": "upstream_blocker_count_zero"},
    {"guard_id": "invalid_c_install_candidate_count_not_5", "go_key": "install_candidate_count_verified", "depends_on": "install_candidate_count_is_5"},
    {"guard_id": "invalid_d_excluded_count_not_12", "go_key": "excluded_asset_count_verified", "depends_on": "excluded_asset_count_is_12"},
    {"guard_id": "invalid_e_non_install_required_in_candidate", "go_key": "only_install_required_assets_selected", "depends_on": "only_install_required_selected"},
    {"guard_id": "invalid_f_blocked_deferred_reserved_in_candidate", "go_key": "blocked_deferred_reserved_excluded", "depends_on": "blocked_deferred_reserved_excluded"},
    {"guard_id": "invalid_g_install_template_executed", "go_key": "install_templates_not_executed", "depends_on": "install_templates_not_executed"},
    {"guard_id": "invalid_h_pip_or_dependency_install_executed", "go_key": "pip_dependency_install_not_performed", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_i_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_j_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_k_future_install_without_env_isolation", "go_key": "env_isolation_audit_passed", "depends_on": "env_isolation_audit_passed"},
    {"guard_id": "invalid_l_future_install_without_rollback", "go_key": "rollback_audit_passed", "depends_on": "rollback_audit_passed"},
    {"guard_id": "invalid_m_future_install_without_version_pin", "go_key": "version_pin_audit_passed", "depends_on": "version_pin_audit_passed"},
    {"guard_id": "invalid_n_future_inference_without_weight_gate", "go_key": "weight_gate_audit_passed", "depends_on": "weight_gate_audit_passed"},
    {"guard_id": "invalid_o_planning_as_install_execution_approval", "go_key": "post_review_success_not_install_execution_approval", "depends_on": "not_install_execution_approval"},
    {"guard_id": "invalid_p_planning_as_runtime_approval", "go_key": "post_review_success_not_runtime_approval", "depends_on": "not_runtime_approval"},
    {"guard_id": "invalid_q_planning_as_real_output_adapter_approval", "go_key": "post_review_success_not_real_output_adapter_approval", "depends_on": "not_real_output_adapter_approval"},
    {"guard_id": "invalid_r_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_s_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_t_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_u_upstream_test_board_missing_or_not_planning", "go_key": "upstream_test_board_planning_record_verified", "depends_on": "upstream_test_board_planning_verified"},
    {"guard_id": "invalid_v_phase_does_not_write_post_review_test_board", "go_key": "post_review_test_board_record_required", "depends_on": "post_review_test_board_write_planned"},
    {"guard_id": "invalid_w_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_x_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (38 phase + 6 test board = 44).
# --------------------------------------------------------------------------- #
POST_REVIEW_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_install_planning_post_review_only",
    "no_new_install_plan_may_be_generated",
    "no_install_candidate_mutation_is_allowed",
    "no_install_template_generation_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "install_command_templates_must_remain_non_executed",
    "only_install_required_assets_may_remain_candidates",
    "blocked_by_license_assets_must_remain_excluded",
    "deferred_resource_heavy_assets_must_remain_excluded",
    "reserved_only_assets_must_remain_excluded",
    "environment_isolation_plan_audit_is_required",
    "version_pin_plan_audit_is_required",
    "weight_acquisition_plan_audit_is_required",
    "license_boundary_audit_is_required",
    "rollback_plan_audit_is_required",
    "future_install_execution_requires_separate_approval",
    "post_review_success_is_not_install_execution_approval",
    "post_review_success_is_not_runtime_approval",
    "post_review_success_is_not_real_output_adapter_approval",
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
    "P1ControlledInstallPlanningPostReviewProfile",
    "ControlledInstallPlanningArtifactAudit",
    "InstallCandidateAudit",
    "ExcludedAssetAudit",
    "InstallOrderAudit",
    "DependencyResolutionAudit",
    "PackageTemplateNonExecutionAudit",
    "WeightAcquisitionPlanAudit",
    "EnvironmentIsolationAudit",
    "VersionPinPlanAudit",
    "LicenseBoundaryAudit",
    "RollbackPlanAudit",
    "ReadinessMatrixAudit",
    "TestBoardPlanningRecordAudit",
    "NonRuntimeBoundaryAudit",
    "NegativeControlledInstallPostReviewGuard",
    "InstallPlanningHandoffReadiness",
    "P1ControlledInstallPlanningPostReviewDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_execution_planning_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "post_review_test_mode_reused": True,
}

POST_REVIEW_TRUE_INVARIANTS: Dict[str, bool] = {
    "upstream_final_decision_go_verified": True,
    "upstream_blocker_count_zero_verified": True,
    "install_candidate_count_verified": True,
    "excluded_asset_count_verified": True,
    "only_install_required_assets_selected": True,
    "blocked_license_assets_excluded": True,
    "deferred_assets_excluded": True,
    "reserved_only_assets_excluded": True,
    "install_templates_not_executed": True,
    "environment_isolation_audit_passed": True,
    "version_pin_audit_passed": True,
    "weight_gate_audit_passed": True,
    "license_boundary_audit_passed": True,
    "rollback_audit_passed": True,
    "future_install_requires_separate_approval": True,
    "post_review_success_not_install_execution_approval": True,
    "post_review_success_not_runtime_approval": True,
    "post_review_success_not_real_output_adapter_approval": True,
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
class P1ControlledInstallPlanningPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    new_install_plan_generation_allowed: bool
    install_candidate_mutation_allowed: bool
    install_template_generation_allowed: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    controlled_install_planning_ref: str
    reconciliation_post_review_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    expected_candidates: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ControlledInstallPlanningArtifactAudit:
    artifact_rel: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    upstream_final_decision: str
    checks_passed: int
    checks_total: int
    passed: bool


@dataclass(frozen=True)
class InstallCandidateAudit:
    asset_id: str
    source_readiness_state_ok: bool
    refs_present: bool
    license_allows_planning: bool
    install_execution_allowed: bool
    can_enter_controlled_install_plan: bool
    can_enter_install_execution: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    passed: bool


@dataclass(frozen=True)
class ExcludedAssetAudit:
    asset_id: str
    exclusion_bucket: str
    excluded: bool
    not_install_candidate: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    passed: bool


@dataclass(frozen=True)
class InstallOrderAudit:
    asset_id: str
    planned_order: int
    order_reason_present: bool
    order_is_planning_only: bool
    order_does_not_execute_install: bool
    layer_ordering_ok: bool


@dataclass(frozen=True)
class DependencyResolutionAudit:
    asset_id: str
    dependency_group_present: bool
    shared_dependency_policy_present: bool
    version_drift_requires_review: bool
    no_auto_overwrite: bool
    dependency_install_not_performed: bool


@dataclass(frozen=True)
class PackageTemplateNonExecutionAudit:
    asset_id: str
    install_command_template_present: bool
    install_command_not_executed: bool
    template_only: bool
    no_subprocess_execution: bool
    owner_approval_required: bool
    isolated_env_required: bool
    pre_snapshot_required: bool
    post_probe_required: bool
    rollback_required: bool
    passed: bool


@dataclass(frozen=True)
class WeightAcquisitionPlanAudit:
    asset_id: str
    weight_required: bool
    weight_download_not_performed: bool
    auto_weight_download_allowed: bool
    weight_hash_required_before_future_inference: bool
    weight_license_binding_required: bool
    weight_source_review_required: bool
    passed: bool


@dataclass(frozen=True)
class EnvironmentIsolationAudit:
    target_env_label_present: bool
    existing_env_reference_present: bool
    python_version_policy_present: bool
    os_policy_present: bool
    macos_arm64_recorded: bool
    cuda_required_false: bool
    mps_possible_recorded: bool
    cpu_only_possible_recorded: bool
    no_global_site_packages_policy_present: bool
    environment_snapshot_required: bool
    rollback_snapshot_required: bool
    no_runtime_execution_in_install_phase: bool
    passed: bool


@dataclass(frozen=True)
class VersionPinPlanAudit:
    asset_id: str
    exact_pin_required_present: bool
    version_unknown_allowed_for_planning: bool
    version_unknown_blocks_runtime: bool
    version_unknown_blocks_real_inference: bool
    installed_version_must_be_recorded: bool
    version_drift_requires_review: bool
    passed: bool


@dataclass(frozen=True)
class LicenseBoundaryAudit:
    asset_id: str
    commercial_runtime_approved: bool
    install_planning_not_commercial_approval: bool
    install_planning_not_runtime_approval: bool
    permissive_or_explicitly_bounded: bool
    passed: bool


@dataclass(frozen=True)
class RollbackPlanAudit:
    asset_id: str
    pre_install_snapshot_required: bool
    post_install_probe_required: bool
    rollback_triggers_present: bool
    rollback_steps_present: bool
    cleanup_protects_test_board: bool
    cleanup_protects_registry: bool
    cleanup_protects_review_artifacts: bool
    rollback_success_requires_post_review: bool
    passed: bool


@dataclass(frozen=True)
class ReadinessMatrixAudit:
    asset_id: str
    can_enter_future_controlled_install_execution_gated: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    owner_approval_required: bool
    passed: bool


@dataclass(frozen=True)
class TestBoardPlanningRecordAudit:
    record_type: str
    present: bool
    protected: bool
    non_deletable: bool
    deletion_forbidden: bool
    mode_planning: bool


@dataclass(frozen=True)
class NonRuntimeBoundaryAudit:
    audit_item: str
    is_false: bool


@dataclass
class NegativeControlledInstallPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class InstallPlanningHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ControlledInstallPlanningPostReviewDecision:
    decision_ref: str
    controlled_install_post_review_profile_count: int
    controlled_install_planning_artifact_audit_count: int
    install_candidate_audit_count: int
    excluded_asset_audit_count: int
    install_order_audit_count: int
    dependency_resolution_audit_count: int
    package_template_non_execution_audit_count: int
    weight_acquisition_plan_audit_count: int
    environment_isolation_audit_count: int
    version_pin_plan_audit_count: int
    license_boundary_audit_count: int
    rollback_plan_audit_count: int
    readiness_matrix_audit_count: int
    test_board_planning_record_audit_count: int
    non_runtime_boundary_audit_count: int
    negative_post_review_guard_count: int
    negative_post_review_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
