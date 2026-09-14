"""Transition and relationship types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveCycleTransitionCandidateV1:
    cycle_id: str
    source_state: str
    target_state: str
    transition_reason: str
    required_refs: Tuple[str, ...]
    relationship_kind: str
    transition_candidate_only: bool = True
    runtime_transition_executed: bool = False
    owner_mutation: bool = False
    trace_ref: str = ""


@dataclass(frozen=True)
class ReconsiderationCandidateV1:
    cycle_id: str
    source_stage: str
    target_stage: str
    reconsideration_reason: str
    related_refs: Tuple[str, ...]
    candidate_only: bool = True
    runtime_execution: bool = False
    trace_ref: str = ""
