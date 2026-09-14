# -*- coding: utf-8 -*-
"""Document Surface — Option B output boundary check plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_output_boundary_check_plan() -> Dict[str, Any]:
    return {
        "plan_id": "option_b_output_boundary_check_plan_v1",
        "check_type": "output_boundary_check",
        "output_type": "output_boundary_check_candidate",
        "allowed_output_scope": ["_tmp_eval_out"],
        "forbidden_output_scope": [
            "production_registry",
            "active_registry",
            "model_artifact_write",
            "training_data_write",
        ],
        "rules": [
            "tmp_eval_out_only",
            "no_production_registry_write",
            "no_active_registry_write",
        ],
        "abort_on": ["output_boundary_violation"],
        "active_registry_update_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
