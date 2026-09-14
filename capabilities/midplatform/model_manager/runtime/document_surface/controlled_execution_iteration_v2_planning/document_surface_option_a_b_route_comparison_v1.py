# -*- coding: utf-8 -*-
"""Document Surface — Option A/B route comparison v1."""

from __future__ import annotations

from typing import Any, Dict


def build_option_a_b_route_comparison() -> Dict[str, Any]:
    return {
        "relationship_model": "parallel_candidate_routes",
        "option_a_role": "baseline_candidate",
        "option_b_role": "segmentation_candidate_route",
        "competition_mode": False,
        "silent_fallback": False,
        "auto_substitute": False,
        "confidence_auto_override": False,
        "teacher_mode": False,
        "route_selection_output": "route_candidate",
        "route_selection_is_execution_decision": False,
        "conflict_resolution": "validation_review",
        "conflict_resolution_note": "A/B 结果冲突时进入 validation_review，不按 confidence 自动覆盖",
        "comparison_matrix": [
            {"dimension": "dependency", "option_a": "cv2_only", "option_b": "admission_required_lightweight_seg"},
            {"dimension": "cost", "option_a": "low", "option_b": "medium_controlled"},
            {"dimension": "clear_boundary", "option_a": "strong", "option_b": "optional"},
            {"dimension": "overlap_separation", "option_a": "weak", "option_b": "candidate_strength"},
            {"dimension": "high_occlusion", "option_a": "weak", "option_b": "candidate_strength"},
            {"dimension": "attached_surface_mask", "option_a": "weak", "option_b": "candidate_strength"},
            {"dimension": "texture_fp", "option_a": "weak", "option_b": "conditional_with_field_support"},
            {"dimension": "governance_proven", "option_a": "yes", "option_b": "pending_admission"},
        ],
        "verdict": "introduce_option_b_as_parallel_candidate_route",
        "option_a_continue_iteration": True,
        "option_a_as_sole_route": False,
        "candidate_only": True,
        "not_fact": True,
    }
