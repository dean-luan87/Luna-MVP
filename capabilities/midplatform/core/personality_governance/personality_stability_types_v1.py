"""Stability assessment candidates for Personality traits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalityStabilityAssessmentCandidateV1:
    assessment_id: str
    trait_candidate_ref: str
    stability_candidate: str
    repetition: int
    context_diversity: int
    temporal_span: int
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    reason_codes: Tuple[str, ...]
    candidate_only: bool = True


def stability_rank(state: str) -> int:
    return {
        "EMERGING": 0,
        "TENTATIVE": 1,
        "SEMI_STABLE": 2,
        "STABLE_CANDIDATE": 3,
        "CONTESTED": 1,
        "REVISING": 1,
        "SUPERSEDED": -1,
        "REVOKED": -1,
        "EXPIRED": -1,
    }.get(state, -1)
