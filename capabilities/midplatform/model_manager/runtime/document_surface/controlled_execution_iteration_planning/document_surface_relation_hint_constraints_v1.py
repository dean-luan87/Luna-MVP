# -*- coding: utf-8 -*-
"""Document Surface — relation hint constraints v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List

ALLOWED_RELATION_TYPES = (
    "occludes",
    "overlaps",
    "attached_to",
    "possible_screen_content",
    "uncertain_relation",
)

FORBIDDEN = (
    "relation_hint_without_surface_candidates",
    "relation_hint_without_geometric_evidence",
    "fake_relation_to_pass_smoke",
)


def build_relation_hint_constraints_plan() -> Dict[str, Any]:
    constraints: List[Dict[str, Any]] = []
    for rel in ALLOWED_RELATION_TYPES:
        constraints.append({
            "relation_type_candidate": rel,
            "evidence_basis_required": True,
            "geometric_evidence_required": True,
            "minimum_surface_pair_count": 1 if rel == "possible_screen_content" else 2,
        })
    return {
        "plan_id": "document_surface_relation_hint_constraints_v1",
        "allowed_relation_types": list(ALLOWED_RELATION_TYPES),
        "constraints": constraints,
        "forbidden": list(FORBIDDEN),
        "fake_relation_rate_target": 0.0,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }
