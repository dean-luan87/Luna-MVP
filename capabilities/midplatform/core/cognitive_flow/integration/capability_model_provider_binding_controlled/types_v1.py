"""Local candidate and observability types for binding validation.

These records bind separately owned declarations. They do not perform Runtime
Admission, Provider Admission, model loading, checksum calculation, probing,
or invocation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.types_v1 import (
    EdgeObservabilityCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityResolutionCandidateV1,
)
from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_types_v1 import (
    ModelAssetContractV1,
)


@dataclass(frozen=True)
class CapabilityModelBindingInputV1:
    capability_ref: Optional[str]
    capability_slot_ref: Optional[str]
    capability_contract_version: Optional[str]
    logical_resolution_ref: Optional[str]
    logical_resolution: Optional[CapabilityResolutionCandidateV1]
    logical_resolution_status: str
    logical_resolution_capability_ref: Optional[str]
    logical_resolution_slot_ref: Optional[str]
    capability_exists: bool
    slot_exists: bool
    model_asset_ref: Optional[str]
    model_asset: Optional[ModelAssetContractV1]
    model_version_ref: Optional[str]
    weights_version_ref: Optional[str]
    model_capability_declaration_ref: Optional[str]
    declared_capability_ref: Optional[str]
    declared_capability_contract_version: Optional[str]
    model_lifecycle_status: str
    model_version_status: str
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class ModelProviderBindingInputV1:
    model_asset_ref: Optional[str]
    model_asset: Optional[ModelAssetContractV1]
    model_version_ref: Optional[str]
    weights_version_ref: Optional[str]
    loader_contract_ref: Optional[str]
    dependency_declaration_refs: Tuple[str, ...]
    provider_family_ref: Optional[str]
    provider_contract_ref: Optional[str]
    provider_adapter_ref: Optional[str]
    model_provider_declaration_ref: Optional[str]
    model_declared_provider_family_ref: Optional[str]
    model_declared_provider_adapter_ref: Optional[str]
    provider_declared_model_asset_ref: Optional[str]
    provider_supported_loader_contract_refs: Tuple[str, ...]
    declared_provider_contract_version: Optional[str]
    provider_contract_version: Optional[str]
    model_lifecycle_status: str
    model_version_status: str
    provider_declaration_status: str
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    synthetic_only: bool = True
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityModelBindingCandidateV1:
    binding_id: str
    binding_version: str
    capability_ref: str
    capability_slot_ref: Optional[str]
    capability_contract_version: str
    logical_resolution_ref: str
    model_asset_ref: str
    model_version_ref: str
    weights_version_ref: str
    model_capability_declaration_ref: str
    compatibility_status: str
    compatibility_constraints: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Capability Governance"
    responsibility_owner: str = "Capability Governance"
    binding_lifecycle_owner: str = "Capability Governance"
    model_source_owner: str = "Model Governance"
    candidate_only: bool = True
    runtime_admission_executed: bool = False
    model_loading_executed: bool = False
    provider_invocation_executed: bool = False
    no_dual_mutation_authority: bool = True
    lifecycle_status: str = "PROPOSED"


@dataclass(frozen=True)
class ModelProviderBindingCandidateV1:
    binding_id: str
    binding_version: str
    model_asset_ref: str
    model_version_ref: str
    weights_version_ref: str
    loader_contract_ref: str
    dependency_declaration_refs: Tuple[str, ...]
    provider_family_ref: str
    provider_contract_ref: str
    provider_adapter_ref: str
    model_provider_declaration_ref: str
    compatibility_status: str
    compatibility_constraints: Tuple[str, ...]
    source_version_refs: Tuple[str, ...]
    invalidation_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    authority_owner: str = "Provider Governance"
    responsibility_owner: str = "Provider Governance"
    binding_lifecycle_owner: str = "Provider Governance"
    model_source_owner: str = "Model Governance"
    provider_source_owner: str = "Provider Governance"
    candidate_only: bool = True
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False
    model_loading_executed: bool = False
    no_dual_mutation_authority: bool = True
    lifecycle_status: str = "PROPOSED"


@dataclass(frozen=True)
class BindingEdgeObservabilityV1:
    edge: EdgeObservabilityCandidateV1
    runtime_execution_executed: bool = False
    model_loading_executed: bool = False
    provider_admission_executed: bool = False
    provider_invocation_executed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class BindingFailureV1:
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
class BindingResultV1:
    capability_model_binding: Optional[CapabilityModelBindingCandidateV1]
    model_provider_binding: Optional[ModelProviderBindingCandidateV1]
    edge: BindingEdgeObservabilityV1
    failure: Optional[BindingFailureV1]


@dataclass(frozen=True)
class BindingChainResultV1:
    consistent: bool
    edge: BindingEdgeObservabilityV1
    failure: Optional[BindingFailureV1]
