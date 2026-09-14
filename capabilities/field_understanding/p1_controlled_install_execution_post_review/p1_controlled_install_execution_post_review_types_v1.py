# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution Post-Review — types v1.

PURE POST-REVIEW of the first real (package-install-only) execution phase
(Phase-P1-Controlled-Install-Execution-v1-001, final_decision = PARTIAL_GO).

It audits ONLY — it executes NOTHING:
  no pip install, no dependency install, no model/weight/dataset download, no
  inference, no runtime, no runtime activation, no output adapter, no semantic
  layer, NO registry mutation, and it does NOT back-fill / force-install the two
  deferred (source/git) assets.

What it verifies: that the 3 clean PyPI installs really succeeded, that the 2
source/git assets were honestly DEFERRED (package_name_resolution_required /
git_source), that the post-install probe was find_spec-only, that the
environment delta is traceable, that the test board records are protected, and
crucially that the upstream PARTIAL-GO was NOT mis-read as a full GO / model
readiness / inference readiness / runtime readiness. The two deferred assets are
explicitly routed to a separate source-install / registry-correction sub-chain.
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"
SCOPE = "p1_controlled_install_execution_post_review"
SOURCE_CHAIN = "p1_controlled_install_execution_post_review_v1"

POST_REVIEW_PRINCIPLE_ZH = (
    "对已完成的 Phase-P1-Controlled-Install-Execution-v1-001（真实 package-install-only，PARTIAL_GO）做纯事后复核。"
    "只审查：3 个 clean PyPI 安装是否真实成功、2 个 source/git 资产是否诚实 deferred、find_spec 是否只做探针、"
    "环境变化是否可追踪、测试板块是否 protected、PARTIAL-GO 是否没有被误读为 full GO / model readiness / inference "
    "readiness。不执行 pip install、不安装依赖、不下载模型/权重/数据集、不执行 inference、不进入 runtime / output "
    "adapter / 语义层、不修改 registry、不补装 deferred 资产。两个 deferred 资产明确转入独立的 source install / "
    "registry correction 子链。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_post_review_is_audit_only_no_install_no_download_no_inference_no_runtime_no_registry_mutation"
)

# --------------------------------------------------------------------------- #
# Bindings.
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
PACKAGE_INSTALL_EXECUTION_POST_REVIEW = True
REGISTRY_MUTATION_ALLOWED = False
DEFERRED_ASSET_INSTALL_ALLOWED = False
NEW_PIP_INSTALL_ALLOWED = False
DEPENDENCY_INSTALL_ALLOWED = False
MODEL_DOWNLOAD_ALLOWED = False
WEIGHT_DOWNLOAD_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_EXECUTION_REF = "Phase-P1-Controlled-Install-Execution-v1-001"
UPSTREAM_PREP_READINESS_REF = (
    "Phase-P1-Controlled-Install-Execution-Preparation-And-Readiness-Review-v1-001"
)
UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# Recommended next step is NOT weight download but a deferred-asset sub-chain.
NEXT_STEP_REF = "Phase-P1-Source-Install-And-Package-Name-Resolution-Planning-v1-001"

UPSTREAM_EXECUTION_EXPECTED_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PACKAGE_ONLY_PARTIAL_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "post_review"

# --------------------------------------------------------------------------- #
# Upstream artifacts to read (sealed-ref fallback allowed, with warning).
# --------------------------------------------------------------------------- #
_UP_DIR = "_tmp_eval_out/p1_controlled_install_execution_v1_smoke_v0"
UPSTREAM_REVIEW_ARTIFACT_REL = f"{_UP_DIR}/p1_controlled_install_execution_review_v1.json"
UPSTREAM_SNAPSHOT_ARTIFACT_REL = f"{_UP_DIR}/pre_execution_snapshot_v1.json"
UPSTREAM_STEP_RECORDS_ARTIFACT_REL = f"{_UP_DIR}/install_step_records_v1.json"
UPSTREAM_PROBE_RECORDS_ARTIFACT_REL = f"{_UP_DIR}/post_install_probe_records_v1.json"

# Upstream real_test test board dir (relative; resolved across read roots).
UPSTREAM_TEST_BOARD_DIR_REL = (
    "capabilities/test_board/recognition_models/phase_p1_controlled_install_execution_v1_001"
)

# --------------------------------------------------------------------------- #
# Scope (locked).
# --------------------------------------------------------------------------- #
EXECUTION_ASSET_IDS: Tuple[str, ...] = ("supervision", "byte_track", "deep_sort", "midas", "mobile_sam")
RESOLVABLE_ASSET_IDS: Tuple[str, ...] = ("supervision", "deep_sort", "midas")
DEFERRED_ASSET_IDS: Tuple[str, ...] = ("byte_track", "mobile_sam")
EXCLUDED_ASSET_COUNT = 12

# Expected per-asset install result (audited against the upstream artifact).
EXPECTED_INSTALL_RESULTS: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "supervision", "expected_status_class": "INSTALLED_SUCCESS",
        "package_name": "supervision", "import_name": "supervision",
        "expected_find_spec": "found", "install_not_attempted": False,
        "deferred_reason_tokens": (),
    },
    {
        "asset_id": "byte_track", "expected_status_class": "DEFERRED",
        "package_name": "bytetrack", "import_name": "yolox",
        "expected_find_spec": "deferred_or_not_found", "install_not_attempted": True,
        "deferred_reason_tokens": ("package_name_resolution_required", "clean_pypi_wheel"),
    },
    {
        "asset_id": "deep_sort", "expected_status_class": "INSTALLED_SUCCESS",
        "package_name": "deep-sort-realtime", "import_name": "deep_sort_realtime",
        "expected_find_spec": "found", "install_not_attempted": False,
        "deferred_reason_tokens": (),
    },
    {
        "asset_id": "midas", "expected_status_class": "INSTALLED_SUCCESS",
        "package_name": "timm", "import_name": "timm",
        "expected_find_spec": "found", "install_not_attempted": False,
        "deferred_reason_tokens": (),
    },
    {
        "asset_id": "mobile_sam", "expected_status_class": "DEFERRED",
        "package_name": "mobile_sam", "import_name": "mobile_sam",
        "expected_find_spec": "deferred_or_not_found", "install_not_attempted": True,
        "deferred_reason_tokens": ("git_source", "clean_pypi_wheel"),
    },
)

INSTALLED_SUCCESS_STATUSES: Tuple[str, ...] = ("installed", "install_already_satisfied")
DEFERRED_STATUSES: Tuple[str, ...] = ("deferred_resolution_required",)

# Deferred asset -> follow-up routing.
DEFERRED_ASSET_ROUTING: Tuple[Dict[str, Any], ...] = (
    {
        "asset_id": "byte_track",
        "routed_to_phase_refs": (
            "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001",
            "Phase-P1-Registry-Package-Name-Correction-Planning-v1-001",
        ),
        "routing_reason": "registry_package_bytetrack_import_yolox_requires_source_install_or_registry_name_correction",
        "source_install_required": True,
        "registry_correction_candidate": True,
    },
    {
        "asset_id": "mobile_sam",
        "routed_to_phase_refs": (
            "Phase-P1-Controlled-Source-Install-Resolution-Planning-v1-001",
        ),
        "routing_reason": "registry_package_mobile_sam_is_git_source_mobilesam_repo_requires_source_install",
        "source_install_required": True,
        "registry_correction_candidate": False,
    },
)

# Upstream review artifact audit spec: (field_path, comparator, expected).
# field_path may be dotted to read nested ('decision.attempted_install_count').
ARTIFACT_AUDIT_SPEC: Tuple[Tuple[str, str, Any], ...] = (
    ("final_decision", "eq", UPSTREAM_EXECUTION_EXPECTED_GO),
    ("blocker_count", "eq", 0),
    ("negative_guard_passed", "eq", 22),
    ("decision.attempted_install_count", "eq", 3),
    ("decision.successful_install_count", "eq", 3),
    ("decision.failed_install_count", "eq", 0),
    ("decision.skipped_install_count", "eq", 0),
    ("decision.deferred_install_count", "eq", 2),
    ("decision.post_install_probe_count", "eq", 5),
    ("decision.post_install_probe_success_count", "eq", 3),
    ("decision.post_install_probe_failed_count", "eq", 0),
    ("execution_summary_record.post_install_probe_deferred_count", "eq", 2),
    ("execution_summary_record.weight_download_performed", "eq", False),
    ("execution_summary_record.model_download_performed", "eq", False),
    ("execution_summary_record.dataset_download_performed", "eq", False),
    ("execution_summary_record.real_inference_performed", "eq", False),
    ("execution_summary_record.runtime_execution_performed", "eq", False),
)

SEALED_EXPECTED_UPSTREAM: Dict[str, Any] = {
    "final_decision": UPSTREAM_EXECUTION_EXPECTED_GO,
    "blocker_count": 0,
    "negative_guard_passed": 22,
    "decision": {
        "attempted_install_count": 3,
        "successful_install_count": 3,
        "failed_install_count": 0,
        "skipped_install_count": 0,
        "deferred_install_count": 2,
        "post_install_probe_count": 5,
        "post_install_probe_success_count": 3,
        "post_install_probe_failed_count": 0,
    },
    "execution_summary_record": {
        "post_install_probe_deferred_count": 2,
        "weight_download_performed": False,
        "model_download_performed": False,
        "dataset_download_performed": False,
        "real_inference_performed": False,
        "runtime_execution_performed": False,
    },
}

# Pre-execution snapshot fields the snapshot audit must confirm exist.
SNAPSHOT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "python_version",
    "executable_path",
    "pip_version",
    "pip_freeze_before_count",
    "installed_package_list_before_count",
    "sys_path_summary",
    "working_directory",
    "target_env_label",
    "timestamp",
    "registry_ref",
    "test_board_ref",
    "rollback_snapshot_ref",
)

# Upstream real_test test board record types the audit must confirm present.
UPSTREAM_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "test_process_record",
    "test_result_summary",
    "test_conclusion_record",
    "test_artifact_refs",
    "protected_marker",
    "non_deletable_notice",
    "test_board_manifest",
    "pre_execution_snapshot_record",
    "package_install_execution_record",
    "post_install_probe_record",
    "stop_condition_record",
    "rollback_readiness_record",
)

# Non-runtime boundary flags (>= 16) the audit must confirm false.
NON_RUNTIME_BOUNDARY_FLAGS: Tuple[str, ...] = (
    "model_download_performed",
    "weight_download_performed",
    "dataset_download_performed",
    "real_inference_performed",
    "runtime_execution_performed",
    "runtime_activation_performed",
    "real_output_adapter_performed",
    "semantic_promotion_performed",
    "live_camera_connected",
    "live_sensor_connected",
    "continuous_runtime_allowed",
    "navigation_runtime_allowed",
    "action_runtime_allowed",
    "speech_runtime_allowed",
    "fact_write_runtime_allowed",
    "vla_action_chain_allowed",
    "commercial_runtime_approved",
)

# --------------------------------------------------------------------------- #
# Negative guards (20: Invalid A..T).
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_package_only_partial_go", "go_key": "upstream_partial_go_verified", "depends_on": "upstream_partial_go_verified"},
    {"guard_id": "invalid_b_upstream_blocker_count_nonzero", "go_key": "upstream_blocker_count_zero", "depends_on": "upstream_blocker_count_zero"},
    {"guard_id": "invalid_c_attempted_install_count_not_three", "go_key": "attempted_install_count_verified", "depends_on": "attempted_install_count_correct"},
    {"guard_id": "invalid_d_successful_install_count_not_three", "go_key": "successful_install_count_verified", "depends_on": "successful_install_count_correct"},
    {"guard_id": "invalid_e_deferred_install_count_not_two", "go_key": "deferred_install_count_verified", "depends_on": "deferred_install_count_correct"},
    {"guard_id": "invalid_f_deferred_asset_force_installed", "go_key": "no_deferred_asset_forced_install", "depends_on": "deferred_assets_not_installed"},
    {"guard_id": "invalid_g_deferred_reason_not_recorded", "go_key": "deferred_reasons_recorded", "depends_on": "deferred_reasons_recorded"},
    {"guard_id": "invalid_h_find_spec_uses_real_import", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_i_probe_loads_model_or_inference", "go_key": "probe_no_load_no_inference", "depends_on": "probe_no_load_no_inference"},
    {"guard_id": "invalid_j_model_weight_dataset_download", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_k_git_clone_or_source_install", "go_key": "no_source_install_performed", "depends_on": "no_source_install_performed"},
    {"guard_id": "invalid_l_runtime_output_adapter_semantic_triggered", "go_key": "no_runtime_output_semantic", "depends_on": "no_runtime_output_semantic"},
    {"guard_id": "invalid_m_partial_go_marked_full_go", "go_key": "partial_go_not_full_go", "depends_on": "partial_go_not_full_go"},
    {"guard_id": "invalid_n_find_spec_success_marked_model_readiness", "go_key": "find_spec_success_not_model_readiness", "depends_on": "find_spec_not_model_readiness"},
    {"guard_id": "invalid_o_install_success_marked_inference_runtime_approval", "go_key": "install_success_not_inference_runtime_approval", "depends_on": "install_not_inference_runtime_approval"},
    {"guard_id": "invalid_p_test_board_real_test_records_missing", "go_key": "test_board_real_execution_records_present", "depends_on": "test_board_real_execution_records_present"},
    {"guard_id": "invalid_q_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
    {"guard_id": "invalid_s_post_review_executes_new_pip_install", "go_key": "no_new_pip_install_in_post_review", "depends_on": "no_new_pip_install_in_post_review"},
    {"guard_id": "invalid_t_post_review_mutates_registry", "go_key": "no_registry_mutation_in_post_review", "depends_on": "no_registry_mutation_in_post_review"},
)

# --------------------------------------------------------------------------- #
# Governance rules (31 phase + 6 test board = 37).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_package_install_execution_post_review_only",
    "no_new_pip_install_is_allowed_in_post_review",
    "no_dependency_install_is_allowed_in_post_review",
    "no_model_download_is_allowed",
    "no_weight_download_is_allowed",
    "no_dataset_download_is_allowed",
    "no_real_inference_is_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "registry_mutation_is_not_allowed",
    "deferred_assets_must_remain_deferred",
    "deferred_source_installs_require_separate_approval",
    "registry_package_name_correction_requires_separate_review",
    "partial_go_must_remain_partial",
    "partial_go_must_not_be_promoted_to_full_go",
    "package_install_success_is_not_model_readiness",
    "package_install_success_is_not_weight_readiness",
    "find_spec_success_is_not_model_readiness",
    "find_spec_success_is_not_inference_approval",
    "find_spec_success_is_not_runtime_approval",
    "find_spec_success_is_not_output_adapter_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "vla_action_chain_is_excluded",
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
    "package_install_result_audit_record",
    "deferred_asset_audit_record",
    "environment_delta_audit_record",
    "post_install_probe_audit_record",
    "partial_go_boundary_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionPostReviewProfile",
    "ExecutionArtifactAudit",
    "PreExecutionSnapshotAudit",
    "PackageInstallResultAudit",
    "PostInstallFindSpecProbeAudit",
    "DeferredAssetAudit",
    "EnvironmentDeltaAudit",
    "PartialGoBoundaryAudit",
    "TestBoardRealExecutionRecordAudit",
    "NonRuntimeBoundaryAudit",
    "SourceInstallFollowupRoutingRecord",
    "NegativeControlledInstallExecutionPostReviewGuard",
    "P1ControlledInstallExecutionPostReviewDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
    "post_review_test_mode_reused": True,
}


@dataclass(frozen=True)
class P1ControlledInstallExecutionPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    package_install_execution_post_review: bool
    registry_mutation_allowed: bool
    deferred_asset_install_allowed: bool
    new_pip_install_allowed: bool
    dependency_install_allowed: bool
    model_download_allowed: bool
    weight_download_allowed: bool
    dataset_download_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    upstream_execution_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    execution_asset_ids: Tuple[str, ...]
    resolvable_asset_ids: Tuple[str, ...]
    deferred_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ExecutionArtifactAudit:
    artifact_ref: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    upstream_final_decision: str
    upstream_blocker_count: int
    checks_total: int
    checks_passed: int
    field_results: Tuple[Dict[str, Any], ...]
    audit_holds: bool


@dataclass(frozen=True)
class PreExecutionSnapshotAudit:
    audit_ref: str
    artifact_read_mode: str
    snapshot_present: bool
    required_fields_present: Tuple[str, ...]
    missing_fields: Tuple[str, ...]
    snapshot_taken_before_first_install: bool
    snapshot_record_protected: bool
    snapshot_missing_blocks_full_go: bool
    audit_holds: bool


@dataclass(frozen=True)
class PackageInstallResultAudit:
    asset_id: str
    expected_status_class: str
    observed_status: str
    status_class_matches: bool
    package_name: str
    import_name: str
    expected_find_spec: str
    observed_find_spec_found: bool
    find_spec_matches: bool
    install_not_attempted_expected: bool
    install_not_attempted_observed: bool
    deferred_reason_tokens_present: bool
    audit_holds: bool


@dataclass(frozen=True)
class PostInstallFindSpecProbeAudit:
    audit_ref: str
    probe_count: int
    probe_success_count: int
    probe_failed_count: int
    probe_deferred_count: int
    probe_uses_find_spec_only: bool
    real_import_used: bool
    model_load_used: bool
    inference_used: bool
    runtime_used: bool
    output_adapter_used: bool
    find_spec_success_not_model_readiness: bool
    find_spec_success_not_weight_readiness: bool
    find_spec_success_not_inference_approval: bool
    find_spec_success_not_runtime_approval: bool
    audit_holds: bool


@dataclass(frozen=True)
class DeferredAssetAudit:
    asset_id: str
    deferred_observed: bool
    install_not_attempted: bool
    not_runtime_ready: bool
    deferred_reason: str
    deferred_reason_tokens_present: bool
    routed_to_phase_refs: Tuple[str, ...]
    source_install_required: bool
    registry_correction_candidate: bool
    audit_holds: bool


@dataclass(frozen=True)
class EnvironmentDeltaAudit:
    audit_ref: str
    pre_snapshot_exists: bool
    post_snapshot_exists: bool
    post_snapshot_missing_warning: bool
    post_snapshot_required_for_next_execution: bool
    installed_packages_limited_to_approved_clean_assets: bool
    no_git_clone_performed: bool
    no_source_install_performed: bool
    no_model_file_downloaded: bool
    no_weight_file_downloaded: bool
    no_dataset_file_downloaded: bool
    controlled_venv_path_recorded: bool
    environment_delta_recorded: bool
    audit_holds: bool


@dataclass(frozen=True)
class PartialGoBoundaryAudit:
    audit_ref: str
    partial_go_accepted: bool
    partial_go_not_full_go: bool
    partial_go_success_not_model_readiness: bool
    partial_go_success_not_weight_readiness: bool
    partial_go_success_not_inference_approval: bool
    partial_go_success_not_runtime_approval: bool
    partial_go_success_not_output_adapter_approval: bool
    deferred_assets_not_blocking_partial_go: bool
    audit_holds: bool


@dataclass(frozen=True)
class TestBoardRealExecutionRecordAudit:
    audit_ref: str
    board_dir_ref: str
    board_read_mode: str
    expected_record_types: Tuple[str, ...]
    present_record_types: Tuple[str, ...]
    missing_record_types: Tuple[str, ...]
    test_mode_is_real_test: bool
    protected: bool
    non_deletable: bool
    deletion_forbidden: bool
    package_install_only: bool
    weight_download_execution_allowed_false: bool
    record_count: int
    audit_holds: bool


@dataclass(frozen=True)
class NonRuntimeBoundaryAudit:
    audit_ref: str
    flags_checked: Tuple[str, ...]
    all_false: bool
    flag_count: int
    audit_holds: bool


@dataclass(frozen=True)
class SourceInstallFollowupRoutingRecord:
    asset_id: str
    routed_to_phase_refs: Tuple[str, ...]
    routing_reason: str
    deferred_assets_require_separate_phase: bool
    source_install_requires_separate_approval: bool
    registry_correction_requires_separate_review: bool
    deferred_asset_not_installed: bool


@dataclass
class NegativeControlledInstallExecutionPostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallExecutionPostReviewDecision:
    decision_ref: str
    controlled_install_execution_post_review_profile_count: int
    execution_artifact_audit_count: int
    pre_execution_snapshot_audit_count: int
    package_install_result_audit_count: int
    post_install_find_spec_probe_audit_count: int
    deferred_asset_audit_count: int
    environment_delta_audit_count: int
    partial_go_boundary_audit_count: int
    test_board_real_execution_record_audit_count: int
    non_runtime_boundary_audit_count: int
    source_install_followup_routing_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
