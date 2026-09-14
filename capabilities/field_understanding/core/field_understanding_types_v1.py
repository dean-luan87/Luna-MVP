# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Tuple

PHASE_ID = "Phase-Field-Oriented-Egocentric-Action-Understanding-Architecture-v1-001"
SCOPE = "field_oriented_egocentric_action_understanding_architecture_only"
SOURCE_CHAIN = "field_understanding_v1"

FINAL_DECISION_ARCHITECTURE_READY = (
    "FIELD_ORIENTED_EGOCENTRIC_ACTION_UNDERSTANDING_ARCHITECTURE_READY_FOR_DRYRUN"
)
FINAL_DECISION_DRYRUN_GO = (
    "FIELD_ORIENTED_EGOCENTRIC_ACTION_UNDERSTANDING_ARCHITECTURE_DRYRUN_GO"
)

FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID = "field_information_priority_governance_v1"
FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE = (
    "Field information is the primary synthesis layer above isolated fact candidates. "
    "Isolated facts may influence but must not directly override field information, "
    "except through governed influence policies such as recheck, temporary adjustment, "
    "or user confirmation."
)
FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE_ZH = (
    "场信息是高于孤立事实候选的主合成层。孤立事实可以影响场信息，但不得直接覆盖场信息；"
    "只能通过复核、临时调整或用户确认等受治理路径产生影响。"
)

FIELD_CONTEXT_GOVERNANCE_ID = "field_context_governance_v1"
FIELD_CONTEXT_GOVERNANCE_NOTE = (
    "Field context must be resolved before isolated facts are used for action. "
    "Facts affect field dimensions, not field identity by default."
)
FIELD_CONTEXT_GOVERNANCE_NOTE_ZH = (
    "场提供主语境，细节提供影响因子。必须先解析场语境，再使用孤立事实影响行动；"
    "事实默认影响场的维度，而不是改变场的身份。"
)
FIELD_CONTEXT_DIMENSION_PRINCIPLE = "field_provides_context_details_provide_influence_factors"

FIELD_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "field_ref",
    "field_type",
    "field_confidence",
    "source_refs",
    "static_structure_refs",
    "dynamic_state_refs",
    "semantic_object_refs",
    "map_alignment_refs",
    "candidate_only",
)

STATIC_FIELD_STRUCTURE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "structure_ref",
    "object_class",
    "stability_score",
    "observed_count",
    "last_observed_at",
    "position_band",
    "semantic_label",
    "source_refs",
    "candidate_only",
)

DYNAMIC_FIELD_STATE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "state_ref",
    "object_ref",
    "tracker_ref",
    "dynamic_type",
    "current_state",
    "movement_trend",
    "ttl_ms",
    "risk_level",
    "source_refs",
    "candidate_only",
)

SEMANTIC_FIELD_OBJECT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "semantic_ref",
    "object_ref",
    "object_class",
    "semantic_roles",
    "risk_tags",
    "attention_tags",
    "destination_tags",
    "memory_tags",
    "action_relevance",
    "source_refs",
    "confidence",
    "candidate_only",
)

FIELD_INFLUENCE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "influence_ref",
    "field_ref",
    "influence_type",
    "affected_target",
    "risk_level",
    "action_relevance",
    "emotional_relevance",
    "memory_relevance",
    "source_refs",
    "confidence",
    "fact_ref",
    "influence_scope",
    "affected_field_dimension",
    "candidate_only",
)

ACTION_DISTANCE_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "distance_ref",
    "object_ref",
    "distance_band",
    "estimated_distance_m",
    "error_band_m",
    "method",
    "confidence",
    "source_refs",
    "candidate_only",
)

EXTERNAL_MAP_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "map_ref",
    "map_source",
    "map_type",
    "area_ref",
    "poi_ref",
    "route_ref",
    "expected_anchor",
    "confidence",
    "freshness",
    "candidate_only",
)

EGOCENTRIC_MAP_ALIGNMENT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "alignment_ref",
    "map_ref",
    "visual_anchor_refs",
    "ocr_anchor_refs",
    "pose_refs",
    "semantic_match_score",
    "alignment_status",
    "confidence",
    "candidate_only",
)

SPATIAL_FUSION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "fusion_ref",
    "field_ref",
    "static_refs",
    "dynamic_refs",
    "semantic_refs",
    "influence_refs",
    "distance_refs",
    "map_alignment_refs",
    "conflict_refs",
    "confidence",
    "action_readiness",
    "fact_influence_refs",
    "fact_influence_level",
    "field_revision_policy",
    "candidate_only",
)

CORE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "FieldCandidate",
    "StaticFieldStructureCandidate",
    "DynamicFieldStateCandidate",
    "SemanticFieldObjectCandidate",
    "FieldInfluenceCandidate",
    "ActionDistanceCandidate",
    "ExternalMapCandidate",
    "EgocentricMapAlignmentCandidate",
    "SpatialFusionCandidate",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_camera_runtime": True,
    "no_model_execution": True,
    "no_slam_execution": True,
    "no_map_api_runtime": True,
    "no_speech_output": True,
    "no_navigation_output": True,
    "no_fact_layer_write": True,
    "no_world_model_entry_write": True,
    "external_perception_candidate_only": True,
}


@dataclass(frozen=True)
class FieldCandidate:
    field_ref: str
    field_type: str
    field_confidence: float
    source_refs: Tuple[str, ...]
    static_structure_refs: Tuple[str, ...]
    dynamic_state_refs: Tuple[str, ...]
    semantic_object_refs: Tuple[str, ...]
    map_alignment_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class StaticFieldStructureCandidate:
    structure_ref: str
    object_class: str
    stability_score: float
    observed_count: int
    last_observed_at: str
    position_band: str
    semantic_label: Optional[str]
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class DynamicFieldStateCandidate:
    state_ref: str
    object_ref: str
    tracker_ref: Optional[str]
    dynamic_type: str
    current_state: str
    movement_trend: str
    ttl_ms: int
    risk_level: str
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SemanticFieldObjectCandidate:
    semantic_ref: str
    object_ref: str
    object_class: str
    semantic_roles: Tuple[str, ...]
    risk_tags: Tuple[str, ...]
    attention_tags: Tuple[str, ...]
    destination_tags: Tuple[str, ...]
    memory_tags: Tuple[str, ...]
    action_relevance: str
    source_refs: Tuple[str, ...]
    confidence: float
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldInfluenceCandidate:
    influence_ref: str
    field_ref: str
    influence_type: str
    affected_target: str
    risk_level: str
    action_relevance: str
    emotional_relevance: str
    memory_relevance: str
    source_refs: Tuple[str, ...]
    confidence: float
    fact_ref: Optional[str] = None
    influence_scope: str = "field_synthesis"
    affected_field_dimension: Optional[str] = None
    candidate_only: bool = True


@dataclass(frozen=True)
class ActionDistanceCandidate:
    distance_ref: str
    object_ref: str
    distance_band: str
    estimated_distance_m: Optional[float]
    error_band_m: Optional[float]
    method: str
    confidence: float
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ExternalMapCandidate:
    map_ref: str
    map_source: str
    map_type: str
    area_ref: Optional[str]
    poi_ref: Optional[str]
    route_ref: Optional[str]
    expected_anchor: Optional[str]
    confidence: float
    freshness: str
    candidate_only: bool = True


@dataclass(frozen=True)
class EgocentricMapAlignmentCandidate:
    alignment_ref: str
    map_ref: str
    visual_anchor_refs: Tuple[str, ...]
    ocr_anchor_refs: Tuple[str, ...]
    pose_refs: Tuple[str, ...]
    semantic_match_score: float
    alignment_status: str
    confidence: float
    candidate_only: bool = True


@dataclass(frozen=True)
class SpatialFusionCandidate:
    fusion_ref: str
    field_ref: str
    static_refs: Tuple[str, ...]
    dynamic_refs: Tuple[str, ...]
    semantic_refs: Tuple[str, ...]
    influence_refs: Tuple[str, ...]
    distance_refs: Tuple[str, ...]
    map_alignment_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    confidence: float
    action_readiness: str
    fact_influence_refs: Tuple[str, ...] = ()
    fact_influence_level: str = "none"
    field_revision_policy: str = "no_revision"
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
