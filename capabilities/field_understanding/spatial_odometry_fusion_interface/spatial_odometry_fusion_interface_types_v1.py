# -*- coding: utf-8 -*-
"""Spatial Odometry Fusion Interface — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001"
SCOPE = "spatial_odometry_fusion_interface_planning_only"
SOURCE_CHAIN = "spatial_odometry_fusion_interface_v1"

FUSION_INTERFACE_REF = "spatial_odometry_fusion_interface"
FUSION_INTERFACE_NAME = "Spatial Odometry Fusion Interface"

FUSION_PRINCIPLE_ZH = (
    "多源空间里程计融合接口：GPS/GNSS 负责大尺度粗定位，SLAM/VIO 负责局部连续运动，"
    "RTAB-Map graph 负责空间锚点/重定位/漂移提示，Field Synthesis 负责融合。"
    "任何单一来源不得直接触发 action / speech / fact_write。"
)

MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
SOURCE_INTERFACE_PROFILE = "spatial_evidence_ingest_interface"
INTERNAL_STANDARD_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

FINAL_DECISION_PLANNING_READY = (
    "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_READY_FOR_FIELD_PROTOCOL_ALIGNMENT"
)
FINAL_DECISION_REVIEW_BLOCKED = (
    "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_REVIEW_BLOCKED"
)

FUSION_PIPELINE: Tuple[str, ...] = (
    "GPS/GNSS Coarse Position Candidate",
    "SLAM/VIO Local Odometry Candidate",
    "RTAB-Map Graph Anchor / Relocalization / Drift Candidate",
    "Spatial Odometry Fusion Candidate",
    "field_synthesis_v1",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "SpatialOdometryFusionInterface",
    "GPSGNSSCoarsePositionCandidate",
    "SLAMLocalOdometryCandidate",
    "RTABGraphAnchorCandidate",
    "MapAlignmentHintCandidate",
    "SpatialOdometryFusionCandidate",
    "SpatialOdometryFusionPlanningDecision",
)

INPUT_EVIDENCE_SOURCE_REFS: Tuple[str, ...] = (
    "gps_gnss_coarse_position_stub",
    "generic_json_spatial_trace_pose_motion",
    "rtab_map_trajectory_export_subset",
    "rtab_map_odometry_export_subset",
    "rtab_map_graph_export_subset",
    "map_place_ref_stub",
)

FUSION_SCENARIO_REFS: Tuple[str, ...] = (
    "outdoor_gps_primary_slam_support",
    "indoor_slam_primary_gps_degraded",
    "transition_outdoor_to_indoor",
    "gps_slam_conflict",
    "rtab_graph_relocalization_with_gps_hint",
)

COORDINATE_SCOPES: Tuple[str, ...] = (
    "global_coarse",
    "local",
    "aligned_local",
    "mixed",
)

FUSION_CANDIDATE_OUTPUT_FIELDS: Tuple[str, ...] = (
    "fusion_candidate_id",
    "coordinate_scope",
    "global_position_hint",
    "local_motion_hint",
    "anchor_alignment_hint",
    "drift_status",
    "relocalization_status",
    "confidence",
    "source_chain",
    "source_candidate_refs",
    "fusion_policy",
    "field_synthesis_entrypoint",
    "candidate_only",
)

FUSION_GOVERNANCE_RULES: Tuple[str, ...] = (
    "gps_gnss_must_not_override_field_identity",
    "gps_gnss_must_not_trigger_action_speech_fact_write",
    "slam_vio_must_not_trigger_action_speech_fact_write",
    "rtab_graph_relocalization_must_not_restore_runtime_trust",
    "gps_slam_conflict_must_emit_conflict_candidate",
    "coordinate_scope_must_be_explicit",
    "source_chain_must_be_preserved",
    "fusion_candidate_enters_field_synthesis_v1_only",
    "all_inputs_remain_candidate_only",
    "no_real_gps_gnss_in_this_phase",
)

SPATIAL_ODOMETRY_FUSION_INTERFACE_FIELDS: Tuple[str, ...] = (
    "interface_ref",
    "interface_name",
    "interface_layer_protocol_ref",
    "model_management_protocol_ref",
    "source_interface_profile",
    "internal_standard_format",
    "target_entrypoint",
    "fusion_pipeline",
    "input_evidence_source_refs",
    "fusion_scenario_refs",
    "governance_rules",
    "candidate_only",
)

GPS_GNSS_COARSE_POSITION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "candidate_ref",
    "source_evidence_ref",
    "coordinate_scope",
    "global_position_hint",
    "confidence",
    "source_chain",
    "field_synthesis_entrypoint",
    "candidate_only",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "field_identity_mutation_allowed",
)

SLAM_LOCAL_ODOMETRY_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "candidate_ref",
    "source_evidence_ref",
    "coordinate_scope",
    "local_motion_hint",
    "confidence",
    "source_chain",
    "field_synthesis_entrypoint",
    "candidate_only",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
)

RTAB_GRAPH_ANCHOR_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "candidate_ref",
    "source_evidence_ref",
    "coordinate_scope",
    "anchor_alignment_hint",
    "drift_status",
    "relocalization_status",
    "confidence",
    "source_chain",
    "field_synthesis_entrypoint",
    "candidate_only",
    "restore_runtime_trust",
    "direct_action_allowed",
)

MAP_ALIGNMENT_HINT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "candidate_ref",
    "source_evidence_ref",
    "coordinate_scope",
    "anchor_alignment_hint",
    "global_alignment_hint",
    "gps_anchor_ref",
    "map_alignment_ref",
    "confidence",
    "source_chain",
    "field_synthesis_entrypoint",
    "candidate_only",
    "field_identity_mutation_allowed",
)

SPATIAL_ODOMETRY_FUSION_CANDIDATE_FIELDS: Tuple[str, ...] = FUSION_CANDIDATE_OUTPUT_FIELDS

SPATIAL_ODOMETRY_FUSION_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "interface_ref",
    "fusion_scenario_count",
    "planning_only",
    "real_gps_connected",
    "runtime_activation_allowed",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "field_synthesis_entrypoint_locked",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "planning_only": True,
    "no_real_gps_gnss": True,
    "no_live_sensor": True,
    "no_runtime_activation": True,
    "runtime_activation_allowed": False,
    "commercial_runtime_approved": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "no_field_identity_mutation": True,
    "no_runtime_trust_restore": True,
}


@dataclass(frozen=True)
class SpatialOdometryFusionInterface:
    interface_ref: str
    interface_name: str
    interface_layer_protocol_ref: str
    model_management_protocol_ref: str
    source_interface_profile: str
    internal_standard_format: str
    target_entrypoint: str
    fusion_pipeline: Tuple[str, ...]
    input_evidence_source_refs: Tuple[str, ...]
    fusion_scenario_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class GPSGNSSCoarsePositionCandidate:
    candidate_ref: str
    source_evidence_ref: str
    coordinate_scope: str
    global_position_hint: Dict[str, Any]
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    direct_action_allowed: bool = False
    direct_speech_allowed: bool = False
    direct_fact_write_allowed: bool = False
    field_identity_mutation_allowed: bool = False


@dataclass(frozen=True)
class SLAMLocalOdometryCandidate:
    candidate_ref: str
    source_evidence_ref: str
    coordinate_scope: str
    local_motion_hint: Dict[str, Any]
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    direct_action_allowed: bool = False
    direct_speech_allowed: bool = False
    direct_fact_write_allowed: bool = False


@dataclass(frozen=True)
class RTABGraphAnchorCandidate:
    candidate_ref: str
    source_evidence_ref: str
    coordinate_scope: str
    anchor_alignment_hint: Dict[str, Any]
    drift_status: str
    relocalization_status: str
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    restore_runtime_trust: bool = False
    direct_action_allowed: bool = False


@dataclass(frozen=True)
class MapAlignmentHintCandidate:
    candidate_ref: str
    source_evidence_ref: str
    coordinate_scope: str
    anchor_alignment_hint: Dict[str, Any]
    global_alignment_hint: str
    gps_anchor_ref: str
    map_alignment_ref: str
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    field_identity_mutation_allowed: bool = False


@dataclass(frozen=True)
class SpatialOdometryFusionCandidate:
    fusion_candidate_id: str
    coordinate_scope: str
    global_position_hint: Dict[str, Any]
    local_motion_hint: Dict[str, Any]
    anchor_alignment_hint: Dict[str, Any]
    drift_status: str
    relocalization_status: str
    confidence: float
    source_chain: Tuple[str, ...]
    source_candidate_refs: Tuple[str, ...]
    fusion_policy: str
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class SpatialOdometryFusionPlanningDecision:
    decision_ref: str
    interface_ref: str
    fusion_scenario_count: int
    planning_only: bool
    real_gps_connected: bool
    runtime_activation_allowed: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    field_synthesis_entrypoint_locked: str
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
