"""Self reference candidates; these are not identity truth or memory facts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from .self_governance_registry_v1 import CANONICAL_OWNER


@dataclass(frozen=True)
class SelfReferenceCandidateV1:
    candidate_id: str
    source_owner: str
    reference_kind: str
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    temporal_validity: str
    uncertainty: str
    sensitivity: str
    self_ref_id: str
    self_id_ref: str
    identity_ref: str | None
    subject_boundary_class: str
    confidence_candidate: str
    uncertainty_refs: Tuple[str, ...]
    temporal_validity_candidate: str
    candidate_only: bool = True
    fact_admitted: bool = False
    persisted: bool = False
    source_owner_mutation: bool = False

    @property
    def owner(self) -> str:
        return CANONICAL_OWNER
