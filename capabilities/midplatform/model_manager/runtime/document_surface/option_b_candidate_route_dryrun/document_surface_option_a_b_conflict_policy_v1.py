# -*- coding: utf-8 -*-
"""Document Surface — Option A/B conflict policy v1."""

from __future__ import annotations

from typing import Any, Dict


def apply_ab_conflict_policy(
    *,
    option_a_result: Dict[str, Any],
    option_b_route: Dict[str, Any],
) -> Dict[str, Any]:
    a_surfaces = option_a_result.get("surface_count", 0)
    b_recommended = option_b_route.get("option_b_recommended") is True
    conflict = b_recommended and option_a_result.get("status") not in (None, "ok")
    if b_recommended and a_surfaces == 0:
        conflict = True
    if option_b_route.get("selected_route_candidate") == "option_a_baseline_with_optional_b":
        conflict = True

    if conflict:
        resolution = "validation_review"
        silent_fallback = False
        confidence_override = False
        auto_replace_a = False
    else:
        resolution = "no_conflict"
        silent_fallback = False
        confidence_override = False
        auto_replace_a = False

    return {
        "policy_id": "document_surface_option_a_b_conflict_policy_v1",
        "conflict_detected": conflict,
        "conflict_resolution": resolution,
        "validation_review_required": conflict,
        "silent_fallback": silent_fallback,
        "confidence_auto_override": confidence_override,
        "option_a_auto_replaced": auto_replace_a,
        "option_b_silent_fallback": False,
        "candidate_only": True,
        "not_fact": True,
    }
