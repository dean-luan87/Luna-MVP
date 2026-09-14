"""Candidate-only provider runtime bridge contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


PROVIDER_RESULT_STATUSES = ("SUCCESS", "EMPTY_SUCCESS", "UNAVAILABLE", "REJECTED", "ERROR")


@dataclass(frozen=True)
class ProviderRuntimeRequestV1:
    provider_request_ref: str
    observation_demand_ref: str
    observation_request_ref: str
    capability_requirement_ref: str
    capability_ref: str
    provider_ref: str
    model_ref: str | None
    execution_instance_ref: str
    input_source_ref: str
    modality: str
    temporal_ref: str | None
    spatial_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    execution_mode: str = "LIVE_RUNTIME"
    candidate_only: bool = True
    invocation_requested: bool = False


@dataclass(frozen=True)
class ProviderRuntimeResultV1:
    provider_result_ref: str
    provider_request_ref: str
    provider_ref: str
    capability_ref: str
    model_ref: str | None
    execution_instance_ref: str
    modality: str
    output_ref: str
    raw_result_ref: str
    status: str
    confidence_candidate: float | None
    quality_candidate: float | None
    temporal_ref: str | None
    spatial_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    empty_result: bool = False
    candidate_only: bool = True
    truth_declared: bool = False
    provider_invoked: bool = False
    model_invoked: bool = False
    output_candidate: Dict[str, Any] | None = None
    error_category: str | None = None


@dataclass(frozen=True)
class ProviderObservationIngressCaseV1:
    case_id: str
    title: str
    capability_kind: str
    capability_ref: str
    modality: str
    input_source_ref: str
    execution_instance_ref: str
    information_need_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    context_ref: str
    intent_ref: str
    task_ref: str
    goal_ref: str
    concern_ref: str
    role_refs: Tuple[str, ...]
    field_refs: Tuple[str, ...]
    relation_refs: Tuple[str, ...]
    source_ref: str
    raw_result_ref: str
    confidence_candidate: float = 0.85
    quality_candidate: float = 0.80
    spatial_refs: Tuple[str, ...] = ()
    temporal_ref: str | None = None
    expected_evidence_kinds: Tuple[str, ...] = ()
    next_cycle_requested: bool = False
    provider_result_status: str = "SUCCESS"
    # Optional upper-layer cognitive-loop bindings.  Empty defaults preserve
    # the original one-shot OCR execution behavior.
    observation_information_refs: Tuple[str, ...] = ()
    evidence_information_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()
    inherited_information_refs: Tuple[str, ...] = ()
    cycle_index: int = 1
    prior_current_world_ref: str | None = None
    prior_hypothesis_refs: Tuple[str, ...] = ()
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: object | None = None
    prior_information_gap_candidate: object | None = None
    prior_reobservation_candidate: object | None = None


@dataclass(frozen=True)
class ProviderRuntimeObservationResultV1:
    case_id: str
    capability_requirement_ref: str | None
    capability_resolution_status: str | None
    provider_request: ProviderRuntimeRequestV1 | None
    provider_result: ProviderRuntimeResultV1 | None
    runtime_observation_ref: str | None
    gateway_admission_ref: str | None
    a_route_execution_ref: str | None
    sufficiency_ref: str | None
    information_gap_ref: str | None
    stop_ref: str | None
    demand_ref: str | None
    observation_request_ref: str | None
    reobservation_request_ref: str | None
    next_cycle_ingress_ref: str | None
    evidence_refs: Tuple[str, ...] = ()
    errors: Tuple[str, ...] = field(default_factory=tuple)
    provider_runtime_contract_verified: bool = False
    provider_real_execution_verified: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    details: Dict[str, Any] = field(default_factory=dict)
