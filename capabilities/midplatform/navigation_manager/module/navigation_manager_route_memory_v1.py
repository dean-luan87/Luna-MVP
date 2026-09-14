from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_route_memory_v1(
    input_candidate: Mapping[str, Any], route_state: Mapping[str, Any]
) -> Dict[str, Any]:
    route_memory_ref = str(input_candidate.get("route_memory_ref") or "")
    memory_available = bool(route_memory_ref)
    effective_route_ref = str(route_state.get("route_ref") or route_memory_ref)
    return {
        "schema_version": "navigation_manager_route_memory_v1",
        "route_memory_ref": route_memory_ref,
        "route_memory_available": memory_available,
        "effective_route_ref": effective_route_ref,
        **not_fact(),
    }
