# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Preparation And Readiness Review — types v1.

COMPRESSED phase that merges three things for byte_track and mobile_sam:
  1. source approval issuance post-review (scope-limited to source install
     preparation only),
  2. source install preparation (preparation package + final requirements),
  3. source install readiness review (execution readiness decision).

It only produces a source install preparation package and a source execution
readiness decision. It executes NOTHING and MUTATES NOTHING: no git clone, no
source checkout, no source install, no pip install, no dependency install, no
model/weight/dataset download, no real import, no model load, no inference, no
runtime, no output adapter, no semantic layer, NO registry mutation, and NO
network repository lookup.

dependency_review_required_and_uncompleted and license_review_required_and_
uncompleted do NOT block this phase's GO (this is preparation/readiness planning,
not source execution); the next real source-execution phase MUST complete
repository verification / commit pin / license review / dependency review before
execution, else a stop condition blocks it. Both assets REMAIN DEFERRED.
Protected, non-deletable test board records are written in planning mode.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001"
SCOPE = "p1_controlled_source_install_preparation_and_readiness_review"
SOURCE_CHAIN = "p1_controlled_source_install_preparation_and_readiness_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "压缩阶段：合并 source approval issuance post-review、source install preparation、source install readiness "
    "review。复核源码安装 approval issuance 范围只限 source install preparation，并完成真实 source install execution "
    "前的准备与 readiness review。不 git clone、不 source checkout、不源码安装、不 pip install、不安装依赖、不下载模型/"
    "权重/数据集、不真实 import / model load / inference、不进入 runtime / output adapter / 语义层、不修改 registry、不"
    "联网检索仓库。只生成 source install preparation package 与 source execution readiness decision。"
    "dependency/license review 在本阶段标记为 required_and_uncompleted，不阻断本阶段 GO（本阶段是 preparation/readiness"
    "，不是 source execution）；下一阶段真实 source execution 必须在执行前完成 repository verification / commit pin / "
    "license review / dependency review，否则 stop condition 阻断。byte_track 与 mobile_sam 保持 DEFERRED。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_install_preparation_and_readiness_is_planning_only_no_clone_no_install_no_weight_download_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
COMPRESSED_PHASE = True
SOURCE_APPROVAL_ISSUANCE_POST_REVIEW_INCLUDED = True
SOURCE_INSTALL_PREPARATION_INCLUDED = True
SOURCE_INSTALL_READINESS_REVIEW_INCLUDED = True

SOURCE_INSTALL_PREPARATION_PACKAGE_CREATED = True
SOURCE_EXECUTION_READINESS_DECISION_CREATED = True
CAN_ENTER_CONTROLLED_SOURCE_INSTALL_EXECUTION_NEXT = True

GIT_CLONE_ALLOWED_IN_THIS_PHASE = False
SOURCE_CHECKOUT_ALLOWED_IN_THIS_PHASE = False
SOURCE_INSTALL_ALLOWED_IN_THIS_PHASE = False
PIP_INSTALL_ALLOWED_IN_THIS_PHASE = False
DEPENDENCY_INSTALL_ALLOWED_IN_THIS_PHASE = False
MODEL_DOWNLOAD_ALLOWED_IN_THIS_PHASE = False
WEIGHT_DOWNLOAD_ALLOWED_IN_THIS_PHASE = False
DATASET_DOWNLOAD_ALLOWED_IN_THIS_PHASE = False
REAL_IMPORT_ALLOWED_IN_THIS_PHASE = False
MODEL_LOAD_ALLOWED_IN_THIS_PHASE = False
REAL_INFERENCE_ALLOWED_IN_THIS_PHASE = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_REQUEST_PLANNING_REF = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
UPSTREAM_RESOLUTION_PLANNING_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
UPSTREAM_REGISTRY_CORRECTION_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
UPSTREAM_PACKAGE_RESOLUTION_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
UPSTREAM_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up phase candidate (this phase only routes; it does NOT create it).
SOURCE_INSTALL_EXECUTION_PHASE_REF = "Phase-P1-Controlled-Source-Install-Execution-v1-001"
NEXT_STEP_REF = SOURCE_INSTALL_EXECUTION_PHASE_REF

UPSTREAM_ISSUANCE_EXPECTED_GO = "P1_CONTROLLED_SOURCE_INSTALL_OWNER_APPROVAL_ISSUANCE_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "planning"

# --------------------------------------------------------------------------- #
# Prepared asset scope (locked) — ONLY the two deferred assets.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}

# Upstream approval issuance expected scope (for the scope audit).
EXPECTED_ISSUANCE_SCOPE: Dict[str, Any] = {
    "final_decision": UPSTREAM_ISSUANCE_EXPECTED_GO,
    "owner_approval_granted_for_source_install_preparation": True,
    "owner_approval_granted_for_git_clone": False,
    "owner_approval_granted_for_source_checkout": False,
    "owner_approval_granted_for_source_install": False,
    "owner_approval_granted_for_weight_download": False,
    "can_enter_source_install_preparation": True,
    "can_enter_source_install": False,
}

# Final command whitelist template text (TEMPLATE ONLY — never executed).
COMMAND_TEMPLATE_TEXT: Dict[str, str] = {
    "byte_track": (
        "# TEMPLATE_ONLY_DO_NOT_EXECUTE\n"
        "# git clone <verified_pinned_ByteTrack_or_YOLOX_repo> <controlled_checkout_path>\n"
        "# pip install --no-deps -e <controlled_checkout_path>  # code-only, no weights\n"
    ),
    "mobile_sam": (
        "# TEMPLATE_ONLY_DO_NOT_EXECUTE\n"
        "# git clone <verified_pinned_MobileSAM_repo> <controlled_checkout_path>\n"
        "# pip install --no-deps -e <controlled_checkout_path>  # code-only, no checkpoints\n"
    ),
}

# Final stop conditions (>=25; here 25).
STOP_CONDITIONS: Tuple[str, ...] = (
    "pre_snapshot_missing",
    "repository_unverified",
    "commit_not_pinned",
    "license_review_missing",
    "dependency_review_missing",
    "network_boundary_missing",
    "command_not_whitelisted",
    "command_scope_changed",
    "unexpected_external_download",
    "model_weight_download_attempted",
    "dataset_download_attempted",
    "example_asset_download_attempted",
    "source_checkout_failure",
    "source_install_failure",
    "dependency_conflict",
    "unexpected_package_overwrite",
    "version_drift",
    "import_side_effect_risk",
    "rollback_unavailable",
    "post_probe_failure",
    "test_board_unwritable",
    "runtime_flag_enabled",
    "inference_flag_enabled",
    "output_adapter_flag_enabled",
    "semantic_promotion_flag_enabled",
)

# Per-asset weight boundary specifics.
WEIGHT_BOUNDARY_SPECIFICS: Dict[str, Dict[str, bool]] = {
    "byte_track": {"tracker_or_detector_weight_boundary_required": True, "checkpoint_weight_boundary_required": False},
    "mobile_sam": {"tracker_or_detector_weight_boundary_required": False, "checkpoint_weight_boundary_required": True},
}

# --------------------------------------------------------------------------- #
# Negative guards (26: Invalid A..Z).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_issuance_as_clone_checkout_install_approval", "go_key": "approval_scope_correct", "depends_on": "approval_scope_correct"},
    {"guard_id": "invalid_b_git_clone_checkout_install_executed", "go_key": "no_clone_checkout_install", "depends_on": "no_clone_checkout_install"},
    {"guard_id": "invalid_c_pip_or_dependency_install_executed", "go_key": "no_pip_dependency_install", "depends_on": "no_pip_dependency_install"},
    {"guard_id": "invalid_d_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_e_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_f_runtime_output_adapter_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_g_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_h_preparation_package_missing", "go_key": "preparation_package_present", "depends_on": "preparation_package_present"},
    {"guard_id": "invalid_i_prepared_asset_scope_not_two_assets", "go_key": "scope_limited_to_deferred", "depends_on": "scope_limited_to_deferred"},
    {"guard_id": "invalid_j_repository_verification_requirement_missing", "go_key": "repo_verification_requirement_present", "depends_on": "repo_verification_requirement_present"},
    {"guard_id": "invalid_k_commit_pin_requirement_missing", "go_key": "commit_pin_requirement_present", "depends_on": "commit_pin_requirement_present"},
    {"guard_id": "invalid_l_license_review_requirement_missing", "go_key": "license_review_requirement_present", "depends_on": "license_review_requirement_present"},
    {"guard_id": "invalid_m_dependency_expansion_review_requirement_missing", "go_key": "dependency_requirement_present", "depends_on": "dependency_requirement_present"},
    {"guard_id": "invalid_n_network_boundary_missing", "go_key": "network_boundary_present", "depends_on": "network_boundary_present"},
    {"guard_id": "invalid_o_command_whitelist_missing", "go_key": "command_whitelist_present", "depends_on": "command_whitelist_present"},
    {"guard_id": "invalid_p_command_whitelist_executed", "go_key": "command_whitelist_not_executed", "depends_on": "command_whitelist_not_executed"},
    {"guard_id": "invalid_q_isolation_requirement_missing", "go_key": "isolation_requirement_present", "depends_on": "isolation_requirement_present"},
    {"guard_id": "invalid_r_rollback_requirement_missing", "go_key": "rollback_requirement_present", "depends_on": "rollback_requirement_present"},
    {"guard_id": "invalid_s_post_install_probe_requirement_missing", "go_key": "post_install_probe_requirement_present", "depends_on": "post_install_probe_requirement_present"},
    {"guard_id": "invalid_t_post_install_probe_real_import_load_inference_runtime", "go_key": "post_install_probe_find_spec_only", "depends_on": "post_install_probe_find_spec_only"},
    {"guard_id": "invalid_u_weight_download_approved_next_execution", "go_key": "weight_not_approved_next_execution", "depends_on": "weight_not_approved_next_execution"},
    {"guard_id": "invalid_v_readiness_allows_inference_runtime_output_semantic", "go_key": "readiness_no_inference_runtime_output_semantic", "depends_on": "readiness_no_inference_runtime_output_semantic"},
    {"guard_id": "invalid_w_dependency_license_review_marked_completed", "go_key": "reviews_not_marked_completed", "depends_on": "reviews_not_marked_completed"},
    {"guard_id": "invalid_x_test_process_or_conclusion_not_in_test_board", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_y_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_z_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (54 phase + 6 test board = 60).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_is_a_compressed_source_install_preparation_and_readiness_review_phase",
    "source_approval_issuance_post_review_is_included",
    "source_install_preparation_is_included",
    "source_install_readiness_review_is_included",
    "approval_issuance_remains_limited_to_source_install_preparation",
    "approval_issuance_is_not_git_clone_approval",
    "approval_issuance_is_not_source_checkout_approval",
    "approval_issuance_is_not_source_install_approval",
    "no_git_clone_is_allowed_in_this_phase",
    "no_source_checkout_is_allowed_in_this_phase",
    "no_source_install_is_allowed_in_this_phase",
    "no_pip_install_is_allowed_in_this_phase",
    "no_dependency_install_is_allowed_in_this_phase",
    "no_model_download_is_allowed_in_this_phase",
    "no_weight_download_is_allowed_in_this_phase",
    "no_dataset_download_is_allowed_in_this_phase",
    "no_real_import_is_allowed_in_this_phase",
    "no_model_load_is_allowed_in_this_phase",
    "no_inference_is_allowed_in_this_phase",
    "runtime_execution_is_not_allowed_in_this_phase",
    "output_adapter_is_not_allowed_in_this_phase",
    "semantic_layer_is_not_allowed_in_this_phase",
    "registry_mutation_is_not_allowed",
    "source_install_preparation_package_is_required",
    "prepared_asset_scope_is_limited_to_byte_track_and_mobile_sam",
    "repository_verification_requirement_is_required",
    "commit_pin_requirement_is_required",
    "license_review_requirement_is_required",
    "dependency_expansion_review_requirement_is_required",
    "network_boundary_is_required",
    "command_whitelist_is_required",
    "command_whitelist_must_not_be_executed_in_this_phase",
    "isolation_requirement_is_required",
    "rollback_requirement_is_required",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_is_not_inference",
    "post_install_probe_is_not_runtime",
    "post_install_probe_is_not_output_adapter",
    "weight_download_is_not_approved_by_default",
    "weight_download_requires_separate_approval",
    "next_source_execution_phase_may_checkout_install_code_only_unless_separate_weight_approval",
    "readiness_review_is_not_source_execution",
    "readiness_review_is_not_inference_approval",
    "readiness_review_is_not_runtime_approval",
    "readiness_review_is_not_output_adapter_approval",
    "readiness_review_is_not_semantic_layer_approval",
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
    "source_approval_scope_audit_record",
    "source_preparation_package_record",
    "source_final_repository_review_requirement_record",
    "source_final_network_boundary_record",
    "source_final_command_whitelist_record",
    "source_final_isolation_requirement_record",
    "source_final_weight_boundary_record",
    "source_readiness_review_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallPreparationReadinessProfile",
    "SourceApprovalIssuanceScopeAudit",
    "SourceInstallPreparationPackage",
    "SourcePreparedAssetScope",
    "SourceRepositoryVerificationRequirement",
    "SourceCommitPinRequirement",
    "SourceNetworkBoundaryRequirement",
    "SourceDependencyExpansionRequirement",
    "SourceLicenseReviewRequirement",
    "SourceIsolationRequirementFinal",
    "SourceCommandWhitelistFinal",
    "SourceStopConditionFinal",
    "SourceRollbackRequirementFinal",
    "SourcePostInstallProbeRequirementFinal",
    "SourceWeightBoundaryFinal",
    "SourceExecutionReadinessReview",
    "SourceExecutionHandoffRecord",
    "NegativeSourceInstallPreparationReadinessGuard",
    "P1ControlledSourceInstallPreparationReadinessDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_PREPARATION_AND_READINESS_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_PREPARATION_AND_READINESS_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "planning_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallPreparationReadinessProfile:
    profile_ref: str
    phase_id: str
    compressed_phase: bool
    source_approval_issuance_post_review_included: bool
    source_install_preparation_included: bool
    source_install_readiness_review_included: bool
    source_install_preparation_package_created: bool
    source_execution_readiness_decision_created: bool
    can_enter_controlled_source_install_execution_next: bool
    git_clone_allowed_in_this_phase: bool
    source_checkout_allowed_in_this_phase: bool
    source_install_allowed_in_this_phase: bool
    pip_install_allowed_in_this_phase: bool
    dependency_install_allowed_in_this_phase: bool
    model_download_allowed_in_this_phase: bool
    weight_download_allowed_in_this_phase: bool
    dataset_download_allowed_in_this_phase: bool
    real_import_allowed_in_this_phase: bool
    model_load_allowed_in_this_phase: bool
    real_inference_allowed_in_this_phase: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_issuance_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceApprovalIssuanceScopeAudit:
    audit_id: str
    upstream_issuance_ref: str
    expected_final_decision: str
    approval_issuance_limited_to_source_install_preparation: bool
    owner_approval_granted_for_source_install_preparation: bool
    owner_approval_granted_for_git_clone: bool
    owner_approval_granted_for_source_checkout: bool
    owner_approval_granted_for_source_install: bool
    owner_approval_granted_for_weight_download: bool
    source_chain_complete: bool
    can_enter_source_install_preparation: bool
    can_enter_source_install: bool
    approval_issuance_success_not_git_clone_approval: bool
    approval_issuance_success_not_source_checkout_approval: bool
    approval_issuance_success_not_source_install_approval: bool
    approval_issuance_success_not_weight_download_approval: bool


@dataclass(frozen=True)
class SourceInstallPreparationPackage:
    preparation_package_id: str
    phase_id: str
    source_approval_issuance_ref: str
    source_request_ref: str
    source_resolution_ref: str
    prepared_assets: Tuple[str, ...]
    repository_verification_required: bool
    commit_pin_required: bool
    license_review_required: bool
    dependency_expansion_review_required: bool
    network_boundary_required: bool
    pre_source_install_snapshot_required: bool
    command_whitelist_required: bool
    isolation_environment_required: bool
    rollback_required: bool
    post_install_probe_required: bool
    test_board_write_required: bool
    weight_download_separate_approval_required: bool
    source_install_preparation_complete: bool
    git_clone_allowed_in_this_phase: bool
    source_install_allowed_in_this_phase: bool


@dataclass(frozen=True)
class SourcePreparedAssetScope:
    asset_id: str
    included_in_source_preparation: bool
    current_status: str
    source_family: str
    repository_requirement_ref: str
    network_boundary_ref: str
    dependency_expansion_ref: str
    license_review_ref: str
    isolation_ref: str
    command_whitelist_ref: str
    rollback_ref: str
    post_install_probe_ref: str
    weight_boundary_ref: str
    can_enter_next_source_execution_phase: bool
    can_enter_weight_download: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_output_adapter: bool
    can_enter_semantic_layer: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationRequirement:
    asset_id: str
    repository_ref_type: str
    repository_url_unverified: bool
    repository_verification_required_before_execution: bool
    repository_commit_pin_required_before_execution: bool
    repository_license_review_required_before_execution: bool
    repository_verification_not_performed_in_this_phase: bool
    source_checkout_allowed_now: bool


@dataclass(frozen=True)
class SourceCommitPinRequirement:
    asset_id: str
    commit_pin_required_before_execution: bool
    commit_pinned_now: bool
    commit_pin_not_performed_in_this_phase: bool


@dataclass(frozen=True)
class SourceNetworkBoundaryRequirement:
    asset_id: str
    network_access_must_be_explicitly_scoped: bool
    git_clone_scope_must_be_whitelisted: bool
    pip_install_scope_must_be_whitelisted: bool
    external_url_download_blocked_by_default: bool
    model_weight_download_blocked_by_default: bool
    dataset_download_blocked_by_default: bool
    example_asset_download_blocked_by_default: bool
    network_log_required: bool
    network_boundary_violation_stops_execution: bool


@dataclass(frozen=True)
class SourceDependencyExpansionRequirement:
    asset_id: str
    dependency_expansion_review_required: bool
    transitive_dependency_review_required: bool
    review_completed: bool
    review_required_and_uncompleted: bool


@dataclass(frozen=True)
class SourceLicenseReviewRequirement:
    asset_id: str
    source_license_review_required: bool
    repository_license_review_required: bool
    transitive_dependency_license_review_required: bool
    review_completed: bool
    review_required_and_uncompleted: bool


@dataclass(frozen=True)
class SourceIsolationRequirementFinal:
    asset_id: str
    separate_source_install_env_required: bool
    no_global_site_packages_preferred: bool
    pre_source_install_snapshot_required: bool
    source_checkout_path_must_be_controlled: bool
    install_target_path_must_be_controlled: bool
    rollback_snapshot_required: bool
    test_board_write_required: bool
    registry_preservation_required: bool
    review_artifact_preservation_required: bool


@dataclass(frozen=True)
class SourceCommandWhitelistFinal:
    asset_id: str
    command_template_ref: str
    command_template_text: str
    template_only_marker: str
    command_not_executed_in_this_phase: bool
    git_clone_command_allowed_now: bool
    source_checkout_command_allowed_now: bool
    pip_install_command_allowed_now: bool
    command_allowed_only_in_next_source_execution_phase: bool
    command_requires_pre_snapshot: bool
    command_requires_repository_verification: bool
    command_requires_commit_pin: bool
    command_requires_license_review: bool
    command_requires_dependency_review: bool
    command_requires_network_boundary: bool
    command_requires_rollback_available: bool
    command_requires_post_probe: bool


@dataclass(frozen=True)
class SourceStopConditionFinal:
    condition_id: str
    condition: str
    stops_execution: bool


@dataclass(frozen=True)
class SourceRollbackRequirementFinal:
    asset_id: str
    rollback_required: bool
    rollback_trigger_conditions_exist: bool
    rollback_template_ref: str
    rollback_command_not_executed_in_this_phase: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool
    rollback_failure_escalation_required: bool


@dataclass(frozen=True)
class SourcePostInstallProbeRequirementFinal:
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
class SourceWeightBoundaryFinal:
    asset_id: str
    weight_download_allowed_in_next_source_execution: bool
    model_download_allowed_in_next_source_execution: bool
    dataset_download_allowed_in_next_source_execution: bool
    source_execution_may_checkout_code_only: bool
    source_execution_may_install_code_only: bool
    source_execution_must_not_download_weights: bool
    source_execution_must_not_download_datasets: bool
    weight_download_requires_separate_approval: bool
    no_weight_download_phase_until_source_install_post_review: bool
    tracker_or_detector_weight_boundary_required: bool
    checkpoint_weight_boundary_required: bool


@dataclass(frozen=True)
class SourceExecutionReadinessReview:
    review_id: str
    approval_scope_valid: bool
    source_preparation_package_complete: bool
    prepared_assets_verified: bool
    repository_requirements_ready: bool
    network_boundary_ready: bool
    dependency_review_required_and_uncompleted: bool
    license_review_required_and_uncompleted: bool
    command_whitelist_ready: bool
    isolation_requirement_ready: bool
    stop_conditions_ready: bool
    rollback_ready: bool
    post_install_probe_ready: bool
    weight_download_scope_not_approved: bool
    test_board_ready: bool
    non_execution_boundary_preserved: bool
    can_enter_controlled_source_install_execution_next: bool
    can_enter_weight_download_execution_next: bool
    can_enter_inference: bool
    can_enter_runtime: bool
    can_enter_output_adapter: bool
    can_enter_semantic_layer: bool


@dataclass(frozen=True)
class SourceExecutionHandoffRecord:
    handoff_id: str
    next_phase_ref: str
    can_enter_controlled_source_install_execution_next: bool
    first_source_execution_scope: str
    weight_download_still_blocked: bool
    inference_still_blocked: bool


@dataclass
class NegativeSourceInstallPreparationReadinessGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallPreparationReadinessDecision:
    decision_ref: str
    source_install_preparation_readiness_profile_count: int
    source_approval_issuance_scope_audit_count: int
    source_install_preparation_package_count: int
    source_prepared_asset_scope_count: int
    source_repository_verification_requirement_count: int
    source_commit_pin_requirement_count: int
    source_network_boundary_requirement_count: int
    source_dependency_expansion_requirement_count: int
    source_license_review_requirement_count: int
    source_isolation_requirement_final_count: int
    source_command_whitelist_final_count: int
    source_stop_condition_final_count: int
    source_rollback_requirement_final_count: int
    source_post_install_probe_requirement_final_count: int
    source_weight_boundary_final_count: int
    source_execution_readiness_review_count: int
    source_execution_handoff_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
