"""Read-only influence and handoff types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MemoryRetrievalCandidateV1:
    memory_ref: str
    retrieval_reason: str
    relevance_candidate: str
    confidence_reference_status: str
    temporal_status: str
    contradiction_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    context_mutation: bool = False
    field_mutation: bool = False
    current_world_truth_declaration: bool = False


@dataclass(frozen=True)
class MemoryInfluenceCandidateV1:
    influence_id: str
    target_owner: str
    target_kind: str
    memory_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    influence_reason: str
    candidate_only: bool = True
    target_mutation: bool = False


@dataclass(frozen=True)
class LearningEvidenceCandidateV1:
    learning_evidence_id: str
    memory_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    learning_execution: bool = False
    parameter_mutation: bool = False
    genome_activation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class SelfPersonalityEvolutionEvidenceCandidateV1:
    evidence_id: str
    memory_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    personality_mutation: bool = False
    self_model_mutation: bool = False
    identity_mutation: bool = False
    automatic_trait_change: bool = False
    candidate_only: bool = True
