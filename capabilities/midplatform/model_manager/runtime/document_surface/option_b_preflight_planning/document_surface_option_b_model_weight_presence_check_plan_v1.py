# -*- coding: utf-8 -*-
"""Document Surface — Option B model weight presence check plan v1."""

from __future__ import annotations

from typing import Any, Dict


def build_model_weight_presence_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_model_weight_presence_check_plan_v1",
        "check_type": "model_weight_presence_check",
        "output_type": "model_weight_presence_check_candidate",
        "status_output": "weight_status_candidate",
        "rules": [
            "check_weight_exists_only",
            "no_weight_download",
            "no_network_fetch",
        ],
        "abort_on": ["model_weight_missing", "uncontrolled_weight_location"],
        "abort_reason_template": "model_weight_missing_or_uncontrolled",
        "download_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
