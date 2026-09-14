# -*- coding: utf-8 -*-
"""P1 Controlled Source Install Execution Retry And Post-Review — types v1
(REAL EXECUTION + INLINE POST-REVIEW).

Second controlled source-install execution for byte_track and mobile_sam, with the
post-review merged into the same phase. Allowed actions: pre-execution snapshot,
scoped source checkout, commit pin validation, code-only source install,
post-install find_spec probe, and execution post-review. STRICTLY forbidden: weight
/ model / checkpoint / dataset / example-asset download, real import, model load,
inference, runtime, output adapter, semantic layer and registry mutation. mobile_sam
MUST NOT be full-cloned; it must use a weight-excluding checkout that excludes
weights/mobile_sam.pt and every weight/checkpoint extension. Honest partial success
(including all_deferred_no_violation) is allowed; partial success must never be
promoted to full GO; and code-only install success is NOT weight / inference /
runtime / model readiness. Protected, non-deletable test board records are written
in real_test mode.

The embedded EXECUTION_EVIDENCE_* constants below are the REAL results captured
during this phase: a pre-snapshot, two scoped checkouts at the pinned commits
(mobile_sam via partial-clone + sparse-checkout excluding weights, so the ~40MB
committed checkpoint was NEVER fetched), and two code-only `pip install --no-index
--no-deps --no-build-isolation --target <controlled>` installs (no PyPI download, no
global pollution), followed by find_spec-only probes.
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

PHASE_ID = "Phase-P1-Controlled-Source-Install-Execution-Retry-And-Post-Review-v1-001"
SCOPE = "p1_controlled_source_install_execution_retry_and_post_review"
SOURCE_CHAIN = "p1_controlled_source_install_execution_retry_and_post_review_v1"

RETRY_PRINCIPLE_ZH = (
    "byte_track 与 mobile_sam 的第二次受控源码安装执行 + 同阶段 post-review。允许 pre-snapshot、scoped source checkout、"
    "commit pin 校验、code-only source install、find_spec 探针与执行后复核。禁止下载权重/模型/checkpoint/数据集/示例资产，"
    "禁止真实 import、model load、inference、runtime、output adapter、语义层、registry mutation。mobile_sam 禁止 full clone，"
    "必须排除权重的 checkout（排除 weights/mobile_sam.pt 与全部权重后缀），宁可 deferred 也不 full clone。byte_track 若 C++ "
    "扩展编译失败诚实 failed/deferred，不得改成 success。允许诚实 partial success；partial 不得伪造成 full GO；code-only "
    "安装成功不代表权重/推理/runtime/模型就绪。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "source_install_retry_is_code_only_no_weight_download_no_full_clone_no_import_no_inference_no_runtime_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
SOURCE_EXECUTION_RETRY = True
POST_REVIEW_INCLUDED = True
CONTROLLED_SOURCE_INSTALL_EXECUTION = True
ALLOWED_PARTIAL_SUCCESS = True
FULL_GO_REQUIRED = False
SOURCE_EXECUTION_SCOPE = "code_only"

REGISTRY_MUTATION_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
CHECKPOINT_DOWNLOAD_ALLOWED = False
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

# Allowed actions.
PRE_SOURCE_EXECUTION_SNAPSHOT_ALLOWED = True
SCOPED_SOURCE_CHECKOUT_ALLOWED = True
COMMIT_PIN_VALIDATION_ALLOWED = True
CODE_ONLY_SOURCE_INSTALL_ALLOWED = True
POST_INSTALL_FIND_SPEC_PROBE_ALLOWED = True
EXECUTION_POST_REVIEW_ALLOWED = True
TEST_BOARD_WRITE_ALLOWED = True

# Forbidden actions.
FULL_CLONE_FOR_MOBILE_SAM_ALLOWED = False
UNSCOPED_NETWORK_ACCESS_ALLOWED = False
EXTERNAL_URL_DOWNLOAD_ALLOWED = False

WEIGHT_DOWNLOAD_REQUIRES_SEPARATE_APPROVAL = True
NO_WEIGHT_DOWNLOAD_PHASE_UNTIL_CODE_ONLY_INSTALL_REGISTRY_READINESS_COMPLETE = True
NO_INFERENCE_PHASE_UNTIL_WEIGHT_DOWNLOAD_POST_REVIEW = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_REVIEW_REF = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Review-v1-001"
UPSTREAM_REVIEW_EXPECTED_GO = "P1_SOURCE_REPOSITORY_VERIFICATION_COMMITPIN_LICENSE_DEPENDENCY_WEIGHT_EXCLUSION_REVIEW_GO"
UPSTREAM_PLANNING_REF = "Phase-P1-Source-Repository-Verification-CommitPin-License-Dependency-And-WeightExclusion-Planning-v1-001"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Follow-up routing targets.
NEXT_PHASE_REGISTRY_PATCH = "Phase-P1-Source-Code-Only-Install-Registry-Patch-And-Readiness-Planning-v1-001"
NEXT_PHASE_FOLLOWUP_PLANNING = "Phase-P1-Controlled-Source-Install-Execution-Retry-Post-Review-Followup-Planning-v1-001"
NEXT_PHASE_BLOCKER_REVIEW = "Phase-P1-Controlled-Source-Install-Execution-Retry-Blocker-Review-v1-001"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Scope.
# --------------------------------------------------------------------------- #
IN_SCOPE_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
SOURCE_FAMILY: Dict[str, str] = {"byte_track": "ByteTrack_YOLOX", "mobile_sam": "MobileSAM"}
MUST_NOT_PROCESS_ASSET_IDS: Tuple[str, ...] = (
    "supervision", "deep_sort", "midas",
    "fast_sam", "yolov8n", "pyannote", "sam2", "depth_anything", "zoe_depth",
    "grounding_dino", "scene_relation_vlm", "open_vocab_vlm", "sense_voice",
    "emotion_multimodal_bridge", "rt_detr",
)

BLOCKED_WEIGHT_PATTERNS: Tuple[str, ...] = (
    "weights/mobile_sam.pt", "*.pth", "*.pt", "*.ckpt", "*.safetensors", "*.onnx", "*.bin", "*.h5", "*.pb",
)

# Locked upstream evidence (must not be re-invented).
LOCKED_UPSTREAM_EVIDENCE: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "repository_url": "https://github.com/FoundationVision/ByteTrack",
        "commit_hash": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "license": "MIT",
        "default_branch": "main",
        "import_root_candidate": "yolox",
        "source_family": "ByteTrack_YOLOX",
        "build_compile_risk_high": True,
        "cpp_extension_risk": True,
        "onnx_version_conflict_risk": True,
        "committed_weight_risk": False,
    },
    "mobile_sam": {
        "repository_url": "https://github.com/ChaoningZhang/MobileSAM",
        "commit_hash": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "license": "Apache-2.0",
        "default_branch": "master",
        "import_root_candidate": "mobile_sam",
        "source_family": "MobileSAM",
        "committed_weight_file": "weights/mobile_sam.pt",
        "committed_weight_file_size_bytes": 40728226,
        "full_clone_allowed": False,
        "weight_excluding_checkout_required": True,
    },
}

# --------------------------------------------------------------------------- #
# Embedded REAL execution evidence captured during this phase.
# --------------------------------------------------------------------------- #
EXECUTION_EVIDENCE_SNAPSHOT: Dict[str, Any] = {
    "python_version": "3.9.6",
    "executable_path": "/usr/bin/python3",
    "pip_version": "25.2",
    "installed_package_count_before": 392,
    "installed_package_count_after": 392,
    "global_env_diff_empty": True,
    "working_directory": "_tmp_eval_out/p1_source_retry_workspace",
    "source_checkout_root": "_tmp_eval_out/p1_source_retry_workspace/checkout",
    "source_install_target_path": "_tmp_eval_out/p1_source_retry_workspace/install_target",
    "network_policy_ref": "scoped_github_readonly_checkout_only_no_weight_download",
    "command_whitelist_ref": "git_clone_filter_blob_none+git_sparse_checkout+git_checkout_pinned_commit+pip_install_no_index_no_deps_no_build_isolation_target+importlib_find_spec",
    "rollback_snapshot_ref": "snapshot_pip_freeze_before.txt",
    "snapshot_performed": True,
    "snapshot_written_before_execution": True,
}

# Per-asset checkout command whitelist (only these command shapes were executed).
COMMAND_WHITELIST: Tuple[str, ...] = (
    "git clone --filter=blob:none --no-checkout [--depth 1] <verified_repo_url> <controlled_path>",
    "git sparse-checkout init --no-cone",
    "git checkout <pinned_commit_or_default_branch>",
    "git rev-parse HEAD",
    "pip install --no-index --no-deps --no-build-isolation --target <controlled_target> <controlled_checkout_path>",
    "python -c importlib.util.find_spec(<candidate>)  # find_spec only, no import",
)

EXECUTION_EVIDENCE_ASSET: Dict[str, Dict[str, Any]] = {
    "byte_track": {
        "checkout_strategy": "scoped_partial_clone_then_checkout_pinned_commit",
        "full_clone_used": False,
        "weight_excluding_checkout_used": False,
        "checkout_path": "_tmp_eval_out/p1_source_retry_workspace/checkout/byte_track_src",
        "resolved_commit_hash": "d1bf0191adff59bc8fcfeaa0b33d3d1642552a99",
        "commit_pin_matches_locked_evidence": True,
        "checkout_succeeded": True,
        "weight_files_materialized": (),
        "code_install_command": "pip install --no-index --no-deps --no-build-isolation --target install_target/byte_track checkout/byte_track_src",
        "code_install_return_code": 0,
        "code_install_succeeded": True,
        "built_artifact": "yolox-0.1.0-cp39-cp39-macosx_10_9_universal2.whl",
        "cpp_extension_compiled": True,
        "installed_into_controlled_target_only": True,
        "global_env_polluted": False,
        "dependency_download_performed": False,
        "weight_download_performed": False,
        "install_stdout_summary": "Building wheel for yolox (setup.py): finished done; Successfully built yolox; Successfully installed yolox-0.1.0",
        "install_stderr_summary": "legacy setup.py bdist_wheel DEPRECATION notice only (non-fatal)",
        "probe_candidates": ("yolox", "bytetrack", "byte_track"),
        "find_spec_results": {"yolox": True, "bytetrack": False, "byte_track": False},
        "real_import_used": False,
        "execution_status": "SUCCESS",
        "defer_or_fail_reason": None,
    },
    "mobile_sam": {
        "checkout_strategy": "weight_excluding_partial_clone_sparse_checkout_exclude_weights",
        "full_clone_used": False,
        "weight_excluding_checkout_used": True,
        "checkout_path": "_tmp_eval_out/p1_source_retry_workspace/checkout/mobile_sam_src",
        "resolved_commit_hash": "f706ad9c4eb7f219c00d9050e46328518ffb65d2",
        "commit_pin_matches_locked_evidence": True,
        "checkout_succeeded": True,
        "weight_files_materialized": (),
        "committed_weight_file_excluded": "weights/mobile_sam.pt",
        "committed_weight_blob_fetched": False,
        "git_lfs_triggered": False,
        "code_install_command": "pip install --no-index --no-deps --no-build-isolation --target install_target/mobile_sam checkout/mobile_sam_src",
        "code_install_return_code": 0,
        "code_install_succeeded": True,
        "built_artifact": "mobile_sam-1.0-py3-none-any.whl",
        "cpp_extension_compiled": False,
        "installed_into_controlled_target_only": True,
        "global_env_polluted": False,
        "dependency_download_performed": False,
        "weight_download_performed": False,
        "install_stdout_summary": "Created wheel for mobile-sam (pure python); Successfully installed mobile-sam-1.0",
        "install_stderr_summary": "none",
        "probe_candidates": ("mobile_sam",),
        "find_spec_results": {"mobile_sam": True},
        "real_import_used": False,
        "execution_status": "SUCCESS",
        "defer_or_fail_reason": None,
    },
}

EXECUTION_EVIDENCE_NETWORK: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "mobile_sam",
        "allowed_target": "github.com (scoped readonly source checkout)",
        "actual_target": "https://github.com/ChaoningZhang/MobileSAM (partial clone, blob:none, sparse exclude weights/)",
        "command_ref": "git clone --filter=blob:none --no-checkout + sparse-checkout + git checkout",
        "purpose": "weight_excluding_source_checkout",
        "network_boundary_compliant": True,
        "violation_detected": False,
        "violation_reason": None,
    },
    {
        "asset_id": "byte_track",
        "allowed_target": "github.com (scoped readonly source checkout)",
        "actual_target": "https://github.com/FoundationVision/ByteTrack (partial clone, blob:none, checkout pinned commit)",
        "command_ref": "git clone --filter=blob:none --no-checkout + git checkout d1bf0191",
        "purpose": "scoped_source_checkout_pinned_commit",
        "network_boundary_compliant": True,
        "violation_detected": False,
        "violation_reason": None,
    },
    {
        "asset_id": "both",
        "allowed_target": "no package index / no external URL",
        "actual_target": "pip install --no-index (local checkout path only, no PyPI, no weight/model/dataset/example download)",
        "command_ref": "pip install --no-index --no-deps --no-build-isolation --target",
        "purpose": "code_only_install_no_download",
        "network_boundary_compliant": True,
        "violation_detected": False,
        "violation_reason": None,
    },
)

# Derived execution summary (honest).
ATTEMPTED_SOURCE_ASSET_COUNT = 2
SUCCESSFUL_SOURCE_ASSET_COUNT = 2
FAILED_OR_DEFERRED_SOURCE_ASSET_COUNT = 0
PARTIAL_GO_SUBTYPES: Tuple[str, ...] = ("partial_success", "all_deferred_no_violation")

# --------------------------------------------------------------------------- #
# Negative guards (23: Invalid A..W).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_no_pre_snapshot_before_execution", "go_key": "snapshot_present", "depends_on": "snapshot_present"},
    {"guard_id": "invalid_b_scope_includes_non_target_asset", "go_key": "scope_only_two", "depends_on": "scope_only_two"},
    {"guard_id": "invalid_c_unverified_url_or_unpinned_commit_checkout", "go_key": "checkout_pinned_verified", "depends_on": "checkout_pinned_verified"},
    {"guard_id": "invalid_d_mobile_sam_full_clone", "go_key": "mobile_sam_no_full_clone", "depends_on": "mobile_sam_no_full_clone"},
    {"guard_id": "invalid_e_mobile_sam_weight_file_downloaded", "go_key": "mobile_sam_weight_excluded", "depends_on": "mobile_sam_weight_excluded"},
    {"guard_id": "invalid_f_model_weight_checkpoint_dataset_example_download", "go_key": "no_asset_download", "depends_on": "no_asset_download"},
    {"guard_id": "invalid_g_non_whitelisted_command_executed", "go_key": "only_whitelisted_commands", "depends_on": "only_whitelisted_commands"},
    {"guard_id": "invalid_h_unauthorized_network_access", "go_key": "network_boundary_compliant", "depends_on": "network_boundary_compliant"},
    {"guard_id": "invalid_i_source_checkout_non_controlled_path", "go_key": "checkout_path_controlled", "depends_on": "checkout_path_controlled"},
    {"guard_id": "invalid_j_source_install_global_env_unapproved", "go_key": "install_target_controlled", "depends_on": "install_target_controlled"},
    {"guard_id": "invalid_k_real_import_model_load_inference", "go_key": "no_real_import_load_inference", "depends_on": "no_real_import_load_inference"},
    {"guard_id": "invalid_l_runtime_output_semantic", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_m_registry_mutated", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_n_post_install_probe_not_find_spec_only", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_o_source_install_success_marked_weight_readiness", "go_key": "success_not_weight_readiness", "depends_on": "success_not_weight_readiness"},
    {"guard_id": "invalid_p_source_install_success_marked_inference_runtime_readiness", "go_key": "success_not_inference_runtime_readiness", "depends_on": "success_not_inference_runtime_readiness"},
    {"guard_id": "invalid_q_partial_success_faked_full_go", "go_key": "partial_not_faked_full_go", "depends_on": "partial_not_faked_full_go"},
    {"guard_id": "invalid_r_post_review_missing_or_no_boundary_review", "go_key": "post_review_present", "depends_on": "post_review_present"},
    {"guard_id": "invalid_s_test_board_real_test_record_missing", "go_key": "test_board_record_required", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_t_test_board_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_u_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
    {"guard_id": "invalid_v_rollback_readiness_missing", "go_key": "rollback_readiness_present", "depends_on": "rollback_readiness_present"},
    {"guard_id": "invalid_w_execution_retry_enters_weight_download_phase", "go_key": "no_weight_download_phase_now", "depends_on": "no_weight_download_phase_now"},
)

# --------------------------------------------------------------------------- #
# Governance rules (42 phase + 6 test board = 48).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_source_install_execution_retry_and_post_review",
    "only_byte_track_and_mobile_sam_are_in_scope",
    "verified_repository_url_is_required_before_checkout",
    "pinned_commit_is_required_before_checkout_or_install",
    "byte_track_must_use_foundationvision_bytetrack_pinned_commit",
    "mobile_sam_must_use_chaoningzhang_mobilesam_pinned_commit",
    "mobile_sam_full_clone_is_forbidden",
    "mobile_sam_committed_weight_file_must_be_excluded",
    "weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "checkpoint_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "example_asset_download_is_not_allowed",
    "source_checkout_path_must_be_controlled",
    "source_install_target_path_must_be_controlled",
    "only_whitelisted_commands_may_execute",
    "code_only_source_install_is_allowed",
    "real_import_is_not_allowed",
    "model_load_is_not_allowed",
    "inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "post_install_probe_must_use_find_spec_only",
    "source_install_success_is_not_model_readiness",
    "source_install_success_is_not_weight_readiness",
    "source_install_success_is_not_inference_approval",
    "source_install_success_is_not_runtime_approval",
    "source_install_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "honest_partial_success_is_allowed",
    "partial_success_must_not_be_promoted_to_full_go",
    "rollback_readiness_is_required",
    "post_review_is_included_and_required",
    "no_weight_download_phase_until_code_only_install_registry_readiness_is_complete",
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
    "source_retry_pre_execution_snapshot_record",
    "source_retry_checkout_execution_record",
    "source_retry_code_install_execution_record",
    "source_retry_post_install_probe_record",
    "source_retry_network_boundary_record",
    "source_retry_weight_exclusion_record",
    "source_retry_partial_success_record",
    "source_retry_post_review_record",
    "source_retry_followup_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledSourceInstallExecutionRetryPostReviewProfile",
    "SourceRetryPreExecutionSnapshotRecord",
    "SourceRetryAssetScope",
    "SourceRetryCommitPinValidationRecord",
    "SourceRetryCheckoutPlanRecord",
    "SourceRetryCheckoutExecutionRecord",
    "SourceRetryCodeInstallExecutionRecord",
    "SourceRetryNetworkBoundaryRecord",
    "SourceRetryWeightExclusionRecord",
    "SourceRetryPostInstallFindSpecProbeRecord",
    "SourceRetryExecutionStepResult",
    "SourceRetryPostReviewAudit",
    "SourceRetryRollbackReadinessRecord",
    "SourceRetryPartialSuccessRecord",
    "SourceRetryFollowupRecord",
    "NegativeSourceInstallExecutionRetryPostReviewGuard",
    "P1ControlledSourceInstallExecutionRetryPostReviewDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_RETRY_CODE_ONLY_GO"
FINAL_DECISION_PARTIAL_GO = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_RETRY_CODE_ONLY_PARTIAL_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_SOURCE_INSTALL_EXECUTION_RETRY_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "real_test_mode_reused": True,
    "upstream_review_evidence_locked_and_reused": True,
}


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionRetryPostReviewProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    source_execution_retry: bool
    post_review_included: bool
    controlled_source_install_execution: bool
    allowed_partial_success: bool
    full_go_required: bool
    source_execution_scope: str
    registry_mutation_allowed: bool
    weight_download_allowed: bool
    model_download_allowed: bool
    checkpoint_download_allowed: bool
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
    full_clone_for_mobile_sam_allowed: bool
    mobile_sam_weight_file_excluded: bool
    in_scope_asset_ids: Tuple[str, ...]
    upstream_review_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SourceRetryPreExecutionSnapshotRecord:
    snapshot_id: str
    python_version: str
    executable_path: str
    pip_version: str
    installed_package_count_before: int
    installed_package_count_after: int
    global_env_diff_empty: bool
    working_directory: str
    source_checkout_root: str
    source_install_target_path: str
    network_policy_ref: str
    command_whitelist_ref: str
    rollback_snapshot_ref: str
    timestamp: str
    upstream_repository_review_ref: str
    upstream_readiness_ref: str
    test_board_ref: str
    snapshot_performed: bool
    snapshot_written_before_execution: bool


@dataclass(frozen=True)
class SourceRetryAssetScope:
    asset_id: str
    source_family: str
    ready_for_retry: bool
    repository_url: str
    commit_hash: str
    license: str
    import_root_candidate: str
    weight_excluding_checkout_required: bool
    full_clone_allowed: bool


@dataclass(frozen=True)
class SourceRetryCommitPinValidationRecord:
    asset_id: str
    expected_commit_hash: str
    resolved_commit_hash: str
    commit_pin_matches: bool
    commit_pin_not_fabricated: bool
    commit_pin_validation_passed: bool


@dataclass(frozen=True)
class SourceRetryCheckoutPlanRecord:
    asset_id: str
    checkout_strategy: str
    full_clone_allowed: bool
    weight_excluding_checkout_required: bool
    blocked_file_patterns: Tuple[str, ...]
    controlled_checkout_path: str


@dataclass(frozen=True)
class SourceRetryCheckoutExecutionRecord:
    asset_id: str
    checkout_strategy: str
    full_clone_used: bool
    weight_excluding_checkout_used: bool
    checkout_path: str
    checkout_path_is_controlled: bool
    resolved_commit_hash: str
    checkout_succeeded: bool
    weight_files_materialized: Tuple[str, ...]
    committed_weight_blob_fetched: bool
    git_lfs_triggered: bool
    unauthorized_large_file_download: bool


@dataclass(frozen=True)
class SourceRetryCodeInstallExecutionRecord:
    asset_id: str
    code_install_command: str
    code_install_return_code: int
    code_install_succeeded: bool
    built_artifact: Optional[str]
    cpp_extension_compiled: bool
    installed_into_controlled_target_only: bool
    global_env_polluted: bool
    dependency_download_performed: bool
    weight_download_performed: bool
    install_stdout_summary: str
    install_stderr_summary: str
    execution_status: str
    defer_or_fail_reason: Optional[str]


@dataclass(frozen=True)
class SourceRetryNetworkBoundaryRecord:
    record_id: str
    asset_id: str
    allowed_target: str
    actual_target: str
    command_ref: str
    purpose: str
    timestamp: str
    network_boundary_compliant: bool
    violation_detected: bool
    violation_reason: Optional[str]


@dataclass(frozen=True)
class SourceRetryWeightExclusionRecord:
    asset_id: str
    weight_excluding_checkout_required: bool
    full_clone_used: bool
    committed_weight_file: str
    committed_weight_blob_fetched: bool
    weight_files_materialized: Tuple[str, ...]
    blocked_file_patterns: Tuple[str, ...]
    git_lfs_triggered: bool
    weight_exclusion_enforced: bool
    weight_download_performed: bool


@dataclass(frozen=True)
class SourceRetryPostInstallFindSpecProbeRecord:
    asset_id: str
    probe_candidates: Tuple[str, ...]
    find_spec_results: Dict[str, bool]
    probe_uses_find_spec_only: bool
    real_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool
    output_adapter_used: bool


@dataclass(frozen=True)
class SourceRetryExecutionStepResult:
    asset_id: str
    snapshot_ok: bool
    commit_pin_validated: bool
    checkout_succeeded: bool
    weight_exclusion_ok: bool
    code_install_succeeded: bool
    probe_find_spec_only: bool
    execution_status: str


@dataclass(frozen=True)
class SourceRetryPostReviewAudit:
    audit_id: str
    pre_snapshot_exists: bool
    checkout_path_controlled: bool
    commit_pin_honored: bool
    mobile_sam_weight_file_excluded: bool
    no_weight_checkpoint_model_dataset_example_download: bool
    no_real_import: bool
    no_model_load: bool
    no_inference: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_layer: bool
    no_registry_mutation: bool
    post_install_probe_find_spec_only: bool
    partial_or_full_decision_honest: bool
    test_board_written_and_protected: bool
    post_review_completed: bool


@dataclass(frozen=True)
class SourceRetryRollbackReadinessRecord:
    asset_id: str
    rollback_available: bool
    rollback_trigger_conditions: Tuple[str, ...]
    rollback_executed: bool
    rollback_not_executed_by_default: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_registry: bool
    rollback_must_preserve_review_artifacts: bool
    rollback_success_requires_post_review: bool


@dataclass(frozen=True)
class SourceRetryPartialSuccessRecord:
    record_id: str
    attempted_source_asset_count: int
    successful_source_asset_count: int
    failed_or_deferred_source_asset_count: int
    all_assets_succeeded: bool
    all_assets_deferred: bool
    partial_go_subtype: Optional[str]
    partial_go_not_full_go: bool
    source_install_success_not_weight_readiness: bool
    source_install_success_not_inference_approval: bool
    source_install_success_not_runtime_approval: bool
    code_only_install_success_not_model_readiness: bool
    no_boundary_violation: bool
    no_environment_contamination: bool


@dataclass(frozen=True)
class SourceRetryFollowupRecord:
    routing_id: str
    recommended_next_phase: str
    ready_for_registry_patch_planning: bool
    no_weight_download_phase_until_code_only_install_registry_readiness_complete: bool
    no_inference_phase_until_weight_download_post_review: bool
    weight_download_requires_separate_approval: bool


@dataclass
class NegativeSourceInstallExecutionRetryPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledSourceInstallExecutionRetryPostReviewDecision:
    decision_ref: str
    controlled_source_install_execution_retry_post_review_profile_count: int
    source_retry_pre_execution_snapshot_record_count: int
    source_retry_asset_scope_count: int
    source_retry_commit_pin_validation_record_count: int
    source_retry_checkout_plan_record_count: int
    source_retry_checkout_execution_record_count: int
    source_retry_code_install_execution_record_count: int
    source_retry_network_boundary_record_count: int
    source_retry_weight_exclusion_record_count: int
    source_retry_post_install_find_spec_probe_record_count: int
    source_retry_post_review_audit_count: int
    source_retry_rollback_readiness_record_count: int
    attempted_source_asset_count: int
    successful_source_asset_count: int
    failed_or_deferred_source_asset_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
