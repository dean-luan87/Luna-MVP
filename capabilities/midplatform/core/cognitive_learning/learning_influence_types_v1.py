"""Optional future evidence/influence candidate types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfEvolutionEvidenceCandidateV1:
    evidence_id: str
    learning_candidate_refs: Tuple[str, ...]
    self_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityEvolutionEvidenceCandidateV1:
    evidence_id: str
    learning_candidate_refs: Tuple[str, ...]
    personality_mutation: bool = False
    trait_activation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class EmotionEngineEvidenceCandidateV1:
    evidence_id: str
    learning_candidate_refs: Tuple[str, ...]
    emotional_state_mutation: bool = False
    candidate_only: bool = True
