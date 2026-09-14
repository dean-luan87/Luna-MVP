# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Asset Import UI Patch Execution — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
SCOPE = "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_local_asset_import_ui_patch_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "对 Model Test Lens 静态页执行本地资产导入 UI Patch。"
    "用户可选择 image/video/frame_sequence/audio/text，"
    "在浏览器内生成 manifest、job request、runner bridge request，"
    "并显示 runner 输出占位状态。页面不执行模型、不 inference、"
    "不启动 SLAM/OCR/SAM/TTS 后端。"
)

LUNA_CORE_PRINCIPLE = (
    "page_registers_local_test_assets_generates_job_requests_"
    "runner_executes_in_separate_phase_not_in_browser"
)

REAL_EXECUTION_PHASE = True
STATIC_SITE_UI_PATCH_EXECUTION = True
LOCAL_ASSET_IMPORT_UI_ENABLED = True
RUNNER_BRIDGE_UI_ENABLED = True
LOCAL_STATIC_PAGE_ONLY = True
PAGE_MAY_REGISTER_ASSETS = True
PAGE_MAY_CREATE_JOB_REQUEST = True
PAGE_MAY_CREATE_RUNNER_BRIDGE_REQUEST = True
PAGE_MAY_READ_RUNNER_OUTPUT_MANIFEST = True
PAGE_MAY_IMPORT_ENVELOPE = True
PAGE_MUST_NOT_EXECUTE_MODEL = True
MODEL_EXECUTION_ALLOWED = False
REAL_INFERENCE_ALLOWED = False
RUNTIME_EXECUTION_ALLOWED = False
RUNTIME_ACTIVATION_ALLOWED = False
OUTPUT_ADAPTER_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
REGISTRY_MUTATION_ALLOWED = False
EXTERNAL_URL_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
MICROPHONE_LIVE_CAPTURE_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
FILE_DELETE_ALLOWED = False
TESTBOARD_DELETE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-And-Runner-Bridge-Planning-v1-001"
)
UPSTREAM_SKELETON_EXECUTION_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Execution-And-Post-Review-v1-001"
)
UPSTREAM_LENS_PLANNING_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001"
)
UPSTREAM_MOBILE_SAM_MULTI_EXEC_REF = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)

NEXT_PHASE_RUNNER_BRIDGE_SERVICE = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Planning-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "real_test"

STATIC_SITE_ROOT_REL = "capabilities/midplatform/model_test_lens/static_site"
MODEL_TEST_LENS_ROOT_REL = "capabilities/midplatform/model_test_lens"

REQUIRED_STATIC_FILES: Tuple[str, ...] = (
    f"{STATIC_SITE_ROOT_REL}/index.html",
    f"{STATIC_SITE_ROOT_REL}/app.js",
    f"{STATIC_SITE_ROOT_REL}/styles.css",
    f"{STATIC_SITE_ROOT_REL}/local_asset_import_ui_v1.js",
    f"{STATIC_SITE_ROOT_REL}/runner_bridge_ui_v1.js",
    f"{STATIC_SITE_ROOT_REL}/local_asset_import_examples_v1.js",
)

OPTIONAL_EXAMPLE_FILES: Tuple[str, ...] = (
    f"{MODEL_TEST_LENS_ROOT_REL}/examples/local_asset_import_example_manifest_v1.json",
    f"{MODEL_TEST_LENS_ROOT_REL}/examples/model_test_job_request_example_v1.json",
    f"{MODEL_TEST_LENS_ROOT_REL}/examples/runner_bridge_request_example_v1.json",
)

FORBIDDEN_CODE_PATTERNS: Tuple[Dict[str, str], ...] = (
    {"pattern_id": "external_fetch", "regex": r"fetch\s*\(\s*['\"]https?://"},
    {"pattern_id": "camera_api", "regex": r"getUserMedia|MediaRecorder"},
    {"pattern_id": "media_devices", "regex": r"navigator\.mediaDevices"},
    {"pattern_id": "websocket", "regex": r"new\s+WebSocket\s*\("},
    {"pattern_id": "xhr_external", "regex": r"new\s+XMLHttpRequest\s*\("},
    {"pattern_id": "runtime_endpoint", "regex": r"/runtime|/run_model|/infer\b"},
    {"pattern_id": "registry_write", "regex": r"/registry/write|mutateRegistry\s*\(|updateRegistry\s*\("},
    {"pattern_id": "model_execution", "regex": r"runInference\s*\(|executeModel\s*\(|startInference\s*\("},
    {"pattern_id": "output_adapter_call", "regex": r"output_adapter_call\s*\("},
    {"pattern_id": "fact_write", "regex": r"writeFact\s*\(|writeSemantic\s*\("},
    {"pattern_id": "navigation_speech", "regex": r"triggerSpeech\s*\(|triggerNavigation\s*\("},
    {"pattern_id": "delete_artifact", "regex": r"deleteArtifact\s*\(|removeTestBoard\s*\("},
)

UI_AUDIT_MARKERS: Tuple[Dict[str, str], ...] = (
    {"key": "asset_type_selector_present", "needle": "lai-asset-type"},
    {"key": "local_file_selector_present", "needle": "lai-file-input"},
    {"key": "model_category_selector_present", "needle": "lai-model-category"},
    {"key": "generate_manifest_button_present", "needle": "lai-generate-manifest"},
    {"key": "create_job_request_button_present", "needle": "rb-create-job"},
    {"key": "create_runner_bridge_request_button_present", "needle": "rb-create-bridge"},
    {"key": "runner_output_status_placeholder_present", "needle": "rb-runner-status"},
    {"key": "debug_mode_json_preview_present", "needle": "import-json-debug-block"},
    {"key": "slam_without_gt_hints_present", "needle": "SLAM_HINT_LINES"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = TEST_BOARD_GOVERNANCE_RULES + (
    "This phase patches Model Test Lens local asset import UI.",
    "Page may register local test assets.",
    "Page may generate local asset manifest.",
    "Page may generate model test job request.",
    "Page may generate runner bridge request.",
    "Page may show runner output status placeholder.",
    "Page may import completed envelope.",
    "Page must not execute models.",
    "Page must not run inference.",
    "Page must not start SLAM/OCR/SAM/TTS backend.",
    "Page must not trigger runtime.",
    "Page must not call output adapter.",
    "Page must not write semantic layer.",
    "Page must not write facts.",
    "Page must not trigger navigation/action/speech.",
    "Page must not mutate registry.",
    "Page must not access live camera.",
    "Page must not access live microphone.",
    "Page must not fetch external URL assets.",
    "Page must not download datasets.",
    "Imported assets are scoped local test assets.",
    "Imported assets are candidate-only.",
    "Imported assets are not fact sources.",
    "Imported assets are not runtime sources.",
    "Runner bridge requires separate execution phase.",
    "Runner bridge requires owner approval.",
    "SLAM without GT must not compute ATE.",
    "SLAM without GT must not be compared to GT benchmark.",
    "Existing envelope import must be preserved.",
    "Existing examples must be preserved.",
    "Insight Layer must be preserved.",
    "Debug Mode must hide JSON by default.",
    "TestBoard record is required.",
    "Test process record is required.",
    "Test conclusion record is required.",
    "Test artifacts are protected.",
    "Test records are non-deletable.",
    "Cleanup must not delete TestBoard artifacts.",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "local_asset_import_ui_file_patch_record",
    "local_asset_manifest_generation_ui_record",
    "model_test_job_request_ui_record",
    "runner_bridge_request_ui_record",
    "runner_output_status_placeholder_record",
    "no_model_execution_boundary_audit_record",
    "local_asset_import_ui_post_review_record",
    "followup_runner_bridge_execution_route_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "negative_guard_invalid_a_blocked", "depends_on": "upstream_planning_go_verified"},
    {"guard_id": "invalid_b_page_model_execution", "go_key": "negative_guard_invalid_b_blocked", "depends_on": "no_model_execution"},
    {"guard_id": "invalid_c_page_slam_sam_backend", "go_key": "negative_guard_invalid_c_blocked", "depends_on": "no_inference_execution"},
    {"guard_id": "invalid_d_runtime_output_adapter", "go_key": "negative_guard_invalid_d_blocked", "depends_on": "no_runtime_output_adapter"},
    {"guard_id": "invalid_e_semantic_fact_nav_speech", "go_key": "negative_guard_invalid_e_blocked", "depends_on": "no_semantic_fact_navigation"},
    {"guard_id": "invalid_f_registry_mutation", "go_key": "negative_guard_invalid_f_blocked", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_g_external_url", "go_key": "negative_guard_invalid_g_blocked", "depends_on": "no_external_url"},
    {"guard_id": "invalid_h_camera_microphone", "go_key": "negative_guard_invalid_h_blocked", "depends_on": "no_camera_microphone"},
    {"guard_id": "invalid_i_delete_artifact", "go_key": "negative_guard_invalid_i_blocked", "depends_on": "no_delete_artifact_button"},
    {"guard_id": "invalid_j_manifest_missing", "go_key": "negative_guard_invalid_j_blocked", "depends_on": "generate_manifest_button_present"},
    {"guard_id": "invalid_k_job_request_missing", "go_key": "negative_guard_invalid_k_blocked", "depends_on": "create_job_request_button_present"},
    {"guard_id": "invalid_l_runner_bridge_missing", "go_key": "negative_guard_invalid_l_blocked", "depends_on": "create_runner_bridge_request_button_present"},
    {"guard_id": "invalid_m_runner_status_missing", "go_key": "negative_guard_invalid_m_blocked", "depends_on": "runner_output_status_placeholder_present"},
    {"guard_id": "invalid_n_existing_features_broken", "go_key": "negative_guard_invalid_n_blocked", "depends_on": "existing_features_preserved"},
    {"guard_id": "invalid_o_debug_mode_missing", "go_key": "negative_guard_invalid_o_blocked", "depends_on": "debug_mode_json_preview_present"},
    {"guard_id": "invalid_p_slam_gt_hints_missing", "go_key": "negative_guard_invalid_p_blocked", "depends_on": "slam_without_gt_hints_present"},
    {"guard_id": "invalid_q_testboard_missing", "go_key": "negative_guard_invalid_q_blocked", "depends_on": "test_board_record_required"},
    {"guard_id": "invalid_r_testboard_not_protected", "go_key": "negative_guard_invalid_r_blocked", "depends_on": "test_artifact_protected"},
    {"guard_id": "invalid_s_cleanup_deletes_testboard", "go_key": "negative_guard_invalid_s_blocked", "depends_on": "cleanup_preserves_testboard"},
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_UI_PATCH_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_UI_PATCH_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_UI_PATCH_EXECUTION_BLOCKED"

NEXT_PHASE_BLOCKED = "BLOCKED"
NEXT_PHASE_FAILED = "UI_PATCH_RETRY"
NEXT_PHASE_GO = NEXT_PHASE_RUNNER_BRIDGE_SERVICE

REUSE_FLAGS: Dict[str, bool] = {
    "reuse_local_asset_import_planning": True,
    "reuse_insight_layer": True,
    "reuse_slam_diagnostics": True,
    "reuse_envelope_import": True,
    "reuse_mobile_sam_example": True,
    "reuse_slam_example": True,
}


@dataclass(frozen=True)
class P1ModelTestLensLocalAssetImportUIPatchExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    static_site_ui_patch_execution: bool
    local_asset_import_ui_enabled: bool
    runner_bridge_ui_enabled: bool
    page_must_not_execute_model: bool
    model_execution_allowed: bool
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class LocalAssetImportUIFilePatchRecord:
    record_id: str
    static_site_root_rel: str
    files_written: Tuple[str, ...]
    index_html_updated: bool
    app_js_updated: bool
    styles_css_updated: bool
    local_asset_import_ui_js_written: bool
    runner_bridge_ui_js_written: bool
    local_asset_import_examples_js_written: bool
    ui_patch_files_written: bool


@dataclass(frozen=True)
class LocalAssetManifestGenerationUIRecord:
    record_id: str
    generate_manifest_button_present: bool
    asset_type_selector_present: bool
    local_file_selector_present: bool
    manifest_fields_documented: bool


@dataclass(frozen=True)
class ModelTestJobRequestUIRecord:
    record_id: str
    create_job_request_button_present: bool
    requires_runner_execution: bool
    requires_owner_approval: bool
    candidate_output_only: bool


@dataclass(frozen=True)
class RunnerBridgeRequestUIRecord:
    record_id: str
    create_runner_bridge_request_button_present: bool
    lens_may_not_execute_runner: bool
    adapter_required: bool
    adapter_target_envelope: str


@dataclass(frozen=True)
class RunnerOutputStatusPlaceholderRecord:
    record_id: str
    runner_output_status_placeholder_present: bool
    waiting_for_runner_output_label: bool
    import_envelope_when_ready_label: bool


@dataclass(frozen=True)
class NoModelExecutionBoundaryAuditRecord:
    record_id: str
    no_model_execution: bool
    no_inference_execution: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_fact_navigation: bool
    no_registry_mutation: bool
    no_external_url: bool
    no_camera_microphone: bool
    no_delete_artifact_button: bool
    forbidden_pattern_scan_passed: bool


@dataclass(frozen=True)
class LocalAssetImportUIPostReviewAudit:
    audit_id: str
    index_html_updated: bool
    app_js_updated: bool
    styles_css_updated: bool
    local_asset_import_ui_js_written: bool
    runner_bridge_ui_js_written: bool
    asset_type_selector_present: bool
    local_file_selector_present: bool
    model_category_selector_present: bool
    generate_manifest_button_present: bool
    create_job_request_button_present: bool
    create_runner_bridge_request_button_present: bool
    runner_output_status_placeholder_present: bool
    debug_mode_json_preview_present: bool
    existing_envelope_import_preserved: bool
    mobilesam_example_preserved: bool
    slam_example_preserved: bool
    insight_layer_preserved: bool
    model_panel_count: int
    no_model_execution: bool
    no_inference_execution: bool
    no_runtime: bool
    no_output_adapter: bool
    no_semantic_fact_navigation: bool
    no_registry_mutation: bool
    no_external_url: bool
    no_camera_microphone: bool
    no_delete_artifact_button: bool
    test_board_written: bool
    test_board_protected: bool
    post_review_passed: bool


@dataclass(frozen=True)
class LocalAssetImportUIRollbackReadinessRecord:
    record_id: str
    rollback_available: bool
    rollback_can_restore_previous_static_site_files: bool
    rollback_must_preserve_planning_artifacts: bool
    rollback_must_preserve_test_board: bool
    rollback_must_preserve_examples: bool
    rollback_not_executed_by_default: bool


@dataclass(frozen=True)
class FollowupRunnerBridgeExecutionRouteRecord:
    record_id: str
    recommended_next_phase: str
    route_note: str
    page_submits_job_runner_executes_separately: bool


@dataclass
class NegativeLocalAssetImportUIPatchGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1ModelTestLensLocalAssetImportUIPatchExecutionDecision:
    decision_ref: str
    model_test_lens_local_asset_import_ui_patch_execution_profile_count: int
    ui_patch_files_written: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
