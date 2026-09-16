from __future__ import annotations

from typing import Iterable, Tuple

from .observation_gateway_core_types_v1 import (
    ADMISSION_STATES,
    INGRESS_TYPES,
    ROUTING_TARGETS,
    ObservationCandidateV1,
    ObservationGatewayNegativeGuardsV1,
    ObservationIngressCandidateV1,
    ObservationIngressRequestV1,
    PerceptionEvidenceV1,
    RuntimeObservationEnvelopeV1,
)


def _valid_ref_collection(value: object, *, allow_empty: bool = True) -> bool:
    """Validate a collection representation without treating strings as collections."""
    if not isinstance(value, (list, tuple)):
        return False
    if not allow_empty and not value:
        return False
    return all(isinstance(item, str) and bool(item.strip()) for item in value)


def validate_ingress_request_shape(request: ObservationIngressRequestV1) -> Tuple[str, ...]:
    """Validate raw ingress shape before any evidence/candidate formation."""
    if not isinstance(request, ObservationIngressRequestV1):
        return ("request_must_be_observation_ingress_request",)
    errors = []
    collection_fields = (
        "evidence_refs", "spatial_refs", "routing_targets",
        "required_information_refs", "available_information_refs",
        "inherited_information_refs", "prior_hypothesis_refs",
    )
    for name in collection_fields:
        if not _valid_ref_collection(getattr(request, name), allow_empty=True):
            errors.append(f"{name}_must_be_string_collection")
    if not isinstance(request.evidence_information_refs, (list, tuple)):
        errors.append("evidence_information_refs_must_be_collection")
    else:
        for index, item in enumerate(request.evidence_information_refs):
            if (
                not isinstance(item, (list, tuple)) or len(item) != 2
                or not isinstance(item[0], str) or not item[0].strip()
                or not _valid_ref_collection(item[1], allow_empty=True)
            ):
                errors.append(f"evidence_information_refs[{index}]_shape_invalid")
    runtime = request.runtime_observation
    if runtime is not None:
        for name in ("provenance_refs", "trace_refs", "spatial_refs", "context_refs"):
            if not _valid_ref_collection(getattr(runtime, name), allow_empty=True):
                errors.append(f"runtime_observation.{name}_must_be_string_collection")
    replay = request.replay_input
    if replay is not None:
        for name in (
            "evidence_refs", "provenance_refs", "ordering_refs",
            "required_information_refs", "available_information_refs",
            "prior_hypothesis_refs",
        ):
            if not _valid_ref_collection(getattr(replay, name), allow_empty=True):
                errors.append(f"replay_input.{name}_must_be_string_collection")
    return tuple(dict.fromkeys(errors))
from .observation_gateway_trace_types_v1 import ObservationGatewayTraceV1
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
    SYNTHETIC_CONTROLLED,
)


def validate_ingress(ingress: ObservationIngressCandidateV1) -> bool:
    return bool(
        ingress.ingress_id and ingress.ingress_type in INGRESS_TYPES
        and ingress.provider_ref and ingress.source_ref and ingress.payload_ref
        and ingress.temporal_ref and ingress.trace_ref and ingress.provenance_refs
        and ingress.candidate_only
    )


def validate_evidence(evidence: PerceptionEvidenceV1) -> bool:
    return bool(
        evidence.evidence_id and evidence.source_provider and evidence.source_capability
        and evidence.raw_output_ref and evidence.source_temporal_ref
        and evidence.trace_ref and evidence.provenance_refs
        and evidence.candidate_only and evidence.fact_declared is False
    )


def validate_observation(observation: ObservationCandidateV1) -> bool:
    return bool(
        observation.observation_id and observation.evidence_refs
        and observation.admission_state in ADMISSION_STATES
        and all(target in ROUTING_TARGETS for target in observation.routing_targets)
        and observation.trace_ref and observation.provenance_refs
        and observation.candidate_only and observation.truth_declared is False
    )


def validate_trace(trace: ObservationGatewayTraceV1) -> bool:
    return bool(
        trace.root_trace_id and trace.a_route_ingress_ref
        and trace.observation_trace_ref
        and (trace.evidence_trace_refs or trace.observation_trace_ref == "not-formed")
        and (trace.provider_trace_refs or trace.observation_trace_ref == "not-formed")
        and trace.source_input_refs
        and trace.provenance_refs and trace.reverse_lookup_path
        and trace.authority_granted is False and trace.candidate_only
    )


def validate_runtime_observation_envelope(
    envelope: RuntimeObservationEnvelopeV1 | None,
) -> bool:
    if envelope is None:
        return False
    required = (
        envelope.observation_id,
        envelope.execution_instance_ref,
        envelope.provider_ref,
        envelope.capability_ref,
        envelope.modality,
        envelope.source_ref,
        envelope.raw_result_ref,
        envelope.temporal_ref,
        envelope.observed_at,
        envelope.provenance_refs,
    )
    return (
        all(bool(value) for value in required)
        and envelope.modality in INGRESS_TYPES
        and envelope.result_status in {"AVAILABLE", "UNAVAILABLE"}
        and envelope.candidate_only is True
        and envelope.truth_declared is False
        and (envelope.confidence_candidate is None or 0.0 <= envelope.confidence_candidate <= 1.0)
        and (envelope.quality_candidate is None or 0.0 <= envelope.quality_candidate <= 1.0)
    )


def validate_runtime_observation_admission(admission: object) -> bool:
    required = (
        getattr(admission, "gateway_admission_ref", None),
        getattr(admission, "runtime_observation_ref", None),
        getattr(admission, "execution_instance_ref", None),
        getattr(admission, "observation_ref", None),
        getattr(admission, "evidence_refs", None),
        getattr(admission, "provenance_refs", None),
        getattr(admission, "gateway_trace_ref", None),
    )
    return bool(
        all(required)
        and getattr(admission, "admission_state", None) == "ADMITTED_OBSERVATION"
        and getattr(admission, "owner_ref", None) == "Observation Gateway Governance"
        and getattr(admission, "candidate_only", None) is True
        and getattr(admission, "world_truth_declared", None) is False
        and getattr(admission, "model_invocation", None) is False
        and getattr(admission, "provider_invocation", None) is False
        and getattr(admission, "live_observation_execution", None) is False
    )


def validate_negative_guards(guards: ObservationGatewayNegativeGuardsV1) -> bool:
    return all(
        value is False
        for name, value in vars(guards).items()
        if name not in {"synthetic_only", "controlled_integration_only", "execution_mode"}
    ) and guards.controlled_integration_only and (
        (guards.execution_mode == SYNTHETIC_CONTROLLED and guards.synthetic_only)
        or (guards.execution_mode == CONTROLLED_REPLAY_RUNTIME and not guards.synthetic_only)
        or (guards.execution_mode == LIVE_RUNTIME and (
            not guards.synthetic_only
            or (guards.synthetic_only and guards.controlled_integration_only)
        ))
    )


def validate_supported_ingress_types(values: Iterable[str]) -> bool:
    return set(values) == set(INGRESS_TYPES)
