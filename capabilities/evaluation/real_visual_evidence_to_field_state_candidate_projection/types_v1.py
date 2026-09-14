"""Evaluation-only contracts for the visual-evidence to Field boundary."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class VisualEvidenceFieldProjectionCandidateV1:
    """A Field-compatible candidate projection, never Field truth."""

    projection_ref: str
    source_runtime_observation_ref: str
    source_evidence_refs: Tuple[str, ...]
    source_detection_refs: Tuple[str, ...]
    field_ref_candidate: str
    field_ref_resolution_status: str
    region_ref_candidate: str
    region_semantics: str
    observation_type: str
    object_class_candidate: str
    frame_width: int | None
    frame_height: int | None
    bbox_candidate: Tuple[float, float, float, float]
    confidence_candidate: float | None
    temporal_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    truth_declared: bool = False
    field_mutation: bool = False


@dataclass(frozen=True)
class FieldProjectionCaseResultV1:
    case_id: str
    projection: VisualEvidenceFieldProjectionCandidateV1
    event_candidate: Dict[str, Any] | None
    admission: Any | None
    reducer_adapter: Any | None
    reducer_result: Dict[str, Any] | None
    field_state_candidate: Dict[str, Any] | None
    behavior: Dict[str, Any]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "FieldProjectionCaseResultV1",
    "VisualEvidenceFieldProjectionCandidateV1",
]
