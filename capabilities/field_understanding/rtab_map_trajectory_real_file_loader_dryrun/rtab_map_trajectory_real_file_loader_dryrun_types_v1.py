# -*- coding: utf-8 -*-
"""RTAB-Map Trajectory Real File Loader DryRun — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RTAB-Map-Trajectory-Real-File-Loader-DryRun-v1-001"
SCOPE = "rtab_map_trajectory_real_file_loader_dryrun_v1"
SOURCE_CHAIN = "rtab_map_trajectory_real_file_loader_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "执行 RTAB-Map trajectory export real file loader dry-run：将本地受控 RTAB trajectory export "
    "样例文件读取、字段准入、别名归一、转换为 Luna Generic JSON Spatial Trace，并复用 Generic JSON "
    "Spatial Trace Parser 进入 spatial_evidence_candidate_bundle。允许离线转换执行，不读 RTAB "
    "database，不接 ROS，不启动 RTAB live runtime。"
)

RTAB_TRAJECTORY_LOADER_PLANNING_REF = (
    "Phase-RTAB-Map-Trajectory-Real-File-Loader-Planning-v1-001"
)
RTAB_TRAJECTORY_FIXTURE_REF = (
    "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
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
SOURCE_FORMAT = "rtab_map_trajectory_export_file"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"

RUNTIME_TRIAL_MODE = "rtab_trajectory_real_file_loader_dryrun_only"

NODE_ID_ALIASES: Tuple[str, ...] = ("node_id", "id", "vertex_id")
TIMESTAMP_MS_ALIASES: Tuple[str, ...] = ("timestamp_ms",)
TIMESTAMP_SEC_ALIASES: Tuple[str, ...] = ("timestamp", "timestamp_sec", "stamp", "time")
TRANSLATION_ALIASES: Dict[str, Tuple[str, ...]] = {
    "x": ("x", "tx"),
    "y": ("y", "ty"),
    "z": ("z", "tz"),
}
ORIENTATION_FIELDS: Tuple[str, ...] = ("qx", "qy", "qz", "qw")

PROHIBITED_FILE_FLAGS: Tuple[str, ...] = (
    "direct_field_synthesis_write",
    "rtab_db_read",
    "ros_topic_read",
    "live_rtab_runtime",
)

FINAL_DECISION_GO = "RTAB_MAP_TRAJECTORY_REAL_FILE_LOADER_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RTAB_MAP_TRAJECTORY_REAL_FILE_LOADER_DRYRUN_BLOCKED"

NEXT_PHASE_REF = "Phase-RTAB-Map-Odometry-Real-File-Loader-Planning-v1-001"

SAMPLES_REL_DIR = (
    "capabilities/field_understanding/rtab_map_trajectory_real_file_loader_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_rtab_trajectory_valid.json",
    "sample_rtab_trajectory_alias_fields.json",
    "sample_rtab_trajectory_with_metadata.json",
    "invalid_rtab_trajectory_missing_node_id.json",
    "invalid_rtab_trajectory_zero_quaternion.json",
    "invalid_rtab_trajectory_missing_source_chain.json",
    "invalid_rtab_trajectory_native_rtab_object.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "rtab_trajectory_valid_file_to_pose_motion_json_trace",
    "rtab_trajectory_alias_fields_to_standard_trace",
    "rtab_trajectory_metadata_and_source_chain_preserved",
    "rtab_trajectory_to_field_task_guidance_replay_path",
    "rtab_trajectory_motion_only_from_consecutive_valid_records",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_node_id_rejected",
    "invalid_zero_quaternion_rejected",
    "invalid_missing_source_chain_rejected",
    "invalid_direct_field_synthesis_write_rejected",
    "invalid_rtab_db_ros_live_runtime_rejected",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RTABMapTrajectoryRealFileLoaderDryRunCase",
    "RTABTrajectoryRealFileInputBundle",
    "RTABTrajectoryFileSourceAdmissionResult",
    "RTABTrajectoryRecordParseResult",
    "RTABTrajectoryToJSONSpatialTraceConversionResult",
    "RTABTrajectoryRealFileReplayResult",
    "RTABTrajectoryRealFileLoaderDryRunTrace",
    "RTABTrajectoryRealFileLoaderDryRunReviewDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "rtab_trajectory_real_file_loader_dryrun_is_not_live_runtime",
    "local_file_read_only_under_controlled_samples_directory",
    "file_source_admission_must_run_before_record_parsing",
    "record_must_include_node_id_timestamp_pose_confidence_source_chain_file_origin",
    "field_aliases_must_normalize_before_conversion",
    "quaternion_must_be_valid_and_not_all_zero",
    "conversion_output_must_be_generic_json_spatial_trace",
    "generic_json_spatial_trace_parser_must_be_reused",
    "converted_json_trace_must_preserve_file_origin_export_session_id_node_id_source_chain",
    "motion_candidate_only_from_consecutive_valid_records",
    "backend_native_rtab_object_must_not_enter_field_synthesis_directly",
    "rtab_database_read_ros_topic_live_rtab_runtime_prohibited",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "rtab_trajectory_real_file_loader_dryrun_only": True,
    "real_file_conversion_execution_allowed": True,
    "real_file_replay_execution_allowed": True,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "live_sensor_connected": False,
    "rtab_database_read_allowed": False,
    "ros_connected": False,
    "live_rtab_runtime_started": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class RTABMapTrajectoryRealFileLoaderDryRunCase:
    case_ref: str
    case_kind: str
    sample_file: str
    expected_outcome: str
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryRealFileInputBundle:
    bundle_ref: str
    sample_file: str
    source_format: str
    export_session_id: str
    file_origin: Dict[str, Any]
    source_chain_prefix: Tuple[str, ...]
    raw_record_count: int
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryFileSourceAdmissionResult:
    result_ref: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    format_ref_ok: bool
    file_origin_metadata_present: bool
    source_chain_present: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryRecordParseResult:
    result_ref: str
    valid_record_count: int
    rejected_record_count: int
    alias_field_mapping_used: bool
    parse_errors: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryToJSONSpatialTraceConversionResult:
    result_ref: str
    conversion_ok: bool
    json_trace_item_count: int
    pose_item_count: int
    motion_item_count: int
    target_internal_format: str
    file_origin_preserved: bool
    export_session_id_preserved: bool
    source_chain_preserved: bool
    motion_generated_only_from_consecutive_records: bool
    conversion_issues: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryRealFileReplayResult:
    result_ref: str
    generic_json_parser_reused: bool
    parsed_count: int
    candidate_bundle_mapping_ok: bool
    output_candidate_types: Tuple[str, ...]
    bundle_issues: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryRealFileLoaderDryRunTrace:
    trace_ref: str
    replay_path: str
    candidate_only: bool
    candidate_refs: Tuple[str, ...]
    guidance_candidate_is_not_runtime_navigation: bool
    direct_field_synthesis_write: bool
    runtime_navigation_started: bool
    field_entrypoint: str
    source_chain: str


@dataclass(frozen=True)
class RTABTrajectoryRealFileLoaderDryRunReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    rtab_trajectory_loader_planning_go_verified: bool
    rtab_trajectory_fixture_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    generic_tum_real_file_loader_dryrun_go_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_conversion_execution_allowed: bool = True
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
