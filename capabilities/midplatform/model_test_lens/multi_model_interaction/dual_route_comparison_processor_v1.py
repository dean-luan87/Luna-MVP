# -*- coding: utf-8
"""Midplatform dual route comparison processor v1 — candidate only, no fact."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

COMPARISON_DIMENSIONS = (
    "region_overlap",
    "text_likelihood",
    "route_agreement",
    "route_conflict",
    "trace_completeness",
    "uncertainty",
    "recommended_next_task",
)


def _bbox_center(bbox: Dict[str, float]) -> Tuple[float, float]:
    return (
        (bbox.get("x1", 0) + bbox.get("x2", 0)) / 2.0,
        (bbox.get("y1", 0) + bbox.get("y2", 0)) / 2.0,
    )


def _bbox_overlap(a: Dict[str, float], b: Dict[str, float]) -> float:
    x1 = max(a.get("x1", 0), b.get("x1", 0))
    y1 = max(a.get("y1", 0), b.get("y1", 0))
    x2 = min(a.get("x2", 1), b.get("x2", 1))
    y2 = min(a.get("y2", 1), b.get("y2", 1))
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    area_a = max((a.get("x2", 0) - a.get("x1", 0)) * (a.get("y2", 0) - a.get("y1", 0)), 1e-6)
    area_b = max((b.get("x2", 0) - b.get("x1", 0)) * (b.get("y2", 0) - b.get("y1", 0)), 1e-6)
    union = area_a + area_b - inter
    return max(0.0, min(1.0, inter / union))


def _max_region_overlap(
    grounding: List[Dict[str, Any]],
    attention_regions: List[Dict[str, Any]],
) -> float:
    best = 0.0
    for g in grounding:
        gb = g.get("bbox") or {}
        for reg in attention_regions:
            hb = reg.get("bbox_hint") or {}
            best = max(best, _bbox_overlap(gb, hb))
    return best


def _text_likelihood_score(grounding: List[Dict[str, Any]], vlm: Dict[str, Any]) -> float:
    if not grounding:
        return 0.0
    g_scores = [float(g.get("text_likelihood", 0.0)) for g in grounding]
    base = max(g_scores) if g_scores else 0.0
    if "ocr" in (vlm.get("suggested_followup_models") or []):
        base = max(base, 0.55)
    return min(1.0, base)


def _trace_complete(route_a: Dict[str, Any], route_b: Dict[str, Any]) -> bool:
    g = route_a.get("grounding_detection_candidates") or []
    m = route_a.get("sam_refine_mask_candidates") or []
    v = route_b.get("vlm_route_candidate") or {}
    if not v.get("trace_chain"):
        return False
    if g and not m:
        return False
    for item in g:
        if not item.get("trace_chain"):
            return False
    return True


def _label_conflict(grounding: List[Dict[str, Any]], vlm: Dict[str, Any]) -> bool:
    if not grounding:
        return False
    labels = {g.get("detected_label_candidate", "") for g in grounding}
    if "person_candidate" in labels:
        regions = vlm.get("suggested_attention_regions") or []
        for reg in regions:
            hint = reg.get("region_hint", "")
            reason = reg.get("attention_reason_candidate", "")
            if "sign" in hint or "ocr" in reason or "text" in reason:
                return True
    return False


def compare_routes(
    route_a_pkg: Dict[str, Any],
    route_b_pkg: Dict[str, Any],
    *,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    fixture_config = fixture_config or {}
    grounding = route_a_pkg.get("grounding_detection_candidates") or []
    masks = route_a_pkg.get("sam_refine_mask_candidates") or []
    vlm = route_b_pkg.get("vlm_route_candidate") or {}
    attention = vlm.get("suggested_attention_regions") or []

    route_a_refs = [g["candidate_id"] for g in grounding] + [m["candidate_id"] for m in masks]
    route_b_refs = [vlm["candidate_id"]] if vlm.get("candidate_id") else []

    trace_ok = _trace_complete(route_a_pkg, route_b_pkg)
    overlap = _max_region_overlap(grounding, attention)
    text_score = _text_likelihood_score(grounding, vlm)
    conflict = _label_conflict(grounding, vlm) or bool(fixture_config.get("route_conflict"))

    if fixture_config.get("route_a_miss") or (not grounding and vlm.get("candidate_id")):
        agreement = "route_a_miss_route_b_only"
        conflict_type = "none"
        followup = "manual_review"
        priority = "downgrade"
        admission = "manual_review_only"
        agreement_score = 0.2
    elif conflict:
        agreement = "conflict"
        conflict_type = "label_semantic_conflict"
        followup = "conflict_review"
        priority = "block_auto_admission"
        admission = "block_auto_admission"
        agreement_score = 0.15
    elif not trace_ok:
        agreement = "no_overlap"
        conflict_type = "low_confidence_both"
        followup = "manual_review"
        priority = "downgrade"
        admission = "manual_review_only"
        agreement_score = 0.25
    elif overlap >= 0.45 and text_score >= 0.7:
        agreement = "high_overlap"
        conflict_type = "none"
        followup = "ocr_task_candidate"
        priority = "boost"
        admission = "task_candidate_only"
        agreement_score = 0.85
    elif overlap >= 0.2:
        agreement = "partial_overlap"
        conflict_type = "none"
        followup = "detection_task_candidate" if text_score < 0.5 else "ocr_task_candidate"
        priority = "neutral"
        admission = "task_candidate_only"
        agreement_score = 0.55
    else:
        agreement = "no_overlap"
        conflict_type = "region_mismatch"
        followup = "manual_review"
        priority = "downgrade"
        admission = "manual_review_only"
        agreement_score = 0.3

    uncertainty = float(vlm.get("uncertainty", vlm.get("confidence_or_uncertainty", 0.5)))

    comparison_id = f"drc_{uuid4().hex[:10]}"
    return {
        "comparison_id": comparison_id,
        "route_a_refs": route_a_refs,
        "route_b_refs": route_b_refs,
        "agreement_level": agreement,
        "conflict_type": conflict_type,
        "region_overlap_score": round(overlap, 3),
        "text_likelihood_score": round(text_score, 3),
        "route_agreement_score": round(agreement_score, 3),
        "uncertainty_score": round(uncertainty, 3),
        "comparison_dimensions": list(COMPARISON_DIMENSIONS),
        "recommended_followup_route": followup,
        "recommended_next_task": followup,
        "priority_signal": priority,
        "recommended_admission_mode": admission,
        "candidate_only": True,
        "not_fact": True,
        "dual_route_comparison_not_fact": True,
        "dual_route_conflict_not_auto_fact": priority == "block_auto_admission",
        "no_fact_write": True,
        "no_ocr_execution": True,
        "no_navigation_decision": True,
        "trace_chain": [
            {"stage": "route_a_grounding_detection", "ref": route_a_refs[0] if route_a_refs else "none"},
            {"stage": "route_b_vlm_route", "ref": route_b_refs[0] if route_b_refs else "none"},
            {"stage": "midplatform_dual_route_comparison", "ref": comparison_id},
        ],
    }


def run_dual_route_validation(
    *,
    image_ref: str,
    scene_profile_candidate: Optional[Dict[str, Any]] = None,
    fixture_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_route_a_v1 import (
        run_route_a_stub,
    )
    from capabilities.midplatform.model_test_lens.multi_model_interaction.dual_route_perception_route_b_v1 import (
        run_route_b_stub,
    )

    fixture_config = dict(fixture_config or {})
    route_a = run_route_a_stub(
        image_ref=image_ref,
        scene_profile_candidate=scene_profile_candidate,
        fixture_config=fixture_config,
    )
    route_b = run_route_b_stub(
        image_ref=image_ref,
        scene_profile_candidate=scene_profile_candidate,
        fixture_config=fixture_config,
    )
    comparison = compare_routes(route_a, route_b, fixture_config=fixture_config)
    return {
        "execution_mode": "deterministic_stub",
        "no_model_call": True,
        "route_a": route_a,
        "route_b": route_b,
        "dual_route_comparison_candidate": comparison,
        "candidate_only": True,
        "not_fact": True,
    }
