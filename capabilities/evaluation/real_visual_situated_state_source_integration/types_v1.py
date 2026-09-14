"""Evaluation-only contracts for projecting real visual output into situated state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class VisualTargetBindingCandidateV1:
    """Candidate correlation; it does not establish semantic target truth."""

    binding_ref: str
    target_requirement_ref: str
    target_ref: str
    detection_ref: str
    source_ref: str
    semantic_target_resolved: bool
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class RealVisualSituatedStateSourceV1:
    """A real visual provider projection consumed by existing preconditions."""

    source_ref: str
    runtime_observation_ref: str | None
    evidence_refs: Tuple[str, ...]
    detection_ref: str | None
    target_binding_ref: str
    frame_width: int | None
    frame_height: int | None
    bbox: Tuple[float, float, float, float] | None
    target_visibility_candidate: str
    target_completeness_candidate: str
    target_scale_metrics: Dict[str, float]
    target_scale_condition_status: str
    stable_relation_status: str
    condition_state_candidate_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class VisualSituatedCaseResultV1:
    """One bounded source projection and its existing precondition result."""

    case_id: str
    source: RealVisualSituatedStateSourceV1
    target_binding: VisualTargetBindingCandidateV1
    perception: object
    precondition_result: object
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "RealVisualSituatedStateSourceV1",
    "VisualSituatedCaseResultV1",
    "VisualTargetBindingCandidateV1",
]
