"""Trace and provenance candidates for Decision Governance controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DecisionTraceCandidateV1:
    trace_id: str
    owner: str
    decision_candidate_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    causal_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    risk_refs: Tuple[str, ...]
    utility_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    resource_state_refs: Tuple[str, ...]
    alternative_option_refs: Tuple[str, ...]
    rejected_alternative_refs: Tuple[str, ...]
    selection_or_nonselection_reason_refs: Tuple[str, ...]
    state_transition_refs: Tuple[str, ...]
    revision_lineage_refs: Tuple[str, ...]
    provenance: Tuple[str, ...]
    candidate_only: bool = True
