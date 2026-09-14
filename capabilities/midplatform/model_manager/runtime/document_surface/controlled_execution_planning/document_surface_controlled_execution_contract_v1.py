# -*- coding: utf-8 -*-
"""Document Surface — controlled execution contract v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    build_implementation_input_contract,
    build_implementation_output_contract,
    validate_contract_alignment,
)

IMPLEMENTATION_MODE = "option_a_classical_cv_boundary"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_controlled_execution_input_contract(
    *,
    source_region_id: str = "region_001",
    source_image_ref: str = "single_flat_paper_controlled.png",
    attention_gate_status: str = "allowed",
    field_context_candidate: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    base = build_implementation_input_contract(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
        field_context_candidate=field_context_candidate,
    )
    return {
        **base,
        "contract_id": _uid("ceic"),
        "source_image_ref": source_image_ref,
        "controlled_execution_only": True,
        "cv2_import_forbidden_in_planning": True,
        "candidate_only": True,
        "planning_only": True,
    }


def build_controlled_execution_trace_template(
    *,
    source_image_ref: str = "single_flat_paper_controlled.png",
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    return {
        "execution_id": _uid("ex"),
        "source_image_ref": source_image_ref,
        "source_region_id": source_region_id,
        "attention_gate_status": "allowed",
        "field_context_candidate": {},
        "runtime_id": RUNTIME_ID,
        "implementation_mode": IMPLEMENTATION_MODE,
        "dependency_status": "pending_controlled_execution",
        "input_boundary_status": "registry_only",
        "output_boundary_status": "controlled_tmp_only",
        "candidate_outputs": {},
        "validation_status_candidate": "pending_validation",
        "abort_status": "none",
        "fallback_attempted": False,
        "ocr_called": False,
        "vlm_called": False,
        "layout_called": False,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }


def validate_controlled_contract_alignment() -> Dict[str, Any]:
    inp = build_controlled_execution_input_contract()
    out = build_implementation_output_contract(implementation_mode="classical_cv_boundary_v1")
    alignment = validate_contract_alignment(input_contract=inp, output_contract=out)
    return {
        "aligned_with_implementation_contract": alignment.get("aligned_with_dryrun") is True,
        "controlled_image_ref_present": "source_image_ref" in inp,
        "trace_template_valid": True,
        "candidate_only": True,
    }
