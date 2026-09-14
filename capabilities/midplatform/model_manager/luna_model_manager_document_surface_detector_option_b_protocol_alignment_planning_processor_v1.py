# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B protocol alignment planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_planning.document_surface_option_b_protocol_alignment_planning_adapter_v1 import (
    run_option_b_protocol_alignment_planning,
)


def run_processor() -> Dict[str, Any]:
    return run_option_b_protocol_alignment_planning(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    c = r.get("contract_mapping") or {}
    return {
        "primary": c.get("primary_contract") is not None,
        "mounted": c.get("local_admission_mounted") is True,
        "not_replace": c.get("local_admission_replaces_contract") is False,
        "refs": len(c.get("referenced_protocols") or []) >= 8,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    reg = r.get("registry_alignment") or {}
    return {
        "count": reg.get("fixture_count") == 8,
        "no_active": reg.get("active_registry_update_allowed") is False,
        "not_model_admitted": reg.get("admitted_for_preflight_not_equal_model_admitted") is True,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    d = r.get("dependency_mapping") or {}
    return {
        "install": d.get("all_install_blocked") is True,
        "download": d.get("all_download_blocked") is True,
        "exec": d.get("all_execution_blocked") is True,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    o = r.get("output_mapping") or {}
    return {
        "no_fact": o.get("no_fact_promotion") is True,
        "no_ocr": o.get("no_ocr_text_caption_downstream") is True,
        "allowed": len(o.get("allowed_output_types") or []) >= 6,
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    b = r.get("boundary_mapping") or {}
    fs = b.get("option_b_frozen_state") or {}
    return {
        "runtime": fs.get("runtime_activation_allowed") is False,
        "controlled": fs.get("controlled_execution_allowed") is False,
        "admission_req": fs.get("model_skill_admission_required") is True,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    ch = r.get("change_control_mapping") or {}
    return {
        "frozen": ch.get("boundary_status") == "frozen",
        "pipeline": "Model / Skill Admission Protocol Alignment" in (ch.get("adjusted_pipeline") or []),
        "skip_forbidden": ch.get("skip_protocol_alignment_forbidden") is True,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    fs = r.get("option_b_frozen_state") or {}
    return {
        "model_route": fs.get("model_candidate_route") is True,
        "skill_route": fs.get("skill_candidate_route") is True,
        "no_active_model": fs.get("active_model") is False,
        "no_active_skill": fs.get("active_skill") is False,
        "preflight": fs.get("preflight_required") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_planning(write_outputs=False)
    return {
        "protocol": r.get("protocol_compliance_check") == "required",
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "branch": r.get("protocol_patch_not_new_branch") is True,
        "review": r.get("alignment_review_passed") is True,
        "next_dryrun": "DryRun" in str(r.get("recommended_next_phase") or ""),
    }
