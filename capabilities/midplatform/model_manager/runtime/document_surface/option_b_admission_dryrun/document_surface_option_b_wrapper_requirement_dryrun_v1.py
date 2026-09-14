# -*- coding: utf-8 -*-
"""Document Surface — Option B wrapper requirement dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

WRAPPER_ALLOWED = [
    "surface_mask_candidate",
    "boundary_candidate",
    "partial_surface_candidate",
    "occlusion_surface_hint_candidate",
]


def run_wrapper_requirement_dryrun(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    raw = candidate.get("raw_output_profile", "mask_only")
    needs_wrapper = raw == "caption_or_text_possible"
    if not needs_wrapper:
        return {
            "wrapper_required": False,
            "wrapper_contract_candidate": None,
            "raw_output_not_allowed_downstream": False,
            "candidate_only": True,
            "not_fact": True,
        }
    if candidate.get("wrapper_available"):
        return {
            "wrapper_required": True,
            "admission_status_candidate": "admitted_with_wrapper_candidate",
            "wrapper_contract_candidate": WRAPPER_ALLOWED,
            "raw_output_must_be_normalized": True,
            "raw_output_not_allowed_downstream": True,
            "execution_allowed": False,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "wrapper_required": True,
        "admission_status_candidate": "blocked_or_requires_wrapper_candidate",
        "wrapper_contract_candidate": WRAPPER_ALLOWED,
        "raw_output_must_be_normalized": True,
        "raw_output_not_allowed_downstream": True,
        "execution_allowed": False,
        "wrapper_missing_blocked": True,
        "candidate_only": True,
        "not_fact": True,
    }
