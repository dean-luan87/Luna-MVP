# -*- coding: utf-8 -*-
"""Document Surface — relation hint constraint runtime v1."""

from __future__ import annotations

from typing import Any, Dict, List


def apply_relation_hint_constraints(*, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
    relations: List[Dict[str, Any]] = list(pipeline_result.get("relation_hint_candidates") or [])
    surfaces = pipeline_result.get("document_surface_candidates") or []
    valid: List[Dict[str, Any]] = []
    rejected = 0
    fake_blocked = 0

    for rel in relations:
        if not rel.get("evidence_basis"):
            rejected += 1
            continue
        if rel.get("relation_type_candidate") in ("overlaps", "occludes", "attached_to"):
            if len(surfaces) < 1:
                rejected += 1
                continue
            if rel.get("entity_a") and rel.get("entity_b") is None and rel.get("relation_type_candidate") != "uncertain_relation":
                if rel.get("relation_type_candidate") != "uncertain_relation":
                    pass
        if rel.get("fake_relation"):
            fake_blocked += 1
            continue
        valid.append({**rel, "candidate_only": True, "not_fact": True})

    compliance = len(valid) / max(1, len(relations)) if relations else 1.0
    return {
        **pipeline_result,
        "relation_hint_candidates": valid,
        "relation_constraint": {
            "input_count": len(relations),
            "valid_count": len(valid),
            "rejected_count": rejected,
            "fake_relation_blocked": fake_blocked,
            "relation_hint_evidence_compliance_rate": round(compliance, 4),
            "fake_relation_rate": 0.0 if fake_blocked == 0 else round(fake_blocked / max(1, len(relations)), 4),
            "candidate_only": True,
            "not_fact": True,
        },
    }
