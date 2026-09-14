# -*- coding: utf-8 -*-
"""Document Surface — iteration v2 fixture plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_iteration_v2_fixture_plan() -> Dict[str, Any]:
    fixtures: List[Dict[str, Any]] = [
        {
            "fixture_id": "true_screen_document_fixture",
            "type": "real_photo",
            "target_route": "Option A + defer",
            "expected_behavior": "defer_to_screen_surface_detector",
            "forbidden_behavior": "document_surface_fact_promotion",
        },
        {
            "fixture_id": "clear_receipt_attached_to_box",
            "type": "real_photo",
            "target_route": "Option B",
            "expected_behavior": "attached_surface_mask_candidate",
            "forbidden_behavior": "receipt_text_to_package_fact",
        },
        {
            "fixture_id": "receipt_attached_to_wrinkled_plastic",
            "type": "real_photo",
            "target_route": "Option B",
            "expected_behavior": "uncertain_attached_to_candidate",
            "forbidden_behavior": "forced_attached_to",
        },
        {
            "fixture_id": "overlapping_receipts_clear_two_surfaces",
            "type": "real_photo",
            "target_route": "A+B comparison",
            "expected_behavior": "two_surface_candidates_or_uncertain_relation",
            "forbidden_behavior": "fake_relation_forced_two_surface",
        },
        {
            "fixture_id": "high_overlap_with_visible_corners",
            "type": "real_photo",
            "target_route": "Option B",
            "expected_behavior": "partial_surface_or_occlusion_hint",
            "forbidden_behavior": "separation_success_upgrade",
        },
        {
            "fixture_id": "texture_false_positive_no_document",
            "type": "synthetic_controlled",
            "not_real_world_benchmark": True,
            "target_route": "Option A",
            "expected_behavior": "false_surface_suppressed_or_marked",
            "forbidden_behavior": "fact_output",
        },
        {
            "fixture_id": "single_clear_boundary_baseline",
            "type": "real_photo",
            "target_route": "Option A",
            "expected_behavior": "single_surface_candidate",
            "forbidden_behavior": "over_segmentation",
        },
        {
            "fixture_id": "low_contrast_with_ground_truth_context",
            "type": "synthetic_controlled",
            "not_real_world_benchmark": True,
            "target_route": "Option A",
            "expected_behavior": "low_confidence_boundary_candidate",
            "forbidden_behavior": "fact_promotion",
        },
    ]
    return {
        "plan_id": "document_surface_iteration_v2_fixture_plan_v2_1",
        "immediate_fixture_required": False,
        "category_count": len(fixtures),
        "fixtures": fixtures,
        "synthetic_marked": sum(1 for f in fixtures if f.get("not_real_world_benchmark")),
        "candidate_only": True,
        "not_fact": True,
    }
