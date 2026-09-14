from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, Optional

from .logical_capability_runtime_admission_types_v1 import (
    ADMISSION_BLOCKED_ASSET,
    ADMISSION_BLOCKED_CHECKSUM,
    ADMISSION_BLOCKED_CONTRACT,
    ADMISSION_BLOCKED_DEPENDENCY,
    ADMISSION_BLOCKED_IDENTITY,
    ADMISSION_BLOCKED_PERMISSION,
    ADMISSION_BLOCKED_PROVIDER,
    ADMISSION_BLOCKED_RESOURCE,
    ADMISSION_BLOCKED_SAFETY,
    ADMISSION_BLOCKED_STALE,
    ADMISSION_DEGRADED,
    ADMISSION_READY,
    ExecutableCapabilityCandidateV1,
    ProviderAdmissionInputCandidateV1,
    RuntimeAdmissionAssessmentCandidateV1,
    RuntimeAdmissionInputCandidateV1,
)


def build_runtime_admission_input_v1(**kwargs: Any) -> RuntimeAdmissionInputCandidateV1:
    return RuntimeAdmissionInputCandidateV1(**kwargs)


def _assessment(
    candidate: RuntimeAdmissionInputCandidateV1,
    *,
    status: str,
    reasons: tuple[str, ...] = (),
    stale_refs: tuple[str, ...] = (),
) -> RuntimeAdmissionAssessmentCandidateV1:
    admission_ref = f"runtime-admission:{candidate.logical_resolution_ref}"
    evidence_refs = tuple(
        item
        for item in (
            *candidate.dependency_health_refs,
            *candidate.device_runtime_health_refs,
            *candidate.provider_compatibility_refs,
            candidate.declared_checksum_ref,
            candidate.observed_integrity_evidence_ref,
        )
        if item
    )
    admitted = status == ADMISSION_READY
    return RuntimeAdmissionAssessmentCandidateV1(
        admission_candidate_ref=admission_ref,
        logical_resolution_ref=candidate.logical_resolution_ref,
        logical_capability_ref=candidate.logical_capability_ref,
        capability_slot_ref=candidate.capability_slot_ref,
        model_asset_ref=candidate.model_asset_ref,
        model_version_ref=candidate.model_version_ref,
        governed_model_path_ref=candidate.governed_model_path_ref,
        declared_checksum_ref=candidate.declared_checksum_ref,
        observed_integrity_evidence_ref=candidate.observed_integrity_evidence_ref,
        dependency_health_refs=candidate.dependency_health_refs,
        device_runtime_health_refs=candidate.device_runtime_health_refs,
        provider_compatibility_refs=candidate.provider_compatibility_refs,
        permission_refs=candidate.permission_refs,
        resource_refs=candidate.resource_refs,
        safety_refs=candidate.safety_refs,
        source_acquisition_context_ref=candidate.source_acquisition_context_ref,
        source_state_version_ref=candidate.source_state_version_ref,
        admission_status=status,
        admitted_model_asset_ref=candidate.model_asset_ref if admitted else None,
        admitted_provider_compatibility_ref=(
            candidate.provider_compatibility_refs[0]
            if admitted and candidate.provider_compatibility_refs
            else None
        ),
        blocking_reason_refs=reasons,
        evidence_refs=evidence_refs,
        valid_state_version_ref=(
            candidate.source_state_version_ref
            if candidate.source_state_version_ref == candidate.valid_source_state_version_ref
            else ""
        ),
        expiry_staleness_refs=tuple(dict.fromkeys((*candidate.staleness_refs, *stale_refs))),
        trace_refs=candidate.trace_refs,
        provenance_refs=candidate.provenance_refs,
    )


def assess_runtime_admission_v1(
    candidate: RuntimeAdmissionInputCandidateV1,
) -> RuntimeAdmissionAssessmentCandidateV1:
    """Assess supplied candidate evidence only; never probe or execute."""
    resolution = candidate.logical_resolution
    if resolution.status != "READY_CANDIDATE":
        return _assessment(
            candidate,
            status="UNAVAILABLE_CANDIDATE",
            reasons=(f"LOGICAL_RESOLUTION_{resolution.status}",),
        )
    if not candidate.model_asset_ref or not candidate.governed_model_path_ref:
        return _assessment(candidate, status=ADMISSION_BLOCKED_ASSET, reasons=("MODEL_ASSET_OR_PATH_MISSING",))
    if candidate.model_version_status_ref != "MODEL_VERSION_MATCH":
        return _assessment(candidate, status=ADMISSION_BLOCKED_IDENTITY, reasons=("MODEL_VERSION_MISMATCH",))
    if candidate.source_state_version_ref != candidate.valid_source_state_version_ref:
        return _assessment(candidate, status=ADMISSION_BLOCKED_STALE, reasons=("SOURCE_STATE_VERSION_STALE",))
    if candidate.staleness_refs:
        return _assessment(candidate, status=ADMISSION_BLOCKED_STALE, reasons=candidate.staleness_refs)
    if not candidate.declared_checksum_ref or not candidate.observed_integrity_evidence_ref:
        return _assessment(candidate, status=ADMISSION_BLOCKED_CHECKSUM, reasons=("INTEGRITY_EVIDENCE_MISSING",))
    if candidate.integrity_status_ref != "CHECKSUM_VERIFIED":
        return _assessment(candidate, status=ADMISSION_BLOCKED_CHECKSUM, reasons=(candidate.integrity_status_ref,))
    if candidate.dependency_status_ref != "PYTHON_DEPENDENCY_VERIFIED":
        return _assessment(candidate, status=ADMISSION_BLOCKED_DEPENDENCY, reasons=(candidate.dependency_status_ref,))
    if candidate.runtime_health_status_ref == "RUNTIME_HEALTH_DEGRADED":
        return _assessment(candidate, status=ADMISSION_DEGRADED, reasons=("RUNTIME_HEALTH_DEGRADED",))
    if candidate.runtime_health_status_ref != "RUNTIME_HEALTH_VERIFIED":
        return _assessment(candidate, status=ADMISSION_BLOCKED_RESOURCE, reasons=(candidate.runtime_health_status_ref,))
    if not candidate.provider_compatibility_refs:
        return _assessment(candidate, status=ADMISSION_BLOCKED_PROVIDER, reasons=("PROVIDER_COMPATIBILITY_MISSING",))
    if candidate.permission_status_ref != "PERMISSION_GRANTED":
        return _assessment(candidate, status=ADMISSION_BLOCKED_PERMISSION, reasons=(candidate.permission_status_ref,))
    if candidate.resource_status_ref != "RESOURCE_AVAILABLE":
        return _assessment(candidate, status=ADMISSION_BLOCKED_RESOURCE, reasons=(candidate.resource_status_ref,))
    if candidate.safety_status_ref != "SAFETY_ALLOWED":
        return _assessment(candidate, status=ADMISSION_BLOCKED_SAFETY, reasons=(candidate.safety_status_ref,))
    if not candidate.logical_resolution.provider_contract_refs:
        return _assessment(candidate, status=ADMISSION_BLOCKED_CONTRACT, reasons=("PROVIDER_CONTRACT_MISSING",))
    return _assessment(candidate, status=ADMISSION_READY)


def build_executable_capability_candidate_v1(
    assessment: RuntimeAdmissionAssessmentCandidateV1,
) -> Optional[ExecutableCapabilityCandidateV1]:
    if assessment.admission_status != ADMISSION_READY:
        return None
    required = (
        assessment.admitted_model_asset_ref,
        assessment.model_version_ref,
        assessment.governed_model_path_ref,
        assessment.admitted_provider_compatibility_ref,
        assessment.valid_state_version_ref,
    )
    if not all(required):
        return None
    return ExecutableCapabilityCandidateV1(
        executable_capability_ref=f"executable-capability:{assessment.admission_candidate_ref}",
        admission_candidate_ref=assessment.admission_candidate_ref,
        logical_resolution_ref=assessment.logical_resolution_ref,
        logical_capability_ref=assessment.logical_capability_ref,
        capability_slot_ref=assessment.capability_slot_ref,
        admitted_model_asset_ref=assessment.admitted_model_asset_ref or "",
        admitted_model_version_ref=assessment.model_version_ref or "",
        governed_model_path_ref=assessment.governed_model_path_ref or "",
        admitted_provider_compatibility_ref=assessment.admitted_provider_compatibility_ref or "",
        source_acquisition_context_ref=assessment.source_acquisition_context_ref,
        source_state_version_ref=assessment.source_state_version_ref,
        permission_refs=assessment.permission_refs,
        resource_refs=assessment.resource_refs,
        safety_refs=assessment.safety_refs,
        valid_state_version_ref=assessment.valid_state_version_ref,
        expiry_staleness_refs=assessment.expiry_staleness_refs,
        trace_refs=assessment.trace_refs,
        provenance_refs=assessment.provenance_refs,
    )


def build_provider_admission_input_v1(
    executable: Optional[ExecutableCapabilityCandidateV1],
) -> Optional[ProviderAdmissionInputCandidateV1]:
    if executable is None:
        return None
    return ProviderAdmissionInputCandidateV1(
        executable_capability_ref=executable.executable_capability_ref,
        admission_candidate_ref=executable.admission_candidate_ref,
        logical_capability_ref=executable.logical_capability_ref,
        admitted_model_asset_ref=executable.admitted_model_asset_ref,
        admitted_provider_compatibility_ref=executable.admitted_provider_compatibility_ref,
        source_acquisition_context_ref=executable.source_acquisition_context_ref,
        source_state_version_ref=executable.source_state_version_ref,
        trace_refs=executable.trace_refs,
        provenance_refs=executable.provenance_refs,
    )


def candidate_payload(value: Any) -> Dict[str, Any]:
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return dict(value)

