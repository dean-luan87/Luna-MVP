"""Fail-closed assembly of the real YOLO11n canonical context.

The builder assembles records already produced by canonical boundaries.  It
does not produce Capability Resolution, binding, Runtime Admission, Provider
Admission, or model identity state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.capability_model_provider_binding_controlled.types_v1 import (
    CapabilityModelBindingCandidateV1,
    ModelProviderBindingCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_types_v1 import (
    ExecutableCapabilityCandidateV1,
    RuntimeAdmissionAssessmentCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityResolutionCandidateV1,
)

from .canonical_yolo11n_binding_seam_v1 import (
    CanonicalBindingSeamValidationV1,
    CanonicalYOLO11nBindingContextV1,
    validate_canonical_yolo11n_binding_context_v1,
)


def _unique(*groups: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(item for group in groups for item in group if str(item).strip()))


@dataclass(frozen=True)
class CanonicalYOLO11nUpstreamRecordsV1:
    capability_resolution: CapabilityResolutionCandidateV1
    capability_model_binding: CapabilityModelBindingCandidateV1
    runtime_admission_assessment: RuntimeAdmissionAssessmentCandidateV1
    executable_capability: ExecutableCapabilityCandidateV1
    model_provider_binding: ModelProviderBindingCandidateV1
    runtime_admission_ref: str
    runtime_admission_version: str
    grant_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextConstructionFailureV1:
    classification: str
    reason: str
    responsible_owner: str
    source_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]


@dataclass(frozen=True)
class CanonicalYOLO11nContextConstructionResultV1:
    context: Optional[CanonicalYOLO11nBindingContextV1]
    validation: CanonicalBindingSeamValidationV1
    failure: Optional[ContextConstructionFailureV1]


def _missing_failure(name: str) -> ContextConstructionFailureV1:
    owners = {
        "capability_resolution": "Capability Governance",
        "capability_model_binding": "Capability Governance",
        "runtime_admission_assessment": "Runtime Admission",
        "executable_capability": "Runtime Admission",
        "model_provider_binding": "Provider Governance",
    }
    return ContextConstructionFailureV1(
        classification=f"{name.upper()}_MISSING",
        reason=f"upstream governed record is required: {name}",
        responsible_owner=owners[name],
        source_refs=(),
        invalidation_refs=(),
    )


def build_canonical_yolo11n_context_v1(
    records: Optional[CanonicalYOLO11nUpstreamRecordsV1],
) -> CanonicalYOLO11nContextConstructionResultV1:
    if records is None:
        validation = validate_canonical_yolo11n_binding_context_v1(None)
        return CanonicalYOLO11nContextConstructionResultV1(
            context=None,
            validation=validation,
            failure=ContextConstructionFailureV1(
                classification="UPSTREAM_RECORDS_MISSING",
                reason="all canonical upstream records must be supplied; no success context is synthesized",
                responsible_owner="Integration adapter",
                source_refs=(),
                invalidation_refs=(),
            ),
        )

    required = (
        ("capability_resolution", records.capability_resolution),
        ("capability_model_binding", records.capability_model_binding),
        ("runtime_admission_assessment", records.runtime_admission_assessment),
        ("executable_capability", records.executable_capability),
        ("model_provider_binding", records.model_provider_binding),
    )
    for name, value in required:
        if value is None:
            validation = validate_canonical_yolo11n_binding_context_v1(None)
            return CanonicalYOLO11nContextConstructionResultV1(None, validation, _missing_failure(name))

    context = CanonicalYOLO11nBindingContextV1(
        capability_resolution=records.capability_resolution,
        capability_model_binding=records.capability_model_binding,
        runtime_admission_assessment=records.runtime_admission_assessment,
        executable_capability=records.executable_capability,
        model_provider_binding=records.model_provider_binding,
        runtime_admission_ref=records.runtime_admission_ref,
        runtime_admission_version=records.runtime_admission_version,
        grant_refs=records.grant_refs,
        constraint_refs=records.constraint_refs,
        source_version_refs=_unique(
            records.source_version_refs,
            records.capability_model_binding.source_version_refs,
            records.model_provider_binding.source_version_refs,
            (
                records.runtime_admission_assessment.source_state_version_ref,
                records.runtime_admission_assessment.valid_state_version_ref,
            ),
        ),
        trace_refs=_unique(
            records.trace_refs,
            records.capability_model_binding.trace_refs,
            records.model_provider_binding.trace_refs,
            records.runtime_admission_assessment.trace_refs,
        ),
        provenance_refs=_unique(
            records.provenance_refs,
            records.capability_model_binding.provenance_refs,
            records.model_provider_binding.provenance_refs,
            records.runtime_admission_assessment.provenance_refs,
        ),
        invalidation_refs=_unique(
            records.invalidation_refs,
            records.capability_model_binding.invalidation_refs,
            records.model_provider_binding.invalidation_refs,
            records.runtime_admission_assessment.expiry_staleness_refs,
            records.executable_capability.expiry_staleness_refs,
        ),
    )
    validation = validate_canonical_yolo11n_binding_context_v1(context)
    if validation.valid:
        return CanonicalYOLO11nContextConstructionResultV1(context, validation, None)

    owner = "Integration adapter"
    reason_lower = validation.reason.lower()
    if "capability" in reason_lower or "slot" in reason_lower or "resolution" in reason_lower:
        owner = "Capability Governance"
    elif "runtime admission" in reason_lower or "executable" in reason_lower:
        owner = "Runtime Admission"
    elif "provider" in reason_lower:
        owner = "Provider Governance"
    failure = ContextConstructionFailureV1(
        classification=validation.failure or "CANONICAL_CONTEXT_INVALID",
        reason=validation.reason,
        responsible_owner=owner,
        source_refs=_unique(
            (records.capability_model_binding.binding_id, records.model_provider_binding.binding_id, records.runtime_admission_ref),
        ),
        invalidation_refs=validation.invalidation_refs,
    )
    return CanonicalYOLO11nContextConstructionResultV1(None, validation, failure)


__all__ = [
    "CanonicalYOLO11nContextConstructionResultV1",
    "CanonicalYOLO11nUpstreamRecordsV1",
    "ContextConstructionFailureV1",
    "build_canonical_yolo11n_context_v1",
]
