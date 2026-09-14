# -*- coding: utf-8 -*-
"""OCR Recognition Response Parser — raw runtime → structured text candidates v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def parse_text_recognition_response(
    raw: Dict[str, Any],
    *,
    provider_id: str = "paddleocr_recognizer_v1",
    source_region_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Parse PaddleOCR recognition output — character candidates per region."""
    if raw.get("runtime_unavailable"):
        return {
            "parse_status": "runtime_unavailable",
            "provider_id": provider_id,
            "text_candidates": [],
            "runtime_unavailable": True,
            "candidate_only": True,
        }

    if raw.get("unsupported_claim"):
        return {
            "parse_status": "unsupported_claim",
            "provider_id": provider_id,
            "text_candidates": raw.get("text_candidates") or [],
            "unsupported_claim": True,
            "missing_region_support": True,
            "candidate_only": True,
        }

    items = raw.get("rec_texts") or raw.get("text_candidates") or []
    region_ids = source_region_ids or raw.get("source_region_ids") or []
    text_candidates: List[Dict[str, Any]] = []

    for i, item in enumerate(items):
        if isinstance(item, str):
            text = item
            conf = raw.get("confidence", 0.0)
            region_id = region_ids[i] if i < len(region_ids) else f"region_{i + 1:03d}"
        else:
            text = item.get("text") or item.get("candidate_text", "")
            conf = item.get("confidence", item.get("score", 0.0))
            region_id = item.get("source_region_id") or (
                region_ids[i] if i < len(region_ids) else f"region_{i + 1:03d}"
            )

        text_candidates.append({
            "candidate_text": text,
            "confidence": conf,
            "source_region_id": region_id,
            "language": item.get("language", "zh") if isinstance(item, dict) else "zh",
        })

    return {
        "parse_status": "ok" if text_candidates else "empty",
        "provider_id": provider_id,
        "text_candidate_count": len(text_candidates),
        "text_candidates": text_candidates,
        "low_confidence": raw.get("low_confidence", False),
        "candidate_only": True,
    }
