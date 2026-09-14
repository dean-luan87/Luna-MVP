# -*- coding: utf-8 -*-
"""Document Surface — Option B admission metrics reviewer v1."""

from __future__ import annotations

from typing import Any, Dict


EXPECTED = {
    "admitted_for_preflight_candidate_count": 2,
    "blocked_candidate_count": 6,
    "execution_block_rate": 1.0,
    "download_block_rate": 1.0,
    "install_block_rate": 1.0,
    "active_model_selection_rate": 0.0,
    "active_registry_update_rate": 0.0,
    "no_ocr_leak_rate": 1.0,
    "no_vlm_leak_rate": 1.0,
    "no_layout_leak_rate": 1.0,
    "no_fact_output_rate": 1.0,
    "protocol_compliance_rate": 1.0,
}


def review_admission_metrics(*, metrics: Dict[str, Any]) -> Dict[str, Any]:
    checks = {k: metrics.get(k) == v for k, v in EXPECTED.items()}
    checks["candidate_fixture_count_8"] = metrics.get("candidate_fixture_count") == 8
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_metrics_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "metrics": metrics,
        "interpretation": "metrics 代表 admission gate 可用，不代表 segmentation quality 已验证",
        "candidate_only": True,
        "not_fact": True,
    }
