# -*- coding: utf-8 -*-
"""Text Detection Execution Simulator — deterministic dryrun fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

DRYRUN_FIXTURES: Dict[str, Dict[str, Any]] = {
    "shopfront_sign": {
        "status": "ok",
        "boxes": [{"bbox": [120, 80, 340, 160], "confidence": 0.91, "region_id": "region_001"}],
        "forbidden_fields": ["text", "place_name", "shop_name"],
    },
    "subway_platform": {
        "status": "ok",
        "boxes": [{"bbox": [50, 200, 400, 260], "confidence": 0.88, "region_id": "region_dir_001"}],
        "direction_hint": "direction_sign_area",
        "forbidden_fields": ["station_name", "text"],
    },
    "corridor_no_text": {
        "status": "ok",
        "no_text": True,
        "boxes": [],
    },
    "ad_texture_low_conf": {
        "status": "ok",
        "boxes": [{"bbox": [10, 10, 100, 50], "confidence": 0.30}],
        "low_confidence": True,
        "possible_texture_false_positive": True,
    },
    "runtime_unavailable": {
        "status": "error",
        "error_code": "text_detection_runtime_unavailable",
        "unavailable": True,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_text_detection_execution(
    *,
    fixture_key: str,
    provider_id: str = "paddleocr_detector_v1",
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Deterministic runtime — no real PaddleOCR."""
    fixture = DRYRUN_FIXTURES.get(fixture_key, DRYRUN_FIXTURES["shopfront_sign"])
    if fixture.get("unavailable"):
        return {
            "provider_execution_id": _uid("pex"),
            "request_id": request_id,
            "provider_id": provider_id,
            "status": "unavailable",
            "runtime_error_candidate": True,
            "error_code": fixture.get("error_code"),
            "fixture_key": fixture_key,
            "real_inference": False,
            "candidate_only": True,
        }
    return {
        "provider_execution_id": _uid("pex"),
        "request_id": request_id,
        "provider_id": provider_id,
        "status": "completed" if fixture.get("status") == "ok" else "failed",
        "raw_output": fixture,
        "fixture_key": fixture_key,
        "real_inference": False,
        "deterministic_fixture": True,
        "candidate_only": True,
    }
