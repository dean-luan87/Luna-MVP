from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    list_capability_providers,
    load_model_registry,
)
from capabilities.midplatform.model_manager.engines.model_provider_routing_lifecycle_closure_v1 import (
    filter_model_provider_routing_lifecycle_eligible,
)


def build_identity_registry_view_v1(
    *,
    requested_capability: str,
    forbidden_model_ids: Iterable[str],
) -> Dict[str, Any]:
    forbidden = {str(x) for x in forbidden_model_ids}
    model_registry = load_model_registry()
    by_id = {
        str(m.get("model_id", "")): dict(m)
        for m in model_registry.get("models", [])
        if isinstance(m, dict)
    }

    providers = list_capability_providers(requested_capability)
    providers = [p for p in providers if str(p.get("model_id", "")) not in forbidden]
    eligible = filter_model_provider_routing_lifecycle_eligible(providers)

    return {
        "requested_capability": requested_capability,
        "provider_records": tuple(providers),
        "eligible_provider_records": tuple(eligible),
        "model_registry_by_id": by_id,
        "registry_found": len(providers) > 0,
    }
