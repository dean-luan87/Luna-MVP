"""Narrow compatibility seam from canonical cognitive-flow records to FPO.

This module does not create Capability/Model/Provider bindings and does not
perform Runtime or Provider Admission.  It validates references supplied by
those owners and adapts them into the existing FPO admission input.
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
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_evidence_types_v1 import (
    VisionProviderAdmissionCandidateV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.field_perception_real_vision_provider_adapter_v1 import (
    build_vision_provider_admission_candidate_v1,
)


def _unique(*groups: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(item for group in groups for item in group if str(item).strip()))


@dataclass(frozen=True)
class CanonicalYOLO11nBindingContextV1:
    """References supplied by existing canonical owners for one invocation."""

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
class CanonicalBindingSeamValidationV1:
    valid: bool
    failure: Optional[str]
    reason: str
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]


@dataclass(frozen=True)
class CanonicalProviderAdmissionSeamResultV1:
    admission: VisionProviderAdmissionCandidateV1
    validation: CanonicalBindingSeamValidationV1


def validate_canonical_yolo11n_binding_context_v1(
    context: Optional[CanonicalYOLO11nBindingContextV1],
) -> CanonicalBindingSeamValidationV1:
    if context is None:
        return CanonicalBindingSeamValidationV1(
            valid=False,
            failure="CANONICAL_BINDING_CONTEXT_MISSING",
            reason="real Provider invocation requires upstream canonical binding and Runtime Admission references",
            source_version_refs=(),
            invalidation_refs=(),
            trace_refs=(),
            provenance_refs=(),
        )

    capability_binding = context.capability_model_binding
    resolution = context.capability_resolution
    runtime_assessment = context.runtime_admission_assessment
    executable = context.executable_capability
    provider_binding = context.model_provider_binding
    invalidation_refs = _unique(
        capability_binding.invalidation_refs,
        provider_binding.invalidation_refs,
        runtime_assessment.expiry_staleness_refs,
        executable.expiry_staleness_refs,
        context.invalidation_refs,
    )
    source_versions = _unique(
        capability_binding.source_version_refs,
        provider_binding.source_version_refs,
        (executable.source_state_version_ref, executable.valid_state_version_ref),
        (context.runtime_admission_version,),
    )
    trace_refs = _unique(capability_binding.trace_refs, provider_binding.trace_refs, executable.trace_refs)
    provenance_refs = _unique(capability_binding.provenance_refs, provider_binding.provenance_refs, executable.provenance_refs)

    checks = (
        (capability_binding.candidate_only, "capability/model binding must remain candidate/reference data"),
        (resolution.status in {"READY_CANDIDATE", "RESOLVED_UNIQUE", "VALID"}, "Capability Resolution is not valid/current"),
        (resolution.module_ref == capability_binding.capability_ref, "Capability Resolution differs from Capability binding"),
        (resolution.slot_ref in {None, capability_binding.capability_slot_ref}, "Capability Slot differs from Capability binding"),
        (capability_binding.model_asset_ref in resolution.model_asset_refs, "Capability Resolution does not reference the bound Model"),
        (provider_binding.provider_contract_ref in resolution.provider_contract_refs, "Capability Resolution does not reference the bound Provider contract"),
        (provider_binding.candidate_only, "model/provider binding must remain candidate/reference data"),
        (capability_binding.lifecycle_status not in {"STALE", "SUPERSEDED"}, "Capability/Model binding is stale or superseded"),
        (provider_binding.lifecycle_status not in {"STALE", "SUPERSEDED"}, "Model/Provider binding is stale or superseded"),
        (runtime_assessment.candidate_only, "Runtime Admission assessment must remain candidate/reference data"),
        (runtime_assessment.admission_status == "READY_FOR_EXECUTABLE_CANDIDATE", "Runtime Admission is not executable-ready"),
        (runtime_assessment.admission_candidate_ref == context.runtime_admission_ref, "Runtime Admission assessment differs from context ref"),
        (runtime_assessment.logical_capability_ref == capability_binding.capability_ref, "Runtime Admission Capability differs from binding"),
        (runtime_assessment.model_asset_ref == capability_binding.model_asset_ref, "Runtime Admission model differs from binding"),
        (runtime_assessment.model_version_ref == capability_binding.model_version_ref, "Runtime Admission model version differs from binding"),
        (bool(runtime_assessment.permission_refs and runtime_assessment.resource_refs and runtime_assessment.safety_refs), "Runtime Admission constraint refs are incomplete"),
        (not runtime_assessment.provider_invocation_executed and not runtime_assessment.model_loading_executed and not runtime_assessment.runtime_health_probe_executed, "Runtime Admission assessment contains executed runtime facts"),
        (executable.candidate_only, "Executable Capability must remain candidate-only"),
        (capability_binding.authority_owner == "Capability Governance", "Capability binding owner is not Capability Governance"),
        (provider_binding.authority_owner == "Provider Governance", "Provider binding owner is not Provider Governance"),
        (capability_binding.binding_lifecycle_owner == "Capability Governance", "Capability binding lifecycle owner changed"),
        (provider_binding.binding_lifecycle_owner == "Provider Governance", "Provider binding lifecycle owner changed"),
        (capability_binding.model_asset_ref == provider_binding.model_asset_ref, "model asset differs across canonical bindings"),
        (bool(capability_binding.model_asset_ref and capability_binding.model_version_ref and capability_binding.weights_version_ref), "Capability/model identity or version refs are missing"),
        (bool(provider_binding.model_asset_ref and provider_binding.model_version_ref and provider_binding.weights_version_ref), "Model/provider identity or version refs are missing"),
        (capability_binding.model_asset_ref == executable.admitted_model_asset_ref, "Executable Capability model differs from binding"),
        (capability_binding.model_version_ref == provider_binding.model_version_ref, "model version differs across bindings"),
        (capability_binding.model_version_ref == executable.admitted_model_version_ref, "Executable Capability model version differs from binding"),
        (capability_binding.compatibility_status == "COMPATIBLE", "Capability/model compatibility is not valid"),
        (provider_binding.compatibility_status == "COMPATIBLE", "Model/provider compatibility is not valid"),
        (bool(context.runtime_admission_ref and context.runtime_admission_version), "Runtime Admission reference/version is missing"),
        (context.runtime_admission_ref == executable.admission_candidate_ref, "Runtime Admission ref differs from Executable Capability"),
        (bool(executable.admitted_provider_compatibility_ref), "Executable Capability has no Provider compatibility ref"),
        (executable.admitted_provider_compatibility_ref in (provider_binding.binding_id, provider_binding.provider_contract_ref) or executable.admitted_provider_compatibility_ref in provider_binding.compatibility_constraints, "Provider compatibility ref is not bound to Model/provider declaration"),
        (bool(source_versions), "canonical source-version lineage is missing"),
        (bool(trace_refs), "canonical trace lineage is missing"),
        (bool(provenance_refs), "canonical provenance lineage is missing"),
        (bool(context.source_version_refs), "context source-version refs are missing"),
        (bool(context.trace_refs), "context trace refs are missing"),
        (bool(context.provenance_refs), "context provenance refs are missing"),
        (not invalidation_refs, "canonical binding/admission input is stale or invalidated"),
        (not executable.model_loading_executed and not executable.provider_invocation_executed, "upstream candidate reports runtime execution"),
    )
    for passed, reason in checks:
        if not passed:
            return CanonicalBindingSeamValidationV1(False, "CANONICAL_BINDING_CHAIN_INVALID", reason, source_versions, invalidation_refs, trace_refs, provenance_refs)
    return CanonicalBindingSeamValidationV1(True, None, "canonical binding and Runtime Admission references validated", source_versions, (), trace_refs, provenance_refs)


def build_canonical_yolo11n_provider_admission_v1(
    *,
    context: Optional[CanonicalYOLO11nBindingContextV1],
    observation_demand_ref: str,
    observation_request_ref: str,
    capability_requirement_ref: str,
    provider_session_ref: str,
    provider_candidate_ref: str,
    region_scope_candidate: str,
    expected_evidence: Tuple[str, ...],
    bounded: bool,
    trace_ref: str,
) -> CanonicalProviderAdmissionSeamResultV1:
    validation = validate_canonical_yolo11n_binding_context_v1(context)
    capability_binding = context.capability_model_binding if context else None
    provider_binding = context.model_provider_binding if context else None
    admission = build_vision_provider_admission_candidate_v1(
        observation_demand_ref=observation_demand_ref,
        observation_request_ref=observation_request_ref,
        capability_requirement_ref=capability_requirement_ref,
        provider_session_ref=provider_session_ref,
        provider_candidate_ref=provider_candidate_ref,
        model_candidate_ref=capability_binding.model_asset_ref if capability_binding else "",
        model_admission_ref=context.runtime_admission_ref if context else "",
        region_scope_candidate=region_scope_candidate,
        expected_evidence=expected_evidence,
        bounded=bounded,
        provider_admitted=validation.valid,
        trace_ref=trace_ref,
        provenance_refs=_unique(validation.provenance_refs, (trace_ref,)),
        canonical_capability_model_binding_ref=capability_binding.binding_id if capability_binding else "",
        canonical_capability_model_binding_version=capability_binding.binding_version if capability_binding else "",
        canonical_runtime_admission_ref=context.runtime_admission_ref if context else "",
        canonical_runtime_admission_version=context.runtime_admission_version if context else "",
        canonical_model_provider_binding_ref=provider_binding.binding_id if provider_binding else "",
        canonical_model_provider_binding_version=provider_binding.binding_version if provider_binding else "",
        canonical_invalidation_refs=validation.invalidation_refs,
        canonical_chain_validated=validation.valid,
        require_canonical_chain=True,
    )
    return CanonicalProviderAdmissionSeamResultV1(admission=admission, validation=validation)


__all__ = [
    "CanonicalBindingSeamValidationV1",
    "CanonicalProviderAdmissionSeamResultV1",
    "CanonicalYOLO11nBindingContextV1",
    "build_canonical_yolo11n_provider_admission_v1",
    "validate_canonical_yolo11n_binding_context_v1",
]
