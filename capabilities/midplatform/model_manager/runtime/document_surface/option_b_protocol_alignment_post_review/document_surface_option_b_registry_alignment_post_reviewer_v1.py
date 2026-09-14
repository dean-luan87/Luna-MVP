# -*- coding: utf-8 -*-
"""Document Surface — Option B registry alignment post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List

PREFLIGHT_IDS = frozenset({
    "family_a_classical_helper_ok_candidate",
    "family_c_document_specific_surface_model_ok_for_preflight",
})


def review_registry_alignment(*, registry_results: Dict[str, Any]) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = registry_results.get("records") or []
    checks = {
        "no_active_model_id": registry_results.get("active_model_id_generated") is False,
        "no_active_skill_id": registry_results.get("active_skill_id_generated") is False,
        "update_count_0": registry_results.get("active_registry_update_count") == 0,
        "candidate_only_status": all(p.get("registry_alignment_status") == "candidate_only" for p in records),
        "a1_c1_candidate_allowed": all(
            p.get("candidate_registry_allowed") is True
            for p in records if p.get("model_candidate_id") in PREFLIGHT_IDS
        ),
        "all_active_blocked": all(p.get("active_registry_allowed") is False for p in records),
        "no_runtime_registry_update": all(p.get("runtime_registry_updated") is False for p in records),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_registry_alignment_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
