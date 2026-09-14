# -*- coding: utf-8 -*-
"""Document Surface — Option A limit review v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_option_a_limit_review() -> Dict[str, Any]:
    case_performance: List[Dict[str, Any]] = [
        {"case": "case_a_clear_edges", "observation": "1 surface, uncertain_relation", "limitation": "under-separated"},
        {"case": "case_b_low_overlap", "observation": "3 surfaces, overlaps relation", "limitation": "possible over-segmentation"},
        {"case": "case_c_high_overlap", "observation": "0 surface, uncertain_relation", "limitation": "surface missed"},
        {"case": "case_e_texture_false_positive", "observation": "1 surface candidate", "limitation": "texture false positive remains"},
        {"case": "case_f_receipt_clear", "observation": "0 surface, uncertain_attached_to", "limitation": "receipt surface missed"},
        {"case": "case_h_screen_control", "observation": "defer guard pass", "limitation": "fixture semantic mismatch, not detector solvable"},
    ]
    return {
        "option_a_id": "option_a_classical_cv_boundary",
        "option_a_strengths": [
            "dependency_light",
            "low_cost_baseline",
            "simple_clear_boundary_effective",
            "abort_and_uncertainty_fallback",
            "governance_metrics_proven",
        ],
        "option_a_limitations": [
            "under_separated_overlapping_documents",
            "high_overlap_surface_missed",
            "possible_over_segmentation_low_overlap",
            "texture_false_positive_persistence",
            "attached_receipt_surface_missed",
            "cannot_resolve_fixture_semantic_mismatch",
        ],
        "option_a_keep_scope": [
            "single_flat_paper",
            "simple_clear_boundary",
            "low_cost_baseline",
            "dependency_light_baseline",
            "abort_uncertainty_fallback",
        ],
        "option_a_not_sufficient_for": [
            "overlapping_papers_clear_separation",
            "high_overlap_occlusion_recovery",
            "attached_receipt_surface_mask",
            "texture_false_positive_suppression",
            "screen_document_semantic_fixture",
        ],
        "option_a_activation_status": "not_allowed",
        "option_a_sole_route": False,
        "case_performance_review": case_performance,
        "route_verdict": "retain_as_baseline_candidate_not_sole_route",
        "candidate_only": True,
        "not_fact": True,
    }
