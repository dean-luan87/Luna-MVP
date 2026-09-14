"""Trace candidates for Intent Governance v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class IntentTraceCandidateV1:
    trace_id: str
    scenario_id: str
    source_refs: Tuple[str, ...]
    potential_intent_ids: Tuple[str, ...]
    intent_candidate_ids: Tuple[str, ...]
    interaction_ids: Tuple[str, ...]
    carryover_ids: Tuple[str, ...]
    resource_constraint_id: str
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    omissions: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
