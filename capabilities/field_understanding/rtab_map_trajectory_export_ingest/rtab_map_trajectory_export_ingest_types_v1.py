# -*- coding: utf-8 -*-
"""RTAB-Map Trajectory Export Ingest — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
SCOPE = "rtab_map_trajectory_export_ingest_fixture_only"
SOURCE_CHAIN = "rtab_map_trajectory_export_ingest_v1"
INGEST_REF = "rtab_map_trajectory_export_ingest_v1"

INGEST_PRINCIPLE_ZH = (
    "Interface Layer Governance Protocol 下的 RTAB-Map trajectory_export_subset "
    "最小 fixture 转换样例。不运行 RTAB-Map、不读 database、不接 ROS。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
SOURCE_INTERFACE_PROFILE = "spatial_evidence_ingest_interface"
INTERNAL_STANDARD_FORMAT = "generic_json_spatial_trace"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
TARGET_ENTRYPOINT = "field_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

INPUT_EXPORT_KIND = "trajectory_export_subset"
INPUT_FORMAT_REF = "rtab_map_trajectory_export_subset"
TARGET_FORMAT_REF = INTERNAL_STANDARD_FORMAT
GENERIC_JSON_PARSER_MODULE_REF = (
    "capabilities.field_understanding.generic_json_spatial_trace_parser."
    "generic_json_spatial_trace_parser_static_validators_v1"
)

FINAL_DECISION_REVIEW_GO = (
    "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO"
)
FINAL_DECISION_REVIEW_BLOCKED = (
    "RTAB_MAP_TRAJECTORY_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_BLOCKED"
)

EXPECTED_TRAJECTORY_FIXTURE_COUNT = 3
EXPECTED_JSON_TRACE_ITEM_COUNT = 5
EXPECTED_POSE_ITEM_COUNT = 3
EXPECTED_MOTION_ITEM_COUNT = 2

TRAJECTORY_RECORD_REQUIRED_FIELDS: Tuple[str, ...] = (
    "node_id",
    "timestamp_ms",
    "tx",
    "ty",
    "tz",
    "qx",
    "qy",
    "qz",
    "qw",
    "confidence",
    "source_chain",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_fixture_ingest_only": True,
    "no_rtabmap_runtime": True,
    "no_rtabmap_database_read": True,
    "no_ros_runtime": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_pointcloud_large_object": True,
    "no_long_term_map_write": True,
    "no_provider_runtime_activation": True,
    "runtime_activation_allowed": False,
    "commercial_runtime_approved": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
    "no_rtabmap_private_ingest_entrypoint": True,
    "no_interface_layer_bypass": True,
    "no_generic_json_spatial_trace_bypass": True,
    "no_field_synthesis_v1_bypass": True,
}
