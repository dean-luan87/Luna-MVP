"""Normalize provider results into the existing Gateway runtime envelope."""

from __future__ import annotations

from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    RuntimeObservationEnvelopeV1,
)

from .types_v1 import ProviderRuntimeRequestV1, ProviderRuntimeResultV1


def validate_provider_result(
    request: ProviderRuntimeRequestV1,
    result: ProviderRuntimeResultV1,
) -> tuple[str, ...]:
    errors = []
    for value, error in (
        (result.provider_result_ref, "provider_result_ref_missing"),
        (result.output_ref, "provider_result_output_ref_missing"),
        (result.raw_result_ref, "provider_result_raw_result_ref_missing"),
    ):
        if not value:
            errors.append(error)
    if result.provider_request_ref != request.provider_request_ref:
        errors.append("provider_result_request_ref_mismatch")
    if result.provider_ref != request.provider_ref:
        errors.append("provider_result_provider_ref_mismatch")
    if result.capability_ref != request.capability_ref:
        errors.append("provider_result_capability_ref_mismatch")
    if result.execution_instance_ref != request.execution_instance_ref:
        errors.append("provider_result_execution_identity_mismatch")
    if result.modality != request.modality:
        errors.append("provider_result_modality_mismatch")
    if result.status not in {"SUCCESS", "EMPTY_SUCCESS", "UNAVAILABLE", "REJECTED", "ERROR"}:
        errors.append("provider_result_status_invalid")
    if not result.candidate_only:
        errors.append("provider_result_not_candidate_only")
    if result.truth_declared:
        errors.append("provider_result_declares_truth")
    if (result.provider_invoked or result.model_invoked) and request.execution_mode != "LIVE_RUNTIME":
        errors.append("provider_invocation_requires_live_runtime")
    for value in (result.confidence_candidate, result.quality_candidate):
        if value is not None and not 0.0 <= value <= 1.0:
            errors.append("provider_result_quality_out_of_range")
    return tuple(errors)


def provider_result_to_runtime_observation(
    request: ProviderRuntimeRequestV1,
    result: ProviderRuntimeResultV1,
) -> tuple[RuntimeObservationEnvelopeV1 | None, tuple[str, ...]]:
    errors = validate_provider_result(request, result)
    if errors or result.status not in {"SUCCESS", "EMPTY_SUCCESS"}:
        return None, errors
    return (
        RuntimeObservationEnvelopeV1(
            observation_id=f"runtime-observation:{result.provider_result_ref}",
            execution_instance_ref=result.execution_instance_ref,
            provider_ref=result.provider_ref,
            capability_ref=result.capability_ref,
            modality=result.modality,
            source_ref=request.input_source_ref,
            raw_result_ref=result.raw_result_ref,
            temporal_ref=result.temporal_ref,
            observed_at=result.temporal_ref,
            provenance_refs=tuple(dict.fromkeys((*request.provenance_refs, *result.provenance_refs))),
            trace_refs=tuple(dict.fromkeys((*request.trace_refs, *result.trace_refs))),
            confidence_candidate=result.confidence_candidate,
            quality_candidate=result.quality_candidate,
            source_model_ref=result.model_ref,
            spatial_refs=result.spatial_refs,
            provider_available=True,
            capability_available=True,
            result_status="AVAILABLE",
            candidate_only=True,
            truth_declared=False,
            empty_result=result.empty_result,
            output_candidate=result.output_candidate,
        ),
        (),
    )
