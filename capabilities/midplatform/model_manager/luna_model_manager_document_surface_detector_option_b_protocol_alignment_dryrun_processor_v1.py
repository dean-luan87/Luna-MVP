# -*- coding: utf-8 -*-
"""Luna Document Surface — Option B protocol alignment dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.option_b_protocol_alignment_dryrun.document_surface_option_b_protocol_alignment_dryrun_adapter_v1 import (
    run_option_b_protocol_alignment_dryrun,
)


def _by_id(results: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {r["model_candidate_id"]: r for r in (results.get("contract_mapping") or {}).get("records", [])}


def run_processor() -> Dict[str, Any]:
    return run_option_b_protocol_alignment_dryrun(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    c = r.get("contract_mapping") or {}
    return {
        "count": c.get("candidate_count") == 8,
        "all_mapped": c.get("all_mapped") is True,
        "preflight": c.get("preflight_candidate_count") == 2,
        "blocked": c.get("blocked_admission_record_count") == 6,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    reg = r.get("registry_alignment") or {}
    return {
        "no_active_model": reg.get("active_model_id_generated") is False,
        "no_active_skill": reg.get("active_skill_id_generated") is False,
        "no_update": reg.get("active_registry_update_count") == 0,
        "candidate_only": reg.get("candidate_registry_alignment_only") is True,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    d = r.get("dependency_mapping") or {}
    records = d.get("records") or []
    denied = [x for x in records if x.get("permission_mapping") == "permission_denied_candidate"]
    return {
        "denied_count": len(denied) >= 4,
        "no_install": d.get("no_install_escalation") is True,
        "no_download": d.get("no_download_escalation") is True,
        "no_exec": d.get("no_execution_escalation") is True,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    o = r.get("output_mapping") or {}
    records = o.get("records") or []
    b3 = next((x for x in records if x["model_candidate_id"] == "family_b_sam_like_caption_or_text_default"), {})
    c2 = next((x for x in records if x["model_candidate_id"] == "family_c_document_model_outputs_document_type_fact"), {})
    return {
        "b3_wrapper": b3.get("protocol_mapping") == "blocked_or_requires_wrapper",
        "c2_fact": c2.get("protocol_mapping") == "fact_output_blocked",
        "raw_blocked": b3.get("raw_output_not_allowed_downstream") is True,
    }


def run_case_e() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    rt = r.get("runtime_mapping") or {}
    return {
        "no_activation": rt.get("runtime_activation_count") == 0,
        "no_controlled": rt.get("all_controlled_execution_blocked") is True,
        "no_exec": rt.get("all_execution_blocked") is True,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    ch = r.get("change_control_mapping") or {}
    return {
        "dryrun_only": ch.get("change_control_status") == "planning_dryrun_only",
        "no_active": ch.get("no_active_changes") is True,
        "freeze": ch.get("freeze_boundary_respected") is True,
        "next_post_review": "Post-Review" in str(ch.get("recommended_next_phase") or ""),
        "no_preflight": ch.get("preflight_planning_not_recommended") is True,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    ev = r.get("evidence_mapping") or {}
    return {
        "refs": ev.get("admission_refs_preserved") is True,
        "protocol": ev.get("protocol_refs_preserved") is True,
        "rate": ev.get("evidence_chain_preservation_rate") == 1.0,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_option_b_protocol_alignment_dryrun(write_outputs=False)
    m = r.get("metrics") or {}
    return {
        "protocol_ref": m.get("protocol_ref_completeness_rate") == 1.0,
        "candidate_only": m.get("candidate_only_compliance_rate") == 1.0,
        "no_active_model": m.get("active_model_mapping_count") == 0,
        "no_registry": m.get("active_registry_update_count") == 0,
        "chain": r.get("existing_midplatform_protocol_chain_extension") is True,
        "branch": r.get("protocol_patch_not_new_branch") is True,
    }
