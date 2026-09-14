# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B candidate route dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_admission_dryrun_v1 import (
    run_option_b_admission_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_candidate_route_dryrun_adapter_v1 import (
    run_option_b_candidate_route_dryrun,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_a_b_conflict_policy_v1 import (
    apply_ab_conflict_policy,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_output_contract_v1 import (
    validate_option_b_output_contract,
)
from capabilities.midplatform.model_manager.runtime.document_surface.option_b_candidate_route_dryrun.document_surface_option_b_route_selector_v1 import (
    select_route_candidate,
)


def _find(cases: List[Dict[str, Any]], profile: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_profile") == profile), {})


def run_processor() -> Dict[str, Any]:
    return run_option_b_candidate_route_dryrun(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    a = run_option_b_admission_dryrun(case_profile="case_a_clear_edges")
    return {
        "candidate_route_only": a.get("option_b_status") == "candidate_route_only",
        "execution_forbidden": a.get("execution_allowed") is False,
        "admission_required": a.get("dependency_admission_required") is True,
        "no_active_model": a.get("active_model_id") is None,
    }


def run_case_b() -> Dict[str, Any]:
    c = validate_option_b_output_contract({"output_types": [
        "surface_mask_candidate", "document_surface_candidate", "boundary_candidate",
    ]})
    bad = validate_option_b_output_contract({"output_types": ["ocr_text"], "ocr_text": "x"})
    return {
        "allowed_ok": c.get("contract_compliant") is True,
        "forbidden_blocked": bad.get("contract_compliant") is False,
    }


def run_case_c() -> Dict[str, Any]:
    r = select_route_candidate(case_profile="case_a_clear_edges")
    return {
        "route_candidate_only": r.get("execution_decision") is None,
        "no_execution_decision": r.get("execution_decision") is None,
        "validation_required": r.get("validation_required") is True,
    }


def run_case_d() -> Dict[str, Any]:
    route = select_route_candidate(case_profile="case_b_low_overlap")
    conflict = apply_ab_conflict_policy(
        option_a_result={"surface_count": 3, "status": "ok"},
        option_b_route=route,
    )
    return {
        "validation_review": conflict.get("conflict_resolution") == "validation_review",
        "no_confidence_override": conflict.get("confidence_auto_override") is False,
        "no_silent_fallback": conflict.get("silent_fallback") is False,
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_candidate_route_dryrun(write_outputs=False)
    cases = r.get("case_results", [])
    ca = _find(cases, "case_a_clear_edges")
    cc = _find(cases, "case_c_high_overlap")
    cf = _find(cases, "case_f_receipt_clear")
    return {
        "a_b_recommended": (ca.get("route_selection") or {}).get("option_b_recommended") is True,
        "c_b_recommended": (cc.get("route_selection") or {}).get("option_b_recommended") is True,
        "f_b_recommended": (cf.get("route_selection") or {}).get("option_b_recommended") is True,
        "no_execution": (ca.get("admission") or {}).get("execution_allowed") is False,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_candidate_route_dryrun(write_outputs=False)
    cases = r.get("case_results", [])
    cb = _find(cases, "case_b_low_overlap")
    ce = _find(cases, "case_e_texture_false_positive")
    ch = _find(cases, "case_h_screen_control")
    return {
        "b_conflict_review": (cb.get("conflict_policy") or {}).get("validation_review_required") is True,
        "e_not_default_b": (ce.get("route_selection") or {}).get("option_b_recommended") is False,
        "h_defer": (ch.get("route_selection") or {}).get("selected_route_candidate") == "defer_screen_surface_detector",
        "h_fixture_correction": "fixture_semantic" in str((ch.get("route_selection") or {}).get("route_reason_candidate", "")),
    }


def run_case_g() -> Dict[str, Any]:
    m = run_option_b_candidate_route_dryrun(write_outputs=False).get("metrics") or {}
    return {
        "exec_block": m.get("option_b_execution_block_rate") == 1.0,
        "download_block": m.get("option_b_model_download_block_rate") == 1.0,
        "registry_block": m.get("option_b_active_registry_block_rate") == 1.0,
        "no_leak": m.get("option_b_no_ocr_leak_rate") == 1.0 and m.get("option_b_no_vlm_leak_rate") == 1.0,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_candidate_route_dryrun(write_outputs=False)
    return {
        "protocol": r.get("protocol_compliance_passed") is True,
        "chain_extension": r.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": r.get("protocol_patch_not_new_branch") is True,
        "candidate_only": r.get("candidate_only") is True,
        "not_fact": r.get("not_fact") is True,
    }
