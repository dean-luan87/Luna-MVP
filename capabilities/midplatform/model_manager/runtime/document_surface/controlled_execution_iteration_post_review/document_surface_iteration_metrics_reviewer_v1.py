# -*- coding: utf-8 -*-
"""Document Surface Iteration — metrics reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/"
    "iteration_dryrun_summary.json"
)

REQUIRED_METRICS = {
    "fake_relation_rate": 0.0,
    "forced_multi_surface_rate": 0.0,
    "no_ocr_leak_rate": 1.0,
    "no_fact_output_rate": 1.0,
    "no_fallback_rate": 1.0,
    "relation_hint_evidence_compliance_rate": 1.0,
    "protocol_compliance_rate": 1.0,
}


def review_iteration_metrics(*, repo_root: Path) -> Dict[str, Any]:
    summary = json.loads((repo_root / DRYRUN_SUMMARY_REL).read_text(encoding="utf-8")) if (repo_root / DRYRUN_SUMMARY_REL).is_file() else {}
    metrics = summary.get("metrics") or {}
    checks: Dict[str, bool] = {}
    for key, expected in REQUIRED_METRICS.items():
        actual = metrics.get(key)
        checks[key] = actual == expected

    failed: List[str] = [k for k, ok in checks.items() if not ok]
    return {
        "review_id": "iteration_metrics_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "metrics": metrics,
        "required_checks": checks,
        "failed_checks": failed,
        "quality_interpretation": {
            "go_means": "策略链路安全有效；relation 治理有效",
            "go_does_not_mean": [
                "document surface detector 已可激活",
                "叠放文档已稳定分离",
                "attached receipt 已稳定识别",
                "texture false positive 已完全解决",
            ],
        },
        "candidate_only": True,
        "not_fact": True,
    }
