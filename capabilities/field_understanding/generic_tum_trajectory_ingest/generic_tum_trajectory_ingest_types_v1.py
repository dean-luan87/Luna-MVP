# -*- coding: utf-8 -*-
"""Generic TUM Trajectory Ingest — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001"
SCOPE = "generic_tum_trajectory_ingest_v1"
SOURCE_CHAIN = "generic_tum_trajectory_ingest_v1"
INGEST_REF = "generic_tum_trajectory_ingest_v1"

INGEST_PRINCIPLE_ZH = (
    "第一个外部常见轨迹格式到 Luna Generic JSON Spatial Trace 的离线 ingest 样例。"
    "只处理离线 TUM trajectory fixture，不运行第三方 SLAM runtime。"
)

INPUT_FORMAT_REF = "generic_tum_trajectory"
TARGET_FORMAT_REF = "generic_json_spatial_trace"
GENERIC_JSON_PARSER_MODULE_REF = (
    "capabilities.field_understanding.generic_json_spatial_trace_parser."
    "generic_json_spatial_trace_parser_static_validators_v1"
)

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TUM_COLUMN_COUNT = 8

FINAL_DECISION_REVIEW_GO = "GENERIC_TUM_TRAJECTORY_TO_JSON_SPATIAL_TRACE_INGEST_REVIEW_GO"
FINAL_DECISION_REVIEW_BLOCKED = (
    "GENERIC_TUM_TRAJECTORY_TO_JSON_SPATIAL_TRACE_INGEST_REVIEW_BLOCKED"
)

EXPECTED_TUM_FIXTURE_LINE_COUNT = 3
EXPECTED_JSON_TRACE_ITEM_COUNT = 5
EXPECTED_POSE_ITEM_COUNT = 3
EXPECTED_MOTION_ITEM_COUNT = 2

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_ingest_only": True,
    "no_openvins_runtime": True,
    "no_orb_slam3_runtime": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_ros_runtime": True,
    "no_provider_runtime_activation": True,
    "runtime_activation_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
    "no_commercial_runtime_approval": True,
}
