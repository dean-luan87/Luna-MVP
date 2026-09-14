"""Reverse-locatable trace and provenance candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalityTraceV1:
    trace_id: str
    root_cycle_trace_id: str
    cognitive_cycle_ref: str
    personality_evidence_refs: Tuple[str, ...]
    trait_candidate_refs: Tuple[str, ...]
    profile_candidate_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    memory_refs: Tuple[str, ...]
    learning_refs: Tuple[str, ...]
    self_refs: Tuple[str, ...]
    emotion_refs: Tuple[str, ...]
    regulation_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    supersession_refs: Tuple[str, ...]
    revocation_refs: Tuple[str, ...]
    expiration_refs: Tuple[str, ...]
    reverse_locatable: bool = True
    provenance_grants_authority: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityProvenanceV1:
    provenance_id: str
    source_owner: str
    original_source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    owner_trace_refs: Tuple[str, ...]
    source_owner_mutation: bool = False
    reverse_locatable: bool = True
    candidate_only: bool = True
