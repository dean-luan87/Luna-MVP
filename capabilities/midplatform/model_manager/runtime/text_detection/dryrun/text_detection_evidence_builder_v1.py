# -*- coding: utf-8 -*-
"""Text Detection Evidence Builder — runtime output → governed evidence v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_response_parser_v1 import (
    parse_text_detection_response,
)
from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_evidence_normalizer_v1 import (
    normalize_text_detection_evidence,
)

FORBIDDEN_DETECTOR_FIELDS = frozenset({"text", "place_name", "shop_name", "station_name"})


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_text_detection_evidence(
    *,
    execution: Dict[str, Any],
    scenario: str = "shopfront",
    provider_id: str = "paddleocr_detector_v1",
) -> Dict[str, Any]:
    """Build evidence package — detector never outputs recognized text."""
    if execution.get("runtime_error_candidate"):
        return {
            "evidence_id": _uid("ev"),
            "slot_id": "slot_1",
            "evidence_type": "runtime_error_candidate",
            "error_code": execution.get("error_code"),
            "provider_id": provider_id,
            "candidate_only": True,
            "not_fact": True,
        }

    raw = execution.get("raw_output") or {}
    parsed = parse_text_detection_response(raw, provider_id=provider_id)
    evidence = normalize_text_detection_evidence(parsed=parsed, scenario=scenario)
    evidence["slot_id"] = "slot_1"
    evidence["provider_id"] = provider_id
    evidence["provider_execution_id"] = execution.get("provider_execution_id")

    payload = evidence.get("regions") or []
    for region in payload:
        for forbidden in FORBIDDEN_DETECTOR_FIELDS:
            if forbidden in region:
                region.pop(forbidden, None)

    evidence["detector_output_has_no_text"] = not any(
        forbidden in str(evidence) for forbidden in FORBIDDEN_DETECTOR_FIELDS
    )
    if evidence.get("evidence_type") == "text_region_candidate" and payload:
        evidence["region_type"] = "text_region_candidate"
        evidence["confidence"] = payload[0].get("confidence")

    return evidence


def assert_no_recognized_text(evidence: Dict[str, Any]) -> bool:
    """Case A guard — detector must not output OCR text."""
    blob = str(evidence)
    return not any(f'"{f}"' in blob or f"'{f}'" in blob for f in ("阿叔阿姨的店", "嘉会湖站", "Starbucks"))
