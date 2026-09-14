from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_progress_state_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    position = dict(input_candidate.get("current_position_candidate") or {})
    progress = dict(input_candidate.get("route_progress_candidate") or {})
    progress_ratio = float(progress.get("progress_ratio", 0.0) or 0.0)
    return {
        "schema_version": "navigation_manager_progress_resolver_v1",
        "current_position_candidate": position,
        "route_progress_candidate": progress,
        "progress_ratio": max(0.0, min(1.0, progress_ratio)),
        "position_present": bool(position),
        "progress_present": bool(progress),
        **not_fact(),
    }
