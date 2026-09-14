# -*- coding: utf-8 -*-
"""Document Surface — Option B runtime boundary post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})


def review_runtime_boundary(*, runtime_results: Dict[str, Any]) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = runtime_results.get("records") or []
    preflight = [r for r in records if r.get("model_candidate_id") in PREFLIGHT_IDS]
    checks = {
        "activation_count_0": runtime_results.get("runtime_activation_count") == 0,
        "all_execution_blocked": runtime_results.get("all_execution_blocked") is True,
        "all_controlled_blocked": runtime_results.get("all_controlled_execution_blocked") is True,
        "boundary_closed": all(r.get("runtime_boundary_status") == "closed" for r in records),
        "preflight_required": all(r.get("preflight_required") is True for r in records),
        "a1_c1_preflight_planning_ok": all(
            r.get("preflight_planning_may_be_recommended") is True
            and r.get("execution_cannot_be_recommended") is True
            for r in preflight
        ),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_runtime_boundary_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
