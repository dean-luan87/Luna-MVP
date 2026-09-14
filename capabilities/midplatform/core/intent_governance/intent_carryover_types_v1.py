"""Carryover candidates across context/field transitions for Intent Governance v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class IntentCarryoverCandidateV1:
    carryover_id: str
    intent_candidate_id: str
    source_context_ref: str
    target_context_ref: str
    continuity_support_refs: Tuple[str, ...]
    decay_or_amplification_candidate: str
    state_candidate: str
    unknowns: Tuple[str, ...] = field(default_factory=tuple)
    provenance: Tuple[str, ...] = field(default_factory=tuple)
    trace: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    context_switch_forces_termination: bool = False
