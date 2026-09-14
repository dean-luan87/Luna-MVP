# -*- coding: utf-8 -*-
"""OCR controlled execution record builders — execution / error / result envelope."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_ocr_execution_id(candidate_id: str) -> str:
    return f"rex_ocr_{candidate_id}_{uuid4().hex[:8]}"


def build_ocr_execution_record(
    *,
    ocr_execution_id: str,
    source_ocr_execution_candidate_id: str,
    runner_name: str,
    runner_version: str,
    status: str,
    input_ref: str,
    output_ref: str = "",
    error_ref: str = "",
    trace_chain: Optional[List[Dict[str, str]]] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "ocr_execution_id": ocr_execution_id,
        "source_ocr_execution_candidate_id": source_ocr_execution_candidate_id,
        "runner_name": runner_name,
        "runner_version": runner_version,
        "execution_mode": "manual_controlled",
        "status": status,
        "started_at": start_time or _now(),
        "ended_at": end_time or _now(),
        "input_ref": input_ref,
        "output_ref": output_ref,
        "error_ref": error_ref,
        "trace_chain": trace_chain or [],
        "completed_not_fact": True,
        "not_fact": True,
        "candidate_only": True,
    }


def build_ocr_result_layer_record(
    *,
    ocr_result_envelope: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "result_type": "ocr_result_envelope",
        "source_execution_id": ocr_result_envelope.get("source_ocr_execution_id"),
        "source_execution_candidate_id": ocr_result_envelope.get("source_ocr_execution_candidate_id"),
        "source_region_id": ocr_result_envelope.get("source_region_id"),
        "payload_ref": ocr_result_envelope.get("output_payload_ref"),
        "confidence": ocr_result_envelope.get("confidence"),
        "model_source": ocr_result_envelope.get("model_name"),
        "model_version": ocr_result_envelope.get("model_version"),
        "text_candidate_list": ocr_result_envelope.get("text_candidate_list", []),
        "text_region_candidate": ocr_result_envelope.get("text_region_candidate"),
        "reading_order_candidate": ocr_result_envelope.get("reading_order_candidate", []),
        "needs_fact_admission": True,
        "not_fact": True,
        "candidate_only": True,
        "trace_chain": ocr_result_envelope.get("trace_chain", []),
        "result_layer_not_observation_layer": True,
        "ocr_result_not_fact": True,
    }
