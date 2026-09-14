"""Candidate-only builder API for Luna Cognitive Primitive Layer v1."""

from __future__ import annotations

from typing import Any, Mapping

from .models_v1 import (
    normalize_confidence,
    normalize_evidence_source_type,
    normalize_refs,
    normalize_schema_version,
    require_mapping,
    require_nonempty_text,
)
from .types_v1 import (
    EntityCandidateV1,
    EvidenceReferenceV1,
    FieldReferenceCandidateV1,
    ObservationEventV1,
    RelationCandidateV1,
    StateCandidateV1,
)


def _input(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    return require_mapping(value, name)


def create_observation(value: Mapping[str, Any]) -> ObservationEventV1:
    data = _input(value, "observation")
    return ObservationEventV1(
        observation_id=require_nonempty_text(data.get("observation_id"), "observation_id"),
        source_ref=require_nonempty_text(data.get("source_ref"), "source_ref"),
        observation_type=require_nonempty_text(data.get("observation_type"), "observation_type"),
        occurred_at=require_nonempty_text(data.get("occurred_at"), "occurred_at"),
        observed_at=require_nonempty_text(data.get("observed_at"), "observed_at"),
        payload=require_mapping(data.get("payload"), "payload"),
        evidence_refs=normalize_refs(data.get("evidence_refs"), "evidence_refs"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )


def create_evidence(value: Mapping[str, Any]) -> EvidenceReferenceV1:
    data = _input(value, "evidence")
    return EvidenceReferenceV1(
        evidence_id=require_nonempty_text(data.get("evidence_id"), "evidence_id"),
        source_type=normalize_evidence_source_type(data.get("source_type")),
        source_ref=require_nonempty_text(data.get("source_ref"), "source_ref"),
        content_ref=require_nonempty_text(data.get("content_ref"), "content_ref"),
        confidence=normalize_confidence(data.get("confidence")),
        created_at=require_nonempty_text(data.get("created_at"), "created_at"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )


def create_entity_candidate(value: Mapping[str, Any]) -> EntityCandidateV1:
    data = _input(value, "entity_candidate")
    return EntityCandidateV1(
        entity_id=require_nonempty_text(data.get("entity_id"), "entity_id"),
        entity_type=require_nonempty_text(data.get("entity_type"), "entity_type"),
        attributes=require_mapping(data.get("attributes"), "attributes"),
        evidence_refs=normalize_refs(data.get("evidence_refs"), "evidence_refs"),
        observation_refs=normalize_refs(data.get("observation_refs"), "observation_refs"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )


def create_relation_candidate(value: Mapping[str, Any]) -> RelationCandidateV1:
    data = _input(value, "relation_candidate")
    return RelationCandidateV1(
        relation_id=require_nonempty_text(data.get("relation_id"), "relation_id"),
        subject_ref=require_nonempty_text(data.get("subject_ref"), "subject_ref"),
        predicate=require_nonempty_text(data.get("predicate"), "predicate"),
        object_ref=require_nonempty_text(data.get("object_ref"), "object_ref"),
        evidence_refs=normalize_refs(data.get("evidence_refs"), "evidence_refs"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )


def create_field_reference_candidate(value: Mapping[str, Any]) -> FieldReferenceCandidateV1:
    data = _input(value, "field_reference_candidate")
    return FieldReferenceCandidateV1(
        field_ref=require_nonempty_text(data.get("field_ref"), "field_ref"),
        field_type_candidate=require_nonempty_text(data.get("field_type_candidate"), "field_type_candidate"),
        relation_context=require_mapping(data.get("relation_context"), "relation_context"),
        evidence_refs=normalize_refs(data.get("evidence_refs"), "evidence_refs"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )


def create_state_candidate(value: Mapping[str, Any]) -> StateCandidateV1:
    data = _input(value, "state_candidate")
    return StateCandidateV1(
        state_id=require_nonempty_text(data.get("state_id"), "state_id"),
        target_ref=require_nonempty_text(data.get("target_ref"), "target_ref"),
        state_type=require_nonempty_text(data.get("state_type"), "state_type"),
        value=require_mapping(data.get("value"), "value"),
        evidence_refs=normalize_refs(data.get("evidence_refs"), "evidence_refs"),
        temporal_context=require_mapping(data.get("temporal_context"), "temporal_context"),
        trace_ref=require_nonempty_text(data.get("trace_ref"), "trace_ref"),
        provenance_refs=normalize_refs(data.get("provenance_refs"), "provenance_refs"),
        schema_version=normalize_schema_version(data.get("schema_version")),
    )

