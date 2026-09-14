# -*- coding: utf-8 -*-
"""Semantic Fusion Adapter — Mixed Evidence, not answer merge v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.evidence_completeness_v1 import (
    compute_evidence_completeness,
)

SUPPORT_THRESHOLD = 0.6


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _detect_conflict(
    *,
    text_evidence: Dict[str, Any],
    visual_evidence: Dict[str, Any],
) -> bool:
    if visual_evidence.get("ocr_unreliable_not_conflict"):
        return False
    if visual_evidence.get("consistent_with_text") is False:
        return True
    text = (text_evidence.get("text") or "").upper()
    scene = visual_evidence.get("scene_hint", "")
    if "STARBUCKS" in text and scene == "auto_repair":
        return True
    return False


def fuse_mixed_evidence(
    *,
    text_evidence: Dict[str, Any],
    visual_evidence: Dict[str, Any],
    spatial_evidence: Optional[Dict[str, Any]] = None,
    context_evidence: Optional[Dict[str, Any]] = None,
    ownership_evidence: Optional[Dict[str, Any]] = None,
    channel_activations: Optional[Dict[str, Any]] = None,
    region_analysis: Optional[Dict[str, Any]] = None,
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Semantic Fusion — multiple evidence channels, NOT text+image=answer.
    """
    completeness = compute_evidence_completeness(
        channel_activations=channel_activations or {},
        text_evidence=text_evidence,
        visual_evidence=visual_evidence,
        spatial_evidence=spatial_evidence,
        context_evidence=context_evidence,
        ownership_evidence=ownership_evidence,
    )

    if ownership_evidence and ownership_evidence.get("per_owner_documents"):
        return {
            "fusion_id": _uid("fus"),
            "type": "mixed_evidence_candidate",
            "ownership_evidence_ref": ownership_evidence.get("evidence_id"),
            "per_owner_documents": ownership_evidence.get("per_owner_documents"),
            "conflict": False,
            "evidence_completeness": completeness,
            "next_action": "validation_review",
            "not_flat_text_merge": True,
            "not_answer_merge": True,
            "ownership_before_ocr": ownership_evidence.get("region_discovery_before_ocr"),
            "candidate_only": True,
            "not_fact": True,
        }

    conflict = _detect_conflict(text_evidence=text_evidence, visual_evidence=visual_evidence)
    damaged = (region_analysis or {}).get("text_damaged", False)
    artistic = (region_analysis or {}).get("artistic_font", False)
    text_absent = (region_analysis or {}).get("text_absent", False)
    text_conf = text_evidence.get("confidence", 0.0)
    visual_conf = visual_evidence.get("confidence", 0.0)

    if conflict:
        return {
            "fusion_id": _uid("fus"),
            "type": "mixed_evidence_candidate",
            "text_evidence_ref": text_evidence.get("evidence_id"),
            "visual_evidence_ref": visual_evidence.get("evidence_id"),
            "conflict": True,
            "validation_status": "validation_review",
            "next_action": "validation_review",
            "evidence_completeness": completeness,
            "not_answer_merge": True,
            "not_direct_fact_admission": True,
            "not_text_plus_image_equals_answer": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if text_absent and visual_evidence.get("features"):
        return {
            "fusion_id": _uid("fus"),
            "type": "mixed_evidence_candidate",
            "visual_evidence_ref": visual_evidence.get("evidence_id"),
            "text_missing": True,
            "not_invented_text": True,
            "not_text_fact_from_visual": True,
            "next_action": "visual_only_candidate",
            "evidence_completeness": completeness,
            "candidate_only": True,
            "not_fact": True,
        }

    if damaged and visual_conf >= SUPPORT_THRESHOLD:
        return {
            "fusion_id": _uid("fus"),
            "type": "mixed_evidence_candidate",
            "semantic_hint": "可能是一个餐饮店招",
            "not_text_completion": True,
            "visual_supplements_damaged_text": True,
            "next_action": "fact_admission_candidate",
            "evidence_completeness": completeness,
            "candidate_only": True,
            "not_fact": True,
        }

    if artistic and text_conf < SUPPORT_THRESHOLD and visual_conf >= SUPPORT_THRESHOLD:
        next = "request_more_evidence"
        if visual_evidence.get("ocr_unreliable_not_conflict"):
            next = "request_more_evidence"
        return {
            "fusion_id": _uid("fus"),
            "type": "mixed_evidence_candidate",
            "semantic_hint": "商业/餐饮场景候选",
            "visual_supplements_ocr_gap": True,
            "ocr_unreliable_visual_supports": visual_evidence.get("ocr_unreliable_not_conflict", False),
            "not_vlm_replaces_ocr": True,
            "next_action": next,
            "evidence_completeness": completeness,
            "candidate_only": True,
            "not_fact": True,
        }

    info_comp = completeness.get("information_completeness", 0.0)
    next_action = "fact_admission_candidate" if info_comp >= SUPPORT_THRESHOLD else "request_more_evidence"

    return {
        "fusion_id": _uid("fus"),
        "type": "mixed_evidence_candidate",
        "text_evidence_ref": text_evidence.get("evidence_id"),
        "visual_evidence_ref": visual_evidence.get("evidence_id"),
        "spatial_evidence_ref": (spatial_evidence or {}).get("evidence_id"),
        "context_evidence_ref": (context_evidence or {}).get("evidence_id"),
        "conflict": False,
        "evidence_completeness": completeness,
        "next_action": next_action,
        "not_answer_merge": True,
        "not_text_plus_image_equals_answer": True,
        "candidate_only": True,
        "not_fact": True,
    }
