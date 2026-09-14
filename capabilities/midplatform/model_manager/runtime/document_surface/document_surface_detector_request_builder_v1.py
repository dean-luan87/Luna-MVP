# -*- coding: utf-8 -*-
"""Document Surface Detector — request builder v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    ALLOWED_CAPABILITIES,
    CAPABILITY,
    FORBIDDEN_CAPABILITIES,
    RUNTIME_ID,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_document_surface_request(
    *,
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    goal_context: Optional[Dict[str, Any]] = None,
    region_crop_ref: str = "",
    fixture_ref: str = "stacked_papers",
) -> Dict[str, Any]:
    """Build runtime request — attention gate required, no OCR in request."""
    if attention_gate_status == "blocked":
        return {
            "request_id": _uid("dsr"),
            "source_region_id": source_region_id,
            "attention_gate_status": "blocked",
            "skipped_by_attention_gate": True,
            "runtime_call_count": 0,
            "candidate_only": True,
        }

    return {
        "request_id": _uid("dsr"),
        "runtime_id": RUNTIME_ID,
        "capability": CAPABILITY,
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "goal_context": goal_context or {},
        "region_crop_ref": region_crop_ref or f"crop_{source_region_id}",
        "fixture_ref": fixture_ref,
        "allowed_capabilities": list(ALLOWED_CAPABILITIES),
        "forbidden_capabilities": list(FORBIDDEN_CAPABILITIES),
        "run_ocr": False,
        "run_vlm": False,
        "candidate_only": True,
    }
