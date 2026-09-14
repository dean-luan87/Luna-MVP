"""Revision, revocation, supersession, and expiration lineage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfRevisionCandidateV1:
    revision_id: str
    prior_candidate_ref: str
    revised_candidate_ref: str
    trigger: str
    reason: str
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    explicit_user_correction: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class SelfRevocationCandidateV1:
    revocation_id: str
    candidate_ref: str
    trigger: str
    reason: str
    contradiction_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SelfSupersessionCandidateV1:
    supersession_id: str
    superseded_candidate_ref: str
    superseding_candidate_ref: str
    reason: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SelfExpirationCandidateV1:
    expiration_id: str
    candidate_ref: str
    temporal_reason: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


def user_correction_precedes_other_revision(explicit_user_correction: bool) -> bool:
    return explicit_user_correction is True
