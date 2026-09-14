"""Typed candidate value for an observed Entity-to-Field relation state."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Mapping, Tuple


ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1 = (
    "entity_field_observation_relation_state"
)
ENTITY_FIELD_RELATION_EVENT_V1 = "entity_field_relation_observed"
ENTITY_TO_FIELD_OBSERVATION_RELATION_V1 = "ENTITY_TO_FIELD_OBSERVATION_RELATION"
OBSERVED_IN_FIELD_V1 = "OBSERVED_IN_FIELD"


def _unique(values: Iterable[Any]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if str(value).strip()))


@dataclass(frozen=True)
class EntityFieldRelationStateValueV1:
    """Candidate-only semantic value carried by ``FieldStateCandidate``."""

    relation_candidate_ref: str
    subject_ref: str
    predicate: str
    object_ref: str
    relation_semantic_kind: str
    evidence_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    fact_admitted: bool = False
    truth_declared: bool = False
    persistent_relation_declared: bool = False
    identity_resolution_status: str = "UNRESOLVED"

    def __post_init__(self) -> None:
        if self.predicate != OBSERVED_IN_FIELD_V1:
            raise ValueError("unsupported Entity-to-Field observation predicate")
        if self.relation_semantic_kind != ENTITY_TO_FIELD_OBSERVATION_RELATION_V1:
            raise ValueError("unsupported Entity-to-Field relation semantic kind")
        if not self.candidate_only or self.fact_admitted:
            raise ValueError("relation state value must remain candidate-only")
        if self.truth_declared or self.persistent_relation_declared:
            raise ValueError("relation state value cannot promote truth or persistence")
        if self.identity_resolution_status != "UNRESOLVED":
            raise ValueError("relation state value cannot resolve identity")


def build_entity_field_relation_state_value_v1(
    admitted_events: Iterable[Mapping[str, Any]],
) -> Dict[str, Any] | None:
    """Derive a typed value from admitted relation events, never from fixtures."""

    events = tuple(admitted_events)
    if not events:
        return None

    payloads = []
    source_refs = []
    for event in events:
        payload = event.get("payload")
        if not isinstance(payload, Mapping):
            return None
        if event.get("event_type") != ENTITY_FIELD_RELATION_EVENT_V1:
            return None
        if payload.get("relation_semantic_kind") != ENTITY_TO_FIELD_OBSERVATION_RELATION_V1:
            return None
        if payload.get("predicate") != OBSERVED_IN_FIELD_V1:
            return None
        if payload.get("candidate_only") is not True:
            return None
        if payload.get("fact_admitted") is not False:
            return None
        if payload.get("truth_declared") is not False:
            return None
        if payload.get("persistent_relation_declared") is not False:
            return None
        if payload.get("identity_resolution_status") != "UNRESOLVED":
            return None
        source_id = str(event.get("source_id") or "")
        if not source_id:
            return None
        payloads.append(payload)
        source_refs.append(source_id)

    first = payloads[0]
    relation_fields = (
        "relation_candidate_ref",
        "subject_ref",
        "predicate",
        "object_ref",
        "relation_semantic_kind",
    )
    if any(not first.get(field) for field in relation_fields):
        return None
    if any(any(payload.get(field) != first.get(field) for field in relation_fields) for payload in payloads[1:]):
        return None

    evidence_refs = _unique(
        ref
        for payload in payloads
        for ref in payload.get("evidence_refs", ())
    )
    provenance_refs = _unique(
        ref
        for event, payload in zip(events, payloads)
        for ref in (
            *tuple(payload.get("provenance_refs", ())),
            str(event.get("trace_ref") or ""),
        )
    )
    trace_ref = str(events[0].get("trace_ref") or "")
    if not trace_ref:
        return None

    return asdict(
        EntityFieldRelationStateValueV1(
            relation_candidate_ref=str(first["relation_candidate_ref"]),
            subject_ref=str(first["subject_ref"]),
            predicate=str(first["predicate"]),
            object_ref=str(first["object_ref"]),
            relation_semantic_kind=str(first["relation_semantic_kind"]),
            evidence_refs=evidence_refs,
            source_refs=_unique(source_refs),
            trace_ref=trace_ref,
            provenance_refs=provenance_refs,
        )
    )


__all__ = [
    "ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1",
    "ENTITY_FIELD_RELATION_EVENT_V1",
    "ENTITY_TO_FIELD_OBSERVATION_RELATION_V1",
    "OBSERVED_IN_FIELD_V1",
    "EntityFieldRelationStateValueV1",
    "build_entity_field_relation_state_value_v1",
]
