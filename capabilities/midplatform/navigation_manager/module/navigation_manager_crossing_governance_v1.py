from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_crossing_assessment_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    crossings = tuple(input_candidate.get("crossing_candidates") or ())
    traffic = tuple(input_candidate.get("traffic_light_candidates") or ())
    requires_attention = bool(crossings) or bool(traffic)
    waiting_required = any(str(item).lower().find("red") >= 0 for item in traffic)
    return {
        "schema_version": "navigation_manager_crossing_governance_v1",
        "crossing_assessment": {
            "crossing_candidates": crossings,
            "traffic_light_candidates": traffic,
            "attention_required": requires_attention,
            "waiting_required": waiting_required,
        },
        **not_fact(),
    }
