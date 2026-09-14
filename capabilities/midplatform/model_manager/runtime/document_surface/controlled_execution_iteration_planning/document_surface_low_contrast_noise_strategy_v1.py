# -*- coding: utf-8 -*-
"""Document Surface — low contrast noise strategy v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List


def build_low_contrast_noise_strategy_plan() -> Dict[str, Any]:
    return {
        "strategy_id": "document_surface_low_contrast_noise_strategy_v1",
        "target_case": "case_c_low_contrast_paper_controlled",
        "observed_issue": "9 surfaces + 4 relations — candidate noise high",
        "suppression_strategy": [
            "candidate_count_cap",
            "minimum_area_threshold",
            "duplicate_candidate_suppression",
            "contour_quality_filtering",
        ],
        "uncertainty_path": {
            "low_contrast_uncertainty_status": True,
            "request_better_view_or_lighting": True,
            "preserve_uncertain_candidate_path": True,
        },
        "forbidden": [
            "global_threshold_delete_all_low_confidence",
            "accuracy_only_metric_as_gate",
            "forced_single_surface_output",
        ],
        "candidate_count_cap_candidate": 5,
        "accuracy_not_admission_criterion": True,
        "candidate_only": True,
        "not_fact": True,
        "planning_only": True,
    }
