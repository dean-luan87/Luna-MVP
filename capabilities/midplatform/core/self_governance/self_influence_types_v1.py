"""Read-only evidence interfaces to other owners."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfEvidenceInfluenceCandidateV1:
    influence_id: str
    source_owner: str
    source_refs: Tuple[str, ...]
    evidence_kind: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    source_owner_mutation: bool = False
    semantic_compression_execution: bool = False


@dataclass(frozen=True)
class SelfEvolutionEvidenceCandidateV1(SelfEvidenceInfluenceCandidateV1):
    evidence_kind: str
    activates_self_state: bool = False


@dataclass(frozen=True)
class EmotionEvidenceToSelfCandidateV1(SelfEvidenceInfluenceCandidateV1):
    evidence_kind: str


@dataclass(frozen=True)
class SelfContextToEmotionCandidateV1(SelfEvidenceInfluenceCandidateV1):
    evidence_kind: str


@dataclass(frozen=True)
class ReadOnlyOwnerInfluenceV1(SelfEvidenceInfluenceCandidateV1):
    read_only: bool = True
