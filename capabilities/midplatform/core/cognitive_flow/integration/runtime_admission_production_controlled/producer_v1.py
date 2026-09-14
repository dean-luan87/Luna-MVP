"""Generic repository-backed Runtime Admission production source.

The producer validates supplied owner-issued records and declared readiness
evidence.  It never probes a device, computes a checksum, loads a model,
admits a Provider, or invokes anything.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_adapter_v1 import (
    assess_runtime_admission_v1,
    build_executable_capability_candidate_v1,
    build_runtime_admission_input_v1,
)

from .types_v1 import (
    DECLARATION_VALIDATION_PROFILE,
    RUNTIME_ADMISSION_OWNER,
    RuntimeAdmissionProductionFailureV1,
    RuntimeAdmissionProductionInputV1,
    RuntimeAdmissionProductionResultV1,
)


READY = "READY_FOR_EXECUTABLE_CANDIDATE"


def _failure(
    data: RuntimeAdmissionProductionInputV1,
    classification: str,
    reason: str,
    owner: str = RUNTIME_ADMISSION_OWNER,
    next_target: str = "Runtime Admission",
) -> RuntimeAdmissionProductionResultV1:
    source_refs = tuple(dict.fromkeys(data.repository_source_refs + tuple(
        item for item in (
            data.model_asset_ref,
            data.capability_model_binding.binding_id if data.capability_model_binding else None,
            data.model_provider_binding.binding_id if data.model_provider_binding else None,
        ) if item
    )))
    return RuntimeAdmissionProductionResultV1(
        assessment=None,
        executable=None,
        failure=RuntimeAdmissionProductionFailureV1(
            failure_ref=f"failure:runtime-admission:{classification.lower()}",
            classification=classification,
            reason=reason,
            responsible_owner=owner,
            next_target=next_target,
            source_refs=source_refs,
            trace_refs=data.trace_refs,
            provenance_refs=data.provenance_refs,
            invalidation_refs=data.invalidation_refs,
        ),
        source_refs=source_refs,
        trace_refs=data.trace_refs,
        provenance_refs=data.provenance_refs,
        invalidation_refs=data.invalidation_refs,
        validation_profile=data.validation_profile,
    )


def _common_failure(data: RuntimeAdmissionProductionInputV1) -> Optional[RuntimeAdmissionProductionResultV1]:
    if not data.candidate_only:
        return _failure(data, "NON_CANDIDATE_INPUT", "Runtime Admission production source accepts candidate/reference inputs only", next_target="caller")
    if data.validation_profile != DECLARATION_VALIDATION_PROFILE:
        return _failure(data, "VALIDATION_PROFILE_UNSUPPORTED", "Runtime readiness profile is not an approved no-runtime validation profile", next_target="Runtime Admission")
    if not data.repository_source_refs:
        return _failure(data, "REPOSITORY_SOURCE_MISSING", "repository-backed declaration source refs are required", next_target="source owner")
    if not data.trace_refs or not data.provenance_refs:
        return _failure(data, "PROVENANCE_INVALID", "Runtime Admission inputs require trace and provenance", next_target="source owner")
    if data.invalidation_refs:
        return _failure(data, "INPUT_INVALIDATED", "invalidated or superseded inputs cannot produce executable candidates")
    if any((data.model_loading_executed, data.provider_admission_executed, data.provider_invocation_executed, data.observation_execution_executed, data.action_execution_executed, data.source_mutation_executed, data.world_truth_declared)):
        return _failure(data, "EXECUTION_OR_MUTATION_DETECTED", "production source cannot accept executed or source-mutating inputs")
    if data.capability_resolution is None:
        return _failure(data, "CAPABILITY_RESOLUTION_MISSING", "Capability Resolution is required", owner="Capability Governance", next_target="Capability Governance")
    if data.capability_model_binding is None:
        return _failure(data, "CAPABILITY_MODEL_BINDING_MISSING", "Capability↔Model binding is required", owner="Capability Governance", next_target="Capability Governance")
    if data.model_provider_binding is None:
        return _failure(data, "MODEL_PROVIDER_BINDING_MISSING", "Model↔Provider binding is required", owner="Provider Governance", next_target="Provider Governance")
    capability_binding = data.capability_model_binding
    provider_binding = data.model_provider_binding
    resolution = data.capability_resolution
    if capability_binding.authority_owner != "Capability Governance" or capability_binding.binding_lifecycle_owner != "Capability Governance":
        return _failure(data, "CAPABILITY_BINDING_OWNER_INVALID", "Capability↔Model lifecycle owner is not Capability Governance", owner="Capability Governance", next_target="Capability Governance")
    if provider_binding.authority_owner != "Provider Governance" or provider_binding.binding_lifecycle_owner != "Provider Governance":
        return _failure(data, "PROVIDER_BINDING_OWNER_INVALID", "Model↔Provider lifecycle owner is not Provider Governance", owner="Provider Governance", next_target="Provider Governance")
    if resolution.status not in {"READY_CANDIDATE", "RESOLVED_UNIQUE", "VALID"}:
        return _failure(data, "CAPABILITY_RESOLUTION_INVALID", "Capability Resolution is not current/usable", owner="Capability Governance", next_target="Capability Governance")
    if resolution.module_ref != capability_binding.capability_ref or resolution.slot_ref not in {None, capability_binding.capability_slot_ref}:
        return _failure(data, "CAPABILITY_RESOLUTION_BINDING_MISMATCH", "Capability Resolution does not match Capability↔Model binding", owner="Capability Governance", next_target="Capability Governance")
    if capability_binding.model_asset_ref != provider_binding.model_asset_ref or capability_binding.model_version_ref != provider_binding.model_version_ref or capability_binding.weights_version_ref != provider_binding.weights_version_ref:
        return _failure(data, "BINDING_MODEL_VERSION_MISMATCH", "Capability↔Model and Model↔Provider bindings disagree", owner="Runtime Admission", next_target="Runtime Admission")
    if capability_binding.lifecycle_status in {"STALE", "SUPERSEDED"}:
        return _failure(data, "CAPABILITY_MODEL_BINDING_STALE", "Capability↔Model binding is stale or superseded", owner="Capability Governance", next_target="Capability Governance")
    if provider_binding.lifecycle_status in {"STALE", "SUPERSEDED"}:
        return _failure(data, "MODEL_PROVIDER_BINDING_STALE", "Model↔Provider binding is stale or superseded", owner="Provider Governance", next_target="Provider Governance")
    if not data.model_asset_ref or not data.model_version_ref or not data.weights_version_ref:
        return _failure(data, "MODEL_DECLARATION_MISSING", "Model identity/version/weights refs are required", owner="Model Governance", next_target="Model Governance")
    if data.model_asset_ref != capability_binding.model_asset_ref or data.model_asset_ref != provider_binding.model_asset_ref:
        return _failure(data, "MODEL_DECLARATION_MISMATCH", "Model declaration does not match both governed bindings", owner="Model Governance", next_target="Model Governance")
    if data.model_version_status_ref != "MODEL_VERSION_MATCH":
        return _failure(data, "MODEL_VERSION_MISMATCH", "Model version is not current", owner="Model Governance", next_target="Model Governance")
    if data.grant_status_ref != "GRANT_VALID":
        return _failure(data, "GRANT_INVALID", "Grant is stale or revoked", owner="Brain Governance", next_target="Brain Governance")
    if not data.grant_refs or not data.permission_refs or not data.safety_refs or not data.resource_refs:
        return _failure(data, "CONSTRAINT_REFS_MISSING", "Grant, Permission, Safety and Resource refs are required", owner="Runtime Admission", next_target="Runtime Admission")
    if data.permission_status_ref != "PERMISSION_GRANTED":
        return _failure(data, "PERMISSION_BLOCKED", "Permission does not permit executable eligibility", owner="Permission Governance", next_target="Permission Governance")
    if data.safety_status_ref != "SAFETY_ALLOWED":
        return _failure(data, "SAFETY_BLOCKED", "Safety policy blocks executable eligibility", owner="Safety Governance", next_target="Safety Governance")
    if data.resource_status_ref != "RESOURCE_AVAILABLE":
        return _failure(data, "RESOURCE_UNAVAILABLE", "Resource policy/evidence does not permit executable eligibility", owner="Resource Governance", next_target="Resource Governance")
    if data.working_envelope_status_ref != "ENVELOPE_COMPATIBLE":
        return _failure(data, "WORKING_ENVELOPE_INCOMPATIBLE", "Working Envelope is stale or incompatible", owner="Working Envelope", next_target="Working Envelope")
    if data.dependency_status_ref != "DECLARATION_VALIDATED" or data.runtime_readiness_status_ref != "DECLARATION_VALIDATED":
        return _failure(data, "RUNTIME_READINESS_UNAVAILABLE", "runtime/dependency readiness is not available for this validation profile", next_target="Runtime Admission")
    if data.integrity_status_ref != "DECLARATION_VALIDATED" or not data.integrity_evidence_ref:
        return _failure(data, "INTEGRITY_EVIDENCE_UNAVAILABLE", "declared integrity evidence is required; no checksum is computed here", owner="Model Governance", next_target="Model Governance")
    if not data.source_version_refs:
        return _failure(data, "SOURCE_VERSION_MISSING", "source version lineage is required", next_target="source owner")
    if not data.model_asset_ref in resolution.model_asset_refs or provider_binding.provider_contract_ref not in resolution.provider_contract_refs:
        return _failure(data, "CAPABILITY_PROVIDER_DECLARATION_MISMATCH", "Capability Resolution does not retain governed model/provider refs", owner="Capability Governance", next_target="Capability Governance")
    return None


def _build_legacy_input(data: RuntimeAdmissionProductionInputV1):
    resolution = data.capability_resolution
    assert resolution is not None
    return build_runtime_admission_input_v1(
        logical_resolution_ref=resolution.requirement_id,
        logical_resolution=resolution,
        logical_capability_ref=data.capability_model_binding.capability_ref if data.capability_model_binding else "",
        capability_slot_ref=data.capability_model_binding.capability_slot_ref if data.capability_model_binding else "",
        model_asset_ref=data.model_asset_ref,
        model_version_ref=data.model_version_ref,
        governed_model_path_ref=data.governed_model_path_ref,
        declared_checksum_ref=data.integrity_evidence_ref,
        observed_integrity_evidence_ref=data.integrity_evidence_ref,
        dependency_health_refs=data.dependency_declaration_refs,
        dependency_status_ref="PYTHON_DEPENDENCY_VERIFIED",
        device_runtime_health_refs=("runtime-readiness:repository-declaration:v1",),
        runtime_health_status_ref="RUNTIME_HEALTH_VERIFIED",
        provider_compatibility_refs=(data.model_provider_binding.binding_id,) if data.model_provider_binding else (),
        permission_refs=data.permission_refs,
        permission_status_ref=data.permission_status_ref,
        resource_refs=data.resource_refs,
        resource_status_ref=data.resource_status_ref,
        safety_refs=data.safety_refs,
        safety_status_ref=data.safety_status_ref,
        integrity_status_ref="CHECKSUM_VERIFIED",
        model_version_status_ref=data.model_version_status_ref,
        source_acquisition_context_ref=data.working_envelope_refs[0] if data.working_envelope_refs else "working-envelope:repository-validation:v1",
        source_state_version_ref=data.source_version_refs[0],
        valid_source_state_version_ref=data.source_version_refs[0],
        staleness_refs=(),
        trace_refs=data.trace_refs,
        provenance_refs=data.provenance_refs,
        candidate_only=True,
        synthetic_only=False,
    )


def assess_runtime_admission_production_v1(data: RuntimeAdmissionProductionInputV1) -> RuntimeAdmissionProductionResultV1:
    failure = _common_failure(data)
    if failure is not None:
        return failure
    legacy_input = _build_legacy_input(data)
    assessment = replace(assess_runtime_admission_v1(legacy_input), synthetic_only=False)
    if assessment.admission_status != READY:
        return _failure(data, "RUNTIME_ADMISSION_BLOCKED", "reused Runtime Admission assessment rejected the supplied governed inputs")
    executable = build_executable_capability_candidate_v1(assessment)
    if executable is None:
        return _failure(data, "EXECUTABLE_CANDIDATE_NOT_FORMED", "Runtime Admission did not satisfy executable candidate conditions")
    executable = replace(executable, synthetic_only=False)
    return RuntimeAdmissionProductionResultV1(
        assessment=assessment,
        executable=executable,
        failure=None,
        source_refs=data.repository_source_refs,
        trace_refs=data.trace_refs,
        provenance_refs=data.provenance_refs,
        invalidation_refs=data.invalidation_refs,
        validation_profile=data.validation_profile,
    )


def build_executable_capability_candidate_production_v1(data: RuntimeAdmissionProductionInputV1) -> Optional[object]:
    return assess_runtime_admission_production_v1(data).executable


__all__ = [
    "assess_runtime_admission_production_v1",
    "build_executable_capability_candidate_production_v1",
]
