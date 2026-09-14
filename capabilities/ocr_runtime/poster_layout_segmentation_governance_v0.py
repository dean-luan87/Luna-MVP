# -*- coding: utf-8 -*-
"""Poster layout segmentation governance stub (no OCR, no vision provider).

Phase-OCR-Poster-Layout-Segmentation-Governance-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SUMMARY_SCHEMA = "poster_layout_segmentation_governance_summary_v0"
FIXTURE_MANIFEST_SCHEMA = "poster_synthetic_fixture_manifest_v0"
LAYOUT_CANDIDATE_SCHEMA = "poster_layout_candidate_v0"
TEXT_REGIONS_SCHEMA = "poster_text_region_candidates_v0"
NON_TEXT_REGIONS_SCHEMA = "poster_non_text_region_candidates_v0"
VISUAL_SYMBOL_SCHEMA = "poster_visual_symbol_candidates_v0"
OCR_PLAN_SCHEMA = "poster_ocr_region_plan_v0"
READING_ORDER_SCHEMA = "poster_reading_order_candidate_v0"
RISK_SCHEMA = "poster_layout_risk_report_v0"
GATE_SCHEMA = "poster_layout_gate_policy_report_v0"
AUDIT_SCHEMA = "poster_layout_governance_audit_v0"

PHASE_ID = "OCR-Poster-Layout-Segmentation-Governance-001"
POSTER_W = 720
POSTER_H = 900

# region_id -> (bbox, label text or None, region_type for layout)
_LAYOUT_SPECS: Tuple[Tuple[str, str, List[int], Optional[str]], ...] = (
    ("title_area", "title_area", [40, 24, 680, 110], "BIG SALE"),
    ("body_text_area", "body_text_area", [40, 118, 680, 200], "Summer Discount"),
    ("price_or_promo_area", "price_or_promo_area", [40, 210, 420, 290], "50% OFF"),
    ("time_location_area", "time_location_area", [40, 300, 680, 360], "2026.05.18 - 2026.05.25"),
    ("qr_or_logo_area", "qr_or_logo_area", [40, 372, 400, 552], None),
    ("product_or_decoration_area", "product_or_decoration_area", [420, 372, 680, 860], None),
)

_LOGO_BBOX = [40, 372, 190, 552]
_QR_BBOX = [200, 372, 400, 552]
_BACKGROUND_BBOX = [40, 572, 680, 880]


def _load_font(size: int = 28) -> Any:
    from PIL import ImageFont

    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(fp, size)
        except OSError:
            continue
    return ImageFont.load_default()


def create_synthetic_poster_fixture_v0(work_dir: Path) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    image_path = (work_dir / "poster_synthetic_fixture_v0.png").resolve()

    img = Image.new("RGB", (POSTER_W, POSTER_H), (245, 248, 252))
    draw = ImageDraw.Draw(img)
    title_font = _load_font(48)
    body_font = _load_font(32)
    promo_font = _load_font(36)
    small_font = _load_font(22)
    logo_font = _load_font(18)

    for region_id, _rtype, bbox, text in _LAYOUT_SPECS:
        x1, y1, x2, y2 = bbox
        draw.rectangle([x1, y1, x2, y2], outline=(180, 190, 200), width=2)
        if text:
            font = title_font if region_id == "title_area" else body_font
            if region_id == "price_or_promo_area":
                font = promo_font
            if region_id == "time_location_area":
                font = small_font
            draw.text((x1 + 12, y1 + 10), text, fill=(20, 20, 30), font=font)

    lx1, ly1, lx2, ly2 = _LOGO_BBOX
    draw.rectangle([lx1, ly1, lx2, ly2], fill=(230, 235, 245), outline=(120, 130, 150))
    draw.text((lx1 + 16, ly1 + 40), "LUNA LOGO", fill=(60, 70, 90), font=logo_font)
    draw.ellipse([lx1 + 120, ly1 + 20, lx1 + 160, ly1 + 60], outline=(80, 100, 140), width=3)

    qx1, qy1, qx2, qy2 = _QR_BBOX
    draw.rectangle([qx1, qy1, qx2, qy2], fill=(255, 255, 255), outline=(0, 0, 0))
    cell = 14
    for row in range(0, (qy2 - qy1) // cell):
        for col in range(0, (qx2 - qx1) // cell):
            if (row + col) % 2 == 0:
                cx = qx1 + col * cell
                cy = qy1 + row * cell
                draw.rectangle([cx, cy, cx + cell - 1, cy + cell - 1], fill=(0, 0, 0))

    px1, py1, px2, py2 = [420, 372, 680, 860]
    colors = [(255, 120, 90), (90, 160, 220), (140, 200, 120)]
    for i, c in enumerate(colors):
        oy = py1 + 20 + i * 140
        draw.rectangle([px1 + 20, oy, px2 - 20, oy + 110], fill=c, outline=(80, 80, 80))

    bx1, by1, bx2, by2 = _BACKGROUND_BBOX
    draw.rectangle([bx1, by1, bx2, by2], fill=(235, 238, 242), outline=(200, 205, 210))
    for i in range(6):
        draw.line([bx1 + 30 + i * 100, by1 + 20, bx1 + 50 + i * 100, by2 - 20], fill=(210, 215, 220), width=2)

    img.save(image_path, format="PNG")

    return {
        "schema_version": FIXTURE_MANIFEST_SCHEMA,
        "fixture_id": "poster_synthetic_fixture_v0",
        "source_image_ref": str(image_path),
        "width": POSTER_W,
        "height": POSTER_H,
        "image_type": "poster_like",
        "synthetic": True,
        "regions_drawn": [s[0] for s in _LAYOUT_SPECS] + ["logo_area", "qr_area", "background_or_decoration_area"],
        "ocr_invoked": False,
    }


def _region_stub(
    *,
    region_id: str,
    region_type: str,
    bbox: List[int],
    ocr_allowed: bool,
    recommended_evidence_type: str,
    recommended_provider_class: str,
    reading_order_hint: int,
    risk_flags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "region_id": region_id,
        "region_type": region_type,
        "bbox": bbox,
        "ocr_allowed": ocr_allowed,
        "recommended_evidence_type": recommended_evidence_type,
        "recommended_provider_class": recommended_provider_class,
        "reading_order_hint": reading_order_hint,
        "risk_flags": list(risk_flags or []),
    }


def build_layout_candidate(*, source_image_ref: str) -> Dict[str, Any]:
    regions: List[Dict[str, Any]] = []
    order = 1
    for region_id, region_type, bbox, _text in _LAYOUT_SPECS:
        ocr_ok = region_id not in ("qr_or_logo_area", "product_or_decoration_area")
        ev = "layout_text_evidence_candidate" if ocr_ok else "non_text_region"
        if region_id == "qr_or_logo_area":
            ev = "visual_symbol_zone"
        prov = "ocr_lightweight_text" if ocr_ok else "none"
        risks: List[str] = []
        if region_id == "price_or_promo_area":
            risks.append("commercial_text_may_expire")
        if region_id == "time_location_area":
            risks.append("temporal_text_requires_ttl")
        regions.append(
            _region_stub(
                region_id=region_id,
                region_type=region_type,
                bbox=bbox,
                ocr_allowed=ocr_ok,
                recommended_evidence_type=ev,
                recommended_provider_class=prov,
                reading_order_hint=order if ocr_ok else 0,
                risk_flags=risks,
            )
        )
        if ocr_ok:
            order += 1

    return {
        "schema_version": LAYOUT_CANDIDATE_SCHEMA,
        "source_image_ref": source_image_ref,
        "image_type": "poster_like",
        "text_density": "high",
        "layout_complexity": "high",
        "full_image_ocr_allowed": False,
        "ocr_strategy": "segment_first",
        "regions": regions,
    }


def build_text_region_candidates() -> Dict[str, Any]:
    rows = [
        _region_stub(
            region_id="title_area",
            region_type="title_area",
            bbox=[40, 24, 680, 110],
            ocr_allowed=True,
            recommended_evidence_type="layout_text_evidence_candidate",
            recommended_provider_class="ocr_lightweight_text",
            reading_order_hint=1,
            risk_flags=[],
        ),
        _region_stub(
            region_id="body_text_area",
            region_type="body_text_area",
            bbox=[40, 118, 680, 200],
            ocr_allowed=True,
            recommended_evidence_type="layout_text_evidence_candidate",
            recommended_provider_class="ocr_lightweight_text",
            reading_order_hint=2,
            risk_flags=[],
        ),
        _region_stub(
            region_id="price_or_promo_area",
            region_type="price_or_promo_area",
            bbox=[40, 210, 420, 290],
            ocr_allowed=True,
            recommended_evidence_type="layout_text_evidence_candidate",
            recommended_provider_class="ocr_lightweight_text",
            reading_order_hint=3,
            risk_flags=["commercial_text_may_expire"],
        ),
        _region_stub(
            region_id="time_location_area",
            region_type="time_location_area",
            bbox=[40, 300, 680, 360],
            ocr_allowed=True,
            recommended_evidence_type="layout_text_evidence_candidate",
            recommended_provider_class="ocr_lightweight_text",
            reading_order_hint=4,
            risk_flags=["temporal_text_requires_ttl"],
        ),
    ]
    return {"schema_version": TEXT_REGIONS_SCHEMA, "candidate_count": len(rows), "candidates": rows}


def build_non_text_region_candidates() -> Dict[str, Any]:
    rows = [
        _region_stub(
            region_id="product_or_decoration_area",
            region_type="product_or_decoration_area",
            bbox=[420, 372, 680, 860],
            ocr_allowed=False,
            recommended_evidence_type="non_text_region",
            recommended_provider_class="none",
            reading_order_hint=0,
            risk_flags=["non_text_region_filtered"],
        ),
        _region_stub(
            region_id="background_or_decoration_area",
            region_type="background_or_decoration_area",
            bbox=_BACKGROUND_BBOX,
            ocr_allowed=False,
            recommended_evidence_type="non_text_region",
            recommended_provider_class="none",
            reading_order_hint=0,
            risk_flags=["non_text_region_filtered"],
        ),
    ]
    return {"schema_version": NON_TEXT_REGIONS_SCHEMA, "candidate_count": len(rows), "candidates": rows}


def build_visual_symbol_candidates() -> Dict[str, Any]:
    rows = [
        _region_stub(
            region_id="logo_area",
            region_type="logo_area",
            bbox=_LOGO_BBOX,
            ocr_allowed=False,
            recommended_evidence_type="visual_symbol_candidate",
            recommended_provider_class="none",
            reading_order_hint=0,
            risk_flags=["logo_not_ocr_text", "visual_symbol_not_plain_text"],
        ),
        _region_stub(
            region_id="qr_area",
            region_type="qr_area",
            bbox=_QR_BBOX,
            ocr_allowed=False,
            recommended_evidence_type="qr_candidate",
            recommended_provider_class="none",
            reading_order_hint=0,
            risk_flags=["qr_not_ocr_text", "visual_symbol_not_plain_text"],
        ),
    ]
    return {"schema_version": VISUAL_SYMBOL_SCHEMA, "candidate_count": len(rows), "candidates": rows}


def build_ocr_region_plan() -> Dict[str, Any]:
    text_doc = build_text_region_candidates()
    planned: List[Dict[str, Any]] = []
    for i, cand in enumerate(text_doc["candidates"], start=1):
        planned.append(
            {
                "region_id": cand["region_id"],
                "region_type": cand["region_type"],
                "bbox": cand["bbox"],
                "recommended_provider_class": cand["recommended_provider_class"],
                "priority": i,
                "timeout_policy_placeholder": "poster_region_ocr_timeout_stub_v0",
                "expected_output": "layout_text_evidence_candidate",
            }
        )
    return {
        "schema_version": OCR_PLAN_SCHEMA,
        "full_image_ocr_allowed": False,
        "ocr_strategy": "segment_first",
        "planned_regions": planned,
    }


def build_reading_order_candidate() -> Dict[str, Any]:
    return {
        "schema_version": READING_ORDER_SCHEMA,
        "reading_order_confidence": "low",
        "reading_order_strategy": "layout_region_order_stub",
        "ordered_region_ids": [
            "title_area",
            "body_text_area",
            "price_or_promo_area",
            "time_location_area",
        ],
        "force_semantic_join_allowed": False,
        "reason_codes": ["complex_layout", "reading_order_uncertain"],
    }


def build_risk_report() -> Dict[str, Any]:
    items = [
        {
            "risk_id": "complex_layout",
            "active": True,
            "description": "Poster layout has multiple text blocks and visual zones.",
        },
        {
            "risk_id": "reading_order_uncertain",
            "active": True,
            "description": "Reading order is stub-only; semantic join forbidden.",
        },
        {
            "risk_id": "commercial_text_may_expire",
            "active": True,
            "description": "Promotional copy may be stale; not durable facts.",
        },
        {
            "risk_id": "visual_symbol_not_plain_text",
            "active": True,
            "description": "Logo/QR are visual symbols, not plain OCR text chain.",
        },
        {
            "risk_id": "full_image_ocr_forbidden_by_default",
            "active": True,
            "description": "full_image_ocr_allowed=false for poster_like inputs.",
        },
        {
            "risk_id": "non_text_region_filtered",
            "active": True,
            "description": "Product/decoration/background excluded from OCR plan.",
        },
        {
            "risk_id": "logo_not_ocr_text",
            "active": True,
            "description": "Logo area must not enter ordinary OCR text chain.",
        },
        {
            "risk_id": "qr_not_ocr_text",
            "active": True,
            "description": "QR area must not enter ordinary OCR text chain.",
        },
        {
            "risk_id": "no_fact_write",
            "active": True,
            "description": "All governance outputs remain not_fact; no writes.",
        },
    ]
    return {"schema_version": RISK_SCHEMA, "risk_count": len(items), "risks": items}


def build_gate_policy_report() -> Dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA,
        "full_image_ocr_allowed_default": False,
        "segment_first_required": True,
        "visual_symbol_evidence_split_required": True,
        "ordinary_ocr_text_chain_excludes_logo_qr": True,
        "layout_text_evidence_not_fact": True,
        "commercial_text_requires_ttl": True,
        "world_model_write_allowed": False,
        "scene_delta_write_allowed": False,
        "midplatform_fact_write_allowed": False,
        "navigation_decision_allowed": False,
        "auto_approval_allowed": False,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "poster_layout_governance_executed": True,
        "governance_only": True,
        "full_image_ocr_allowed": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(*, source_image_ref: str) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "governance_scope": "layout_governance_only",
        "image_type": "poster_like",
        "ocr_strategy": "segment_first",
        "full_image_ocr_allowed": False,
        "layout_segmentation_required": True,
        "source_image_ref": source_image_ref,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fact_status": "not_fact",
    }


def run_poster_layout_segmentation_governance_v0(
    *,
    v1_planning_root: Optional[str] = None,
    work_dir: Path,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    if v1_planning_root:
        plan = Path(v1_planning_root).resolve()
        gate_path = plan / "cross_modal_vision_ocr_testboard_v1_gate_policy.json"
        if not gate_path.is_file():
            errs.append("missing_v1_gate_policy")
        else:
            gate = json.loads(gate_path.read_text(encoding="utf-8"))
            poster = (
                gate.get("track_policies", {}).get("TVOCR_V1_B_POSTER_LAYOUT", {})
                if isinstance(gate.get("track_policies"), dict)
                else {}
            )
            if poster.get("full_image_ocr_allowed_default") is not False:
                errs.append("v1_poster_full_image_ocr_not_false")

    fixture_dir = work_dir / "fixtures"
    manifest = create_synthetic_poster_fixture_v0(fixture_dir)
    source_ref = str(manifest["source_image_ref"])

    summary = build_summary(source_image_ref=source_ref)
    layout = build_layout_candidate(source_image_ref=source_ref)
    text_regions = build_text_region_candidates()
    non_text = build_non_text_region_candidates()
    visual = build_visual_symbol_candidates()
    ocr_plan = build_ocr_region_plan()
    reading = build_reading_order_candidate()
    risks = build_risk_report()
    gate_report = build_gate_policy_report()
    audit = build_audit()

    if v1_planning_root:
        summary["v1_planning_root"] = str(Path(v1_planning_root).resolve())

    return (
        summary,
        manifest,
        layout,
        text_regions,
        non_text,
        visual,
        ocr_plan,
        reading,
        risks,
        gate_report,
        audit,
        errs,
    )
