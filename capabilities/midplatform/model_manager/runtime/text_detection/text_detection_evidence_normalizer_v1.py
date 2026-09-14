# -*- coding: utf-8 -*-
"""Text Detection Evidence Normalizer — regions → evidence candidate v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def normalize_text_detection_evidence(
    *,
    parsed: Dict[str, Any],
    scenario: str = "shopfront",
) -> Dict[str, Any]:
    """Normalize to Luna evidence types — never place facts."""
    regions = parsed.get("regions") or []

    if parsed.get("no_text"):
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "no_text_candidate",
            "regions": [],
            "next_slot_candidate": None,
            "no_forced_ocr": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if parsed.get("low_confidence") or (regions and all(r.get("confidence", 0) < 0.4 for r in regions)):
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "low_confidence_text_candidate",
            "regions": regions,
            "requires_validation": True,
            "not_direct_ocr": True,
            "next_slot_candidate": None,
            "candidate_only": True,
            "not_fact": True,
        }

    if scenario == "metro_direction":
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "direction_text_region_candidate",
            "regions": regions,
            "not_output": "station_name_fact",
            "next_slot_candidate": {
                "slot_id": "slot_2",
                "capability": "text_recognition",
                "reason": "direction_text_region_detected",
            },
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "evidence_id": _uid("ev"),
        "evidence_type": "text_region_candidate",
        "regions": regions,
        "region_ids": [r.get("region_id") for r in regions],
        "not_semantic": True,
        "not_shopfront_identification": True,
        "next_slot_candidate": {
            "slot_id": "slot_2",
            "capability": "text_recognition",
            "reason": "text_regions_detected",
        },
        "candidate_only": True,
        "not_fact": True,
    }
