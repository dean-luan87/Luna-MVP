"""Causal-to-Decision handoff candidate types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CausalToDecisionHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    handoff_kind: str
    causal_hypothesis_refs: Tuple[str, ...]
    supporting_evidence_refs: Tuple[str, ...]
    opposing_evidence_refs: Tuple[str, ...]
    uncertainty: Tuple[str, ...]
    provenance: Tuple[str, ...]
    alternative_hypothesis_refs: Tuple[str, ...]
    unresolved_conflict_refs: Tuple[str, ...]
    counterfactual_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    decision_executed: bool = False
    action_triggered: bool = False
    task_created: bool = False
