# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Parser — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
SCOPE = "generic_json_spatial_trace_parser_v1"
SOURCE_CHAIN = "generic_json_spatial_trace_parser_v1"
PARSER_REF = "generic_json_spatial_trace_parser_v1"

PARSER_PRINCIPLE_ZH = (
    "Luna 第一版空间证据离线输入标准 parser。解析 Generic JSON Spatial Trace 为 "
    "spatial_evidence_candidate_bundle，不运行第三方 SLAM runtime。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
INPUT_FORMAT_REF = "generic_json_spatial_trace"

FINAL_DECISION_REVIEW_GO = "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_GO"
FINAL_DECISION_REVIEW_BLOCKED = "GENERIC_JSON_SPATIAL_TRACE_PARSER_REVIEW_BLOCKED"

REQUIRED_CANDIDATE_TYPE_SLUGS: Tuple[str, ...] = (
    "pose",
    "motion",
    "anchor",
    "local_map",
    "health",
    "drift",
    "relocalization",
)

OPTIONAL_RESERVED_CANDIDATE_TYPE_SLUGS: Tuple[str, ...] = (
    "field_graph",
    "semantic_placeholders",
)

ALLOWED_CANDIDATE_TYPE_SLUGS: Tuple[str, ...] = (
    REQUIRED_CANDIDATE_TYPE_SLUGS + OPTIONAL_RESERVED_CANDIDATE_TYPE_SLUGS
)

CANDIDATE_SLUG_TO_LUNA_TYPE: Dict[str, str] = {
    "pose": "PoseCandidate",
    "motion": "MotionCandidate",
    "anchor": "SpatialAnchorCandidate",
    "local_map": "LocalMapCandidate",
    "health": "SLAMHealthCandidate",
    "drift": "MapDriftCandidate",
    "relocalization": "RelocalizationCandidate",
    "field_graph": "FieldGraphCandidate",
    "semantic_placeholders": "SemanticFieldObjectCandidate",
}

LUNA_CANDIDATE_BUNDLE_KEYS: Tuple[str, ...] = (
    "pose_candidates",
    "motion_candidates",
    "spatial_anchor_candidates",
    "local_map_candidates",
    "slam_health_candidates",
    "map_drift_candidates",
    "relocalization_candidates",
    "field_graph_candidates",
    "semantic_field_object_candidates",
)

TRACE_ITEM_REQUIRED_FIELDS: Tuple[str, ...] = (
    "trace_id",
    "source_chain",
    "confidence",
    "candidate_type",
    "field_synthesis_entrypoint",
)

PARSED_TRACE_FIELDS: Tuple[str, ...] = (
    "parsed_ref",
    "trace_id",
    "source_chain",
    "time_ref",
    "confidence",
    "candidate_type_slug",
    "luna_candidate_type",
    "field_synthesis_entrypoint",
    "normalized_payload",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_parser_only": True,
    "no_third_party_slam_runtime": True,
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


@dataclass(frozen=True)
class GenericJsonSpatialTraceItem:
    trace_id: str
    source_chain: Tuple[str, ...]
    timestamp_ms: int | None
    time_window_ms: Tuple[int, int] | None
    confidence: float
    candidate_type: str
    field_synthesis_entrypoint: str
    payload: Dict[str, Any]
    candidate_only: bool = True


@dataclass(frozen=True)
class NormalizedParsedTrace:
    parsed_ref: str
    trace_id: str
    source_chain: Tuple[str, ...]
    time_ref: Dict[str, Any]
    confidence: float
    candidate_type_slug: str
    luna_candidate_type: str
    field_synthesis_entrypoint: str
    normalized_payload: Dict[str, Any]
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
