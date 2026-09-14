# -*- coding: utf-8 -*-
"""Document Surface — Option B admission boundary reviewer v1."""

from __future__ import annotations

from typing import Any, Dict


def review_admission_boundary(*, dryrun_summary: Dict[str, Any]) -> Dict[str, Any]:
    checks = {
        "no_option_b_execution": dryrun_summary.get("option_b_execution_allowed") is False,
        "no_segmentation_execution": dryrun_summary.get("segmentation_execution_forbidden") is True,
        "no_active_model_selection": dryrun_summary.get("option_b_active_model_selected") is False,
        "no_model_download": dryrun_summary.get("model_download_forbidden") is True,
        "no_dependency_install": dryrun_summary.get("dependency_install_forbidden") is True,
        "no_preflight_execution": dryrun_summary.get("preflight_execution_forbidden") is True,
        "no_controlled_execution": dryrun_summary.get("controlled_execution_forbidden") is True,
        "no_runtime_activation": dryrun_summary.get("runtime_activation_allowed") is False,
        "admission_dryrun_only": dryrun_summary.get("admission_dryrun_only") is True,
        "boundary_frozen": dryrun_summary.get("boundary_status") == "frozen",
        "protocol_compliance": dryrun_summary.get("protocol_compliance_passed") is True,
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_admission_boundary_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
