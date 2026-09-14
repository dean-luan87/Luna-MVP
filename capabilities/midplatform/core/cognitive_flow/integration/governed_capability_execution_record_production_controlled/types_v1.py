"""Local integration records for repository-backed governed-record production.

These records describe production availability and composition only.  They do
not replace Capability, Model, Runtime Admission, or Provider contracts.
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


@dataclass(frozen=True)
class GovernedDeclarationInventoryV1:
    target_model_asset_id: str
    target_capability_contract_id: str
    target_provider_family: str
    source_refs: Tuple[str, ...]
    capability_registry_entry_found: bool
    capability_slot_declaration_found: bool
    model_registry_entry_found: bool
    model_contract_candidate_found: bool
    capability_model_declaration_found: bool
    provider_registry_entry_found: bool
    provider_contract_candidate_found: bool
    model_provider_declaration_found: bool
    runtime_admission_source_found: bool
    missing_declarations: Tuple[str, ...]


@dataclass(frozen=True)
class GovernedExecutionRecordBundleV1:
    """A generic bundle of records already produced by canonical owners."""

    capability_resolution: Optional[CapabilityResolutionCandidateV1]
    capability_model_binding: Optional[CapabilityModelBindingCandidateV1]
    runtime_admission_assessment: Optional[RuntimeAdmissionAssessmentCandidateV1]
    executable_capability: Optional[ExecutableCapabilityCandidateV1]
    model_provider_binding: Optional[ModelProviderBindingCandidateV1]
    runtime_admission_ref: str
    runtime_admission_version: str
    grant_refs: Tuple[str, ...]
    constraint_refs: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    candidate_only: bool = True
    model_loading_executed: bool = False
    provider_invocation_executed: bool = False
    observation_execution_executed: bool = False
    action_execution_executed: bool = False
    source_mutation_executed: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class GovernedRecordProductionResultV1:
    status: str
    inventory: GovernedDeclarationInventoryV1
    bundle: Optional[GovernedExecutionRecordBundleV1]
    missing_declarations: Tuple[str, ...]
    responsible_owners: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    no_success_synthesized: bool = True
    runtime_execution: bool = False
    model_loading: bool = False
    provider_invocation: bool = False
    observation_execution: bool = False
    action_execution: bool = False
    source_mutation: bool = False
    world_truth_declared: bool = False


__all__ = [
    "GovernedDeclarationInventoryV1",
    "GovernedExecutionRecordBundleV1",
    "GovernedRecordProductionResultV1",
]
