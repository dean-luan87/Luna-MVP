"""Evidence support/opposition relation candidates for Causal Governance."""

from __future__ import annotations

from dataclasses import dataclass


EVIDENCE_RELATION_TYPES_V1 = ("SUPPORT", "OPPOSITION", "NEUTRAL")


@dataclass(frozen=True)
class CausalEvidenceRelationCandidateV1:
    relation_id: str
    hypothesis_ref: str
    evidence_ref: str
    relation_type: str
    confidence_candidate: str
    temporal_validity_ref: str
    provenance: str
