# -*- coding: utf-8 -*-
"""Document Surface Detector — planning adapter v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_evidence_normalizer_v1 import (
    normalize_document_surface_evidence,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    match_capability_for_document_surface,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_request_builder_v1 import (
    build_document_surface_request,
)
from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_response_parser_v1 import (
    parse_document_surface_response,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_DOCUMENT_SURFACE_DETECTOR_REAL_RUNTIME_INTEGRATION_PLANNING_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_document_surface_detector_planning(
    *,
    fixture_ref: str = "stacked_papers",
    source_region_id: str = "region_001",
    attention_gate_status: str = "allowed",
    goal_context: Optional[Dict[str, Any]] = None,
    runtime_unavailable: bool = False,
) -> Dict[str, Any]:
    """
    Planning pipeline:
    Attention-Gated Region → Capability Match → Request → Response → Evidence → Validation
    """
    if runtime_unavailable:
        return {
            "planning_only": True,
            "fixture_ref": fixture_ref,
            "document_surface_runtime_error_candidate": {
                "error_id": _uid("dsre"),
                "error_type": "document_surface_runtime_unavailable",
                "handoff_to": "L2_or_attention_replan",
                "candidate_only": True,
            },
            "no_silent_fallback_to_ocr": True,
            "no_silent_fallback_to_vlm": True,
            "no_full_scene_segmentation_fallback": True,
            "failure_returns_runtime_error_candidate": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    if attention_gate_status == "blocked":
        request = build_document_surface_request(
            source_region_id=source_region_id,
            attention_gate_status="blocked",
            fixture_ref=fixture_ref,
        )
        return {
            "planning_only": True,
            "fixture_ref": fixture_ref,
            "capability_match": match_capability_for_document_surface(attention_gate_status="blocked"),
            "runtime_request": request,
            "skipped_by_attention_gate": True,
            "runtime_call_count": 0,
            "no_surface_candidates": True,
            "attention_gate_required": True,
            "governance_loop_complete": True,
            "candidate_only": True,
            "not_fact": True,
        }

    match = match_capability_for_document_surface(attention_gate_status=attention_gate_status)
    request = build_document_surface_request(
        source_region_id=source_region_id,
        attention_gate_status=attention_gate_status,
        fixture_ref=fixture_ref,
        goal_context=goal_context,
    )
    response = parse_document_surface_response(fixture_ref=fixture_ref, source_region_id=source_region_id)
    evidence = normalize_document_surface_evidence(request=request, response=response)

    pkg = evidence.get("ownership_evidence_package") or {}

    return {
        "planning_only": True,
        "fixture_ref": fixture_ref,
        "capability_match": match,
        "runtime_request": request,
        "runtime_response": response,
        "ownership_evidence_package": pkg,
        "evidence_normalization": evidence,
        "runtime_call_count": 1,
        "no_ocr_text_output": evidence.get("no_ocr_text_output") is True,
        "surface_before_text_owner": evidence.get("surface_candidate_before_text_owner") is True,
        "attention_gate_required": True,
        "no_global_ocr": True,
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }
