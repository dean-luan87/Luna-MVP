# -*- coding: utf-8 -*-
"""Candidate schema compliance check dryrun."""

from __future__ import annotations

from typing import Any, Dict, List

ALLOWED = [
    "surface_mask_candidate", "document_surface_candidate", "boundary_candidate",
    "partial_surface_candidate", "occlusion_surface_hint_candidate", "runtime_error_candidate",
]


def run_candidate_schema_compliance_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    raw = fixture.get("raw_output_profile", "mask_only")
    ok = "fact" not in raw and raw != "caption_or_text_possible"
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "candidate_schema_compliance_check_candidate": "schema_compliant_candidate" if ok else "schema_violation_candidate",
        "allowed_output_types": ALLOWED,
        "abort_reason": None if ok else "candidate_schema_violation",
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
