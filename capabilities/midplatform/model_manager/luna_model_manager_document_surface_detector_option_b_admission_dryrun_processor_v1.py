# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B admission dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.luna_model_manager_document_surface_detector_option_b_admission_dryrun_types_v1 import (
    REQUIRED_FIXTURE_FIELDS,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_admission_dryrun.document_surface_option_b_admission_dryrun_adapter_v1 import (
    run_option_b_admission_dryrun,
)


def _by_id(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {r["model_candidate_id"]: r for r in results}


def run_processor() -> Dict[str, Any]:
    return run_option_b_admission_dryrun(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    fixtures = (r.get("registry") or {}).get("fixtures") or []
    complete = all(all(f.get(k) is not None for k in REQUIRED_FIXTURE_FIELDS) for f in fixtures)
    return {
        "count": len(fixtures) == 8,
        "registry_complete": complete,
        "active_false": all(f.get("active_status") is False for f in fixtures),
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    m = _by_id(r.get("results") or [])
    a1 = m.get("family_a_classical_helper_ok_candidate", {})
    c1 = m.get("family_c_document_specific_surface_model_ok_for_preflight", {})
    return {
        "a1_admitted": a1.get("admission_status_candidate") == "admitted_for_preflight_candidate",
        "c1_admitted": c1.get("admission_status_candidate") == "admitted_for_preflight_candidate",
        "no_execution": all(x.get("execution_allowed") is False for x in (a1, c1) if x),
        "no_active": all(x.get("active_model_selected") is False for x in (a1, c1) if x),
    }


def run_case_c() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    a2 = _by_id(r.get("results") or {}).get("family_a_requires_uncontrolled_binary", {})
    dep = a2.get("dependency_admission") or {}
    return {
        "blocked": a2.get("admission_status_candidate") == "blocked_dependency_not_admitted_candidate",
        "no_install": dep.get("install_allowed") is False,
        "no_download": dep.get("download_allowed") is False,
        "no_execution": dep.get("execution_allowed") is False,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    m = _by_id(r.get("results") or {})
    b1 = m.get("family_b_lightweight_sam_like_weight_missing", {})
    b2 = m.get("family_b_sam_like_license_unknown", {})
    d1 = m.get("family_d_depth_geometric_requires_hardware", {})
    return {
        "b1_weight": b1.get("admission_status_candidate") == "blocked_model_weight_missing_candidate",
        "b2_license": b2.get("admission_status_candidate") == "blocked_license_not_cleared_candidate",
        "d1_hardware": d1.get("admission_status_candidate") == "blocked_hardware_requirement_missing_candidate",
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    c2 = _by_id(r.get("results") or {}).get("family_c_document_model_outputs_document_type_fact", {})
    contract = c2.get("output_contract") or {}
    return {
        "blocked": c2.get("admission_status_candidate") == "blocked_output_contract_violation_candidate",
        "no_fact_downstream": contract.get("contract_compliant") is False,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    b3 = _by_id(r.get("results") or {}).get("family_b_sam_like_caption_or_text_default", {})
    wrapper = b3.get("wrapper_requirement") or {}
    return {
        "blocked_or_wrapper": b3.get("admission_status_candidate") == "blocked_or_requires_wrapper_candidate",
        "wrapper_required": wrapper.get("wrapper_required") is True,
        "raw_not_downstream": wrapper.get("raw_output_not_allowed_downstream") is True,
        "not_direct_preflight": b3.get("admission_status_candidate") != "admitted_for_preflight_candidate",
        "wrapper_missing_blocked": wrapper.get("wrapper_missing_blocked") is True,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    blocked = [x for x in (r.get("results") or []) if str(x.get("admission_status_candidate", "")).startswith("blocked")]
    abort_ok = all(
        (x.get("abort_rollback") or {}).get("abort_reason")
        and (x.get("abort_rollback") or {}).get("next_action")
        and (x.get("abort_rollback") or {}).get("forbidden_workaround")
        and (x.get("abort_rollback") or {}).get("rollback_action")
        for x in blocked
    )
    rollback_ok = all(
        (x.get("abort_rollback") or {}).get("no_active_registry_update") is True
        and (x.get("abort_rollback") or {}).get("no_runtime_activation") is True
        and (x.get("abort_rollback") or {}).get("no_silent_fallback_to_option_a") is True
        and (x.get("abort_rollback") or {}).get("no_fallback_to_ocr_vlm_layout") is True
        for x in blocked
    )
    return {
        "blocked_count": len(blocked) == 6,
        "abort_complete": abort_ok,
        "rollback_complete": rollback_ok,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_admission_dryrun(write_outputs=False)
    return {
        "protocol": r.get("protocol_compliance_check") == "required",
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "branch": r.get("protocol_patch_not_new_branch") is True,
        "co": r.get("candidate_only") is True,
        "nf": r.get("not_fact") is True,
        "next_not_execution": "Post-Review" in str(r.get("recommended_next_phase") or ""),
    }
