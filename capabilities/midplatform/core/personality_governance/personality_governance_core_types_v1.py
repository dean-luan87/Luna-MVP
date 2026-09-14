"""Shared immutable references for Personality Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalitySourceReferenceV1:
    source_owner: str
    source_ref: str
    source_kind: str
    trace_ref: str
    provenance_ref: str
    context_refs: Tuple[str, ...] = ()
    read_only: bool = True
    candidate_only: bool = True
    source_owner_mutation: bool = False


@dataclass(frozen=True)
class PersonalityEvidenceSummaryV1:
    evidence_id: str
    evidence_kind: str
    source_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    temporal_span: int
    repetition: int
    user_correction: bool = False
    user_confirmed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityBoundaryStatusV1:
    source_owner_mutation: bool = False
    self_mutation: bool = False
    memory_mutation: bool = False
    learning_execution: bool = False
    intent_mutation: bool = False
    pcn_mutation: bool = False
    emotion_mutation: bool = False
    regulation_parameter_mutation: bool = False
    trait_activation: bool = False
    semantic_compression_execution: bool = False
    cross_user_transfer: bool = False
