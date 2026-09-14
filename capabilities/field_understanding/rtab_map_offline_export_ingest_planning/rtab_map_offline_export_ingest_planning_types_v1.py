# -*- coding: utf-8 -*-
"""RTAB-Map Offline Export Ingest Planning — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-RTAB-Map-Offline-Export-To-JSON-Spatial-Trace-Ingest-Planning-v1-001"
SCOPE = "rtab_map_offline_export_ingest_planning_only"
SOURCE_CHAIN = "rtab_map_offline_export_ingest_planning_v1"

PLANNING_PRINCIPLE_EN = (
    "Luna owns its input standard, model management protocol, candidate schema, and "
    "field_synthesis main chain. External models only provide capability; they must not "
    "pull Luna's main architecture. RTAB-Map offline export is planned as a subset "
    "conversion into Generic JSON Spatial Trace, not as a native Luna standard."
)
PLANNING_PRINCIPLE_ZH = (
    "Luna 有自己的输入标准、模型管理协议、candidate schema 和 field_synthesis 主链。"
    "外部模型只负责提供能力，不允许反过来牵引 Luna 的主架构。"
    "RTAB-Map offline export 仅规划为 Generic JSON Spatial Trace 的子集转换，"
    "不作为 Luna 原生标准。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
SOURCE_INTERNAL_STANDARD = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"

FINAL_DECISION_READY_FOR_SUBSET_FIXTURE = (
    "RTAB_MAP_OFFLINE_EXPORT_INGEST_PLANNING_READY_FOR_SUBSET_FIXTURE"
)
FINAL_DECISION_REVIEW_BLOCKED = "RTAB_MAP_OFFLINE_EXPORT_INGEST_PLANNING_REVIEW_BLOCKED"

EXPORT_SUBSET_REFS: Tuple[str, ...] = (
    "trajectory_export_subset",
    "odometry_export_subset",
    "graph_export_subset",
    "local_map_metadata_subset",
    "occupancy_or_pointcloud_metadata_subset",
)

P0_EXPORT_SUBSETS: Tuple[str, ...] = (
    "trajectory_export_subset",
    "odometry_export_subset",
)
P1_EXPORT_SUBSETS: Tuple[str, ...] = ("graph_export_subset",)
P2_EXPORT_SUBSETS: Tuple[str, ...] = ("local_map_metadata_subset",)
OBSERVATION_EXPORT_SUBSETS: Tuple[str, ...] = (
    "occupancy_or_pointcloud_metadata_subset",
)

PARSER_PRIORITY_LEVELS: Tuple[str, ...] = ("p0", "p1", "p2", "observation")
OFFLINE_FEASIBILITY_LEVELS: Tuple[str, ...] = ("high", "medium", "low")
RISK_LEVELS: Tuple[str, ...] = ("low", "medium", "high")

SUBSET_PLANNING_FIELDS: Tuple[str, ...] = (
    "subset_ref",
    "source_export_kind",
    "expected_fields",
    "required_fields",
    "optional_fields",
    "luna_candidate_mapping",
    "generic_json_trace_mapping",
    "lossy_conversion_notes",
    "unsupported_fields",
    "offline_feasibility",
    "parser_priority",
    "risk_level",
    "candidate_only",
)

PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "planning_ref",
    "model_id",
    "model_family",
    "domain_id",
    "model_management_protocol_ref",
    "model_admission_standard_ref",
    "source_internal_standard",
    "target_entrypoint",
    "adapter_profile_ref",
    "output_candidate_contract_ref",
    "p0_export_subsets",
    "p1_export_subsets",
    "p2_export_subsets",
    "observation_export_subsets",
    "recommended_first_subset_fixture",
    "ingest_pipeline",
    "architecture_principle_locked",
    "offline_planning_only",
    "no_runtime_activation",
    "final_decision",
    "candidate_only",
)

FORBIDDEN_ARCHITECTURE_RULES: Tuple[str, ...] = (
    "rtabmap_database_not_luna_standard",
    "ros_topic_not_luna_standard",
    "no_raw_pointcloud_in_candidate",
    "no_occupancy_map_long_term_write",
    "no_generic_json_spatial_trace_bypass",
    "no_field_synthesis_v1_bypass",
    "no_provider_runtime_activation",
    "no_commercial_runtime_approval",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_export_ingest_planning_only": True,
    "no_rtabmap_runtime": True,
    "no_rtabmap_database_read": True,
    "no_ros_runtime": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_provider_runtime_activation": True,
    "runtime_activation_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
    "no_commercial_runtime_approval": True,
    "no_long_term_map_write": True,
}


@dataclass(frozen=True)
class RTABMapExportSubsetPlanningEntry:
    subset_ref: str
    source_export_kind: str
    expected_fields: Tuple[str, ...]
    required_fields: Tuple[str, ...]
    optional_fields: Tuple[str, ...]
    luna_candidate_mapping: Dict[str, str]
    generic_json_trace_mapping: Dict[str, str]
    lossy_conversion_notes: Tuple[str, ...]
    unsupported_fields: Tuple[str, ...]
    offline_feasibility: str
    parser_priority: str
    risk_level: str
    candidate_only: bool = True


@dataclass(frozen=True)
class RTABMapOfflineExportIngestPlanningDecision:
    decision_ref: str
    planning_ref: str
    model_id: str
    model_family: str
    domain_id: str
    model_management_protocol_ref: str
    model_admission_standard_ref: str
    source_internal_standard: str
    target_entrypoint: str
    adapter_profile_ref: str
    output_candidate_contract_ref: str
    p0_export_subsets: Tuple[str, ...]
    p1_export_subsets: Tuple[str, ...]
    p2_export_subsets: Tuple[str, ...]
    observation_export_subsets: Tuple[str, ...]
    recommended_first_subset_fixture: str
    ingest_pipeline: Tuple[str, ...]
    architecture_principle_locked: bool
    offline_planning_only: bool
    no_runtime_activation: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
