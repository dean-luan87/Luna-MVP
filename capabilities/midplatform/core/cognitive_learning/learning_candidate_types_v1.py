"""Learning candidate types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LearningCandidateV1:
    learning_candidate_id: str
    learning_evidence_refs: Tuple[str, ...]
    learning_kind: str
    candidate_statement: str
    scope: str
    confidence_candidate: str
    generalization_level_candidate: str
    transferability_candidate: str
    reversibility_candidate: str
    uncertainty_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    temporal_validity_candidate: str
    revision_of_ref: str | None
    supersedes_ref: str | None
    revoked_ref: str | None
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    truth_declared: bool = False
