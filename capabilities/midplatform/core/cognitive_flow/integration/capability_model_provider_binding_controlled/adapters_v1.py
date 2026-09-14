"""Synthetic candidate-only binding validators and consistency adapter."""

from __future__ import annotations

from typing import Optional, Tuple

from .types_v1 import (
    BindingChainResultV1,
    BindingEdgeObservabilityV1,
    BindingFailureV1,
    BindingResultV1,
    CapabilityModelBindingCandidateV1,
    CapabilityModelBindingInputV1,
    ModelProviderBindingCandidateV1,
    ModelProviderBindingInputV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.canonical_source_state_outcome_return_controlled.types_v1 import (
    EdgeObservabilityCandidateV1,
)


VALID_LOGICAL_STATUSES = {"VALID", "RESOLVED_UNIQUE", "READY_CANDIDATE"}
STALE_MODEL_STATUSES = {"STALE", "EXPIRED", "INVALID", "VERSION_MISMATCH"}
STALE_PROVIDER_STATUSES = {"STALE", "EXPIRED", "INVALID", "VERSION_MISMATCH"}


def _edge(
    *,
    transition_id: str,
    trace_id: str,
    producer: str,
    consumer: str,
    authority_owner: str,
    responsibility_owner: str,
    transition_class: str,
    input_refs: Tuple[str, ...],
    input_versions: Tuple[str, ...],
    output_refs: Tuple[str, ...],
    output_versions: Tuple[str, ...],
    status: str,
    invalidation_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
    failure_classification: Optional[str],
    next_target: str,
) -> BindingEdgeObservabilityV1:
    edge_provenance = provenance_refs or (f"prov:edge:{transition_id}:binding-adapter",)
    edge = EdgeObservabilityCandidateV1(
        transition_id=transition_id,
        trace_id=trace_id,
        parent_transition_refs=(),
        concern_ref=None,
        reasoning_cycle_ref=None,
        producer=producer,
        consumer=consumer,
        authority_owner=authority_owner,
        responsibility_owner=responsibility_owner,
        transition_class=transition_class,
        input_refs=input_refs,
        input_versions=input_versions,
        output_refs=output_refs,
        output_versions=output_versions,
        admission_or_validation_status=status,
        constraint_refs=(),
        evidence_refs=(),
        provenance_refs=edge_provenance,
        invalidation_refs=invalidation_refs,
        failure_classification=failure_classification,
        blocker_refs=(),
        next_target=next_target,
    )
    return BindingEdgeObservabilityV1(edge=edge)


def _failure(
    *,
    ref: str,
    classification: str,
    reason: str,
    owner: str,
    next_target: str,
    source_refs: Tuple[str, ...],
    trace_refs: Tuple[str, ...],
    provenance_refs: Tuple[str, ...],
    invalidation_refs: Tuple[str, ...] = (),
) -> BindingFailureV1:
    return BindingFailureV1(
        failure_ref=ref,
        classification=classification,
        reason=reason,
        responsible_owner=owner,
        next_target=next_target,
        source_refs=source_refs,
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        invalidation_refs=invalidation_refs,
    )


def _cap_failure(data: CapabilityModelBindingInputV1) -> Optional[BindingFailureV1]:
    source = (data.capability_ref or data.model_asset_ref or "binding:capability-model",)
    if not data.synthetic_only or not data.candidate_only:
        return _failure(ref="failure:capability-model:synthetic", classification="NON_SYNTHETIC_INPUT", reason="binding input is not synthetic candidate-only data", owner="Capability Model binding adapter", next_target="caller", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.capability_exists or not data.capability_ref:
        return _failure(ref="failure:capability-model:capability", classification="CAPABILITY_NOT_FOUND", reason="Capability identity is unavailable", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.slot_exists or not data.capability_slot_ref:
        return _failure(ref="failure:capability-model:slot", classification="SLOT_NOT_FOUND", reason="Capability Slot is unavailable", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.logical_resolution_ref or data.logical_resolution_status not in VALID_LOGICAL_STATUSES:
        return _failure(ref="failure:capability-model:resolution", classification="LOGICAL_RESOLUTION_INVALID", reason="logical Capability resolution is not valid", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.logical_resolution_capability_ref != data.capability_ref or data.logical_resolution_slot_ref not in {None, data.capability_slot_ref}:
        return _failure(ref="failure:capability-model:cross-capability", classification="CROSS_CAPABILITY_CONTAMINATION", reason="logical resolution is bound to another Capability or Slot", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.model_asset_ref or data.model_asset is None:
        return _failure(ref="failure:capability-model:model", classification="MODEL_DECLARATION_MISSING", reason="Model declaration is unavailable", owner="Model Governance", next_target="Model Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.model_capability_declaration_ref:
        return _failure(ref="failure:capability-model:declaration", classification="MODEL_CAPABILITY_DECLARATION_MISSING", reason="model-side Capability declaration ref is missing", owner="Model Governance", next_target="Model Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.declared_capability_ref != data.capability_ref:
        return _failure(ref="failure:capability-model:declaration-mismatch", classification="CAPABILITY_DECLARATION_MISMATCH", reason="model declaration does not match requested Capability", owner="Model Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.declared_capability_contract_version != data.capability_contract_version:
        return _failure(ref="failure:capability-model:contract", classification="CAPABILITY_CONTRACT_VERSION_MISMATCH", reason="Capability contract versions are incompatible", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.source_version_refs or data.invalidation_refs or data.model_version_status in STALE_MODEL_STATUSES:
        return _failure(ref="failure:capability-model:stale", classification="BINDING_STALE", reason="Capability or Model source version is stale/invalidated", owner="Capability Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    if data.model_lifecycle_status in {"RETIRED", "DEPRECATED"}:
        return _failure(ref="failure:capability-model:lifecycle", classification="MODEL_RETIRED_OR_DEPRECATED", reason="Model lifecycle blocks a new binding", owner="Model Governance", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.provenance_refs:
        return _failure(ref="failure:capability-model:provenance", classification="PROVENANCE_INVALID", reason="Capability/Model declarations have no provenance", owner="Capability Model binding adapter", next_target="Capability Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return None


def build_capability_model_binding(data: CapabilityModelBindingInputV1, *, binding_id: str) -> BindingResultV1:
    failure = _cap_failure(data)
    trace_id = data.trace_refs[0] if data.trace_refs else f"trace:capability-model:{binding_id}"
    edge = _edge(
        transition_id=f"transition:capability-model:{binding_id}",
        trace_id=trace_id,
        producer="Capability Governance binding adapter",
        consumer="Runtime Admission",
        authority_owner="Capability Governance",
        responsibility_owner="Capability Governance" if failure is None or failure.responsible_owner == "Capability Governance" else failure.responsible_owner,
        transition_class="BINDING / VALIDATION",
        input_refs=tuple(ref for ref in (data.capability_ref, data.capability_slot_ref, data.logical_resolution_ref, data.model_asset_ref, data.model_capability_declaration_ref) if ref),
        input_versions=data.source_version_refs,
        output_refs=() if failure else (f"binding:capability-model:{binding_id}",),
        output_versions=() if failure else (f"binding-v:{binding_id}:v1",),
        status="BLOCKED" if failure else "VALID",
        invalidation_refs=data.invalidation_refs,
        provenance_refs=data.provenance_refs,
        failure_classification=failure.classification if failure else None,
        next_target=failure.next_target if failure else "Runtime Admission",
    )
    if failure:
        return BindingResultV1(None, None, edge, failure)
    candidate = CapabilityModelBindingCandidateV1(
        binding_id=f"binding:capability-model:{binding_id}",
        binding_version=f"binding-v:{binding_id}:v1",
        capability_ref=data.capability_ref or "",
        capability_slot_ref=data.capability_slot_ref,
        capability_contract_version=data.capability_contract_version or "",
        logical_resolution_ref=data.logical_resolution_ref or "",
        model_asset_ref=data.model_asset_ref or "",
        model_version_ref=data.model_version_ref or "",
        weights_version_ref=data.weights_version_ref or "",
        model_capability_declaration_ref=data.model_capability_declaration_ref or "",
        compatibility_status="COMPATIBLE",
        compatibility_constraints=("declared-compatibility-only", "runtime-admission-required"),
        source_version_refs=data.source_version_refs,
        invalidation_refs=data.invalidation_refs,
        trace_refs=data.trace_refs,
        provenance_refs=data.provenance_refs,
    )
    return BindingResultV1(candidate, None, edge, None)


def _provider_failure(data: ModelProviderBindingInputV1) -> Optional[BindingFailureV1]:
    source = (data.model_asset_ref or data.provider_contract_ref or "binding:model-provider",)
    if not data.synthetic_only or not data.candidate_only:
        return _failure(ref="failure:model-provider:synthetic", classification="NON_SYNTHETIC_INPUT", reason="binding input is not synthetic candidate-only data", owner="Model Provider binding adapter", next_target="caller", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.model_asset_ref or data.model_asset is None:
        return _failure(ref="failure:model-provider:model", classification="MODEL_DECLARATION_MISSING", reason="Model declaration is unavailable", owner="Model Governance", next_target="Model Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.model_provider_declaration_ref or not data.provider_family_ref or not data.provider_contract_ref or not data.provider_adapter_ref:
        return _failure(ref="failure:model-provider:provider", classification="PROVIDER_DECLARATION_MISSING", reason="Provider family/contract/adapter declaration is unavailable", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.model_declared_provider_family_ref != data.provider_family_ref:
        return _failure(ref="failure:model-provider:family", classification="PROVIDER_FAMILY_MISMATCH", reason="Model and Provider families are incompatible", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.provider_declared_model_asset_ref != data.model_asset_ref:
        return _failure(ref="failure:model-provider:cross-provider", classification="CROSS_PROVIDER_CONTAMINATION", reason="Provider declaration is bound to another Model asset", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.model_declared_provider_adapter_ref != data.provider_adapter_ref:
        return _failure(ref="failure:model-provider:adapter", classification="PROVIDER_ADAPTER_MISMATCH", reason="Model and Provider adapter declarations are incompatible", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.loader_contract_ref or data.loader_contract_ref not in data.provider_supported_loader_contract_refs:
        return _failure(ref="failure:model-provider:loader", classification="LOADER_INCOMPATIBLE", reason="Provider declaration does not support the declared loader contract", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if data.declared_provider_contract_version != data.provider_contract_version:
        return _failure(ref="failure:model-provider:contract", classification="PROVIDER_CONTRACT_VERSION_MISMATCH", reason="Provider contract versions are incompatible", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    if not data.source_version_refs or data.invalidation_refs or data.model_version_status in STALE_MODEL_STATUSES or data.provider_declaration_status in STALE_PROVIDER_STATUSES:
        return _failure(ref="failure:model-provider:stale", classification="BINDING_STALE", reason="Model or Provider source version is stale/invalidated", owner="Provider Governance", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs, invalidation_refs=data.invalidation_refs)
    if not data.provenance_refs:
        return _failure(ref="failure:model-provider:provenance", classification="PROVENANCE_INVALID", reason="Model/Provider declarations have no provenance", owner="Model Provider binding adapter", next_target="Provider Governance", source_refs=source, trace_refs=data.trace_refs, provenance_refs=data.provenance_refs)
    return None


def build_model_provider_binding(data: ModelProviderBindingInputV1, *, binding_id: str) -> BindingResultV1:
    failure = _provider_failure(data)
    trace_id = data.trace_refs[0] if data.trace_refs else f"trace:model-provider:{binding_id}"
    edge = _edge(
        transition_id=f"transition:model-provider:{binding_id}",
        trace_id=trace_id,
        producer="Provider Governance binding adapter",
        consumer="Runtime Admission",
        authority_owner="Provider Governance",
        responsibility_owner="Provider Governance" if failure is None or failure.responsible_owner == "Provider Governance" else failure.responsible_owner,
        transition_class="BINDING / VALIDATION",
        input_refs=tuple(ref for ref in (data.model_asset_ref, data.loader_contract_ref, data.model_provider_declaration_ref, data.provider_family_ref, data.provider_contract_ref, data.provider_adapter_ref) if ref),
        input_versions=data.source_version_refs,
        output_refs=() if failure else (f"binding:model-provider:{binding_id}",),
        output_versions=() if failure else (f"binding-v:{binding_id}:v1",),
        status="BLOCKED" if failure else "VALID",
        invalidation_refs=data.invalidation_refs,
        provenance_refs=data.provenance_refs,
        failure_classification=failure.classification if failure else None,
        next_target=failure.next_target if failure else "Runtime Admission",
    )
    if failure:
        return BindingResultV1(None, None, edge, failure)
    candidate = ModelProviderBindingCandidateV1(
        binding_id=f"binding:model-provider:{binding_id}",
        binding_version=f"binding-v:{binding_id}:v1",
        model_asset_ref=data.model_asset_ref or "",
        model_version_ref=data.model_version_ref or "",
        weights_version_ref=data.weights_version_ref or "",
        loader_contract_ref=data.loader_contract_ref or "",
        dependency_declaration_refs=data.dependency_declaration_refs,
        provider_family_ref=data.provider_family_ref or "",
        provider_contract_ref=data.provider_contract_ref or "",
        provider_adapter_ref=data.provider_adapter_ref or "",
        model_provider_declaration_ref=data.model_provider_declaration_ref or "",
        compatibility_status="COMPATIBLE",
        compatibility_constraints=("declared-compatibility-only", "provider-admission-required"),
        source_version_refs=data.source_version_refs,
        invalidation_refs=data.invalidation_refs,
        trace_refs=data.trace_refs,
        provenance_refs=data.provenance_refs,
    )
    return BindingResultV1(None, candidate, edge, None)


def check_binding_chain(capability_binding: CapabilityModelBindingCandidateV1, provider_binding: ModelProviderBindingCandidateV1, *, chain_id: str) -> BindingChainResultV1:
    invalidation_refs = capability_binding.invalidation_refs + provider_binding.invalidation_refs
    failure: Optional[BindingFailureV1] = None
    if capability_binding.lifecycle_status in {"STALE", "SUPERSEDED"}:
        failure = _failure(ref=f"failure:chain:upstream:{chain_id}", classification="UPSTREAM_BINDING_STALE", reason="Capability↔Model binding is not current", owner="Capability Governance", next_target="Capability Governance", source_refs=(capability_binding.binding_id,), trace_refs=capability_binding.trace_refs, provenance_refs=capability_binding.provenance_refs, invalidation_refs=invalidation_refs)
    elif provider_binding.lifecycle_status in {"STALE", "SUPERSEDED"}:
        failure = _failure(ref=f"failure:chain:downstream:{chain_id}", classification="DOWNSTREAM_BINDING_STALE", reason="Model↔Provider binding is not current", owner="Provider Governance", next_target="Provider Governance", source_refs=(provider_binding.binding_id,), trace_refs=provider_binding.trace_refs, provenance_refs=provider_binding.provenance_refs, invalidation_refs=invalidation_refs)
    elif capability_binding.model_asset_ref != provider_binding.model_asset_ref:
        failure = _failure(ref=f"failure:chain:model:{chain_id}", classification="MODEL_REF_MISMATCH", reason="binding chain references different Model assets", owner="Capability/Provider binding boundary", next_target="Runtime Admission", source_refs=(capability_binding.binding_id, provider_binding.binding_id), trace_refs=capability_binding.trace_refs + provider_binding.trace_refs, provenance_refs=capability_binding.provenance_refs + provider_binding.provenance_refs)
    elif capability_binding.model_version_ref != provider_binding.model_version_ref or capability_binding.weights_version_ref != provider_binding.weights_version_ref:
        failure = _failure(ref=f"failure:chain:version:{chain_id}", classification="MODEL_VERSION_MISMATCH", reason="binding chain references different Model or weights versions", owner="Capability/Provider binding boundary", next_target="Runtime Admission", source_refs=(capability_binding.binding_id, provider_binding.binding_id), trace_refs=capability_binding.trace_refs + provider_binding.trace_refs, provenance_refs=capability_binding.provenance_refs + provider_binding.provenance_refs)
    edge = _edge(
        transition_id=f"transition:binding-chain:{chain_id}",
        trace_id=(capability_binding.trace_refs + provider_binding.trace_refs or (f"trace:chain:{chain_id}",))[0],
        producer="Capability/Provider binding consistency adapter",
        consumer="Runtime Admission",
        authority_owner="Capability Governance and Provider Governance",
        responsibility_owner=failure.responsible_owner if failure else "Capability/Provider binding consistency adapter",
        transition_class="VALIDATION",
        input_refs=(capability_binding.binding_id, provider_binding.binding_id),
        input_versions=capability_binding.source_version_refs + provider_binding.source_version_refs,
        output_refs=() if failure else (f"binding-chain:{chain_id}",),
        output_versions=() if failure else (f"binding-chain-v:{chain_id}:v1",),
        status="BLOCKED" if failure else "VALID",
        invalidation_refs=invalidation_refs,
        provenance_refs=capability_binding.provenance_refs + provider_binding.provenance_refs,
        failure_classification=failure.classification if failure else None,
        next_target=failure.next_target if failure else "Runtime Admission",
    )
    return BindingChainResultV1(failure is None, edge, failure)

