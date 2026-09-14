"""Static validation for the repository-backed RF-DETR/Roboflow declaration set.

This helper reads existing owner-controlled registries only.  It does not
construct Runtime Admission, select a Provider, load a model, or invoke an
external service.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


CAPABILITY_REGISTRY = Path("capabilities/midplatform/model_manager/registries/capability_registry_v1.json")
MODEL_REGISTRY = Path("capabilities/midplatform/model_manager/registries/model_registry_v1.json")
PROVIDER_REGISTRY = Path("capabilities/midplatform/model_manager/registry/provider_registry_v1.json")
CAPABILITY_MODEL_BINDING_REGISTRY = Path("capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json")
MODEL_PROVIDER_BINDING_REGISTRY = Path("capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json")
MODEL_CONTRACT_REPOSITORY = Path("capabilities/midplatform/model_manager/model_contract_repository/model_contract_repository_registry_v1.py")

CAPABILITY_ID = "object_detection"
CAPABILITY_CONTRACT_REF = "capability:object-detection:v1"
SLOT_REF = "slot:object-detection:vision:v1"
MODEL_ASSET_REF = "model-asset:rf-detr-small:roboflow-v1"
MODEL_VERSION_REF = "workflow-declared-v1"
WEIGHTS_VERSION_REF = "provider-managed-declared-v1"
PROVIDER_REF = "provider:roboflow:vision:poc:v1"
PROVIDER_FAMILY = "roboflow"
WORKFLOW_REF = "workflow:roboflow:lei-luan:custom-workflow:v1"
WORKSPACE_REF = "workspace:roboflow:lei-luan:v1"
WORKFLOW_ID = "custom-workflow"
ADAPTER_REF = "adapter:roboflow:vision-evidence:v1"
LOADER_REF = "loader:roboflow:workflow-api:v1"
MODEL_PROVIDER_BINDING_REF = "model-provider-binding:rf-detr-small:roboflow:custom-workflow:v1"
CAPABILITY_MODEL_BINDING_REF = "capability-model-binding:object-detection:rf-detr-small:v1"
DETECTION_OUTPUT_PATH = "$[0].model_output_3.predictions"


def _load(root: Path, relative: Path) -> Mapping[str, Any]:
    path = root / relative
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, Mapping) else {}


def _items(registry: Mapping[str, Any], key: str) -> tuple[Mapping[str, Any], ...]:
    return tuple(item for item in registry.get(key, ()) if isinstance(item, Mapping))


def _has_secret_key(value: Any) -> bool:
    if isinstance(value, Mapping):
        return any(
            str(key).lower() in {"api_key", "api_secret", "access_token", "secret"}
            or _has_secret_key(item)
            for key, item in value.items()
        )
    if isinstance(value, (tuple, list)):
        return any(_has_secret_key(item) for item in value)
    return False


def inspect_rf_detr_declarations_v1(root: Path) -> dict[str, Any]:
    capability_registry = _load(root, CAPABILITY_REGISTRY)
    model_registry = _load(root, MODEL_REGISTRY)
    provider_registry = _load(root, PROVIDER_REGISTRY)
    capability_model_registry = _load(root, CAPABILITY_MODEL_BINDING_REGISTRY)
    model_provider_registry = _load(root, MODEL_PROVIDER_BINDING_REGISTRY)

    capability = next((item for item in _items(capability_registry, "capabilities") if item.get("capability_id") == CAPABILITY_ID), None)
    slot = next((item for item in _items(capability_registry, "slots") if item.get("slot_id") == SLOT_REF), None)
    model = next((item for item in _items(model_registry, "models") if item.get("model_asset_id") == MODEL_ASSET_REF), None)
    provider = next((item for item in _items(provider_registry, "providers") if item.get("provider_id") == PROVIDER_REF), None)
    capability_binding = next((item for item in _items(capability_model_registry, "bindings") if item.get("binding_id") == CAPABILITY_MODEL_BINDING_REF), None)
    provider_binding = next((item for item in _items(model_provider_registry, "bindings") if item.get("binding_id") == MODEL_PROVIDER_BINDING_REF), None)

    checks = {
        "capability_exists": capability is not None,
        "slot_exists": bool(slot and slot.get("capability_ref") == CAPABILITY_ID and slot.get("capability_contract_ref") == CAPABILITY_CONTRACT_REF),
        "model_declaration_exists": bool(model and model.get("owner") == "Model Governance" and model.get("model_id") == "rf-detr-small"),
        "model_versions_present": bool(model and model.get("model_version") == MODEL_VERSION_REF and model.get("weights_version") == WEIGHTS_VERSION_REF),
        "model_capability_declared": bool(
            model
            and CAPABILITY_CONTRACT_REF in tuple(model.get("capability_contract_refs") or ())
            and "object_detection" in tuple(model.get("capabilities") or ())
        ),
        "capability_model_binding_exists": bool(
            capability_binding
            and capability_binding.get("lifecycle_owner") == "Capability Governance"
            and capability_binding.get("capability_ref") == CAPABILITY_ID
            and capability_binding.get("capability_slot_ref") == SLOT_REF
            and capability_binding.get("model_asset_ref") == MODEL_ASSET_REF
        ),
        "provider_declaration_exists": bool(
            provider
            and provider.get("owner") == "Provider Governance"
            and provider.get("provider_family") == PROVIDER_FAMILY
            and provider.get("provider_id") == PROVIDER_REF
        ),
        "workflow_binding_exists": bool(
            provider
            and provider.get("workflow_ref") == WORKFLOW_REF
            and provider.get("workspace_ref") == WORKSPACE_REF
            and provider.get("workflow_id") == WORKFLOW_ID
            and provider.get("workflow_binding_lifecycle_owner") == "Provider Governance"
        ),
        "transport_is_inference_sdk": bool(
            provider
            and provider.get("transport_ref") == "transport:inference_sdk:InferenceHTTPClient:v1"
            and "dependency:inference-sdk" in tuple(provider.get("dependency_declaration_refs") or ())
        ),
        "workflow_io_mapping_declared": bool(
            provider
            and any("image" in str(ref) for ref in tuple(provider.get("workflow_input_contract_refs") or ()))
            and provider.get("workflow_output_mapping", {}).get("detections") == DETECTION_OUTPUT_PATH
        ),
        "model_provider_binding_exists": bool(
            provider_binding
            and provider_binding.get("lifecycle_owner") == "Provider Governance"
            and provider_binding.get("model_asset_ref") == MODEL_ASSET_REF
            and provider_binding.get("provider_ref") == PROVIDER_REF
            and provider_binding.get("workflow_binding_ref") == WORKFLOW_REF
            and provider_binding.get("provider_adapter_ref") == ADAPTER_REF
            and provider_binding.get("loader_contract_ref") == LOADER_REF
        ),
        "binding_versions_present": bool(
            capability_binding
            and capability_binding.get("binding_version")
            and provider_binding
            and provider_binding.get("binding_version")
        ),
        "provenance_present": bool(
            model and model.get("provenance_refs")
            and provider and provider.get("provenance_refs")
            and capability_binding and capability_binding.get("provenance_refs")
            and provider_binding and provider_binding.get("provenance_refs")
        ),
        "credential_not_embedded": not any(_has_secret_key(item) for item in (provider or {}, provider_binding or {}, model or {})),
        "candidate_only_and_no_execution": all(
            item is not None
            and item.get("candidate_only") is True
            and not any(bool(item.get(flag)) for flag in ("runtime_execution", "model_loading_implied", "provider_invocation_implied", "provider_invocation_executed"))
            for item in (model, provider, capability_binding, provider_binding)
        ),
        "model_contract_repository_contains_external_contracts": bool(
            (root / MODEL_CONTRACT_REPOSITORY).is_file()
            and LOADER_REF in (root / MODEL_CONTRACT_REPOSITORY).read_text(encoding="utf-8")
            and ADAPTER_REF in (root / MODEL_CONTRACT_REPOSITORY).read_text(encoding="utf-8")
            and MODEL_ASSET_REF in (root / MODEL_CONTRACT_REPOSITORY).read_text(encoding="utf-8")
        ),
    }
    return {
        "target_model_asset_ref": MODEL_ASSET_REF,
        "target_provider_ref": PROVIDER_REF,
        "target_workflow_ref": WORKFLOW_REF,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "source_refs": [str(path) for path in (CAPABILITY_REGISTRY, MODEL_REGISTRY, PROVIDER_REGISTRY, CAPABILITY_MODEL_BINDING_REGISTRY, MODEL_PROVIDER_BINDING_REGISTRY, MODEL_CONTRACT_REPOSITORY)],
        "runtime_execution": False,
        "model_loading": False,
        "provider_invocation": False,
    }


__all__ = [
    "ADAPTER_REF",
    "CAPABILITY_MODEL_BINDING_REF",
    "CAPABILITY_MODEL_BINDING_REGISTRY",
    "CAPABILITY_REGISTRY",
    "DETECTION_OUTPUT_PATH",
    "MODEL_ASSET_REF",
    "MODEL_CONTRACT_REPOSITORY",
    "MODEL_PROVIDER_BINDING_REF",
    "MODEL_PROVIDER_BINDING_REGISTRY",
    "MODEL_REGISTRY",
    "PROVIDER_REF",
    "PROVIDER_REGISTRY",
    "WORKFLOW_REF",
    "inspect_rf_detr_declarations_v1",
]
