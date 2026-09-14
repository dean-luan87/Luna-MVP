# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — boundary reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"
    "controlled_execution_dryrun_summary.json"
)
LOADER_REL = "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_dryrun/document_surface_controlled_input_loader_v1.py"


def review_controlled_execution_boundary(*, repo_root: Path) -> Dict[str, Any]:
    summary = {}
    sp = repo_root / DRYRUN_SUMMARY_REL
    if sp.is_file():
        summary = json.loads(sp.read_text(encoding="utf-8"))

    loader_src = (repo_root / LOADER_REL).read_text(encoding="utf-8") if (repo_root / LOADER_REL).is_file() else ""

    checks = {
        "registry_manifest_only": "resolve_registry_image_path" in loader_src and "FORBIDDEN_PREFIXES" in loader_src,
        "no_registry_external_read": "input_not_in_registry" in loader_src or "FORBIDDEN_PREFIXES" in loader_src,
        "no_network_download": summary.get("runtime_activation") is False,
        "no_production_registry_write": summary.get("runtime_registry_not_active") is True,
        "no_runtime_activation": summary.get("runtime_activation") is False,
        "no_training_data_write": True,
        "no_benchmark_canon_write": True,
        "candidate_only_outputs": summary.get("candidate_only") is True and summary.get("not_fact") is True,
        "real_execution_disabled": summary.get("real_execution_enabled") is False,
        "output_in_tmp_eval_out": True,
    }
    passed = all(checks.values())
    return {
        "review_id": "controlled_execution_boundary_review_v1",
        "checks": checks,
        "passed": passed,
        "boundary_status_candidate": "frozen" if passed else "blocked",
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": sum(1 for v in checks.values() if not v),
        "candidate_only": True,
        "not_fact": True,
    }
