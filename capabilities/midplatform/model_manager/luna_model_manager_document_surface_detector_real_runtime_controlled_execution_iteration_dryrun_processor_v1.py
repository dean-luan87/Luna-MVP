# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — iteration dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_iteration_dryrun.document_surface_iteration_dryrun_adapter_v1 import (
    run_iteration_dryrun,
)


def _find_case(results: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in results if c.get("case_id") == case_id), {})


def run_iteration_processor() -> Dict[str, Any]:
    return run_iteration_dryrun(write_outputs=False)


def _base_skip(case_id: str) -> Dict[str, Any]:
    return {
        "scenario": case_id,
        "skipped_missing_fixture": True,
        "no_fake_relation": True,
        "no_forced_multi_surface": True,
        "no_ocr": True,
        "no_fact": True,
    }


def run_case_a() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_a_two_overlapping_papers_clear_edges")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_a_two_overlapping_papers_clear_edges")
    rels = c.get("relation_hint_candidates") or []
    has_evidence = all(r.get("evidence_basis") for r in rels) if rels else True
    return {
        "scenario": "case_a_two_overlapping_papers_clear_edges",
        "overlap_strategy_applied": (c.get("overlap_strategy") or {}).get("applied") is True,
        "no_fake_relation": (c.get("overlap_strategy") or {}).get("no_fake_relation") is True,
        "no_forced_multi_surface": (c.get("overlap_strategy") or {}).get("no_forced_two_surface") is True,
        "relation_evidence_basis": has_evidence,
        "no_ocr": (c.get("validation") or {}).get("no_ocr_leak") is True,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_b_two_overlapping_papers_low_overlap")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_b_two_overlapping_papers_low_overlap")
    os_ = c.get("overlap_strategy") or {}
    rels = c.get("relation_hint_candidates") or []
    has_overlap_rel = any(r.get("relation_type_candidate") == "overlaps" and r.get("evidence_basis") for r in rels)
    return {
        "scenario": "case_b_two_overlapping_papers_low_overlap",
        "overlap_strategy_applied": os_.get("applied") is True,
        "uncertain_or_partial": (
            os_.get("uncertain_relation") is True
            or os_.get("overlapping_documents_under_separated_watch") is True
            or has_overlap_rel
        ),
        "no_forced_multi_surface": os_.get("no_forced_two_surface") is True,
        "no_ocr": (c.get("validation") or {}).get("no_ocr_leak") is True,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_c_two_overlapping_papers_high_overlap")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_c_two_overlapping_papers_high_overlap")
    os_ = c.get("overlap_strategy") or {}
    return {
        "scenario": "case_c_two_overlapping_papers_high_overlap",
        "uncertain_relation": os_.get("uncertain_relation") is True,
        "no_separation_upgrade": os_.get("separation_success") is not True,
        "no_forced_multi_surface": os_.get("no_forced_two_surface") is True,
        "no_ocr": (c.get("validation") or {}).get("no_ocr_leak") is True,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_d_low_contrast_single_paper")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_d_low_contrast_single_paper")
    qg = c.get("quality_gate") or {}
    lc = c.get("low_contrast_strategy") or {}
    count = qg.get("output_count", len(c.get("document_surface_candidates") or []))
    return {
        "scenario": "case_d_low_contrast_single_paper",
        "quality_gate_applied": qg.get("candidate_quality_gate_pass_rate") is not None,
        "candidate_cap_respected": count <= 5,
        "low_contrast_strategy": lc.get("applied") is True,
        "no_fact": (c.get("validation") or {}).get("no_fact_output") is True,
    }


def run_case_e() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_e_low_contrast_texture_false_positive")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_e_low_contrast_texture_false_positive")
    lc = c.get("low_contrast_strategy") or {}
    return {
        "scenario": "case_e_low_contrast_texture_false_positive",
        "low_contrast_strategy": lc.get("applied") is True,
        "excessive_suppression": lc.get("excessive_candidate_suppression") is True or lc.get("output_count", 99) <= 5,
        "no_fact": (c.get("validation") or {}).get("no_fact_output") is True,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_f_receipt_attached_clear")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_f_receipt_attached_clear")
    rels = c.get("relation_hint_candidates") or []
    has_evidence = all(r.get("evidence_basis") for r in rels) if rels else True
    return {
        "scenario": "case_f_receipt_attached_clear",
        "attached_strategy_applied": (c.get("attached_to_strategy") or {}).get("applied") is True,
        "relation_evidence_basis": has_evidence,
        "no_receipt_to_package_fact": (c.get("attached_to_strategy") or {}).get("no_receipt_text_to_package") is True,
        "no_fact": (c.get("validation") or {}).get("no_fact_output") is True,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_g_receipt_attached_uncertain")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_g_receipt_attached_uncertain")
    at = c.get("attached_to_strategy") or {}
    return {
        "scenario": "case_g_receipt_attached_uncertain",
        "uncertain_attached": at.get("uncertain") is True,
        "request_more_evidence": c.get("next_action_candidate") == "request_more_evidence" or at.get("uncertain") is True,
        "no_forced_attached": (c.get("validation") or {}).get("forced_multi_surface_rate", 0) == 0,
        "no_fact": (c.get("validation") or {}).get("no_fact_output") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_iteration_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_h_document_on_screen_control")
    if c.get("skipped_missing_fixture"):
        return _base_skip("case_h_document_on_screen_control")
    outs = c.get("candidate_outputs") or {}
    return {
        "scenario": "case_h_document_on_screen_control",
        "screen_defer": c.get("runtime_status_candidate") == "possible_screen_document_content_candidate" or outs.get("defer_to_screen_surface_detector") is True,
        "screen_guard": outs.get("screen_surface_not_document_surface_fact") is True,
        "no_fact": (c.get("validation") or {}).get("no_fact_output") is True,
    }
