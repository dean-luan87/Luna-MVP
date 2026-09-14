# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair NoDeps Install Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only, target = timm, route = no-deps).

Real controlled `pip install timm --no-deps --target <path>` (NO global install, NO transitive
deps). Records version, target-path files, find_spec('timm')-only probe, global-env
contamination audit, post-review, rollback readiness. Does NOT real import timm/mobile_sam,
model load/retry, inference/runtime/output/semantic, registry mutation, extra downloads.
Three outcomes: GO, FAILED_NO_BOUNDARY_VIOLATION, BLOCKED. timm install success is NOT
model-load/inference/runtime approval. Protected test board records in `real_test` mode.
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

PHASE_ID = "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_dependency_repair_nodeps_install_execution_and_post_review_v1"

INSTALL_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only，target=timm，route=no-deps。受控 pip install timm --no-deps "
    "--target <path>（不全局安装、不拉传递依赖）：pre-install snapshot、真实安装、版本记录、target path 记录、"
    "find_spec('timm') 探针（不真实 import）、全局环境污染审计、post-review、rollback readiness。"
    "不真实 import timm/mobile_sam、不 model load、不 retry、不 inference/runtime/output/语义层、"
    "不改 registry、不额外权重下载。torch/torchvision 不得装入 target。三种诚实结局：GO、"
    "FAILED_NO_BOUNDARY_VIOLATION、BLOCKED。timm no-deps 安装成功 ≠ model-load/inference/runtime 批准。"
    "测试板块 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "nodeps_timm_install_only_reuse_torch_no_transitive_deps_no_import_no_load"
)

REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
TARGET_DEPENDENCY = "timm"
SELECTED_ROUTE = "timm_no_deps_controlled_install"
NODEPS_INSTALL_EXECUTION = True
POST_REVIEW_INCLUDED = True
TIMM_INSTALL_ALLOWED = True
PIP_INSTALL_ALLOWED = True
DEPENDENCY_INSTALL_ALLOWED = True
NO_DEPS_REQUIRED = True
INSTALL_SCOPE = "controlled_dependency_repair_only"
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
UPSTREAM_NODEPS_REQUEST_APPROVAL_REF = (
    "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Request-Approval-And-Readiness-v1-001"
)
UPSTREAM_NODEPS_REQUEST_APPROVAL_EXPECTED_GO = (
    "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_REQUEST_APPROVAL_AND_READINESS_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

CONTROLLED_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"
INSTALL_TIMEOUT_SECONDS = 600
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"

NEXT_PHASE_GO = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Dependency-Repair-NoDeps-Install-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

TIMM_PACKAGE_NAME = "timm"
TIMM_IMPORT_ROOT = "timm"

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_install_snapshot_but_install", "go_key": "pre_install_snapshot_present", "depends_on": "pre_install_snapshot_present"},
    {"guard_id": "invalid_b_install_target_not_timm", "go_key": "install_target_is_timm", "depends_on": "install_target_is_timm"},
    {"guard_id": "invalid_c_command_missing_no_deps", "go_key": "no_deps_flag_present", "depends_on": "no_deps_flag_present"},
    {"guard_id": "invalid_d_command_missing_target", "go_key": "target_flag_present", "depends_on": "target_flag_present"},
    {"guard_id": "invalid_e_install_scope_not_controlled", "go_key": "install_scope_controlled", "depends_on": "install_scope_controlled"},
    {"guard_id": "invalid_f_global_env_contamination_but_go", "go_key": "no_global_env_contamination", "depends_on": "no_global_env_contamination"},
    {"guard_id": "invalid_g_torch_torchvision_in_target_but_go", "go_key": "no_torch_torchvision_in_target", "depends_on": "no_torch_torchvision_in_target"},
    {"guard_id": "invalid_h_real_import_timm_or_mobile_sam", "go_key": "no_real_import", "depends_on": "no_real_import"},
    {"guard_id": "invalid_i_model_load_or_retry", "go_key": "no_model_load_retry", "depends_on": "no_model_load_retry"},
    {"guard_id": "invalid_j_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_k_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_l_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_m_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_n_post_install_probe_not_find_spec_only", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_o_install_success_marked_model_load_success", "go_key": "install_not_model_load_success", "depends_on": "install_not_model_load_success"},
    {"guard_id": "invalid_p_install_success_marked_inference_runtime_ready", "go_key": "install_not_inference_runtime_ready", "depends_on": "install_not_inference_runtime_ready"},
    {"guard_id": "invalid_q_rollback_readiness_missing", "go_key": "rollback_readiness_present", "depends_on": "rollback_readiness_present"},
    {"guard_id": "invalid_r_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_s_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_t_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_u_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_nodeps_timm_install_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "target_dependency_is_timm",
    "pre_install_snapshot_is_required",
    "timm_install_is_allowed_only_with_no_deps",
    "timm_install_is_allowed_only_with_target_controlled_path",
    "global_install_is_not_allowed",
    "transitive_dependency_install_is_not_allowed_by_route",
    "torch_torchvision_must_not_be_installed_into_target",
    "global_environment_contamination_is_blocker",
    "real_import_is_not_allowed",
    "mobile_sam_import_is_not_allowed",
    "model_load_is_not_allowed",
    "model_load_retry_is_not_allowed",
    "inference_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "post_install_probe_must_be_find_spec_only",
    "timm_install_success_is_not_model_load_success",
    "timm_install_success_is_not_inference_approval",
    "timm_install_success_is_not_runtime_approval",
    "timm_install_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "rollback_readiness_is_required",
    "post_review_is_required",
    "candidate_only_boundary_is_preserved",
    "honest_failure_is_not_blocked_unless_boundary_violation",
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
    "timm_nodeps_pre_install_snapshot_record",
    "timm_nodeps_install_execution_record",
    "timm_nodeps_version_record",
    "timm_nodeps_target_path_record",
    "timm_nodeps_find_spec_probe_record",
    "timm_nodeps_environment_contamination_audit_record",
    "timm_nodeps_install_post_review_record",
    "timm_nodeps_rollback_readiness_record",
    "mobile_sam_model_load_retry_gate_record",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_NODEPS_INSTALL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "nodeps_route_reused": True,
    "torch_reuse_boundary_preserved": True,
}


@dataclass(frozen=True)
class P1MobileSAMNoDepsTimmInstallExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    target_dependency: str
    selected_route: str
    nodeps_install_execution: bool
    post_review_included: bool
    timm_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    no_deps_required: bool
    install_scope: str
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
    upstream_nodeps_request_approval_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class TimmNoDepsPreInstallSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    working_directory: str
    controlled_install_target_path: str
    pip_version: str
    pip_freeze_before_count: int
    pip_freeze_before_digest: str
    installed_package_list_before_count: int
    existing_timm_status_by_find_spec_only: bool
    target_path_before_exists: bool
    target_path_before_file_count: int
    target_path_before_size_bytes: int
    global_env_snapshot_ref: str
    rollback_snapshot_ref: str
    upstream_nodeps_request_approval_ref: str
    test_board_ref: str
    timestamp: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class TimmNoDepsInstallExecutionRecord:
    record_id: str
    command: str
    command_whitelisted: bool
    no_deps_flag_present: bool
    target_flag_present: bool
    install_target: str
    no_global_install: bool
    no_transitive_dependency_install_intended: bool
    install_attempted: bool
    return_code: int
    elapsed_seconds: float
    stdout_summary: str
    stderr_summary: str
    timm_install_success: bool
    install_error: str


@dataclass(frozen=True)
class TimmNoDepsVersionRecord:
    record_id: str
    timm_install_attempted: bool
    timm_install_success: bool
    resolved_version: str
    installed_version: str
    version_source: str
    version_fabricated: bool
    version_pin_preexisting: bool
    version_status: str
    lockfile_patch_required_later: bool


@dataclass(frozen=True)
class TimmNoDepsTargetPathRecord:
    record_id: str
    target_path: str
    target_path_exists: bool
    target_path_file_count: int
    target_path_size_bytes: int
    installed_dist_info_dirs: Tuple[str, ...]
    installed_top_level_dirs: Tuple[str, ...]
    timm_package_dir_exists: bool
    unexpected_large_files_detected: bool
    torch_files_installed_in_target: bool
    torchvision_files_installed_in_target: bool
    no_transitive_dependencies_installed: bool


@dataclass(frozen=True)
class TimmNoDepsFindSpecProbeRecord:
    record_id: str
    probe_method: str
    probe_target: str
    find_spec_result: bool
    found_origin: str
    target_path_used_for_probe: bool
    real_import_used: bool
    mobile_sam_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool


@dataclass(frozen=True)
class TimmNoDepsEnvironmentContaminationAudit:
    audit_id: str
    pip_freeze_after_count: int
    pip_freeze_after_digest: str
    installed_package_list_after_count: int
    global_env_changed: bool
    torch_changed: bool
    torchvision_changed: bool
    torch_version_before: str
    torch_version_after: str
    torchvision_version_before: str
    torchvision_version_after: str
    contamination_detected: bool
    no_global_env_contamination: bool
    dependency_mutation_scope: str


@dataclass(frozen=True)
class TimmNoDepsInstallPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    install_command_whitelisted: bool
    no_deps_flag_present: bool
    install_scope_controlled: bool
    timm_install_attempted: bool
    timm_install_success: bool
    timm_version_recorded: bool
    find_spec_probe_only: bool
    find_spec_timm: bool
    real_import_performed: bool
    mobile_sam_import_performed: bool
    model_load_performed: bool
    inference_performed: bool
    runtime_performed: bool
    output_adapter_performed: bool
    semantic_layer_performed: bool
    registry_mutation_performed: bool
    additional_weight_download_performed: bool
    torch_or_torchvision_installed_in_target: bool
    global_env_contamination: bool
    rollback_ready: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class TimmNoDepsRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_not_executed_by_default: bool
    rollback_target_path: str
    rollback_removes_timm_target_if_failed: bool
    rollback_preserves_mobile_sam_code: bool
    rollback_preserves_weight_file: bool
    rollback_preserves_registry: bool
    rollback_preserves_test_board: bool
    rollback_preserves_review_artifacts: bool
    global_env_contamination_check_done: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRetryGateAfterNoDepsInstall:
    record_id: str
    can_enter_model_load_retry_next: bool
    timm_nodeps_install_execution_go: bool
    timm_find_spec_verified: bool
    timm_dependency_available: bool
    mobile_sam_weight_sha256_recheck_required_before_retry: bool
    mobile_sam_code_and_weight_ready_must_be_reverified: bool
    torch_torchvision_reuse_boundary_must_be_checked_at_retry: bool
    model_load_retry_requires_separate_execution_phase: bool
    timm_nodeps_install_success_not_model_load_success: bool
    timm_nodeps_install_success_not_inference_approval: bool
    timm_nodeps_install_success_not_runtime_approval: bool
    timm_nodeps_install_success_not_output_adapter_approval: bool
    timm_nodeps_install_success_not_semantic_layer_approval: bool
    recommended_next_phase: str


@dataclass
class NegativeTimmNoDepsInstallExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMNoDepsTimmInstallExecutionDecision:
    decision_ref: str
    mobile_sam_nodeps_timm_install_execution_profile_count: int
    timm_nodeps_pre_install_snapshot_record_count: int
    timm_nodeps_install_execution_record_count: int
    timm_nodeps_version_record_count: int
    timm_nodeps_target_path_record_count: int
    timm_nodeps_find_spec_probe_record_count: int
    timm_nodeps_environment_contamination_audit_count: int
    timm_nodeps_install_post_review_audit_count: int
    timm_nodeps_rollback_readiness_record_count: int
    mobile_sam_model_load_retry_gate_after_nodeps_install_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    timm_install_success: bool
    timm_find_spec_verified: bool
    no_global_env_contamination: bool
    no_transitive_dependency_install_violation: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
