# -*- coding: utf-8 -*-
"""Document Surface → Ownership adapter v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def adapt_surfaces_to_ownership_entities(
    *,
    document_surface_candidates: List[Dict[str, Any]],
    relation_hint_candidates: List[Dict[str, Any]],
    source_region_id: str,
) -> Dict[str, Any]:
    """Map document_surface_candidates → ownership entity_candidates."""
    entities: List[Dict[str, Any]] = []
    for s in document_surface_candidates:
        entities.append({
            "entity_id": s.get("owner_entity_candidate_ref") or s.get("surface_id"),
            "entity_type_candidate": "document_surface",
            "surface_id": s.get("surface_id"),
            "attention_gate": "allowed",
            "ownership_candidate": {"owner_type": "document_surface", "surface_id": s.get("surface_id")},
            "source_runtime": RUNTIME_ID,
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "ownership_package_id": _uid("own"),
        "source_region_id": source_region_id,
        "entity_candidates": entities,
        "relation_candidates": [
            {
                "relation_id": r.get("relation_id", _uid("rel")),
                "entity_a": r.get("entity_a"),
                "entity_b": r.get("entity_b"),
                "relation_type": r.get("relation_type_candidate"),
                "evidence_basis": r.get("evidence_basis"),
                "occlusion_not_absence": r.get("relation_type_candidate") == "occludes",
                "candidate_only": True,
            }
            for r in relation_hint_candidates
        ],
        "runtime_does_not_override_ownership_graph": True,
        "candidate_only": True,
    }
