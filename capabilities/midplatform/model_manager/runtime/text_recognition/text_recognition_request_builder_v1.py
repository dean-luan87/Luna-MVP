# -*- coding: utf-8 -*-
"""OCR Recognition Request Builder — text_region_candidate → runtime request v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_text_recognition_request(
    *,
    image_ref: str = "image_fixture",
    text_region_evidence: Dict[str, Any],
    slot_id: str = "slot_2",
    capability: str = "text_recognition",
    provider_id: str = "paddleocr_recognizer_v1",
    plan: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build OCR runtime request from upstream text_region_candidate.
    Recognition only — no full-image scan, no bundled detection.
    """
    regions = text_region_evidence.get("regions") or []
    region_ids = text_region_evidence.get("region_ids") or [r.get("region_id") for r in regions]
    goal = ((plan or {}).get("plan_goal_candidate") or {}).get("goal_type", "unknown")

    return {
        "request_id": _uid("ocr"),
        "slot_id": slot_id,
        "capability": capability,
        "provider_id": provider_id,
        "image_ref": image_ref,
        "runtime_mode": "recognition_only",
        "run_detection": False,
        "recognition_regions": regions,
        "source_region_ids": [rid for rid in region_ids if rid],
        "upstream_evidence_id": text_region_evidence.get("evidence_id"),
        "upstream_evidence_type": text_region_evidence.get("evidence_type"),
        "goal_hint_for_logging_only": goal,
        "not_task_decider": True,
        "not_full_image_ocr": True,
        "candidate_only": True,
    }
