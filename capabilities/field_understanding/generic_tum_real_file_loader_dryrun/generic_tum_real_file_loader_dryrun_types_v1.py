# -*- coding: utf-8 -*-
"""Generic TUM Real File Loader DryRun — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001"
SCOPE = "generic_tum_real_file_loader_dryrun_v1"
SOURCE_CHAIN = "generic_tum_real_file_loader_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "用本地真实 TUM 格式文件完成第一次外部真实导出文件读取、校验、转换、Parser replay：将本地受控目录下 "
    "真实 TUM trajectory 文件读取、校验并转换为 Luna Generic JSON Spatial Trace，再复用 Generic JSON "
    "Spatial Trace Parser 进入 spatial_evidence_candidate_bundle。允许离线转换执行，不接 RTAB / ROS / "
    "live sensor，不启动 live runtime。"
)

EXPORT_LOADER_PLANNING_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Export-Loader-Planning-v1-001"
)
GENERIC_TUM_INGEST_REF = "Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001"
GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
REAL_FILE_REPLAY_DRYRUN_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-DryRun-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
SOURCE_FORMAT = "tum_trajectory_file"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"

RUNTIME_TRIAL_MODE = "tum_real_file_loader_dryrun_only"

TUM_COLUMN_COUNT = 8
POSE_CONFIDENCE = 0.9

FINAL_DECISION_GO = "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "GENERIC_TUM_REAL_FILE_LOADER_DRYRUN_BLOCKED"

NEXT_PHASE_REF = "Phase-RTAB-Map-Trajectory-Real-File-Loader-Planning-v1-001"

SAMPLES_REL_DIR = (
    "capabilities/field_understanding/generic_tum_real_file_loader_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_tum_valid_trajectory.txt",
    "sample_tum_valid_with_comments.txt",
    "invalid_tum_bad_column_count.txt",
    "invalid_tum_zero_quaternion.txt",
    "invalid_tum_missing_source_chain_policy.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "tum_valid_file_to_pose_motion_json_trace",
    "tum_valid_file_with_comments_and_empty_lines",
    "tum_file_to_field_task_guidance_replay_path",
    "tum_file_origin_and_source_chain_preserved",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_bad_column_count_rejected",
    "invalid_zero_quaternion_rejected",
    "invalid_missing_source_chain_rejected",
    "invalid_direct_candidate_bundle_bypass_rejected",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "GenericTUMRealFileLoaderDryRunCase",
    "TUMRealFileInputBundle",
    "TUMFileSourceAdmissionResult",
    "TUMTrajectoryRowParseResult",
    "TUMToJSONSpatialTraceConversionResult",
    "TUMRealFileReplayResult",
    "TUMRealFileLoaderDryRunTrace",
    "TUMRealFileLoaderDryRunReviewDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "tum_real_file_loader_dryrun_is_not_live_runtime",
    "local_file_read_only_under_controlled_samples_directory",
    "file_source_admission_must_run_before_row_parsing",
    "tum_row_must_have_exactly_eight_numeric_columns",
    "quaternion_must_be_valid_and_not_all_zero",
    "conversion_output_must_be_generic_json_spatial_trace",
    "generic_json_spatial_trace_parser_must_be_reused",
    "converted_json_trace_must_preserve_file_origin_and_source_chain",
    "motion_candidate_only_from_consecutive_valid_pose_rows",
    "backend_native_output_must_not_enter_field_synthesis_directly",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "tum_real_file_loader_dryrun_only": True,
    "real_file_conversion_execution_allowed": True,
    "real_file_replay_execution_allowed": True,
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
class GenericTUMRealFileLoaderDryRunCase:
    case_ref: str
    case_kind: str
    sample_file: str
    expected_outcome: str
    source_chain: str


@dataclass(frozen=True)
class TUMRealFileInputBundle:
    bundle_ref: str
    sample_file: str
    source_format: str
    file_origin: Dict[str, Any]
    source_chain_prefix: Tuple[str, ...]
    raw_line_count: int
    source_chain: str


@dataclass(frozen=True)
class TUMFileSourceAdmissionResult:
    result_ref: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    file_origin_metadata_present: bool
    source_chain_present: bool
    source_format_ok: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class TUMTrajectoryRowParseResult:
    result_ref: str
    valid_row_count: int
    skipped_line_count: int
    hard_error_count: int
    parse_errors: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class TUMToJSONSpatialTraceConversionResult:
    result_ref: str
    conversion_ok: bool
    json_trace_item_count: int
    pose_item_count: int
    motion_item_count: int
    target_internal_format: str
    file_origin_preserved: bool
    source_chain_preserved: bool
    conversion_issues: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class TUMRealFileReplayResult:
    result_ref: str
    generic_json_parser_reused: bool
    parsed_count: int
    candidate_bundle_mapping_ok: bool
    output_candidate_types: Tuple[str, ...]
    bundle_issues: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class TUMRealFileLoaderDryRunTrace:
    trace_ref: str
    replay_path: str
    candidate_only: bool
    candidate_refs: Tuple[str, ...]
    guidance_candidate_is_not_runtime_navigation: bool
    runtime_navigation_started: bool
    field_entrypoint: str
    source_chain: str


@dataclass(frozen=True)
class TUMRealFileLoaderDryRunReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    export_loader_planning_go_verified: bool
    generic_tum_ingest_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_conversion_execution_allowed: bool = True
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
