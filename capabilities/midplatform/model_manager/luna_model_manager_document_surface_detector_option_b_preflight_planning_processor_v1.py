# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B preflight planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_planning.document_surface_option_b_preflight_planning_adapter_v1 import (
    run_option_b_preflight_planning,
)


def run_processor() -> Dict[str, Any]:
    return run_option_b_preflight_planning(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    s = r.get("scope") or {}
    return {
        "count_2": s.get("preflight_candidate_count") == 2,
        "blocked_excluded": s.get("blocked_excluded_from_preflight") is True,
        "no_active": s.get("active_model_selected") is False and s.get("active_skill_selected") is False,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    d, w, l = r.get("dependency_plan") or {}, r.get("weight_plan") or {}, r.get("license_plan") or {}
    return {
        "dep": d.get("check_type") == "dependency_availability_check",
        "weight": w.get("check_type") == "model_weight_presence_check",
        "license": l.get("check_type") == "license_check",
        "no_install": d.get("install_allowed") is False,
        "no_download": d.get("download_allowed") is False and w.get("download_allowed", False) is False,
        "abort": len(d.get("abort_on") or []) >= 2,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    inp, out = r.get("input_plan") or {}, r.get("output_plan") or {}
    return {
        "no_image": inp.get("image_read_allowed") is False,
        "metadata": any("metadata" in str(rule) for rule in (inp.get("rules") or [])),
        "tmp_out": "_tmp_eval_out" in (out.get("allowed_output_scope") or []),
        "no_active_reg": out.get("active_registry_update_allowed") is False,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    n = r.get("normalization_plan") or {}
    return {
        "no_downstream": n.get("raw_output_downstream_allowed") is False,
        "wrapper_abort": "wrapper_missing" in (n.get("abort_on") or []),
        "caption": "caption" in str(n.get("abort_or_requires_wrapper_on") or n.get("rules") or ""),
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    sc, lk = r.get("schema_plan") or {}, r.get("leak_plan") or {}
    return {
        "allowed_6": len(sc.get("allowed_output_types") or []) >= 6,
        "forbidden": "ocr_text" in (sc.get("forbidden_output_types") or []),
        "leak_abort": "text_or_fact_leak_detected" in (lk.get("abort_on") or []),
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    t = r.get("trace_plan") or {}
    fd = t.get("frozen_defaults") or {}
    return {
        "fields": len(t.get("required_trace_fields") or []) >= 16,
        "no_exec": fd.get("execution_performed") is False,
        "no_seg": fd.get("segmentation_performed") is False,
        "no_active": fd.get("active_model_selected") is False,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    a = r.get("abort_policy") or {}
    rb = a.get("rollback_policy") or {}
    return {
        "abort_16": len(a.get("abort_conditions") or []) >= 16,
        "no_registry": rb.get("no_active_registry_update") is True,
        "no_fallback": rb.get("no_fallback_to_ocr_vlm_layout") is True,
        "no_option_a": rb.get("no_silent_fallback_to_option_a") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_preflight_planning(write_outputs=False)
    return {
        "protocol": r.get("protocol_compliance_check") == "required",
        "contract": r.get("primary_contract") is not None,
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "branch": r.get("protocol_patch_not_new_branch") is True,
        "next_dryrun": "DryRun" in str(r.get("recommended_next_phase") or ""),
        "no_exec": r.get("preflight_execution_allowed") is False,
    }
