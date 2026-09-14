# -*- coding: utf-8 -*-
"""Spatial Evidence Builder — layout / direction / position channel v1."""

from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

SPATIAL_FIXTURES: Dict[str, Dict[str, Any]] = {
    "metro_direction": {
        "spatial_hints": ["arrow pointing right", "exit direction candidate"],
        "layout_relation": "direction_to_platform",
        "confidence": 0.82,
    },
    "billboard_multi": {
        "spatial_hints": ["logo top-left", "price bottom-right", "qr bottom-center"],
        "layout_relation": "multi_object_grid",
        "confidence": 0.8,
    },
    "shopfront_default": {
        "spatial_hints": ["sign centered above entrance"],
        "layout_relation": "horizontal_sign",
        "confidence": 0.75,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_spatial_evidence(
    *,
    fixture_key: str = "shopfront_default",
    region_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """Build spatial channel evidence — position/layout/direction, not fact."""
    slots = region_analysis.get("information_slots") or []
    if not any(s in slots for s in ("layout", "layout_relation", "spatial")):
        return {
            "evidence_id": _uid("sev"),
            "type": "spatial_candidate",
            "spatial_hints": [],
            "status": "slot_not_required",
            "candidate_only": True,
            "not_fact": True,
        }

    fixture = SPATIAL_FIXTURES.get(fixture_key, SPATIAL_FIXTURES["shopfront_default"])
    return {
        "evidence_id": _uid("sev"),
        "type": "spatial_candidate",
        "spatial_hints": fixture.get("spatial_hints", []),
        "layout_relation": fixture.get("layout_relation"),
        "confidence": fixture.get("confidence", 0.0),
        "source": "spatial_analyzer_fixture",
        "not_location_fact": True,
        "candidate_only": True,
        "not_fact": True,
    }
