# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Failure Review And Repair Planning — types v1
(PLANNING ONLY, scope = mobile_sam_only, target = timm).

Reviews the upstream timm controlled-install FAILED_NO_BOUNDARY_VIOLATION result. The
failure is NOT timm package corruption, NOT MobileSAM code/weight failure, NOT torch
missing — it is a dependency INSTALL STRATEGY timeout: full isolated `--target` install
attempted to re-download heavy transitive deps (torch/torchvision). This phase compares
repair routes (Route A no-deps P0 selected, Route B wheel/cache P1 fallback, Route C
extended timeout P2 fallback-only, Route D global reuse rejected), plans the next no-deps
install request/approval/readiness phase, and records model-load retry gate boundaries.
It does NOT pip install / install timm / real import / model load / retry / inference /
runtime / output adapter / semantic promotion / registry mutation / extra downloads.
Protected, non-deletable test board records are written in `planning` mode.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-MobileSAM-Dependency-Repair-Install-Failure-Review-And-Repair-Planning-v1-001"
SCOPE = "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning"
WEIGHT_CHAIN = "p1_mobile_sam_dependency_repair_install_failure_review_and_repair_planning_v1"

REPAIR_PRINCIPLE_ZH = (
    "纯规划，scope=mobile_sam_only，target=timm。复核上游 timm 受控安装的 FAILED_NO_BOUNDARY_VIOLATION："
    "失败不是 timm 包损坏、不是 MobileSAM 代码/权重问题、不是 torch 缺失，而是依赖安装策略超时——"
    "完整 isolated --target 安装试图重新下载 torch/torchvision 等大依赖导致 1200s 超时、target 0B。"
    "比较修复路线：Route A timm --no-deps 受控安装（P0 首选，复用已有 torch/torchvision）、"
    "Route B wheel/cache 预下载离线安装（P1 备选）、Route C 延长 timeout 完整 isolated install（P2 仅备选）、"
    "Route D 全局环境复用（拒绝）。规划下一步 no-deps install request/approval/readiness，"
    "记录 model-load retry 门槛。不 pip install、不装 timm、不真实 import、不 model load、不 retry、"
    "不 inference/runtime/output adapter/语义层、不改 registry、不额外下载。no-deps 规划 ≠ 安装批准 ≠ 安装成功。"
    "测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "install_failure_is_strategy_timeout_not_timm_or_weight_failure_no_deps_route_p0_reuse_torch"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
TIMM_INSTALL_FAILURE_REVIEW = True
REPAIR_REPLANNING_ONLY = True
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

UPSTREAM_INSTALL_EXECUTION_REF = "Phase-P1-MobileSAM-Dependency-Repair-Install-Execution-And-Post-Review-v1-001"
UPSTREAM_INSTALL_EXECUTION_EXPECTED_DECISION = (
    "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_OUTPUT_DIR_REL = (
    "_tmp_eval_out/p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1_smoke_v0"
)
UPSTREAM_REVIEW_FILE = "p1_mobile_sam_dependency_repair_install_execution_and_post_review_review_v1.json"
UPSTREAM_EVIDENCE_FILES: Tuple[str, ...] = (
    "p1_mobile_sam_dependency_repair_install_execution_and_post_review_review_v1.json",
    "timm_pre_install_snapshot_v1.json",
    "timm_version_resolution_v1.json",
    "timm_install_execution_record_v1.json",
    "timm_dependency_mutation_record_v1.json",
    "timm_find_spec_probe_v1.json",
    "timm_install_post_review_audit_v1.json",
)

CONTROLLED_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"
INSTALL_TIMEOUT_SECONDS_OBSERVED = 1200
FALLBACK_TORCH_VERSION = "2.8.0"

# Follow-up phases.
NEXT_PHASE_NO_DEPS_REQUEST = (
    "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Request-Approval-And-Readiness-v1-001"
)
SUGGESTED_RETRY_PHASE = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# Failure attribution.
FAILURE_CATEGORY = "dependency_install_timeout"
ROOT_CAUSE_CANDIDATE = (
    "transitive_dependency_download_install_too_heavy_under_isolated_target"
)
SELECTED_ROUTE = "timm_no_deps_controlled_install"

MOBILE_SAM_ASSET_ID = "mobile_sam"
TIMM_PACKAGE_NAME = "timm"
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_failed_no_boundary_violation", "go_key": "upstream_failed_no_boundary_violation", "depends_on": "upstream_failed_no_boundary_violation"},
    {"guard_id": "invalid_b_upstream_global_env_pollution_but_repair_as_clean", "go_key": "upstream_no_global_contamination", "depends_on": "upstream_no_global_contamination"},
    {"guard_id": "invalid_c_upstream_not_timeout_return_code_minus_one", "go_key": "upstream_timeout_return_code_minus_one", "depends_on": "upstream_timeout_return_code_minus_one"},
    {"guard_id": "invalid_d_target_path_nonempty_but_recorded_empty", "go_key": "target_path_empty_as_recorded", "depends_on": "target_path_empty_as_recorded"},
    {"guard_id": "invalid_e_pip_install_or_timm_install_executed", "go_key": "no_install_executed", "depends_on": "no_install_executed"},
    {"guard_id": "invalid_f_real_import_timm_or_mobile_sam", "go_key": "no_real_import", "depends_on": "no_real_import"},
    {"guard_id": "invalid_g_model_load_or_retry", "go_key": "no_model_load_retry", "depends_on": "no_model_load_retry"},
    {"guard_id": "invalid_h_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_i_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_j_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_k_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_l_route_a_treated_as_install_approval", "go_key": "route_a_not_install_approval", "depends_on": "route_a_not_install_approval"},
    {"guard_id": "invalid_m_no_deps_planning_treated_as_successful_install", "go_key": "no_deps_planning_not_install_success", "depends_on": "no_deps_planning_not_install_success"},
    {"guard_id": "invalid_n_timm_install_success_assumed", "go_key": "timm_availability_not_assumed", "depends_on": "timm_availability_not_assumed"},
    {"guard_id": "invalid_o_model_load_retry_allowed_immediately", "go_key": "model_load_retry_not_allowed_now", "depends_on": "model_load_retry_not_allowed_now"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (31 phase + 1 cleanup + 6 test board = 38).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_timm_install_failure_review_and_repair_planning_only",
    "scope_is_mobile_sam_only",
    "target_dependency_is_timm",
    "upstream_must_be_failed_no_boundary_violation",
    "upstream_failure_must_be_timeout_with_no_global_contamination",
    "root_cause_is_dependency_install_strategy_timeout",
    "same_full_isolated_install_command_should_not_be_retried_blindly",
    "route_a_no_deps_controlled_install_is_selected_planning_route",
    "no_pip_install_is_allowed_in_this_phase",
    "no_timm_install_is_allowed_in_this_phase",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_model_load_retry_is_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "no_deps_install_planning_is_not_install_approval",
    "no_deps_install_planning_is_not_install_success",
    "timm_availability_must_not_be_assumed",
    "model_load_retry_is_not_allowed_now",
    "commercial_runtime_is_not_approved",
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
    "timm_install_failure_audit_record",
    "timm_timeout_root_cause_record",
    "timm_repair_route_comparison_record",
    "timm_no_deps_install_plan_record",
    "timm_cache_or_wheel_install_plan_record",
    "timm_retry_gate_record",
    "mobile_sam_model_load_retry_boundary_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMTimmInstallFailureRepairPlanningProfile",
    "TimmInstallFailureAudit",
    "TimmInstallTimeoutRootCauseRecord",
    "TimmRepairRouteComparisonRecord",
    "TimmNoDepsInstallPlanningRecord",
    "TimmCacheWheelInstallPlanningRecord",
    "TimmTimeoutExtensionPlanningRecord",
    "TimmSecondRepairRiskRecord",
    "TimmSecondInstallRetryGatePlanningRecord",
    "MobileSAMModelLoadRetryBoundaryAfterTimmRepair",
    "NegativeTimmInstallFailureRepairPlanningGuard",
    "P1MobileSAMTimmInstallFailureRepairPlanningDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_FAILURE_REVIEW_AND_REPAIR_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "upstream_install_execution_evidence_reused": True,
    "torch_reuse_boundary_planned": True,
}


@dataclass(frozen=True)
class P1MobileSAMTimmInstallFailureRepairPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    mobile_sam_only: bool
    timm_install_failure_review: bool
    repair_replanning_only: bool
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
    upstream_install_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class TimmInstallFailureAudit:
    audit_id: str
    upstream_review_file_ref: str
    upstream_review_exists: bool
    final_decision_observed: str
    final_decision_ok: bool
    blocker_count_observed: int
    no_boundary_violation_observed: bool
    timm_install_success_observed: bool
    find_spec_timm_observed: bool
    return_code_observed: int
    timeout_occurred_observed: bool
    timeout_seconds_observed: int
    target_path_size_bytes_observed: int
    no_global_env_contamination_observed: bool
    global_env_changed_observed: bool
    torch_changed_observed: bool
    real_import_performed_observed: bool
    model_load_performed_observed: bool
    inference_performed_observed: bool
    runtime_performed_observed: bool
    registry_mutation_performed_observed: bool
    additional_weight_download_performed_observed: bool
    failure_category: str
    root_cause_candidate: str
    timm_package_corruption_related: bool
    mobile_sam_code_related: bool
    mobile_sam_weight_related: bool
    torch_missing_related: bool
    boundary_violation_related: bool
    global_env_pollution_related: bool
    retry_with_same_command_not_recommended: bool
    repair_replan_required: bool
    audit_passed: bool


@dataclass(frozen=True)
class TimmInstallTimeoutRootCauseRecord:
    record_id: str
    failure_category: str
    root_cause_candidate: str
    isolated_target_install_attempted: bool
    full_transitive_dependency_download_attempted: bool
    heavy_deps_include_torch_torchvision: bool
    timeout_seconds: int
    return_code: int
    target_path_empty_after_timeout: bool
    not_timm_package_missing: bool
    not_mobile_sam_weight_issue: bool
    not_mobile_sam_code_issue: bool
    is_dependency_install_strategy_issue: bool
    same_full_isolated_install_retry_not_recommended: bool


@dataclass(frozen=True)
class TimmRepairRouteComparisonRecord:
    record_id: str
    route_a_id: str
    route_a_priority: str
    route_a_selected: bool
    route_b_id: str
    route_b_priority: str
    route_b_selected: bool
    route_c_id: str
    route_c_priority: str
    route_c_selected: bool
    route_d_id: str
    route_d_priority: str
    route_d_selected: bool
    selected_route: str
    same_full_isolated_install_retry_not_recommended: bool


@dataclass(frozen=True)
class TimmNoDepsInstallPlanningRecord:
    record_id: str
    selected_route: str
    install_scope: str
    command_template: str
    command_template_only: bool
    command_not_executed: bool
    no_global_install: bool
    no_transitive_dependency_install: bool
    reuse_existing_torch_allowed_for_model_load_retry: bool
    existing_torch_version_must_be_verified: bool
    existing_torchvision_status_must_be_checked: bool
    post_install_probe: str
    real_import_timm_not_allowed_until_model_load_retry_execution: bool
    model_load_retry_not_allowed_until_install_go: bool
    planning_not_install_approval: bool
    planning_not_install_success: bool


@dataclass(frozen=True)
class TimmCacheWheelInstallPlanningRecord:
    record_id: str
    route_id: str
    priority: str
    selected: bool
    rationale: str
    requires_wheel_source_review: bool
    requires_hash_record: bool
    fallback_only: bool


@dataclass(frozen=True)
class TimmTimeoutExtensionPlanningRecord:
    record_id: str
    route_id: str
    priority: str
    selected: bool
    rationale: str
    timeout_seconds_candidate: int
    fallback_only: bool


@dataclass(frozen=True)
class TimmSecondRepairRiskRecord:
    record_id: str
    no_deps_install_missing_transitive_dependency_risk: bool
    timm_version_latest_drift_risk: bool
    torch_timm_compatibility_risk: bool
    torchvision_reuse_risk: bool
    hidden_import_chain_risk: bool
    repeated_repair_loop_risk: bool
    model_load_retry_failure_risk: bool
    global_env_contamination_risk: bool
    inference_boundary_violation_risk: bool
    runtime_boundary_violation_risk: bool


@dataclass(frozen=True)
class TimmSecondInstallRetryGatePlanningRecord:
    record_id: str
    model_load_retry_allowed_now: bool
    model_load_retry_requires_no_deps_timm_install_go: bool
    model_load_retry_requires_timm_find_spec_verified: bool
    model_load_retry_requires_mobile_sam_weight_sha256_recheck: bool
    model_load_retry_requires_code_and_weight_ready_still_valid: bool
    model_load_retry_requires_no_extra_dependency_gap_or_repair_loop: bool
    recommended_next_phase: str


@dataclass(frozen=True)
class MobileSAMModelLoadRetryBoundaryAfterTimmRepair:
    record_id: str
    existing_torch_reuse_allowed: bool
    existing_torch_version_expected: str
    existing_torch_reuse_does_not_allow_global_mutation: bool
    existing_torch_reuse_does_not_allow_reinstall: bool
    torchvision_status_check_required: bool
    torch_compatibility_must_be_observed_after_model_load_retry: bool
    if_timm_requires_missing_lightweight_dependency_enter_next_repair_loop: bool
    mobile_sam_weight_sha256: str


@dataclass
class NegativeTimmInstallFailureRepairPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMTimmInstallFailureRepairPlanningDecision:
    decision_ref: str
    mobile_sam_timm_install_failure_repair_planning_profile_count: int
    timm_install_failure_audit_count: int
    timm_timeout_root_cause_record_count: int
    timm_repair_route_comparison_record_count: int
    timm_no_deps_install_plan_record_count: int
    timm_cache_or_wheel_install_plan_record_count: int
    timm_retry_gate_record_count: int
    mobile_sam_model_load_retry_boundary_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    selected_route: str
    same_full_isolated_install_retry_not_recommended: bool
    model_load_retry_allowed_now: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
