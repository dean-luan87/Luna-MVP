"""Candidate-only contracts for cross-frame visual relation evidence."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class MultiFrameVisualObservationV1:
    frame_ref: str
    source_ref: str
    runtime_observation_ref: Optional[str]
    provider_request_ref: Optional[str]
    provider_result_ref: Optional[str]
    temporal_ref: Optional[str]
    detection_ref: Optional[str]
    class_label: Optional[str]
    confidence: Optional[float]
    frame_width: Optional[int]
    frame_height: Optional[int]
    bbox: Optional[Tuple[float, float, float, float]]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CrossFrameTargetAssociationCandidateV1:
    association_ref: str
    frame_a_ref: str
    frame_b_ref: str
    detection_a_ref: str
    detection_b_ref: str
    association_basis: Tuple[str, ...]
    association_confidence_candidate: Optional[float]
    semantic_identity_resolved: bool
    physical_identity_declared: bool
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class TemporalVisualRelationMetricsV1:
    metrics_ref: str
    frame_a_ref: str
    frame_b_ref: str
    normalized_center_a: Tuple[float, float]
    normalized_center_b: Tuple[float, float]
    normalized_size_a: Tuple[float, float]
    normalized_size_b: Tuple[float, float]
    area_ratio_a: float
    area_ratio_b: float
    delta_center: Tuple[float, float]
    delta_center_distance: float
    delta_size: Tuple[float, float]
    delta_area: float
    temporal_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class VisualRelationStabilityCandidateV1:
    stability_ref: str
    association_ref: str
    metrics_ref: str
    status: str
    threshold_ref: Optional[str]
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


__all__ = [
    "CrossFrameTargetAssociationCandidateV1",
    "MultiFrameVisualObservationV1",
    "TemporalVisualRelationMetricsV1",
    "VisualRelationStabilityCandidateV1",
]
