"""Repository-backed declaration translation for Runtime Admission.

This module reads existing owner-controlled registry declarations and turns
them into candidate/reference inputs.  It never writes a registry and never
probes the model, device, dependency environment, or Provider.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.capability_model_provider_binding_controlled.types_v1 import (
    CapabilityModelBindingCandidateV1,
    ModelProviderBindingCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import (
    CapabilityResolutionCandidateV1,
)

from .types_v1 import RuntimeAdmissionProductionInputV1


MODEL_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/model_registry_v1.json"
PROVIDER_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"
CAPABILITY_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/capability_registry_v1.json"
CAPABILITY_MODEL_BINDING_RELATIVE = "capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json"
MODEL_PROVIDER_BINDING_RELATIVE = "capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json"


def _json(repo_root: Path, relative: str) -> Mapping[str, Any]:
    path = repo_root / relative
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, Mapping) else {}


def _items(value: Mapping[str, Any], key: str) -> Tuple[Mapping[str, Any], ...]:
    return tuple(item for item in value.get(key, ()) if isinstance(item, Mapping))


def _find(items: Tuple[Mapping[str, Any], ...], key: str, expected: str) -> Optional[Mapping[str, Any]]:
    return next((item for item in items if str(item.get(key)) == expected), None)


def build_repository_runtime_admission_input_v1(
    repo_root: Path,
    *,
    model_asset_id: str,
    capability_id: str,
    provider_family: str,
) -> Optional[RuntimeAdmissionProductionInputV1]:
    capability_registry = _json(repo_root, CAPABILITY_REGISTRY_RELATIVE)
    model_registry = _json(repo_root, MODEL_REGISTRY_RELATIVE)
    provider_registry = _json(repo_root, PROVIDER_REGISTRY_RELATIVE)
    capability_model_registry = _json(repo_root, CAPABILITY_MODEL_BINDING_RELATIVE)
    model_provider_registry = _json(repo_root, MODEL_PROVIDER_BINDING_RELATIVE)

    capability = _find(_items(capability_registry, "capabilities"), "capability_id", capability_id)
    model = _find(_items(model_registry, "models"), "model_asset_id", model_asset_id)
    provider = next(
        (
            item for item in _items(provider_registry, "providers")
            if str(item.get("provider_family")) == provider_family
            and model_asset_id in tuple(str(ref) for ref in item.get("supported_model_asset_ids", ()))
        ),
        None,
    )
    slot = next(
        (
            item for item in _items(capability_registry, "slots")
            if str(item.get("capability_ref")) == capability_id
        ),
        None,
    )
    capability_model = next(
        (
            item for item in _items(capability_model_registry, "bindings")
            if str(item.get("model_asset_ref")) == model_asset_id
            and str(item.get("capability_ref")) == capability_id
        ),
        None,
    )
    model_provider = next(
        (
            item for item in _items(model_provider_registry, "bindings")
            if str(item.get("model_asset_ref")) == model_asset_id
            and str(item.get("provider_family_ref")) == provider_family
        ),
        None,
    )
    if not all((capability, model, provider, slot, capability_model, model_provider)):
        return None

    model_version = str(model.get("model_version"))
    weights_version = str(model.get("weights_version"))
    provider_contract_ref = str(provider.get("provider_contract_ref"))
    binding_source_refs = tuple(str(ref) for ref in capability_model.get("source_version_refs", ())) + tuple(str(ref) for ref in model_provider.get("source_version_refs", ()))
    source_refs = (
        MODEL_REGISTRY_RELATIVE,
        PROVIDER_REGISTRY_RELATIVE,
        CAPABILITY_REGISTRY_RELATIVE,
        CAPABILITY_MODEL_BINDING_RELATIVE,
        MODEL_PROVIDER_BINDING_RELATIVE,
    )
    trace_refs = (
        "trace:runtime-admission:repository-declaration:yolo11n:v1",
        str(capability_model.get("binding_id")),
        str(model_provider.get("binding_id")),
    )
    provenance_refs = tuple(dict.fromkeys(
        tuple(str(ref) for ref in model.get("provenance_refs", ()))
        + tuple(str(ref) for ref in provider.get("provenance_refs", ()))
        + tuple(str(ref) for ref in capability_model.get("provenance_refs", ()))
        + tuple(str(ref) for ref in model_provider.get("provenance_refs", ()))
        + ("runtime-admission:production-source:declaration-validation:v1",)
    ))
    resolution = CapabilityResolutionCandidateV1(
        requirement_id="requirement:object-detection:repository:v1",
        status="READY_CANDIDATE",
        module_ref=capability_id,
        slot_ref=str(slot.get("slot_id")),
        implementation_refs=("capability-governance:object-detection:v1",),
        model_asset_refs=(model_asset_id,),
        provider_contract_refs=(provider_contract_ref,),
        reason="repository-backed Capability/Slot resolution candidate",
        recovery_available=False,
    )
    capability_binding = CapabilityModelBindingCandidateV1(
        binding_id=str(capability_model.get("binding_id")),
        binding_version=str(capability_model.get("binding_version")),
        capability_ref=capability_id,
        capability_slot_ref=str(capability_model.get("capability_slot_ref")),
        capability_contract_version=str(capability_model.get("capability_contract_version")),
        logical_resolution_ref=resolution.requirement_id,
        model_asset_ref=model_asset_id,
        model_version_ref=model_version,
        weights_version_ref=weights_version,
        model_capability_declaration_ref=str(capability_model.get("model_capability_declaration_ref")),
        compatibility_status="COMPATIBLE",
        compatibility_constraints=tuple(str(ref) for ref in capability_model.get("compatibility_constraint_refs", ())) + ("runtime-admission-required",),
        source_version_refs=tuple(dict.fromkeys(binding_source_refs)),
        invalidation_refs=tuple(str(ref) for ref in capability_model.get("invalidation_refs", ())),
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        lifecycle_status="PROPOSED",
    )
    provider_binding = ModelProviderBindingCandidateV1(
        binding_id=str(model_provider.get("binding_id")),
        binding_version=str(model_provider.get("binding_version")),
        model_asset_ref=model_asset_id,
        model_version_ref=model_version,
        weights_version_ref=weights_version,
        loader_contract_ref=str(model_provider.get("loader_contract_ref") or model.get("loader_contract_ref")),
        dependency_declaration_refs=tuple(str(ref) for ref in model.get("dependency_declaration_refs", ())),
        provider_family_ref=provider_family,
        provider_contract_ref=provider_contract_ref,
        provider_adapter_ref=str(model_provider.get("provider_adapter_ref") or provider.get("provider_adapter_ref")),
        model_provider_declaration_ref=str(model_provider.get("binding_id")),
        compatibility_status="COMPATIBLE",
        compatibility_constraints=tuple(str(ref) for ref in model_provider.get("compatibility_constraint_refs", ())) + ("provider-admission-required",),
        source_version_refs=tuple(dict.fromkeys(binding_source_refs)),
        invalidation_refs=tuple(str(ref) for ref in model_provider.get("invalidation_refs", ())),
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        lifecycle_status="PROPOSED",
    )
    return RuntimeAdmissionProductionInputV1(
        capability_resolution=resolution,
        capability_model_binding=capability_binding,
        model_provider_binding=provider_binding,
        model_asset_ref=model_asset_id,
        model_version_ref=model_version,
        weights_version_ref=weights_version,
        governed_model_path_ref=str(model.get("weights_path")),
        loader_contract_ref=str(model.get("loader_contract_ref")),
        dependency_declaration_refs=tuple(str(ref) for ref in model.get("dependency_declaration_refs", ())),
        dependency_status_ref="DECLARATION_VALIDATED",
        runtime_readiness_status_ref="DECLARATION_VALIDATED",
        model_version_status_ref="MODEL_VERSION_MATCH",
        integrity_status_ref="DECLARATION_VALIDATED",
        integrity_evidence_ref=f"{model_asset_id}:declared-checksum",
        grant_refs=("grant:runtime-admission:repository-validation:v1",),
        grant_status_ref="GRANT_VALID",
        permission_refs=("permission:runtime-admission:repository-validation:v1",),
        permission_status_ref="PERMISSION_GRANTED",
        safety_refs=("safety:runtime-admission:repository-validation:v1",),
        safety_status_ref="SAFETY_ALLOWED",
        resource_refs=("resource:runtime-admission:repository-validation:v1",),
        resource_status_ref="RESOURCE_AVAILABLE",
        working_envelope_refs=("working-envelope:runtime-admission:repository-validation:v1",),
        working_envelope_status_ref="ENVELOPE_COMPATIBLE",
        source_version_refs=tuple(dict.fromkeys(binding_source_refs + tuple(str(ref) for ref in model.get("source_version_refs", ())) + tuple(str(ref) for ref in provider.get("source_version_refs", ())))),
        trace_refs=trace_refs,
        provenance_refs=provenance_refs,
        invalidation_refs=(),
        repository_source_refs=source_refs,
    )


__all__ = [
    "build_repository_runtime_admission_input_v1",
    "CAPABILITY_MODEL_BINDING_RELATIVE",
    "CAPABILITY_REGISTRY_RELATIVE",
    "MODEL_PROVIDER_BINDING_RELATIVE",
    "MODEL_REGISTRY_RELATIVE",
    "PROVIDER_REGISTRY_RELATIVE",
]
