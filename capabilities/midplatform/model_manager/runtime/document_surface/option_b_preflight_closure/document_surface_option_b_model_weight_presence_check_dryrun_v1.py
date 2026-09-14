# -*- coding: utf-8 -*-
"""Model weight presence check dryrun."""

from __future__ import annotations

from typing import Any, Dict


def run_model_weight_presence_check_dryrun(*, fixture: Dict[str, Any], run_id: str) -> Dict[str, Any]:
    w = fixture.get("weight_profile") or {}
    ok = w.get("type") != "model_weight_missing" and w.get("present") is not False
    status = "weight_present_candidate" if ok else "weight_missing_candidate"
    return {
        "model_candidate_id": fixture["model_candidate_id"],
        "model_weight_presence_check_candidate": status,
        "weight_status_candidate": status,
        "download_performed": False,
        "network_fetch_performed": False,
        "abort_reason": None if ok else "model_weight_missing",
        "preflight_run_id": run_id,
        "candidate_only": True,
        "not_fact": True,
    }
