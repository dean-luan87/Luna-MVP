"""Inheritance and future insertion boundary types for Cognitive Flow controlled implementation v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CycleInheritanceCandidateV1:
    cycle_id: str
    next_cycle_id: str
    inherited_refs: Tuple[str, ...]
    prohibited_refs_rejected: Tuple[str, ...]
    candidate_only: bool = True
    mutable_runtime_state_inherited: bool = False
    trace_ref: str = ""


@dataclass(frozen=True)
class CognitiveMemoryObservationCandidateV1:
    cycle_id: str
    cycle_summary_candidate: str
    salient_cognitive_event_candidate: str
    hypothesis_resolution_candidate: str
    intent_evolution_candidate: str
    current_world_transition_candidate: str
    regulation_outcome_candidate: str
    unresolved_uncertainty_candidate: str
    memory_write: bool = False
    memory_fact_creation: bool = False
    memory_owner_transfer: bool = False
    candidate_only: bool = True
    trace_ref: str = ""


@dataclass(frozen=True)
class FutureLearningHandoffCandidateV1:
    cycle_id: str
    experience_candidate_ref: str
    learning_candidate_ref: str
    parameter_update_candidate_ref: str
    learning_execution: bool = False
    parameter_mutation: bool = False
    genome_activation: bool = False
    intent_mutation: bool = False
    state_mutation: bool = False
    candidate_only: bool = True
    trace_ref: str = ""
