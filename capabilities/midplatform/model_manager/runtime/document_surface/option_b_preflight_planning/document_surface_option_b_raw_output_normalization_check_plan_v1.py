# -*- coding: utf-8 -*-
"""Document Surface — Option B raw output normalization check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_raw_output_normalization_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_raw_output_normalization_check_plan_v1",
        "check_type": "raw_output_normalization_check",
        "output_type": "raw_output_normalization_check_candidate",
        "wrapper_output": "wrapper_required_candidate",
        "rules": [
            "raw_output_not_allowed_downstream",
            "caption_text_fact_requires_wrapper",
            "wrapper_missing_aborts",
        ],
        "abort_on": ["wrapper_missing", "raw_output_contract_violation", "caption_or_text_default"],
        "abort_or_requires_wrapper_on": ["caption_or_text_possible"],
        "raw_output_downstream_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
