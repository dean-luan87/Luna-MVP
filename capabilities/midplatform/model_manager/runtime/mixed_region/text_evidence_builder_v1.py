# -*- coding: utf-8 -*-
"""Text Evidence Builder — Layer 1: characters, digits, symbols v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_text_evidence(
    *,
    ocr_evidence: Dict[str, Any],
    region_analysis: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Normalize OCR output to Layer 1 text_candidate — not fact."""
    etype = ocr_evidence.get("evidence_type", "")
    if etype not in ("ocr_text_candidate", "ocr_low_confidence_candidate"):
        return {
            "evidence_id": _uid("tev"),
            "type": "text_candidate",
            "text": None,
            "confidence": 0.0,
            "status": "unavailable",
            "source": "ocr_recognition",
            "candidate_only": True,
            "not_fact": True,
        }

    text = ocr_evidence.get("candidate_text", "")
    conf = ocr_evidence.get("confidence", 0.0)
    damaged = (region_analysis or {}).get("text_damaged", False)

    return {
        "evidence_id": _uid("tev"),
        "type": "text_candidate",
        "text": text,
        "confidence": conf,
        "source_region_id": ocr_evidence.get("source_region_id"),
        "language": ocr_evidence.get("language", "zh"),
        "text_damaged": damaged,
        "not_text_completion_by_vlm": True,
        "source": "ocr_recognition",
        "candidate_only": True,
        "not_fact": True,
    }
