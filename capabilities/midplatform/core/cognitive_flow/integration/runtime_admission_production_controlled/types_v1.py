"""Generic production-source records for Runtime Admission.

These records are an integration input/output surface.  They do not own
Capability, Model, Provider, Grant, Permission, Safety, or Resource state.
All outputs remain candidate-only and no execution is performed.
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


RUNTIME_ADMISSION_OWNER = "Runtime Admission"
DECLARATION_VALIDATION_PROFILE = "REPOSITORY_BACKED_DECLARATION_VALIDATION_NO_RUNTIME"


@dataclass(frozen=True)
class RuntimeAdmissionProductionInputV1:
    capability_resolution: Optional[CapabilityResolutionCandidateV1]
    capability_model_binding: Optional[CapabilityModelBindingCandidateV1]
    model_provider_binding: Optional[ModelProviderBindingCandidateV1]
    model_asset_ref: Optional[str]
    model_version_ref: Optional[str]
    weights_version_ref: Optional[str]
    governed_model_path_ref: Optional[str]
    loader_contract_ref: Optional[str]
    dependency_declaration_refs: Tuple[str, ...]
    dependency_status_ref: str
    runtime_readiness_status_ref: str
    model_version_status_ref: str
    integrity_status_ref: str
    integrity_evidence_ref: Optional[str]
    grant_refs: Tuple[str, ...]
    grant_status_ref: str
    permission_refs: Tuple[str, ...]
    permission_status_ref: str
    safety_refs: Tuple[str, ...]
    safety_status_ref: str
    resource_refs: Tuple[str, ...]
    resource_status_ref: str
    working_envelope_refs: Tuple[str, ...]
    working_envelope_status_ref: str
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    repository_source_refs: Tuple[str, ...]
    validation_profile: str = DECLARATION_VALIDATION_PROFILE
    candidate_only: bool = True
    model_loading_executed: bool = False
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False
    observation_execution_executed: bool = False
    action_execution_executed: bool = False
    source_mutation_executed: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class RuntimeAdmissionProductionFailureV1:
    failure_ref: str
    classification: str
    reason: str
    responsible_owner: str
    next_target: str
    source_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...] = ()
    candidate_only: bool = True


@dataclass(frozen=True)
class RuntimeAdmissionProductionResultV1:
    assessment: Optional[RuntimeAdmissionAssessmentCandidateV1]
    executable: Optional[ExecutableCapabilityCandidateV1]
    failure: Optional[RuntimeAdmissionProductionFailureV1]
    source_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    validation_profile: str
    candidate_only: bool = True
    runtime_execution: bool = False
    model_loading: bool = False
    provider_admission: bool = False
    provider_invocation: bool = False
    observation_execution: bool = False
    action_execution: bool = False
    source_mutation: bool = False
    world_truth_declared: bool = False


__all__ = [
    "DECLARATION_VALIDATION_PROFILE",
    "RUNTIME_ADMISSION_OWNER",
    "RuntimeAdmissionProductionFailureV1",
    "RuntimeAdmissionProductionInputV1",
    "RuntimeAdmissionProductionResultV1",
]
