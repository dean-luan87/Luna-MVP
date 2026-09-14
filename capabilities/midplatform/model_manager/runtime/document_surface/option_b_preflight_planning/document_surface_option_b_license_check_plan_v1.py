# -*- coding: utf-8 -*-
"""Document Surface — Option B license check plan v1."""

from __future__ import annotations

from typing import Any, Dict


def build_license_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_license_check_plan_v1",
        "check_type": "license_check",
        "output_type": "license_check_candidate",
        "status_output": "license_status_candidate",
        "rules": [
            "check_license_metadata_exists",
            "no_assume_clear_without_metadata",
        ],
        "abort_on": ["license_unknown", "license_incompatible", "commercial_use_unclear"],
        "abort_reason_template": "license_not_cleared",
        "candidate_only": True,
        "not_fact": True,
    }
