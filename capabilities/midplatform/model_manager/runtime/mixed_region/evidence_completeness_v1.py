# -*- coding: utf-8 -*-
"""Evidence Completeness — information coverage, not probability v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def _channel_completeness(
    *,
    channel: str,
    evidence: Dict[str, Any],
    slot_expected: bool,
) -> float:
    """Compute how much of expected channel information is covered (0-1)."""
    if not slot_expected:
        return 0.0

    if channel == "text_channel":
        text = evidence.get("text")
        if not text or evidence.get("status") == "unavailable":
            return 0.0
        if evidence.get("text_damaged") or evidence.get("low_confidence"):
            return 0.5
        conf = evidence.get("confidence", 0.0)
        return min(1.0, conf) if conf > 0 else 0.3

    if channel == "visual_channel":
        features = evidence.get("features") or []
        if not features:
            return 0.0
        return min(1.0, evidence.get("confidence", 0.7))

    if channel == "spatial_channel":
        hints = evidence.get("spatial_hints") or []
        if not hints:
            return 0.0
        return min(1.0, evidence.get("confidence", 0.75))

    if channel == "context_channel":
        relations = evidence.get("scene_relations") or []
        if not relations:
            return 0.0
        return min(1.0, evidence.get("confidence", 0.7))

    if channel == "ownership_channel":
        objects = evidence.get("object_candidates") or []
        if not objects:
            return 0.0
        assigned = evidence.get("text_with_owners") or []
        if objects and assigned and all(a.get("owner_candidate") for a in assigned):
            return 0.9
        return 0.5 if objects else 0.0

    return 0.0


def compute_evidence_completeness(
    *,
    channel_activations: Dict[str, Any],
    text_evidence: Optional[Dict[str, Any]] = None,
    visual_evidence: Optional[Dict[str, Any]] = None,
    spatial_evidence: Optional[Dict[str, Any]] = None,
    context_evidence: Optional[Dict[str, Any]] = None,
    ownership_evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Information completeness — coverage of target information, NOT probability.
    """
    slots = channel_activations.get("information_slots") or []
    text_expected = any(s in slots for s in ("text", "price_number"))
    visual_expected = any(s in slots for s in ("visual_symbol", "style", "direction_symbol", "logo", "qr_code"))
    spatial_expected = any(s in slots for s in ("layout", "layout_relation", "spatial"))
    context_expected = any(s in slots for s in ("context", "scene_relation"))

    ownership_expected = "ownership" in slots

    text_comp = _channel_completeness(
        channel="text_channel", evidence=text_evidence or {}, slot_expected=text_expected,
    )
    visual_comp = _channel_completeness(
        channel="visual_channel", evidence=visual_evidence or {}, slot_expected=visual_expected,
    )
    spatial_comp = _channel_completeness(
        channel="spatial_channel", evidence=spatial_evidence or {}, slot_expected=spatial_expected,
    )
    context_comp = _channel_completeness(
        channel="context_channel", evidence=context_evidence or {}, slot_expected=context_expected,
    )
    ownership_comp = _channel_completeness(
        channel="ownership_channel", evidence=ownership_evidence or {}, slot_expected=ownership_expected,
    )

    components = [c for c, exp in [
        (text_comp, text_expected),
        (visual_comp, visual_expected),
        (spatial_comp, spatial_expected),
        (context_comp, context_expected),
        (ownership_comp, ownership_expected),
    ] if exp]

    combined = sum(components) / len(components) if components else 0.0

    return {
        "text_completeness": round(text_comp, 2),
        "visual_completeness": round(visual_comp, 2),
        "spatial_completeness": round(spatial_comp, 2),
        "context_completeness": round(context_comp, 2),
        "ownership_completeness": round(ownership_comp, 2),
        "information_completeness": round(combined, 2),
        "not_confidence": True,
        "is_coverage_not_probability": True,
        "candidate_only": True,
    }
