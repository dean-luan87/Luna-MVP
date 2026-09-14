"""Evaluation-only contracts for relation-bearing Field Event admission.

The integration projection is deliberately thinner than a Field ontology
change.  It identifies the semantic kind carried by a generic
``FieldEventCandidateV1`` while retaining candidate-only governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class RelationBearingFieldSemanticEventProjectionV1:
    """Explicit Entity-to-Field observation semantics for an event payload."""

    projection_ref: str
    relation_semantic_kind: str
    relation_candidate_ref: str
    subject_ref: str
    predicate: str
    object_ref: str
    field_ref: str
    entity_candidate_ref: str
    runtime_observation_ref: str
    evidence_refs: Tuple[str, ...]
    source_detection_refs: Tuple[str, ...]
    subject_binding_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    field_ref_resolution_status: str
    candidate_only: bool = True
    fact_admitted: bool = False
    truth_declared: bool = False
    persistent_relation_declared: bool = False
    identity_resolution_status: str = "UNRESOLVED"
    target_binding_status: str = (
        "EVALUATION_CANDIDATE_CANONICAL_OWNER_UNAVAILABLE"
    )


@dataclass(frozen=True)
class RelationSemanticAdmissionCaseResultV1:
    case_id: str
    relation_candidate: Dict[str, Any] | None
    projection: Dict[str, Any] | None
    field_event_candidate: Dict[str, Any] | None
    admission: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "RelationBearingFieldSemanticEventProjectionV1",
    "RelationSemanticAdmissionCaseResultV1",
]
