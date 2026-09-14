# -*- coding: utf-8 -*-
"""Document Surface — Option B license/weight dryrun v1."""

from __future__ import annotations

from typing import Any, Dict


def run_license_weight_dryrun(*, candidate: Dict[str, Any]) -> Dict[str, Any]:
    license_status = candidate.get("license_status_candidate", "")
    weight = candidate.get("weight_profile") or {}
    blocked = False
    reason = None

    if license_status in ("license_unknown", "unknown"):
        blocked = True
        reason = "blocked_license_not_cleared_candidate"
    elif weight.get("type") == "model_weight_missing" or weight.get("present") is False:
        blocked = True
        reason = "blocked_model_weight_missing_candidate"
    elif weight.get("size_mb", 0) > 500:
        blocked = True
        reason = "blocked_model_weight_too_large_candidate"

    if blocked:
        return {
            "license_weight_result_candidate": reason,
            "allowed_to_preflight_candidate": False,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "license_weight_result_candidate": "license_weight_passed_candidate",
        "allowed_to_preflight_candidate": license_status in ("clear", "clear_candidate"),
        "candidate_only": True,
        "not_fact": True,
    }
