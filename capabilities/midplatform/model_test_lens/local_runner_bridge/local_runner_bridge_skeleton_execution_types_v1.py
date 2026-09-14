# -*- coding: utf-8 -*-
"""P1 Local Runner Bridge Service Skeleton Execution — types v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Skeleton-Execution-And-Post-Review-v1-001"
SCOPE = "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution"
WEIGHT_CHAIN = "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_v1"

EXECUTION_PRINCIPLE_ZH = (
    "实现 Model Test Lens 本地 Runner Bridge Service skeleton（127.0.0.1:8787）。"
    "支持资产登记、job 创建/执行/状态/结果查询；MobileSAM image runner 受控执行；"
    "SLAM video limited placeholder。不是 runtime，不是 output adapter，不是商业后端。"
)

LUNA_CORE_PRINCIPLE = (
    "localhost_runner_bridge_skeleton_mobilesam_test_runner_slam_limited_placeholder_"
    "adapter_envelope_testboard_candidate_only"
)

REAL_EXECUTION_PHASE = True
LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION = True
LOCALHOST_ONLY = True
BIND_HOST = "127.0.0.1"
BIND_PORT = 8787
NOT_RUNTIME = True
NOT_OUTPUT_ADAPTER = True
NOT_COMMERCIAL_BACKEND = True
PAGE_MAY_SUBMIT_LOCAL_JOB = True
SERVICE_MAY_REGISTER_ASSETS = True
SERVICE_MAY_CREATE_JOBS = True
SERVICE_MAY_EXECUTE_TEST_RUNNER = True
SERVICE_MAY_EXECUTE_MOBILE_SAM_IMAGE_RUNNER = True
SERVICE_MAY_EXECUTE_SLAM_VIDEO_LIMITED_RUNNER = True
SERVICE_MUST_WRITE_TESTBOARD = True
ADAPTER_REQUIRED_BEFORE_UI_DISPLAY = True
REGISTRY_MUTATION_ALLOWED = False
SEMANTIC_LAYER_ALLOWED = False
FACT_WRITE_ALLOWED = False
NAVIGATION_ACTION_SPEECH_ALLOWED = False
EXTERNAL_NETWORK_ALLOWED = False
BIND_EXTERNAL_NETWORK_ALLOWED = False
LIVE_CAMERA_ALLOWED = False
LIVE_MICROPHONE_ALLOWED = False
DATASET_DOWNLOAD_ALLOWED = False
MODEL_WEIGHT_DOWNLOAD_ALLOWED = False
COMMERCIAL_RUNTIME_APPROVED = False
CANDIDATE_ONLY_BOUNDARY_DEFINED = True
TESTBOARD_REQUIRED_FOR_EACH_JOB = True

SERVICE_NAME = "model_test_lens_local_runner_bridge_v1"
SERVICE_VERSION = "skeleton_v1"

UI_HOST = "http://localhost:8765"
SERVICE_HOST = "http://127.0.0.1:8787"

ASSET_STORE_REL = "capabilities/test_assets/model_test_lens"
EVAL_OUT_REL = "_tmp_eval_out/model_test_lens_local_runner_bridge_v1"
JOBS_STORE_REL = "capabilities/midplatform/model_test_lens/local_runner_bridge/jobs"

JOB_LIFECYCLE_STATES: Tuple[str, ...] = (
    "created",
    "asset_registered",
    "awaiting_approval",
    "ready_to_run",
    "running",
    "adapter_processing",
    "completed",
    "completed_limited",
    "failed_no_boundary_violation",
    "blocked",
)

RUNNER_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {"runner_id": "segmentation_mobile_sam_runner", "runner_type": "segmentation_mobile_sam", "status": "skeleton_v1"},
    {"runner_id": "slam_video_limited_runner", "runner_type": "slam_video_limited", "status": "limited_placeholder_v1"},
    {"runner_id": "ocr_runner", "runner_type": "ocr_placeholder", "status": "placeholder"},
    {"runner_id": "tts_runner", "runner_type": "tts_placeholder", "status": "placeholder"},
    {"runner_id": "asr_runner", "runner_type": "asr_placeholder", "status": "placeholder"},
)

API_ENDPOINTS: Tuple[Dict[str, str], ...] = (
    {"method": "GET", "path": "/api/v1/capabilities"},
    {"method": "POST", "path": "/api/v1/assets/register"},
    {"method": "POST", "path": "/api/v1/jobs/create"},
    {"method": "POST", "path": "/api/v1/jobs/{job_id}/run"},
    {"method": "GET", "path": "/api/v1/jobs/{job_id}/status"},
    {"method": "GET", "path": "/api/v1/jobs/{job_id}/result"},
)

FORBIDDEN_CODE_PATTERNS: Tuple[Dict[str, str], ...] = (
    {"pattern_id": "bind_all_interfaces", "regex": r'host\s*=\s*["\']0\.0\.0\.0["\']|bind\s*0\.0\.0\.0'},
    {"pattern_id": "external_fetch", "regex": r'requests\.get\s*\(\s*["\']https?://|urllib\.request\.urlopen\s*\('},
    {"pattern_id": "camera_api", "regex": r"getUserMedia|MediaRecorder"},
    {"pattern_id": "registry_write", "regex": r"mutateRegistry\s*\(|registry.*\.write\s*\("},
    {"pattern_id": "fact_write", "regex": r"writeFact\s*\(|semantic_write\s*\("},
    {"pattern_id": "output_adapter_call", "regex": r"output_adapter_call\s*\("},
    {"pattern_id": "navigation_speech", "regex": r"triggerSpeech\s*\(|triggerNavigation\s*\("},
    {"pattern_id": "delete_testboard", "regex": r"removeTestBoard\s*\(|deleteArtifact\s*\("},
)

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"

UPSTREAM_RUNNER_BRIDGE_PLANNING_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-Service-Planning-v1-001"
)
UPSTREAM_UI_PATCH_REF = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Asset-Import-UI-Patch-Execution-And-Post-Review-v1-001"
)

NEXT_PHASE_UI_INTEGRATION = (
    "Phase-P1-Midplatform-Model-Test-Lens-Local-Runner-Bridge-UI-Service-Integration-Execution-And-Post-Review-v1-001"
)

TEST_BOARD_MODULE = "model_governance"
TEST_BOARD_TEST_MODE = "real_test"

PHASE_GOVERNANCE_RULES: Tuple[str, ...] = TEST_BOARD_GOVERNANCE_RULES + (
    "Local Runner Bridge skeleton is localhost-only.",
    "Local Runner Bridge skeleton is not runtime.",
    "Local Runner Bridge skeleton is not output adapter.",
    "Local Runner Bridge skeleton is not commercial backend.",
    "UI may submit jobs to Local Runner Bridge.",
    "Runner may execute models only as test jobs.",
    "Runner must write TestBoard.",
    "Adapter must generate MUEP envelope before UI display.",
    "Results are candidate-only.",
    "Results are not facts.",
    "Results are not runtime outputs.",
    "Results are not output adapter outputs.",
    "Results are not semantic outputs.",
    "Results must not trigger navigation/action/speech.",
    "Service must bind 127.0.0.1 only.",
    "Service must reject external host binding.",
    "Service must not access external URL.",
    "Service must not use live camera.",
    "Service must not use live microphone.",
    "Service must not mutate registry.",
    "Service must not download dataset.",
    "Service must not download model/weight.",
    "SLAM limited route without GT must not compute ATE.",
    "SLAM limited route must not fake trajectory or GT.",
    "Job lifecycle is required.",
    "Runner registry is required.",
    "API endpoints are required.",
    "TestBoard record is required.",
    "Test artifacts are protected.",
    "Test records are non-deletable.",
    "Cleanup must not delete TestBoard artifacts.",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = PHASE_GOVERNANCE_RULES
REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

EXTRA_TEST_BOARD_RECORD_TYPES: Tuple[str, ...] = (
    "local_runner_bridge_service_file_generation_record",
    "local_runner_bridge_api_endpoint_record",
    "local_runner_bridge_storage_job_store_record",
    "mobilesam_image_runner_skeleton_record",
    "slam_video_limited_runner_skeleton_record",
    "local_runner_bridge_testboard_write_record",
    "local_runner_bridge_boundary_audit_record",
    "local_runner_bridge_post_review_record",
    "followup_ui_service_integration_route_record",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_not_go", "go_key": "negative_guard_invalid_a_blocked", "depends_on": "upstream_planning_go_verified"},
    {"guard_id": "invalid_b_service_as_runtime", "go_key": "negative_guard_invalid_b_blocked", "depends_on": "not_runtime"},
    {"guard_id": "invalid_c_external_bind", "go_key": "negative_guard_invalid_c_blocked", "depends_on": "localhost_only_enforced"},
    {"guard_id": "invalid_d_external_url", "go_key": "negative_guard_invalid_d_blocked", "depends_on": "no_external_network"},
    {"guard_id": "invalid_e_camera_mic", "go_key": "negative_guard_invalid_e_blocked", "depends_on": "no_live_camera_mic"},
    {"guard_id": "invalid_f_registry", "go_key": "negative_guard_invalid_f_blocked", "depends_on": "no_registry_mutation"},
    {"guard_id": "invalid_g_fact_semantic", "go_key": "negative_guard_invalid_g_blocked", "depends_on": "no_fact_semantic"},
    {"guard_id": "invalid_h_output_adapter_nav", "go_key": "negative_guard_invalid_h_blocked", "depends_on": "not_output_adapter_nav_speech"},
    {"guard_id": "invalid_i_runner_no_testboard", "go_key": "negative_guard_invalid_i_blocked", "depends_on": "testboard_write_path_present"},
    {"guard_id": "invalid_j_adapter_required", "go_key": "negative_guard_invalid_j_blocked", "depends_on": "adapter_required"},
    {"guard_id": "invalid_k_slam_no_gt_ate", "go_key": "negative_guard_invalid_k_blocked", "depends_on": "slam_limited_no_ate"},
    {"guard_id": "invalid_l_slam_fake_trajectory", "go_key": "negative_guard_invalid_l_blocked", "depends_on": "slam_limited_no_fake_trajectory"},
    {"guard_id": "invalid_m_job_lifecycle", "go_key": "negative_guard_invalid_m_blocked", "depends_on": "job_lifecycle_defined"},
    {"guard_id": "invalid_n_runner_registry", "go_key": "negative_guard_invalid_n_blocked", "depends_on": "runner_registry_defined"},
    {"guard_id": "invalid_o_api_endpoints", "go_key": "negative_guard_invalid_o_blocked", "depends_on": "api_endpoints_present"},
    {"guard_id": "invalid_p_candidate_only", "go_key": "negative_guard_invalid_p_blocked", "depends_on": "candidate_only_boundary_defined"},
    {"guard_id": "invalid_q_testboard_protected", "go_key": "negative_guard_invalid_q_blocked", "depends_on": "test_artifact_protected"},
)

FINAL_DECISION_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_GO"
FINAL_DECISION_PARTIAL_GO = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_PARTIAL_GO"
FINAL_DECISION_FAILED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_FAILED_NO_BOUNDARY_VIOLATION"
FINAL_DECISION_BLOCKED = "P1_MIDPLATFORM_MODEL_TEST_LENS_LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION_BLOCKED"

REQUIRED_SERVICE_FILES: Tuple[str, ...] = (
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_server_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_api_handlers_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_service_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_storage_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_job_store_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/slam_video_limited_runner_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/adapters/mobilesam_runner_to_envelope_adapter_v1.py",
    "capabilities/midplatform/model_test_lens/local_runner_bridge/adapters/slam_limited_runner_to_envelope_adapter_v1.py",
)


@dataclass(frozen=True)
class P1LocalRunnerBridgeServiceSkeletonExecutionProfile:
    profile_ref: str
    phase_id: str
    real_execution_phase: bool
    localhost_only: bool
    bind_host: str
    bind_port: int
    not_runtime: bool
    not_output_adapter: bool
    service_may_execute_mobile_sam_image_runner: bool
    service_may_execute_slam_video_limited_runner: bool
    luna_core_principle: str
    governance_rules: Tuple[str, ...]


@dataclass
class NegativeLocalRunnerBridgeServiceSkeletonGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1LocalRunnerBridgeServiceSkeletonExecutionDecision:
    decision_ref: str
    local_runner_bridge_service_skeleton_execution_profile_count: int
    service_files_written: bool
    mobilesam_runner_wired: bool
    negative_guard_count: int
    negative_guard_passed: int
    blocker_count: int
    failure_recorded: bool
    final_decision: str


def to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
