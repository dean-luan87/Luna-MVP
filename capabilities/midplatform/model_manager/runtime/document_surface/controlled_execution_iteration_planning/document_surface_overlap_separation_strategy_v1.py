# -*- coding: utf-8 -*-
"""Document Surface — overlap separation strategy v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List

FORBIDDEN = (
    "no_fake_overlap_relation",
    "no_relation_without_evidence",
    "no_forced_two_surface_output",
)


def build_overlap_separation_strategy_plan() -> Dict[str, Any]:
    return {
        "strategy_id": "document_surface_overlap_separation_strategy_v1",
        "target_case": "case_b_two_overlapping_papers_controlled",
        "observed_issue": "1 surface / 0 relation — boundary safe, separation insufficient",
        "two_phase_strategy": [
            "primary_outer_boundary_candidate",
            "inner_secondary_edge_candidates",
            "visible_corner_grouping",
            "partial_boundary_hypothesis",
        ],
        "relation_policy": {
            "occlusion_relation_candidate": "only_if_evidence_sufficient",
            "fallback": "overlap_relation_uncertain_candidate",
            "evidence_required": ["geometric_overlap", "distinct_edge_groups", "non_duplicate_bbox"],
        },
        "forbidden": list(FORBIDDEN),
        "does_not_upgrade_case_b_to_separated": True,
        "does_not_fake_relation": True,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }
