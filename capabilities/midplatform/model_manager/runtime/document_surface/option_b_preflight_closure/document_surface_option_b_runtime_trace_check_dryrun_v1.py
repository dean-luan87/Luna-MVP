# -*- coding: utf-8 -*-
"""Runtime trace check dryrun."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_dryrun_common_v1 import (
    ABORT_ROLLBACK,
    base_trace,
)


def run_runtime_trace_check_dryrun(
    *,
    fixture: Dict[str, Any],
    run_id: str,
    check_results: Dict[str, Any],
) -> Dict[str, Any]:
    trace = base_trace(candidate_id=fixture["model_candidate_id"], run_id=run_id)
    trace.update({
        "dependency_check_result": check_results.get("dependency"),
        "weight_check_result": check_results.get("weight"),
        "license_check_result": check_results.get("license"),
        "input_boundary_result": check_results.get("input"),
        "output_boundary_result": check_results.get("output"),
        "normalization_check_result": check_results.get("normalization"),
        "schema_check_result": check_results.get("schema"),
        "leak_check_result": check_results.get("leak"),
        "abort_reason": check_results.get("abort_reason"),
        "rollback_action": ABORT_ROLLBACK["rollback_action"],
    })
    return trace
