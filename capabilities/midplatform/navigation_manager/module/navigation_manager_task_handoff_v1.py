from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_task_handoff_candidate_v1(
    input_candidate: Mapping[str, Any],
    route_state: Mapping[str, Any],
    progress_state: Mapping[str, Any],
    arrival_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    arrival = arrival_candidate.get("arrival_candidate") or {}
    return {
        "schema_version": "navigation_manager_task_handoff_v1",
        "task_handoff_candidate": {
            "candidate_id": f"task_handoff_{input_candidate.get('navigation_request_id')}",
            "task_id": input_candidate.get("task_id"),
            "route_ref": route_state.get("route_ref"),
            "progress_ratio": progress_state.get("progress_ratio"),
            "arrival_candidate": bool(arrival.get("arrived", False)),
            "candidate_only": True,
            **not_fact(),
        },
        **not_fact(),
    }
