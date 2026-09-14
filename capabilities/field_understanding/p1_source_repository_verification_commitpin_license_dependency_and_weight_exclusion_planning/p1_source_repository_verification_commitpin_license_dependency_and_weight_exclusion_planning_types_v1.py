# -*- coding: utf-8 -*-
"""P1 Source Repository Verification / CommitPin / License / Dependency /
Weight-Exclusion Planning — types v1 (PLANNING ONLY).

Compressed pre-retry planning for byte_track and mobile_sam. It merges the
problems that MUST be resolved before the next source-execution retry:
  1. who the real repository candidate is,
  2. how commit pin should be determined,
  3. how license review is done,
  4. how dependency review is done,
  5. how mobile_sam avoids cloning committed checkpoint weights.

It only PLANS. It executes/mutates NOTHING and does NO network lookup: no git
clone, no source checkout, no source install, no pip install, no dependency
install, no model/weight/dataset/example download, no real import, no model load,
no inference, no runtime, no output adapter, no semantic layer, no registry
mutation. Repository candidates remain unverified, commits remain unpinned,
license/dependency reviews remain uncompleted (this is planning, not the review).
A weight-excluding checkout plan is required for mobile_sam BEFORE any retry, and
weight-exclusion PLANNING is NOT weight-download approval. Protected,
non-deletable test board records are written in planning mode.
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

PHASE_ID = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Planning-v1-001"
SCOPE = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning"
SOURCE_CHAIN = "p1_source_repository_verification_commitpin_license_dependency_and_weight_exclusion_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "byte_track 与 mobile_sam 的合并前置规划：解决下一次 source execution retry 前必须明确的问题——真实仓库候选是谁、"
    "commit pin 如何确定、license review 怎么做、dependency review 怎么做、mobile_sam 如何避免 clone 到 checkpoint 权重。"
    "本阶段只做 planning，不联网检索、不 clone、不 checkout、不源码安装、不 pip install、不安装依赖、不下载模型/权重/"
    "数据集/示例资产、不真实 import / model load / inference、不进入 runtime / output adapter / 语义层、不修改 registry。"
    "repository candidate 保持未验证，commit 保持未 pin，license/dependency review 保持未完成（本阶段是规划，不是 review）。"
    "mobile_sam 重试前必须有 weight-excluding checkout plan；weight-exclusion 规划不是权重下载批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_repository_verification_commitpin_license_dependency_weight_exclusion_is_planning_only_no_network_no_clone_no_install_no_weight_download"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
PLANNING_ONLY = True
REPOSITORY_VERIFICATION_PLANNING_ONLY = True
COMMIT_PIN_PLANNING_ONLY = True
LICENSE_REVIEW_PLANNING_ONLY = True
DEPENDENCY_REVIEW_PLANNING_ONLY = True
WEIGHT_EXCLUSION_PLANNING_ONLY = True

REGISTRY_MUTATION_ALLOWED = False
NETWORK_LOOKUP_ALLOWED = False
GIT_CLONE_ALLOWED = False
SOURCE_CHECKOUT_ALLOWED = False
SOURCE_INSTALL_ALLOWED = False
PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
EXAMPLE_ASSET_DOWNLOAD_ALLOWED = False
REAL_IMPORT_ALLOWED = False
MODEL_LOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False
WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL = True

SOURCE_EXECUTION_RETRY_ALLOWED_NOW = False
SOURCE_EXECUTION_RETRY_REQUIRES_FUTURE_READINESS = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Source-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Source-Install-Execution-v1-001"
UPSTREAM_PREP_READINESS_REF = "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001"
UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_RESOLUTION_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_POST_REVIEW_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_POST_REVIEW_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# This phase only ROUTES to the next (network-enabled) review phase.
RECOMMENDED_NEXT_PHASE_REF = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Review-v1-001"
NEXT_STEP_REF = RECOMMENDED_NEXT_PHASE_REF

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Input scope (only the two deferred assets).
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

# Weight/checkpoint extensions to block in any future checkout.
BLOCKED_WEIGHT_PATTERNS: Tuple[str, ...] = (
    "*.pth", "*.pt", "*.ckpt", "*.safetensors", "*.onnx", "*.bin", "*.h5", "*.pb",
)

# Source-execution-retry readiness preconditions (10; all currently unsatisfied).
RETRY_READINESS_PRECONDITIONS: Tuple[str, ...] = (
    "repository_url_verified",
    "commit_hash_pinned",
    "source_license_review_completed",
    "dependency_review_completed",
    "network_boundary_finalized",
    "command_whitelist_finalized",
    "source_checkout_strategy_finalized",
    "rollback_ready",
    "test_board_ready",
    "mobile_sam_weight_excluding_checkout_plan_completed",
)

# Risk dimensions (10) recorded per asset.
RISK_DIMENSIONS: Tuple[str, ...] = (
    "fabricated_repository_risk",
    "commit_pin_fabrication_risk",
    "license_unknown_risk",
    "dependency_unknown_risk",
    "network_scope_risk",
    "source_install_side_effect_risk",
    "weight_download_contamination_risk",
    "environment_contamination_risk",
    "rollback_complexity_risk",
    "runtime_misreadiness_risk",
)

# --------------------------------------------------------------------------- #
# Negative guards (19: Invalid A..S).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_network_lookup_performed", "go_key": "no_network_lookup", "depends_on": "no_network_lookup"},
    {"guard_id": "invalid_b_git_clone_or_source_checkout", "go_key": "no_clone_checkout", "depends_on": "no_clone_checkout"},
    {"guard_id": "invalid_c_source_pip_dependency_install", "go_key": "no_install", "depends_on": "no_install"},
    {"guard_id": "invalid_d_model_weight_dataset_example_download", "go_key": "no_download", "depends_on": "no_download"},
    {"guard_id": "invalid_e_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_f_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_h_repository_candidate_faked_verified", "go_key": "repo_not_faked_verified", "depends_on": "repo_not_faked_verified"},
    {"guard_id": "invalid_i_commit_hash_faked_pinned", "go_key": "commit_not_fabricated", "depends_on": "commit_not_fabricated"},
    {"guard_id": "invalid_j_license_review_faked_completed", "go_key": "license_not_fabricated", "depends_on": "license_not_fabricated"},
    {"guard_id": "invalid_k_dependency_review_faked_completed", "go_key": "dependency_not_fabricated", "depends_on": "dependency_not_fabricated"},
    {"guard_id": "invalid_l_mobile_sam_weight_exclusion_plan_missing", "go_key": "weight_exclusion_plan_present", "depends_on": "weight_exclusion_plan_present"},
    {"guard_id": "invalid_m_mobile_sam_full_clone_weight_risk_unrecorded", "go_key": "weight_risk_recorded", "depends_on": "weight_risk_recorded"},
    {"guard_id": "invalid_n_weight_exclusion_planning_as_weight_download_approval", "go_key": "exclusion_not_download_approval", "depends_on": "exclusion_not_download_approval"},
    {"guard_id": "invalid_o_source_execution_retry_allowed_now", "go_key": "retry_not_allowed_now", "depends_on": "retry_not_allowed_now"},
    {"guard_id": "invalid_p_weight_download_default_allowed", "go_key": "weight_not_default_allowed", "depends_on": "weight_not_default_allowed"},
    {"guard_id": "invalid_q_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_r_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_s_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (37 phase + 6 test board = 43).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_repository_verification_commit_pin_license_dependency_and_weight_exclusion_planning_only",
    "only_byte_track_and_mobile_sam_are_in_scope",
    "no_network_lookup_is_allowed_in_this_phase",
    "no_git_clone_is_allowed",
    "no_source_checkout_is_allowed",
    "no_source_install_is_allowed",
    "no_pip_install_is_allowed",
    "no_dependency_install_is_allowed",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_example_asset_download_is_allowed",
    "no_real_import_is_allowed",
    "no_model_load_is_allowed",
    "no_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "repository_candidate_must_not_be_treated_as_verified",
    "commit_hash_must_not_be_fabricated",
    "license_review_must_not_be_fabricated",
    "dependency_review_must_not_be_fabricated",
    "mobile_sam_weight_excluding_checkout_plan_is_required",
    "mobile_sam_full_clone_weight_risk_must_be_recorded",
    "weight_excluding_checkout_planning_is_not_weight_download_approval",
    "source_execution_retry_is_not_allowed_now",
    "source_execution_retry_requires_future_readiness",
    "weight_download_is_not_approved",
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
    "repository_verification_plan_record",
    "commit_pin_plan_record",
    "license_review_plan_record",
    "dependency_review_plan_record",
    "mobile_sam_weight_exclusion_plan_record",
    "source_execution_retry_gate_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionPlanningProfile",
    "SourceRepositoryVerificationPlanningInput",
    "SourceRepositoryCandidatePlanningRecord",
    "SourceCommitPinPlanningRecord",
    "SourceLicenseReviewPlanningRecord",
    "SourceDependencyReviewPlanningRecord",
    "MobileSAMWeightExclusionPlanningRecord",
    "SourceExecutionRetryGatePlanningRecord",
    "SourceExecutionRetryReadinessPrecondition",
    "SourceRepositoryPlanningRiskRecord",
    "NegativeSourceRepositoryVerificationCommitPinPlanningGuard",
    "P1SourceRepositoryVerificationCommitPinPlanningDecision",
)

FINAL_DECISION_GO = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1SourceRepositoryVerificationCommitPinLicenseDependencyWeightExclusionPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    repository_verification_planning_only: bool
    commit_pin_planning_only: bool
    license_review_planning_only: bool
    dependency_review_planning_only: bool
    weight_exclusion_planning_only: bool
    registry_mutation_allowed: bool
    network_lookup_allowed: bool
    git_clone_allowed: bool
    source_checkout_allowed: bool
    source_install_allowed: bool
    pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    example_asset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    source_execution_retry_allowed_now: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_post_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceRepositoryVerificationPlanningInput:
    asset_id: str
    source_family: str
    from_all_deferred_no_violation: bool
    current_status: str
    source_execution_retry_allowed_now: bool
    weight_download_allowed_now: bool


@dataclass(frozen=True)
class SourceRepositoryCandidatePlanningRecord:
    asset_id: str
    source_family: str
    repository_candidate_required: bool
    repository_url_candidate_status: str
    repository_url_must_be_verified_before_execution: bool
    repository_candidate_must_not_be_fabricated: bool
    network_lookup_required_in_future_review: bool
    network_lookup_allowed_now: bool
    git_clone_allowed_now: bool
    source_checkout_allowed_now: bool
    repository_identity_resolution_required: bool
    package_import_identity_unresolved_or_source_component: bool
    repository_may_contain_committed_checkpoint_weight: bool
    full_clone_may_equal_weight_download: bool


@dataclass(frozen=True)
class SourceCommitPinPlanningRecord:
    asset_id: str
    commit_pin_required: bool
    commit_hash_currently_unverified: bool
    branch_or_tag_candidate_currently_unverified: bool
    commit_must_be_resolved_before_execution: bool
    commit_pin_must_not_be_fabricated: bool
    commit_drift_after_pin_blocks_execution: bool
    commit_pin_review_required: bool


@dataclass(frozen=True)
class SourceLicenseReviewPlanningRecord:
    asset_id: str
    license_review_required: bool
    source_license_currently_unverified: bool
    repository_license_file_must_be_checked: bool
    transitive_dependency_license_review_required: bool
    commercial_runtime_not_approved: bool
    license_review_must_complete_before_source_execution_retry: bool
    license_review_must_not_be_fabricated: bool


@dataclass(frozen=True)
class SourceDependencyReviewPlanningRecord:
    asset_id: str
    dependency_review_required: bool
    source_requirements_currently_unverified: bool
    transitive_dependencies_currently_unverified: bool
    dependency_conflict_review_required: bool
    build_or_compile_risk_review_required: bool
    torch_dependency_review_required: bool
    opencv_dependency_review_required: bool
    numpy_scipy_dependency_review_required: bool
    dependency_review_must_complete_before_source_execution_retry: bool
    dependency_review_must_not_be_fabricated: bool


@dataclass(frozen=True)
class MobileSAMWeightExclusionPlanningRecord:
    asset_id: str
    mobile_sam_weight_excluding_checkout_required: bool
    full_clone_may_include_committed_checkpoint_weight: bool
    weight_files_must_be_excluded_from_checkout_or_blocked: bool
    checkpoint_files_must_be_excluded_from_checkout_or_blocked: bool
    large_binary_files_must_be_detected_before_checkout: bool
    git_lfs_must_be_blocked_or_explicitly_scoped: bool
    sparse_checkout_or_archive_filtering_required_if_supported: bool
    allowed_file_patterns_must_be_defined_before_execution: bool
    blocked_file_patterns_must_include_weight_checkpoint_extensions: bool
    blocked_file_patterns: Tuple[str, ...]
    weight_excluding_checkout_plan_required_before_retry: bool
    weight_excluding_checkout_plan_success_not_weight_download_approval: bool
    weight_download_allowed: bool


@dataclass(frozen=True)
class SourceExecutionRetryReadinessPrecondition:
    precondition_id: str
    precondition: str
    required_before_retry: bool
    currently_satisfied: bool


@dataclass(frozen=True)
class SourceExecutionRetryGatePlanningRecord:
    gate_id: str
    source_execution_retry_allowed_now: bool
    source_execution_retry_requires_future_readiness: bool
    source_execution_retry_not_allowed_until_repository_verification_complete: bool
    source_execution_retry_not_allowed_until_commit_pin_complete: bool
    source_execution_retry_not_allowed_until_license_review_complete: bool
    source_execution_retry_not_allowed_until_dependency_review_complete: bool
    mobile_sam_retry_not_allowed_until_weight_excluding_checkout_plan_complete: bool
    readiness_precondition_count: int
    readiness_preconditions_all_unsatisfied_now: bool


@dataclass(frozen=True)
class SourceRepositoryPlanningRiskRecord:
    asset_id: str
    risk_dimensions: Tuple[str, ...]
    all_risk_dimensions_recorded: bool


@dataclass
class NegativeSourceRepositoryVerificationCommitPinPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1SourceRepositoryVerificationCommitPinPlanningDecision:
    decision_ref: str
    source_repository_verification_commitpin_planning_profile_count: int
    source_repository_verification_planning_input_count: int
    source_repository_candidate_planning_record_count: int
    source_commit_pin_planning_record_count: int
    source_license_review_planning_record_count: int
    source_dependency_review_planning_record_count: int
    mobile_sam_weight_exclusion_planning_record_count: int
    source_execution_retry_gate_planning_record_count: int
    source_execution_retry_readiness_precondition_count: int
    source_repository_planning_risk_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
