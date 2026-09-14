# -*- coding: utf-8 -*-
"""Text Detection Runtime Adapter — Collaboration Slot → Real Runtime v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_evidence_normalizer_v1 import (
    normalize_text_detection_evidence,
)
from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_request_builder_v1 import (
    build_text_detection_request,
)
from capabilities.midplatform.model_manager.runtime.text_detection.text_detection_response_parser_v1 import (
    parse_text_detection_response,
)

# Deterministic planning fixtures — stand in for real PaddleOCR until DryRun
PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "shopfront_ashu": {
        "boxes": [{"bbox": [120, 80, 340, 160], "confidence": 0.91, "polygon": None}],
    },
    "metro_jiahui": {
        "boxes": [{"bbox": [50, 200, 400, 260], "confidence": 0.88, "polygon": None}],
    },
    "no_text": {"no_text": True, "boxes": []},
    "low_confidence_texture": {
        "boxes": [{"bbox": [10, 10, 100, 50], "confidence": 0.22}],
        "low_confidence": True,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def invoke_text_detection_runtime(
    *,
    request: Dict[str, Any],
    fixture_key: str = "shopfront_ashu",
    planning_only: bool = True,
) -> Dict[str, Any]:
    """Planning stub — real PaddleOCR deferred to DryRun."""
    raw = PLANNING_FIXTURES.get(fixture_key, PLANNING_FIXTURES["shopfront_ashu"])
    return {
        "execution_id": _uid("tex"),
        "request_id": request.get("request_id"),
        "provider_id": request.get("provider_id"),
        "raw_response": raw,
        "planning_fixture": fixture_key,
        "real_inference": not planning_only,
        "planning_only": planning_only,
        "candidate_only": True,
    }


def run_text_detection_slot(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    fixture_key: str = "shopfront_ashu",
    scenario: str = "shopfront",
    provider_id: str = "paddleocr_detector_v1",
) -> Dict[str, Any]:
    """
    Full slot_1 pipeline:
    Collaboration Slot → MM Binding → Runtime → Normalizer → Evidence Package
    """
    request = build_text_detection_request(
        situation=situation,
        plan=plan,
        provider_id=provider_id,
    )
    runtime_result = invoke_text_detection_runtime(request=request, fixture_key=fixture_key)
    parsed = parse_text_detection_response(
        runtime_result.get("raw_response") or {},
        provider_id=provider_id,
    )
    evidence = normalize_text_detection_evidence(parsed=parsed, scenario=scenario)

    validation = _build_validation_stub(evidence)

    return {
        "slot_id": "slot_1",
        "capability": "text_detection",
        "provider_id": provider_id,
        "runtime_request": request,
        "runtime_result": runtime_result,
        "parsed_response": parsed,
        "evidence_package": evidence,
        "validation_review": validation,
        "l2_plan_unchanged": True,
        "detector_not_auto_ocr": evidence.get("next_slot_candidate") is not None or evidence.get("no_forced_ocr"),
        "candidate_only": True,
        "not_fact": True,
    }


def _build_validation_stub(evidence: Dict[str, Any]) -> Dict[str, Any]:
    etype = evidence.get("evidence_type", "")
    if etype == "low_confidence_text_candidate":
        status = "requires_validation_before_ocr"
    elif etype == "no_text_candidate":
        status = "no_text_acknowledged"
    else:
        status = "accepted_as_region_candidate"
    return {
        "validation_id": _uid("val"),
        "validation_status": status,
        "not_fact_admission": True,
        "candidate_only": True,
    }
