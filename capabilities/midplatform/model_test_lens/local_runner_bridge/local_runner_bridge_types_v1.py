# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Runner Bridge Service — types v1 (planning only)."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Planning-v1-001"
SCOPE = "p1_midplatform_model_test_lens_local_runner_bridge_service_planning"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_local_runner_bridge_service_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "规划 Model Test Lens 本地 Runner Bridge Service（localhost:8787）。"
    "该 service 仅服务本机模型测试：接收页面提交的本地资产与 job，"
    "在受控 runner phase 中执行模型、经 adapter 生成 MUEP envelope，"
    "写 TestBoard 并返回 job 状态与结果路径给 localhost:8765 页面展示。"
    "本 service 不是 runtime、不是 output adapter、不是商业后端。"
    "本阶段仅 planning，不实现服务、不执行模型、不上传真实文件、不启动 HTTP。"
)

LUNA_CORE_PRINCIPLE = (
    "model_test_lens_ui_at_8765_submits_jobs_local_runner_bridge_at_8787_executes_tests_"
    "adapter_required_candidate_only_not_runtime_not_fact"
)

PLANNING_ONLY = True
LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING = True
LOCALHOST_ONLY = True
MODEL_TEST_LENS_BACKEND_BRIDGE = True
NOT_RUNTIME = True
NOT_OUTPUT_ADAPTER = True
NOT_COMMERCIAL_BACKEND = True
PAGE_MAY_SUBMIT_LOCAL_JOB = True
SERVICE_MAY_EXECUTE_MODEL_AFTER_APPROVAL = True
SERVICE_MUST_WRITE_TESTBOARD = True
ADAPTER_REQUIRED_BEFORE_UI_DISPLAY = True
REGISTRY_MUTATION_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
EXTERNAL_NETWORK_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
LIVE_MICROPHONE_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False
DATASET_DOWNLOAD_ALLOWED = False

SLAM_WITHOUT_GT_NO_ATE = True
SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON = True
CANDIDATE_ONLY_BOUNDARY_DEFINED = True
TESTBOARD_REQUIRED_FOR_EACH_JOB = True

UI_HOST = "http://localhost:8765"
SERVICE_HOST = "http://127.0.0.1:8787"
SERVICE_BIND_ADDRESS = "127.0.0.1"
SERVICE_PORT = 8787

ASSET_STORE_REL = "capabilities/test_assets/model_test_lens"
EVAL_OUT_REL = "_tmp_eval_out/model_test_lens_local_runner_bridge"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_LOCAL_ASSET_IMPORT_PLANNING_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-And-Runner-Bridge-Planning-v1-001"
)
UPSTREAM_UI_PATCH_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
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
MUEP_V1_REF = "capabilities/midplatform/model_test_lens/standards/muep/"
SLAM_ADAPTER_V1_REF = "capabilities/midplatform/model_test_lens/adapters/slam/slam_evaluation_adapter_v1.py"
SLAM_DIAGNOSTIC_V1_REF = "capabilities/midplatform/model_test_lens/adapters/slam/slam_diagnostic_engine_v1.py"

NEXT_PHASE_SKELETON_EXECUTION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Skeleton-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "planning"

MODEL_TEST_LENS_ROOT_REL = "capabilities/midplatform/model_test_lens"
LOCAL_RUNNER_BRIDGE_ROOT_REL = f"{MODEL_TEST_LENS_ROOT_REL}/local_runner_bridge"
SCHEMAS_LOCAL_RUNNER_BRIDGE_REL = f"{LOCAL_RUNNER_BRIDGE_ROOT_REL}/schemas"

API_ENDPOINTS: Tuple[Dict[str, Any], ...] = (
    {
        "method": "POST",
        "path": "/api/v1/assets/register",
        "purpose": "receive local upload or path ref; generate manifest; return asset_id/manifest_ref",
    },
    {
        "method": "POST",
        "path": "/api/v1/jobs/create",
        "purpose": "create test job from asset_manifest + model_category + model_id",
        "run_after_create_default": False,
    },
    {
        "method": "POST",
        "path": "/api/v1/jobs/{job_id}/run",
        "purpose": "trigger local runner execution; localhost only; candidate-only; TestBoard required",
    },
    {
        "method": "GET",
        "path": "/api/v1/jobs/{job_id}/status",
        "purpose": "return queued/running/completed/failed/blocked",
    },
    {
        "method": "GET",
        "path": "/api/v1/jobs/{job_id}/result",
        "purpose": "return envelope path, result manifest, TestBoard refs",
    },
    {
        "method": "GET",
        "path": "/api/v1/capabilities",
        "purpose": "return available local runners on this machine",
    },
)

JOB_LIFECYCLE_STATES: Tuple[str, ...] = (
    "created",
    "asset_registered",
    "awaiting_approval",
    "ready_to_run",
    "running",
    "adapter_processing",
    "completed",
    "failed_no_boundary_violation",
    "blocked",
)

RUNNER_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "runner_id": "segmentation_mobile_sam_runner",
        "runner_type": "segmentation_runner",
        "status": "planned_v1",
        "inputs": ("image_manifest", "prompt_plan"),
        "outputs": ("candidate_masks", "quality_metrics", "muep_envelope"),
        "model_id": "mobile_sam",
    },
    {
        "runner_id": "slam_video_runner",
        "runner_type": "slam_runner",
        "status": "planned_v1_limited",
        "inputs": ("video_manifest", "frame_sequence_manifest", "optional_gt_trajectory"),
        "outputs": ("trajectory", "diagnostics", "slam_envelope"),
        "constraints": ("no_ate_without_gt", "no_gt_benchmark_comparison_without_gt"),
    },
    {
        "runner_id": "ocr_runner",
        "runner_type": "ocr_runner",
        "status": "placeholder",
        "inputs": ("image_manifest", "frame_manifest"),
        "outputs": ("text_boxes", "recognized_text", "confidence", "ocr_envelope"),
    },
    {
        "runner_id": "tts_eval_runner",
        "runner_type": "tts_runner",
        "status": "placeholder",
        "inputs": ("text_manifest", "generated_audio_ref"),
        "outputs": ("waveform", "duration", "quality_metrics", "tts_envelope"),
    },
    {
        "runner_id": "asr_runner",
        "runner_type": "asr_runner",
        "status": "placeholder",
        "inputs": ("audio_manifest",),
        "outputs": ("transcript", "timestamps", "wer_if_reference", "asr_envelope"),
    },
)

CAPABILITY_IDS: Tuple[str, ...] = (
    "segmentation_mobile_sam",
    "slam_orb_placeholder",
    "ocr_placeholder",
    "tts_placeholder",
    "asr_placeholder",
)

SLAM_VIDEO_RUNNER_ROUTE_STAGES: Tuple[str, ...] = (
    "video_or_frame_sequence_upload",
    "asset_register_api",
    "job_create_api",
    "job_run_api_after_approval",
    "slam_video_runner",
    "raw_trajectory_output",
    "slam_evaluation_adapter_v1",
    "slam_diagnostic_engine_v1",
    "muep_envelope",
    "ui_load_result_api",
)

MOBILESAM_IMAGE_RUNNER_ROUTE_STAGES: Tuple[str, ...] = (
    "image_upload",
    "asset_register_api",
    "job_create_api",
    "job_run_api_after_approval",
    "segmentation_mobile_sam_runner",
    "candidate_masks",
    "segmentation_metrics",
    "muep_envelope",
    "ui_load_result_api",
)

SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS: Tuple[str, ...] = (
    "trajectory_visualization",
    "tracking_lost_ratio",
    "smoothness_proxy",
    "failure_timeline_if_tracking_state_available",
    "no_ate",
    "no_full_drift_score",
    "no_gt_limited_mode",
    "not_comparable_to_gt_benchmark",
)

UI_INTEGRATION_PATCH_ITEMS: Tuple[Dict[str, str], ...] = (
    {"ui_id": "upload_and_register_asset", "action": "call_post_api_v1_assets_register"},
    {"ui_id": "create_test_job", "action": "call_post_api_v1_jobs_create"},
    {"ui_id": "run_local_test", "action": "call_post_api_v1_jobs_run_after_approval"},
    {"ui_id": "view_job_status", "action": "poll_get_api_v1_jobs_status"},
    {"ui_id": "load_result", "action": "get_api_v1_jobs_result_then_render_envelope"},
)

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = TEST_BOARD_GOVERNANCE_RULES + (
    "Local Runner Bridge is localhost-only.",
    "Local Runner Bridge is not runtime.",
    "Local Runner Bridge is not output adapter.",
    "Local Runner Bridge is not commercial backend.",
    "UI may submit jobs to Local Runner Bridge.",
    "Runner may execute model only as test job.",
    "Runner must write TestBoard.",
    "Adapter must generate MUEP envelope before UI display.",
    "Results are candidate-only.",
    "Results are not facts.",
    "Results are not runtime outputs.",
    "Results are not output adapter outputs.",
    "Results are not semantic outputs.",
    "Results must not trigger navigation/action/speech.",
    "Service must not bind external network.",
    "Service must not access external URL.",
    "Service must not use live camera.",
    "Service must not use live microphone.",
    "Service must not mutate registry.",
    "Service must not download dataset.",
    "SLAM without GT must not compute ATE.",
    "SLAM without GT must not compare with GT benchmark.",
    "Job lifecycle is required.",
    "Runner registry is required.",
    "API schema is required.",
    "TestBoard record is required.",
    "Test artifacts are protected.",
    "Test records are non-deletable.",
    "Cleanup must not delete TestBoard artifacts.",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "local_runner_bridge_api_plan_record",
    "local_runner_job_lifecycle_record",
    "local_runner_registry_plan_record",
    "slam_local_video_runner_route_record",
    "mobilesam_local_image_runner_route_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_service_as_runtime", "go_key": "negative_guard_invalid_a_blocked", "depends_on": "not_runtime"},
    {"guard_id": "invalid_b_bind_external_network", "go_key": "negative_guard_invalid_b_blocked", "depends_on": "localhost_only"},
    {"guard_id": "invalid_c_external_url_dataset", "go_key": "negative_guard_invalid_c_blocked", "depends_on": "no_external_network"},
    {"guard_id": "invalid_d_live_camera_mic", "go_key": "negative_guard_invalid_d_blocked", "depends_on": "no_live_camera_mic"},
    {"guard_id": "invalid_e_registry_mutation", "go_key": "negative_guard_invalid_e_blocked", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_f_fact_semantic_write", "go_key": "negative_guard_invalid_f_blocked", "depends_on": "no_fact_semantic"},
    {"guard_id": "invalid_g_output_adapter_nav_speech", "go_key": "negative_guard_invalid_g_blocked", "depends_on": "not_output_adapter_nav_speech"},
    {"guard_id": "invalid_h_runner_no_testboard", "go_key": "negative_guard_invalid_h_blocked", "depends_on": "testboard_required_for_each_job"},
    {"guard_id": "invalid_i_adapter_not_required", "go_key": "negative_guard_invalid_i_blocked", "depends_on": "adapter_required_before_ui_display"},
    {"guard_id": "invalid_j_slam_no_gt_ate", "go_key": "negative_guard_invalid_j_blocked", "depends_on": "slam_without_gt_no_ate"},
    {"guard_id": "invalid_k_slam_no_gt_benchmark", "go_key": "negative_guard_invalid_k_blocked", "depends_on": "slam_without_gt_no_gt_benchmark"},
    {"guard_id": "invalid_l_job_lifecycle_missing", "go_key": "negative_guard_invalid_l_blocked", "depends_on": "job_lifecycle_defined"},
    {"guard_id": "invalid_m_runner_registry_missing", "go_key": "negative_guard_invalid_m_blocked", "depends_on": "runner_registry_defined"},
    {"guard_id": "invalid_n_api_schema_missing", "go_key": "negative_guard_invalid_n_blocked", "depends_on": "api_schema_defined"},
    {"guard_id": "invalid_o_candidate_only_missing", "go_key": "negative_guard_invalid_o_blocked", "depends_on": "candidate_only_boundary_defined"},
    {"guard_id": "invalid_p_testboard_not_protected", "go_key": "negative_guard_invalid_p_blocked", "depends_on": "test_artifact_protected"},
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING_GO"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "reuse_local_asset_import_planning": True,
    "reuse_muep_v1": True,
    "reuse_slam_adapter_v1": True,
    "reuse_slam_diagnostic_v1": True,
    "reuse_model_test_lens_static_site": True,
    "reuse_testboard_protocol": True,
}


@dataclass(frozen=True)
class LocalRunnerBridgeServicePlanningProfile:
    profile_ref: str
    phase_id: str
    planning_only: bool
    local_runner_bridge_service_planning: bool
    localhost_only: bool
    model_test_lens_backend_bridge: bool
    not_runtime: bool
    not_output_adapter: bool
    not_commercial_backend: bool
    page_may_submit_local_job: bool
    service_may_execute_model_after_approval: bool
    service_must_write_testboard: bool
    adapter_required_before_ui_display: bool
    registry_mutation_allowed: bool
    semantic_layer_allowed: bool
    fact_write_allowed: bool
    navigation_action_speech_allowed: bool
    external_network_allowed: bool
    live_camera_allowed: bool
    live_microphone_allowed: bool
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class LocalRunnerBridgeApiPlanRecord:
    record_id: str
    service_host: str
    service_bind_address: str
    service_port: int
    ui_host: str
    endpoints: Tuple[Dict[str, Any], ...]
    localhost_only: bool
    external_network_allowed: bool


@dataclass(frozen=True)
class LocalRunnerJobLifecycleRecord:
    record_id: str
    states: Tuple[str, ...]
    required_fields_per_state: Tuple[str, ...]
    lifecycle_defined: bool


@dataclass(frozen=True)
class LocalRunnerRegistryPlanRecord:
    record_id: str
    runners: Tuple[Dict[str, Any], ...]
    capability_ids: Tuple[str, ...]
    runner_registry_defined: bool
    v1_implementation_runners: Tuple[str, ...]


@dataclass(frozen=True)
class SlamLocalVideoRunnerRouteRecord:
    record_id: str
    route_stages: Tuple[str, ...]
    without_gt_limited_diagnostics: Tuple[str, ...]
    no_ate_without_gt: bool
    no_gt_benchmark_comparison_without_gt: bool


@dataclass(frozen=True)
class MobileSamLocalImageRunnerRouteRecord:
    record_id: str
    route_stages: Tuple[str, ...]
    candidate_only: bool
    not_fact_not_runtime: bool


@dataclass
class NegativeLocalRunnerBridgeServicePlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1MidplatformModelTestLensLocalRunnerBridgeServicePlanningDecision:
    decision_ref: str
    local_runner_bridge_service_planning_profile_count: int
    api_schema_defined: bool
    job_lifecycle_defined: bool
    runner_registry_defined: bool
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
