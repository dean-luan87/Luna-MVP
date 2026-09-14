# -*- coding: utf-8 -*-
"""Luna Document Surface — iteration planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_planning.document_surface_iteration_planning_adapter_v1 import (
    run_iteration_planning,
)


def run_risk_mapping_case() -> Dict[str, Any]:
    r = run_iteration_planning(write_outputs=False)
    m = r.get("risk_mapping") or {}
    return {
        "scenario": "case_a_post_review_risk_mapping",
        "bcd_mapped": m.get("all_case_bcd_mapped") is True,
        "watch_retained": m.get("non_blocker_watch_retained") is True,
        "count": m.get("mapping_count", 0) >= 7,
    }


def run_overlap_separation_case() -> Dict[str, Any]:
    o = (run_iteration_planning(write_outputs=False).get("overlap_strategy") or {})
    return {
        "scenario": "case_b_overlap_separation_planning",
        "two_phase": len(o.get("two_phase_strategy") or []) >= 3,
        "uncertain_allowed": o.get("relation_policy", {}).get("fallback") == "overlap_relation_uncertain_candidate",
        "no_fake": o.get("does_not_fake_relation") is True,
        "no_forced": "no_forced_two_surface_output" in (o.get("forbidden") or []),
    }


def run_low_contrast_case() -> Dict[str, Any]:
    l = (run_iteration_planning(write_outputs=False).get("low_contrast_strategy") or {})
    return {
        "scenario": "case_c_low_contrast_noise_planning",
        "suppression": len(l.get("suppression_strategy") or []) >= 3,
        "uncertain_path": l.get("uncertainty_path", {}).get("preserve_uncertain_candidate_path") is True,
        "not_accuracy_only": l.get("accuracy_not_admission_criterion") is True,
    }


def run_attached_to_case() -> Dict[str, Any]:
    a = (run_iteration_planning(write_outputs=False).get("attached_strategy") or {})
    return {
        "scenario": "case_d_attached_to_uncertainty_planning",
        "evidence_req": len(a.get("attached_to_evidence_requirements") or []) >= 2,
        "uncertain_out": "uncertain_attached_to_candidate" in (a.get("uncertain_outputs") or []),
        "no_receipt_to_package": "do_not_assign_receipt_text_to_package" in (a.get("forbidden") or []),
    }


def run_relation_constraint_case() -> Dict[str, Any]:
    rel = (run_iteration_planning(write_outputs=False).get("relation_constraints") or {})
    return {
        "scenario": "case_e_relation_constraint_planning",
        "evidence_basis": all(c.get("evidence_basis_required") for c in (rel.get("constraints") or [])),
        "no_fake": "fake_relation_to_pass_smoke" in (rel.get("forbidden") or []),
        "fake_rate_zero": rel.get("fake_relation_rate_target") == 0.0,
    }


def run_fixture_case() -> Dict[str, Any]:
    f = (run_iteration_planning(write_outputs=False).get("fixture_plan") or {})
    return {
        "scenario": "case_f_fixture_iteration_planning",
        "eight_plus": f.get("at_least_eight_categories") is True,
        "no_image": f.get("no_image_read_in_planning") is True,
        "no_real_required": f.get("no_real_image_required_in_planning") is True,
    }


def run_metrics_case() -> Dict[str, Any]:
    m = (run_iteration_planning(write_outputs=False).get("metrics_plan") or {})
    t = m.get("targets") or {}
    return {
        "scenario": "case_g_metrics_update_planning",
        "new_metrics": len(m.get("new_metrics") or []) >= 8,
        "fake_zero": t.get("fake_relation_rate") == 0.0,
        "forced_zero": t.get("forced_multi_surface_rate") == 0.0,
        "not_accuracy_only": m.get("accuracy_not_primary_admission_criterion") is True,
    }


def run_protocol_case() -> Dict[str, Any]:
    r = run_iteration_planning(write_outputs=False)
    return {
        "scenario": "case_h_protocol_compliance_retained",
        "required": r.get("protocol_compliance_check") == "required",
        "candidate_only": r.get("candidate_only") is True,
        "chain_ext": r.get("existing_midplatform_protocol_chain_extension") is True,
        "not_new_branch": r.get("protocol_patch_not_new_branch") is True,
    }
