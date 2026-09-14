# -*- coding: utf-8 -*-
"""Field Map Place / Realtime Context / Event Overlay Alignment — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001"
SCOPE = "field_map_place_event_overlay_alignment_planning_only"
SOURCE_CHAIN = "field_map_place_event_overlay_alignment_v1"

ALIGNMENT_PRINCIPLE_ZH = (
    "Field 协议对齐：用户交互层 Field ≈ Map Place / POI / 用户认知地点；"
    "Luna 内部层 Field = Map Place + Realtime Context + Event Overlay + Spatial Evidence + Task Context。"
    "地图地点锚定场但不完整定义场；临时事件可覆盖用户交互层场名称但不得改写 map_place_ref。"
)

FIELD_DEFINITION_USER_LAYER = "map_place_or_poi_or_user_cognitive_location"
FIELD_DEFINITION_INTERNAL = (
    "map_place_plus_realtime_context_plus_event_overlay_plus_spatial_evidence_plus_task_context"
)
FIELD_DEFINITION_REF = "map_place_plus_realtime_context_plus_event_overlay"

TARGET_ENTRYPOINT = "field_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

SPATIAL_EVIDENCE_CHAIN_REF = "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
SPATIAL_ODOMETRY_FUSION_REF = "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

FINAL_DECISION_ALIGNMENT_READY = (
    "FIELD_MAP_PLACE_REALTIME_EVENT_OVERLAY_ALIGNMENT_READY_FOR_SYNTHESIS_DRYRUN"
)
FINAL_DECISION_ALIGNMENT_BLOCKED = (
    "FIELD_MAP_PLACE_REALTIME_EVENT_OVERLAY_ALIGNMENT_REVIEW_BLOCKED"
)

FIELD_ALIGNMENT_PIPELINE: Tuple[str, ...] = (
    "MapPlaceRefCandidate",
    "RealtimeContextOverlayCandidate",
    "EventOverlayCandidate",
    "SpatialEvidenceFieldBindingCandidate",
    "FieldInteractionLabelCandidate",
    "field_synthesis_v1",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "FieldMapPlaceAlignmentProfile",
    "MapPlaceRefCandidate",
    "RealtimeContextOverlayCandidate",
    "EventOverlayCandidate",
    "SpatialEvidenceFieldBindingCandidate",
    "FieldInteractionLabelCandidate",
    "FieldAlignmentDecision",
)

FIELD_ALIGNMENT_SCENARIO_REFS: Tuple[str, ...] = (
    "stable_map_place_field",
    "indoor_map_place_with_slam_local_field",
    "temporary_event_overlay",
    "realtime_context_changes_field_state",
    "map_place_spatial_conflict",
    "event_time_window_expired",
)

REALTIME_CONTEXT_TYPES: Tuple[str, ...] = (
    "crowd",
    "construction",
    "closure",
    "queue",
    "traffic",
    "risk",
    "lighting",
    "noise",
    "unknown",
)

EVENT_OVERLAY_TYPES: Tuple[str, ...] = (
    "concert",
    "market",
    "job_fair",
    "exhibition",
    "sports_event",
    "temporary_control",
    "unknown",
)

FIELD_LABEL_SOURCES: Tuple[str, ...] = (
    "map_place",
    "event_overlay",
    "user_task",
    "memory",
    "realtime_context",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    SPATIAL_EVIDENCE_CHAIN_REF,
    SPATIAL_ODOMETRY_FUSION_REF,
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    MODEL_ADMISSION_STANDARD_REF,
)

FIELD_ALIGNMENT_GOVERNANCE_RULES: Tuple[str, ...] = (
    "map_place_anchors_field_but_does_not_fully_define_field",
    "event_overlay_may_override_user_facing_label_not_map_place_ref",
    "gps_gnss_must_not_override_field_identity",
    "slam_vio_must_not_override_field_identity",
    "realtime_context_overlay_only_no_direct_fact_write",
    "event_overlay_must_include_time_window_source_chain_confidence",
    "field_interaction_label_separated_from_internal_field_state",
    "all_inputs_candidate_only",
    "all_outputs_enter_field_synthesis_v1_only",
    "map_place_spatial_conflict_must_emit_conflict_candidate",
    "event_time_window_expiry_must_downgrade_overlay",
    "no_action_speech_fact_write_in_this_phase",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "planning_only": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_real_event_api": True,
    "no_live_sensor": True,
    "no_runtime_activation": True,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
}


@dataclass(frozen=True)
class FieldMapPlaceAlignmentProfile:
    profile_ref: str
    field_definition_user_layer: str
    field_definition_internal: str
    field_definition_ref: str
    spatial_evidence_chain_ref: str
    spatial_odometry_fusion_ref: str
    interface_layer_protocol_ref: str
    target_entrypoint: str
    alignment_pipeline: Tuple[str, ...]
    scenario_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class MapPlaceRefCandidate:
    candidate_ref: str
    map_place_ref: str
    poi_name: str
    address_hint: str
    category_hint: str
    global_position_hint: Dict[str, Any]
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    field_identity_mutation_allowed: bool = False


@dataclass(frozen=True)
class RealtimeContextOverlayCandidate:
    candidate_ref: str
    realtime_context_id: str
    context_type: str
    observed_state: str
    time_window: Tuple[int, int]
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    direct_fact_write_allowed: bool = False


@dataclass(frozen=True)
class EventOverlayCandidate:
    candidate_ref: str
    event_overlay_id: str
    event_type: str
    base_map_place_ref: str
    user_facing_field_label: str
    time_window: Tuple[int, int]
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    map_place_ref_rewrite_allowed: bool = False


@dataclass(frozen=True)
class SpatialEvidenceFieldBindingCandidate:
    candidate_ref: str
    binding_id: str
    spatial_evidence_refs: Tuple[str, ...]
    pose_supported: bool
    motion_supported: bool
    health_supported: bool
    anchor_supported: bool
    relocalization_supported: bool
    drift_supported: bool
    fusion_candidate_ref: str
    coordinate_scope: str
    confidence: float
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldInteractionLabelCandidate:
    candidate_ref: str
    field_label: str
    label_source: str
    display_priority: int
    underlying_map_place_ref: str
    overlay_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    internal_field_state_ref: str = ""


@dataclass(frozen=True)
class FieldAlignmentDecision:
    decision_ref: str
    profile_ref: str
    scenario_count: int
    map_place_field_anchor_supported: bool
    realtime_context_overlay_supported: bool
    event_overlay_supported: bool
    spatial_evidence_binding_supported: bool
    field_interaction_label_separated: bool
    conflict_candidate_required: bool
    field_synthesis_entrypoint_locked: str
    real_map_api_connected: bool
    real_gps_connected: bool
    real_event_api_connected: bool
    runtime_activation_allowed: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
