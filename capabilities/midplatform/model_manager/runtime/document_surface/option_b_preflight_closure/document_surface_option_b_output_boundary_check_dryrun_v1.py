# -*- coding: utf-8 -*-
"""Output boundary check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_output_boundary_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "output_boundary_check_candidate": "output_boundary_ok_candidate",
        "allowed_output_scope": ["_tmp_eval_out"],
        "production_registry_write": False,
        "active_registry_write": False,
        "abort_reason": None,
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
