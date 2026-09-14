# -*- coding: utf-8 -*-
"""Document Surface — Option B metrics reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

METRICS_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_metrics_summary.json"
)

REQUIRED = {
    "option_b_execution_block_rate": 1.0,
    "option_b_model_download_block_rate": 1.0,
    "option_b_active_registry_block_rate": 1.0,
    "option_b_no_fact_compliance_rate": 1.0,
    "option_b_no_ocr_leak_rate": 1.0,
    "option_b_no_vlm_leak_rate": 1.0,
    "option_b_no_layout_leak_rate": 1.0,
    "protocol_compliance_rate": 1.0,
}


def review_option_b_metrics(*, repo_root: Path) -> Dict[str, Any]:
    metrics = json.loads((repo_root / METRICS_REL).read_text(encoding="utf-8")) if (repo_root / METRICS_REL).is_file() else {}
    checks = {k: metrics.get(k) == v for k, v in REQUIRED.items()}
    failed = [k for k, ok in checks.items() if not ok]
    return {
        "review_id": "option_b_metrics_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "metrics": metrics,
        "required_checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
