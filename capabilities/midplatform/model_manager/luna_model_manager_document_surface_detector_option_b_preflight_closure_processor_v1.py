# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B preflight closure processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_preflight_closure.document_surface_option_b_preflight_closure_adapter_v1 import (
    run_option_b_preflight_closure,
)


def run_processor() -> Dict[str, Any]:
    return run_option_b_preflight_closure(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    s = r.get("dryrun", {}).get("scope_results") or {}
    return {
        "count": s.get("preflight_candidate_count") == 2,
        "blocked": len(s.get("blocked_reference_ids") or []) == 6,
        "no_active": s.get("active_model_selected") is False,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    deps = r.get("dryrun", {}).get("dependency_results") or []
    return {
        "has_results": len(deps) == 2,
        "no_install": all(d.get("install_performed") is False for d in deps),
        "no_download": all(d.get("download_performed") is False for d in deps),
    }


def run_case_c() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    w = r.get("dryrun", {}).get("weight_results") or []
    l = r.get("dryrun", {}).get("license_results") or []
    return {
        "weight": len(w) == 2,
        "license": len(l) == 2,
        "no_dl": all(x.get("download_performed") is False for x in w),
    }


def run_case_d() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    inp = r.get("dryrun", {}).get("input_results") or []
    out = r.get("dryrun", {}).get("output_results") or []
    return {
        "no_image": all(i.get("image_content_read") is False for i in inp),
        "tmp_out": all("_tmp_eval_out" in str(o.get("allowed_output_scope")) for o in out),
        "no_reg": all(o.get("active_registry_write") is False for o in out),
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    n = r.get("dryrun", {}).get("normalization_results") or []
    return {
        "no_ds": all(x.get("raw_output_downstream_allowed") is False for x in n),
        "ok": all(x.get("abort_reason") is None for x in n),
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    sc = r.get("dryrun", {}).get("schema_results") or []
    lk = r.get("dryrun", {}).get("leak_results") or []
    return {
        "schema": all("compliant" in str(s.get("candidate_schema_compliance_check_candidate")) for s in sc),
        "no_leak": all(l.get("leak_detected") is False for l in lk),
    }


def run_case_g() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    tr = r.get("dryrun", {}).get("trace_results") or []
    return {
        "trace": len(tr) == 2,
        "no_exec": all(t.get("execution_performed") is False for t in tr),
        "no_seg": all(t.get("segmentation_performed") is False for t in tr),
        "no_active": all(t.get("active_model_selected") is False for t in tr),
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_preflight_closure(write_outputs=False)
    return {
        "planning": r.get("preflight_planning_decision", "").endswith("GO"),
        "dryrun": r.get("preflight_dryrun_decision", "").endswith("GO"),
        "post": r.get("preflight_post_review_decision", "").endswith("GO"),
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "next_ce": "Controlled-Execution-Planning" in str(r.get("recommended_next_phase") or ""),
        "no_exec": r.get("preflight_execution_allowed") is False,
    }
