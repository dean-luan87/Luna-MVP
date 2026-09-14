# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — OCR capability boundary router policy draft v0.

Evaluation-only policy draft. MUST NOT be imported by runtime.
"""

from __future__ import annotations

from typing import Any, Dict

from capabilities.evaluation.ocr.ocr_capability_boundary_taxonomy_v0 import OcrContentType


def recommend_route_for_content_type_v0(content_type: OcrContentType) -> Dict[str, Any]:
    """
    Returns an evaluation-only routing recommendation for a content type.
    This is a draft for future mainline router design (manual review required).
    """
    ct = content_type
    if ct in ("zh_plain_text", "en_plain_text", "digits", "mixed_zh_en_digit", "multi_line_text"):
        return {
            "content_type": ct,
            "recommended_route": "rapidocr_primary",
            "rapidocr_expected": "strong_candidate",
            "paddleocr_expected": "fallback_candidate",
            "ocr_vl_expected": "optional",
            "mainline_action_hint": "ok_to_use_ocr_raw_text_with_quality_gate_and_layout_check",
        }
    if ct in ("document_text", "product_label"):
        return {
            "content_type": ct,
            "recommended_route": "layout_branch",
            "rapidocr_expected": "baseline_only",
            "paddleocr_expected": "strong_candidate",
            "ocr_vl_expected": "candidate",
            "mainline_action_hint": "prefer_layout_then_ocr_per_group; consider document-ocr provider",
        }
    if ct in ("icon_text_mix", "multi_panel_layout"):
        return {
            "content_type": ct,
            "recommended_route": "layout_branch",
            "rapidocr_expected": "candidate_with_symbol_guard",
            "paddleocr_expected": "candidate",
            "ocr_vl_expected": "candidate",
            "mainline_action_hint": "layout_branch_first_then_symbol_branch_then_ocr_per_roi",
        }
    if ct in ("artistic_text", "stylized_digits", "handwritten_style", "vertical_text"):
        return {
            "content_type": ct,
            "recommended_route": "visual_glyph_branch",
            "rapidocr_expected": "weak_or_unstable",
            "paddleocr_expected": "candidate",
            "ocr_vl_expected": "strong_candidate",
            "mainline_action_hint": "do_not_use_global_raw_text; route to glyph/layout specialized",
        }
    if ct in ("symbols_and_punctuation", "decorative_graphic_non_text"):
        return {
            "content_type": ct,
            "recommended_route": "visual_symbol_branch",
            "rapidocr_expected": "noise_risk",
            "paddleocr_expected": "noise_risk",
            "ocr_vl_expected": "optional",
            "mainline_action_hint": "filter_or_symbol_branch; avoid polluting OCR text evidence",
        }
    if ct in ("low_quality_text", "signboard", "zh_traditional_text"):
        return {
            "content_type": ct,
            "recommended_route": "manual_review",
            "rapidocr_expected": "unknown",
            "paddleocr_expected": "candidate",
            "ocr_vl_expected": "candidate",
            "mainline_action_hint": "apply quality gate; preprocess/crop/deskew; consider provider fallback",
        }
    return {
        "content_type": ct,
        "recommended_route": "manual_review",
        "rapidocr_expected": "unknown",
        "paddleocr_expected": "unknown",
        "ocr_vl_expected": "unknown",
        "mainline_action_hint": "unknown_content_type",
    }


def build_routing_policy_draft_v0() -> Dict[str, Any]:
    content_types = [
        "zh_plain_text",
        "zh_traditional_text",
        "en_plain_text",
        "digits",
        "symbols_and_punctuation",
        "mixed_zh_en_digit",
        "artistic_text",
        "stylized_digits",
        "icon_text_mix",
        "multi_panel_layout",
        "product_label",
        "signboard",
        "document_text",
        "vertical_text",
        "multi_line_text",
        "handwritten_style",
        "low_quality_text",
        "decorative_graphic_non_text",
    ]
    return {
        "phase": "Phase-EvaluationTools-OCR-006",
        "policy_kind": "ocr_capability_boundary_router_policy_draft_v0",
        "entries": [recommend_route_for_content_type_v0(ct) for ct in content_types],  # type: ignore[arg-type]
        "notes": "Evaluation-only draft; manual review required before any mainline reference.",
    }

