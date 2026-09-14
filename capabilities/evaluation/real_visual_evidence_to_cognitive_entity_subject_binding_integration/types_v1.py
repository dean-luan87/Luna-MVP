"""Evaluation-only contracts for visual evidence to L1 entity binding."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class VisualEvidenceSubjectBindingCandidateV1:
    """A candidate-only link from visual evidence to an entity candidate."""

    binding_ref: str
    entity_candidate_ref: str
    source_runtime_observation_ref: str
    source_evidence_refs: Tuple[str, ...]
    source_detection_refs: Tuple[str, ...]
    field_ref_candidate: str
    binding_status: str
    identity_resolution_status: str
    target_binding_status: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    fact_admitted: bool = False
    truth_declared: bool = False
    field_mutation: bool = False


@dataclass(frozen=True)
class EntitySubjectBindingCaseResultV1:
    case_id: str
    entity_candidate: Dict[str, Any] | None
    subject_binding: Dict[str, Any] | None
    semantic_projection: Dict[str, Any] | None
    semantic_event_candidate: Dict[str, Any] | None
    admission: Any | None
    reducer_result: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "EntitySubjectBindingCaseResultV1",
    "VisualEvidenceSubjectBindingCandidateV1",
]

