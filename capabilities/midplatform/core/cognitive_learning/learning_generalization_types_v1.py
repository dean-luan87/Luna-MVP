"""Generalization and confidence support types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GeneralizationAssessmentCandidateV1:
    assessment_id: str
    generalization_level_candidate: str
    evidence_diversity_sufficient: bool
    counterexample_blocking: bool
    contradiction_visible: bool
    candidate_only: bool = True
