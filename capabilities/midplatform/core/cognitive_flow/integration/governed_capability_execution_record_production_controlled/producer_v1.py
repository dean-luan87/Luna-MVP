"""Repository-backed declaration inspection and fail-closed production.

The producer never fabricates governed records.  A complete bundle can only
be returned after the canonical registries and runtime-admission source are
available; the current YOLO11n repository state intentionally returns a
blocked result because those declarations are incomplete.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from .types_v1 import (
    GovernedDeclarationInventoryV1,
    GovernedExecutionRecordBundleV1,
    GovernedRecordProductionResultV1,
)


MODEL_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/model_registry_v1.json"
PROVIDER_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"
CAPABILITY_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/capability_registry_v1.json"
CAPABILITY_MODEL_BINDING_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json"
MODEL_PROVIDER_BINDING_REGISTRY_RELATIVE = "capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json"
OFFICIAL_CATALOG_RELATIVE = "capabilities/midplatform/model_manager/registries/universal_capability_slot/official_capability_catalog_governance_v1.py"
MODEL_CONTRACT_REPOSITORY_RELATIVE = "capabilities/midplatform/model_manager/model_contract_repository/model_contract_repository_registry_v1.py"
RUNTIME_ADMISSION_INTEGRATION_RELATIVE = "capabilities/midplatform/core/cognitive_flow/integration/logical_capability_to_runtime_admission_candidate_adapter_controlled"
RUNTIME_ADMISSION_PRODUCTION_RELATIVE = "capabilities/midplatform/core/cognitive_flow/integration/runtime_admission_production_controlled"
RUNTIME_ADMISSION_PRODUCTION_MARKER = "assess_runtime_admission_production_v1"


def _load_json(repo_root: Path, relative: str) -> Mapping[str, Any]:
    path = repo_root / relative
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, Mapping) else {}


def _items(registry: Mapping[str, Any], key: str) -> Tuple[Mapping[str, Any], ...]:
    values = registry.get(key, ())
    return tuple(item for item in values if isinstance(item, Mapping))


def _normal_capability_id(value: str) -> str:
    return value.removeprefix("capability:").removesuffix(":v1").replace("-", "_").lower()


def inspect_repository_declarations_v1(
    repo_root: Path,
    *,
    target_model_asset_id: str,
    target_capability_contract_id: str,
    target_provider_family: str,
) -> GovernedDeclarationInventoryV1:
    model_registry = _load_json(repo_root, MODEL_REGISTRY_RELATIVE)
    provider_registry = _load_json(repo_root, PROVIDER_REGISTRY_RELATIVE)
    capability_registry = _load_json(repo_root, CAPABILITY_REGISTRY_RELATIVE)
    capability_model_registry = _load_json(repo_root, CAPABILITY_MODEL_BINDING_REGISTRY_RELATIVE)
    model_provider_registry = _load_json(repo_root, MODEL_PROVIDER_BINDING_REGISTRY_RELATIVE)
    capability_items = _items(capability_registry, "capabilities")
    model_items = _items(model_registry, "models")
    provider_items = _items(provider_registry, "providers")
    model_contract_source = repo_root / MODEL_CONTRACT_REPOSITORY_RELATIVE
    runtime_source = repo_root / RUNTIME_ADMISSION_INTEGRATION_RELATIVE
    runtime_production_source = repo_root / RUNTIME_ADMISSION_PRODUCTION_RELATIVE

    model_contract_candidate_found = bool(
        model_contract_source.is_file()
        and target_model_asset_id in model_contract_source.read_text(encoding="utf-8")
    )
    provider_contract_candidate_found = bool(
        model_contract_source.is_file()
        and target_provider_family in model_contract_source.read_text(encoding="utf-8")
    )
    target_capability_id = _normal_capability_id(target_capability_contract_id)
    capability_registry_entry_found = any(
        _normal_capability_id(str(item.get("capability_id"))) == target_capability_id
        for item in capability_items
    )
    model_registry_entry_found = any(
        str(item.get("model_asset_id")) == target_model_asset_id
        and bool(item.get("model_version"))
        and bool(item.get("weights_version"))
        and bool(item.get("loader_contract_ref"))
        and bool(item.get("capability_declaration_refs"))
        and bool(item.get("provider_compatibility_declaration_refs"))
        and item.get("owner") == "Model Governance"
        and bool(item.get("provenance_refs"))
        for item in model_items
    )
    provider_registry_entry_found = any(
        (
            str(item.get("model_family")) == target_provider_family
            or str(item.get("provider_family")) == target_provider_family
        )
        and bool(item.get("provider_contract_ref"))
        and bool(item.get("provider_contract_version"))
        and isinstance(item.get("provider_contract"), Mapping)
        and bool(item.get("provenance_refs"))
        for item in provider_items
    )
    slot_items = _items(capability_registry, "slots")
    capability_slot_declaration_found = any(
        _normal_capability_id(str(item.get("capability_contract_ref"))) == target_capability_id
        and bool(item.get("slot_id"))
        and bool(item.get("slot_version"))
        and bool(item.get("provenance_refs"))
        for item in slot_items
    )
    capability_model_items = _items(capability_model_registry, "bindings")
    capability_model_declaration_found = bool(
        any(
            str(item.get("model_asset_ref")) == target_model_asset_id
            and _normal_capability_id(str(item.get("capability_contract_version"))) == target_capability_id
            and str(item.get("lifecycle_owner")) in {"Capability Governance", "Capability Registry / Capability Governance"}
            and bool(item.get("binding_id"))
            and bool(item.get("binding_version"))
            and bool(item.get("provenance_refs"))
            for item in capability_model_items
        )
    )
    model_provider_items = _items(model_provider_registry, "bindings")
    model_provider_declaration_found = bool(
        any(
            str(item.get("model_asset_ref")) == target_model_asset_id
            and str(item.get("provider_family_ref")) == target_provider_family
            and str(item.get("lifecycle_owner")) == "Provider Governance"
            and bool(item.get("binding_id"))
            and bool(item.get("binding_version"))
            and bool(item.get("provenance_refs"))
            for item in model_provider_items
        )
        and provider_registry_entry_found
        and model_registry_entry_found
    )
    runtime_admission_source_found = bool(
        runtime_production_source.is_dir()
        and (runtime_production_source / "producer_v1.py").is_file()
        and RUNTIME_ADMISSION_PRODUCTION_MARKER in (runtime_production_source / "producer_v1.py").read_text(encoding="utf-8")
    )

    missing = []
    if not capability_registry_entry_found:
        missing.append("CAPABILITY_DECLARATION")
    if not capability_slot_declaration_found:
        missing.append("CAPABILITY_SLOT_DECLARATION")
    if not model_registry_entry_found:
        missing.append("MODEL_REGISTRY_DECLARATION")
    if not capability_model_declaration_found:
        missing.append("CAPABILITY_MODEL_GOVERNED_BINDING_DECLARATION")
    if not provider_registry_entry_found:
        missing.append("PROVIDER_REGISTRY_DECLARATION")
    if not model_provider_declaration_found:
        missing.append("MODEL_PROVIDER_GOVERNED_BINDING_DECLARATION")
    if not runtime_admission_source_found:
        missing.append("RUNTIME_ADMISSION_PRODUCTION_SOURCE")

    return GovernedDeclarationInventoryV1(
        target_model_asset_id=target_model_asset_id,
        target_capability_contract_id=target_capability_contract_id,
        target_provider_family=target_provider_family,
        source_refs=(
            MODEL_REGISTRY_RELATIVE,
            PROVIDER_REGISTRY_RELATIVE,
            CAPABILITY_REGISTRY_RELATIVE,
            CAPABILITY_MODEL_BINDING_REGISTRY_RELATIVE,
            MODEL_PROVIDER_BINDING_REGISTRY_RELATIVE,
            OFFICIAL_CATALOG_RELATIVE,
            MODEL_CONTRACT_REPOSITORY_RELATIVE,
            RUNTIME_ADMISSION_INTEGRATION_RELATIVE,
            RUNTIME_ADMISSION_PRODUCTION_RELATIVE,
        ),
        capability_registry_entry_found=capability_registry_entry_found,
        capability_slot_declaration_found=capability_slot_declaration_found,
        model_registry_entry_found=model_registry_entry_found,
        model_contract_candidate_found=model_contract_candidate_found,
        capability_model_declaration_found=capability_model_declaration_found,
        provider_registry_entry_found=provider_registry_entry_found,
        provider_contract_candidate_found=provider_contract_candidate_found,
        model_provider_declaration_found=model_provider_declaration_found,
        runtime_admission_source_found=runtime_admission_source_found,
        missing_declarations=tuple(missing),
    )


def produce_governed_execution_records_v1(
    repo_root: Path,
    *,
    target_model_asset_id: str,
    target_capability_contract_id: str,
    target_provider_family: str,
) -> GovernedRecordProductionResultV1:
    inventory = inspect_repository_declarations_v1(
        repo_root,
        target_model_asset_id=target_model_asset_id,
        target_capability_contract_id=target_capability_contract_id,
        target_provider_family=target_provider_family,
    )
    if inventory.missing_declarations:
        return GovernedRecordProductionResultV1(
            status="BLOCKED_BY_MISSING_CANONICAL_DECLARATION",
            inventory=inventory,
            bundle=None,
            missing_declarations=inventory.missing_declarations,
            responsible_owners=(
                "Capability Governance",
                "Model Governance",
                "Provider Governance",
                "Runtime Admission",
            ),
            trace_refs=("trace:governed-record-production:blocked",),
            provenance_refs=inventory.source_refs,
        )

    # The repository currently cannot reach this branch without a real
    # Runtime Admission producer and owner-issued records.  Keep the branch
    # fail-closed rather than constructing records from registry strings.
    return GovernedRecordProductionResultV1(
        status="BLOCKED_BY_MISSING_OWNER_ISSUED_RECORDS",
        inventory=inventory,
        bundle=None,
        missing_declarations=("OWNER_ISSUED_GOVERNED_RECORD_BUNDLE",),
        responsible_owners=("Capability Governance", "Runtime Admission", "Provider Governance"),
        trace_refs=("trace:governed-record-production:owner-records-missing",),
        provenance_refs=inventory.source_refs,
    )


__all__ = [
    "CAPABILITY_REGISTRY_RELATIVE",
    "CAPABILITY_MODEL_BINDING_REGISTRY_RELATIVE",
    "MODEL_CONTRACT_REPOSITORY_RELATIVE",
    "MODEL_REGISTRY_RELATIVE",
    "MODEL_PROVIDER_BINDING_REGISTRY_RELATIVE",
    "OFFICIAL_CATALOG_RELATIVE",
    "PROVIDER_REGISTRY_RELATIVE",
    "RUNTIME_ADMISSION_INTEGRATION_RELATIVE",
    "RUNTIME_ADMISSION_PRODUCTION_MARKER",
    "RUNTIME_ADMISSION_PRODUCTION_RELATIVE",
    "inspect_repository_declarations_v1",
    "produce_governed_execution_records_v1",
]
