# -*- coding: utf-8 -*-
"""Document Surface — Option B dependency availability check plan v1."""

from __future__ import annotations

from typing import Any, Dict


def build_dependency_availability_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_dependency_availability_check_plan_v1",
        "check_type": "dependency_availability_check",
        "output_type": "dependency_availability_check_candidate",
        "status_output": "dependency_status_candidate",
        "rules": [
            "check_existing_dependency_only",
            "no_install",
            "no_download",
            "no_silent_import_unadmitted",
        ],
        "abort_on": ["dependency_missing", "dependency_uncontrolled"],
        "abort_reason_template": "dependency_not_available_or_uncontrolled",
        "install_allowed": False,
        "download_allowed": False,
        "execution_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
