# -*- coding: utf-8 -*-
"""OCR Recognition Runtime Adapter — text_region → ocr_text_candidate v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_evidence_normalizer_v1 import (
    build_fusion_candidate,
    normalize_text_recognition_evidence,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_request_builder_v1 import (
    build_text_recognition_request,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_response_parser_v1 import (
    parse_text_recognition_response,
)
from capabilities.midplatform.model_manager.runtime.text_recognition.text_recognition_runtime_metrics_v1 import (
    get_ocr_runtime_metrics,
    record_ocr_latency,
    record_ocr_region_attempt,
    record_ocr_runtime_error,
    record_ocr_slot_selected,
)

# Planning fixtures — stand in for PaddleOCR Recognition until DryRun
PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "shopfront_ashu": {
        "text_candidates": [
            {
                "candidate_text": "阿叔阿姨的店",
                "confidence": 0.91,
                "source_region_id": "region_001",
                "language": "zh",
            }
        ],
    },
    "metro_jiahui_direction": {
        "text_candidates": [
            {
                "candidate_text": "开往 嘉会湖",
                "confidence": 0.87,
                "source_region_id": "region_001",
                "language": "zh",
            }
        ],
    },
    "blurry_partial": {
        "text_candidates": [
            {
                "candidate_text": "阿叔阿姨的...",
                "confidence": 0.42,
                "source_region_id": "region_001",
                "language": "zh",
            }
        ],
        "low_confidence": True,
    },
    "hallucination_no_region": {
        "text_candidates": [
            {
                "candidate_text": "Starbucks",
                "confidence": 0.9,
                "source_region_id": None,
                "language": "en",
            }
        ],
        "unsupported_claim": True,
    },
    "runtime_unavailable": {
        "runtime_unavailable": True,
    },
    "damaged_text": {
        "text_candidates": [
            {
                "candidate_text": "阿叔阿?的店",
                "confidence": 0.55,
                "source_region_id": "region_001",
                "language": "zh",
            }
        ],
        "low_confidence": True,
    },
    "starbucks_text": {
        "text_candidates": [
            {
                "candidate_text": "STARBUCKS",
                "confidence": 0.92,
                "source_region_id": "region_001",
                "language": "en",
            }
        ],
    },
    "artistic_hotpot_fail": {
        "text_candidates": [],
        "low_confidence": True,
    },
    "coffee_wrong_ocr": {
        "text_candidates": [
            {
                "candidate_text": "Xx咖啡",
                "confidence": 0.38,
                "source_region_id": "region_001",
                "language": "zh",
            }
        ],
        "low_confidence": True,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def invoke_text_recognition_runtime(
    *,
    request: Dict[str, Any],
    fixture_key: str = "shopfront_ashu",
    planning_only: bool = True,
) -> Dict[str, Any]:
    """Planning stub — real PaddleOCR Recognition deferred to DryRun."""
    raw = PLANNING_FIXTURES.get(fixture_key, PLANNING_FIXTURES["shopfront_ashu"])
    return {
        "execution_id": _uid("ocr"),
        "request_id": request.get("request_id"),
        "provider_id": request.get("provider_id"),
        "raw_response": raw,
        "planning_fixture": fixture_key,
        "real_inference": not planning_only,
        "planning_only": planning_only,
        "recognition_only": True,
        "candidate_only": True,
    }


def run_text_recognition_slot(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    text_region_evidence: Dict[str, Any],
    fixture_key: str = "shopfront_ashu",
    scenario: str = "shopfront",
    provider_id: str = "paddleocr_recognizer_v1",
) -> Dict[str, Any]:
    """
    Full slot_2 pipeline:
    text_region_candidate → Collaboration Slot → MM Binding → Runtime → Normalizer → Fusion
    """
    record_ocr_slot_selected()
    request = build_text_recognition_request(
        text_region_evidence=text_region_evidence,
        plan=plan,
        provider_id=provider_id,
    )
    runtime_result = invoke_text_recognition_runtime(request=request, fixture_key=fixture_key)
    raw = runtime_result.get("raw_response") or {}

    if raw.get("runtime_unavailable"):
        record_ocr_runtime_error()
        record_ocr_region_attempt(success=False)

    parsed = parse_text_recognition_response(
        raw,
        provider_id=provider_id,
        source_region_ids=request.get("source_region_ids"),
    )
    evidence = normalize_text_recognition_evidence(
        parsed=parsed,
        scenario=scenario,
        text_region_evidence=text_region_evidence,
    )

    etype = evidence.get("evidence_type", "")
    if etype == "ocr_text_candidate":
        record_ocr_region_attempt(success=True)
    elif etype == "ocr_low_confidence_candidate":
        record_ocr_region_attempt(success=False, low_confidence=True)
    elif etype == "unsupported_ocr_claim":
        record_ocr_region_attempt(success=False, unsupported=True)

    record_ocr_latency(latency_ms=12.5, cost_units=0.001)
    fusion = build_fusion_candidate(ocr_evidence=evidence, situation=situation)
    validation = _build_validation_stub(evidence)

    return {
        "slot_id": "slot_2",
        "capability": "text_recognition",
        "provider_id": provider_id,
        "upstream_evidence_type": text_region_evidence.get("evidence_type"),
        "runtime_request": request,
        "runtime_result": runtime_result,
        "parsed_response": parsed,
        "evidence_package": evidence,
        "fusion_candidate": fusion,
        "validation_review": validation,
        "recognition_not_detection": request.get("run_detection") is False,
        "not_full_image_ocr": request.get("not_full_image_ocr") is True,
        "ocr_runtime_metrics": get_ocr_runtime_metrics(),
        "candidate_only": True,
        "not_fact": True,
    }


def _build_validation_stub(evidence: Dict[str, Any]) -> Dict[str, Any]:
    etype = evidence.get("evidence_type", "")
    if etype == "unsupported_ocr_claim":
        status = "rejected"
    elif etype == "ocr_low_confidence_candidate":
        status = "request_more_evidence"
    elif etype == "ocr_runtime_error_candidate":
        status = "runtime_error_acknowledged"
    elif etype == "ocr_text_candidate":
        status = "accepted_as_text_candidate"
    else:
        status = "pending_review"
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
    }
