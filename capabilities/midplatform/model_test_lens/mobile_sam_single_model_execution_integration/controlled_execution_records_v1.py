# -*- coding: utf-8 -*-
"""Controlled execution record builders — execution / error / result envelope."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_runner_execution_record(
    *,
    execution_id: str,
    source_execution_candidate_id: str,
    model_name: str,
    model_version: str,
    status: str,
    input_ref: str,
    output_ref: str,
    trace_chain: List[Dict[str, str]],
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "execution_id": execution_id,
        "source_execution_candidate_id": source_execution_candidate_id,
        "model_name": model_name,
        "model_version": model_version,
        "start_time": start_time or _now(),
        "end_time": end_time or _now(),
        "status": status,
        "input_ref": input_ref,
        "output_ref": output_ref,
        "trace_chain": trace_chain,
        "runner_execution_completed_not_fact": status == "completed",
        "not_fact": True,
        "candidate_only": True,
    }


def build_runner_error_candidate(
    *,
    execution_id: str,
    error_type: str,
    error_stage: str,
    error_reason: str,
    source_execution_candidate_id: str,
    trace_chain: List[Dict[str, str]],
    recoverable: bool = False,
) -> Dict[str, Any]:
    return {
        "envelope_type": "runner_error_candidate",
        "execution_id": execution_id,
        "source_execution_candidate_id": source_execution_candidate_id,
        "error_type": error_type,
        "error_stage": error_stage,
        "error_reason": error_reason,
        "recoverable": recoverable,
        "trace_chain": trace_chain,
        "not_fact": True,
        "runner_error_not_fact": True,
        "candidate_only": True,
    }


def build_result_envelope_record(
    *,
    source_execution_id: str,
    source_execution_candidate_id: str,
    result_type: str,
    payload_ref: str,
    confidence: float,
    trace_chain: List[Dict[str, str]],
    mask_ref: Optional[str] = None,
    model_source: str = "MobileSAM",
    model_version: str = "mobile_sam_v1",
) -> Dict[str, Any]:
    return {
        "source_execution_id": source_execution_id,
        "source_execution_candidate_id": source_execution_candidate_id,
        "result_type": result_type,
        "payload_ref": payload_ref,
        "mask_ref": mask_ref or payload_ref,
        "confidence": confidence,
        "model_source": model_source,
        "model_version": model_version,
        "needs_fact_admission": True,
        "not_fact": True,
        "candidate_only": True,
        "trace_chain": trace_chain,
        "result_layer_not_observation_layer": True,
        "result_layer_not_segmentation_owner": True,
    }
