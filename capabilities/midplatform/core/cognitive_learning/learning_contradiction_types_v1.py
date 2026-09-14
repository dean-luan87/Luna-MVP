"""Contradiction and counterexample candidate types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LearningContradictionCandidateV1:
    contradiction_id: str
    learning_candidate_refs: Tuple[str, ...]
    contradiction_reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class LearningCounterexampleCandidateV1:
    counterexample_id: str
    learning_candidate_refs: Tuple[str, ...]
    counterexample_reason: str
    candidate_only: bool = True
