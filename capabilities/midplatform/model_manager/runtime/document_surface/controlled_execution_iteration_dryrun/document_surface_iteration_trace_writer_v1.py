# -*- coding: utf-8 -*-
"""Document Surface — iteration trace writer v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

RUNTIME_ID = "document_surface_detector_v1"
IMPLEMENTATION_MODE = "option_a_classical_cv_boundary_iteration_v1"


def build_iteration_trace(
    *,
    source_image_ref: Optional[str],
    category: str,
    candidate_outputs: Dict[str, Any],
    iteration_layer_applied: bool = True,
    cv2_processing_executed: bool = True,
) -> Dict[str, Any]:
    return {
        "execution_id": f"itex_{uuid4().hex[:10]}",
        "source_image_ref": source_image_ref,
        "source_region_id": "region_001",
        "attention_gate_status": "allowed",
        "runtime_id": RUNTIME_ID,
        "implementation_mode": IMPLEMENTATION_MODE,
        "iteration_strategy_layer": iteration_layer_applied,
        "category": category,
        "dependency_status": "cv2_available",
        "input_boundary_status": "iteration_registry_only",
        "output_boundary_status": "controlled_tmp_only",
        "candidate_outputs": candidate_outputs,
        "validation_status_candidate": "pending_validation",
        "abort_status": "none",
        "fallback_attempted": False,
        "ocr_called": False,
        "vlm_called": False,
        "layout_called": False,
        "cv2_processing_executed": cv2_processing_executed,
        "candidate_only": True,
        "not_fact": True,
        "trace_complete": True,
    }
