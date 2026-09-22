from __future__ import annotations

from dataclasses import dataclass, field
import weakref
from typing import Dict, Mapping, Tuple, Union

from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    SYNTHETIC_CONTROLLED,
    ControlledReplayAdmissionV1,
    ControlledReplayInputV1,
)

SCHEMA_VERSION = "observation-gateway-schema-v1"
CONTRACT_VERSION = "observation-gateway-contract-v1"
INGRESS_TYPES = (
    "USER_INPUT", "VISION", "OCR", "AUDIO", "SLAM_SPATIAL", "FIELD_REFERENCE",
    "SYSTEM_EVENT", "EXTERNAL_PROVIDER",
)
ADMISSION_STATES = (
    "RECEIVED", "NORMALIZED", "EVIDENCE_READY", "OBSERVATION_CANDIDATE_READY",
    "NEEDS_CONFIRMATION", "CONTESTED", "ADMITTED_OBSERVATION", "REJECTED",
    "REVOKED", "EXPIRED", "SUPERSEDED",
)
ROUTING_TARGETS = (
    "Context", "Field / World State", "Attention", "Hypothesis",
    "Intent influence path", "Safety / Permission", "Cognitive Flow",
    "A Route Orchestration",
)


@dataclass(frozen=True)
class ObservationIngressCandidateV1:
    ingress_id: str
    ingress_type: str
    provider_ref: str
    source_ref: str
    payload_ref: str
    temporal_ref: str
    observed_at: str
    valid_from_candidate: str
    valid_until_candidate: str
    confidence_candidate: float
    quality_candidate: float
    sensitivity: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION
    candidate_only: bool = True


@dataclass(frozen=True)
class PerceptionEvidenceV1:
    evidence_id: str
    evidence_type: str
    source_provider: str
    source_capability: str
    source_model_ref: str | None
    source_region_ref: str | None
    source_temporal_ref: str
    raw_output_ref: str
    confidence_candidate: float
    quality_candidate: float
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    correction_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    sensitivity: str
    schema_version: str = SCHEMA_VERSION
    contract_version: str = CONTRACT_VERSION
    candidate_only: bool = True
    fact_declared: bool = False
    candidate_payload: Mapping[str, object] | None = None
    empty_result: bool = False


@dataclass(frozen=True)
class EvidenceReferenceBindingV1:
    """Read-only Evidence projection derived from a Gateway admission."""

    gateway_admission_ref: str
    evidence_refs: Tuple[str, ...]
    owner_ref: str = "Observation Gateway Governance"
    binding_kind: str = "ADMITTED_EVIDENCE"
    candidate_only: bool = True


@dataclass(frozen=True)
class GatewayAdmissionStateRecordV1:
    """The governed fact that Gateway admitted Evidence for one execution."""

    execution_identity_ref: str
    gateway_admission_ref: str
    evidence_refs: Tuple[str, ...]
    admission_state: str = "ADMITTED"
    execution_mode: str = SYNTHETIC_CONTROLLED
    trace_refs: Tuple[str, ...] = ()
    provenance_refs: Tuple[str, ...] = ()


class ObservationGatewayAdmissionRuntimeStateV1:
    """Gateway-owned, execution-scoped mutable admission store.

    This type is an owner-internal root.  It must never be placed in a proof,
    DTO, or downstream handoff.  Downstream consumers use the separate
    ``ObservationGatewayAdmissionQueryV1`` surface instead.
    """

    __slots__ = ("_records", "_canonical_admissions")

    def __init__(self) -> None:
        self._records: Dict[Tuple[str, str], GatewayAdmissionStateRecordV1] = {}
        self._canonical_admissions: Dict[Tuple[str, str], object] = {}

    def _record_admission(
        self,
        *,
        execution_identity_ref: str,
        gateway_admission_ref: str,
        evidence_refs: Tuple[str, ...],
        execution_mode: str,
        trace_refs: Tuple[str, ...] = (),
        provenance_refs: Tuple[str, ...] = (),
        canonical_admission: object | None = None,
    ) -> bool:
        """Record one Gateway-owned transition, preserving exact key data."""

        if not execution_identity_ref or not gateway_admission_ref or not evidence_refs:
            return False
        normalized_refs = tuple(evidence_refs)
        if any(not isinstance(ref, str) or not ref for ref in normalized_refs):
            return False
        if len(set(normalized_refs)) != len(normalized_refs):
            return False
        record = GatewayAdmissionStateRecordV1(
            execution_identity_ref=execution_identity_ref,
            gateway_admission_ref=gateway_admission_ref,
            evidence_refs=normalized_refs,
            execution_mode=execution_mode,
            trace_refs=tuple(trace_refs),
            provenance_refs=tuple(provenance_refs),
        )
        key = (execution_identity_ref, gateway_admission_ref)
        previous = self._records.get(key)
        if previous is not None:
            return previous == record and self._canonical_admissions.get(key) is canonical_admission
        self._records[key] = record
        if canonical_admission is not None:
            self._canonical_admissions[key] = canonical_admission
        return True

    def lookup(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
    ) -> GatewayAdmissionStateRecordV1 | None:
        """Read the Gateway admission fact for an exact execution scope."""

        return self._records.get((execution_identity_ref, gateway_admission_ref))

    def matches_canonical_admission(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
        admission: object,
    ) -> bool:
        """Check the Gateway-produced admission object for this state key."""

        key = (execution_identity_ref, gateway_admission_ref)
        return self._records.get(key) is not None and self._canonical_admissions.get(key) is admission

    def __copy__(self):
        return type(self)()

    def __deepcopy__(self, memo):
        return type(self)()


class ObservationGatewayAdmissionQueryV1:
    """Owner-mediated read surface for current Gateway admission state."""

    __slots__ = ("__query_identity", "__weakref__")

    def __init__(self) -> None:
        self.__query_identity = object()

    @classmethod
    def _from_gateway_owner(
        cls, state: ObservationGatewayAdmissionRuntimeStateV1
    ) -> "ObservationGatewayAdmissionQueryV1":
        query = cls()
        _GATEWAY_QUERY_BINDINGS[query] = state
        return query

    def lookup(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
    ) -> GatewayAdmissionStateRecordV1 | None:
        if (
            not isinstance(execution_identity_ref, str)
            or not execution_identity_ref
            or not isinstance(gateway_admission_ref, str)
            or not gateway_admission_ref
        ):
            return None
        state = _GATEWAY_QUERY_BINDINGS.get(self)
        if state is None:
            return None
        record = state.lookup(execution_identity_ref, gateway_admission_ref)
        return record if isinstance(record, GatewayAdmissionStateRecordV1) else None

    def matches_canonical_admission(
        self,
        execution_identity_ref: str,
        gateway_admission_ref: str,
        admission: object,
    ) -> bool:
        if self.lookup(execution_identity_ref, gateway_admission_ref) is None:
            return False
        state = _GATEWAY_QUERY_BINDINGS.get(self)
        if state is None:
            return False
        return state.matches_canonical_admission(
            execution_identity_ref, gateway_admission_ref, admission
        ) is True

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        memo[id(self)] = self
        return self

    def __getstate__(self) -> dict:
        return {"state_surface": "gateway_admission_query_only"}

    def __setstate__(self, _state: object) -> None:
        raise TypeError("gateway_admission_query_is_not_deserializable")


_GATEWAY_QUERY_BINDINGS: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()
_GATEWAY_OWNER_QUERIES: weakref.WeakSet = weakref.WeakSet()


def _register_gateway_owner_query(query: ObservationGatewayAdmissionQueryV1) -> None:
    """Register a query identity issued by the Gateway engine."""

    if isinstance(query, ObservationGatewayAdmissionQueryV1):
        _GATEWAY_OWNER_QUERIES.add(query)


def resolve_owner_bound_gateway_record(
    query: object,
    execution_identity_ref: str,
    gateway_admission_ref: str,
) -> tuple[GatewayAdmissionStateRecordV1, object | None] | None:
    """Resolve owner state and its canonical admission identity.

    The binding map is populated only by the Gateway owner construction path.
    Resolution reads that owner-bound state directly without invoking
    caller-overridable query methods.
    """

    try:
        if query not in _GATEWAY_OWNER_QUERIES:
            return None
        state = _GATEWAY_QUERY_BINDINGS.get(query)
    except TypeError:
        return None
    if state is None:
        return None
    record = state.lookup(execution_identity_ref, gateway_admission_ref)
    if not isinstance(record, GatewayAdmissionStateRecordV1):
        return None
    canonical_admission = state._canonical_admissions.get(
        (execution_identity_ref, gateway_admission_ref)
    )
    return record, canonical_admission


def resolve_owner_bound_gateway_admission(
    query: object,
    execution_identity_ref: str,
    gateway_admission_ref: str,
    admission: object,
) -> GatewayAdmissionStateRecordV1 | None:
    """Resolve Gateway truth and require the canonical admission identity."""

    resolution = resolve_owner_bound_gateway_record(
        query,
        execution_identity_ref,
        gateway_admission_ref,
    )
    if resolution is None:
        return None
    record, canonical_admission = resolution
    return record if canonical_admission is admission else None


@dataclass(frozen=True)
class ObservationCandidateV1:
    observation_id: str
    observation_type: str
    evidence_refs: Tuple[str, ...]
    subject_candidate: str | None
    attribute_candidate: str | None
    relation_candidate: str | None
    spatial_refs: Tuple[str, ...]
    temporal_refs: Tuple[str, ...]
    uncertainty_refs: Tuple[str, ...]
    contradiction_refs: Tuple[str, ...]
    correction_refs: Tuple[str, ...]
    admission_state: str
    routing_targets: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    sensitivity: str
    candidate_only: bool = True
    truth_declared: bool = False


@dataclass(frozen=True)
class RuntimeObservationEnvelopeV1:
    """Reference-only envelope for an already-produced runtime observation.

    The envelope describes provider output; it does not invoke the provider or
    grant semantic authority.  Optional modality fields remain unavailable
    when a provider does not supply them.
    """

    observation_id: str
    execution_instance_ref: str
    provider_ref: str
    capability_ref: str
    modality: str
    source_ref: str
    raw_result_ref: str
    temporal_ref: str
    observed_at: str
    provenance_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...] = ()
    confidence_candidate: float | None = None
    quality_candidate: float | None = None
    source_model_ref: str | None = None
    source_region_ref: str | None = None
    spatial_refs: Tuple[str, ...] = ()
    context_refs: Tuple[str, ...] = ()
    provider_available: bool = True
    capability_available: bool = True
    result_status: str = "AVAILABLE"
    candidate_only: bool = True
    truth_declared: bool = False
    empty_result: bool = False
    output_candidate: Mapping[str, object] | None = None


@dataclass(frozen=True)
class ObservationGatewayRuntimeAdmissionV1:
    """Gateway-owned admission proof for a LIVE_RUNTIME observation."""

    gateway_admission_ref: str
    runtime_observation_ref: str
    execution_instance_ref: str
    observation_ref: str
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    gateway_trace_ref: str
    evidence_binding: EvidenceReferenceBindingV1 | None = None
    admission_state: str = "ADMITTED_OBSERVATION"
    owner_ref: str = "Observation Gateway Governance"
    candidate_only: bool = True
    world_truth_declared: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    live_observation_execution: bool = False
    cycle_index: int = 1
    required_information_refs: Tuple[str, ...] = ()
    available_information_refs: Tuple[str, ...] = ()
    requirement_establishment_status: str = "NOT_ESTABLISHED"
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None
    evidence_information_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = ()
    inherited_information_refs: Tuple[str, ...] = ()
    prior_current_world_ref: str | None = None
    prior_hypothesis_refs: Tuple[str, ...] = ()
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: object | None = None
    prior_information_gap_candidate: object | None = None
    prior_reobservation_candidate: object | None = None
    required_cognitive_condition_formation_result: object | None = None
    contradiction_refs: Tuple[str, ...] = ()


CanonicalGatewayAdmissionResultV1 = Union[
    ObservationGatewayRuntimeAdmissionV1,
    ControlledReplayAdmissionV1,
]


@dataclass(frozen=True)
class ObservationIngressRequestV1:
    scenario_id: str
    ingress_type: str = "USER_INPUT"
    provider_ref: str = "provider:synthetic"
    source_ref: str = "source:synthetic"
    payload_ref: str = "payload:synthetic"
    temporal_ref: str = "temporal:synthetic"
    observed_at: str = "2026-08-13T00:00:00Z"
    valid_from_candidate: str = "2026-08-13T00:00:00Z"
    valid_until_candidate: str = ""
    confidence_candidate: float = 0.8
    quality_candidate: float = 0.8
    sensitivity: str = "NORMAL"
    source_model_ref: str | None = None
    source_region_ref: str | None = None
    correction_ref: str = ""
    corrected_evidence_ref: str = ""
    corrected_observation_ref: str = ""
    evidence_refs: Tuple[str, ...] = ()
    spatial_refs: Tuple[str, ...] = ()
    routing_targets: Tuple[str, ...] = ("A Route Orchestration",)
    missing_provider: bool = False
    missing_provenance: bool = False
    invalid_ingress: bool = False
    contract_mismatch: bool = False
    version_mismatch: bool = False
    duplicate_ingress: bool = False
    duplicate_evidence: bool = False
    duplicate_observation: bool = False
    duplicate_correction: bool = False
    duplicate_refresh: bool = False
    revocation_replay: bool = False
    expiration_replay: bool = False
    supersession_replay: bool = False
    needs_confirmation: bool = False
    contested: bool = False
    rejected: bool = False
    revoked: bool = False
    expired: bool = False
    superseded: bool = False
    refresh: bool = False
    user_correction: bool = False
    multi_evidence_agreement: bool = False
    multi_evidence_contradiction: bool = False
    uncertainty: bool = False
    route_to_field: bool = False
    route_to_context: bool = False
    route_to_attention: bool = False
    route_to_orchestration: bool = True
    emotion_deferred: bool = False
    b_route_deferred: bool = False
    semantic_compression_deferred: bool = False
    synthetic_only: bool = True
    controlled_integration_only: bool = True
    candidate_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED
    execution_identity_ref: str | None = None
    replay_input: ControlledReplayInputV1 | None = None
    runtime_observation: RuntimeObservationEnvelopeV1 | None = None
    required_information_refs: Tuple[str, ...] = ()
    available_information_refs: Tuple[str, ...] = ()
    requirement_establishment_status: str = "NOT_ESTABLISHED"
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None
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
    required_cognitive_condition_formation_result: object | None = None


@dataclass(frozen=True)
class ObservationGatewayNegativeGuardsV1:
    gateway_can_execute_vision: bool = False
    gateway_can_execute_ocr: bool = False
    gateway_can_execute_slam: bool = False
    gateway_can_execute_audio_model: bool = False
    gateway_can_mutate_field_state: bool = False
    gateway_can_mutate_context: bool = False
    gateway_can_mutate_attention: bool = False
    gateway_can_mutate_hypothesis: bool = False
    gateway_can_mutate_intent: bool = False
    gateway_can_mutate_decision: bool = False
    gateway_can_mutate_task: bool = False
    gateway_can_mutate_memory: bool = False
    gateway_can_execute_learning: bool = False
    gateway_can_mutate_self: bool = False
    gateway_can_mutate_personality: bool = False
    gateway_can_mutate_emotion: bool = False
    observation_is_world_truth: bool = False
    ocr_evidence_is_fact: bool = False
    visual_detection_is_fact: bool = False
    slam_geometry_is_semantic_truth: bool = False
    database_write: bool = False
    vector_store_write: bool = False
    embedding_execution: bool = False
    model_call: bool = False
    scheduler_execution: bool = False
    device_control: bool = False
    real_side_effect: bool = False
    cross_user_transfer: bool = False
    emotion_engine_execution: bool = False
    b_route_execution: bool = False
    semantic_compression_execution: bool = False
    synthetic_only: bool = True
    controlled_integration_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED


@dataclass(frozen=True)
class ObservationGatewayResultV1:
    scenario_id: str
    ingress: ObservationIngressCandidateV1 | None
    evidence: Tuple[PerceptionEvidenceV1, ...]
    observation: ObservationCandidateV1 | None
    admission_state: str
    route_status: str
    route_refs: Tuple[str, ...]
    errors: Tuple[object, ...]
    trace: "ObservationGatewayTraceV1"
    negative_guards: ObservationGatewayNegativeGuardsV1 = field(default_factory=ObservationGatewayNegativeGuardsV1)
    deferred_refs: Tuple[str, ...] = ()
    candidate_only: bool = True
    synthetic_only: bool = True
    execution_mode: str = SYNTHETIC_CONTROLLED
    replay_input_ref: str | None = None
    replay_admission: ControlledReplayAdmissionV1 | None = None
    runtime_admission: ObservationGatewayRuntimeAdmissionV1 | None = None
