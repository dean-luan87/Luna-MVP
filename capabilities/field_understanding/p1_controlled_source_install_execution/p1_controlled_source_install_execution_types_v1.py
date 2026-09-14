# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution — types v1 (FIRST REAL SOURCE EXECUTION).

This is the first REAL controlled source install execution for byte_track and
mobile_sam. The ONLY allowed real actions are: repository verification, commit
pin, scoped git clone / source checkout, code-only source install, post-install
find_spec probe, and test board write. Strictly forbidden: weight download, model
download, dataset download, example asset download, real import, model load,
inference, runtime, runtime activation, output adapter, semantic layer, registry
mutation, unscoped network access, external URL download.

Honest partial success is allowed (allowed_partial_success=true,
full_go_required=false). Any failed/deferred asset must stop its OWN downstream
steps; it must not stop the other asset unless the shared env is polluted, pip
state is corrupted, rollback is unavailable, or a network-boundary violation
indicates global risk.

GOVERNANCE REALITY (decisive): every upstream phase (resolution/request/approval/
preparation) deliberately left BOTH repositories as UNVERIFIED PLACEHOLDERS —
repository_url_unverified=true, repository_commit_not_pinned=true,
repository_license_not_verified=true, network_lookup_performed=false; byte_track's
registry identity is "source_component_or_unresolved_package". Therefore, per the
phase rule "repo/commit/license/dependency unclear => DEFER, do NOT force
clone/install", repository verification cannot honestly pass on a placeholder.
The conservative, honest outcome is to DEFER at the repository-verification gate
(no clone, no checkout, no install, no network access, no boundary violation)
rather than fabricate a repository URL. This yields an honest partial outcome
with zero boundary violations; nothing is forced. Protected, non-deletable test
board records are written in real_test mode.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Execution-v1-001"
SCOPE = "p1_controlled_source_install_execution"
SOURCE_CHAIN = "p1_controlled_source_install_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "byte_track 与 mobile_sam 的第一次真实 controlled source install execution。允许的真实动作仅限：repository "
    "verification、commit pin、scoped git clone / source checkout、code-only source install、post-install find_spec "
    "probe、test board 写入。禁止：weight/model/dataset/example 资产下载、外部 URL 下载、未授权网络访问、真实 import、"
    "model load、inference、runtime、runtime activation、output adapter、语义层、registry mutation。允许诚实的 partial "
    "success（allowed_partial_success=true, full_go_required=false）；任一资产失败只停止其自身后续步骤，不得波及另一资产，"
    "除非共享 env 污染 / pip state 损坏 / rollback 不可用 / 网络边界违规带来全局风险。治理事实：上游各阶段刻意将两个仓库"
    "都标为未验证 placeholder（repository_url_unverified=true、commit_not_pinned=true、license_not_verified=true、"
    "network_lookup_performed=false；byte_track 身份为 source_component_or_unresolved_package）。因此按本阶段规则"
    "“repo/commit/license/dependency 不清楚 → 资产 deferred，不强行 clone/install”，repository verification 在 "
    "placeholder 上无法诚实通过；保守且诚实的结果是在 repository-verification gate 处 DEFER（不 clone、不 checkout、"
    "不 install、不联网、无边界违规），而非凭空编造仓库 URL。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_install_execution_is_code_only_no_weight_download_no_inference_no_runtime_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
CONTROLLED_SOURCE_INSTALL_EXECUTION = True
ALLOWED_PARTIAL_SUCCESS = True
FULL_GO_REQUIRED = False
ANY_FAILED_EXECUTION_MUST_STOP_DOWNSTREAM_FOR_THAT_ASSET = True
SOURCE_EXECUTION_SCOPE = "code_only"

# Forbidden execution flags (all False).
REGISTRY_MUTATION_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
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
UNSCOPED_NETWORK_ACCESS_ALLOWED = False
EXTERNAL_URL_DOWNLOAD_ALLOWED = False

# Allowed actions (real, bounded).
REPO_VERIFICATION_ALLOWED = True
COMMIT_PIN_ALLOWED = True
SCOPED_GIT_CLONE_ALLOWED = True
SOURCE_CHECKOUT_ALLOWED = True
CODE_ONLY_SOURCE_INSTALL_ALLOWED = True
POST_INSTALL_FIND_SPEC_PROBE_ALLOWED = True
TEST_BOARD_WRITE_ALLOWED = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PREP_READINESS_REF = "Phase-P1-Controlled-Source-Install-Preparation-And-Readiness-Review-v1-001"
UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Source-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Source-Install-Request-Planning-v1-001"
UPSTREAM_RESOLUTION_REF = "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001"
UPSTREAM_REGISTRY_CORRECTION_REF = "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001"
UPSTREAM_PACKAGE_RESOLUTION_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

NEXT_STEP_REF = "Phase-P1-Controlled-Source-Install-Execution-Post-Review-v1-001"

TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

CONTROLLED_VENV_DIRNAME = "controlled_source_env"
TARGET_ENV_LABEL = "controlled_source_install_env_workspace_local_v1"
SOURCE_CHECKOUT_DIRNAME = "source_checkout"

# --------------------------------------------------------------------------- #
# Execution scope (only the two deferred assets).
# --------------------------------------------------------------------------- #
EXECUTION_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
EXECUTION_ORDER: Tuple[Tuple[str, int], ...] = (("byte_track", 1), ("mobile_sam", 2))

EXCLUDED_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

# Per-asset source-execution input. Repository refs are PLACEHOLDERS carried from
# upstream resolution planning (deliberately unverified). find_spec probe import
# candidates are recorded but NOT imported.
SOURCE_EXECUTION_INPUT: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "source_family": "ByteTrack_YOLOX",
        "repository_ref_type": "placeholder",
        "repository_url_unverified": True,
        "repository_commit_not_pinned": True,
        "repository_license_not_verified": True,
        "registry_correction_recommendation": "source_component_or_unresolved_package",
        "probe_import_candidates": ("yolox", "bytetrack"),
        "command_template_ref": "source_command_whitelist_template::byte_track",
        "defer_reason": (
            "repository_ref_is_unverified_placeholder_and_registry_identity_is_"
            "source_component_or_unresolved_package_repo_commit_license_dependency_unclear"
        ),
    },
    "mobile_sam": {
        "source_family": "MobileSAM",
        "repository_ref_type": "placeholder",
        "repository_url_unverified": True,
        "repository_commit_not_pinned": True,
        "repository_license_not_verified": True,
        "registry_correction_recommendation": "source_install_method_binding",
        "probe_import_candidates": ("mobile_sam",),
        "command_template_ref": "source_command_whitelist_template::mobile_sam",
        "defer_reason": (
            "repository_ref_is_unverified_placeholder_repo_commit_license_unclear_and_"
            "canonical_repo_ships_committed_checkpoint_weight_so_full_clone_would_be_weight_download"
        ),
    },
}

# --------------------------------------------------------------------------- #
# Stop conditions (29).
# --------------------------------------------------------------------------- #
EXECUTION_STOP_CONDITIONS: Tuple[str, ...] = (
    "pre_snapshot_missing",
    "repository_ref_missing",
    "repository_verification_failed",
    "commit_pin_failed",
    "license_presence_unrecorded",
    "network_boundary_missing",
    "command_not_whitelisted",
    "command_scope_changed",
    "unexpected_external_download",
    "model_weight_download_attempted",
    "checkpoint_download_attempted",
    "dataset_download_attempted",
    "example_asset_download_attempted",
    "git_submodule_unapproved",
    "source_checkout_failure",
    "source_install_failure",
    "dependency_conflict",
    "package_overwrite_detected",
    "global_env_write_detected",
    "registry_write_detected",
    "test_board_write_failure",
    "rollback_unavailable",
    "post_probe_failure",
    "real_import_attempted",
    "model_load_attempted",
    "inference_attempted",
    "runtime_flag_enabled",
    "output_adapter_flag_enabled",
    "semantic_promotion_flag_enabled",
)

# Flags that must remain False throughout execution.
EXECUTION_CONTROL_FLAGS_FALSE: Dict[str, bool] = {
    "weight_download_performed": False,
    "model_download_performed": False,
    "dataset_download_performed": False,
    "example_asset_download_performed": False,
    "unauthorized_external_download_performed": False,
    "real_import_performed": False,
    "model_load_performed": False,
    "real_inference_performed": False,
    "runtime_execution_performed": False,
    "runtime_activation_performed": False,
    "real_output_adapter_performed": False,
    "semantic_promotion_performed": False,
    "registry_write_performed": False,
    "global_env_write_performed": False,
}

CAN_ENTER_FLAGS: Dict[str, bool] = {
    "can_enter_post_review_next": True,
    "can_enter_weight_download_execution_next": False,
    "can_enter_inference": False,
    "can_enter_runtime": False,
    "can_enter_output_adapter": False,
    "can_enter_semantic_layer": False,
}

# --------------------------------------------------------------------------- #
# Negative guards (22: Invalid A..V).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_executed_without_pre_snapshot", "go_key": "snapshot_before_execution_enforced", "depends_on": "snapshot_before_execution_enforced"},
    {"guard_id": "invalid_b_non_scope_asset_executed", "go_key": "scope_only_two_assets", "depends_on": "scope_only_two_assets"},
    {"guard_id": "invalid_c_checkout_without_repository_verification", "go_key": "verification_before_checkout_enforced", "depends_on": "verification_before_checkout_enforced"},
    {"guard_id": "invalid_d_checkout_install_without_commit_pin", "go_key": "commit_pin_before_checkout_enforced", "depends_on": "commit_pin_before_checkout_enforced"},
    {"guard_id": "invalid_e_network_boundary_or_log_missing", "go_key": "network_boundary_and_log_present", "depends_on": "network_boundary_and_log_present"},
    {"guard_id": "invalid_f_non_whitelisted_command_executed", "go_key": "only_whitelisted_commands", "depends_on": "only_whitelisted_commands"},
    {"guard_id": "invalid_g_unauthorized_external_download", "go_key": "no_unauthorized_download", "depends_on": "no_unauthorized_download"},
    {"guard_id": "invalid_h_weight_model_dataset_example_download", "go_key": "no_weight_model_dataset_download", "depends_on": "no_weight_model_dataset_download"},
    {"guard_id": "invalid_i_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_j_runtime_output_semantic_triggered", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_k_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_l_checkout_to_uncontrolled_path", "go_key": "checkout_path_controlled", "depends_on": "checkout_path_controlled"},
    {"guard_id": "invalid_m_install_to_global_env_unapproved", "go_key": "install_not_global", "depends_on": "install_not_global"},
    {"guard_id": "invalid_n_probe_not_find_spec_only", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_o_install_success_marked_weight_readiness", "go_key": "success_not_weight_readiness", "depends_on": "success_not_weight_readiness"},
    {"guard_id": "invalid_p_install_success_marked_inference_runtime_readiness", "go_key": "success_not_inference_runtime_readiness", "depends_on": "success_not_inference_runtime_readiness"},
    {"guard_id": "invalid_q_partial_faked_as_full_go", "go_key": "partial_not_full_go", "depends_on": "partial_not_full_go"},
    {"guard_id": "invalid_r_test_board_real_test_record_missing", "go_key": "test_board_real_test_present", "depends_on": "test_board_real_test_present"},
    {"guard_id": "invalid_s_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_t_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
    {"guard_id": "invalid_u_rollback_readiness_missing", "go_key": "rollback_readiness_present", "depends_on": "rollback_readiness_present"},
    {"guard_id": "invalid_v_source_execution_enters_weight_download_phase", "go_key": "not_enter_weight_download", "depends_on": "not_enter_weight_download"},
)

# --------------------------------------------------------------------------- #
# Governance rules (36 phase + 6 test board = 42).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_source_install_execution",
    "only_byte_track_and_mobile_sam_are_in_scope",
    "repo_verification_is_required_before_checkout",
    "commit_pin_is_required_before_checkout_install",
    "network_boundary_is_required",
    "network_log_is_required",
    "source_checkout_path_must_be_controlled",
    "source_install_target_path_must_be_controlled",
    "only_whitelisted_commands_may_execute",
    "code_only_source_install_is_allowed",
    "weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "post_install_probe_must_use_find_spec_only",
    "source_install_success_is_not_weight_readiness",
    "source_install_success_is_not_inference_approval",
    "source_install_success_is_not_runtime_approval",
    "source_install_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "honest_partial_success_is_allowed",
    "partial_success_must_not_be_promoted_to_full_go",
    "rollback_readiness_is_required",
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
    "source_pre_execution_snapshot_record",
    "source_repository_verification_record",
    "source_checkout_execution_record",
    "source_code_install_execution_record",
    "source_post_install_probe_record",
    "source_network_log_record",
    "source_stop_condition_record",
    "source_rollback_readiness_record",
    "source_partial_success_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallExecutionProfile",
    "SourceExecutionPreSnapshotRecord",
    "SourceRepositoryVerificationExecutionRecord",
    "SourceCommitPinExecutionRecord",
    "SourceCheckoutExecutionRecord",
    "SourceCodeInstallExecutionRecord",
    "SourceNetworkAccessLogRecord",
    "SourceExecutionStepResult",
    "SourcePostInstallFindSpecProbeRecord",
    "SourceExecutionStopConditionRecord",
    "SourceExecutionFailureRecord",
    "SourceRollbackReadinessRecord",
    "SourceExecutionPartialSuccessRecord",
    "SourceExecutionSummaryRecord",
    "SourceExecutionPermissionBoundary",
    "NegativeControlledSourceInstallExecutionGuard",
    "P1ControlledSourceInstallExecutionDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_CODE_ONLY_GO"
FINAL_DECISION_PARTIAL_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_CODE_ONLY_PARTIAL_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_used": True,
    "controlled_venv_pattern_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    controlled_source_install_execution: bool
    source_execution_scope: str
    allowed_partial_success: bool
    full_go_required: bool
    repo_verification_allowed: bool
    commit_pin_allowed: bool
    scoped_git_clone_allowed: bool
    source_checkout_allowed: bool
    code_only_source_install_allowed: bool
    post_install_find_spec_probe_allowed: bool
    test_board_write_allowed: bool
    unscoped_network_access_allowed: bool
    external_url_download_allowed: bool
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    example_asset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    controlled_venv_label: str
    execution_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    upstream_prep_readiness_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceExecutionPreSnapshotRecord:
    snapshot_ref: str
    python_version: str
    executable_path: str
    pip_version: str
    pip_freeze_before_count: int
    installed_package_list_before_count: int
    working_directory: str
    source_execution_env_path: str
    source_checkout_root: str
    source_install_target_path: str
    network_policy_ref: str
    command_whitelist_ref: str
    rollback_snapshot_ref: str
    timestamp: str
    upstream_readiness_ref: str
    test_board_ref: str
    snapshot_performed: bool
    snapshot_written_before_execution: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool
    all_required_fields_present: bool


@dataclass(frozen=True)
class SourceRepositoryVerificationExecutionRecord:
    asset_id: str
    repository_ref_type: str
    repository_url_recorded: bool
    repository_url_value: str
    repository_remote_ref_recorded: bool
    target_branch_or_tag_recorded: bool
    resolved_commit_hash_recorded: bool
    repository_license_presence_recorded: bool
    repository_verification_performed: bool
    repository_verification_result: str
    repository_verification_failure_blocks_asset_execution: bool
    network_lookup_performed: bool


@dataclass(frozen=True)
class SourceCommitPinExecutionRecord:
    asset_id: str
    commit_pin_required: bool
    commit_pin_recorded: bool
    resolved_commit_hash: str
    commit_pin_result: str
    commit_pin_failure_blocks_asset_execution: bool


@dataclass(frozen=True)
class SourceCheckoutExecutionRecord:
    asset_id: str
    source_checkout_root: str
    asset_checkout_path: str
    checkout_path_is_controlled: bool
    checkout_writes_global_path: bool
    checkout_overwrites_registry: bool
    checkout_overwrites_test_board: bool
    checkout_overwrites_package_venv: bool
    checkout_attempted: bool
    checkout_status: str
    checkout_succeeded: bool


@dataclass(frozen=True)
class SourceCodeInstallExecutionRecord:
    asset_id: str
    install_target_path: str
    install_target_is_controlled: bool
    code_only_install: bool
    weight_download_in_command: bool
    dataset_download_in_command: bool
    example_asset_download_in_command: bool
    installed_package_name: str
    installed_version: str
    editable_path: str
    source_commit: str
    install_attempted: bool
    install_status: str
    install_succeeded: bool


@dataclass(frozen=True)
class SourceNetworkAccessLogRecord:
    asset_id: str
    network_boundary_defined: bool
    allowed_network_target: str
    actual_network_target: str
    command_ref: str
    network_access_performed: bool
    violation_detected: bool
    violation_reason: str


@dataclass(frozen=True)
class SourcePostInstallFindSpecProbeRecord:
    asset_id: str
    probe_import_candidates: Tuple[str, ...]
    probe_performed: bool
    probe_uses_find_spec_only: bool
    real_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool
    output_adapter_used: bool
    find_spec_found: bool
    probe_result: str
    probe_recorded: bool


@dataclass(frozen=True)
class SourceExecutionStepResult:
    asset_id: str
    order_index: int
    pre_step_stop_condition_check_passed: bool
    repository_verification_ref: str
    commit_pin_ref: str
    checkout_ref: str
    code_install_ref: str
    probe_ref: str
    network_log_ref: str
    step_status: str
    step_succeeded: bool
    downstream_skipped_for_this_asset: bool
    affected_other_asset: bool


@dataclass(frozen=True)
class SourceExecutionStopConditionRecord:
    condition_id: str
    enforced: bool
    triggered: bool


@dataclass(frozen=True)
class SourceExecutionFailureRecord:
    asset_id: str
    failure_kind: str
    downstream_steps_skipped_for_this_asset: bool
    other_asset_affected: bool
    failure_record_written: bool
    rollback_readiness_record_written: bool
    blocks_go_unless_partial: bool


@dataclass(frozen=True)
class SourceRollbackReadinessRecord:
    asset_id: str
    rollback_available: bool
    rollback_not_executed_by_default: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class SourceExecutionPartialSuccessRecord:
    record_ref: str
    allowed_partial_success: bool
    full_go_required: bool
    attempted_source_asset_count: int
    successful_source_asset_count: int
    failed_source_asset_count: int
    deferred_source_asset_count: int
    partial_go_not_full_go: bool
    source_install_success_not_weight_readiness: bool
    source_install_success_not_inference_approval: bool
    source_install_success_not_runtime_approval: bool
    all_assets_deferred: bool


@dataclass(frozen=True)
class SourceExecutionSummaryRecord:
    summary_ref: str
    attempted_source_asset_count: int
    successful_source_asset_count: int
    failed_source_asset_count: int
    deferred_source_asset_count: int
    repository_verification_count: int
    commit_pin_count: int
    checkout_count: int
    code_install_count: int
    post_install_probe_count: int
    network_access_performed_count: int
    boundary_violation_count: int
    global_env_pollution_detected: bool
    weight_download_performed: bool
    model_download_performed: bool
    dataset_download_performed: bool
    real_import_performed: bool
    runtime_execution_performed: bool


@dataclass(frozen=True)
class SourceExecutionPermissionBoundary:
    boundary_ref: str
    real_execution_phase: bool
    controlled_source_install_execution: bool
    source_execution_scope: str
    weight_download_allowed: bool
    model_download_allowed: bool
    dataset_download_allowed: bool
    example_asset_download_allowed: bool
    real_import_allowed: bool
    model_load_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    registry_mutation_allowed: bool
    commercial_runtime_approved: bool
    source_install_success_not_weight_readiness: bool
    source_install_success_not_inference_approval: bool
    source_install_success_not_runtime_approval: bool
    source_install_success_not_output_adapter_approval: bool


@dataclass
class NegativeControlledSourceInstallExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionDecision:
    decision_ref: str
    controlled_source_install_execution_profile_count: int
    source_execution_pre_snapshot_record_count: int
    source_repository_verification_execution_record_count: int
    source_commit_pin_execution_record_count: int
    source_checkout_execution_record_count: int
    source_code_install_execution_record_count: int
    source_network_access_log_record_count: int
    source_post_install_find_spec_probe_record_count: int
    source_execution_step_result_count: int
    source_rollback_readiness_record_count: int
    source_execution_summary_record_count: int
    source_execution_partial_success_record_count: int
    attempted_source_asset_count: int
    successful_source_asset_count: int
    failed_source_asset_count: int
    deferred_source_asset_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
