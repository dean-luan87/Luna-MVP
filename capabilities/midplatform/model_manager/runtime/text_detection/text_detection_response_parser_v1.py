# -*- coding: utf-8 -*-
"""Text Detection Response Parser — raw runtime → structured regions v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def parse_text_detection_response(
    raw: Dict[str, Any],
    *,
    provider_id: str = "paddleocr_detector_v1",
) -> Dict[str, Any]:
    """Parse PaddleOCR/DBNet-style detection output."""
    boxes = raw.get("boxes") or raw.get("dt_boxes") or []
    regions: List[Dict[str, Any]] = []
    for i, box in enumerate(boxes):
        bbox = box.get("bbox") or box.get("box") or box
        conf = box.get("confidence", box.get("score", 0.0))
        regions.append({
            "region_id": f"region_{i + 1:03d}",
            "bbox": bbox,
            "confidence": conf,
            "polygon": box.get("polygon"),
        })

    return {
        "parse_status": "ok" if regions or raw.get("no_text") else "empty",
        "provider_id": provider_id,
        "region_count": len(regions),
        "regions": regions,
        "no_text": raw.get("no_text", False),
        "low_confidence": raw.get("low_confidence", False),
        "candidate_only": True,
    }
