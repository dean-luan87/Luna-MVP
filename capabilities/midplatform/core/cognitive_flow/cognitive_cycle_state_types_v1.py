"""State and lifecycle types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveCycleStateCandidateV1:
    cycle_id: str
    current_state: str
    entry_condition: str
    allowed_source_states: Tuple[str, ...]
    allowed_next_states: Tuple[str, ...]
    transition_authorizer: str
    required_refs: Tuple[str, ...]
    forbidden_side_effects: Tuple[str, ...]
    terminal: bool
    candidate_only: bool = True
    runtime_transition_executed: bool = False
    owner_mutation: bool = False
    trace_ref: str = ""
