"""Core candidate types for Causal Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class SourceRefV1:
    owner: str
    ref_id: str
    ref_type: str = "REFERENCE"
    read_only: bool = True
    reference_only: bool = True
    source_mutation_allowed: bool = False


@dataclass(frozen=True)
class UncertaintyEnvelopeV1:
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    confidence_candidate: str = "LOW"
    confidence_not_truth: bool = True
    unresolved_conflicts: Tuple[str, ...] = field(default_factory=tuple)
    insufficient_evidence_flag: bool = False


@dataclass(frozen=True)
class CausalHypothesisCandidateV1:
    hypothesis_id: str
    owner: str
    candidate_kind: str
    hypothesis_statement: str
    target_event_refs: Tuple[SourceRefV1, ...]
    cause_candidate_refs: Tuple[SourceRefV1, ...]
    evidence_support_refs: Tuple[SourceRefV1, ...]
    evidence_opposition_refs: Tuple[SourceRefV1, ...]
    confounder_refs: Tuple[SourceRefV1, ...]
    temporal_order_refs: Tuple[SourceRefV1, ...]
    uncertainty: UncertaintyEnvelopeV1
    alternative_hypothesis_refs: Tuple[SourceRefV1, ...]
    state_candidate: str
    provenance: Tuple[SourceRefV1, ...]
    trace_ref: str
    decision_authority: bool = False
    action_authority: bool = False
    task_authority: bool = False
    candidate_only: bool = True
