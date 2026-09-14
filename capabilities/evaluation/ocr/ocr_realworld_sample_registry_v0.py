# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-RealSamples-001 — Real-world difficult sample registry (no OCR provider).

Manifest / taxonomy / annotation templates only; safe for offline curation.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

REQUIRED_CONTENT_TYPES_V0: Tuple[str, ...] = (
    "icon_text_mix",
    "multi_panel_layout",
    "artistic_text",
    "stylized_digits",
    "decorative_graphic_non_text",
)

OPTIONAL_CONTENT_TYPES_V0: Tuple[str, ...] = (
    "product_label",
    "signboard",
    "vertical_text",
    "low_quality_text",
)

ALL_CURATED_TYPES_V0: Tuple[str, ...] = REQUIRED_CONTENT_TYPES_V0 + OPTIONAL_CONTENT_TYPES_V0

EXPECTED_ROUTE_BY_TYPE_V0: Dict[str, str] = {
    "icon_text_mix": "visual_symbol_branch",
    "multi_panel_layout": "layout_branch",
    "artistic_text": "visual_glyph_branch",
    "stylized_digits": "visual_glyph_branch",
    "decorative_graphic_non_text": "reject_low_quality",
    "product_label": "layout_branch",
    "signboard": "layout_branch",
    "vertical_text": "layout_branch",
    "low_quality_text": "reject_low_quality",
}


def _expected_route(content_type: str) -> str:
    return EXPECTED_ROUTE_BY_TYPE_V0.get(content_type, "manual_review")


def build_realworld_annotation_template_v0(*, sample_id: str, content_type: str) -> Dict[str, Any]:
    """Per-image human curation template (OCR-006 taxonomy aligned)."""
    return {
        "sample_id": sample_id,
        "content_type": content_type,
        "human_review_status": "pending",
        "visible_text_regions": [],
        "visual_symbols": [],
        "visual_glyphs": [],
        "layout_groups": [],
        "expected_ocr_behavior": {
            "ordinary_ocr_should_read": content_type != "decorative_graphic_non_text",
            "ordinary_ocr_should_not_read_symbols": True,
            "global_raw_text_joined_allowed": False,
            "expected_route": _expected_route(content_type),
        },
        "notes": "",
    }


def build_realworld_sample_manifest_row_v0(
    *,
    sample_id: str,
    image_rel_path: str,
    annotation_rel_path: str,
    content_type: str,
    sample_source: str,
    language: str,
    has_ground_truth: bool,
    ground_truth_quality: str,
    sha256_hex: str,
    width: int,
    height: int,
) -> Dict[str, Any]:
    er = _expected_route(content_type)
    return {
        "sample_id": sample_id,
        "image_path": image_rel_path,
        "annotation_path": annotation_rel_path,
        "content_type": content_type,
        "sample_source": sample_source,
        "language": language,
        "has_ground_truth": has_ground_truth,
        "ground_truth_quality": ground_truth_quality,
        "expected_route": er,
        "should_enter_mainline_ocr": content_type not in ("decorative_graphic_non_text",),
        "should_enter_fact_text_layer": False,
        "requires_layout_branch": content_type in ("multi_panel_layout", "product_label", "signboard", "vertical_text"),
        "requires_symbol_branch": content_type == "icon_text_mix",
        "requires_glyph_branch": content_type in ("artistic_text", "stylized_digits"),
        "sha256": sha256_hex,
        "width": int(width),
        "height": int(height),
    }


def validate_realworld_sample_manifest_v0(*, rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    violations: List[str] = []
    seen_ids: set[str] = set()
    for i, row in enumerate(rows):
        sid = str(row.get("sample_id") or "")
        if not sid:
            violations.append(f"row_{i}:missing_sample_id")
        elif sid in seen_ids:
            violations.append(f"row_{i}:duplicate_sample_id:{sid}")
        else:
            seen_ids.add(sid)

        src = str(row.get("sample_source") or "")
        if src not in ("manual_import", "user_fixture", "captured_frame", "public_reference", "placeholder"):
            violations.append(f"row_{i}:bad_sample_source:{src}")

        if src == "placeholder":
            if row.get("has_ground_truth") is True:
                violations.append(f"row_{i}:placeholder_must_not_claim_ground_truth")
            if str(row.get("ground_truth_quality") or "") not in ("missing", "not_applicable"):
                violations.append(f"row_{i}:placeholder_ground_truth_quality")

        if src != "placeholder":
            if not str(row.get("sha256") or "").strip():
                violations.append(f"row_{i}:missing_sha256_non_placeholder")

        ct = str(row.get("content_type") or "")
        if ct not in ALL_CURATED_TYPES_V0:
            violations.append(f"row_{i}:unknown_content_type:{ct}")

        if row.get("should_enter_fact_text_layer") is True:
            violations.append(f"row_{i}:fact_text_layer_must_be_false_in_this_phase")

    return {"validation_passed": len(violations) == 0, "violations": violations}


def build_realworld_taxonomy_coverage_report_v0(*, rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, Dict[str, int]] = {t: {"real": 0, "placeholder": 0, "total": 0} for t in ALL_CURATED_TYPES_V0}
    for row in rows:
        ct = str(row.get("content_type") or "")
        if ct not in counts:
            continue
        is_ph = str(row.get("sample_source") or "") == "placeholder"
        counts[ct]["total"] += 1
        if is_ph:
            counts[ct]["placeholder"] += 1
        else:
            counts[ct]["real"] += 1

    required_met = all(counts[t]["total"] > 0 for t in REQUIRED_CONTENT_TYPES_V0)
    return {
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "per_type": counts,
        "required_types_all_present": required_met,
        "required_content_types": list(REQUIRED_CONTENT_TYPES_V0),
    }


def build_ocr_realworld_dataset_registry_for_reeval_v0(
    *,
    dataset_id: str,
    dataset_root: str,
    manifest_rows: Sequence[Dict[str, Any]],
    taxonomy_report: Dict[str, Any],
) -> Dict[str, Any]:
    """Single registry entry document for follow-on OCR-006-RealEval (evaluation-only)."""
    cats = sorted({str(r.get("content_type")) for r in manifest_rows if r.get("content_type")})
    return {
        "registry_kind": "ocr_realworld_difficult_v0",
        "phase": "Phase-EvaluationTools-OCR-RealSamples-001",
        "entry": {
            "dataset_id": dataset_id,
            "dataset_type": "difficult_cases",
            "root": dataset_root,
            "sample_count": len(manifest_rows),
            "has_ground_truth": any(bool(r.get("has_ground_truth")) for r in manifest_rows),
            "ground_truth_quality": "partial",
            "language_coverage": ["zh", "en", "mixed", "unknown"],
            "sample_categories": cats,
            "intended_use": "provider_eval",
            "runtime_allowed": False,
            "taxonomy": taxonomy_report,
        },
    }


def sha256_file_v0(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def image_dimensions_v0(path: Path) -> Tuple[int, int]:
    from PIL import Image

    with Image.open(str(path)) as im:
        return int(im.width), int(im.height)


__all__ = [
    "ALL_CURATED_TYPES_V0",
    "OPTIONAL_CONTENT_TYPES_V0",
    "REQUIRED_CONTENT_TYPES_V0",
    "build_ocr_realworld_dataset_registry_for_reeval_v0",
    "build_realworld_annotation_template_v0",
    "build_realworld_sample_manifest_row_v0",
    "build_realworld_taxonomy_coverage_report_v0",
    "image_dimensions_v0",
    "sha256_file_v0",
    "validate_realworld_sample_manifest_v0",
]
