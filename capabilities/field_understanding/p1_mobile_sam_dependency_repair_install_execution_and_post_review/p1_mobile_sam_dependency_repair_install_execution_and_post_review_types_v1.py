# -*- coding: utf-8 -*-
"""P1 MobileSAM Dependency Repair Install Execution And Post Review — types v1
(REAL EXECUTION, scope = mobile_sam_only, target = timm).

The FIRST real controlled install for the `timm` dependency gap. It allows a pre-install
snapshot, real timm version resolution, a REAL controlled `--target` install of timm (NO
global install), a dependency-mutation record, a find_spec('timm')-only post-install probe
(NO real import), a global-environment contamination audit, a post-review, and rollback
readiness. It does NOT real import timm / mobile_sam, does NOT model load / model-load
retry / inference / segmentation / prediction / runtime / output adapter / semantic
promotion, does NOT mutate the registry, and downloads NO extra weight. Three honest
outcomes: GO (install succeeds + find_spec true + no contamination), FAILED_NO_BOUNDARY_
VIOLATION (install/find_spec fails but no boundary violation), or BLOCKED (global env
contamination, uncontrolled scope, real import, model load, inference/runtime, registry
mutation, or test-board failure). timm install success is NOT model-load / inference /
runtime / output-adapter / semantic approval. Protected, non-deletable test board records
are written in `real_test` mode.
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

PHASE_ID = "Phase-P1-MobileSAM-Dependency-Repair-Install-Execution-And-Post-Review-v1-001"
SCOPE = "p1_mobile_sam_dependency_repair_install_execution_and_post_review"
WEIGHT_CHAIN = "p1_mobile_sam_dependency_repair_install_execution_and_post_review_v1"

INSTALL_PRINCIPLE_ZH = (
    "真实执行，scope=mobile_sam_only，target=timm。首次受控依赖安装：pre-install snapshot、真实解析 timm 版本、真实受控 "
    "--target 安装 timm（不全局安装）、记录依赖变化、find_spec('timm') 探针（不真实 import）、全局环境污染审计、post-review、"
    "rollback readiness。不真实 import timm/mobile_sam、不 model load、不 retry、不 inference/segmentation/prediction、"
    "不 runtime/output adapter/语义层、不改 registry、不额外权重下载。三种诚实结局：GO（安装成功+find_spec=true+无污染）、"
    "FAILED_NO_BOUNDARY_VIOLATION（安装或 find_spec 失败但无边界违规）、BLOCKED（全局污染/越权 scope/真实 import/model load/"
    "inference/runtime/registry mutation/test board 失败）。timm 安装成功 ≠ model-load/inference/runtime/output/语义 批准。"
    "测试板块 real_test 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "controlled_timm_install_only_no_import_no_load_install_success_is_not_model_load_success"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
MOBILE_SAM_ONLY = True
TARGET_DEPENDENCY = "timm"
DEPENDENCY_REPAIR_INSTALL_EXECUTION = True
POST_REVIEW_INCLUDED = True
TIMM_INSTALL_ALLOWED = True
PIP_INSTALL_ALLOWED = True
DEPENDENCY_INSTALL_ALLOWED = True
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

UPSTREAM_REQUEST_APPROVAL_REF = "Phase-P1-MobileSAM-Dependency-Repair-Install-Request-Approval-And-Readiness-v1-001"
UPSTREAM_REQUEST_APPROVAL_EXPECTED_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_REQUEST_APPROVAL_AND_READINESS_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Controlled install target path (isolated; NOT global site-packages).
CONTROLLED_INSTALL_TARGET_REL = "_tmp_eval_out/p1_timm_repair_workspace/install_target"

# Follow-up phases (decision-dependent).
NEXT_PHASE_GO = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"
NEXT_PHASE_FAILED = "Phase-P1-MobileSAM-Dependency-Repair-Install-Failure-Review-And-Repair-Planning-v1-001"
NEXT_PHASE_BLOCKED = "Phase-P1-MobileSAM-Dependency-Repair-Install-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Facts.
# --------------------------------------------------------------------------- #
MOBILE_SAM_ASSET_ID = "mobile_sam"
TIMM_PACKAGE_NAME = "timm"
TIMM_IMPORT_ROOT = "timm"
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
INSTALL_TIMEOUT_SECONDS = 1200

# --------------------------------------------------------------------------- #
# Negative guards (18: Invalid A..R).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_install_snapshot_but_install", "go_key": "pre_install_snapshot_present", "depends_on": "pre_install_snapshot_present"},
    {"guard_id": "invalid_b_install_target_not_timm", "go_key": "install_target_is_timm", "depends_on": "install_target_is_timm"},
    {"guard_id": "invalid_c_install_scope_not_controlled", "go_key": "install_scope_controlled", "depends_on": "install_scope_controlled"},
    {"guard_id": "invalid_d_global_env_contamination_but_go", "go_key": "no_global_env_contamination", "depends_on": "no_global_env_contamination"},
    {"guard_id": "invalid_e_real_import_timm_or_mobile_sam", "go_key": "no_real_import", "depends_on": "no_real_import"},
    {"guard_id": "invalid_f_model_load_or_retry", "go_key": "no_model_load_retry", "depends_on": "no_model_load_retry"},
    {"guard_id": "invalid_g_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_h_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_i_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_j_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_k_post_install_probe_not_find_spec_only", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_l_install_success_marked_model_load_success", "go_key": "install_not_model_load_success", "depends_on": "install_not_model_load_success"},
    {"guard_id": "invalid_m_install_success_marked_inference_runtime_ready", "go_key": "install_not_inference_runtime_ready", "depends_on": "install_not_inference_runtime_ready"},
    {"guard_id": "invalid_n_rollback_readiness_missing", "go_key": "rollback_readiness_present", "depends_on": "rollback_readiness_present"},
    {"guard_id": "invalid_o_post_review_missing", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_p_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_q_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (32 phase + 6 test board = 38).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_dependency_repair_install_execution_and_post_review",
    "scope_is_mobile_sam_only",
    "target_dependency_is_timm",
    "pre_install_snapshot_is_required",
    "timm_install_is_allowed_only_in_controlled_target_or_env",
    "global_install_is_not_allowed",
    "global_environment_contamination_is_blocker",
    "real_import_is_not_allowed",
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
    "timm_pre_install_snapshot_record",
    "timm_version_resolution_record",
    "timm_install_execution_record",
    "timm_dependency_mutation_record",
    "timm_find_spec_probe_record",
    "timm_environment_contamination_audit_record",
    "timm_install_post_review_record",
    "timm_rollback_readiness_record",
    "mobile_sam_model_load_retry_gate_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMDependencyRepairInstallExecutionPostReviewProfile",
    "TimmPreInstallSnapshotRecord",
    "TimmVersionResolutionRecord",
    "TimmInstallExecutionRecord",
    "TimmDependencyMutationRecord",
    "TimmFindSpecProbeRecord",
    "TimmEnvironmentContaminationAudit",
    "TimmInstallPostReviewAudit",
    "TimmRollbackReadinessRecord",
    "MobileSAMModelLoadRetryGateAfterTimmInstall",
    "NegativeTimmDependencyRepairInstallExecutionGuard",
    "P1MobileSAMDependencyRepairInstallExecutionDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_DEPENDENCY_REPAIR_INSTALL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "controlled_install_target_isolated": True,
    "global_env_preserved": True,
}


@dataclass(frozen=True)
class P1MobileSAMDependencyRepairInstallExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    mobile_sam_only: bool
    target_dependency: str
    dependency_repair_install_execution: bool
    post_review_included: bool
    timm_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
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
    upstream_request_approval_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class TimmPreInstallSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    working_directory: str
    controlled_install_target_path: str
    pip_version: str
    pip_freeze_before_count: int
    pip_freeze_before_digest: str
    installed_package_list_before_count: int
    sys_path_plan: str
    existing_timm_status_by_find_spec_only: bool
    global_env_snapshot_ref: str
    rollback_snapshot_ref: str
    upstream_request_approval_ref: str
    test_board_ref: str
    timestamp: str
    snapshot_succeeded: bool


@dataclass(frozen=True)
class TimmVersionResolutionRecord:
    record_id: str
    package_name: str
    import_root: str
    version_resolution_attempted: bool
    version_pin_preexisting: bool
    resolved_version: str
    installed_version: str
    version_resolution_evidence_ref: str
    version_fabricated: bool
    version_status: str


@dataclass(frozen=True)
class TimmInstallExecutionRecord:
    record_id: str
    command: str
    command_whitelisted: bool
    install_target: str
    no_global_install: bool
    install_attempted: bool
    return_code: int
    stdout_summary: str
    stderr_summary: str
    installed_files_count: int
    timm_install_success: bool
    install_error: str


@dataclass(frozen=True)
class TimmDependencyMutationRecord:
    record_id: str
    pip_freeze_after_count: int
    pip_freeze_after_digest: str
    installed_package_list_after_count: int
    target_path_top_level_count: int
    new_packages_in_target_path: Tuple[str, ...]
    transitive_dependencies_installed: Tuple[str, ...]
    torch_changed: bool
    global_env_changed: bool
    no_global_env_contamination: bool
    dependency_mutation_scope: str


@dataclass(frozen=True)
class TimmFindSpecProbeRecord:
    record_id: str
    probe_method: str
    probe_target: str
    find_spec_result: bool
    found_origin: str
    real_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool


@dataclass(frozen=True)
class TimmEnvironmentContaminationAudit:
    audit_id: str
    global_site_packages_timm_present_before: bool
    global_site_packages_timm_present_after: bool
    global_env_changed: bool
    torch_version_before: str
    torch_version_after: str
    torch_changed: bool
    contamination_detected: bool
    install_confined_to_target: bool


@dataclass(frozen=True)
class TimmInstallPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    install_command_whitelisted: bool
    install_scope_controlled: bool
    timm_install_attempted: bool
    timm_install_success: bool
    timm_version_recorded: bool
    find_spec_probe_only: bool
    find_spec_timm: bool
    real_import_performed: bool
    model_load_performed: bool
    inference_performed: bool
    runtime_performed: bool
    output_adapter_performed: bool
    semantic_layer_performed: bool
    registry_mutation_performed: bool
    additional_weight_download_performed: bool
    global_env_contamination: bool
    rollback_ready: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class TimmRollbackReadinessRecord:
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
class MobileSAMModelLoadRetryGateAfterTimmInstall:
    record_id: str
    can_enter_model_load_retry_next: bool
    timm_install_execution_go: bool
    timm_find_spec_verified: bool
    timm_dependency_available: bool
    mobile_sam_weight_sha256_recheck_required_before_retry: bool
    mobile_sam_code_and_weight_ready_must_be_reverified: bool
    model_load_retry_requires_separate_execution_phase: bool
    timm_install_success_not_model_load_success: bool
    timm_install_success_not_inference_approval: bool
    timm_install_success_not_runtime_approval: bool
    timm_install_success_not_output_adapter_approval: bool
    timm_install_success_not_semantic_layer_approval: bool
    recommended_next_phase: str


@dataclass
class NegativeTimmDependencyRepairInstallExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMDependencyRepairInstallExecutionDecision:
    decision_ref: str
    mobile_sam_dependency_repair_install_execution_profile_count: int
    timm_pre_install_snapshot_record_count: int
    timm_version_resolution_record_count: int
    timm_install_execution_record_count: int
    timm_dependency_mutation_record_count: int
    timm_find_spec_probe_record_count: int
    timm_environment_contamination_audit_count: int
    timm_install_post_review_audit_count: int
    timm_rollback_readiness_record_count: int
    mobile_sam_model_load_retry_gate_after_timm_install_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    timm_install_success: bool
    timm_find_spec_verified: bool
    no_global_env_contamination: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
