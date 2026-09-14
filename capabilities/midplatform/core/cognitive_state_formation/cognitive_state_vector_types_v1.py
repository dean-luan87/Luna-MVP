"""Cognitive state vector candidate types for controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CognitiveStateVectorCandidateV1:
    state_vector_id: str
    attention_distribution_refs: Tuple[str, ...]
    hypothesis_state_refs: Tuple[str, ...]
    uncertainty_level_candidate: str
    conflict_level_candidate: str
    world_stability_candidate: str
    intent_pressure_candidate: str
    resource_pressure_candidate: str
    current_world_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    parameter_mutation: bool = False
    adaptive_update: bool = False
    self_regulation_execution: bool = False
    learning_update: bool = False
