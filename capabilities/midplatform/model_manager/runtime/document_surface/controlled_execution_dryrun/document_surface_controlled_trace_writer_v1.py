# -*- coding: utf-8 -*-
"""Document Surface — controlled trace writer v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)

IMPLEMENTATION_MODE = "option_a_classical_cv_boundary"
TRACE_REQUIRED = (
    "execution_id", "source_image_ref", "source_region_id", "attention_gate_status",
    "field_context_candidate", "runtime_id", "implementation_mode", "dependency_status",
    "input_boundary_status", "output_boundary_status", "candidate_outputs",
    "validation_status_candidate", "abort_status", "fallback_attempted",
    "ocr_called", "vlm_called", "layout_called", "candidate_only", "not_fact",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_runtime_trace(
    *,
    source_image_ref: Optional[str],
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    field_context_candidate: Optional[Dict[str, Any]] = None,
    dependency_status: str = "cv2_available",
    input_boundary_status: str = "registry_only",
    output_boundary_status: str = "controlled_tmp_only",
    candidate_outputs: Optional[Dict[str, Any]] = None,
    validation_status_candidate: str = "pending_validation",
    abort_status: str = "none",
    abort_reason: Optional[str] = None,
    cv2_processing_executed: bool = False,
    runtime_call_count: int = 1,
    skipped_by_attention_gate: bool = False,
) -> Dict[str, Any]:
    trace = {
        "execution_id": _uid("ex"),
        "source_image_ref": source_image_ref,
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "field_context_candidate": field_context_candidate or {},
        "runtime_id": RUNTIME_ID,
        "implementation_mode": IMPLEMENTATION_MODE,
        "dependency_status": dependency_status,
        "input_boundary_status": input_boundary_status,
        "output_boundary_status": output_boundary_status,
        "candidate_outputs": candidate_outputs or {},
        "validation_status_candidate": validation_status_candidate,
        "abort_status": abort_status,
        "abort_reason_candidate": abort_reason,
        "fallback_attempted": False,
        "ocr_called": False,
        "vlm_called": False,
        "layout_called": False,
        "cv2_processing_executed": cv2_processing_executed,
        "runtime_call_count": runtime_call_count,
        "skipped_by_attention_gate": skipped_by_attention_gate,
        "candidate_only": True,
        "not_fact": True,
    }
    trace["trace_complete"] = all(k in trace for k in TRACE_REQUIRED)
    return trace
