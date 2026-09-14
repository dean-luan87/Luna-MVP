from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_arrival_candidate_v1(
    input_candidate: Mapping[str, Any], progress_state: Mapping[str, Any]
) -> Dict[str, Any]:
    progress_ratio = float(progress_state.get("progress_ratio", 0.0) or 0.0)
    destination = dict(input_candidate.get("destination_candidate") or {})
    arrived = bool(destination.get("arrived", False)) or progress_ratio >= 0.98
    return {
        "schema_version": "navigation_manager_arrival_resolver_v1",
        "arrival_candidate": {
            "candidate_id": f"arrival_{input_candidate.get('navigation_request_id')}",
            "arrived": arrived,
            "progress_ratio": round(progress_ratio, 3),
            "destination_ref": str(destination.get("destination_ref") or ""),
            "candidate_only": True,
            **not_fact(),
        },
        **not_fact(),
    }
