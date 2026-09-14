# -*- coding: utf-8 -*-
"""
OCR evidence item schemas v0 — design contract (TypedDict-style documentation).

Serialized as JSON dicts; no runtime persistence layer.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


QualityGateV0 = Literal["GO", "CONDITIONAL_GO", "NO_GO"]
UncertaintyLevelV0 = Literal["low", "medium", "high"]
SymbolTypeV0 = Literal[
    "warning_icon",
    "prohibition_icon",
    "arrow",
    "border",
    "slash",
    "circle",
    "triangle",
    "icon",
    "unknown",
]
GlyphTypeV0 = Literal["stylized_digit", "stylized_letter", "logo_text", "artistic_text", "unknown"]
LayoutGroupTypeV0 = Literal[
    "sign_panel",
    "product_label",
    "warning_block",
    "button_area",
    "poster_block",
    "unknown",
]


class SourceRefsV0(TypedDict, total=False):
    """Refs required for traceability; evaluation builds use eval:* URIs."""

    source_image_ref: str
    provider_ref: str
    quality_gate_ref: str
    layout_ref: str
    eligibility_gate_ref: str
    routing_ref: str
    eval_case_id: str
    eval_content_type: str
    eval_evidence_route: str


class EligibleTextEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    text: str
    bbox: List[float]
    layout_group_id: str
    provider: str
    confidence: float
    cer_estimate: Optional[float]
    quality_gate: QualityGateV0
    should_enter_fact_text_layer: bool
    source_candidate_ids: List[str]
    source_refs: SourceRefsV0


class ConditionalTextEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    text: str
    reason: List[str]
    uncertainty_level: UncertaintyLevelV0
    requires_preprocess: bool
    requires_layout_branch: bool
    requires_provider_fallback: bool
    should_enter_fact_text_layer: bool
    source_refs: SourceRefsV0


class SymbolEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    symbol_type: SymbolTypeV0
    bbox: List[float]
    overlapping_ocr_candidate_ids: List[str]
    should_enter_raw_text: bool
    should_enter_fact_text_layer: bool
    source_refs: SourceRefsV0


class GlyphEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    glyph_type: GlyphTypeV0
    visual_hint: str
    bbox: List[float]
    ocr_confirmed: bool
    requires_confirmation: bool
    should_enter_raw_text: bool
    should_enter_fact_text_layer: bool
    source_refs: SourceRefsV0


class LayoutEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    layout_group_id: str
    group_type: LayoutGroupTypeV0
    bbox: List[float]
    text_evidence_ids: List[str]
    symbol_evidence_ids: List[str]
    glyph_evidence_ids: List[str]
    reading_order_id: str
    group_raw_text_joined: str
    group_confidence: float
    should_enter_fact_text_layer: bool
    source_refs: SourceRefsV0


class RejectedOrUncertainEvidenceV0(TypedDict, total=False):
    evidence_id: str
    evidence_type: str
    rejection_reason: List[str]
    uncertainty_reason: List[str]
    original_text_or_candidate: str
    should_enter_fact_text_layer: bool
    source_refs: SourceRefsV0


def default_source_refs_v0(
    *,
    case_id: str,
    content_type: str,
    evidence_route: str,
    pack_id: str,
    eligibility_gate_root: str,
    boundary_eval_root: str,
) -> Dict[str, Any]:
    return {
        "source_image_ref": f"eval:image_ref:{case_id}",
        "provider_ref": "eval:provider:rapidocr_boundary_v0",
        "quality_gate_ref": f"eval:quality_gate:{case_id}",
        "layout_ref": f"eval:layout_ref:{case_id}",
        "eligibility_gate_ref": f"eval:eligibility_gate:{pack_id}:{case_id}",
        "routing_ref": f"eval:routing_pack:{pack_id}:{evidence_route}:{case_id}",
        "eval_case_id": case_id,
        "eval_content_type": content_type,
        "eval_evidence_route": evidence_route,
        "eval_eligibility_gate_root": eligibility_gate_root,
        "eval_boundary_eval_root": boundary_eval_root,
    }
