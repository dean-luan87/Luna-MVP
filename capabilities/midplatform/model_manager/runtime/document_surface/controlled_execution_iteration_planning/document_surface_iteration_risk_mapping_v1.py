# -*- coding: utf-8 -*-
"""Document Surface — iteration risk mapping v1."""

from __future__ import annotations

from typing import Any, Dict, List

RISK_TO_STRATEGY: List[Dict[str, Any]] = [
    {
        "risk_id": "overlapping_documents_under_separated",
        "source_case": "case_b_two_overlapping_papers_controlled",
        "observed": "1 surface / 0 relation",
        "strategy_module": "overlap_separation_strategy_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "relation_hint_missing_for_overlap_case",
        "source_case": "case_b_two_overlapping_papers_controlled",
        "observed": "no overlaps/occludes relation",
        "strategy_module": "overlap_separation_strategy_v1 + relation_hint_constraints_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "low_contrast_false_surface_risk",
        "source_case": "case_c_low_contrast_paper_controlled",
        "observed": "9 surfaces + 4 relations",
        "strategy_module": "low_contrast_noise_strategy_v1 + candidate_quality_gate_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "candidate_count_noise_in_low_contrast_case",
        "source_case": "case_c_low_contrast_paper_controlled",
        "observed": "excessive candidate count",
        "strategy_module": "low_contrast_noise_strategy_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "receipt_attachment_boundary_uncertain",
        "source_case": "case_d_receipt_attached_to_package_controlled",
        "observed": "low confidence, uncertain separation",
        "strategy_module": "attached_to_uncertainty_strategy_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "screen_vs_document_ambiguity_continues",
        "source_case": "case_e_document_on_screen_controlled",
        "observed": "defer_to_screen_surface_detector",
        "strategy_module": "relation_hint_constraints_v1 (possible_screen_content)",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "classical_cv_boundary_limitations_confirmed",
        "source_case": "post_review_global",
        "observed": "Option A limits in overlap/low-contrast",
        "strategy_module": "candidate_quality_gate_v1",
        "blocker": False,
        "watch_status": "retained",
    },
    {
        "risk_id": "OCR_per_surface_not_started",
        "source_case": "deferred",
        "strategy_module": "out_of_scope_iteration_v1",
        "blocker": False,
        "watch_status": "deferred",
    },
    {
        "risk_id": "field_centric_role_dryrun_pending",
        "source_case": "parallel_track",
        "strategy_module": "parallel_next_track",
        "blocker": False,
        "watch_status": "parallel_track",
    },
]

CASE_BCD_RISKS = {
    "case_b": ["overlapping_documents_under_separated", "relation_hint_missing_for_overlap_case"],
    "case_c": ["low_contrast_false_surface_risk", "candidate_count_noise_in_low_contrast_case"],
    "case_d": ["receipt_attachment_boundary_uncertain"],
}


def build_iteration_risk_mapping() -> Dict[str, Any]:
    bcd_mapped = all(
        rid in [m["risk_id"] for m in RISK_TO_STRATEGY]
        for ids in CASE_BCD_RISKS.values() for rid in ids
    )
    return {
        "mapping_id": "document_surface_iteration_risk_mapping_v1",
        "risk_mappings": RISK_TO_STRATEGY,
        "case_bcd_risks": CASE_BCD_RISKS,
        "all_case_bcd_mapped": bcd_mapped,
        "mapping_count": len(RISK_TO_STRATEGY),
        "non_blocker_watch_retained": True,
        "candidate_only": True,
        "not_fact": True,
    }
