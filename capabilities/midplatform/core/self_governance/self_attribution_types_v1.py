"""Candidate-only self attribution across identity and self-state domains."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SelfAttributionCandidateV1:
    self_attribution_id: str
    self_ref: str
    attribution_domain: str
    attributed_value_candidate_ref: str
    source_owner_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    confidence_candidate: str
    uncertainty_refs: Tuple[str, ...]
    temporal_validity_candidate: str
    revision_parent_ref: str | None
    revocation_parent_ref: str | None
    contradiction_refs: Tuple[str, ...]
    revision_refs: Tuple[str, ...]
    revocation_refs: Tuple[str, ...]
    supersession_refs: Tuple[str, ...]
    state: str
    stability_partition: str
    sensitivity: str
    candidate_only: bool = True
    fact_admitted: bool = False
    persisted: bool = False
    source_owner_mutation: bool = False
    explicit_user_correction: bool = False
