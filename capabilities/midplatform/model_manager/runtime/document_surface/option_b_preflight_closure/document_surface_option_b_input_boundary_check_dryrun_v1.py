# -*- coding: utf-8 -*-
"""Input boundary check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_input_boundary_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "input_boundary_check_candidate": "input_boundary_ok_candidate",
        "allowed_input_registry_scope": ["controlled_fixture_registry_metadata", "allowed_fixture_ids"],
        "image_content_read": False,
        "pixel_inspection": False,
        "abort_reason": None,
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
