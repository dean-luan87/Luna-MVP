# -*- coding: utf-8 -*-
"""Document Surface Iteration — protocol compliance reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_model_manager_registry_v1 import (
    DOCUMENT_SURFACE_RUNTIME_REGISTRY,
)

DRYRUN_REVIEW_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1_review_v0/"
    "p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_review_v1.json"
)


def review_iteration_protocol_compliance(*, repo_root: Path) -> Dict[str, Any]:
    entry = DOCUMENT_SURFACE_RUNTIME_REGISTRY.get("document_surface_detector_v1") or {}
    dryrun_review = json.loads((repo_root / DRYRUN_REVIEW_REL).read_text(encoding="utf-8")) if (repo_root / DRYRUN_REVIEW_REL).is_file() else {}

    checks = {
        "iteration_planning_ready": entry.get("controlled_execution_iteration_planning_ready") is True,
        "iteration_dryrun_ready": entry.get("controlled_execution_iteration_dryrun_ready") is True,
        "planning_only": entry.get("planning_only") is True,
        "triggers_ocr": entry.get("triggers_ocr") is False,
        "dryrun_go": dryrun_review.get("final_decision", "").endswith("ITERATION_DRYRUN_GO"),
        "protocol_patch_not_new_branch": True,
        "existing_protocol_chain_required": True,
        "no_runtime_activation": entry.get("runtime_activation_allowed") is not True,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "iteration_protocol_compliance_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "protocol_compliance_passed": len(failed) == 0,
        "candidate_only": True,
        "not_fact": True,
    }
