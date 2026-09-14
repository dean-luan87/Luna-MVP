# -*- coding: utf-8 -*-
"""Document Surface — Option B dependency/permission post-reviewer v1."""

from __future__ import annotations

from typing import Any, Dict

DENIED_IDS = {
    "family_a_requires_uncontrolled_binary",
    "family_b_lightweight_sam_like_weight_missing",
    "family_b_sam_like_license_unknown",
    "family_d_depth_geometric_requires_hardware",
}


def review_dependency_permission(
    *,
    dependency_results: Dict[str, Any],
    permission_results: Dict[str, Any],
) -> Dict[str, Any]:
    records = {r["model_candidate_id"]: r for r in (dependency_results.get("records") or [])}
    checks: Dict[str, bool] = {}
    for cid in DENIED_IDS:
        checks[f"{cid}_denied"] = records.get(cid, {}).get("permission_mapping") == "permission_denied_candidate"
    checks.update({
        "no_install_escalation": dependency_results.get("no_install_escalation") is True,
        "no_download_escalation": dependency_results.get("no_download_escalation") is True,
        "no_execution_escalation": dependency_results.get("no_execution_escalation") is True,
        "permission_mapping_complete": permission_results.get("no_permission_escalation") is True,
    })
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_dependency_permission_post_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "candidate_only": True,
        "not_fact": True,
    }
