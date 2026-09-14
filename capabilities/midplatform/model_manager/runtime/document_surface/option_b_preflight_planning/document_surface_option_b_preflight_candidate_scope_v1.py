# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight candidate scope v1."""

from __future__ import annotations

from typing import Any, Dict, List

PREFLIGHT_CANDIDATES: List[Dict[str, Any]] = [
    {
        "model_candidate_id": "family_a_classical_helper_ok_candidate",
        "family_type": "classical_lightweight_segmentation_helper",
        "admission_status": "admitted_for_preflight_candidate",
        "preflight_candidate": True,
        "execution_allowed": False,
        "active_model": False,
        "active_skill": False,
    },
    {
        "model_candidate_id": "family_c_document_specific_surface_model_ok_for_preflight",
        "family_type": "document_specific_segmentation_surface_model",
        "admission_status": "admitted_for_preflight_candidate",
        "preflight_candidate": True,
        "execution_allowed": False,
        "active_model": False,
        "active_skill": False,
    },
]

BLOCKED_REFERENCE_IDS = [
    "family_a_requires_uncontrolled_binary",
    "family_b_lightweight_sam_like_weight_missing",
    "family_b_sam_like_license_unknown",
    "family_b_sam_like_caption_or_text_default",
    "family_c_document_model_outputs_document_type_fact",
    "family_d_depth_geometric_requires_hardware",
]


def build_preflight_candidate_scope() -> Dict[str, Any]:
    return {
        "scope_id": "option_b_preflight_candidate_scope_v1",
        "preflight_candidates": PREFLIGHT_CANDIDATES,
        "preflight_candidate_count": len(PREFLIGHT_CANDIDATES),
        "blocked_reference_ids": BLOCKED_REFERENCE_IDS,
        "blocked_excluded_from_preflight": True,
        "active_model_selected": False,
        "active_skill_selected": False,
        "not_model_admitted": True,
        "not_skill_admitted": True,
        "not_runtime_admitted": True,
        "candidate_only": True,
        "not_fact": True,
    }
