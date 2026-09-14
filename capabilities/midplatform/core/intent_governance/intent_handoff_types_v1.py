"""Intent-to-Causal handoff candidate types for Intent Governance v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class IntentToCausalHandoffCandidateV1:
    handoff_id: str
    producer_owner: str
    consumer_owner: str
    intent_candidate_refs: Tuple[str, ...]
    potential_intent_refs: Tuple[str, ...]
    competition_refs: Tuple[str, ...]
    suppression_refs: Tuple[str, ...]
    temporary_dominance_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    pcn_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    relationship_refs: Tuple[str, ...]
    resource_ref: str
    provenance: Tuple[str, ...]
    uncertainty: Tuple[str, ...] = field(default_factory=tuple)
    handoff_reason_candidate: str = ""
    candidate_only: bool = True
    causal_explanation: bool = False
    decision_output: bool = False
    action_output: bool = False
    task_output: bool = False
