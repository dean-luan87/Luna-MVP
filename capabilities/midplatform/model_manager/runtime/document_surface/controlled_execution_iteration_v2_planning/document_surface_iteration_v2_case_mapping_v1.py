# -*- coding: utf-8 -*-
"""Document Surface — iteration v2 case mapping v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_iteration_v2_case_mapping() -> Dict[str, Any]:
    mappings: List[Dict[str, Any]] = [
        {
            "case_id": "case_a_clear_edges",
            "watch": "overlapping_documents_under_separated",
            "option_a": "baseline_run_allowed",
            "option_b": "recommended_for_surface_separation_candidate",
            "validation": "required_on_a_b_conflict",
            "fixture_correction": False,
        },
        {
            "case_id": "case_b_low_overlap",
            "watch": "possible_over_segmentation_in_low_overlap_case",
            "option_a": "quality_gate_retained",
            "option_b": "optional_candidate_route",
            "validation": "conflict_review_required",
            "fixture_correction": False,
        },
        {
            "case_id": "case_c_high_overlap",
            "watch": "high_overlap_surface_missed",
            "option_a": "uncertain_baseline_output",
            "option_b": "recommended_candidate_route",
            "validation": "required_on_a_b_conflict",
            "fixture_correction": False,
        },
        {
            "case_id": "case_e_texture_false_positive",
            "watch": "texture_false_positive_candidate_remains",
            "option_a": "quality_gate_false_surface_guard",
            "option_b": "only_if_attention_field_supports",
            "validation": "false_surface_guard_retained",
            "fixture_correction": False,
        },
        {
            "case_id": "case_f_receipt_clear",
            "watch": "receipt_attached_clear_surface_missed",
            "option_a": "uncertain_attached_baseline",
            "option_b": "recommended_for_attached_surface_mask",
            "validation": "attached_to_requires_relation_evidence",
            "fixture_correction": False,
        },
        {
            "case_id": "case_h_screen_control",
            "watch": "document_on_screen_fixture_semantic_mismatch",
            "option_a": "defer_to_screen_surface_detector",
            "option_b": "cannot_solve_fixture_mismatch",
            "validation": "not_detector_quality_basis",
            "fixture_correction": True,
            "attribution": "fixture_semantic_mismatch_not_detector_failure",
        },
    ]
    return {
        "mapping_id": "document_surface_iteration_v2_case_mapping_v1",
        "cases_mapped": [m["case_id"] for m in mappings],
        "all_required_cases_covered": all(c in {m["case_id"] for m in mappings} for c in (
            "case_a_clear_edges", "case_b_low_overlap", "case_c_high_overlap",
            "case_e_texture_false_positive", "case_f_receipt_clear", "case_h_screen_control",
        )),
        "mappings": mappings,
        "candidate_only": True,
        "not_fact": True,
    }
