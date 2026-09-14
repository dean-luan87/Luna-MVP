# -*- coding: utf-8 -*-
"""Context Evidence Builder — scene relationship channel v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

CONTEXT_FIXTURES: Dict[str, Dict[str, Any]] = {
    "commercial_shopfront": {
        "scene_relations": ["commercial storefront environment", "street-facing signage"],
        "confidence": 0.78,
    },
    "subway_platform": {
        "scene_relations": ["transit platform environment", "passenger guidance context"],
        "confidence": 0.85,
    },
    "retail_billboard": {
        "scene_relations": ["retail advertisement context", "product promotion environment"],
        "confidence": 0.8,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_context_evidence(
    *,
    situation: Optional[Dict[str, Any]] = None,
    fixture_key: str = "commercial_shopfront",
    region_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """Build context channel evidence — scene relationship, not answer."""
    slots = region_analysis.get("information_slots") or []
    if not any(s in slots for s in ("context", "scene_relation")):
        scene = ((situation or {}).get("scene_profile_candidate") or {}).get("scene_type")
        if scene:
            return {
                "evidence_id": _uid("cev"),
                "type": "context_candidate",
                "scene_relations": [f"scene_type={scene}"],
                "confidence": 0.6,
                "source": "situation_hint",
                "candidate_only": True,
                "not_fact": True,
            }
        return {
            "evidence_id": _uid("cev"),
            "type": "context_candidate",
            "scene_relations": [],
            "status": "slot_not_required",
            "candidate_only": True,
            "not_fact": True,
        }

    fixture = CONTEXT_FIXTURES.get(fixture_key, CONTEXT_FIXTURES["commercial_shopfront"])
    return {
        "evidence_id": _uid("cev"),
        "type": "context_candidate",
        "scene_relations": fixture.get("scene_relations", []),
        "confidence": fixture.get("confidence", 0.0),
        "source": "context_analyzer_fixture",
        "not_semantic_answer": True,
        "candidate_only": True,
        "not_fact": True,
    }
