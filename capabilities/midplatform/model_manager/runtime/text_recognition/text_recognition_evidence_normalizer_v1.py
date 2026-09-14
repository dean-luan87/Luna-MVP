# -*- coding: utf-8 -*-
"""OCR Recognition Evidence Normalizer — text → ocr_text_candidate v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

LOW_CONFIDENCE_THRESHOLD = 0.5


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def normalize_text_recognition_evidence(
    *,
    parsed: Dict[str, Any],
    scenario: str = "shopfront",
    text_region_evidence: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Normalize to Luna evidence types — never location/station facts."""

    if parsed.get("runtime_unavailable"):
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "ocr_runtime_error_candidate",
            "l2_replan_candidate": True,
            "not_silent_fallback_qwen": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if parsed.get("unsupported_claim") or parsed.get("missing_region_support"):
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "unsupported_ocr_claim",
            "text_candidates": parsed.get("text_candidates") or [],
            "reject_reason": "no_text_region_support",
            "validation_status": "rejected",
            "candidate_only": True,
            "not_fact": True,
        }

    candidates = parsed.get("text_candidates") or []
    if not candidates:
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "ocr_empty_candidate",
            "candidate_only": True,
            "not_fact": True,
        }

    primary = candidates[0]
    conf = primary.get("confidence", 0.0)

    if parsed.get("low_confidence") or conf < LOW_CONFIDENCE_THRESHOLD:
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "ocr_low_confidence_candidate",
            "candidate_text": primary.get("candidate_text"),
            "confidence": conf,
            "source_region_id": primary.get("source_region_id"),
            "language": primary.get("language", "zh"),
            "request_more_evidence": True,
            "not_qwen_auto_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if scenario == "metro_direction":
        return {
            "evidence_id": _uid("ev"),
            "evidence_type": "ocr_text_candidate",
            "candidate_text": primary.get("candidate_text"),
            "confidence": conf,
            "source_region_id": primary.get("source_region_id"),
            "language": primary.get("language", "zh"),
            "task_candidate": "find_direction",
            "not_current_station_fact": True,
            "forbidden_output": "current_station",
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "evidence_id": _uid("ev"),
        "evidence_type": "ocr_text_candidate",
        "candidate_text": primary.get("candidate_text"),
        "confidence": conf,
        "source_region_id": primary.get("source_region_id"),
        "language": primary.get("language", "zh"),
        "not_location_fact": True,
        "not_station_name_fact": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_fusion_candidate(
    *,
    ocr_evidence: Dict[str, Any],
    situation: Dict[str, Any],
) -> Dict[str, Any]:
    """Planning stub — fuse OCR candidate with scene context, not fact admission."""
    scene = ((situation or {}).get("scene_profile_candidate") or {}).get("scene_type", "unknown")
    etype = ocr_evidence.get("evidence_type", "")

    if etype != "ocr_text_candidate":
        return {
            "fusion_id": _uid("fus"),
            "fusion_status": "skipped",
            "reason": f"evidence_type={etype}",
            "candidate_only": True,
        }

    fusion_type = "identify_place_candidate" if scene == "shopfront_sign" else "text_scene_fusion_candidate"

    return {
        "fusion_id": _uid("fus"),
        "fusion_type": fusion_type,
        "ocr_text_candidate_ref": ocr_evidence.get("evidence_id"),
        "candidate_text": ocr_evidence.get("candidate_text"),
        "scene_type": scene,
        "not_fact_admission": True,
        "candidate_only": True,
    }
