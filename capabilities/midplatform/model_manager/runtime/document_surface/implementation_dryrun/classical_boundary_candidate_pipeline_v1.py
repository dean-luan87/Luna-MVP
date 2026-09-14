# -*- coding: utf-8 -*-
"""Classical Boundary Candidate Pipeline — deterministic fixture v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_contract_v1 import (
    FIRST_IMPLEMENTATION_MODE,
)
from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_fixture_v1 import (
    OPTION_A_FIXTURES,
)

# Explicitly no cv2 — planning/dryrun only
CV2_IMPORTED = False


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_classical_boundary_candidate_pipeline(
    *,
    fixture_ref: str,
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    """
    Classical CV boundary candidate pipeline — deterministic fixture simulation.
    Simulates edge/contour/quadrilateral/polygon without cv2 or real images.
    """
    fixture = OPTION_A_FIXTURES.get(fixture_ref, OPTION_A_FIXTURES["single_flat_paper"])

    edge_candidate = {
        "edge_id": _uid("edge"),
        "edge_count_candidate": fixture.get("edge_count", 4),
        "source_region_id": source_region_id,
        "candidate_only": True,
        "not_fact": True,
    }

    contour_candidate = {
        "contour_id": _uid("ctr"),
        "contour_type_candidate": fixture.get("contour_type"),
        "closed": True,
        "candidate_only": True,
        "not_fact": True,
    }

    quadrilateral_candidate = None
    if fixture.get("quadrilateral"):
        q = fixture["quadrilateral"]
        quadrilateral_candidate = {
            "quad_id": _uid("quad"),
            "vertices_candidate": [[q[i], q[i + 1]] for i in range(0, len(q), 2)],
            "candidate_only": True,
            "not_fact": True,
        }

    polygon_candidate = None
    if fixture.get("polygon"):
        polygon_candidate = {
            "polygon_id": _uid("poly"),
            "vertices_candidate": fixture["polygon"],
            "uncertain_boundary": fixture.get("contour_type") == "polygon_uncertain",
            "candidate_only": True,
            "not_fact": True,
        }

    boundary_quality_candidate = {
        "quality_id": _uid("bq"),
        "boundary_confidence_candidate": fixture.get("boundary_quality", 0.5),
        "low_contrast": fixture.get("low_contrast", False),
        "candidate_only": True,
        "not_fact": True,
    }

    surfaces: List[Dict[str, Any]] = []
    for s in fixture.get("surfaces") or []:
        vis = s.get("visibility", fixture.get("visibility", "visible"))
        surf = {
            "surface_id": s.get("surface_id"),
            "source_region_id": source_region_id,
            "bbox_candidate": s.get("bbox"),
            "polygon_candidate": fixture.get("polygon") if vis == "uncertain" else None,
            "boundary_confidence_candidate": fixture.get("boundary_quality", 0.5),
            "visibility_status_candidate": vis,
            "surface_orientation_candidate": "portrait",
            "owner_entity_candidate_ref": s.get("owner_ref"),
            "source_runtime": RUNTIME_ID,
            "implementation_mode_candidate": FIRST_IMPLEMENTATION_MODE,
            "candidate_only": True,
            "not_fact": True,
        }
        if fixture.get("low_contrast"):
            surf["low_contrast_boundary_candidate"] = True
        surfaces.append(surf)

    relations: List[Dict[str, Any]] = []
    for r in fixture.get("relations") or []:
        relations.append({
            "relation_id": _uid("rel"),
            "relation_type_candidate": r.get("relation_type"),
            "entity_a": r.get("entity_a"),
            "entity_b": r.get("entity_b"),
            "evidence_basis": r.get("evidence_basis"),
            "source_runtime": RUNTIME_ID,
            "implementation_mode_candidate": FIRST_IMPLEMENTATION_MODE,
            "candidate_only": True,
            "not_fact": True,
        })

    status = "ok"
    if fixture.get("possible_screen_document"):
        status = "possible_screen_document_content_candidate"
    elif fixture.get("request_more_evidence"):
        status = "request_more_evidence_candidate"
    elif fixture.get("low_contrast"):
        status = "low_contrast_boundary_candidate"

    return {
        "pipeline_id": _uid("cbp"),
        "implementation_mode_candidate": FIRST_IMPLEMENTATION_MODE,
        "edge_candidate": edge_candidate,
        "contour_candidate": contour_candidate,
        "quadrilateral_candidate": quadrilateral_candidate,
        "polygon_candidate": polygon_candidate,
        "perspective_surface_candidate": quadrilateral_candidate,
        "boundary_quality_candidate": boundary_quality_candidate,
        "document_surface_candidates": surfaces,
        "relation_hint_candidates": relations,
        "runtime_status_candidate": status,
        "possible_screen_document_content": fixture.get("possible_screen_document", False),
        "low_contrast_boundary": fixture.get("low_contrast", False),
        "request_more_evidence_candidate": fixture.get("request_more_evidence", False),
        "no_cv2_import": not CV2_IMPORTED,
        "no_real_image_read": True,
        "candidate_only": True,
        "not_fact": True,
    }
