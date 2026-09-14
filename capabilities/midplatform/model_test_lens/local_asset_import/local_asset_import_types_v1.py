# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Asset Import & Runner Bridge Planning — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-And-Runner-Bridge-Planning-v1-001"
SCOPE = "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "规划 Model Test Lens 本地图片/视频/帧序列/音频导入与 runner bridge。"
    "页面可作为测试入口：登记 scoped local test asset、生成 manifest 与 job request、"
    "路由至独立 runner 执行 phase，经 adapter 转 envelope 后只读展示。"
    "页面不得直接执行模型、不得 inference、不得启动 SLAM/OCR/SAM/TTS 后端。"
    "本阶段仅 planning，不实现真实导入执行。"
)

LUNA_CORE_PRINCIPLE = (
    "model_test_lens_may_be_test_entry_not_model_executor_"
    "local_asset_import_candidate_only_runner_bridge_requires_approval"
)

PLANNING_ONLY = True
MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_PLANNING = True
RUNNER_BRIDGE_PLANNING = True
LOCAL_STATIC_PAGE_ONLY = True
PAGE_MAY_REGISTER_ASSETS = True
PAGE_MAY_CREATE_JOB_REQUEST = True
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
COMMERCIAL_RUNTIME_APPROVED = False

RUNNER_BRIDGE_REQUIRES_OWNER_APPROVAL = True
ADAPTER_REQUIRED_BEFORE_ENVELOPE_DISPLAY = True
LOCAL_ASSETS_CANDIDATE_ONLY = True
LOCAL_ASSETS_NOT_FACT_SOURCE = True
LOCAL_ASSETS_NOT_RUNTIME_SOURCE = True
SLAM_WITHOUT_GT_NO_ATE = True
SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON = True

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_SKELETON_EXECUTION_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Skeleton-Execution-And-Post-Review-v1-001"
)
UPSTREAM_LENS_PLANNING_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Static-Site-Planning-v1-001"
)
UPSTREAM_MOBILE_SAM_MULTI_EXEC_REF = (
    "Phase-P1-MobileSAM-Multi-Real-Image-Inference-Trial-Execution-And-Post-Review-v1-001"
)
UPSTREAM_MOBILE_SAM_QUALITY_REF = (
    "Phase-P1-MobileSAM-Real-Image-Quality-Review-And-Prompt-Strategy-Planning-v1-001"
)
UPSTREAM_MOBILE_SAM_RUNTIME_BOUNDARY_REF = (
    "Phase-P1-MobileSAM-Runtime-Boundary-Standardization-Planning-v1-001"
)
UPSTREAM_GOVERNANCE_PACKAGING_REF = (
    "Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001"
)
MUEP_V1_REF = "capabilities/midplatform/model_test_lens/standards/muep/"
SLAM_ADAPTER_V1_REF = "capabilities/midplatform/model_test_lens/adapters/slam/slam_evaluation_adapter_v1.py"
SLAM_DIAGNOSTIC_V1_REF = "capabilities/midplatform/model_test_lens/adapters/slam/slam_diagnostic_engine_v1.py"

NEXT_PHASE_UI_PATCH = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

MODEL_TEST_LENS_ROOT_REL = "capabilities/midplatform/model_test_lens"
LOCAL_ASSET_IMPORT_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/local_asset_import"
RUNNER_BRIDGE_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/runner_bridge"
SCHEMAS_LOCAL_ASSET_REL = f"{MODEL_TEST_LENS_ROOT_REL}/schemas/local_asset_import"

LOCAL_ASSET_TYPES: Tuple[str, ...] = (
    "image",
    "video",
    "frame_sequence",
    "audio",
    "text",
)

ASSET_TYPE_MODEL_MAP: Tuple[Dict[str, Any], ...] = (
    {
        "asset_type": "image",
        "applicable_models": (
            "segmentation", "ocr", "depth_world", "detection_tracking",
            "face_expression_gesture", "multimodal_vlm",
        ),
    },
    {
        "asset_type": "video",
        "applicable_models": (
            "slam_vio", "detection_tracking", "ocr", "segmentation",
            "multimodal_vlm", "face_expression_gesture",
        ),
    },
    {
        "asset_type": "frame_sequence",
        "applicable_models": ("slam_vio", "detection_tracking", "ocr", "segmentation"),
    },
    {
        "asset_type": "audio",
        "applicable_models": ("asr", "speaker", "tts"),
    },
    {
        "asset_type": "text",
        "applicable_models": ("tts", "multimodal_vlm"),
    },
)

SLAM_VIDEO_ROUTE_STAGES: Tuple[str, ...] = (
    "video_or_frame_sequence",
    "local_asset_manifest",
    "slam_job_request",
    "runner_bridge_request",
    "orb_slam3_vins_kimera_runner_execution_phase",
    "raw_trajectory_output",
    "slam_evaluation_adapter_v1",
    "slam_diagnostic_engine_v1",
    "muep_envelope",
    "model_test_lens_display",
)

IMAGE_IMPORT_ROUTE_STAGES: Tuple[str, ...] = (
    "image",
    "local_asset_manifest",
    "segmentation_ocr_depth_vlm_job_request",
    "runner_bridge_request",
    "model_specific_runner_execution_phase",
    "model_specific_adapter",
    "muep_envelope",
    "model_test_lens_display",
)

SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS: Tuple[str, ...] = (
    "trajectory_visualization",
    "tracking_state_timeline",
    "trajectory_smoothness_proxy",
    "lost_frame_ratio",
    "no_ate",
    "no_full_drift_score",
)

UI_PATCH_PLAN_ITEMS: Tuple[Dict[str, str], ...] = (
    {"ui_id": "import_test_asset_btn", "action": "select_local_file_generate_manifest_only"},
    {"ui_id": "create_test_job_btn", "action": "select_model_type_generate_job_request_no_execution"},
    {"ui_id": "runner_status_placeholder", "action": "read_local_runner_output_manifest_only"},
    {"ui_id": "import_envelope_json", "action": "retain_existing_json_envelope_import"},
    {"ui_id": "developer_mode", "action": "show_manifest_job_runner_bridge_json"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = TEST_BOARD_GOVERNANCE_RULES + (
    "Model Test Lens may import local test assets.",
    "Local asset import does not mean model execution.",
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
    "Adapter is required before envelope display.",
    "TestBoard record is required.",
    "Test artifacts are protected.",
    "Test records are non-deletable.",
    "Cleanup must not delete TestBoard artifacts.",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "local_test_asset_manifest_record",
    "model_test_job_request_record",
    "runner_bridge_request_record",
    "asset_import_route_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_page_direct_model_execution", "go_key": "negative_guard_invalid_a_blocked", "depends_on": "page_must_not_execute_model"},
    {"guard_id": "invalid_b_import_then_inference", "go_key": "negative_guard_invalid_b_blocked", "depends_on": "no_real_inference_on_page"},
    {"guard_id": "invalid_c_import_video_start_slam", "go_key": "negative_guard_invalid_c_blocked", "depends_on": "no_slam_backend_on_page"},
    {"guard_id": "invalid_d_live_camera_mic", "go_key": "negative_guard_invalid_d_blocked", "depends_on": "no_live_camera_mic"},
    {"guard_id": "invalid_e_external_url", "go_key": "negative_guard_invalid_e_blocked", "depends_on": "no_external_url"},
    {"guard_id": "invalid_f_auto_dataset_download", "go_key": "negative_guard_invalid_f_blocked", "depends_on": "no_dataset_download"},
    {"guard_id": "invalid_g_registry_write", "go_key": "negative_guard_invalid_g_blocked", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_h_output_semantic_fact_nav", "go_key": "negative_guard_invalid_h_blocked", "depends_on": "no_runtime_downstream"},
    {"guard_id": "invalid_i_asset_as_fact_runtime", "go_key": "negative_guard_invalid_i_blocked", "depends_on": "local_assets_not_fact_or_runtime"},
    {"guard_id": "invalid_j_slam_no_gt_ate", "go_key": "negative_guard_invalid_j_blocked", "depends_on": "slam_without_gt_no_ate"},
    {"guard_id": "invalid_k_runner_no_approval", "go_key": "negative_guard_invalid_k_blocked", "depends_on": "runner_bridge_requires_owner_approval"},
    {"guard_id": "invalid_l_manifest_schema_missing", "go_key": "negative_guard_invalid_l_blocked", "depends_on": "local_test_asset_manifest_schema_defined"},
    {"guard_id": "invalid_m_job_schema_missing", "go_key": "negative_guard_invalid_m_blocked", "depends_on": "model_test_job_request_schema_defined"},
    {"guard_id": "invalid_n_runner_bridge_schema_missing", "go_key": "negative_guard_invalid_n_blocked", "depends_on": "runner_bridge_request_schema_defined"},
    {"guard_id": "invalid_o_testboard_missing", "go_key": "negative_guard_invalid_o_blocked", "depends_on": "test_board_record_required"},
    {"guard_id": "invalid_p_testboard_not_protected", "go_key": "negative_guard_invalid_p_blocked", "depends_on": "test_artifact_protected"},
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_RUNNER_BRIDGE_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_RUNNER_BRIDGE_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "reuse_muep_v1": True,
    "reuse_slam_adapter_v1": True,
    "reuse_slam_diagnostic_v1": True,
    "reuse_existing_envelope_import": True,
    "reuse_insight_layer": True,
    "reuse_progressive_disclosure_ui": True,
}


@dataclass(frozen=True)
class ModelTestLensLocalAssetImportPlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    model_test_lens_local_asset_import_planning: bool
    runner_bridge_planning: bool
    local_static_page_only: bool
    page_may_register_assets: bool
    page_may_create_job_request: bool
    page_must_not_execute_model: bool
    model_execution_allowed: bool
    real_inference_allowed: bool
    runtime_execution_allowed: bool
    output_adapter_allowed: bool
    semantic_layer_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    registry_mutation_allowed: bool
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelTestLensImportRouteRecord:
    record_id: str
    slam_video_import_route_defined: bool
    image_import_route_defined: bool
    slam_route_stages: Tuple[str, ...]
    image_route_stages: Tuple[str, ...]
    slam_without_gt_limited_diagnostics: Tuple[str, ...]


@dataclass(frozen=True)
class ModelTestLensImportUiPatchPlanRecord:
    record_id: str
    ui_patch_items: Tuple[Dict[str, str], ...]
    planning_only_no_page_change_this_phase: bool
    retain_json_envelope_import: bool
    retain_mobile_sam_example: bool
    retain_slam_example: bool
    retain_insight_layer: bool
    retain_debug_mode: bool


@dataclass
class NegativeLocalAssetImportPlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MidplatformModelTestLensLocalAssetImportRunnerBridgePlanningDecision:
    decision_ref: str
    model_test_lens_local_asset_import_runner_bridge_planning_profile_count: int
    local_test_asset_manifest_schema_defined: bool
    model_test_job_request_schema_defined: bool
    runner_bridge_request_schema_defined: bool
    asset_to_envelope_route_schema_defined: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
