"""Candidate-only cross-owner evidence interfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalityEvidenceInfluenceCandidateV1:
    influence_id: str
    source_owner: str
    source_refs: Tuple[str, ...]
    evidence_kind: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    source_owner_mutation: bool = False
    target_mutation: bool = False


@dataclass(frozen=True)
class EmotionToPersonalityEvidenceCandidateV1(PersonalityEvidenceInfluenceCandidateV1):
    emotion_refs: Tuple[str, ...] = ()
    emotion_state_mutation: bool = False


@dataclass(frozen=True)
class PersonalityToEmotionContextCandidateV1:
    context_id: str
    personality_candidate_refs: Tuple[str, ...]
    emotion_context_refs: Tuple[str, ...]
    trait_activation: bool = False
    emotional_state_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityEvidenceHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    evidence_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    owner_transfer: bool = False
    candidate_only: bool = True
