"""Trace and provenance candidates for Causal Governance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CausalTraceCandidateV1:
    trace_id: str
    owner: str
    hypothesis_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance: Tuple[str, ...]
    opposition_refs: Tuple[str, ...]
    confounder_refs: Tuple[str, ...]
    temporal_order_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    prior_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    influence_refs: Tuple[str, ...]
    uncertainty: Tuple[str, ...]
    confidence_candidate: str
    conflict_refs: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    counterfactual_refs: Tuple[str, ...]
    revision_chain_refs: Tuple[str, ...]
    parent_trace_refs: Tuple[str, ...]
    admission_steps: Tuple[str, ...]
    handoff_refs: Tuple[str, ...]
    candidate_only: bool = True
