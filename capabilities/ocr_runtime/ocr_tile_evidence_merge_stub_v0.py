# -*- coding: utf-8 -*-
"""
OCR multi-tile evidence merge stub v0 — merge per-tile stub items into unified evidence / bridge fields.

No real OCR. No duplicate-text merge heuristics.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_partial_evidence_completion_stub_v0(
    *,
    raw_observed_core: str,
    evidence_scope: str,
) -> Dict[str, Any]:
    """
    Reserved contract for Phase-OCR-Partial-Evidence-Completion-Policy-001.
    Does NOT generate completions — only strict placeholders and risk gates.
    """
    partial = str(evidence_scope or "") == "partial_image"
    return {
        "schema_version": "ocr_partial_evidence_completion_policy_stub_v0",
        "terminology_en": "Partial_Evidence_Completion_candidate_not_fact_completion",
        "terminology_zh": "局部证据补全候选_非事实补全",
        "completion_allowed": False,
        "completion_required": False,
        "completion_candidates": [],
        "completion_source_policy": "reserved_v0_no_memory_no_search_no_user_loop",
        "user_disclosure_required": partial,
        "direct_observed_text": raw_observed_core,
        "partial_scope": str(evidence_scope or ""),
        "direct_observed_vs_inferred_split": {
            "direct_observed_text": raw_observed_core,
            "inferred_or_completion_text": None,
            "disclosure": "direct_observed_is_materialized_tile_stub_OCR_only_v0",
        },
        "completion_candidate_shape_note": {
            "text": "string",
            "source": "memory|user_confirmation|lexical_association|search|context_inference|resample_async_tile",
            "confidence": "low|medium|high",
            "requires_confirmation": "boolean",
            "can_drive_action": "boolean_default_false_until_confirmed",
        },
        "risk_and_escalation_gates": {
            "completion_not_equivalent_to_ocr_direct_read": True,
            "completion_not_equivalent_to_confirmed_fact": True,
            "completion_default_must_not_drive_high_risk_action": True,
            "world_model_write_default_denied_for_completion": True,
            "user_confirm_or_reject_before_promotion": True,
        },
    }


def merge_tile_stub_evidence_v0(
    *,
    provider_out: Dict[str, Any],
    input_pack: Dict[str, Any],
    tile_plan: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Expects provider_out from stub with per-tile text_items (tile_id, original_bbox, ...).
    Returns merge payload for bridge evidence / bridge_pack.
    """
    pol = input_pack.get("processing_policy") if isinstance(input_pack.get("processing_policy"), dict) else {}
    tc = input_pack.get("tile_coverage") if isinstance(input_pack.get("tile_coverage"), dict) else {}
    items = provider_out.get("text_items") if isinstance(provider_out.get("text_items"), list) else []

    tile_evidence_items: List[Dict[str, Any]] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        tile_evidence_items.append(dict(it))

    merged_text_items: List[Dict[str, Any]] = [dict(it) for it in tile_evidence_items]

    core_parts = [str(it.get("text") or "") for it in merged_text_items if isinstance(it, dict)]
    raw_core = " | ".join(core_parts)

    scope = str(pol.get("evidence_scope") or "")
    if scope == "partial_image":
        text_joined = f"[PARTIAL_TILE_EVIDENCE] {raw_core}"
    else:
        text_joined = f"[TILED_IMAGE_EVIDENCE] {raw_core}"

    cov_complete = bool(tc.get("coverage_complete")) if tc else bool(tile_plan and tile_plan.get("coverage_complete"))
    reading_order_candidate: Dict[str, Any] = {
        "schema_version": "ocr_reading_order_candidate_stub_v0",
        "confidence": "low" if not cov_complete else "medium",
        "reason": "partial_coverage_provider_tile_order_stub_no_duplicate_merge"
        if not cov_complete
        else "tile_set_complete_provider_order_stub",
        "ordered_unit_ids": [str(it.get("unit_id") or "") for it in merged_text_items if isinstance(it, dict)],
    }

    raw_cands: List[Dict[str, Any]] = []
    for i, it in enumerate(merged_text_items):
        if not isinstance(it, dict):
            continue
        raw_cands.append(
            {
                "line_order": i,
                "text": str(it.get("text") or ""),
                "confidence": float(it.get("score") or 0.0),
                "tile_id": it.get("tile_id"),
                "unit_id": it.get("unit_id"),
                "source_unit_ref": it.get("source_unit_ref"),
            }
        )

    eligible = [dict(x) for x in tile_evidence_items]

    tile_evidence_summary = {
        "schema_version": "ocr_tile_evidence_summary_stub_v0",
        "tile_evidence_item_count": len(tile_evidence_items),
        "materialized_tile_count": int(tc.get("materialized_tile_count") or len(tile_evidence_items)),
        "raw_tile_count": int(tc.get("raw_tile_count") or (tile_plan or {}).get("raw_tile_count") or 0),
        "coverage_complete": tc.get("coverage_complete"),
        "truncated_to_budget": tc.get("truncated_to_budget"),
    }

    coverage_summary = dict(tc) if tc else {}

    pec = build_partial_evidence_completion_stub_v0(
        raw_observed_core=raw_core,
        evidence_scope=scope,
    )

    return {
        "schema_version": "ocr_tile_evidence_merge_stub_v0",
        "tile_evidence_items": tile_evidence_items,
        "merged_text_items": merged_text_items,
        "text_joined": text_joined,
        "raw_text_joined_core": raw_core,
        "raw_text_candidates": raw_cands,
        "eligible_text_evidence": eligible,
        "reading_order_candidate": reading_order_candidate,
        "coverage_summary": coverage_summary,
        "tile_evidence_summary": tile_evidence_summary,
        "partial_evidence_completion": pec,
    }
