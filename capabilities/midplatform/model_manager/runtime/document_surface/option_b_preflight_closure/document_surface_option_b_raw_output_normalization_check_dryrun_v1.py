# -*- coding: utf-8 -*-
"""Raw output normalization check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_raw_output_normalization_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    raw = fixture.get("raw_output_profile", "mask_only")
    needs_wrapper = raw in ("caption_or_text_possible",) or "caption" in raw or "text" in raw
    if needs_wrapper:
        return {
            "model_candidate_id": fixture["model_candidate_id"],
            "raw_output_normalization_check_candidate": "abort_or_requires_wrapper_candidate",
            "wrapper_required_candidate": True,
            "raw_output_downstream_allowed": False,
            "abort_reason": "wrapper_missing",
            "preflight_run_id": run_id,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "raw_output_normalization_check_candidate": "normalization_ok_candidate",
        "wrapper_required_candidate": False,
        "raw_output_downstream_allowed": False,
        "abort_reason": None,
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
