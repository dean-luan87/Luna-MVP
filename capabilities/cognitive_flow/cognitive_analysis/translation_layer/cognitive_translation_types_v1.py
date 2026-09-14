"""Immutable, candidate-only types for the A3 Translation Layer Skeleton v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1 = (
    "luna.cognitive_analysis.translation_layer_skeleton.v1"
)

ALLOWED_PRIMITIVE_TYPES_V1 = (
    "entity_candidate",
    "relation_candidate",
    "semantic_candidate",
    "spatial_candidate",
    "temporal_candidate",
)


@dataclass(frozen=True)
class CognitiveTranslationRequestEnvelopeV1:
    """Reference-only input; no external model output or raw evidence payload is accepted."""

    translation_request_id: str
    evidence_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_capability_refs: Tuple[str, ...]
    requested_primitive_type: str
    trace_ref: str
    schema_version: str = COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitivePrimitiveCandidateV1:
    """A possible primitive identity, never a Fact, Entity, State, Decision, or Action."""

    candidate_id: str
    primitive_type: str
    source_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    confidence: float | None
    uncertainty: Mapping[str, object]
    provenance: Mapping[str, object]
    trace_ref: str
    candidate_status: str
    candidate_only: bool = True
    fact_status: str = "not_fact"
    schema_version: str = COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class CognitiveTranslationFlagsV1:
    """Frozen no-execution/no-write boundary flags for the controlled skeleton."""

    translation_executed: bool = False
    simulation_only: bool = True
    model_invoked: bool = False
    external_call: bool = False
    fact_created: bool = False
    decision_created: bool = False
    action_created: bool = False
    state_writeback: bool = False
    context_mutated: bool = False
    snapshot_mutated: bool = False
    memory_updated: bool = False
    learning_candidate_admitted: bool = False


@dataclass(frozen=True)
class CognitiveTranslationCandidateEnvelopeV1:
    """Skeleton output envelope; its candidate is not available for Runtime execution."""

    request_ref: str
    cognitive_primitive_candidate: CognitivePrimitiveCandidateV1
    translation_flags: CognitiveTranslationFlagsV1
    negative_guard_refs: Tuple[str, ...]
    schema_version: str = COGNITIVE_TRANSLATION_SCHEMA_VERSION_V1
