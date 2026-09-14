"""Active Observation Control controlled-integration candidate types v1.

This package extends the existing Field Perception Orchestrator substrate.  It
does not create a semantic owner, execute providers, or mutate downstream
owners.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


CAPABILITY_KINDS = (
    "VISION_DETECTION",
    "REGION_PROPOSAL",
    "OCR_TEXT_EVIDENCE",
    "SLAM_SPATIAL_EVIDENCE",
    "AUDIO_EVIDENCE",
    "USER_INPUT_EVIDENCE",
)
CONTROL_DECISIONS = (
    "STOP",
    "CONTINUE",
    "REDIRECT",
    "SWITCH_PROVIDER",
    "ADD_CAPABILITY",
    "RECONSIDER",
    "DEFER",
    "FAIL",
)
SUFFICIENCY_STATUSES = (
    "SUFFICIENT",
    "INSUFFICIENT",
    "CONTESTED",
    "STALE",
    "NEEDS_CONFIRMATION",
    "NEEDS_ADDITIONAL_MODALITY",
    "NEEDS_REDIRECT",
    "NEEDS_PROVIDER_SWITCH",
)


@dataclass(frozen=True)
class ObservationDemandCandidateV1:
    demand_id: str
    root_cycle_trace_id: str
    source_owner: str
    source_context_refs: Tuple[str, ...]
    source_intent_refs: Tuple[str, ...]
    source_task_refs: Tuple[str, ...]
    source_safety_refs: Tuple[str, ...]
    source_field_refs: Tuple[str, ...]
    information_need: str
    expected_evidence_kinds: Tuple[str, ...]
    target_semantics: str
    spatial_scope_candidate: str
    temporal_scope_candidate: str
    urgency_candidate: str
    priority_candidate: str
    resource_budget_candidate: Dict[str, Any]
    stop_conditions: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationRequestCandidateV1:
    request_id: str
    demand_ref: str
    observation_goal: str
    target_region_candidate: str
    target_semantic_candidate: str
    required_capability_kinds: Tuple[str, ...]
    optional_capability_kinds: Tuple[str, ...]
    forbidden_capability_kinds: Tuple[str, ...]
    evidence_expectation: Tuple[str, ...]
    budget: Dict[str, Any]
    temporal_validity: Dict[str, Any]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityRequirementCandidateV1:
    requirement_id: str
    observation_request_ref: str
    required_capability_kinds: Tuple[str, ...]
    optional_capability_kinds: Tuple[str, ...]
    forbidden_capability_kinds: Tuple[str, ...]
    requirement_reason: str
    target_region_candidate: str
    semantic_scope_candidate: str
    evidence_goal: Tuple[str, ...]
    budget_candidate: Dict[str, Any]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SafetyCriticalObservationExceptionCandidateV1:
    exception_id: str
    explicit_policy_ref: str
    reason: str
    target_scope: str
    capability_scope: Tuple[str, ...]
    bounded_budget: Dict[str, Any]
    temporal_validity: Dict[str, Any]
    revoke_condition: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    general_provider_autonomy: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class BoundedProviderSessionCandidateV1:
    session_id: str
    observation_request_ref: str
    capability_requirement_ref: str
    selected_capability_ref: str
    selected_model_candidate_ref: str
    provider_candidate_ref: str
    region_scope: str
    semantic_scope: str
    evidence_goal: Tuple[str, ...]
    frame_time_budget_candidate: Dict[str, Any]
    retry_budget_candidate: Dict[str, Any]
    resource_budget_candidate: Dict[str, Any]
    start_condition: str
    stop_conditions: Tuple[str, ...]
    revoke_conditions: Tuple[str, ...]
    redirect_allowed: bool
    switch_allowed: bool
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    runtime_execution: bool = False
    provider_invocation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class EvidenceSufficiencyCandidateV1:
    sufficiency_id: str
    information_need_ref: str
    observation_request_ref: str
    expected_evidence: Tuple[str, ...]
    received_evidence_refs: Tuple[str, ...]
    received_evidence_kinds: Tuple[str, ...]
    source_diversity: int
    source_independence_candidate: bool
    contradiction_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    temporal_validity: Dict[str, Any]
    target_coverage: bool
    semantic_coverage: bool
    spatial_coverage: bool
    user_confirmation_required: bool
    user_confirmed: bool
    safety_requirement: bool
    model_confidence_input: float
    status: str
    reason: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationControlDecisionV1:
    decision_id: str
    decision: str
    reason: str
    source_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    budget_state: Dict[str, Any]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    runtime_execution: bool = False
    provider_mutation: bool = False
    downstream_mutation: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class NextCycleIngressCandidateV1:
    ingress_id: str
    source_control_decision_ref: str
    observation_demand_ref: str
    observation_request_ref: str
    feedback_refs: Tuple[str, ...]
    correction_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ActiveObservationTraceV1:
    root_cycle_trace_id: str
    demand_trace_ref: str
    request_trace_ref: str
    attention_trace_ref: str
    capability_trace_ref: str
    session_trace_ref: str
    evidence_trace_refs: Tuple[str, ...]
    gateway_trace_refs: Tuple[str, ...]
    sufficiency_trace_ref: str
    control_trace_ref: str
    next_cycle_trace_ref: str
    provenance_refs: Tuple[str, ...]
    reverse_lookup_path: Tuple[str, ...]
    authority_granted: bool = False


@dataclass(frozen=True)
class ActiveObservationControlResultV1:
    case_id: str
    demand: ObservationDemandCandidateV1
    request: ObservationRequestCandidateV1 | None
    capability_requirement: CapabilityRequirementCandidateV1 | None
    safety_exception: SafetyCriticalObservationExceptionCandidateV1 | None
    provider_session: BoundedProviderSessionCandidateV1 | None
    sufficiency: EvidenceSufficiencyCandidateV1
    control_decision: ObservationControlDecisionV1
    next_cycle_ingress: NextCycleIngressCandidateV1 | None
    trace: ActiveObservationTraceV1
    behavior: Dict[str, Any]
    errors: Tuple[Dict[str, Any], ...] = field(default_factory=tuple)
    negative_guards: Dict[str, bool] = field(default_factory=dict)
    candidate_only: bool = True
    synthetic_only: bool = True
