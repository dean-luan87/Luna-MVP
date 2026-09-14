from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityResolutionCandidateV1,
)


ADMISSION_READY = "READY_FOR_EXECUTABLE_CANDIDATE"
ADMISSION_DEGRADED = "DEGRADED_CANDIDATE"
ADMISSION_BLOCKED_ASSET = "ADMISSION_BLOCKED_ASSET_MISSING"
ADMISSION_BLOCKED_IDENTITY = "ADMISSION_BLOCKED_IDENTITY"
ADMISSION_BLOCKED_CHECKSUM = "ADMISSION_BLOCKED_CHECKSUM"
ADMISSION_BLOCKED_DEPENDENCY = "ADMISSION_BLOCKED_DEPENDENCY"
ADMISSION_BLOCKED_CONTRACT = "ADMISSION_BLOCKED_CONTRACT"
ADMISSION_BLOCKED_PROVIDER = "ADMISSION_BLOCKED_PROVIDER"
ADMISSION_BLOCKED_PERMISSION = "PERMISSION_ADMISSION_BLOCKED"
ADMISSION_BLOCKED_RESOURCE = "RESOURCE_ADMISSION_BLOCKED"
ADMISSION_BLOCKED_SAFETY = "SAFETY_ADMISSION_BLOCKED"
ADMISSION_BLOCKED_STALE = "STALE_ADMISSION_CANDIDATE"


@dataclass(frozen=True)
class RuntimeAdmissionInputCandidateV1:
    logical_resolution_ref: str
    logical_resolution: CapabilityResolutionCandidateV1
    logical_capability_ref: str
    capability_slot_ref: str
    model_asset_ref: Optional[str]
    model_version_ref: Optional[str]
    governed_model_path_ref: Optional[str]
    declared_checksum_ref: Optional[str]
    observed_integrity_evidence_ref: Optional[str]
    dependency_health_refs: Tuple[str, ...]
    dependency_status_ref: str
    device_runtime_health_refs: Tuple[str, ...]
    runtime_health_status_ref: str
    provider_compatibility_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    permission_status_ref: str
    resource_refs: Tuple[str, ...]
    resource_status_ref: str
    safety_refs: Tuple[str, ...]
    safety_status_ref: str
    integrity_status_ref: str
    model_version_status_ref: str
    source_acquisition_context_ref: str
    source_state_version_ref: str
    valid_source_state_version_ref: str
    staleness_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True


@dataclass(frozen=True)
class RuntimeAdmissionAssessmentCandidateV1:
    admission_candidate_ref: str
    logical_resolution_ref: str
    logical_capability_ref: str
    capability_slot_ref: str
    model_asset_ref: Optional[str]
    model_version_ref: Optional[str]
    governed_model_path_ref: Optional[str]
    declared_checksum_ref: Optional[str]
    observed_integrity_evidence_ref: Optional[str]
    dependency_health_refs: Tuple[str, ...]
    device_runtime_health_refs: Tuple[str, ...]
    provider_compatibility_refs: Tuple[str, ...]
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    source_acquisition_context_ref: str
    source_state_version_ref: str
    admission_status: str
    admitted_model_asset_ref: Optional[str]
    admitted_provider_compatibility_ref: Optional[str]
    blocking_reason_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    valid_state_version_ref: str
    expiry_staleness_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    provider_invocation_executed: bool = False
    model_loading_executed: bool = False
    checksum_computed: bool = False
    dependency_probe_executed: bool = False
    runtime_health_probe_executed: bool = False


@dataclass(frozen=True)
class ExecutableCapabilityCandidateV1:
    executable_capability_ref: str
    admission_candidate_ref: str
    logical_resolution_ref: str
    logical_capability_ref: str
    capability_slot_ref: str
    admitted_model_asset_ref: str
    admitted_model_version_ref: str
    governed_model_path_ref: str
    admitted_provider_compatibility_ref: str
    source_acquisition_context_ref: str
    source_state_version_ref: str
    permission_refs: Tuple[str, ...]
    resource_refs: Tuple[str, ...]
    safety_refs: Tuple[str, ...]
    valid_state_version_ref: str
    expiry_staleness_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    synthetic_only: bool = True
    provider_invocation_executed: bool = False
    model_loading_executed: bool = False


@dataclass(frozen=True)
class ProviderAdmissionInputCandidateV1:
    executable_capability_ref: str
    admission_candidate_ref: str
    logical_capability_ref: str
    admitted_model_asset_ref: str
    admitted_provider_compatibility_ref: str
    source_acquisition_context_ref: str
    source_state_version_ref: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    provider_invocation_authorized: bool = False
    candidate_only: bool = True
    synthetic_only: bool = True

