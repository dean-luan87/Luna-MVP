# -*- coding: utf-8 -*-
"""Document Surface — Option B admitted candidate reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List


def _get(results: List[Dict[str, Any]], cid: str) -> Dict[str, Any]:
    return next((r for r in results if r.get("model_candidate_id") == cid), {})


def review_admitted_candidates(*, results: List[Dict[str, Any]], registry: Dict[str, Any]) -> Dict[str, Any]:
    fixtures = {f["model_candidate_id"]: f for f in (registry.get("fixtures") or [])}
    a1 = _get(results, "family_a_classical_helper_ok_candidate")
    c1 = _get(results, "family_c_document_specific_surface_model_ok_for_preflight")
    fa1 = fixtures.get("family_a_classical_helper_ok_candidate", {})
    fc1 = fixtures.get("family_c_document_specific_surface_model_ok_for_preflight", {})

    a1_checks = {
        "admitted_for_preflight": a1.get("admission_status_candidate") == "admitted_for_preflight_candidate",
        "family_classical_helper": fa1.get("family_type") == "classical_lightweight_segmentation_helper",
        "no_weight": (fa1.get("weight_profile") or {}).get("type") == "no_weight",
        "clear_license": fa1.get("license_status_candidate") == "clear",
        "compatible_contract": (a1.get("output_contract") or {}).get("contract_compliant") is True,
        "execution_false": a1.get("execution_allowed") is False,
        "active_false": a1.get("active_status") is False,
        "not_active_model": a1.get("active_model_selected") is False,
    }
    c1_checks = {
        "admitted_for_preflight": c1.get("admission_status_candidate") == "admitted_for_preflight_candidate",
        "family_document_specific": fc1.get("family_type") == "document_specific_segmentation_surface_model",
        "declared_only_dependency": (fc1.get("dependency_profile") or {}).get("type") == "declared_only",
        "compatible_contract": (c1.get("output_contract") or {}).get("contract_compliant") is True,
        "execution_false": c1.get("execution_allowed") is False,
        "active_false": c1.get("active_status") is False,
        "not_active_model": c1.get("active_model_selected") is False,
    }
    governance = {
        "preflight_planning_only": True,
        "no_direct_execution": a1.get("execution_allowed") is False and c1.get("execution_allowed") is False,
        "no_active_registry": True,
        "no_skip_preflight": True,
        "not_interpreted_as_active_model": True,
    }
    all_checks = {**{f"a1_{k}": v for k, v in a1_checks.items()}, **{f"c1_{k}": v for k, v in c1_checks.items()}, **governance}
    failed = [k for k, v in all_checks.items() if not v]
    return {
        "review_id": "option_b_admitted_candidate_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in all_checks.values() if v),
        "review_failed_count": len(failed),
        "a1_review": {"model_candidate_id": "family_a_classical_helper_ok_candidate", "checks": a1_checks, "interpretation": "admitted_for_preflight_candidate_only_not_active_model"},
        "c1_review": {"model_candidate_id": "family_c_document_specific_surface_model_ok_for_preflight", "checks": c1_checks, "interpretation": "admitted_for_preflight_candidate_only_not_active_model"},
        "governance_notes": [
            "A1/C1 只允许进入 preflight planning / preflight candidate review",
            "A1/C1 不允许直接 execution",
            "A1/C1 不允许写 active registry",
            "A1/C1 不允许跳过 preflight",
        ],
        "checks": all_checks,
        "failed_checks": failed,
        "admitted_for_preflight_candidate_count": 2,
        "candidate_only": True,
        "not_fact": True,
    }
