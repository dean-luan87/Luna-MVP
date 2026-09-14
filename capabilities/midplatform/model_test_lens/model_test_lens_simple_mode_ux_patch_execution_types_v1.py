# -*- coding: utf-8 -*-
"""P1 Model Test Lens Simple Mode UX Patch Execution — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Simple-Mode-UX-Patch-Execution-And-Post-Review-v1-001"
SCOPE = "p1_midplatform_model_test_lens_simple_mode_ux_patch_execution"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_simple_mode_ux_patch_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "对 Model Test Lens 本地测试页面执行 Simple Mode UX Patch。"
    "默认界面仅显示：选择文件、选择测试类型、开始测试、进度、结果。"
    "manifest/job/bridge 技术细节仅在高级模式或开发者模式显示。"
    "页面不直接执行模型；真实执行仍由 127.0.0.1:8787 Local Runner Bridge 负责。"
)

LUNA_CORE_PRINCIPLE = "simple_mode_default_one_click_test_via_local_runner_bridge_not_in_browser"

REAL_EXECUTION_PHASE = True
SIMPLE_MODE_UX_PATCH = True
DEFAULT_USER_MODE = "simple"
ADVANCED_MODE_AVAILABLE = True
DEVELOPER_MODE_AVAILABLE = True
LOCAL_RUNNER_BRIDGE_PRESERVED = True
LOCAL_RUNNER_BRIDGE_HOST = "127.0.0.1"
LOCAL_RUNNER_BRIDGE_PORT = 8787
PAGE_MAY_SUBMIT_LOCAL_JOB = True
PAGE_MAY_LOAD_ENVELOPE = True
PAGE_MUST_NOT_EXECUTE_MODEL = True
MODEL_EXECUTION_ALLOWED_IN_PAGE = False
RUNNER_EXECUTION_ALLOWED_IN_SERVICE_ONLY = True
REGISTRY_MUTATION_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
EXTERNAL_NETWORK_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
LIVE_MICROPHONE_ALLOWED = False
OUTPUT_ADAPTER_ALLOWED = False
RUNTIME_ALLOWED = False
TESTBOARD_DELETE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_UI_PATCH_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
)
UPSTREAM_RUNNER_BRIDGE_SKELETON_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Skeleton-Execution-And-Post-Review-v1-001"
)
UPSTREAM_RUNNER_BRIDGE_PLANNING_REF = (
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
    f"{STATIC_SITE_ROOT_REL}/simple_mode_ui_v1.js",
    f"{STATIC_SITE_ROOT_REL}/local_asset_import_ui_v1.js",
    f"{STATIC_SITE_ROOT_REL}/runner_bridge_ui_v1.js",
    f"{STATIC_SITE_ROOT_REL}/local_asset_import_examples_v1.js",
)

FORBIDDEN_CODE_PATTERNS: Tuple[Dict[str, str], ...] = (
    {"pattern_id": "external_fetch", "regex": r"fetch\s*\(\s*['\"]https?://"},
    {"pattern_id": "camera_api", "regex": r"getUserMedia|MediaRecorder"},
    {"pattern_id": "media_devices", "regex": r"navigator\.mediaDevices"},
    {"pattern_id": "runtime_endpoint", "regex": r"/runtime|/run_model|/infer\b"},
    {"pattern_id": "registry_write", "regex": r"/registry/write|mutateRegistry\s*\(|updateRegistry\s*\("},
    {"pattern_id": "page_model_execution", "regex": r"runInference\s*\(|executeModel\s*\(|startInference\s*\("},
    {"pattern_id": "output_adapter_call", "regex": r"output_adapter_call\s*\("},
    {"pattern_id": "fact_write", "regex": r"writeFact\s*\(|writeSemantic\s*\("},
    {"pattern_id": "navigation_speech", "regex": r"triggerSpeech\s*\(|triggerNavigation\s*\("},
    {"pattern_id": "delete_artifact", "regex": r"deleteArtifact\s*\(|removeTestBoard\s*\("},
)

UI_AUDIT_MARKERS: Tuple[Dict[str, str], ...] = (
    {"key": "simple_mode_ui_written", "needle": "simple_mode_ui_v1.js"},
    {"key": "simple_mode_card_present", "needle": "simple-mode-host"},
    {"key": "one_click_start_button_present", "needle": "sm-start"},
    {"key": "file_picker_present", "needle": "sm-file-input"},
    {"key": "test_type_selector_present", "needle": "sm-test-types"},
    {"key": "progress_steps_present", "needle": "sm-progress"},
    {"key": "advanced_mode_toggle_present", "needle": "advanced-mode-toggle"},
    {"key": "advanced_workflow_hidden_by_default", "needle": 'id="advanced-workflow" hidden'},
    {"key": "developer_mode_toggle_present", "needle": "debug-mode-toggle"},
    {"key": "service_status_banner_present", "needle": "sm-service-banner"},
    {"key": "user_friendly_boundary_present", "needle": "不会写入事实层"},
    {"key": "slam_limited_notice_present", "needle": "sm-slam-notice"},
    {"key": "manifest_buttons_in_advanced", "needle": "lai-generate-manifest"},
    {"key": "job_bridge_buttons_in_advanced", "needle": "rb-create-job"},
    {"key": "local_runner_bridge_8787_preserved", "needle": "127.0.0.1:8787"},
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "A", "go_key": "upstream_go_verified", "depends_on": "upstream_go_verified"},
    {"guard_id": "B", "go_key": "no_bypass_8787", "depends_on": "no_bypass_8787"},
    {"guard_id": "C", "go_key": "no_page_inference_endpoint", "depends_on": "no_page_inference_endpoint"},
    {"guard_id": "D", "go_key": "no_runtime", "depends_on": "no_runtime"},
    {"guard_id": "E", "go_key": "no_fact_semantic_navigation", "depends_on": "no_fact_semantic_navigation"},
    {"guard_id": "F", "go_key": "no_registry_mutation", "depends_on": "no_registry_mutation"},
    {"guard_id": "G", "go_key": "no_external_network", "depends_on": "no_external_network"},
    {"guard_id": "H", "go_key": "no_live_camera_microphone", "depends_on": "no_live_camera_microphone"},
    {"guard_id": "I", "go_key": "no_delete_artifact", "depends_on": "no_delete_artifact"},
    {"guard_id": "J", "go_key": "manifest_job_bridge_preserved", "depends_on": "manifest_job_bridge_preserved"},
    {"guard_id": "K", "go_key": "advanced_mode_available", "depends_on": "advanced_mode_available"},
    {"guard_id": "L", "go_key": "developer_mode_available", "depends_on": "developer_mode_available"},
    {"guard_id": "M", "go_key": "technical_json_hidden_by_default", "depends_on": "technical_json_hidden_by_default"},
    {"guard_id": "N", "go_key": "mobilesam_one_click_flow_present", "depends_on": "mobilesam_one_click_flow_present"},
    {"guard_id": "O", "go_key": "slam_limited_one_click_flow_present", "depends_on": "slam_limited_one_click_flow_present"},
    {"guard_id": "P", "go_key": "existing_features_preserved", "depends_on": "existing_features_preserved"},
    {"guard_id": "Q", "go_key": "test_board_written", "depends_on": "test_board_written"},
    {"guard_id": "R", "go_key": "test_board_protected", "depends_on": "test_board_protected"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "Simple Mode is the default user mode.",
    "Default view must be decision-oriented.",
    "Default view must not expose raw JSON.",
    "Default view must not expose manifest/job/bridge internals.",
    "Advanced Mode may expose workflow details.",
    "Developer Mode may expose raw JSON and artifact refs.",
    "One-click local test must still use Local Runner Bridge.",
    "Page must not execute models directly.",
    "Page must not run inference directly.",
    "Page must not bypass 127.0.0.1:8787 service.",
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
    "Imported assets remain scoped local test assets.",
    "Results remain candidate-only.",
    "Results are not fact sources.",
    "Results are not runtime sources.",
    "SLAM limited route must not compute ATE.",
    "SLAM limited route must clearly display limited mode.",
    "Existing envelope import must be preserved.",
    "Existing examples must be preserved.",
    "Insight Layer must be preserved.",
    "Debug Mode must be preserved.",
    "TestBoard record is required.",
    "Test process record is required.",
    "Test conclusion record is required.",
    "Test artifacts are protected.",
    "Test records are non-deletable.",
    "Cleanup must not delete TestBoard artifacts.",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = tuple(TEST_BOARD_GOVERNANCE_RULES) + PHASE_GOVERNANCE_RULES

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "simple_mode_ui_patch_record",
    "simple_mode_one_click_flow_record",
    "simple_mode_boundary_audit",
    "simple_mode_ux_patch_post_review_audit",
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_SIMPLE_MODE_UX_PATCH_EXECUTION_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_SIMPLE_MODE_UX_PATCH_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_SIMPLE_MODE_UX_PATCH_EXECUTION_BLOCKED"


@dataclass
class SimpleModeUIFilePatchRecord:
    simple_mode_ui_written: bool
    index_html_updated: bool
    app_js_updated: bool
    styles_css_updated: bool
    default_view_simplified: bool
    technical_buttons_hidden_by_default: bool


@dataclass
class SimpleModeOneClickFlowRecord:
    one_click_local_test_button_present: bool
    mobilesam_one_click_flow_present: bool
    slam_limited_one_click_flow_present: bool
    user_friendly_progress_steps_present: bool
    user_friendly_error_messages_present: bool
    service_status_simplified: bool
    local_runner_bridge_service_preserved: bool


@dataclass
class SimpleModeBoundaryAudit:
    no_page_model_execution: bool
    no_runtime: bool
    no_output_adapter: bool
    no_fact_semantic_navigation: bool
    no_registry_mutation: bool
    no_external_network: bool
    no_live_camera_microphone: bool
    no_delete_artifact_button: bool


@dataclass
class SimpleModeUXPatchPostReviewAudit:
    post_review_passed: bool
    simple_mode_ui_written: bool
    default_view_simplified: bool
    advanced_mode_available: bool
    developer_mode_available: bool
    manifest_job_bridge_preserved: bool


@dataclass
class NegativeSimpleModeUXPatchGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool


@dataclass
class P1ModelTestLensSimpleModeUXPatchExecutionDecision:
    decision_ref: str
    simple_mode_ux_patch_profile_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    failure_recorded: bool
    no_boundary_violation: bool
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
