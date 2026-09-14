"""Candidate-only types for bounded B Contingency Reasoning (B-CR)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class ABContingencyTriggerCandidateV1:
    trigger_ref: str
    work_ref: str
    concern_ref: str
    source_a_state_version_ref: str
    source_need_ref: str
    source_hypothesis_refs: Tuple[str, ...]
    uncertainty_ref: str
    uncertainty_type: str
    reason_refs: Tuple[str, ...]
    expected_information_value_ref: str
    a_grant_ref: str
    issuing_owner_ref: str = "A_REASONING_ROLE"
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class BContingencyRequestCandidateV1:
    request_ref: str
    work_ref: str
    concern_ref: str
    source_a_state_version_ref: str
    trigger_ref: str
    contingency_question_ref: str
    scenario_scope_refs: Tuple[str, ...]
    assumption_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    depth_limit: int
    branch_limit: int
    resource_envelope_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    required_result_refs: Tuple[str, ...]
    termination_condition_refs: Tuple[str, ...]
    a_grant_ref: str
    derived_b_grant_ref: str
    result_receiver_ref: str = "A_REASONING_ROLE"
    responsibility_owner_ref: str = "A_REASONING_ROLE"
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class BReasoningEnvelopeCandidateV1:
    work_ref: str
    concern_ref: str
    goal_refs: Tuple[str, ...]
    intent_refs: Tuple[str, ...]
    role_refs: Tuple[str, ...]
    perspective_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    current_world_refs: Tuple[str, ...]
    task_behavior_refs: Tuple[str, ...]
    emotion_modulation_refs: Tuple[str, ...]
    experience_refs: Tuple[str, ...]
    source_a_need_ref: str
    source_a_hypothesis_refs: Tuple[str, ...]
    source_a_expectation_refs: Tuple[str, ...]
    source_a_evidence_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    scenario_scope_refs: Tuple[str, ...]
    assumption_refs: Tuple[str, ...]
    depth_limit: int
    branch_limit: int
    safety_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_envelope_refs: Tuple[str, ...]
    source_a_state_version_ref: str
    derived_b_grant_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class BContingencyResultCandidateV1:
    result_ref: str
    request_ref: str
    work_ref: str
    concern_ref: str
    source_a_state_version_ref: str
    scenario_candidate_refs: Tuple[str, ...]
    conditional_response_candidate_refs: Tuple[str, ...]
    assumption_refs: Tuple[str, ...]
    uncertainty_boundary_refs: Tuple[str, ...]
    result_confidence_ref: str
    result_limit_refs: Tuple[str, ...]
    termination_reason_ref: str
    derived_b_grant_ref: str
    result_owner_ref: str = "B_CONTINGENCY_ROLE"
    result_receiver_ref: str = "A_REASONING_ROLE"
    binding: bool = False
    world_truth_declared: bool = False
    decision_created: bool = False
    action_created: bool = False
    additional_contingency_need_ref: Optional[str] = None
    new_concern_suggestion_ref: Optional[str] = None
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ABResultEvaluationCandidateV1:
    evaluation_ref: str
    b_result_ref: str
    current_a_state_version_ref: str
    current_world_refs: Tuple[str, ...]
    current_need_ref: str
    current_hypothesis_refs: Tuple[str, ...]
    evaluation_disposition: str
    adopted_candidate_refs: Tuple[str, ...]
    discarded_candidate_refs: Tuple[str, ...]
    stale_b_result_refs: Tuple[str, ...]
    reason_refs: Tuple[str, ...]
    a_grant_ref: str
    decision_owner_ref: str = "A_REASONING_ROLE"
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ABReasoningHandoffCandidateV1:
    handoff_ref: str
    request_ref: str
    result_ref: str
    source_a_state_version_ref: str
    b_completion_status: str
    scenario_refs: Tuple[str, ...]
    conditional_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    result_receiver_ref: str = "A_REASONING_ROLE"
    direct_brain_handoff: bool = False
    direct_loop_handoff: bool = False
    direct_task_handoff: bool = False
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ABConcurrentStateCandidateV1:
    work_ref: str
    concern_ref: str
    a_state_ref: str
    b_request_ref: str
    b_state_ref: str
    a_active: bool
    b_active: bool
    a_owns_current_reality_reasoning: bool = True
    b_owns_bounded_contingency_reasoning: bool = True
    shared_read_only_refs: Tuple[str, ...] = field(default_factory=tuple)
    isolated_local_refs: Tuple[str, ...] = field(default_factory=tuple)
    scheduler_execution: bool = False
    thread_execution: bool = False
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class ABContingencyValidationCandidateV1:
    validation_ref: str
    validation_kind: str
    accepted: bool
    failure_class: Optional[str]
    source_owner_ref: str
    result_receiver_ref: str
    concern_scope_ok: bool
    work_scope_ok: bool
    state_version_ok: bool
    authority_scope_ok: bool
    grant_active: bool
    b_loop_control: bool = False
    b_recursive_delegation: bool = False
    b_concern_creation: bool = False
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    synthetic_only: bool = True


__all__ = [
    "ABContingencyTriggerCandidateV1",
    "BContingencyRequestCandidateV1",
    "BReasoningEnvelopeCandidateV1",
    "BContingencyResultCandidateV1",
    "ABResultEvaluationCandidateV1",
    "ABReasoningHandoffCandidateV1",
    "ABConcurrentStateCandidateV1",
    "ABContingencyValidationCandidateV1",
]
