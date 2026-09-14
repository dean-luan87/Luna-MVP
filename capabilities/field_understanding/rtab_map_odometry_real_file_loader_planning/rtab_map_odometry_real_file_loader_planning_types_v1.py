# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Real File Loader Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RTAB-Map-Odometry-Real-File-Loader-Planning-v1-001"
SCOPE = "rtab_map_odometry_real_file_loader_planning_review_only"
SOURCE_CHAIN = "rtab_map_odometry_real_file_loader_planning_v1"

LOADER_PLANNING_PRINCIPLE_ZH = (
    "定义 RTAB-Map odometry export real file loader 的规划基线：将 RTAB-Map odometry export 文件规划"
    "转换为 Luna Generic JSON Spatial Trace，并支持 pose / motion / health candidate。重点验证 "
    "tracking_state / odometry_quality / lost / degraded 等状态如何映射为 Luna health candidate。"
    "本阶段只做 Planning + Matrix Review，不执行真实转换，不读取 RTAB database，不接 ROS topic，"
    "不启动 RTAB live runtime。"
)

RTAB_ODOMETRY_FIXTURE_REF = (
    "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
RTAB_TRAJECTORY_LOADER_DRYRUN_REF = (
    "Phase-RTAB-Map-Trajectory-Real-File-Loader-DryRun-v1-001"
)
RTAB_TRAJECTORY_LOADER_PLANNING_REF = (
    "Phase-RTAB-Map-Trajectory-Real-File-Loader-Planning-v1-001"
)
EXPORT_LOADER_PLANNING_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Export-Loader-Planning-v1-001"
)
GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
REAL_FILE_REPLAY_DRYRUN_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001"
)
TUM_REAL_FILE_LOADER_DRYRUN_REF = "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001"
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
SOURCE_FORMAT = "rtab_map_odometry_export_file"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"

RUNTIME_TRIAL_MODE = "rtab_odometry_real_file_loader_planning_only"

FINAL_DECISION_GO = "RTAB_MAP_ODOMETRY_REAL_FILE_LOADER_PLANNING_GO"
FINAL_DECISION_BLOCKED = "RTAB_MAP_ODOMETRY_REAL_FILE_LOADER_PLANNING_BLOCKED"

NEXT_PHASE_REF = "Phase-RTAB-Map-Odometry-Real-File-Loader-DryRun-v1-001"

PIPELINE_STAGES: Tuple[str, ...] = (
    "rtab_map_odometry_export_file",
    "format_admission",
    "rtab_odometry_to_json_trace_converter_planning",
    "pose_motion_health_candidate_planning",
    "generic_json_spatial_trace",
    "generic_json_spatial_trace_parser",
    "spatial_evidence_candidate_bundle",
    "field_task_guidance_candidate_replay_path",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RTABMapOdometryRealFileLoaderPlanningProfile",
    "RTABMapOdometryExportFilePolicy",
    "RTABMapOdometryFormatAdmissionPolicy",
    "RTABMapOdometryToJSONTraceMappingPolicy",
    "RTABMapOdometryHealthMappingPolicy",
    "RTABMapOdometryLoaderBoundaryPolicy",
    "RTABMapOdometryLoaderScenarioPolicy",
    "RTABMapOdometryLoaderSafetyPolicy",
    "RTABMapOdometryRealFileLoaderPlanningDecision",
)

RECORD_REQUIRED_FIELDS: Tuple[str, ...] = (
    "node_id",
    "timestamp",
    "pose_translation_xyz",
    "pose_orientation_quaternion",
    "confidence",
    "tracking_state",
    "source_chain",
    "file_origin",
)

FIELD_ALIASES: Dict[str, Tuple[str, ...]] = {
    "x": ("x", "tx"),
    "y": ("y", "ty"),
    "z": ("z", "tz"),
    "timestamp": ("timestamp", "timestamp_ms", "stamp", "time", "timestamp_sec"),
    "node_id": ("node_id", "id", "vertex_id"),
    "tracking_state": ("tracking_state", "tracking_status", "state", "odom_state"),
    "odometry_quality": ("odometry_quality", "quality", "odom_quality"),
}

HEALTH_STATUS_OK_STATES: Tuple[str, ...] = ("ok", "good", "tracked")
HEALTH_STATUS_DEGRADED_STATES: Tuple[str, ...] = ("degraded", "weak", "low_confidence")
HEALTH_STATUS_LOST_STATES: Tuple[str, ...] = ("lost", "failed", "not_tracked")

HEALTH_SEVERITY_BY_STATUS: Dict[str, str] = {
    "ok": "none",
    "degraded": "warning",
    "lost": "critical",
}

ODOMETRY_QUALITY_DEGRADED_THRESHOLD = 0.5

LOADER_SCENARIO_REFS: Tuple[str, ...] = (
    "rtab_odometry_basic_pose_motion_health_loader_planning",
    "rtab_odometry_health_degraded_mapping_planning",
    "rtab_odometry_lost_tracking_mapping_planning",
    "rtab_odometry_alias_field_compatibility_planning",
    "rtab_odometry_to_replay_path_planning",
    "invalid_or_unsafe_rtab_odometry_export_blocked",
)

LOADER_SCENARIO_GO_KEYS: Tuple[str, ...] = (
    "rtab_odometry_basic_pose_motion_health_loader_planning_supported",
    "rtab_odometry_health_degraded_mapping_supported",
    "rtab_odometry_lost_tracking_mapping_supported",
    "rtab_odometry_alias_field_compatibility_supported",
    "rtab_odometry_to_replay_path_supported",
    "invalid_or_unsafe_rtab_odometry_export_blocked",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    RTAB_ODOMETRY_FIXTURE_REF,
    RTAB_TRAJECTORY_LOADER_DRYRUN_REF,
    RTAB_TRAJECTORY_LOADER_PLANNING_REF,
    EXPORT_LOADER_PLANNING_REF,
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    REAL_FILE_REPLAY_DRYRUN_REF,
    TUM_REAL_FILE_LOADER_DRYRUN_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
)

LOADER_PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "rtab_odometry_real_file_loader_planning_is_not_conversion_execution",
    "rtab_odometry_export_file_must_pass_format_admission_before_conversion",
    "rtab_database_read_is_prohibited",
    "ros_topic_or_live_rtab_runtime_is_prohibited",
    "each_record_must_include_node_id_timestamp_pose_confidence_tracking_state_source_chain_file_origin",
    "quaternion_must_be_valid_and_not_all_zero",
    "conversion_output_must_be_generic_json_spatial_trace",
    "generic_json_spatial_trace_parser_must_remain_entry_validator",
    "backend_native_rtab_odometry_object_must_not_enter_field_synthesis_directly",
    "motion_candidate_only_from_consecutive_valid_records",
    "health_candidate_must_remain_candidate_only",
    "health_degraded_lost_must_not_directly_trigger_action_speech_navigation_shutdown_fact_write",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "conversion_execution",
    "runtime_activation",
    "rtab_database_read",
    "ros_topic_read",
    "live_rtab_runtime",
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "real_navigation",
    "runtime_shutdown_from_health",
    "live_sensor_trigger",
    "live_camera",
    "live_imu",
    "live_gps_gnss",
    "real_map_api",
    "backend_native_direct_to_field_synthesis",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "rtab_odometry_real_file_loader_planning_only": True,
    "real_file_conversion_execution_allowed": False,
    "real_file_replay_execution_allowed": False,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "live_sensor_connected": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class RTABMapOdometryRealFileLoaderPlanningProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    rtab_trajectory_real_file_loader_dryrun_ref: str
    rtab_odometry_fixture_ref: str
    source_format: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    pipeline_stages: Tuple[str, ...]
    loader_scenario_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RTABMapOdometryExportFilePolicy:
    policy_ref: str
    source_format: str
    source_zh: str
    priority: str
    record_required_fields: Tuple[str, ...]
    field_aliases: Dict[str, Tuple[str, ...]]
    output_candidate_types: Tuple[str, ...]
    target_converter: str
    prohibited_operations: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    requires_format_admission: bool
    requires_file_origin_metadata: bool
    requires_source_chain: bool
    requires_tracking_state: bool
    source_chain: str
    supported: bool = True


@dataclass(frozen=True)
class RTABMapOdometryFormatAdmissionPolicy:
    policy_ref: str
    format_admission_required: bool
    node_id_required: bool
    timestamp_required: bool
    pose_required: bool
    confidence_required: bool
    tracking_state_required: bool
    source_chain_required: bool
    file_origin_metadata_required: bool
    quaternion_validation_required: bool
    rtab_database_read_blocked: bool
    ros_topic_blocked: bool
    live_rtab_runtime_blocked: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMapOdometryToJSONTraceMappingPolicy:
    policy_ref: str
    target_internal_format: str
    generic_json_output_required: bool
    generic_json_parser_required: bool
    parser_ref: str
    target_entrypoint: str
    pose_trace_id_template: str
    motion_trace_id_template: str
    health_trace_id_template: str
    motion_generated_only_from_consecutive_records: bool
    field_aliases: Dict[str, Tuple[str, ...]]
    source_chain: str


@dataclass(frozen=True)
class RTABMapOdometryHealthMappingPolicy:
    policy_ref: str
    health_candidate_mapping_required: bool
    health_candidate_candidate_only: bool
    provider: str
    ok_states: Tuple[str, ...]
    degraded_states: Tuple[str, ...]
    lost_states: Tuple[str, ...]
    severity_by_status: Dict[str, str]
    odometry_quality_degraded_threshold: float
    degraded_health_does_not_directly_block_or_allow_action: bool
    lost_health_does_not_trigger_runtime_shutdown: bool
    health_does_not_trigger_speech_navigation_fact_write: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMapOdometryLoaderBoundaryPolicy:
    policy_ref: str
    backend_native_output_direct_to_field_blocked: bool
    conversion_execution_allowed: bool
    parser_must_remain_entry_validator: bool
    parser_ref: str
    target_entrypoint: str
    source_chain: str


@dataclass(frozen=True)
class RTABMapOdometryLoaderScenarioPolicy:
    scenario_ref: str
    input_description: str
    output_planning_target: str
    scenario_requirements: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    allowed_next_step: str
    source_chain: str
    supported: bool = True
    blocked_scenario: bool = False


@dataclass(frozen=True)
class RTABMapOdometryLoaderSafetyPolicy:
    policy_ref: str
    rtab_database_read_blocked: bool
    ros_topic_blocked: bool
    live_rtab_runtime_blocked: bool
    backend_native_direct_to_field_blocked: bool
    health_candidate_candidate_only: bool
    degraded_health_does_not_directly_block_or_allow_action: bool
    lost_health_does_not_trigger_runtime_shutdown: bool
    health_does_not_trigger_speech_navigation_fact_write: bool
    field_task_guidance_replay_candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMapOdometryRealFileLoaderPlanningDecision:
    decision_ref: str
    profile_ref: str
    planning_profile_count: int
    rtab_odometry_export_file_policy_count: int
    health_mapping_policy_count: int
    loader_scenario_count: int
    rtab_trajectory_real_file_loader_dryrun_go_verified: bool
    rtab_odometry_fixture_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_conversion_execution_allowed: bool = False
    real_file_replay_execution_allowed: bool = False
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
