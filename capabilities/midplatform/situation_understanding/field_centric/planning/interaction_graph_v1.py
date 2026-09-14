# -*- coding: utf-8 -*-
"""Interaction Graph — 对象/人/环境如何作用 v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

INTERACTION_FIXTURES: Dict[str, List[Dict[str, Any]]] = {
    "metal_rack_furniture": [
        {"subject": "metal_rack", "object": "display_area", "interaction": "supports_display", "actor": "store"},
    ],
    "metal_rack_construction": [
        {"subject": "metal_rack", "object": "work_zone", "interaction": "structural_support", "actor": "workers"},
    ],
    "person_machine_greenery": [
        {"subject": "worker", "object": "pruning_machine", "interaction": "operates_on_vegetation", "target": "plants"},
    ],
    "person_machine_mall": [
        {"subject": "person", "object": "machine", "interaction": "operates_near", "target": "crowd"},
    ],
    "unknown_sculpture_touch": [
        {"subject": "visitor", "object": "unknown_sculpture", "interaction": "observes_and_touches", "target": "exhibit"},
    ],
    "unknown_object_no_interaction": [
    ],
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_interaction_graph(*, fixture_key: str) -> Dict[str, Any]:
    """Interaction Graph — 对象与对象/人/环境的作用关系."""
    interactions = INTERACTION_FIXTURES.get(fixture_key, [])
    nodes = set()
    edges: List[Dict[str, Any]] = []

    for ix in interactions:
        subj = ix.get("subject", "")
        obj = ix.get("object", "")
        nodes.add(subj)
        nodes.add(obj)
        edges.append({
            "edge_id": _uid("ix"),
            "subject_id": subj,
            "object_id": obj,
            "interaction_type": ix.get("interaction"),
            "target": ix.get("target"),
            "actor": ix.get("actor"),
            "candidate_only": True,
        })

    return {
        "graph_id": _uid("ixg"),
        "interaction_nodes": list(nodes),
        "interaction_edges": edges,
        "has_interaction": len(edges) > 0,
        "candidate_only": True,
    }
