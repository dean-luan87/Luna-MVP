# -*- coding: utf-8 -*-
"""Document Surface — Option B candidate route v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

CONSTRAINTS_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_iteration_v2_planning/document_surface_option_b_admission_constraints_v1.json"


def build_option_b_candidate_route(*, repo_root: Path | None = None) -> Dict[str, Any]:
    root = repo_root or Path.cwd()
    constraints = json.loads((root / CONSTRAINTS_REL).read_text(encoding="utf-8"))
    return {
        "option_b_id": "option_b_lightweight_segmentation_candidate",
        "option_b_status": "candidate_route_only",
        "route_role": "segmentation_candidate_route",
        "active_model_specified": False,
        "model_download_planned": False,
        "model_execution_planned": False,
        "training_planned": False,
        "active_registry_update_planned": False,
        "not_silent_fallback": True,
        "not_auto_substitute": True,
        "not_teacher": True,
        "not_vlm": True,
        "not_fact_source": True,
        "allowed_outputs": constraints.get("allowed_output_types"),
        "forbidden_outputs": constraints.get("forbidden_output_types"),
        "admission_constraints_ref": CONSTRAINTS_REL,
        "next_gate": "OptionB-Candidate-Route-DryRun-v1-001",
        "candidate_only": True,
        "not_fact": True,
    }
