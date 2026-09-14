"""Candidate-only Observation Planning types v1."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ObservationPlanningCandidateV1:
    planning_id: str
    observation_type: str
    context_reference: str
    field_reference: str
    attention_reference: str
    goal_reference: str
    survival_constraint_reference: str
    information_gap_reference: str
    provenance_reference: str
    trace_reference: str
    candidate_only: bool = True
    not_fact: bool = True
    not_state: bool = True
    not_decision: bool = True
    not_action: bool = True
    not_memory: bool = True
