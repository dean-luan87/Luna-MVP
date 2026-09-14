"""Controlled bridge from ProviderInvocationResult to the Gateway envelope.

This adapter only preserves execution lineage and wraps a completed synthetic
result in the existing RuntimeObservationEnvelopeV1.  It does not interpret
the payload, admit truth, decide sufficiency, or invoke any runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    RuntimeObservationEnvelopeV1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_session_invocation_v1 import (
    ProviderInvocationResultV1,
    ProviderRuntimeSessionV1,
    ProviderInvocationRecordV1,
)


FORMATION_STATUS = "RUNTIME_OBSERVATION_FORMED"
BLOCKED_STATUS = "RUNTIME_OBSERVATION_FORMATION_BLOCKED"
INVALID_STATUS = "INVALID_INPUT"
OBSERVABLE_INVOCATION_FORMATION_STATUS = "PROVIDER_INVOCATION_COMPLETED"


def _unique(values: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class ProviderInvocationObservationFormationResultV1:
    """Typed formation result; ``observation`` is absent when blocked."""

    invocation_request_ref: str
    formation_status: str
    observation: Optional[RuntimeObservationEnvelopeV1]
    source_invocation_result_ref: str = ""
    source_invocation_ref: str = ""
    source_session_ref: str = ""
    lineage_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_refs: Tuple[str, ...] = field(default_factory=tuple)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)


def _invalid_result(
    result: object,
    errors: Tuple[str, ...],
) -> ProviderInvocationObservationFormationResultV1:
    return ProviderInvocationObservationFormationResultV1(
        invocation_request_ref=getattr(result, "invocation_request_ref", ""),
        formation_status=INVALID_STATUS,
        observation=None,
        validation_errors=errors,
    )


def _validate_result(result: object) -> Tuple[str, ...]:
    if not isinstance(result, ProviderInvocationResultV1):
        return ("invocation_result_type_invalid",)
    errors = []
    session = result.session
    invocation = result.invocation
    if not result.invocation_request_ref or not result.trace_ref:
        errors.append("invocation_result_identity_missing")
    if result.formation_status != OBSERVABLE_INVOCATION_FORMATION_STATUS:
        errors.append("invocation_outcome_not_observable")
    if not isinstance(session, ProviderRuntimeSessionV1):
        errors.append("runtime_session_missing_or_invalid")
    if not isinstance(invocation, ProviderInvocationRecordV1):
        errors.append("invocation_record_missing_or_invalid")
    if errors:
        return tuple(dict.fromkeys(errors))
    assert session is not None
    assert invocation is not None
    if invocation.status != "COMPLETED" or not invocation.controlled_invocation_completed:
        errors.append("invocation_record_not_completed")
    if session.status != "COMPLETED" or not session.execution_started:
        errors.append("runtime_session_not_completed")
    if invocation.session_ref != session.session_ref:
        errors.append("invocation_session_lineage_mismatch")
    if invocation.execution_instance_ref != session.execution_instance_ref:
        errors.append("invocation_execution_lineage_mismatch")
    if invocation.provider_binding_ref != session.provider_binding_ref:
        errors.append("invocation_binding_lineage_mismatch")
    if invocation.runtime_grant_ref != session.runtime_grant_ref:
        errors.append("invocation_grant_lineage_mismatch")
    if invocation.runtime_allocation_ref != session.runtime_allocation_ref:
        errors.append("invocation_allocation_lineage_mismatch")
    if invocation.provider_ref != session.provider_ref:
        errors.append("invocation_provider_lineage_mismatch")
    if invocation.capability_ref != session.capability_ref:
        errors.append("invocation_capability_lineage_mismatch")
    if invocation.source_model_ref != session.source_model_ref:
        errors.append("invocation_model_lineage_mismatch")
    if not invocation.result_ref or not invocation.payload_ref:
        errors.append("invocation_result_refs_missing")
    if not invocation.lineage_refs or not invocation.provenance_refs:
        errors.append("invocation_lineage_or_provenance_missing")
    if not all(
        value is False
        for value in (
            invocation.real_provider_invoked,
            invocation.real_model_invoked,
            invocation.network_called,
            invocation.subprocess_started,
            invocation.thread_started,
            invocation.socket_used,
            invocation.truth_declared,
            invocation.world_truth_declared,
        )
    ):
        errors.append("real_effect_or_truth_boundary_invalid")
    return tuple(dict.fromkeys(errors))


def form_runtime_observation_from_invocation_result(
    result: object,
) -> ProviderInvocationObservationFormationResultV1:
    """Form an existing Gateway envelope only for a completed result.

    The fixed ``EXTERNAL_PROVIDER`` modality is a governed transport shape,
    not a semantic inference from capability or payload text.
    """

    errors = _validate_result(result)
    if not isinstance(result, ProviderInvocationResultV1):
        return _invalid_result(result, errors)
    session = result.session
    invocation = result.invocation
    if errors:
        lineage = invocation.lineage_refs if isinstance(invocation, ProviderInvocationRecordV1) else ()
        invalid_shape = any(
            error in {
                "invocation_result_identity_missing",
                "runtime_session_missing_or_invalid",
                "invocation_record_missing_or_invalid",
                "invocation_result_refs_missing",
                "invocation_lineage_or_provenance_missing",
            }
            for error in errors
        )
        return ProviderInvocationObservationFormationResultV1(
            invocation_request_ref=result.invocation_request_ref,
            formation_status=INVALID_STATUS if invalid_shape else BLOCKED_STATUS,
            observation=None,
            source_invocation_result_ref=getattr(invocation, "result_ref", ""),
            source_invocation_ref=getattr(invocation, "invocation_ref", ""),
            source_session_ref=getattr(session, "session_ref", ""),
            lineage_refs=lineage,
            provenance_refs=getattr(invocation, "provenance_refs", ()),
            trace_refs=_unique((result.trace_ref, getattr(invocation, "trace_ref", ""))),
            validation_errors=errors,
        )
    assert session is not None
    assert invocation is not None
    lineage_refs = _unique(
        (
            *invocation.lineage_refs,
            invocation.provider_binding_ref,
            invocation.runtime_grant_ref,
            invocation.runtime_allocation_ref,
            invocation.execution_instance_ref,
            invocation.session_ref,
            invocation.invocation_ref,
            invocation.result_ref,
            invocation.provider_ref,
            invocation.capability_ref,
        )
    )
    provenance_refs = _unique(
        (
            *session.provenance_refs,
            *invocation.provenance_refs,
            invocation.provider_binding_ref,
            invocation.runtime_grant_ref,
            invocation.runtime_allocation_ref,
            invocation.execution_instance_ref,
            invocation.session_ref,
            invocation.invocation_ref,
            invocation.result_ref,
        )
    )
    trace_refs = _unique(
        (
            result.trace_ref,
            session.trace_ref,
            invocation.trace_ref,
            f"trace:runtime-observation-formation:{invocation.result_ref}",
        )
    )
    observation = RuntimeObservationEnvelopeV1(
        observation_id=f"runtime-observation:{invocation.result_ref}",
        execution_instance_ref=invocation.execution_instance_ref,
        provider_ref=invocation.provider_ref,
        capability_ref=invocation.capability_ref,
        modality="EXTERNAL_PROVIDER",
        source_ref=invocation.result_ref,
        raw_result_ref=invocation.result_ref,
        temporal_ref=f"temporal:controlled:{invocation.execution_instance_ref}",
        observed_at=f"temporal:controlled:{invocation.execution_instance_ref}",
        provenance_refs=provenance_refs,
        trace_refs=trace_refs,
        source_model_ref=invocation.source_model_ref,
        provider_available=True,
        capability_available=True,
        result_status="AVAILABLE",
        candidate_only=True,
        truth_declared=False,
        output_candidate={"opaque_payload_ref": invocation.payload_ref},
    )
    return ProviderInvocationObservationFormationResultV1(
        invocation_request_ref=result.invocation_request_ref,
        formation_status=FORMATION_STATUS,
        observation=observation,
        source_invocation_result_ref=invocation.result_ref,
        source_invocation_ref=invocation.invocation_ref,
        source_session_ref=session.session_ref,
        lineage_refs=lineage_refs,
        provenance_refs=provenance_refs,
        trace_refs=trace_refs,
    )


__all__ = [
    "FORMATION_STATUS",
    "BLOCKED_STATUS",
    "INVALID_STATUS",
    "ProviderInvocationObservationFormationResultV1",
    "form_runtime_observation_from_invocation_result",
]
