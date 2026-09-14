from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_route_state_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    route_candidate = dict(input_candidate.get("route_candidate") or {})
    route_present = bool(route_candidate)
    route_ref = str(route_candidate.get("route_ref") or "")
    if not route_ref and route_present:
        route_ref = f"route_{input_candidate.get('navigation_request_id') or 'unknown'}"
    return {
        "schema_version": "navigation_manager_route_adapter_v1",
        "route_candidate": route_candidate,
        "route_present": route_present,
        "route_ref": route_ref,
        "route_status_hint": str(
            route_candidate.get("route_status") or "candidate_ready"
        ),
        **not_fact(),
    }
