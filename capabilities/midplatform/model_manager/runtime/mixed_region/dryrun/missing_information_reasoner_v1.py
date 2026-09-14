# -*- coding: utf-8 -*-
"""Missing Information Reasoner — why missing, not just text_missing v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def reason_missing_information(
    *,
    discovery: Dict[str, Any],
    ownership_graph: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Produce missing_information_candidate with reason.
    occluded ≠ ocr_failed ≠ no_text ≠ poor_quality
    """
    results: List[Dict[str, Any]] = []
    for item in discovery.get("missing_information") or []:
        results.append({
            "missing_id": _uid("mis"),
            "type": "missing_information_candidate",
            "info_type": item.get("type", "text"),
            "owner": item.get("owner"),
            "field": item.get("field"),
            "reason": item.get("reason"),
            "confidence_source": item.get("confidence_source", "spatial_relation"),
            "not_assume_absent": item.get("reason") == "occluded",
            "candidate_only": True,
            "not_fact": True,
        })

    for ent in ownership_graph.get("entity_candidates") or []:
        comp = ent.get("completeness") or {}
        if comp.get("missing_reason"):
            results.append({
                "missing_id": _uid("mis"),
                "type": "missing_information_candidate",
                "info_type": "text",
                "owner": ent.get("entity_id"),
                "field": "title",
                "reason": comp.get("missing_reason"),
                "confidence_source": "spatial_relation",
                "information_completeness": comp.get("information_completeness"),
                "not_assume_absent": True,
                "candidate_only": True,
            })

    return results
