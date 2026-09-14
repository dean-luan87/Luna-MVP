"""Core immutable candidate types."""

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class ExpectedOutcomeInputV1:
    expectation_ref: str
    expectation_kind: str
    source_owner: str
    source_ref: str
    target_ref: str
    semantic_scope: str
    temporal_scope: str
    spatial_scope: str
    expected_attributes: Tuple[str, ...] = ()
    completion_criteria: Tuple[str, ...] = ()
    expected_value: Optional[str] = None
    supersedes_ref: Optional[str] = None
    revocation_ref: Optional[str] = None
    uncertainty_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    truth_declared: bool = False


@dataclass(frozen=True)
class ActualResultInputV1:
    actual_result_ref: str
    source_owner: str
    source_ref: str
    result_kind: str
    target_ref: str
    observed_at: str
    valid_from: str
    valid_until: Optional[str]
    status_candidate: str
    observed_attributes: Tuple[str, ...] = ()
    actual_value: Optional[str] = None
    uncertainty_refs: Tuple[str, ...] = ()
    contradiction_refs: Tuple[str, ...] = ()
    correction_refs: Tuple[str, ...] = ()
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = ()
    source_valid: bool = True
    candidate_only: bool = True
    truth_declared: bool = False


@dataclass(frozen=True)
class ComparabilityGateCandidateV1:
    comparability_id: str
    state: str
    expectation_ref: str
    actual_result_ref: str
    checks_passed: Tuple[str, ...]
    blocked_reason_refs: Tuple[str, ...]
    comparison_basis_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    authority: bool = False


@dataclass(frozen=True)
class DeviationCandidateV1:
    deviation_id: str
    expectation_ref: str
    actual_result_ref: str
    comparability_ref: str
    status: str
    dimension_statuses: Tuple[str, ...]
    comparison_basis_refs: Tuple[str, ...]
    magnitude_candidate: Optional[str]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterevidence_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    revision_parent_ref: Optional[str] = None
    supersedes_ref: Optional[str] = None
    revocation_ref: Optional[str] = None
    candidate_only: bool = True
    authority: bool = False


@dataclass(frozen=True)
class AttributionCandidateV1:
    attribution_id: str
    attribution_kind: str
    support_refs: Tuple[str, ...]
    counterevidence_refs: Tuple[str, ...]
    related_expectation_refs: Tuple[str, ...]
    related_actual_result_refs: Tuple[str, ...]
    confidence_candidate: str
    uncertainty_refs: Tuple[str, ...]
    competing_attribution_refs: Tuple[str, ...]
    partial_cause_refs: Tuple[str, ...]
    revision_parent_ref: Optional[str]
    supersedes_ref: Optional[str]
    revocation_ref: Optional[str]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    owner_wrong_declared: bool = False


@dataclass(frozen=True)
class ReconsiderationHandoffCandidateV1:
    reconsideration_id: str
    evaluation_ref: str
    recommendation: str
    reason_refs: Tuple[str, ...]
    expected_refs: Tuple[str, ...]
    actual_refs: Tuple[str, ...]
    attribution_refs: Tuple[str, ...]
    budget_state: str
    reconsideration_depth_candidate: int
    max_depth_ref: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    executes_reconsideration: bool = False


@dataclass(frozen=True)
class LearningSignalHandoffCandidateV1:
    learning_signal_id: str
    evaluation_ref: str
    deviation_refs: Tuple[str, ...]
    attribution_refs: Tuple[str, ...]
    outcome_refs: Tuple[str, ...]
    feedback_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    counterexample_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    status: str
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    learning_executed: bool = False


@dataclass(frozen=True)
class ObservationNeedHandoffCandidateV1:
    observation_need_id: str
    evaluation_ref: str
    information_gap: str
    expected_evidence_kinds: Tuple[str, ...]
    target_scope: str
    temporal_scope: str
    budget_candidate: str
    stop_conditions: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    consumer_owner: str = "Field Perception Orchestrator / Active Observation Control"
    candidate_only: bool = True
    provider_invocation: bool = False


@dataclass(frozen=True)
class TraceProvenanceV1:
    root_cycle_trace_id: str
    evaluation_trace_id: str
    comparison_trace_id: str
    expected_trace_refs: Tuple[str, ...]
    actual_trace_refs: Tuple[str, ...]
    attribution_trace_refs: Tuple[str, ...]
    reconsideration_trace_refs: Tuple[str, ...]
    learning_signal_trace_refs: Tuple[str, ...]
    observation_need_trace_refs: Tuple[str, ...]
    source_owner_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    correction_lineage: Tuple[str, ...]
    contradiction_lineage: Tuple[str, ...]
    reverse_lookup: Tuple[Tuple[str, Tuple[str, ...]], ...]
    provenance_grants_authority: bool = False


@dataclass(frozen=True)
class IdempotencyGuardCandidateV1:
    guard_id: str
    guard_kind: str
    signature: str
    triggered: bool
    action: str
    candidate_only: bool = True


@dataclass(frozen=True)
class OutcomeEvaluationRequestV1:
    scenario_id: str
    root_cycle_trace_id: str
    expected: ExpectedOutcomeInputV1
    actual: ActualResultInputV1
    intended_status: str = "MATCH"
    evidence_sufficient: bool = True
    contradictory: bool = False
    needs_confirmation: bool = False
    temporal_status: str = "WITHIN_TEMPORAL_WINDOW"
    schema_comparable: bool = True
    target_comparable: bool = True
    spatial_comparable: bool = True
    user_correction_ref: Optional[str] = None
    correction_precedence: bool = False
    superseded_expectation: bool = False
    revoked_actual: bool = False
    attribution_kinds: Tuple[str, ...] = ()
    recommendation: str = "NO_ACTION"
    observation_information_gap: Optional[str] = None
    expected_evidence_kinds: Tuple[str, ...] = ()
    duplicate_kinds: Tuple[str, ...] = ()
    completed_evaluation: bool = False
    reconsideration_depth: int = 0
    max_reconsideration_depth: int = 3
    learning_signal_allowed: bool = True
    task_completion_candidate: str = ""
    context_refs: Tuple[str, ...] = ()
    intent_refs: Tuple[str, ...] = ()
    hypothesis_refs: Tuple[str, ...] = ()
    current_world_refs: Tuple[str, ...] = ()
    feedback_refs: Tuple[str, ...] = ()
    counterexample_refs: Tuple[str, ...] = ()
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class OutcomeEvaluationOutputV1:
    scenario_id: str
    comparability: ComparabilityGateCandidateV1
    deviation: DeviationCandidateV1
    evaluation: "OutcomeEvaluationCandidateV1"
    attributions: Tuple[AttributionCandidateV1, ...]
    reconsideration: Optional[ReconsiderationHandoffCandidateV1]
    learning_signal: Optional[LearningSignalHandoffCandidateV1]
    observation_need: Optional[ObservationNeedHandoffCandidateV1]
    idempotency_guards: Tuple[IdempotencyGuardCandidateV1, ...]
    trace: TraceProvenanceV1
    guards: dict[str, bool] = field(default_factory=dict)


@dataclass(frozen=True)
class OutcomeEvaluationCandidateV1:
    evaluation_id: str
    root_cycle_trace_id: str
    expected_outcome_refs: Tuple[str, ...]
    actual_result_refs: Tuple[str, ...]
    comparability_ref: str
    deviation_refs: Tuple[str, ...]
    intended_outcome_observed_candidate: str
    task_completion_candidate: str
    action_effect_observed_candidate: str
    world_change_observed_candidate: str
    evidence_sufficiency_candidate: str
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    attribution_candidate_refs: Tuple[str, ...]
    reconsideration_candidate_refs: Tuple[str, ...]
    learning_signal_candidate_refs: Tuple[str, ...]
    observation_need_candidate_refs: Tuple[str, ...]
    evaluation_status: str
    correction_refs: Tuple[str, ...]
    revision_parent_ref: Optional[str]
    supersedes_ref: Optional[str]
    revocation_ref: Optional[str]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    schema_version: str
    contract_version: str
    candidate_only: bool = True
    truth_declared: bool = False
    mutation_authority: bool = False
