"""Immutable Personality Trait Candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class PersonalityTraitCandidateV1:
    trait_candidate_id: str
    trait_dimension: str
    trait_value_candidate: str
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    memory_refs: Tuple[str, ...]
    learning_refs: Tuple[str, ...]
    self_refs: Tuple[str, ...]
    emotion_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    interaction_refs: Tuple[str, ...]
    confidence_candidate: str
    evidence_strength: str
    repetition: int
    context_diversity: int
    temporal_span: int
    stability_candidate: str
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    revision_parent_ref: Optional[str]
    supersedes_ref: Optional[str]
    revocation_refs: Tuple[str, ...]
    sensitivity: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    activated: bool = False
    persisted: bool = False
    truth_declared: bool = False
    source_owner_mutation: bool = False


@dataclass(frozen=True)
class PersonalityTraitExpressionCandidateV1:
    expression_id: str
    trait_candidate_ref: str
    expression_context_refs: Tuple[str, ...]
    emotion_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    structure_mutation: bool = False
    candidate_only: bool = True
