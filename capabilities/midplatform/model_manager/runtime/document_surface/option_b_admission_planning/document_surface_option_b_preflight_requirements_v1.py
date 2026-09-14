# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight requirements v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_preflight_requirements() -> Dict[str, Any]:
    checks: List[str] = [
        "dependency_availability_check",
        "model_weight_presence_check",
        "license_check",
        "input_boundary_check",
        "output_boundary_check",
        "raw_output_normalization_check",
        "candidate_schema_compliance_check",
        "no_ocr_text_leak_check",
        "no_semantic_fact_leak_check",
        "runtime_trace_check",
        "abort_policy_check",
        "rollback_policy_check",
    ]
    return {
        "requirements_id": "document_surface_option_b_preflight_requirements_v1",
        "preflight_required_before_controlled_execution": True,
        "preflight_skip_forbidden": True,
        "check_count": len(checks),
        "checks": checks,
        "all_checks_required": len(checks) >= 12,
        "candidate_only": True,
        "not_fact": True,
    }
