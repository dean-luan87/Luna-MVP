# -*- coding: utf-8 -*-
"""Document Surface — real runtime implementation contract v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    ALLOWED_CAPABILITIES,
    FORBIDDEN_CAPABILITIES,
    RUNTIME_ID,
)

FIRST_IMPLEMENTATION_MODE = "classical_cv_boundary_v1"

INPUT_REQUIRED = (
    "source_region_id",
    "attention_gate_status",
    "goal_context",
    "allowed_capabilities",
    "forbidden_capabilities",
    "candidate_only",
)

OUTPUT_REQUIRED = (
    "runtime_id",
    "implementation_mode_candidate",
    "document_surface_candidates",
    "relation_hint_candidates",
    "runtime_status_candidate",
    "candidate_only",
    "not_fact",
)

SURFACE_CANDIDATE_REQUIRED = (
    "surface_id",
    "source_region_id",
    "visibility_status_candidate",
    "owner_entity_candidate_ref",
    "source_runtime",
    "implementation_mode_candidate",
    "candidate_only",
    "not_fact",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_implementation_input_contract(
    *,
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    image_region_ref: str = "",
    crop_path_ref: str = "",
    goal_context: Optional[Dict[str, Any]] = None,
    field_context_candidate: Optional[Dict[str, Any]] = None,
    max_runtime_cost: str = "low",
) -> Dict[str, Any]:
    """Implementation Input Contract — planning only, no image execution."""
    return {
        "contract_id": _uid("dsic_in"),
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "image_region_ref": image_region_ref or f"region_ref_{source_region_id}",
        "crop_path_ref": crop_path_ref or f"crop_ref_{source_region_id}",
        "goal_context": goal_context or {},
        "field_context_candidate": field_context_candidate or {},
        "allowed_capabilities": list(ALLOWED_CAPABILITIES),
        "forbidden_capabilities": list(FORBIDDEN_CAPABILITIES),
        "max_runtime_cost": max_runtime_cost,
        "candidate_only": True,
        "planning_only": True,
    }


def build_implementation_output_contract(
    *,
    source_region_id: str = "region_001",
    implementation_mode: str = FIRST_IMPLEMENTATION_MODE,
    surfaces: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Implementation Output Contract — schema-aligned planning sample."""
    surface_list = surfaces or [{
        "surface_id": "surface_plan_001",
        "source_region_id": source_region_id,
        "bbox_candidate": [10, 10, 200, 300],
        "boundary_confidence_candidate": 0.78,
        "visibility_status_candidate": "visible",
        "surface_orientation_candidate": "portrait",
        "owner_entity_candidate_ref": "surface_plan_001",
        "source_runtime": RUNTIME_ID,
        "implementation_mode_candidate": implementation_mode,
        "candidate_only": True,
        "not_fact": True,
    }]
    return {
        "contract_id": _uid("dsic_out"),
        "runtime_id": RUNTIME_ID,
        "implementation_mode_candidate": implementation_mode,
        "document_surface_candidates": surface_list,
        "relation_hint_candidates": [],
        "runtime_status_candidate": "planning_contract_sample",
        "error_candidate": None,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }


def validate_contract_alignment(
    *,
    input_contract: Dict[str, Any],
    output_contract: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate implementation contract vs dryrun schema alignment."""
    in_missing = [k for k in INPUT_REQUIRED if k not in input_contract]
    out_missing = [k for k in OUTPUT_REQUIRED if k not in output_contract]
    surfaces = output_contract.get("document_surface_candidates") or []
    surface_ok = all(
        all(k in s for k in SURFACE_CANDIDATE_REQUIRED)
        and (s.get("bbox_candidate") or s.get("polygon_candidate"))
        for s in surfaces
    )
    return {
        "input_complete": not in_missing,
        "output_complete": not out_missing,
        "surface_candidate_schema_ok": surface_ok,
        "candidate_only_preserved": (
            input_contract.get("candidate_only") is True
            and output_contract.get("candidate_only") is True
            and output_contract.get("not_fact") is True
        ),
        "runtime_id_aligned": output_contract.get("runtime_id") == RUNTIME_ID,
        "aligned_with_dryrun": not in_missing and not out_missing and surface_ok,
        "failures": in_missing + out_missing,
    }
