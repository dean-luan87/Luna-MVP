# -*- coding: utf-8 -*-
"""Document Surface — Option B route selector v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_types_v1 import (
    OPTION_B_ROUTE_ID,
)


def select_route_candidate(
    *,
    case_profile: str,
    option_a_result_profile: Optional[Dict[str, Any]] = None,
    field_context_candidate: Optional[Dict[str, Any]] = None,
    attention_gate_status: str = "allowed",
) -> Dict[str, Any]:
    if attention_gate_status != "allowed":
        return {
            "selected_route_candidate": "blocked_attention_gate",
            "route_reason_candidate": "attention_gate_blocked",
            "validation_required": True,
            "execution_decision": None,
            "candidate_only": True,
            "not_fact": True,
        }

    reason = "baseline_only"
    route = "option_a_baseline_candidate"
    validation_required = False
    option_b_recommended = False

    profiles = {
        "case_a_clear_edges": ("option_b_segmentation_candidate_route", "surface_separation_needed", True, True),
        "case_b_low_overlap": ("option_a_baseline_with_optional_b", "overlap_quality_gate_optional_b", False, True),
        "case_c_high_overlap": ("option_b_segmentation_candidate_route", "partial_surface_or_mask_needed", True, True),
        "case_e_texture_false_positive": ("option_a_baseline_only", "field_attention_gated_no_default_b", False, False),
        "case_f_receipt_clear": ("option_b_segmentation_candidate_route", "attached_surface_mask_needed", True, True),
        "case_h_screen_control": ("defer_screen_surface_detector", "fixture_semantic_mismatch_b_cannot_solve", False, False),
    }
    if case_profile in profiles:
        route, reason, option_b_recommended, validation_required = profiles[case_profile]

    field_supports = (field_context_candidate or {}).get("document_surface_investigation_supported") is True
    if case_profile == "case_e_texture_false_positive" and field_supports:
        route = "option_b_segmentation_candidate_route"
        reason = "field_attention_supports_document_surface_investigation"
        option_b_recommended = True
        validation_required = True

    return {
        "selected_route_candidate": route,
        "route_reason_candidate": reason,
        "option_b_route_id": OPTION_B_ROUTE_ID if option_b_recommended else None,
        "route_constraints": {
            "option_b_status": "candidate_route_only",
            "execution_allowed": False,
            "silent_fallback": False,
            "confidence_auto_override": False,
        },
        "validation_required": validation_required,
        "option_b_recommended": option_b_recommended,
        "execution_decision": None,
        "active_runtime_update": None,
        "direct_model_invocation": None,
        "fallback_decision": None,
        "candidate_only": True,
        "not_fact": True,
    }
