# -*- coding: utf-8 -*-
"""Document Surface — attached-to uncertainty strategy v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict


def build_attached_to_uncertainty_strategy_plan() -> Dict[str, Any]:
    return {
        "strategy_id": "document_surface_attached_to_uncertainty_strategy_v1",
        "target_case": "case_d_receipt_attached_to_package_controlled",
        "observed_issue": "receipt/package separation low confidence, uncertain",
        "separation_conditions": {
            "receipt_like_surface_candidate": "distinct_bbox + edge_group + contrast_from_background",
            "package_background_candidate": "larger_supporting_region + different_texture_band",
            "minimum_confidence_for_attached_to": 0.55,
        },
        "attached_to_evidence_requirements": [
            "spatial_adjacency_candidate",
            "non_duplicate_surface_pair",
            "boundary_confidence_above_threshold_or_uncertain",
        ],
        "uncertain_outputs": [
            "uncertain_attached_to_candidate",
            "request_more_evidence_if_boundary_uncertain",
        ],
        "forbidden": [
            "do_not_assign_receipt_text_to_package",
            "no_receipt_content_as_package_fact",
            "no_attached_to_without_evidence",
        ],
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }
