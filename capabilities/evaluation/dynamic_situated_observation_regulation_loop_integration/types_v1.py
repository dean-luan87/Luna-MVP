"""Candidate-only contracts for a bounded Situated Observation regulation loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class DynamicObservationRegulationStateV1:
    """One finite regulation state; it does not authorize physical action."""

    regulation_ref: str
    case_id: str
    state_id: str
    cycle_index: int
    # Regulation state ordering is not a Cognitive Observation cycle.  This
    # is populated only when this state actually admits a Provider observation.
    observation_cycle_index: int | None
    capability_need_ref: str
    information_need_ref: str
    capability_requirement_ref: str
    current_situated_state_ref: str
    feasibility_ref: str
    condition_gap_refs: Tuple[str, ...]
    adjustment_need_refs: Tuple[str, ...]
    opportunity_ref: str
    eligibility_ref: str
    execution_admission_ref: str | None
    provider_result_ref: str | None
    runtime_observation_ref: str | None
    gateway_admission_ref: str | None
    evidence_refs: Tuple[str, ...]
    a_route_execution_ref: str | None
    cognitive_state_ref: str | None
    sufficiency_ref: str | None
    sufficiency_status: str | None
    information_gap_ref: str | None
    stop_ref: str | None
    regulation_status: str
    temporal_ref: str
    previous_regulation_ref: str | None
    provider_execution_admitted: bool
    provider_real_execution_attempted: bool
    provider_real_execution_verified: bool
    provider_invoked: bool
    model_invoked: bool
    provider_invocation_count: int
    model_invocation_count: int
    recorded_provider_result_used: bool
    situated_precondition_result: object
    execution_admission: object | None
    provider_runtime_result: object | None
    execution_events: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class DynamicObservationRegulationCaseResultV1:
    """Bounded state sequence for one unchanged cognitive need."""

    case_id: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    information_need_ref: str
    capability_requirement_ref: str
    states: Tuple[DynamicObservationRegulationStateV1, ...]
    observation_cycle_count: int
    real_provider_invocation_count: int
    final_regulation_status: str
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


__all__ = [
    "DynamicObservationRegulationCaseResultV1",
    "DynamicObservationRegulationStateV1",
]
