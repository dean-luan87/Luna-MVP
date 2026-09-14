# -*- coding: utf-8 -*-
"""Document Surface — candidate quality gate v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List

QUALITY_GATE_SIGNALS = (
    "boundary_confidence_candidate",
    "polygon_area_ratio",
    "edge_support_score",
    "rectangularity_score",
    "contour_closure_score",
    "background_contrast_score",
    "duplicate_overlap_score",
    "excessive_candidate_count_guard",
)

GATE_OUTCOMES = (
    "keep_candidate",
    "mark_low_confidence",
    "merge_candidate_rejected",
    "request_more_evidence",
)


def build_candidate_quality_gate_plan() -> Dict[str, Any]:
    return {
        "plan_id": "document_surface_candidate_quality_gate_v1",
        "quality_signals": list(QUALITY_GATE_SIGNALS),
        "gate_outcomes": list(GATE_OUTCOMES),
        "writes_fact": False,
        "candidate_only": True,
        "not_fact": True,
        "rules": [
            {"signal": "boundary_confidence_candidate", "threshold_candidate": 0.45, "below_action": "mark_low_confidence"},
            {"signal": "polygon_area_ratio", "min_candidate": 0.02, "below_action": "merge_candidate_rejected"},
            {"signal": "duplicate_overlap_score", "max_candidate": 0.85, "above_action": "merge_candidate_rejected"},
            {"signal": "excessive_candidate_count_guard", "max_candidates": 5, "above_action": "request_more_evidence"},
            {"signal": "background_contrast_score", "min_for_keep": 0.15, "below_action": "mark_low_confidence"},
        ],
        "forbidden_outcomes": ["promote_to_fact", "owner_fact", "document_type_fact"],
        "planning_only": True,
    }
