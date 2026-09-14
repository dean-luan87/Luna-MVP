"""Candidate-only state update boundary for the cognitive loop."""
from __future__ import annotations

from typing import Any, Mapping

from docs.runtime.luna_cognitive_runtime_foundation_impl_v1.state_container import StateContainer

from .decision_candidate_flow import DecisionCandidate


class StateUpdateBoundary:
    """Only runtime-owned candidate state may be written by this adapter."""

    def apply_candidate(self, state: StateContainer, candidate: DecisionCandidate, context_id: str):
        runtime = state.read_domain("runtime")
        runtime["last_cognitive_context_id"] = context_id
        runtime["last_decision_candidate"] = candidate.to_dict()
        runtime["candidate_state"] = True
        return state.update("runtime", runtime, reason="cognitive candidate update")
