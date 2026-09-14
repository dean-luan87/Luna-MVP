# -*- coding: utf-8 -*-
"""Document Surface — iteration fixture plan v1 (planning, no images)."""

from __future__ import annotations

from typing import Any, Dict, List

ITERATION_FIXTURE_CATEGORIES: List[Dict[str, Any]] = [
    {"category": "two_overlapping_papers_clear_edges", "purpose": "Case B — clear edge separation", "real_image_required_in_planning": False},
    {"category": "two_overlapping_papers_low_overlap", "purpose": "Case B — partial overlap", "real_image_required_in_planning": False},
    {"category": "two_overlapping_papers_high_overlap", "purpose": "Case B — high overlap uncertain", "real_image_required_in_planning": False},
    {"category": "low_contrast_single_paper", "purpose": "Case C — single low contrast doc", "real_image_required_in_planning": False},
    {"category": "low_contrast_texture_false_positive", "purpose": "Case C — background texture noise", "real_image_required_in_planning": False},
    {"category": "receipt_attached_clear", "purpose": "Case D — clear attachment", "real_image_required_in_planning": False},
    {"category": "receipt_attached_uncertain", "purpose": "Case D — uncertain attachment", "real_image_required_in_planning": False},
    {"category": "document_on_screen_control", "purpose": "Case E — screen defer control", "real_image_required_in_planning": False},
]


def build_iteration_fixture_plan() -> Dict[str, Any]:
    return {
        "plan_id": "document_surface_iteration_fixture_plan_v1",
        "fixture_root_candidate": "_fixtures/document_surface_real_runtime_controlled_iteration_v2/",
        "categories": ITERATION_FIXTURE_CATEGORIES,
        "category_count": len(ITERATION_FIXTURE_CATEGORIES),
        "at_least_eight_categories": len(ITERATION_FIXTURE_CATEGORIES) >= 8,
        "no_real_image_required_in_planning": True,
        "no_image_read_in_planning": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
