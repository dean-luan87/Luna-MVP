# -*- coding: utf-8 -*-
"""Document Surface — Option B admission gate reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

ADMISSION_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_admission_dryrun_summary.json"
)


def review_option_b_admission_gate(*, repo_root: Path) -> Dict[str, Any]:
    admissions: List[Dict[str, Any]] = json.loads((repo_root / ADMISSION_REL).read_text(encoding="utf-8")) if (repo_root / ADMISSION_REL).is_file() else []
    checks = {
        "candidate_route_only": all(a.get("option_b_status") == "candidate_route_only" for a in admissions),
        "execution_allowed_false": all(a.get("execution_allowed") is False for a in admissions),
        "dependency_admission_required": all(a.get("dependency_admission_required") is True for a in admissions),
        "model_download_allowed_false": all(a.get("model_download_allowed") is False for a in admissions),
        "training_allowed_false": all(a.get("training_allowed") is False for a in admissions),
        "active_registry_update_false": all(a.get("active_registry_update_allowed") is False for a in admissions),
        "planning_before_execution": all(a.get("controlled_execution_planning_required_before_any_execution") is True for a in admissions),
        "no_active_model_id": all(a.get("active_model_id") is None for a in admissions),
        "no_segmentation_result": all(a.get("segmentation_mask_result") is None for a in admissions),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_admission_gate_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
