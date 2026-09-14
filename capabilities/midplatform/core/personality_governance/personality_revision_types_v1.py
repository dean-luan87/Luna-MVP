"""Revision, supersession, revocation, and expiration lineage candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PersonalityRevisionCandidateV1:
    revision_id: str
    prior_candidate_ref: str
    revised_candidate_ref: str
    reason_codes: Tuple[str, ...]
    correction_precedence: bool
    trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalitySupersessionCandidateV1:
    supersession_id: str
    superseded_candidate_ref: str
    superseding_candidate_ref: str
    trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityRevocationCandidateV1:
    revocation_id: str
    revoked_candidate_ref: str
    revocation_refs: Tuple[str, ...]
    trace_ref: str
    idempotent: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class PersonalityExpirationCandidateV1:
    expiration_id: str
    expired_candidate_ref: str
    temporal_scope: str
    trace_ref: str
    candidate_only: bool = True
