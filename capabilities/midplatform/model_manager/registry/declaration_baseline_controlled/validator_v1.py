"""Static validation for the first Capability/Model/Provider declaration set."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CAPABILITY_REGISTRY = "capabilities/midplatform/model_manager/registries/capability_registry_v1.json"
MODEL_REGISTRY = "capabilities/midplatform/model_manager/registries/model_registry_v1.json"
PROVIDER_REGISTRY = "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"
CAPABILITY_MODEL_BINDING_REGISTRY = "capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json"
MODEL_PROVIDER_BINDING_REGISTRY = "capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json"
RUNTIME_ADMISSION_SOURCE = "capabilities/midplatform/core/cognitive_flow/integration/logical_capability_to_runtime_admission_candidate_adapter_controlled"

TARGET_CAPABILITY = "object_detection"
TARGET_CAPABILITY_CONTRACT = "capability:object-detection:v1"
TARGET_SLOT = "slot:object-detection:vision:v1"
TARGET_MODEL_ID = "yolo11n"
TARGET_MODEL_ASSET = "model-asset:yolo11n:weights-v1"
TARGET_PROVIDER_ID = "provider:yolo:local:v1"
TARGET_PROVIDER_FAMILY = "yolo"


def _load(root: Path, relative: str) -> Mapping[str, Any]:
    path = root / relative
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, Mapping) else {}


def _items(registry: Mapping[str, Any], key: str) -> Tuple[Mapping[str, Any], ...]:
    return tuple(item for item in registry.get(key, ()) if isinstance(item, Mapping))


def _unique(values: Tuple[str, ...]) -> bool:
    return len(values) == len(set(values))


def validate_declaration_baseline_v1(root: Path) -> Dict[str, Any]:
    capability_registry = _load(root, CAPABILITY_REGISTRY)
    model_registry = _load(root, MODEL_REGISTRY)
    provider_registry = _load(root, PROVIDER_REGISTRY)
    capability_model_registry = _load(root, CAPABILITY_MODEL_BINDING_REGISTRY)
    model_provider_registry = _load(root, MODEL_PROVIDER_BINDING_REGISTRY)

    capabilities = _items(capability_registry, "capabilities")
    slots = _items(capability_registry, "slots")
    models = _items(model_registry, "models")
    providers = _items(provider_registry, "providers")
    capability_bindings = _items(capability_model_registry, "bindings")
    provider_bindings = _items(model_provider_registry, "bindings")
    runtime_source = root / RUNTIME_ADMISSION_SOURCE
    runtime_admission_production_source_found = bool(
        runtime_source.is_dir()
        and "controlled" not in str(runtime_source).lower()
        and any(runtime_source.glob("*.py"))
    )

    capability = next((item for item in capabilities if item.get("capability_id") == TARGET_CAPABILITY), None)
    slot = next((item for item in slots if item.get("slot_id") == TARGET_SLOT), None)
    model = next((item for item in models if item.get("model_asset_id") == TARGET_MODEL_ASSET), None)
    provider = next((item for item in providers if item.get("provider_id") == TARGET_PROVIDER_ID), None)
    capability_binding = next((item for item in capability_bindings if item.get("model_asset_ref") == TARGET_MODEL_ASSET), None)
    provider_binding = next((item for item in provider_bindings if item.get("model_asset_ref") == TARGET_MODEL_ASSET), None)

    checks = {
        "capability_exists": capability is not None,
        "slot_exists": slot is not None,
        "slot_not_model_bound": bool(slot and slot.get("model_binding_owned_elsewhere") is True and "model_asset_ref" not in slot),
        "model_exists": model is not None,
        "model_owner": bool(model and model.get("owner") == "Model Governance"),
        "provider_exists": provider is not None,
        "provider_owner": bool(provider and provider.get("owner") == "Provider Governance"),
        "capability_model_binding_exists": capability_binding is not None,
        "capability_model_binding_owner": bool(capability_binding and capability_binding.get("lifecycle_owner") == "Capability Governance"),
        "model_provider_binding_exists": provider_binding is not None,
        "model_provider_binding_owner": bool(provider_binding and provider_binding.get("lifecycle_owner") == "Provider Governance"),
        "no_dual_binding_mutation_authority": bool(
            capability_binding
            and provider_binding
            and capability_binding.get("lifecycle_owner") == "Capability Governance"
            and provider_binding.get("lifecycle_owner") == "Provider Governance"
            and capability_binding.get("lifecycle_owner") != provider_binding.get("lifecycle_owner")
            and model
            and model.get("owner") == "Model Governance"
            and provider
            and provider.get("owner") == "Provider Governance"
        ),
        "capability_model_refs_align": bool(
            capability_binding
            and capability_binding.get("capability_ref") == TARGET_CAPABILITY
            and capability_binding.get("capability_slot_ref") == TARGET_SLOT
            and capability_binding.get("model_asset_ref") == TARGET_MODEL_ASSET
        ),
        "model_provider_refs_align": bool(
            provider_binding
            and provider_binding.get("model_asset_ref") == TARGET_MODEL_ASSET
            and provider_binding.get("provider_ref") == TARGET_PROVIDER_ID
            and provider_binding.get("provider_family_ref") == TARGET_PROVIDER_FAMILY
            and provider
            and provider_binding.get("provider_ref") == provider.get("provider_id")
            and provider_binding.get("provider_contract_ref") == provider.get("provider_contract_ref")
        ),
        "model_versions_present": bool(model and model.get("model_version") and model.get("weights_version")),
        "model_capability_declaration_aligned": bool(
            model
            and capability_binding
            and capability_binding.get("model_capability_declaration_ref") in tuple(model.get("capability_declaration_refs") or ())
        ),
        "provider_contract_declaration_complete": bool(
            provider
            and provider.get("provider_contract_ref")
            and provider.get("provider_contract_version")
            and isinstance(provider.get("provider_contract"), Mapping)
            and provider.get("provider_contract", {}).get("contract_ref") == provider.get("provider_contract_ref")
            and provider.get("provider_contract", {}).get("adapter_ref") == provider.get("provider_adapter_ref")
            and provider.get("provider_contract", {}).get("provenance_refs")
        ),
        "lifecycle_values_valid": bool(
            slot
            and slot.get("lifecycle_state") in {"EMPTY", "BOUND", "UNBOUND", "SUSPENDED", "DEGRADED", "RECOVERABLE"}
            and model
            and model.get("lifecycle_state") in {"discovered", "candidate", "evaluating", "admitted", "active", "deprecated", "blocked"}
            and provider
            and provider.get("lifecycle_state") in {"discovered", "candidate", "evaluating", "admitted", "active", "deprecated", "blocked"}
            and capability_binding
            and capability_binding.get("lifecycle_state") in {"candidate", "admitted", "active", "deprecated", "blocked"}
            and provider_binding
            and provider_binding.get("lifecycle_state") in {"candidate", "admitted", "active", "deprecated", "blocked"}
        ),
        "binding_versions_present": bool(
            capability_binding
            and capability_binding.get("binding_version")
            and provider_binding
            and provider_binding.get("binding_version")
        ),
        "provenance_present": bool(
            model
            and model.get("provenance_refs")
            and capability_binding
            and capability_binding.get("provenance_refs")
            and provider
            and provider.get("provenance_refs")
            and provider_binding
            and provider_binding.get("provenance_refs")
        ),
        "duplicate_model_identity_absent": _unique(tuple(str(item.get("model_asset_id")) for item in models if item.get("model_asset_id"))),
        "duplicate_provider_identity_absent": _unique(tuple(str(item.get("provider_id")) for item in providers if item.get("provider_id"))),
        "no_runtime_admission": not any("runtime_admission" in str(item).lower() for item in (model or {}, provider or {})),
        "no_execution_flags": not any(
            bool(item.get(flag))
            for item in (model or {}, provider or {}, capability_binding or {}, provider_binding or {})
            for flag in ("model_loading_executed", "provider_invocation_executed", "runtime_execution", "observation_execution", "action_execution")
        ),
    }
    return {
        "phase": "Phase-P1-Midplatform-Capability-Model-Provider-Governance-Declaration-Baseline-v1-001",
        "checks": checks,
        "all_declaration_checks_passed": all(checks.values()),
        "remaining_runtime_admission_source": not runtime_admission_production_source_found,
        "runtime_admission_production_source_found": runtime_admission_production_source_found,
        "runtime_admission_created": False,
        "executable_candidate_created": False,
        "model_loading": False,
        "provider_invocation": False,
        "observation_execution": False,
        "action_execution": False,
        "source_mutation": False,
        "world_truth_declared": False,
        "source_refs": [
            CAPABILITY_REGISTRY,
            MODEL_REGISTRY,
            PROVIDER_REGISTRY,
            CAPABILITY_MODEL_BINDING_REGISTRY,
            MODEL_PROVIDER_BINDING_REGISTRY,
        ],
    }


__all__ = ["validate_declaration_baseline_v1"]
