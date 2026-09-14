"""Local candidate and observability types for the controlled return-path slice.

These types are integration records. They do not replace Field, Current World,
Outcome, Brain, Provider, Action, or Evidence owner types.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class ResultSourceInputV1:
    source_result_ref: str
    result_kind: str
    status_candidate: str
    source_version_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    target_ref: Optional[str]
    concern_ref: Optional[str]
    observed_time: str
    effective_time_ref: Optional[str]
    uncertainty_refs: Tuple[str, ...]
    confidence_candidate: Optional[str]
    provenance_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...] = ()
    source_valid: bool = True
    synthetic_only: bool = True
    candidate_only: bool = True
    provider_invocation_executed: bool = False
    action_execution_executed: bool = False


@dataclass(frozen=True)
class OutcomeSourceInputV1:
    outcome_candidate_ref: str
    outcome_version: str
    goal_refs: Tuple[str, ...]
    concern_ref: Optional[str]
    grant_ref: Optional[str]
    decision_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    action_result_refs: Tuple[str, ...]
    a_local_evaluation_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    evaluation_status: str
    partiality: str
    uncertainty_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    followup_candidate_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    brain_adjudication_executed: bool = False
    brain_state_mutation: bool = False
    intent_mutation: bool = False
    task_mutation: bool = False
    memory_mutation: bool = False
    experience_mutation: bool = False


@dataclass(frozen=True)
class SourceStateHandoffCandidateV1:
    handoff_id: str
    handoff_version: str
    source_result_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    target_boundary: str
    target_ref: Optional[str]
    source_version_refs: Tuple[str, ...]
    expected_target_version_ref: Optional[str]
    effective_time_ref: Optional[str]
    observed_time: str
    uncertainty_refs: Tuple[str, ...]
    confidence_candidate: Optional[str]
    status_candidate: str
    provenance_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    authority_owner: str
    responsibility_owner: str
    candidate_only: bool = True
    source_mutation_authorized: bool = False
    world_truth_declared: bool = False
    field_reducer_executed: bool = False
    current_world_authoritative_write: bool = False


@dataclass(frozen=True)
class CurrentWorldUpdateCandidateV1:
    update_ref: str
    handoff_ref: str
    current_world_candidate_ref: str
    evidence_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    status_candidate: str
    candidate_only: bool = True
    world_truth_declared: bool = False
    authoritative_write: bool = False


@dataclass(frozen=True)
class FieldEventCandidateAdapterV1:
    event_candidate_ref: str
    handoff_ref: str
    field_ref: Optional[str]
    evidence_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    effective_time_ref: Optional[str]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    status_candidate: str
    candidate_only: bool = True
    admitted: bool = False
    reducer_executed: bool = False
    field_mutation: bool = False


@dataclass(frozen=True)
class BrainAdjudicationInputCandidateV1:
    input_ref: str
    input_version: str
    outcome_candidate_ref: str
    outcome_version: str
    goal_refs: Tuple[str, ...]
    concern_ref: str
    grant_ref: str
    decision_refs: Tuple[str, ...]
    task_refs: Tuple[str, ...]
    action_result_refs: Tuple[str, ...]
    a_local_evaluation_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    evaluation_status: str
    partiality: str
    uncertainty_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    followup_candidate_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Brain Governance"
    responsibility_owner: str = "Outcome→Brain input adapter"
    candidate_only: bool = True
    brain_adjudication_executed: bool = False
    brain_state_mutation: bool = False
    intent_mutation: bool = False
    task_mutation: bool = False
    memory_mutation: bool = False
    experience_mutation: bool = False


@dataclass(frozen=True)
class EdgeObservabilityCandidateV1:
    transition_id: str
    trace_id: str
    parent_transition_refs: Tuple[str, ...]
    concern_ref: Optional[str]
    reasoning_cycle_ref: Optional[str]
    producer: str
    consumer: str
    authority_owner: str
    responsibility_owner: str
    transition_class: str
    input_refs: Tuple[str, ...]
    input_versions: Tuple[str, ...]
    output_refs: Tuple[str, ...]
    output_versions: Tuple[str, ...]
    admission_or_validation_status: str
    constraint_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    failure_classification: Optional[str]
    blocker_refs: Tuple[str, ...]
    next_target: str
    source_mutation_executed: bool = False
    runtime_execution_executed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class AuthorityGuardsV1:
    source_mutation_executed: bool = False
    world_truth_declared: bool = False
    field_reducer_executed: bool = False
    current_world_authoritative_write: bool = False
    brain_adjudication_executed: bool = False
    brain_state_mutation: bool = False
    intent_mutation: bool = False
    task_mutation: bool = False
    memory_mutation: bool = False
    experience_mutation: bool = False
    learning_execution: bool = False
    provider_invocation_executed: bool = False
    action_execution_executed: bool = False
    runtime_execution: bool = False


@dataclass(frozen=True)
class AdapterFailureV1:
    failure_ref: str
    classification: str
    reason: str
    responsible_owner: str
    next_target: str
    source_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SourceStateReturnOutputV1:
    handoff: Optional[SourceStateHandoffCandidateV1]
    current_world_update: Optional[CurrentWorldUpdateCandidateV1]
    field_event: Optional[FieldEventCandidateAdapterV1]
    current_world_candidate_ref: Optional[str]
    edge: EdgeObservabilityCandidateV1
    guards: AuthorityGuardsV1
    failure: Optional[AdapterFailureV1]


@dataclass(frozen=True)
class BrainInputReturnOutputV1:
    input_candidate: Optional[BrainAdjudicationInputCandidateV1]
    edge: EdgeObservabilityCandidateV1
    guards: AuthorityGuardsV1
    failure: Optional[AdapterFailureV1]

