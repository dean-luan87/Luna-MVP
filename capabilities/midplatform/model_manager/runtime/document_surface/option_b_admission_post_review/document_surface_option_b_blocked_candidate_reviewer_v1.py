# -*- coding: utf-8 -*-
"""Document Surface — Option B blocked candidate reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List


BLOCKED_EXPECTATIONS = {
    "family_a_requires_uncontrolled_binary": {
        "status": "blocked_dependency_not_admitted_candidate",
        "checks": ["no_install", "no_download", "no_execution", "abort_complete"],
    },
    "family_b_lightweight_sam_like_weight_missing": {
        "status": "blocked_model_weight_missing_candidate",
        "checks": ["no_weight_download", "next_action_planning"],
    },
    "family_b_sam_like_license_unknown": {
        "status": "blocked_license_not_cleared_candidate",
        "checks": ["no_preflight", "forbidden_ignore_license"],
    },
    "family_b_sam_like_caption_or_text_default": {
        "status": "blocked_or_requires_wrapper_candidate",
        "checks": ["wrapper_required", "raw_not_downstream", "wrapper_missing_blocked"],
    },
    "family_c_document_model_outputs_document_type_fact": {
        "status": "blocked_output_contract_violation_candidate",
        "checks": ["no_fact_downstream", "no_normalization_disguise"],
    },
    "family_d_depth_geometric_requires_hardware": {
        "status": "blocked_hardware_requirement_missing_candidate",
        "checks": ["no_hardware_bypass", "no_forced_execution"],
    },
}


def _get(results: List[Dict[str, Any]], cid: str) -> Dict[str, Any]:
    return next((r for r in results if r.get("model_candidate_id") == cid), {})


def _review_one(cid: str, r: Dict[str, Any], spec: Dict[str, Any]) -> Dict[str, Any]:
    dep = r.get("dependency_admission") or {}
    abort = r.get("abort_rollback") or {}
    wrapper = r.get("wrapper_requirement") or {}
    contract = r.get("output_contract") or {}
    status_ok = r.get("admission_status_candidate") == spec["status"]
    detail: Dict[str, Any] = {"status_ok": status_ok, "expected_status": spec["status"]}
    if "no_install" in spec["checks"]:
        detail["no_install"] = dep.get("install_allowed") is False
        detail["no_download"] = dep.get("download_allowed") is False
        detail["no_execution"] = dep.get("execution_allowed") is False
        detail["abort_complete"] = bool(abort.get("abort_reason") and abort.get("rollback_action"))
    if "no_weight_download" in spec["checks"]:
        detail["no_weight_download"] = dep.get("download_allowed") is False
        detail["next_action_planning"] = "planning" in str(abort.get("next_action", "")).lower() or "review" in str(abort.get("next_action", "")).lower()
    if "no_preflight" in spec["checks"]:
        detail["no_preflight"] = r.get("admission_status_candidate", "").startswith("blocked")
        detail["forbidden_ignore_license"] = "license" in str(abort.get("forbidden_workaround", "")).lower() or "download" in str(abort.get("forbidden_workaround", "")).lower()
    if "wrapper_required" in spec["checks"]:
        detail["wrapper_required"] = wrapper.get("wrapper_required") is True
        detail["raw_not_downstream"] = wrapper.get("raw_output_not_allowed_downstream") is True
        detail["wrapper_missing_blocked"] = wrapper.get("wrapper_missing_blocked") is True
    if "no_fact_downstream" in spec["checks"]:
        detail["no_fact_downstream"] = contract.get("contract_compliant") is False
        detail["no_normalization_disguise"] = r.get("admission_status_candidate") == "blocked_output_contract_violation_candidate"
    if "no_hardware_bypass" in spec["checks"]:
        detail["no_hardware_bypass"] = r.get("admission_status_candidate") == "blocked_hardware_requirement_missing_candidate"
        detail["no_forced_execution"] = r.get("execution_allowed") is False
    detail["passed"] = status_ok and all(v for k, v in detail.items() if k not in ("passed", "expected_status"))
    return {"model_candidate_id": cid, **detail}


def review_blocked_candidates(*, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    per: List[Dict[str, Any]] = []
    for cid, spec in BLOCKED_EXPECTATIONS.items():
        per.append(_review_one(cid, _get(results, cid), spec))
    checks = {
        "blocked_count_6": len(per) == 6,
        "all_status_correct": all(p.get("status_ok") for p in per),
        "all_detail_passed": all(p.get("passed") for p in per),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_blocked_candidate_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "per_candidate": per,
        "blocked_candidate_count": 6,
        "candidate_only": True,
        "not_fact": True,
    }
