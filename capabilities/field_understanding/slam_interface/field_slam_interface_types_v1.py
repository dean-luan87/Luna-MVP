# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-SLAM-Interface-Contract-v1-001"
SCOPE = "field_slam_interface_contract_only"
SOURCE_CHAIN = "field_slam_interface_v1"
ROLE_EN = "Field Spatial Evidence Provider"
ROLE_ZH = "场空间证据提供者"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "FIELD_SLAM_INTERFACE_CONTRACT_READY_FOR_DRYRUN_CASES"
)

SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID = "slam_evidence_provider_governance_v1"
SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE = (
    "SLAM/VIO/IMU outputs are spatial evidence candidates only. "
    "They must enter Field Synthesis and must not directly drive action, speech, "
    "fact writes, destination confirmation, or field identity override."
)
SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE_ZH = (
    "SLAM/VIO/IMU 输出仅为空间证据候选，必须进入 Field Synthesis；"
    "不得直接驱动行动、语音、事实写入、目的地确认或场身份覆盖。"
)

POSE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "pose_ref",
    "timestamp",
    "frame_ref",
    "position_delta_m",
    "rotation_delta_deg",
    "heading_delta_deg",
    "pose_confidence",
    "source_method",
    "source_refs",
    "candidate_only",
)

MOTION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "motion_ref",
    "timestamp",
    "motion_state",
    "speed_band",
    "heading_change",
    "stability_level",
    "confidence",
    "source_refs",
    "candidate_only",
)

SPATIAL_ANCHOR_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "anchor_ref",
    "object_ref",
    "anchor_type",
    "relative_position_band",
    "stability_score",
    "observed_count",
    "last_seen_at",
    "source_refs",
    "candidate_only",
)

LOCAL_MAP_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "local_map_ref",
    "time_window_ms",
    "anchor_refs",
    "static_structure_refs",
    "dynamic_state_refs",
    "pose_refs",
    "confidence",
    "drift_risk",
    "candidate_only",
)

SLAM_HEALTH_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "health_ref",
    "source_method",
    "tracking_status",
    "feature_quality",
    "imu_quality",
    "lighting_quality",
    "motion_blur_level",
    "confidence",
    "degraded_reason",
    "candidate_only",
)

MAP_DRIFT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "drift_ref",
    "local_map_ref",
    "drift_risk",
    "suspected_drift_source",
    "affected_refs",
    "recommended_policy",
    "confidence",
    "candidate_only",
)

RELOCALIZATION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "relocalization_ref",
    "previous_anchor_refs",
    "current_anchor_refs",
    "match_score",
    "relocalization_status",
    "confidence",
    "candidate_only",
)

SLAM_INTERFACE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_camera_runtime": True,
    "no_model_execution": True,
    "no_slam_execution": True,
    "no_slam_framework_binding": True,
    "no_map_api_runtime": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
    "no_world_model_entry_write": True,
    "no_long_term_map_write": True,
    "external_perception_candidate_only": True,
}


@dataclass(frozen=True)
class PoseCandidate:
    pose_ref: str
    timestamp: str
    frame_ref: str
    position_delta_m: Tuple[float, float, float]
    rotation_delta_deg: Tuple[float, float, float]
    heading_delta_deg: float
    pose_confidence: float
    source_method: str
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class MotionCandidate:
    motion_ref: str
    timestamp: str
    motion_state: str
    speed_band: str
    heading_change: str
    stability_level: str
    confidence: float
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SpatialAnchorCandidate:
    anchor_ref: str
    object_ref: str
    anchor_type: str
    relative_position_band: str
    stability_score: float
    observed_count: int
    last_seen_at: str
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class LocalMapCandidate:
    local_map_ref: str
    time_window_ms: int
    anchor_refs: Tuple[str, ...]
    static_structure_refs: Tuple[str, ...]
    dynamic_state_refs: Tuple[str, ...]
    pose_refs: Tuple[str, ...]
    confidence: float
    drift_risk: str
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMHealthCandidate:
    health_ref: str
    source_method: str
    tracking_status: str
    feature_quality: str
    imu_quality: str
    lighting_quality: str
    motion_blur_level: str
    confidence: float
    degraded_reason: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class MapDriftCandidate:
    drift_ref: str
    local_map_ref: str
    drift_risk: str
    suspected_drift_source: str
    affected_refs: Tuple[str, ...]
    recommended_policy: str
    confidence: float
    candidate_only: bool = True


@dataclass(frozen=True)
class RelocalizationCandidate:
    relocalization_ref: str
    previous_anchor_refs: Tuple[str, ...]
    current_anchor_refs: Tuple[str, ...]
    match_score: float
    relocalization_status: str
    confidence: float
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
