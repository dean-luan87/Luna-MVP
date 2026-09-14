"""Synthetic declarations and focused binding scenarios."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Optional

from capabilities.midplatform.model_manager.model_contract_repository.model_contract_repository_types_v1 import ModelAssetContractV1
from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_types_v1 import CapabilityResolutionCandidateV1

from .adapters_v1 import build_capability_model_binding, build_model_provider_binding, check_binding_chain
from .types_v1 import CapabilityModelBindingInputV1, ModelProviderBindingInputV1


@dataclass(frozen=True)
class BindingScenarioV1:
    scenario_id: str
    category: str
    description: str
    expected_blocked: bool
    expected_failure: Optional[str] = None
    focus: Optional[str] = None


CAPABILITY_REF = "capability:object-detection"
SLOT_REF = "slot:perception:vision"
MODEL_REF = "model:yolo11n"
MODEL_VERSION = "model-version:yolo11n:v1"
WEIGHTS_VERSION = "weights:yolo11n:v1"
LOADER_REF = "loader:yolo:v1"
PROVIDER_FAMILY = "provider-family:yolo"
PROVIDER_CONTRACT = "provider-contract:yolo:v1"
PROVIDER_ADAPTER = "provider-adapter:yolo:v1"


def _model(*, lifecycle: str = "SUPPORTED", provider_family: str = PROVIDER_FAMILY) -> ModelAssetContractV1:
    return ModelAssetContractV1(
        model_asset_id=MODEL_REF,
        model_family="yolo",
        model_name="YOLO11n synthetic declaration",
        model_version="v1",
        weights_version="v1",
        weight_format="pt",
        weights_path="ref:model-asset:yolo11n",
        checksum="declared:checksum:yolo11n:v1",
        source="synthetic-governed-model-source",
        license="synthetic-reference",
        provider_family=provider_family,
        declared_loader_contract_id=LOADER_REF,
        declared_capability_contract_ids=("capability-contract:object-detection:v1",),
        declared_evidence_contract_ids=("evidence-contract:detection:v1",),
        deployment_profile_refs=("deployment-profile:synthetic",),
        benchmark_profile_refs=(),
        status=lifecycle,
        contract_lifecycle=lifecycle,
    )


def _cap_input(case_id: str, **changes: object) -> CapabilityModelBindingInputV1:
    data = CapabilityModelBindingInputV1(
        capability_ref=CAPABILITY_REF,
        capability_slot_ref=SLOT_REF,
        capability_contract_version="capability-contract:object-detection:v1",
        logical_resolution_ref=f"logical-resolution:{case_id}",
        logical_resolution=CapabilityResolutionCandidateV1(
            requirement_id=f"requirement:{case_id}",
            status="RESOLVED_UNIQUE",
            module_ref=CAPABILITY_REF,
            slot_ref=SLOT_REF,
            implementation_refs=(),
            model_asset_refs=(MODEL_REF,),
            provider_contract_refs=(PROVIDER_CONTRACT,),
            reason="synthetic logical resolution",
            recovery_available=False,
        ),
        logical_resolution_status="RESOLVED_UNIQUE",
        logical_resolution_capability_ref=CAPABILITY_REF,
        logical_resolution_slot_ref=SLOT_REF,
        capability_exists=True,
        slot_exists=True,
        model_asset_ref=MODEL_REF,
        model_asset=_model(),
        model_version_ref=MODEL_VERSION,
        weights_version_ref=WEIGHTS_VERSION,
        model_capability_declaration_ref=f"model-capability-declaration:{MODEL_REF}:object-detection:v1",
        declared_capability_ref=CAPABILITY_REF,
        declared_capability_contract_version="capability-contract:object-detection:v1",
        model_lifecycle_status="SUPPORTED",
        model_version_status="CURRENT",
        source_version_refs=("capability:v1", "slot:v1", "model:v1", "weights:v1"),
        invalidation_refs=(),
        trace_refs=(f"trace:capability-model:{case_id}",),
        provenance_refs=(f"prov:fixture:{case_id}",),
    )
    return replace(data, **changes)


def _provider_input(case_id: str, **changes: object) -> ModelProviderBindingInputV1:
    data = ModelProviderBindingInputV1(
        model_asset_ref=MODEL_REF,
        model_asset=_model(),
        model_version_ref=MODEL_VERSION,
        weights_version_ref=WEIGHTS_VERSION,
        loader_contract_ref=LOADER_REF,
        dependency_declaration_refs=("dependency:ultralytics:v8",),
        provider_family_ref=PROVIDER_FAMILY,
        provider_contract_ref=PROVIDER_CONTRACT,
        provider_adapter_ref=PROVIDER_ADAPTER,
        model_provider_declaration_ref=f"model-provider-declaration:{MODEL_REF}:{PROVIDER_FAMILY}:v1",
        model_declared_provider_family_ref=PROVIDER_FAMILY,
        model_declared_provider_adapter_ref=PROVIDER_ADAPTER,
        provider_declared_model_asset_ref=MODEL_REF,
        provider_supported_loader_contract_refs=(LOADER_REF,),
        declared_provider_contract_version="provider-contract-version:v1",
        provider_contract_version="provider-contract-version:v1",
        model_lifecycle_status="SUPPORTED",
        model_version_status="CURRENT",
        provider_declaration_status="CURRENT",
        source_version_refs=("model:v1", "weights:v1", "loader:v1", "provider:v1"),
        invalidation_refs=(),
        trace_refs=(f"trace:model-provider:{case_id}",),
        provenance_refs=(f"prov:fixture:{case_id}",),
    )
    return replace(data, **changes)


CAPABILITY_MODEL_SCENARIOS = (
    BindingScenarioV1("cap_model_valid", "CAPABILITY_MODEL", "valid Capability/Model binding", False),
    BindingScenarioV1("cap_model_missing_capability", "CAPABILITY_MODEL", "missing Capability", True, "CAPABILITY_NOT_FOUND"),
    BindingScenarioV1("cap_model_missing_slot", "CAPABILITY_MODEL", "missing Slot", True, "SLOT_NOT_FOUND"),
    BindingScenarioV1("cap_model_invalid_resolution", "CAPABILITY_MODEL", "invalid logical resolution", True, "LOGICAL_RESOLUTION_INVALID"),
    BindingScenarioV1("cap_model_missing_model", "CAPABILITY_MODEL", "missing Model declaration", True, "MODEL_DECLARATION_MISSING"),
    BindingScenarioV1("cap_model_declaration_mismatch", "CAPABILITY_MODEL", "Capability declaration mismatch", True, "CAPABILITY_DECLARATION_MISMATCH"),
    BindingScenarioV1("cap_model_contract_mismatch", "CAPABILITY_MODEL", "Capability contract version mismatch", True, "CAPABILITY_CONTRACT_VERSION_MISMATCH"),
    BindingScenarioV1("cap_model_version_stale", "CAPABILITY_MODEL", "stale Model version", True, "BINDING_STALE"),
    BindingScenarioV1("cap_model_weights_stale", "CAPABILITY_MODEL", "stale weights version", True, "BINDING_STALE"),
    BindingScenarioV1("cap_model_retired", "CAPABILITY_MODEL", "retired Model", True, "MODEL_RETIRED_OR_DEPRECATED"),
    BindingScenarioV1("cap_model_missing_provenance", "CAPABILITY_MODEL", "missing provenance", True, "PROVENANCE_INVALID"),
    BindingScenarioV1("cap_model_cross_capability", "CAPABILITY_MODEL", "cross-Capability contamination", True, "CROSS_CAPABILITY_CONTAMINATION"),
)


MODEL_PROVIDER_SCENARIOS = (
    BindingScenarioV1("model_provider_valid", "MODEL_PROVIDER", "valid Model/Provider binding", False),
    BindingScenarioV1("model_provider_missing_provider", "MODEL_PROVIDER", "missing Provider declaration", True, "PROVIDER_DECLARATION_MISSING"),
    BindingScenarioV1("model_provider_family_mismatch", "MODEL_PROVIDER", "Provider family mismatch", True, "PROVIDER_FAMILY_MISMATCH"),
    BindingScenarioV1("model_provider_adapter_mismatch", "MODEL_PROVIDER", "Provider adapter mismatch", True, "PROVIDER_ADAPTER_MISMATCH"),
    BindingScenarioV1("model_provider_loader_incompatible", "MODEL_PROVIDER", "loader incompatibility", True, "LOADER_INCOMPATIBLE"),
    BindingScenarioV1("model_provider_contract_mismatch", "MODEL_PROVIDER", "Provider contract version mismatch", True, "PROVIDER_CONTRACT_VERSION_MISMATCH"),
    BindingScenarioV1("model_provider_model_stale", "MODEL_PROVIDER", "stale Model version", True, "BINDING_STALE"),
    BindingScenarioV1("model_provider_provider_stale", "MODEL_PROVIDER", "stale Provider declaration", True, "BINDING_STALE"),
    BindingScenarioV1("model_provider_missing_provenance", "MODEL_PROVIDER", "missing provenance", True, "PROVENANCE_INVALID"),
    BindingScenarioV1("model_provider_cross_provider", "MODEL_PROVIDER", "cross-Provider contamination", True, "CROSS_PROVIDER_CONTAMINATION"),
)


CROSS_BINDING_SCENARIOS = (
    BindingScenarioV1("chain_valid", "CROSS_BINDING", "same Model chain valid", False, focus="valid"),
    BindingScenarioV1("chain_model_ref_mismatch", "CROSS_BINDING", "Model ref mismatch", True, "MODEL_REF_MISMATCH"),
    BindingScenarioV1("chain_model_version_mismatch", "CROSS_BINDING", "Model version mismatch", True, "MODEL_VERSION_MISMATCH"),
    BindingScenarioV1("chain_upstream_stale", "CROSS_BINDING", "upstream Capability/Model binding stale", True, "UPSTREAM_BINDING_STALE"),
    BindingScenarioV1("chain_downstream_stale", "CROSS_BINDING", "downstream Model/Provider binding stale", True, "DOWNSTREAM_BINDING_STALE"),
    BindingScenarioV1("chain_superseded", "CROSS_BINDING", "superseded binding rejected", True, "UPSTREAM_BINDING_STALE", focus="superseded"),
)


AUTHORITY_SCENARIOS = (
    BindingScenarioV1("authority_capability_owner", "AUTHORITY", "Capability binding owner preserved", False, focus="capability_owner"),
    BindingScenarioV1("authority_provider_owner", "AUTHORITY", "Provider binding owner preserved", False, focus="provider_owner"),
    BindingScenarioV1("authority_model_source", "AUTHORITY", "Model source owner preserved", False, focus="model_source"),
    BindingScenarioV1("authority_trace_reversible", "AUTHORITY", "trace and provenance reversible", False, focus="trace"),
    BindingScenarioV1("authority_no_execution", "AUTHORITY", "no runtime/model/provider execution", False, focus="no_execution"),
    BindingScenarioV1("authority_no_cross_mutation", "AUTHORITY", "no cross-owner mutation", False, focus="no_mutation"),
)


SCENARIOS = CAPABILITY_MODEL_SCENARIOS + MODEL_PROVIDER_SCENARIOS + CROSS_BINDING_SCENARIOS + AUTHORITY_SCENARIOS


def capability_input_for(scenario_id: str) -> CapabilityModelBindingInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "cap_model_missing_capability": changes.update(capability_ref=None, capability_exists=False)
    if scenario_id == "cap_model_missing_slot": changes.update(capability_slot_ref=None, slot_exists=False)
    if scenario_id == "cap_model_invalid_resolution": changes.update(logical_resolution_status="INVALID")
    if scenario_id == "cap_model_missing_model": changes.update(model_asset_ref=None, model_asset=None)
    if scenario_id == "cap_model_declaration_mismatch": changes.update(declared_capability_ref="capability:other")
    if scenario_id == "cap_model_contract_mismatch": changes.update(declared_capability_contract_version="capability-contract:old:v1")
    if scenario_id in {"cap_model_version_stale", "cap_model_weights_stale"}: changes.update(model_version_status="STALE", invalidation_refs=(f"invalidation:{scenario_id}",))
    if scenario_id == "cap_model_retired": changes.update(model_lifecycle_status="RETIRED")
    if scenario_id == "cap_model_missing_provenance": changes.update(provenance_refs=())
    if scenario_id == "cap_model_cross_capability": changes.update(logical_resolution_capability_ref="capability:other")
    return _cap_input(scenario_id, **changes)


def provider_input_for(scenario_id: str) -> ModelProviderBindingInputV1:
    changes: dict[str, object] = {}
    if scenario_id == "model_provider_missing_provider": changes.update(provider_contract_ref=None, provider_adapter_ref=None, provider_family_ref=None, model_provider_declaration_ref=None)
    if scenario_id == "model_provider_family_mismatch": changes.update(provider_family_ref="provider-family:other")
    if scenario_id == "model_provider_adapter_mismatch": changes.update(provider_adapter_ref="provider-adapter:other:v1")
    if scenario_id == "model_provider_loader_incompatible": changes.update(provider_supported_loader_contract_refs=("loader:other:v1",))
    if scenario_id == "model_provider_contract_mismatch": changes.update(provider_contract_version="provider-contract-version:old")
    if scenario_id == "model_provider_model_stale": changes.update(model_version_status="STALE", invalidation_refs=(f"invalidation:{scenario_id}",))
    if scenario_id == "model_provider_provider_stale": changes.update(provider_declaration_status="STALE", invalidation_refs=(f"invalidation:{scenario_id}",))
    if scenario_id == "model_provider_missing_provenance": changes.update(provenance_refs=())
    if scenario_id == "model_provider_cross_provider": changes.update(provider_declared_model_asset_ref="model:other")
    return _provider_input(scenario_id, **changes)


def chain_inputs_for(scenario_id: str):
    cap = build_capability_model_binding(_cap_input(scenario_id), binding_id=scenario_id).capability_model_binding
    provider = build_model_provider_binding(_provider_input(scenario_id), binding_id=scenario_id).model_provider_binding
    assert cap is not None and provider is not None
    if scenario_id == "chain_model_ref_mismatch": provider = replace(provider, model_asset_ref="model:other")
    if scenario_id == "chain_model_version_mismatch": provider = replace(provider, model_version_ref="model-version:yolo11n:v2")
    if scenario_id == "chain_upstream_stale": cap = replace(cap, lifecycle_status="STALE", invalidation_refs=("invalidation:upstream",))
    if scenario_id == "chain_downstream_stale": provider = replace(provider, lifecycle_status="STALE", invalidation_refs=("invalidation:downstream",))
    if scenario_id == "chain_superseded": cap = replace(cap, lifecycle_status="SUPERSEDED", invalidation_refs=("supersession:upstream",))
    return cap, provider
