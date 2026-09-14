# -*- coding: utf-8 -*-
"""Option A — validation adapter v1."""

from __future__ import annotations

from typing import Any, Dict


def resolve_option_a_validation(
    *,
    runtime_status: str,
    possible_screen_document: bool = False,
    request_more_evidence: bool = False,
    low_contrast: bool = False,
) -> Dict[str, Any]:
    if possible_screen_document:
        return {
            "validation_status_candidate": "defer_to_screen_surface_detector",
            "possible_screen_document_content_candidate": True,
            "screen_surface_not_document_surface_fact": True,
            "candidate_only": True,
        }
    if low_contrast:
        return {
            "validation_status_candidate": "needs_more_evidence",
            "low_contrast_boundary_candidate": True,
            "next_action_candidate": "request_better_view_or_lighting",
            "candidate_only": True,
        }
    if request_more_evidence:
        return {
            "validation_status_candidate": "needs_more_evidence",
            "request_more_evidence_candidate": True,
            "not_document_fact": True,
            "candidate_only": True,
        }
    if runtime_status == "ok":
        return {"validation_status_candidate": "pending_validation", "candidate_only": True}
    return {"validation_status_candidate": runtime_status, "candidate_only": True}
