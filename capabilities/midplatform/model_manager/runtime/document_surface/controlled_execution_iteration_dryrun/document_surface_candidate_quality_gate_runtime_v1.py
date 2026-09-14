# -*- coding: utf-8 -*-
"""Document Surface — candidate quality gate runtime v1."""

from __future__ import annotations

from typing import Any, Dict, List

CAP = 5
MIN_CONF_KEEP = 0.35


def apply_candidate_quality_gate(
    *,
    execution_result: Dict[str, Any],
    category: str,
) -> Dict[str, Any]:
    surfaces: List[Dict[str, Any]] = list(execution_result.get("document_surface_candidates") or [])
    gated: List[Dict[str, Any]] = []
    rejected = 0
    low_conf = 0
    for s in surfaces:
        conf = s.get("boundary_confidence_candidate") or 0.0
        if conf < MIN_CONF_KEEP and category.startswith("low_contrast"):
            s = {**s, "low_confidence_boundary_candidate": True, "gate_action": "mark_low_confidence"}
            low_conf += 1
        elif conf < MIN_CONF_KEEP:
            rejected += 1
            continue
        else:
            s = {**s, "gate_action": "keep_candidate"}
        gated.append({**s, "candidate_only": True, "not_fact": True})

    if len(gated) > CAP:
        gated = gated[:CAP]
        capped = True
    else:
        capped = False

    pass_rate = len(gated) / max(1, len(surfaces)) if surfaces else 1.0
    return {
        **execution_result,
        "document_surface_candidates": gated,
        "quality_gate": {
            "input_count": len(surfaces),
            "output_count": len(gated),
            "rejected_count": rejected,
            "low_confidence_count": low_conf,
            "capped": capped,
            "candidate_quality_gate_pass_rate": round(pass_rate, 4),
            "candidate_only": True,
            "not_fact": True,
        },
    }
