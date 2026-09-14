"""Evaluation-only contracts for canonical Field semantic-event projection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class CanonicalFieldSemanticEventProjectionCandidateV1:
    """A canonical observation-event projection, never a Field or World fact."""

    projection_ref: str
    source_visual_projection_ref: str
    source_runtime_observation_ref: str
    source_evidence_refs: Tuple[str, ...]
    source_detection_refs: Tuple[str, ...]
    canonical_event_type: str
    field_ref_candidate: str
    field_ref_resolution_status: str
    state_type: str
    perspective_scope: str
    field_scope: str
    target_type: str
    subject_ref_candidate: Optional[str]
    semantic_state_resolution_status: str
    semantic_value_candidate: Optional[Any]
    observed_object_class_candidate: str
    confidence_candidate: Optional[float]
    temporal_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    fact_admitted: bool = False
    truth_declared: bool = False
    field_mutation: bool = False


@dataclass(frozen=True)
class CanonicalSemanticEventCaseResultV1:
    case_id: str
    visual_projection: Dict[str, Any]
    semantic_projection: CanonicalFieldSemanticEventProjectionCandidateV1
    semantic_event_candidate: Dict[str, Any]
    admission: Any | None
    reducer_result: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "CanonicalFieldSemanticEventProjectionCandidateV1",
    "CanonicalSemanticEventCaseResultV1",
]
