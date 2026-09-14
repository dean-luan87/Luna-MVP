# -*- coding: utf-8 -*-
"""Document Surface Detector — response parser (planning fixtures) v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    EXECUTION_MODE_PLANNING,
    RUNTIME_ID,
)

PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "stacked_papers": {
        "surfaces": [
            {"surface_id": "paper_A", "bbox": [80, 60, 320, 280], "visibility": "visible", "owner_ref": "paper_A"},
            {"surface_id": "paper_B", "bbox": [140, 120, 380, 340], "visibility": "partial", "owner_ref": "paper_B"},
        ],
        "relations": [
            {"entity_a": "paper_A", "entity_b": "paper_B", "relation_type": "occludes", "evidence_basis": "spatial_overlap"},
        ],
    },
    "stacked_menus": {
        "surfaces": [
            {"surface_id": "menu_A", "bbox": [50, 50, 300, 250], "visibility": "visible", "owner_ref": "menu_A"},
            {"surface_id": "menu_B", "bbox": [120, 100, 350, 300], "visibility": "partial", "owner_ref": "menu_B"},
        ],
        "relations": [
            {"entity_a": "menu_A", "entity_b": "menu_B", "relation_type": "overlaps", "evidence_basis": "stacked_menus"},
        ],
        "next_slot": "text_detection_per_surface",
    },
    "receipt_on_package": {
        "surfaces": [
            {"surface_id": "package_surface", "bbox": [20, 80, 200, 280], "visibility": "visible", "owner_ref": "package_001"},
            {"surface_id": "receipt_surface", "bbox": [30, 200, 150, 280], "visibility": "visible", "owner_ref": "receipt_001"},
        ],
        "relations": [
            {"entity_a": "receipt_surface", "entity_b": "package_surface", "relation_type": "attached_to", "evidence_basis": "spatial_attachment"},
        ],
    },
    "uncertain_boundary": {
        "surfaces": [
            {"surface_id": "doc_uncertain_1", "bbox": [100, 100, 300, 300], "visibility": "uncertain", "owner_ref": "doc_uncertain_1"},
        ],
        "request_more_evidence": True,
    },
    "layout_conflict": {
        "surfaces": [
            {"surface_id": "doc_page_1", "bbox": [0, 0, 400, 500], "visibility": "visible", "owner_ref": "doc_page_1"},
        ],
        "layout_conflict": True,
        "layout_block_count": 4,
    },
    "screen_document": {
        "surfaces": [
            {"surface_id": "tablet_screen", "bbox": [150, 100, 350, 400], "visibility": "visible", "owner_ref": "tablet_screen"},
        ],
        "possible_screen_document": True,
        "not_paper_document": True,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def parse_document_surface_response(
    *,
    fixture_ref: str,
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    """Parse planning fixture into runtime response — NO OCR text."""
    fixture = PLANNING_FIXTURES.get(fixture_ref, PLANNING_FIXTURES["stacked_papers"])

    surfaces: List[Dict[str, Any]] = []
    for s in fixture.get("surfaces") or []:
        surfaces.append({
            "surface_id": s.get("surface_id"),
            "source_region_id": source_region_id,
            "bbox_candidate": s.get("bbox"),
            "boundary_confidence_candidate": 0.85 if s.get("visibility") != "uncertain" else 0.45,
            "visibility_status_candidate": s.get("visibility", "visible"),
            "surface_orientation_candidate": "portrait",
            "owner_entity_candidate_ref": s.get("owner_ref"),
            "candidate_only": True,
            "not_fact": True,
        })

    relations: List[Dict[str, Any]] = []
    for r in fixture.get("relations") or []:
        relations.append({
            "relation_id": _uid("rel"),
            "relation_type_candidate": r.get("relation_type"),
            "entity_a": r.get("entity_a"),
            "entity_b": r.get("entity_b"),
            "evidence_basis": r.get("evidence_basis"),
            "candidate_only": True,
        })

    status = "ok"
    if fixture.get("layout_conflict"):
        status = "detector_conflict_candidate"
    elif fixture.get("possible_screen_document"):
        status = "possible_screen_document_content_candidate"
    elif fixture.get("request_more_evidence"):
        status = "request_more_evidence_candidate"

    return {
        "response_id": _uid("dsresp"),
        "runtime_id": RUNTIME_ID,
        "execution_mode": EXECUTION_MODE_PLANNING,
        "document_surface_candidates": surfaces,
        "relation_hint_candidates": relations,
        "runtime_status_candidate": status,
        "next_slot_suggestion": fixture.get("next_slot"),
        "layout_conflict_detected": fixture.get("layout_conflict", False),
        "possible_screen_document_content": fixture.get("possible_screen_document", False),
        "request_more_evidence": fixture.get("request_more_evidence", False),
        "no_ocr_text": True,
        "candidate_only": True,
        "not_fact": True,
    }
