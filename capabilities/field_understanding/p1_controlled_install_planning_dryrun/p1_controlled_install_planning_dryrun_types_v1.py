# -*- coding: utf-8 -*-
"""P1 Controlled Install Planning DryRun — types v1.

Based on the GO Midplatform Model Version/Dependency Registry, P1 Real Install /
Local Availability DryRun, and the Registry <-> P1 Probe Reconciliation
Post-Review, this phase produces a *controlled install planning* dry-run for the
5 INSTALL_REQUIRED P1 model assets.

It only plans: install order, dependency-resolution order, weight-acquisition
strategy, environment-isolation strategy, version-pin policy, license install
boundary, rollback boundary, blocker conditions, downstream execution gating and
audit records. It does NOT run pip install, NOT install dependencies, NOT
download models/weights/datasets, NOT run real inference, NOT enter runtime, NOT
enter the semantic layer, NOT trigger navigation/action/speech/fact_write.

Install command templates may be generated but are strictly template-only and
must never be executed (no subprocess pip). Install planning success is NOT
install-execution / runtime / real-output-adapter / commercial approval.
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

PHASE_ID = "Phase-P1-Controlled-Install-Planning-DryRun-v1-001"
SCOPE = "p1_controlled_install_planning_dryrun"
SOURCE_CHAIN = "p1_controlled_install_planning_dryrun_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Midplatform Model Version/Dependency Registry、P1 Real Install / Local Availability "
    "DryRun，以及 Registry ↔ P1 Probe Reconciliation Post-Review，生成 P1 模型资产的受控安装规划 dry-run。"
    "只规划安装顺序、依赖解析顺序、权重获取策略、环境隔离策略、版本锁策略、license 安装边界、回滚边界、阻断条件、"
    "后续执行门控和审计记录。不执行 pip install、不安装依赖、不下载模型/权重/数据集、不执行真实 inference、"
    "不进入 runtime、不进入语义层、不触发 navigation/action/speech/fact_write。install command 仅为 "
    "template_only，绝不执行。安装规划成功不等于安装执行/runtime/real output adapter/商用批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_planning_is_planning_only_template_only_no_install_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
PLANNING_DRYRUN_ONLY = True
CONTROLLED_INSTALL_PLANNING_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

RECONCILIATION_POST_REVIEW_REF = (
    "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001"
)
REGISTRY_PLANNING_REF = "Phase-Midplatform-Model-Version-Dependency-Registry-Planning-v1-001"
P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF = "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001"
PLANNING_MODE_PATCH_REF = "Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_REF = "Phase-P1-Controlled-Install-Planning-DryRun-Post-Review-v1-001"

RECONCILIATION_EXPECTED_GO = "MIDPLATFORM_REGISTRY_P1_PROBE_RECONCILIATION_POST_REVIEW_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding — uses the now-valid "planning" mode.
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Candidate / excluded asset scope.
# Only INSTALL_REQUIRED assets from the P1 real-install dry-run may be selected.
# --------------------------------------------------------------------------- #
INSTALL_CANDIDATE_ASSET_IDS: Tuple[str, ...] = (
    "mobile_sam",
    "byte_track",
    "deep_sort",
    "supervision",
    "midas",
)

EXCLUDED_ASSETS: Tuple[Dict[str, str], ...] = (
    # BLOCKED_BY_LICENSE
    {"asset_id": "fast_sam", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    {"asset_id": "yolov8n", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    {"asset_id": "pyannote", "exclusion_bucket": "BLOCKED_BY_LICENSE"},
    # DEFERRED_RESOURCE_HEAVY
    {"asset_id": "sam2", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "depth_anything", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "zoe_depth", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "grounding_dino", "exclusion_bucket": "DEFERRED_RESOURCE_HEAVY"},
    # RESERVED_ONLY
    {"asset_id": "scene_relation_vlm", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "open_vocab_vlm", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "sense_voice", "exclusion_bucket": "RESERVED_ONLY"},
    {"asset_id": "emotion_multimodal_bridge", "exclusion_bucket": "RESERVED_ONLY"},
    # NOTE: in the P1 probe, depth_anything/grounding_dino/sam2 land in
    # DEFERRED; the registry-blocked set already excludes them. The 12th excluded
    # asset is the segmentation-blocked fast_sam variant family member captured
    # above plus the reserved-only set. We additionally exclude the partial-ready
    # asset to keep selection strictly INSTALL_REQUIRED.
    {"asset_id": "rt_detr", "exclusion_bucket": "PARTIAL_OR_NON_INSTALL_REQUIRED"},
)

EXPECTED_INSTALL_CANDIDATE_COUNT = 5
EXPECTED_EXCLUDED_ASSET_COUNT = 12
SOURCE_READINESS_STATE_REQUIRED = "INSTALL_REQUIRED"

# --------------------------------------------------------------------------- #
# Planned install order (planning order, NOT execution). Lower order = earlier.
# --------------------------------------------------------------------------- #
INSTALL_ORDER_PLAN: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "supervision", "planned_order": 1,
        "order_reason": "wrapper_utility_layer_used_by_tracking_and_detection_low_risk",
    },
    {
        "asset_id": "byte_track", "planned_order": 2,
        "order_reason": "lightweight_tracking_core_validate_tracking_family_dependency_first",
    },
    {
        "asset_id": "deep_sort", "planned_order": 3,
        "order_reason": "tracking_alternative_path_slightly_more_complex_deps_than_bytetrack",
    },
    {
        "asset_id": "midas", "planned_order": 4,
        "order_reason": "depth_family_torch_timm_deps_higher_resource_risk",
    },
    {
        "asset_id": "mobile_sam", "planned_order": 5,
        "order_reason": "segmentation_family_more_complex_deps_and_weight_paths_plan_last",
    },
)

# --------------------------------------------------------------------------- #
# Global dependency resolution strategy (ordered layers).
# --------------------------------------------------------------------------- #
GLOBAL_DEPENDENCY_RESOLUTION_STRATEGY: Tuple[str, ...] = (
    "resolve_utility_wrapper_layer_first",
    "then_tracking_layer",
    "then_depth_layer",
    "then_segmentation_layer",
    "torch_core_and_cv_core_are_shared_dependencies_resolved_once_no_unordered_reinstall",
    "any_dependency_version_drift_requires_review",
    "dependency_conflicts_must_not_auto_overwrite_existing_environment",
)

DEPENDENCY_LAYER_BY_FAMILY: Dict[str, str] = {
    "tracking": "tracking_layer",
    "depth_spatial_hint": "depth_layer",
    "segmentation": "segmentation_layer",
}

# --------------------------------------------------------------------------- #
# Rollback trigger conditions (>= 8).
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
)

ROLLBACK_STEPS_TEMPLATE: Tuple[str, ...] = (
    "halt_future_install_execution",
    "restore_pre_install_environment_snapshot",
    "re_run_find_spec_probe_to_confirm_restored_state",
    "record_rollback_event_to_test_board",
    "require_post_review_before_retry",
)

CLEANUP_SCOPE_NOTE = "transient_install_scratch_only_never_test_board_registry_or_review_artifacts"

# --------------------------------------------------------------------------- #
# Negative guards (18: A..R)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_real_pip_or_dependency_install", "go_key": "no_pip_or_dependency_install", "depends_on": "no_install_performed"},
    {"guard_id": "invalid_b_model_weight_dataset_download", "go_key": "no_model_weight_dataset_download", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_c_real_inference", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_d_install_template_marked_executed", "go_key": "install_templates_not_executed", "depends_on": "install_templates_not_executed"},
    {"guard_id": "invalid_e_future_install_without_env_isolation", "go_key": "env_isolation_required_for_future_install", "depends_on": "env_isolation_plan_present"},
    {"guard_id": "invalid_f_future_install_without_rollback", "go_key": "rollback_required_for_future_install", "depends_on": "rollback_plan_present"},
    {"guard_id": "invalid_g_future_install_without_version_pin", "go_key": "version_pin_required_for_future_install", "depends_on": "version_pin_plan_present"},
    {"guard_id": "invalid_h_future_inference_without_weight_hash_source_license", "go_key": "weight_hash_source_license_required_for_future_inference", "depends_on": "weight_gate_present"},
    {"guard_id": "invalid_i_blocked_deferred_reserved_in_candidate", "go_key": "only_install_required_in_candidate", "depends_on": "only_install_required_selected"},
    {"guard_id": "invalid_j_agpl_unknown_as_commercial_runtime", "go_key": "agpl_unknown_not_commercial_runtime", "depends_on": "commercial_runtime_not_approved"},
    {"guard_id": "invalid_k_planning_as_runtime_approval", "go_key": "planning_not_runtime_approval", "depends_on": "planning_not_runtime_approval"},
    {"guard_id": "invalid_l_planning_as_real_output_adapter_approval", "go_key": "planning_not_real_output_adapter_approval", "depends_on": "planning_not_real_output_adapter_approval"},
    {"guard_id": "invalid_m_semantic_promotion_allowed", "go_key": "semantic_promotion_blocked", "depends_on": "semantic_promotion_not_allowed"},
    {"guard_id": "invalid_n_action_speech_factwrite_navigation_allowed", "go_key": "action_speech_factwrite_navigation_blocked", "depends_on": "action_speech_factwrite_navigation_not_allowed"},
    {"guard_id": "invalid_o_vla_action_chain_allowed", "go_key": "vla_action_chain_blocked", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_p_test_record_not_written_to_board", "go_key": "test_board_record_required_enforced", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (34 phase + 6 test board = 40).
# --------------------------------------------------------------------------- #
CONTROLLED_INSTALL_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_install_planning_dry_run_only",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "install_command_templates_must_not_be_executed",
    "only_install_required_assets_may_enter_install_candidate_selection",
    "blocked_by_license_assets_must_not_enter_install_candidate_selection",
    "deferred_resource_heavy_assets_must_not_enter_install_candidate_selection",
    "reserved_only_assets_must_not_enter_install_candidate_selection",
    "environment_isolation_plan_is_required",
    "version_pin_plan_is_required",
    "weight_acquisition_plan_is_required_where_applicable",
    "license_install_boundary_check_is_required",
    "rollback_plan_is_required",
    "future_install_execution_requires_separate_approval",
    "install_planning_success_is_not_install_execution_approval",
    "install_planning_success_is_not_runtime_approval",
    "install_planning_success_is_not_real_output_adapter_approval",
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
    CONTROLLED_INSTALL_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallPlanningProfile",
    "InstallCandidateSelectionRecord",
    "InstallOrderPlan",
    "DependencyResolutionPlan",
    "PackageInstallPlan",
    "WeightAcquisitionPlan",
    "EnvironmentIsolationPlan",
    "VersionPinPlan",
    "LicenseInstallBoundaryCheck",
    "RollbackPlan",
    "InstallBlockerRule",
    "InstallAuditRecord",
    "ControlledInstallReadinessMatrix",
    "InstallHandoffReadiness",
    "NegativeControlledInstallPlanningGuard",
    "P1ControlledInstallPlanningDryRunDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": NEXT_STEP_REF,
        "go_key": "p1_controlled_install_planning_dryrun_post_review_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_PLANNING_DRYRUN_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}

PLANNING_TRUE_INVARIANTS: Dict[str, bool] = {
    "only_install_required_assets_selected": True,
    "blocked_license_assets_excluded": True,
    "deferred_assets_excluded": True,
    "reserved_only_assets_excluded": True,
    "install_order_planned": True,
    "dependency_resolution_planned": True,
    "package_install_templates_created": True,
    "install_templates_not_executed": True,
    "weight_acquisition_planned": True,
    "weight_download_not_performed": True,
    "environment_isolation_planned": True,
    "version_pin_planned": True,
    "license_boundary_checked": True,
    "rollback_planned": True,
    "future_install_requires_separate_approval": True,
    "install_planning_success_not_install_execution_approval": True,
    "install_planning_success_not_runtime_approval": True,
    "install_planning_success_not_real_output_adapter_approval": True,
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
class P1ControlledInstallPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_dryrun_only: bool
    controlled_install_planning_only: bool
    existing_governance_reuse_required: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    reconciliation_post_review_ref: str
    registry_planning_ref: str
    p1_real_install_local_availability_ref: str
    planning_mode_patch_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    install_candidate_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class InstallCandidateSelectionRecord:
    asset_id: str
    source_readiness_state: str
    registry_identity_ref: str
    registry_dependency_ref: str
    registry_license_ref: str
    p1_probe_ref: str
    reconciliation_ref: str
    selection_reason: str
    license_allows_planning: bool
    install_execution_allowed: bool
    can_enter_controlled_install_plan: bool
    can_enter_install_execution: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool


@dataclass(frozen=True)
class InstallOrderPlanRecord:
    asset_id: str
    planned_order: int
    order_reason: str
    execution_performed: bool


@dataclass(frozen=True)
class DependencyResolutionPlan:
    asset_id: str
    primary_package_name: str
    import_probe_name: str
    dependency_group: str
    required_dependencies: Tuple[str, ...]
    optional_dependencies: Tuple[str, ...]
    dependency_resolution_order: int
    conflict_risk: str
    version_pin_policy: str
    visible_version_required_after_future_install: bool
    dependency_install_not_performed: bool


@dataclass(frozen=True)
class PackageInstallPlan:
    asset_id: str
    planned_package_names: Tuple[str, ...]
    install_command_template: str
    install_command_not_executed: bool
    install_requires_owner_approval_before_execution: bool
    install_requires_virtualenv_or_isolated_env: bool
    install_requires_pre_snapshot: bool
    install_requires_post_probe: bool
    install_requires_rollback_plan: bool
    install_risk_level: str
    template_only: bool


@dataclass(frozen=True)
class WeightAcquisitionPlan:
    asset_id: str
    weight_required: bool
    expected_weight_names: Tuple[str, ...]
    expected_weight_paths: Tuple[str, ...]
    weight_source_policy: str
    weight_download_not_performed: bool
    weight_hash_required_before_future_inference: bool
    weight_license_binding_required: bool
    weight_source_review_required: bool
    auto_weight_download_allowed: bool
    note: str


@dataclass(frozen=True)
class EnvironmentIsolationPlan:
    target_env_label: str
    python_version_policy: str
    os_policy: str
    macos_arm64_compatibility: str
    cpu_only_possible: bool
    mps_possible: bool
    cuda_required: bool
    shared_dependency_policy: str
    no_global_site_packages_policy: bool
    environment_snapshot_required: bool
    rollback_snapshot_required: bool
    no_runtime_execution_in_install_phase: bool
    existing_env_reference: str


@dataclass(frozen=True)
class VersionPinPlan:
    asset_id: str
    exact_pin_required_for_future_install_execution: bool
    allowed_minor_range_for_planning: bool
    version_unknown_allowed_for_planning: bool
    version_unknown_blocks_runtime: bool
    version_unknown_blocks_real_inference: bool
    installed_version_must_be_recorded_after_future_install: bool
    version_drift_requires_review: bool


@dataclass(frozen=True)
class LicenseInstallBoundaryCheck:
    asset_id: str
    license_type: str
    permissive_family: bool
    license_allows_install_planning: bool
    unknown_license_blocks_install_execution: bool
    agpl_blocks_commercial_runtime: bool
    commercial_runtime_approved: bool
    install_planning_not_commercial_approval: bool
    install_planning_not_runtime_approval: bool


@dataclass(frozen=True)
class RollbackPlan:
    asset_id: str
    pre_install_snapshot_required: bool
    post_install_probe_required: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_steps_template: Tuple[str, ...]
    cleanup_scope: str
    cleanup_must_not_delete_test_board: bool
    cleanup_must_not_delete_registry: bool
    cleanup_must_not_delete_review_artifacts: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class InstallBlockerRule:
    rule_id: str
    description: str
    is_blocker_when_violated: bool


@dataclass(frozen=True)
class InstallAuditRecord:
    audit_ref: str
    install_candidate_count: int
    excluded_asset_count: int
    candidate_only: bool
    written_to_test_board: bool
    protected: bool
    non_deletable: bool


@dataclass(frozen=True)
class ControlledInstallReadinessMatrix:
    asset_id: str
    install_candidate: bool
    planned_order: int
    dependency_group: str
    package_plan_ready: bool
    weight_plan_ready: bool
    env_isolation_ready: bool
    version_pin_plan_ready: bool
    license_boundary_ok: bool
    rollback_plan_ready: bool
    can_enter_future_controlled_install_execution: bool
    can_enter_runtime_trial: bool
    can_enter_real_output_adapter_dryrun: bool
    blocker_reason: str


@dataclass(frozen=True)
class InstallHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass
class NegativeControlledInstallPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallPlanningDryRunDecision:
    decision_ref: str
    controlled_install_planning_profile_count: int
    install_candidate_count: int
    excluded_asset_count: int
    install_order_plan_count: int
    dependency_resolution_plan_count: int
    package_install_plan_count: int
    weight_acquisition_plan_count: int
    environment_isolation_plan_count: int
    version_pin_plan_count: int
    license_install_boundary_check_count: int
    rollback_plan_count: int
    controlled_install_readiness_matrix_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
