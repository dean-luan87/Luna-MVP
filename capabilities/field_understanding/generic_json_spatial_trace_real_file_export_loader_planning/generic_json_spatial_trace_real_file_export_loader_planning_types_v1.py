# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Real File Export Loader Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Generic-JSON-Spatial-Trace-Real-File-Export-Loader-Planning-v1-001"
SCOPE = "generic_json_spatial_trace_real_file_export_loader_planning_review_only"
SOURCE_CHAIN = "generic_json_spatial_trace_real_file_export_loader_planning_v1"

LOADER_PLANNING_PRINCIPLE_ZH = (
    "定义真实导出文件 loader / converter 的规划基线：将 TUM trajectory、RTAB-Map trajectory "
    "export、RTAB-Map odometry export、RTAB-Map graph export 等真实离线文件，规划转换为 "
    "Luna Generic JSON Spatial Trace，再进入已封口的 real file controlled replay dry-run 路径。"
    "本阶段仅 planning + matrix review，不执行真实转换，不启动 live runtime。"
)

GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
TUM_TRAJECTORY_INGEST_REF = "Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001"
RTAB_TRAJECTORY_EXPORT_FIXTURE_REF = (
    "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
RTAB_ODOMETRY_EXPORT_FIXTURE_REF = (
    "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
RTAB_GRAPH_EXPORT_FIXTURE_REF = (
    "Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
)
REAL_FILE_REPLAY_PLANNING_REF = (
    "Phase-Generic-JSON-Spatial-Trace-Real-File-Controlled-Replay-Planning-v1-001"
)
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
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"

RUNTIME_TRIAL_MODE = "real_file_export_loader_planning_only"

FINAL_DECISION_GO = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_EXPORT_LOADER_PLANNING_GO"
FINAL_DECISION_BLOCKED = "GENERIC_JSON_SPATIAL_TRACE_REAL_FILE_EXPORT_LOADER_PLANNING_BLOCKED"

NEXT_PHASE_REF = "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001"

PIPELINE_STAGES: Tuple[str, ...] = (
    "external_export_file",
    "format_admission",
    "export_to_json_trace_converter_planning",
    "generic_json_spatial_trace",
    "generic_json_spatial_trace_parser",
    "real_file_controlled_replay_dryrun_path",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RealFileExportLoaderPlanningProfile",
    "ExternalExportFileSourcePolicy",
    "ExternalExportFormatAdmissionPolicy",
    "ExternalExportToJSONTraceMappingPolicy",
    "ExternalExportLoaderBoundaryPolicy",
    "ExternalExportLoaderScenarioPolicy",
    "ExternalExportLoaderSafetyPolicy",
    "ExternalExportLoaderPlanningDecision",
)

EXPORT_FILE_SOURCE_REFS: Tuple[str, ...] = (
    "tum_trajectory_file",
    "rtab_map_trajectory_export_file",
    "rtab_map_odometry_export_file",
    "rtab_map_graph_export_file",
    "luna_generic_json_spatial_trace_file",
)

EXPORT_FILE_SOURCE_GO_KEYS: Tuple[str, ...] = (
    "tum_trajectory_file_supported",
    "rtab_trajectory_export_file_supported",
    "rtab_odometry_export_file_supported",
    "rtab_graph_export_file_supported",
    "luna_generic_json_spatial_trace_file_supported",
)

LOADER_SCENARIO_REFS: Tuple[str, ...] = (
    "tum_file_loader_to_json_trace_planning",
    "rtab_trajectory_file_loader_to_json_trace_planning",
    "rtab_odometry_file_loader_to_json_trace_planning",
    "rtab_graph_file_loader_to_json_trace_planning",
    "generic_json_trace_passthrough_loader_planning",
    "invalid_or_unsafe_export_file_blocked",
)

LOADER_SCENARIO_GO_KEYS: Tuple[str, ...] = (
    "tum_file_loader_to_json_trace_planning_supported",
    "rtab_trajectory_loader_to_json_trace_planning_supported",
    "rtab_odometry_loader_to_json_trace_planning_supported",
    "rtab_graph_loader_to_json_trace_planning_supported",
    "generic_json_trace_passthrough_loader_supported",
    "invalid_or_unsafe_export_file_blocked",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    GENERIC_JSON_SPATIAL_TRACE_PARSER_REF,
    TUM_TRAJECTORY_INGEST_REF,
    RTAB_TRAJECTORY_EXPORT_FIXTURE_REF,
    RTAB_ODOMETRY_EXPORT_FIXTURE_REF,
    RTAB_GRAPH_EXPORT_FIXTURE_REF,
    REAL_FILE_REPLAY_PLANNING_REF,
    REAL_FILE_REPLAY_DRYRUN_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
)

LOADER_PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "export_loader_planning_is_not_conversion_execution",
    "export_loader_planning_is_not_live_runtime",
    "external_export_file_must_pass_format_admission_before_conversion",
    "conversion_output_must_be_generic_json_spatial_trace",
    "generic_json_spatial_trace_parser_must_remain_entry_validator",
    "backend_native_file_must_not_enter_field_synthesis_directly",
    "file_origin_metadata_and_source_chain_must_be_preserved",
    "tum_quaternion_must_be_validated",
    "rtab_node_id_timestamp_source_chain_required_where_applicable",
    "rtab_graph_loop_closure_must_not_restore_runtime_trust",
    "gps_gnss_hint_must_not_override_field_identity",
    "no_live_sensor_no_ros_no_camera_no_imu_no_real_gps_no_map_api",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "conversion_execution",
    "runtime_activation",
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "real_navigation",
    "live_sensor_trigger",
    "ros_topic_read",
    "rtab_database_read",
    "live_rtab_runtime",
    "live_camera",
    "live_imu",
    "live_gps_gnss",
    "real_map_api",
    "backend_native_direct_to_field_synthesis",
    "map_fact_write",
    "relocalization_runtime_trust_restore",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "real_file_export_loader_planning_only": True,
    "real_file_conversion_execution_allowed": False,
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
class RealFileExportLoaderPlanningProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    real_file_replay_dryrun_ref: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    pipeline_stages: Tuple[str, ...]
    export_file_source_refs: Tuple[str, ...]
    loader_scenario_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ExternalExportFileSourcePolicy:
    source_ref: str
    source_format: str
    source_zh: str
    priority: str
    expected_fields: Tuple[str, ...]
    output_candidate_types: Tuple[str, ...]
    target_converter: str
    prohibited_operations: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    requires_format_admission: bool
    requires_file_origin_metadata: bool
    requires_source_chain: bool
    source_chain: str
    supported: bool = True


@dataclass(frozen=True)
class ExternalExportFormatAdmissionPolicy:
    policy_ref: str
    format_admission_required: bool
    file_origin_metadata_required: bool
    source_chain_required: bool
    unsupported_candidate_type_rejected: bool
    missing_source_chain_rejected: bool
    tum_quaternion_validation_required: bool
    rtab_node_id_required: bool
    source_chain: str


@dataclass(frozen=True)
class ExternalExportToJSONTraceMappingPolicy:
    policy_ref: str
    target_internal_format: str
    generic_json_output_required: bool
    generic_json_parser_required: bool
    parser_ref: str
    target_entrypoint: str
    source_chain: str


@dataclass(frozen=True)
class ExternalExportLoaderBoundaryPolicy:
    policy_ref: str
    backend_native_output_direct_to_field_blocked: bool
    conversion_execution_allowed: bool
    parser_must_remain_entry_validator: bool
    parser_ref: str
    target_entrypoint: str
    source_chain: str


@dataclass(frozen=True)
class ExternalExportLoaderScenarioPolicy:
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
class ExternalExportLoaderSafetyPolicy:
    policy_ref: str
    rtab_loop_closure_does_not_restore_runtime_trust: bool
    gps_does_not_override_field_identity: bool
    tracking_state_degraded_health_candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class ExternalExportLoaderPlanningDecision:
    decision_ref: str
    profile_ref: str
    planning_profile_count: int
    export_file_source_policy_count: int
    loader_scenario_count: int
    controlled_trial_governance_template_ref_ok: bool
    real_file_replay_dryrun_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    final_decision: str
    real_file_conversion_execution_allowed: bool = False
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
