# -*- coding: utf-8 -*-
"""P1 MobileSAM Model Load Failure Review And Repair Planning — types v1
(PLANNING ONLY, scope = mobile_sam_only).

Reviews the upstream MobileSAM model-load trial FAILED_NO_BOUNDARY_VIOLATION result and
plans a controlled repair. The failure is NOT a model-capability failure, NOT a weight-
download failure, NOT a checkpoint corruption — it is a runtime/model-load DEPENDENCY
GAP: `timm` is missing (ModuleNotFoundError). This phase only reviews the root cause,
records the `timm` dependency gap, plans the controlled repair, routes the next
dependency-install request/approval/readiness phase, and plans the model-load retry
gate. It does NOT install `timm` / pip install / install any dependency, does NOT real
import / model load / retry, does NOT inference / segmentation / prediction / runtime /
output adapter / semantic promotion, does NOT mutate the registry, and downloads NOTHING
extra. Dependency-repair planning is NOT a `timm` install approval; a future `timm`
install would NOT be model-load success, NOT inference/runtime approval. Protected, non-
deletable test board records are written in `planning` mode.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-MobileSAM-Model-Load-Failure-Review-And-Repair-Planning-v1-001"
SCOPE = "p1_mobile_sam_model_load_failure_review_and_repair_planning"
WEIGHT_CHAIN = "p1_mobile_sam_model_load_failure_review_and_repair_planning_v1"

REPAIR_PRINCIPLE_ZH = (
    "纯规划，scope=mobile_sam_only。复核上游 model-load trial 的 FAILED_NO_BOUNDARY_VIOLATION：失败不是模型坏、不是权重坏、"
    "不是 checkpoint 损坏，而是 model-load 阶段暴露的运行期依赖缺口——timm 缺失（ModuleNotFoundError）。本阶段只复核根因、"
    "记录 timm 依赖缺口、规划受控修复、路由下一步依赖安装 request/approval/readiness、规划 model-load 重试门槛。不装 timm、"
    "不 pip install、不装任何依赖、不真实 import、不 model load、不 retry、不 inference/segmentation/prediction/runtime/"
    "output adapter/语义层、不改 registry、不额外下载。依赖修复规划 ≠ timm 安装批准；未来 timm 安装 ≠ model-load 成功 ≠ "
    "inference/runtime 批准。测试板块 planning 模式，protected、non-deletable。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "failure_is_dependency_gap_not_model_or_weight_failure_repair_planning_only_no_install_no_load_no_inference"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
MOBILE_SAM_ONLY = True
FAILURE_REVIEW = True
REPAIR_PLANNING_ONLY = True
DEPENDENCY_REPAIR_PLANNING_ONLY = True
TIMM_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
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

UPSTREAM_TRIAL_EXECUTION_REF = "Phase-P1-MobileSAM-Model-Load-Trial-Execution-And-Post-Review-v1-001"
UPSTREAM_TRIAL_EXECUTION_EXPECTED_DECISION = "P1_MOBILE_SAM_MODEL_LOAD_TRIAL_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Upstream trial-execution artifact directory (read for failure evidence).
UPSTREAM_OUTPUT_DIR_REL = "_tmp_eval_out/p1_mobile_sam_model_load_trial_execution_and_post_review_v1_smoke_v0"
UPSTREAM_REVIEW_FILE = "p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json"
UPSTREAM_EVIDENCE_FILES: Tuple[str, ...] = (
    "p1_mobile_sam_model_load_trial_execution_and_post_review_review_v1.json",
    "mobile_sam_pre_model_load_snapshot_v1.json",
    "mobile_sam_sha256_recheck_v1.json",
    "mobile_sam_model_import_record_v1.json",
    "mobile_sam_model_load_execution_record_v1.json",
    "mobile_sam_memory_timeout_monitor_v1.json",
    "mobile_sam_model_load_post_review_audit_v1.json",
)

# Follow-up phases.
NEXT_PHASE_DEPENDENCY_INSTALL_REQUEST = "Phase-P1-MobileSAM-Dependency-Repair-Install-Request-Approval-And-Readiness-v1-001"
SUGGESTED_RETRY_PHASE = "Phase-P1-MobileSAM-Model-Load-Trial-Retry-Execution-And-Post-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Failure facts (the attribution target).
# --------------------------------------------------------------------------- #
MOBILE_SAM_ASSET_ID = "mobile_sam"
MISSING_DEPENDENCY = "timm"
EXPECTED_ERROR_CLASS = "ModuleNotFoundError"
EXPECTED_ERROR_SUBSTRING = "No module named 'timm'"
FAILURE_CATEGORY = "dependency_gap"
MOBILE_SAM_WEIGHT_SHA256 = "6dbb90523a35330fedd7f1d3dfc66f995213d81b29a5ca8108dbcdd4e37d6c2f"
MOBILE_SAM_WEIGHT_SIZE_BYTES = 40728226

# --------------------------------------------------------------------------- #
# Negative guards (17: Invalid A..Q).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_failed_no_boundary_violation", "go_key": "upstream_failed_no_boundary_violation", "depends_on": "upstream_failed_no_boundary_violation"},
    {"guard_id": "invalid_b_upstream_boundary_violation_present", "go_key": "upstream_boundary_clean", "depends_on": "upstream_boundary_clean"},
    {"guard_id": "invalid_c_sha256_size_mismatch_attributed_to_timm", "go_key": "sha256_size_valid_before_attribution", "depends_on": "sha256_size_valid_before_attribution"},
    {"guard_id": "invalid_d_no_real_import_failure_evidence_attributed_to_timm", "go_key": "real_import_failure_evidence_present", "depends_on": "real_import_failure_evidence_present"},
    {"guard_id": "invalid_e_error_not_modulenotfound_timm_but_attributed", "go_key": "error_is_modulenotfound_timm", "depends_on": "error_is_modulenotfound_timm"},
    {"guard_id": "invalid_f_install_timm_pip_install_dependency_install", "go_key": "no_install_in_this_phase", "depends_on": "no_install_in_this_phase"},
    {"guard_id": "invalid_g_real_import_model_load_retry", "go_key": "no_import_load_retry", "depends_on": "no_import_load_retry"},
    {"guard_id": "invalid_h_inference_segmentation_prediction", "go_key": "no_inference_seg_pred", "depends_on": "no_inference_seg_pred"},
    {"guard_id": "invalid_i_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_j_extra_weight_model_checkpoint_dataset_example_download", "go_key": "no_additional_download", "depends_on": "no_additional_download"},
    {"guard_id": "invalid_k_registry_mutation", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_l_repair_planning_treated_as_timm_install_approval", "go_key": "repair_planning_not_install_approval", "depends_on": "repair_planning_not_install_approval"},
    {"guard_id": "invalid_m_timm_install_treated_as_model_load_approval", "go_key": "timm_install_not_model_load_approval", "depends_on": "timm_install_not_model_load_approval"},
    {"guard_id": "invalid_n_repair_success_treated_as_inference_runtime_approval", "go_key": "repair_success_not_inference_runtime_approval", "depends_on": "repair_success_not_inference_runtime_approval"},
    {"guard_id": "invalid_o_test_process_or_conclusion_not_written", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_p_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_q_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (34 phase + 6 test board = 40).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_mobile_sam_model_load_failure_review_and_repair_planning_only",
    "scope_is_mobile_sam_only",
    "upstream_must_be_failed_no_boundary_violation",
    "upstream_boundary_must_be_clean",
    "sha256_and_size_must_be_valid_before_dependency_gap_attribution",
    "missing_dependency_evidence_must_be_real",
    "failure_root_cause_is_dependency_gap_not_weight_corruption",
    "timm_install_is_not_allowed_in_this_phase",
    "pip_install_is_not_allowed_in_this_phase",
    "dependency_install_is_not_allowed_in_this_phase",
    "real_import_is_not_allowed_in_this_phase",
    "model_load_is_not_allowed_in_this_phase",
    "model_load_retry_is_not_allowed_in_this_phase",
    "inference_is_not_allowed",
    "segmentation_prediction_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "additional_weight_download_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "dependency_repair_planning_is_not_timm_install_approval",
    "timm_install_success_would_not_be_model_load_success",
    "timm_install_success_would_not_be_inference_approval",
    "timm_install_success_would_not_be_runtime_approval",
    "model_load_retry_success_would_not_be_inference_approval",
    "model_load_retry_success_would_not_be_runtime_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "mobile_sam_model_load_failure_audit_record",
    "mobile_sam_dependency_gap_record",
    "mobile_sam_timm_repair_plan_record",
    "mobile_sam_dependency_install_request_route_record",
    "mobile_sam_model_load_retry_gate_record",
    "mobile_sam_inference_runtime_boundary_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1MobileSAMModelLoadFailureRepairPlanningProfile",
    "MobileSAMModelLoadFailureAudit",
    "MobileSAMDependencyGapRecord",
    "MobileSAMTimmRepairPlanningRecord",
    "MobileSAMDependencyInstallRequestRoute",
    "MobileSAMModelLoadRetryGatePlanningRecord",
    "MobileSAMRepairRiskRecord",
    "MobileSAMInferenceRuntimeBoundaryRecord",
    "MobileSAMRepairFollowupRoute",
    "NegativeMobileSAMModelLoadFailureRepairPlanningGuard",
    "P1MobileSAMModelLoadFailureRepairPlanningDecision",
)

FINAL_DECISION_GO = "P1_MOBILE_SAM_MODEL_LOAD_FAILURE_REVIEW_AND_REPAIR_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MOBILE_SAM_MODEL_LOAD_FAILURE_REVIEW_AND_REPAIR_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_mode_reused": True,
    "upstream_failure_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1MobileSAMModelLoadFailureRepairPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    mobile_sam_only: bool
    failure_review: bool
    repair_planning_only: bool
    dependency_repair_planning_only: bool
    timm_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    additional_weight_download_allowed: bool
    commercial_runtime_approved: bool
    upstream_trial_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MobileSAMModelLoadFailureAudit:
    audit_id: str
    upstream_review_file_ref: str
    upstream_review_exists: bool
    final_decision_observed: str
    final_decision_ok: bool
    blocker_count_observed: int
    no_boundary_violation_observed: bool
    sha256_matches_observed: bool
    size_matches_observed: bool
    real_import_attempted_observed: bool
    import_success_observed: bool
    error_class_observed: str
    error_message_observed: str
    error_is_modulenotfound_timm: bool
    checkpoint_load_attempted_observed: bool
    checkpoint_load_success_observed: bool
    image_input_used: bool
    segmentation_used: bool
    prediction_used: bool
    inference_used: bool
    runtime_used: bool
    output_adapter_used: bool
    semantic_layer_used: bool
    registry_mutation_performed: bool
    additional_download_performed: bool
    failure_is_reproducible_candidate: bool
    failure_category: str
    root_cause_candidate: str
    weight_integrity_related: bool
    checkpoint_corruption_related: bool
    model_code_missing_related: bool
    environment_dependency_related: bool
    boundary_violation_related: bool
    registry_patch_required_now: bool
    weight_redownload_required: bool
    source_reinstall_required: bool
    model_load_retry_required_after_dependency_repair: bool
    not_model_capability_failure: bool
    not_weight_download_failure: bool
    not_checkpoint_corruption: bool
    is_transitive_dependency_gap: bool
    audit_passed: bool


@dataclass(frozen=True)
class MobileSAMDependencyGapRecord:
    record_id: str
    dependency_name: str
    dependency_role: str
    dependency_status: str
    discovered_at_phase: str
    discovered_by: str
    package_install_required: bool
    install_scope_required: str
    global_install_allowed: bool
    version_status: str
    version_resolution_required: bool
    license_review_required: bool
    transitive_dependency_review_required: bool
    pip_install_requires_separate_request: bool
    owner_approval_required: bool
    install_execution_not_allowed_now: bool


@dataclass(frozen=True)
class MobileSAMTimmRepairPlanningRecord:
    record_id: str
    repair_target: str
    repair_action_candidate: str
    repair_action_not_executed: bool
    clean_pypi_candidate: bool
    package_name_candidate: str
    import_root_candidate: str
    version_pin_required: bool
    hash_or_lockfile_recommended: bool
    dependency_conflict_review_required: bool
    torch_compatibility_review_required: bool
    offline_or_cached_install_preferred_if_available: bool
    rollback_required: bool
    post_install_probe_required: bool
    probe_method: str
    real_import_after_install_not_allowed_until_model_load_retry: bool


@dataclass(frozen=True)
class MobileSAMDependencyInstallRequestRoute:
    route_id: str
    recommended_next_phase: str
    allows_timm_install_request: bool
    allows_owner_approval_issuance: bool
    allows_package_version_license_dependency_review: bool
    allows_command_whitelist: bool
    allows_readiness_review: bool
    still_no_direct_pip_install: bool
    still_no_model_load: bool
    still_no_inference: bool
    still_no_runtime: bool
    still_no_registry_mutation: bool


@dataclass(frozen=True)
class MobileSAMModelLoadRetryGatePlanningRecord:
    record_id: str
    model_load_retry_allowed_now: bool
    timm_install_request_go_required: bool
    timm_owner_approval_granted_required: bool
    timm_install_execution_go_required: bool
    timm_find_spec_verified_required: bool
    no_global_env_contamination_required: bool
    mobile_sam_weight_sha256_rechecked_required: bool
    mobile_sam_code_and_weight_ready_still_valid_required: bool
    model_load_retry_command_whitelist_updated_required: bool
    test_board_ready_required: bool
    suggested_retry_phase: str


@dataclass(frozen=True)
class MobileSAMRepairRiskRecord:
    record_id: str
    timm_version_compatibility_risk: str
    torch_compatibility_risk: str
    transitive_dependency_risk: str
    package_supply_chain_risk: str
    global_environment_contamination_risk: str
    hidden_import_dependency_risk: str
    repeated_model_load_failure_risk: str
    model_load_retry_scope_creep_risk: str
    inference_boundary_violation_risk: str
    runtime_boundary_violation_risk: str


@dataclass(frozen=True)
class MobileSAMInferenceRuntimeBoundaryRecord:
    record_id: str
    dependency_repair_success_not_model_load_success: bool
    timm_install_success_not_inference_approval: bool
    timm_install_success_not_runtime_approval: bool
    model_load_retry_success_not_inference_approval: bool
    model_load_retry_success_not_runtime_approval: bool
    inference_requires_separate_trial: bool
    runtime_requires_separate_trial: bool
    output_adapter_requires_separate_review: bool
    semantic_layer_requires_separate_promotion: bool
    commercial_runtime_not_approved: bool


@dataclass(frozen=True)
class MobileSAMRepairFollowupRoute:
    route_id: str
    recommended_next_phase: str
    next_phase_scope: str
    next_phase_purpose: str
    suggested_retry_phase: str
    optional_followup_phase: Optional[str]


@dataclass
class NegativeMobileSAMModelLoadFailureRepairPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MobileSAMModelLoadFailureRepairPlanningDecision:
    decision_ref: str
    mobile_sam_model_load_failure_repair_planning_profile_count: int
    mobile_sam_model_load_failure_audit_count: int
    mobile_sam_dependency_gap_record_count: int
    mobile_sam_timm_repair_plan_record_count: int
    mobile_sam_dependency_install_request_route_count: int
    mobile_sam_model_load_retry_gate_planning_record_count: int
    mobile_sam_repair_risk_record_count: int
    mobile_sam_inference_runtime_boundary_record_count: int
    mobile_sam_repair_followup_route_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
