"""Parameter Genome Candidate types; never an active genome or identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveParameterGenomeCandidateV1:
    genome_candidate_id: str
    version: str
    parameter_refs: Tuple[str, ...]
    parameter_class_refs: Tuple[str, ...]
    field_scope: str
    evidence_refs: Tuple[str, ...]
    risk_refs: Tuple[str, ...]
    rollback_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    user_scope_ref: str
    candidate_only: bool = True
    active: bool = False
    persisted: bool = False
    model_weights_rewritten: bool = False
    user_identity_modified: bool = False
    cross_user_propagated: bool = False
    learned_truth: bool = False
