# -*- coding: utf-8 -*-
"""Field zone summary builder v1."""

from __future__ import annotations

from typing import Any, Dict, List

FIELD_ZONE_SUMMARY_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_zone_summary_registry_v1",
    "zones": ("inner_zone", "working_zone", "forecast_zone", "unknown"),
}


def build_field_zone_summary(
    entities: List[Dict[str, Any]],
) -> Dict[str, Any]:
    counts = {
        "inner_zone_entity_count": 0,
        "working_zone_entity_count": 0,
        "forecast_zone_entity_count": 0,
        "unknown_zone_entity_count": 0,
    }
    notes: List[str] = []
    warnings: List[str] = []

    for ent in entities:
        zone = ent.get("field_zone", "unknown")
        if zone == "inner_zone":
            counts["inner_zone_entity_count"] += 1
        elif zone == "working_zone":
            counts["working_zone_entity_count"] += 1
        elif zone == "forecast_zone":
            counts["forecast_zone_entity_count"] += 1
        else:
            counts["unknown_zone_entity_count"] += 1

    if counts["unknown_zone_entity_count"] > 0:
        notes.append("unknown_zone_entities_present")
        warnings.append("unknown_zone_entities_present")
    if counts["inner_zone_entity_count"] > 0:
        notes.append("inner_zone_active")

    return {
        **counts,
        "zone_quality_notes": notes,
        "high_priority_zone_warnings": warnings,
        "total_entity_count": len(entities),
    }
