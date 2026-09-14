# -*- coding: utf-8 -*-
"""Semantic Conflict Detector — same-region channel conflict v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def detect_semantic_conflict(
    *,
    discovery: Dict[str, Any],
    ownership_graph: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """Text STARBUCKS + visual auto repair on same entity → semantic_conflict_candidate."""
    if not discovery.get("semantic_conflict"):
        return None

    for ent in ownership_graph.get("entity_candidates") or []:
        channels = ent.get("information_channels") or {}
        text_cands = (channels.get("text") or {}).get("candidates") or []
        visual = channels.get("visual") or {}
        text = (text_cands[0].get("text") if text_cands else "") or ""
        scene = visual.get("scene_hint", "")

        if "STARBUCKS" in text.upper() and scene == "auto_repair":
            return {
                "conflict_id": _uid("scc"),
                "type": "semantic_conflict_candidate",
                "entity_id": ent.get("entity_id"),
                "text_evidence": text,
                "visual_evidence": visual.get("features"),
                "ownership": "same_region",
                "not_visual_plus_text_answer": True,
                "next_action": "need_additional_evidence",
                "validation_status": "validation_review",
                "candidate_only": True,
                "not_fact": True,
            }

    if discovery.get("semantic_conflict"):
        return {
            "conflict_id": _uid("scc"),
            "type": "semantic_conflict_candidate",
            "not_visual_plus_text_answer": True,
            "next_action": "need_additional_evidence",
            "candidate_only": True,
        }
    return None
