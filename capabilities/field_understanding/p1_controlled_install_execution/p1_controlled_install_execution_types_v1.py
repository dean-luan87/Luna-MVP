# -*- coding: utf-8 -*-
"""P1 Controlled Install Execution — types v1 (FIRST REAL EXECUTION phase).

This is the first phase in the P1 controlled-install chain that produces REAL
side effects, but its scope is strictly PACKAGE-INSTALL-ONLY:

  ALLOWED   : package dependency install (pip) + post-install find_spec probe
  FORBIDDEN : weight / model / dataset download, real inference, runtime,
              runtime activation, output adapter, semantic layer.

The five approved candidates are installed sequentially (no parallel) into a
CONTROLLED virtual environment (workspace-local, --system-site-packages so the
already-present torch/numpy/scipy/opencv are reused). After each install a
find_spec-only probe runs (no real import, no model load, no inference).

Package-name resolution rule (owner-flagged realism guard): package names are
driven from the local model version/dependency registry. If the registry's
canonical package name does NOT resolve to a clean PyPI wheel (e.g. ByteTrack ->
import `yolox`, and MobileSAM -> git source), the engine records
`package_name_resolution_required` and marks that asset DEFERRED (a blocker for
that asset) instead of guessing a similar package name. Under
`allowed_partial_success=True` the cleanly-resolvable assets proceed and the
unresolved ones are carried to the follow-up phase, yielding a PARTIAL-GO.

Package install success is NOT model readiness / weight readiness / inference
approval / runtime approval / output-adapter approval / semantic-layer approval.
Protected, non-deletable test board records are written in `real_test` mode.
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

PHASE_ID = "Phase-P1-Controlled-Install-Execution-v1-001"
SCOPE = "p1_controlled_install_execution"
SOURCE_CHAIN = "p1_controlled_install_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "P1 受控安装第一次真实执行阶段，范围严格限定 package-install-only。允许真实 pip install（仅 5 个候选包依赖）与 "
    "post-install find_spec 探针；不允许权重下载、模型下载、数据集下载、inference、runtime、runtime activation、"
    "output adapter、语义层。安装在受控虚拟环境中按固定顺序串行执行，每步后只做 find_spec 探针（不 import、不加载模型、"
    "不推理）。包名以本地 registry 的 planned_package_names 为准；若 registry 名称无法解析为干净的 PyPI 包（如 "
    "ByteTrack 的 import 名为 yolox、MobileSAM 为 git 源），记录 package_name_resolution_required 并将该资产标为 "
    "blocker/deferred，不擅自安装相似包名。包安装成功不等于模型可用、权重可用、推理批准、runtime 批准、output adapter "
    "批准或语义层批准。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_controlled_install_execution_is_package_install_only_no_weight_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings (per owner spec).
# --------------------------------------------------------------------------- #
REAL_EXECUTION_PHASE = True
PACKAGE_INSTALL_ONLY = True
PACKAGE_INSTALL_EXECUTION_ALLOWED = True
WEIGHT_DOWNLOAD_EXECUTION_ALLOWED = False
MODEL_DOWNLOAD_EXECUTION_ALLOWED = False
DATASET_DOWNLOAD_EXECUTION_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
REAL_OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_PROMOTION_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

# Partial-success policy (owner-selected): cleanly-resolvable assets install and
# the package-name-unresolvable assets are deferred to the follow-up phase.
ALLOWED_PARTIAL_SUCCESS = True
ANY_RESOLVED_STEP_FAILURE_BLOCKS_GO = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

UPSTREAM_PREP_READINESS_REF = (
    "Phase-P1-Controlled-Install-Execution-Preparation-And-Readiness-Review-v1-001"
)
UPSTREAM_ISSUANCE_REF = "Phase-P1-Controlled-Install-Owner-Approval-Issuance-v1-001"
UPSTREAM_REQUEST_POST_REVIEW_REF = "Phase-P1-Controlled-Install-Execution-Request-Post-Review-v1-001"
UPSTREAM_REQUEST_REF = "Phase-P1-Controlled-Install-Execution-Request-v1-001"
EXECUTION_PLANNING_REF = "Phase-P1-Controlled-Install-Execution-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

# If this phase GO/partial-GO, the next step is a POST-REVIEW (NOT weight download).
NEXT_STEP_REF = "Phase-P1-Controlled-Install-Execution-Post-Review-v1-001"

UPSTREAM_PREP_READINESS_EXPECTED_GO = (
    "P1_CONTROLLED_INSTALL_EXECUTION_PREPARATION_AND_READINESS_REVIEW_GO"
)
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

TEST_BOARD_MODULE = "recognition_models"
TEST_BOARD_TEST_MODE = "real_test"

# --------------------------------------------------------------------------- #
# Controlled environment.
# --------------------------------------------------------------------------- #
CONTROLLED_VENV_DIRNAME = "controlled_venv"
TARGET_ENV_LABEL = "p1_controlled_install_execution_controlled_venv_v1"

# --------------------------------------------------------------------------- #
# Scope (locked). Execution order is fixed; no parallel execution.
# --------------------------------------------------------------------------- #
EXECUTION_ORDER: Tuple[Tuple[str, int], ...] = (
    ("supervision", 1),
    ("byte_track", 2),
    ("deep_sort", 3),
    ("midas", 4),
    ("mobile_sam", 5),
)
EXECUTION_ASSET_IDS: Tuple[str, ...] = tuple(a for a, _ in EXECUTION_ORDER)

EXCLUDED_ASSETS: Tuple[Dict[str, str], ...] = (
    {"asset_id": "fast_sam", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "yolov8n", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "pyannote", "exclusion_reason": "BLOCKED_BY_LICENSE"},
    {"asset_id": "sam2", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "depth_anything", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "zoe_depth", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "grounding_dino", "exclusion_reason": "DEFERRED_RESOURCE_HEAVY"},
    {"asset_id": "scene_relation_vlm", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "open_vocab_vlm", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "sense_voice", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "emotion_multimodal_bridge", "exclusion_reason": "RESERVED_ONLY"},
    {"asset_id": "rt_detr", "exclusion_reason": "PARTIAL_OR_NON_INSTALL_REQUIRED"},
)
EXCLUDED_ASSET_IDS: Tuple[str, ...] = tuple(e["asset_id"] for e in EXCLUDED_ASSETS)

# --------------------------------------------------------------------------- #
# Registry-driven package resolution (source of truth = model version/dependency
# registry). `registry_primary_package_name` / `registry_import_name` mirror the
# registry; `pip_install_name` is the PyPI-normalized install token actually
# used. `resolvable` is False when the registry name does NOT map to a clean
# PyPI wheel — those assets are DEFERRED (package_name_resolution_required), not
# guessed.
# --------------------------------------------------------------------------- #
ASSET_PACKAGE_RESOLUTION: Dict[str, Dict[str, Any]] = {
    "supervision": {
        "registry_primary_package_name": "supervision",
        "registry_import_name": "supervision",
        "pip_install_name": "supervision",
        "import_probe_name": "supervision",
        "weight_required": False,
        "resolvable": True,
        "resolution_note": "registry_name_resolves_to_clean_pypi_wheel",
    },
    "byte_track": {
        "registry_primary_package_name": "bytetrack",
        "registry_import_name": "yolox",
        "pip_install_name": "bytetrack",
        "import_probe_name": "yolox",
        "weight_required": False,
        "resolvable": False,
        "resolution_note": (
            "package_name_resolution_required__registry_package_bytetrack_does_not_map_to_clean_pypi_wheel_"
            "providing_import_yolox__bytetrack_is_git_source__deferred_not_guessed"
        ),
    },
    "deep_sort": {
        "registry_primary_package_name": "deep_sort_realtime",
        "registry_import_name": "deep_sort_realtime",
        "pip_install_name": "deep-sort-realtime",
        "import_probe_name": "deep_sort_realtime",
        "weight_required": True,
        "resolvable": True,
        "resolution_note": "registry_name_resolves_to_clean_pypi_wheel__reid_weight_remains_separate",
    },
    "midas": {
        "registry_primary_package_name": "timm",
        "registry_import_name": "timm",
        "pip_install_name": "timm",
        "import_probe_name": "timm",
        "weight_required": True,
        "resolvable": True,
        "resolution_note": "registry_name_resolves_to_clean_pypi_wheel__midas_weights_remain_separate",
    },
    "mobile_sam": {
        "registry_primary_package_name": "mobile_sam",
        "registry_import_name": "mobile_sam",
        "pip_install_name": "mobile-sam",
        "import_probe_name": "mobile_sam",
        "weight_required": True,
        "resolvable": False,
        "resolution_note": (
            "package_name_resolution_required__registry_package_mobile_sam_is_git_source_mobilesam_repo__"
            "no_clean_pypi_wheel__deferred_not_guessed"
        ),
    },
}

RESOLVABLE_ASSET_IDS: Tuple[str, ...] = tuple(
    a for a in EXECUTION_ASSET_IDS if ASSET_PACKAGE_RESOLUTION[a]["resolvable"]
)
DEFERRED_ASSET_IDS: Tuple[str, ...] = tuple(
    a for a in EXECUTION_ASSET_IDS if not ASSET_PACKAGE_RESOLUTION[a]["resolvable"]
)

# Assets that (later, separately) require weight download — NOT in this phase.
WEIGHT_SUBAPPROVAL_ASSETS: Tuple[str, ...] = ("deep_sort", "midas", "mobile_sam")

# --------------------------------------------------------------------------- #
# Stop conditions (any one halts downstream installation).
# --------------------------------------------------------------------------- #
EXECUTION_STOP_CONDITIONS: Tuple[str, ...] = (
    "pre_execution_snapshot_missing",
    "package_install_command_failed",
    "package_install_command_timeout",
    "command_not_in_whitelist",
    "command_scope_drift",
    "unexpected_download_attempt",
    "weight_model_dataset_download_attempt",
    "post_install_find_spec_still_missing",
    "test_board_write_failure",
    "rollback_readiness_missing",
    "environment_corruption_detected",
    "runtime_inference_output_adapter_semantic_flag_enabled",
)

# Pre-execution snapshot fields that must be captured before the first install.
PRE_EXECUTION_SNAPSHOT_FIELDS: Tuple[str, ...] = (
    "python_version",
    "executable_path",
    "pip_version",
    "pip_freeze_before",
    "installed_package_list_before",
    "sys_path_summary",
    "working_directory",
    "target_env_label",
    "timestamp",
    "registry_ref",
    "test_board_ref",
    "rollback_snapshot_ref",
)

INSTALL_COMMAND_GUARD_CHECKS: Tuple[str, ...] = (
    "command_is_in_final_whitelist",
    "asset_id_matches_whitelist",
    "pre_snapshot_exists",
    "rollback_readiness_exists",
    "stop_condition_check_passed",
    "command_has_no_weight_model_dataset_download_url",
    "command_has_no_inference_command",
    "command_has_no_runtime_launch",
    "command_has_no_camera_or_sensor_access",
    "command_has_no_output_adapter_execution",
    "command_has_no_semantic_layer_execution",
)

# --------------------------------------------------------------------------- #
# Negative guards (22: Invalid A..V), per owner spec.
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_install_without_pre_execution_snapshot", "go_key": "snapshot_required_before_install", "depends_on": "pre_execution_snapshot_before_install_enforced"},
    {"guard_id": "invalid_b_command_not_in_whitelist", "go_key": "all_commands_in_whitelist", "depends_on": "all_commands_in_whitelist"},
    {"guard_id": "invalid_c_execution_order_changed", "go_key": "execution_order_verified", "depends_on": "execution_order_verified"},
    {"guard_id": "invalid_d_parallel_execution", "go_key": "parallel_execution_not_used", "depends_on": "parallel_execution_not_used"},
    {"guard_id": "invalid_e_excluded_asset_installed", "go_key": "excluded_assets_not_executed", "depends_on": "excluded_assets_not_executed"},
    {"guard_id": "invalid_f_model_weight_dataset_downloaded", "go_key": "no_download_performed", "depends_on": "no_download_performed"},
    {"guard_id": "invalid_g_command_contains_download_url", "go_key": "no_download_url_in_commands", "depends_on": "no_download_url_in_commands"},
    {"guard_id": "invalid_h_inference_executed", "go_key": "no_real_inference", "depends_on": "no_real_inference"},
    {"guard_id": "invalid_i_runtime_started", "go_key": "no_runtime", "depends_on": "no_runtime"},
    {"guard_id": "invalid_j_output_adapter_started", "go_key": "no_output_adapter", "depends_on": "no_output_adapter"},
    {"guard_id": "invalid_k_semantic_layer_entered", "go_key": "no_semantic_layer", "depends_on": "no_semantic_layer"},
    {"guard_id": "invalid_l_probe_uses_real_import", "go_key": "probe_find_spec_only", "depends_on": "probe_find_spec_only"},
    {"guard_id": "invalid_m_probe_loads_model", "go_key": "no_model_load_on_probe", "depends_on": "no_model_load_on_probe"},
    {"guard_id": "invalid_n_probe_runs_inference", "go_key": "no_inference_on_probe", "depends_on": "no_inference_on_probe"},
    {"guard_id": "invalid_o_downstream_continues_after_failure", "go_key": "failure_stops_downstream", "depends_on": "failure_stops_downstream_enforced"},
    {"guard_id": "invalid_p_test_board_write_fail_but_go", "go_key": "test_board_write_required_for_go", "depends_on": "test_board_write_required_for_go"},
    {"guard_id": "invalid_q_test_artifact_not_protected", "go_key": "test_board_protected_non_deletable", "depends_on": "test_board_protected_non_deletable"},
    {"guard_id": "invalid_r_cleanup_allows_test_board_deletion", "go_key": "cleanup_does_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
    {"guard_id": "invalid_s_install_failure_but_go", "go_key": "install_failure_blocks_go", "depends_on": "install_failure_blocks_go"},
    {"guard_id": "invalid_t_find_spec_failure_but_go", "go_key": "find_spec_failure_blocks_go", "depends_on": "find_spec_failure_blocks_go"},
    {"guard_id": "invalid_u_runtime_inference_adapter_semantic_flag_true", "go_key": "execution_control_flags_all_false", "depends_on": "execution_control_flags_all_false"},
    {"guard_id": "invalid_v_commercial_runtime_approved", "go_key": "commercial_runtime_not_approved", "depends_on": "commercial_runtime_not_approved"},
)

# --------------------------------------------------------------------------- #
# Governance rules (35 phase + 6 test board = 41).
# --------------------------------------------------------------------------- #
PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_controlled_package_install_execution_only",
    "package_install_is_allowed_only_for_five_approved_assets",
    "weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "dataset_download_is_not_allowed",
    "real_inference_is_not_allowed",
    "runtime_execution_is_not_allowed",
    "output_adapter_execution_is_not_allowed",
    "semantic_layer_is_not_allowed",
    "pre_execution_snapshot_is_required_before_first_install_command",
    "final_command_whitelist_is_required",
    "execution_order_is_fixed",
    "parallel_execution_is_not_allowed",
    "failure_must_stop_downstream_execution",
    "excluded_assets_must_not_be_executed",
    "post_install_probe_must_use_find_spec_only",
    "post_install_probe_must_not_use_real_import",
    "post_install_probe_must_not_load_model",
    "post_install_probe_must_not_run_inference",
    "rollback_readiness_must_be_recorded",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
    "package_install_success_is_not_model_readiness",
    "package_install_success_is_not_weight_readiness",
    "package_install_success_is_not_inference_approval",
    "package_install_success_is_not_runtime_approval",
    "package_install_success_is_not_output_adapter_approval",
    "package_install_success_is_not_semantic_layer_approval",
    "commercial_runtime_is_not_approved",
    "candidate_only_boundary_is_preserved",
    "vla_action_chain_is_excluded",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

# Additional protected record types (beyond the 6 protocol records) this
# first-real-execution phase must write.
EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "pre_execution_snapshot_record",
    "package_install_execution_record",
    "post_install_probe_record",
    "stop_condition_record",
    "rollback_readiness_record",
)

OBJECT_TYPES: Tuple[str, ...] = (
    "P1ControlledInstallExecutionProfile",
    "PreExecutionSnapshotRecord",
    "PackageInstallExecutionPlan",
    "PackageInstallExecutionResult",
    "PackageInstallCommandRecord",
    "PostInstallFindSpecProbeRecord",
    "ExecutionStepResult",
    "ExecutionStopConditionRecord",
    "ExecutionFailureRecord",
    "RollbackReadinessRecord",
    "ExecutionSummaryRecord",
    "ExecutionPermissionBoundary",
    "NegativeControlledInstallExecutionGuard",
    "P1ControlledInstallExecutionDecision",
)

FINAL_DECISION_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PACKAGE_ONLY_GO"
FINAL_DECISION_PARTIAL_GO = "P1_CONTROLLED_INSTALL_EXECUTION_PACKAGE_ONLY_PARTIAL_GO"
FINAL_DECISION_BLOCKED = "P1_CONTROLLED_INSTALL_EXECUTION_PACKAGE_ONLY_BLOCKED"

CAN_ENTER_FLAGS: Dict[str, bool] = {
    "can_enter_post_review_next": True,
    "can_enter_weight_download_execution_next": False,
    "can_enter_inference": False,
    "can_enter_runtime": False,
    "can_enter_output_adapter": False,
    "can_enter_semantic_layer": False,
}

# Execution control flags that MUST all stay false.
EXECUTION_CONTROL_FLAGS_FALSE: Dict[str, bool] = {
    "model_download_performed": False,
    "weight_download_performed": False,
    "dataset_download_performed": False,
    "real_inference_performed": False,
    "runtime_execution_performed": False,
    "runtime_activation_performed": False,
    "real_output_adapter_performed": False,
    "semantic_promotion_performed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "vla_action_chain_allowed": False,
}

# Flags that ARE allowed to be true in this real-execution phase.
ALLOWED_TRUE_EXECUTION_FLAGS: Tuple[str, ...] = (
    "pre_execution_snapshot_performed",
    "package_install_attempted",
    "post_install_find_spec_probe_performed",
    "test_board_write_performed",
)


@dataclass(frozen=True)
class P1ControlledInstallExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    package_install_only: bool
    package_install_execution_allowed: bool
    weight_download_execution_allowed: bool
    model_download_execution_allowed: bool
    dataset_download_execution_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    allowed_partial_success: bool
    controlled_venv_label: str
    upstream_prep_readiness_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    execution_asset_ids: Tuple[str, ...]
    resolvable_asset_ids: Tuple[str, ...]
    deferred_asset_ids: Tuple[str, ...]
    excluded_asset_ids: Tuple[str, ...]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class PreExecutionSnapshotRecord:
    snapshot_ref: str
    python_version: str
    executable_path: str
    pip_version: str
    pip_freeze_before_count: int
    installed_package_list_before_count: int
    sys_path_summary: Tuple[str, ...]
    working_directory: str
    target_env_label: str
    timestamp: str
    registry_ref: str
    test_board_ref: str
    rollback_snapshot_ref: str
    snapshot_performed: bool
    snapshot_written_before_first_install: bool
    snapshot_artifact_protected: bool
    snapshot_non_deletable: bool
    all_required_fields_present: bool


@dataclass(frozen=True)
class PackageInstallExecutionPlan:
    asset_id: str
    order_index: int
    registry_primary_package_name: str
    registry_import_name: str
    pip_install_name: str
    import_probe_name: str
    weight_required: bool
    package_name_resolvable: bool
    package_name_resolution_required: bool
    resolution_note: str
    package_install_only: bool
    weight_download_in_scope: bool


@dataclass(frozen=True)
class PackageInstallCommandRecord:
    asset_id: str
    command_argv: Tuple[str, ...]
    command_text: str
    command_in_whitelist: bool
    command_has_no_download_url: bool
    command_has_no_inference: bool
    command_has_no_runtime_launch: bool
    command_has_no_camera_sensor_access: bool
    command_has_no_output_adapter: bool
    command_has_no_semantic_layer: bool
    command_guard_checks_passed: bool
    command_attempted: bool


@dataclass(frozen=True)
class PackageInstallExecutionResult:
    asset_id: str
    order_index: int
    install_attempted: bool
    install_status: str  # installed | install_already_satisfied | deferred_resolution_required | failed | skipped
    install_succeeded: bool
    deferred: bool
    deferred_reason: str
    return_code: Optional[int]
    pip_install_name: str
    output_tail: str
    weight_download_performed: bool
    model_download_performed: bool
    dataset_download_performed: bool


@dataclass(frozen=True)
class PostInstallFindSpecProbeRecord:
    asset_id: str
    import_probe_name: str
    probe_performed: bool
    probe_uses_find_spec_only: bool
    real_import_performed: bool
    model_loaded_on_probe: bool
    inference_on_probe: bool
    runtime_on_probe: bool
    output_adapter_on_probe: bool
    find_spec_found: bool
    probe_result: str  # found | not_found | deferred
    probe_recorded: bool


@dataclass(frozen=True)
class ExecutionStepResult:
    asset_id: str
    order_index: int
    pre_step_stop_condition_check_passed: bool
    command_record_ref: str
    install_result_ref: str
    probe_record_ref: str
    step_status: str  # success | deferred | failed | skipped
    step_succeeded: bool
    downstream_skipped: bool


@dataclass(frozen=True)
class ExecutionStopConditionRecord:
    condition_id: str
    enforced: bool
    triggered: bool


@dataclass(frozen=True)
class ExecutionFailureRecord:
    asset_id: str
    failure_kind: str
    downstream_steps_skipped: bool
    failure_record_written: bool
    rollback_readiness_record_written: bool
    blocks_go_unless_partial: bool


@dataclass(frozen=True)
class RollbackReadinessRecord:
    asset_id: str
    rollback_available: bool
    rollback_template_ref: str
    rollback_not_executed_by_default: bool
    rollback_would_preserve_test_board: bool
    rollback_would_preserve_registry: bool
    rollback_would_preserve_review_artifacts: bool


@dataclass(frozen=True)
class ExecutionSummaryRecord:
    summary_ref: str
    attempted_install_count: int
    successful_install_count: int
    failed_install_count: int
    skipped_install_count: int
    deferred_install_count: int
    post_install_probe_count: int
    post_install_probe_success_count: int
    post_install_probe_failed_count: int
    post_install_probe_deferred_count: int
    package_install_only: bool
    weight_download_performed: bool
    model_download_performed: bool
    dataset_download_performed: bool
    real_inference_performed: bool
    runtime_execution_performed: bool


@dataclass(frozen=True)
class ExecutionPermissionBoundary:
    boundary_ref: str
    real_execution_phase: bool
    package_install_only: bool
    package_install_execution_allowed: bool
    weight_download_execution_allowed: bool
    model_download_execution_allowed: bool
    dataset_download_execution_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    runtime_activation_allowed: bool
    real_output_adapter_allowed: bool
    semantic_promotion_allowed: bool
    commercial_runtime_approved: bool
    package_install_success_not_model_readiness: bool
    package_install_success_not_weight_readiness: bool
    package_install_success_not_inference_approval: bool
    package_install_success_not_runtime_approval: bool
    package_install_success_not_output_adapter_approval: bool
    package_install_success_not_semantic_layer_approval: bool


@dataclass
class NegativeControlledInstallExecutionGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ControlledInstallExecutionDecision:
    decision_ref: str
    controlled_install_execution_profile_count: int
    pre_execution_snapshot_record_count: int
    package_install_execution_plan_count: int
    package_install_command_record_count: int
    package_install_execution_result_count: int
    post_install_find_spec_probe_record_count: int
    execution_step_result_count: int
    rollback_readiness_record_count: int
    execution_summary_record_count: int
    execution_asset_count: int
    excluded_asset_count: int
    attempted_install_count: int
    successful_install_count: int
    failed_install_count: int
    skipped_install_count: int
    deferred_install_count: int
    post_install_probe_count: int
    post_install_probe_success_count: int
    post_install_probe_failed_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
