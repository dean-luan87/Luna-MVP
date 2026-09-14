# -*- coding: utf-8 -*-
"""Document Surface — output boundary preflight v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_planning.document_surface_controlled_output_policy_v1 import (
    CONTROLLED_OUTPUT_ROOT,
    build_controlled_output_policy,
)

PREFLIGHT_OUTPUT_ROOT = "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_preflight_v1/"


def run_output_boundary_preflight(*, repo_root: Path) -> Dict[str, Any]:
    policy = build_controlled_output_policy()
    rules = policy.get("boundary_rules") or {}
    root_ok = CONTROLLED_OUTPUT_ROOT.startswith("_tmp_eval_out/")
    preflight_dir = repo_root / PREFLIGHT_OUTPUT_ROOT

    return {
        "check_id": "output_boundary_preflight_v1",
        "output_root": CONTROLLED_OUTPUT_ROOT,
        "output_root_in_tmp_eval_out": root_ok,
        "no_production_write": policy.get("no_production_write") is True,
        "no_training_data_write": rules.get("no_training_data_write") is True,
        "no_benchmark_canon_write": rules.get("no_benchmark_canon_write") is True,
        "no_fact_write": rules.get("no_fact_write") is True,
        "trace_metrics_candidate_only": rules.get("trace_and_metrics_only") is True,
        "preflight_output_root": PREFLIGHT_OUTPUT_ROOT,
        "preflight_summary_writable": True,
        "passed": root_ok and policy.get("no_production_write") is True and rules.get("no_training_data_write") is True,
        "candidate_only": True,
        "not_fact": True,
    }
