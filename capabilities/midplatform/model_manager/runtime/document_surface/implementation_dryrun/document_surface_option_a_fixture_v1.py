# -*- coding: utf-8 -*-
"""Option A — deterministic fixture definitions v1."""

from __future__ import annotations

from typing import Any, Dict

OPTION_A_FIXTURES: Dict[str, Dict[str, Any]] = {
    "single_flat_paper": {
        "edge_count": 4,
        "contour_type": "closed_quadrilateral",
        "quadrilateral": [10, 10, 290, 10, 290, 410, 10, 410],
        "visibility": "visible",
        "boundary_quality": 0.92,
        "surfaces": [
            {"surface_id": "paper_flat_1", "bbox": [10, 10, 290, 410], "owner_ref": "paper_flat_1"},
        ],
        "relations": [],
    },
    "two_overlapping_papers": {
        "edge_count": 8,
        "contour_type": "multi_contour",
        "quadrilateral": None,
        "visibility": "partial",
        "boundary_quality": 0.78,
        "surfaces": [
            {"surface_id": "paper_A", "bbox": [80, 60, 320, 280], "owner_ref": "paper_A", "visibility": "visible"},
            {"surface_id": "paper_B", "bbox": [140, 120, 380, 340], "owner_ref": "paper_B", "visibility": "partial"},
        ],
        "relations": [
            {"entity_a": "paper_A", "entity_b": "paper_B", "relation_type": "occludes", "evidence_basis": "spatial_overlap"},
        ],
    },
    "folded_or_curved_paper": {
        "edge_count": 6,
        "contour_type": "polygon_uncertain",
        "polygon": [[100, 100], [280, 110], [300, 280], [120, 300], [90, 200]],
        "visibility": "uncertain",
        "boundary_quality": 0.48,
        "request_more_evidence": True,
        "surfaces": [
            {"surface_id": "folded_paper_1", "bbox": [90, 100, 300, 300], "owner_ref": "folded_paper_1", "visibility": "uncertain"},
        ],
        "relations": [],
    },
    "receipt_attached_to_package": {
        "edge_count": 8,
        "contour_type": "multi_contour",
        "boundary_quality": 0.85,
        "surfaces": [
            {"surface_id": "package_surface", "bbox": [20, 80, 200, 280], "owner_ref": "package_001", "visibility": "visible"},
            {"surface_id": "receipt_surface", "bbox": [30, 200, 150, 280], "owner_ref": "receipt_001", "visibility": "visible"},
        ],
        "relations": [
            {"entity_a": "receipt_surface", "entity_b": "package_surface", "relation_type": "attached_to", "evidence_basis": "spatial_attachment"},
        ],
    },
    "document_on_screen": {
        "edge_count": 4,
        "contour_type": "quadrilateral_screen",
        "quadrilateral": [150, 100, 350, 100, 350, 400, 150, 400],
        "visibility": "visible",
        "boundary_quality": 0.88,
        "possible_screen_document": True,
        "surfaces": [
            {"surface_id": "tablet_screen", "bbox": [150, 100, 350, 400], "owner_ref": "tablet_screen"},
        ],
        "relations": [],
    },
    "low_contrast_paper_on_desk": {
        "edge_count": 4,
        "contour_type": "low_contrast_quadrilateral",
        "quadrilateral": [50, 50, 250, 55, 248, 350, 48, 345],
        "visibility": "partial",
        "boundary_quality": 0.35,
        "low_contrast": True,
        "request_more_evidence": True,
        "surfaces": [
            {"surface_id": "low_contrast_paper", "bbox": [48, 50, 250, 350], "owner_ref": "low_contrast_paper", "visibility": "partial"},
        ],
        "relations": [],
    },
}
