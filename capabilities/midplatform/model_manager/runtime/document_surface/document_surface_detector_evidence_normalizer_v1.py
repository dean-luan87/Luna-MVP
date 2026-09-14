# -*- coding: utf-8 -*-
"""Document Surface Detector — evidence normalizer v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def normalize_document_surface_evidence(
    *,
    request: Dict[str, Any],
    response: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize runtime response → Ownership Evidence Package + text owner assignment candidates.
    Surface candidate BEFORE text owner assignment. NO OCR text.
    """
    surfaces = response.get("document_surface_candidates") or []
    relations = response.get("relation_hint_candidates") or []

    text_owner_candidates: List[Dict[str, Any]] = []
    for s in surfaces:
        text_owner_candidates.append({
            "assignment_id": _uid("toa"),
            "surface_id": s.get("surface_id"),
            "owner_entity_candidate_ref": s.get("owner_entity_candidate_ref"),
            "assignment_status": "surface_bound_candidate",
            "text_content": None,
            "no_ocr_text": True,
            "candidate_only": True,
            "not_fact": True,
        })

    validation_status = "pending_validation"
    if response.get("layout_conflict_detected"):
        validation_status = "validation_review"
    elif response.get("possible_screen_document_content"):
        validation_status = "defer_to_screen_surface_detector"
    elif response.get("request_more_evidence"):
        validation_status = "request_more_evidence"

    return {
        "ownership_evidence_package": {
            "package_id": _uid("oep"),
            "source_region_id": request.get("source_region_id"),
            "attention_gate_status": request.get("attention_gate_status", "allowed"),
            "document_surface_candidates": surfaces,
            "relation_hint_candidates": relations,
            "entity_candidates": [
                {
                    "entity_id": s.get("owner_entity_candidate_ref"),
                    "entity_type_candidate": "document_surface",
                    "source_runtime": "document_surface_detector_v1",
                    "candidate_only": True,
                    "not_fact": True,
                }
                for s in surfaces
            ],
            "text_owner_assignment_candidates": text_owner_candidates,
            "next_slot_suggestion": response.get("next_slot_suggestion"),
            "validation_status_candidate": validation_status,
            "candidate_only": True,
            "not_fact": True,
        },
        "surface_candidate_before_text_owner": True,
        "no_ocr_text_output": True,
        "no_merge_overlapped_documents": len(surfaces) >= 1,
        "runtime_does_not_override_ownership_graph": True,
        "candidate_only_not_fact": True,
    }
