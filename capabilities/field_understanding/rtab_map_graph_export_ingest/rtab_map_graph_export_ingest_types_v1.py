# -*- coding: utf-8 -*-
"""RTAB-Map Graph Export Ingest — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

PHASE_ID = "Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001"
SCOPE = "rtab_map_graph_export_ingest_fixture_only"
SOURCE_CHAIN = "rtab_map_graph_export_ingest_v1"
INGEST_REF = "rtab_map_graph_export_ingest_v1"

INGEST_PRINCIPLE_ZH = (
    "Interface Layer Governance Protocol 下的 RTAB-Map graph_export_subset "
    "最小 fixture 转换样例。补充 Anchor / Relocalization / Drift 输入能力，"
    "预留 GPS/GNSS 联动 metadata hint，不运行 RTAB-Map、不读 database、不接真实 GPS。"
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

INPUT_EXPORT_KIND = "graph_export_subset"
INPUT_FORMAT_REF = "rtab_map_graph_export_subset"
TARGET_FORMAT_REF = INTERNAL_STANDARD_FORMAT
GENERIC_JSON_PARSER_MODULE_REF = (
    "capabilities.field_understanding.generic_json_spatial_trace_parser."
    "generic_json_spatial_trace_parser_static_validators_v1"
)

COORDINATE_SCOPES: Tuple[str, ...] = ("local", "global_coarse", "aligned_local")
EDGE_KINDS: Tuple[str, ...] = ("normal", "loop_closure")

GPS_GNSS_LINK_RESERVED_FIELDS: Tuple[str, ...] = (
    "global_alignment_hint",
    "gps_anchor_ref",
    "map_alignment_ref",
)

FINAL_DECISION_REVIEW_GO = (
    "RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_GO"
)
FINAL_DECISION_REVIEW_BLOCKED = (
    "RTAB_MAP_GRAPH_EXPORT_TO_JSON_SPATIAL_TRACE_FIXTURE_REVIEW_BLOCKED"
)

EXPECTED_GRAPH_NODE_COUNT = 3
EXPECTED_GRAPH_EDGE_COUNT = 2
EXPECTED_JSON_TRACE_ITEM_COUNT_MIN = 5
EXPECTED_ANCHOR_ITEM_COUNT = 3
EXPECTED_RELOCALIZATION_ITEM_COUNT = 1
EXPECTED_DRIFT_ITEM_COUNT = 1

GRAPH_NODE_REQUIRED_FIELDS: Tuple[str, ...] = (
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
    "coordinate_scope",
    "source_chain",
)

GRAPH_EDGE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "edge_id",
    "from_node_id",
    "to_node_id",
    "edge_kind",
    "confidence",
    "source_chain",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_fixture_ingest_only": True,
    "no_rtabmap_runtime": True,
    "no_rtabmap_database_read": True,
    "no_ros_runtime": True,
    "no_pointcloud_large_object": True,
    "no_real_gps_gnss": True,
    "no_real_global_map_alignment": True,
    "no_real_relocalization": True,
    "no_runtime_trust_restore": True,
    "no_long_term_map_write": True,
    "no_provider_runtime_activation": True,
    "runtime_activation_allowed": False,
    "commercial_runtime_approved": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
    "no_field_identity_mutation": True,
    "no_rtabmap_private_ingest_entrypoint": True,
    "no_interface_layer_bypass": True,
    "no_generic_json_spatial_trace_bypass": True,
    "no_field_synthesis_v1_bypass": True,
}
