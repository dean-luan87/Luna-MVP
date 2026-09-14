# -*- coding: utf-8 -*-
"""Document Surface Validation Adapter — dryrun v1."""

from __future__ import annotations

from typing import Any, Dict


def resolve_validation_status(
    *,
    runtime_status: str,
    layout_conflict: bool = False,
    possible_screen_document: bool = False,
    request_more_evidence: bool = False,
) -> Dict[str, Any]:
    """Map runtime status → validation_status_candidate."""
    if layout_conflict:
        return {
            "validation_status_candidate": "validation_review",
            "detector_conflict_candidate": True,
            "not_auto_pick_high_confidence": True,
            "candidate_only": True,
        }
    if possible_screen_document:
        return {
            "validation_status_candidate": "defer_to_screen_surface_detector",
            "possible_screen_document_content_candidate": True,
            "screen_surface_not_document_surface_fact": True,
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
        return {
            "validation_status_candidate": "pending_validation",
            "candidate_only": True,
        }
    return {
        "validation_status_candidate": runtime_status,
        "candidate_only": True,
    }
