"""Revision, revocation, supersession, expiration, retention candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MemoryRevisionCandidateV1:
    revision_id: str
    prior_memory_candidate_ref: str
    new_memory_candidate_ref: str
    reason: str
    trace_ref: str


@dataclass(frozen=True)
class MemorySupersessionCandidateV1:
    supersession_id: str
    superseded_memory_candidate_ref: str
    superseding_memory_candidate_ref: str
    reason: str
    trace_ref: str


@dataclass(frozen=True)
class MemoryRevocationCandidateV1:
    revocation_id: str
    memory_candidate_ref: str
    reason: str
    contradiction_refs: Tuple[str, ...]
    trace_ref: str


@dataclass(frozen=True)
class MemoryExpirationCandidateV1:
    expiration_id: str
    memory_candidate_ref: str
    temporal_reason: str
    trace_ref: str
