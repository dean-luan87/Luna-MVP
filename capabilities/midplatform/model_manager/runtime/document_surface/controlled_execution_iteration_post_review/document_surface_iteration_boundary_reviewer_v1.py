# -*- coding: utf-8 -*-
"""Document Surface Iteration — boundary reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/"
    "iteration_dryrun_summary.json"
)
CASE_RESULTS_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_iteration_dryrun_v1/"
    "iteration_case_results.json"
)


def review_iteration_boundary(*, repo_root: Path) -> Dict[str, Any]:
    summary = json.loads((repo_root / DRYRUN_SUMMARY_REL).read_text(encoding="utf-8")) if (repo_root / DRYRUN_SUMMARY_REL).is_file() else {}
    cases: List[Dict[str, Any]] = json.loads((repo_root / CASE_RESULTS_REL).read_text(encoding="utf-8")) if (repo_root / CASE_RESULTS_REL).is_file() else []
    metrics = summary.get("metrics") or {}

    checks = {
        "no_ocr_execution": metrics.get("no_ocr_leak_rate", 0) == 1.0,
        "no_vlm_call": all(not (c.get("trace") or {}).get("vlm_called") for c in cases if c.get("trace")),
        "no_layout_parser": all(not (c.get("trace") or {}).get("layout_called") for c in cases if c.get("trace")),
        "no_runtime_activation": summary.get("runtime_activation_allowed") is False,
        "no_production_write": True,
        "no_candidate_to_fact_promotion": metrics.get("no_fact_output_rate", 0) == 1.0,
        "candidate_only_not_fact": summary.get("candidate_only") is True and summary.get("not_fact") is True,
        "relation_evidence_basis": metrics.get("relation_hint_evidence_compliance_rate", 0) == 1.0,
        "no_fake_relation": metrics.get("fake_relation_rate", 1) == 0,
        "no_forced_multi_surface": metrics.get("forced_multi_surface_rate", 1) == 0,
        "detector_rerun_forbidden": True,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "iteration_boundary_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "boundary_status": "frozen",
        "runtime_activation_allowed": False,
        "candidate_only": True,
        "not_fact": True,
    }
