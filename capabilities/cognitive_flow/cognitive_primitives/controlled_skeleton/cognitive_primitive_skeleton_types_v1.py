"""Immutable candidate-only types for the A3 Cognitive Primitive skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple


COGNITIVE_PRIMITIVE_SKELETON_SCHEMA_VERSION_V1 = (
    "luna.cognitive_primitive.controlled_skeleton.v1"
)
PRIMITIVE_TYPES_V1 = (
    "entity_primitive_candidate",
    "relation_primitive_candidate",
    "state_primitive_candidate",
    "event_primitive_candidate",
    "situation_primitive_candidate",
)


@dataclass(frozen=True)
class CognitivePrimitiveCandidateV1:
    primitive_id: str
    primitive_type: str
    source_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    provenance: Mapping[str, object]
    confidence: float | None
    uncertainty: Mapping[str, object]
    candidate_status: str
    trace_ref: str
    candidate_only: bool = True
    fact_status: str = "not_fact"
    schema_version: str = COGNITIVE_PRIMITIVE_SKELETON_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class EntityPrimitiveCandidateV1(CognitivePrimitiveCandidateV1):
    entity_kind: str = "unspecified_candidate"
    attributes: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class RelationPrimitiveCandidateV1(CognitivePrimitiveCandidateV1):
    subject_ref: str = ""
    predicate: str = ""
    object_ref: str = ""


@dataclass(frozen=True)
class StatePrimitiveCandidateV1(CognitivePrimitiveCandidateV1):
    target_ref: str = ""
    state_kind: str = "unspecified_candidate"
    value: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class EventPrimitiveCandidateV1(CognitivePrimitiveCandidateV1):
    event_kind: str = "unspecified_candidate"
    temporal_context: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SituationPrimitiveCandidateV1(CognitivePrimitiveCandidateV1):
    situation_kind: str = "unspecified_candidate"
    member_refs: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CognitivePrimitiveSkeletonFlagsV1:
    runtime_executed: bool = False
    model_invoked: bool = False
    external_call: bool = False
    database_written: bool = False
    field_kernel_mutated: bool = False
    reducer_invoked: bool = False
    fact_created: bool = False
    decision_created: bool = False
    action_created: bool = False
    state_writeback: bool = False
    memory_updated: bool = False

