# -*- coding: utf-8 -*-
"""Document Surface — Option B abort/rollback dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, Optional


def build_abort_rollback_dryrun(
    *,
    admission_status: str,
    abort_reason: Optional[str] = None,
) -> Dict[str, Any]:
    if admission_status.startswith("admitted"):
        return {
            "abort_reason": None,
            "next_action": "proceed_to_preflight_planning_only",
            "forbidden_workaround": "skip_preflight_or_execute_directly",
            "rollback_action": None,
            "no_active_registry_update": True,
            "no_runtime_activation": True,
            "no_silent_fallback_to_option_a": True,
            "no_fallback_to_ocr_vlm_layout": True,
            "trace_retained": True,
            "candidate_only": True,
            "not_fact": True,
        }
    return {
        "abort_reason": abort_reason or admission_status,
        "next_action": "return_to_admission_planning_or_candidate_review",
        "forbidden_workaround": "download_anyway_or_force_execution",
        "rollback_action": "retain_trace_return_to_admission_planning",
        "no_active_registry_update": True,
        "no_runtime_activation": True,
        "no_silent_fallback_to_option_a": True,
        "no_fallback_to_ocr_vlm_layout": True,
        "trace_retained": True,
        "candidate_only": True,
        "not_fact": True,
    }
