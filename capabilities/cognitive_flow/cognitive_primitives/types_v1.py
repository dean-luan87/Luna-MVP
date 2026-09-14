"""Luna Cognitive Primitive Layer v1 candidate-only domain types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Tuple


COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1 = "luna.cognitive_primitive.v1"


class EvidenceSourceTypeV1(str, Enum):
    SENSOR = "sensor"
    MODEL = "model"
    USER = "user"
    KNOWLEDGE = "knowledge"
    EXPERIENCE = "experience"
    SIMULATION = "simulation"


@dataclass(frozen=True)
class ObservationEventV1:
    observation_id: str
    source_ref: str
    observation_type: str
    occurred_at: str
    observed_at: str
    payload: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    fact_admitted: bool = False
    conclusion_made: bool = False


@dataclass(frozen=True)
class EvidenceReferenceV1:
    evidence_id: str
    source_type: str
    source_ref: str
    content_ref: str
    confidence: float
    created_at: str
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    fact_admitted: bool = False


@dataclass(frozen=True)
class EntityCandidateV1:
    entity_id: str
    entity_type: str
    attributes: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    observation_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    fact_admitted: bool = False


@dataclass(frozen=True)
class RelationCandidateV1:
    relation_id: str
    subject_ref: str
    predicate: str
    object_ref: str
    evidence_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    fact_admitted: bool = False


@dataclass(frozen=True)
class FieldReferenceCandidateV1:
    field_ref: str
    field_type_candidate: str
    relation_context: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    fact_admitted: bool = False


@dataclass(frozen=True)
class StateCandidateV1:
    state_id: str
    target_ref: str
    state_type: str
    value: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    temporal_context: Mapping[str, Any]
    trace_ref: str
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    schema_version: str = COGNITIVE_PRIMITIVE_SCHEMA_VERSION_V1
    candidate_only: bool = True
    field_state_modified: bool = False
    fact_admitted: bool = False

