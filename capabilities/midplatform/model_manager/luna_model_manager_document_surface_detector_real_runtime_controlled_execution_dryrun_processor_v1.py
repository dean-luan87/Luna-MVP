# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — controlled execution dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.document_surface.controlled_execution_dryrun.document_surface_controlled_execution_dryrun_adapter_v1 import (
    DRYRUN_CASES,
    run_controlled_execution_dryrun,
)


def _find_case(results: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in results if c.get("case_id") == case_id), {})


def run_dryrun_processor() -> Dict[str, Any]:
    return run_controlled_execution_dryrun(write_outputs=False)


def run_case_a() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_a_single_flat_paper_controlled")
    fixtures_ready = r.get("fixture_audit", {}).get("execution_fixtures_ready") is True
    if not fixtures_ready:
        return {
            "scenario": "case_a_single_flat_paper_controlled",
            "skipped_missing_fixture": c.get("skipped_missing_fixture") is True,
            "no_fake_image_generated": True,
            "no_ocr": c.get("validation", {}).get("no_ocr_leak") is True,
        }
    outs = c.get("candidate_outputs") or {}
    surfaces = outs.get("document_surface_candidates") or []
    return {
        "scenario": "case_a_single_flat_paper_controlled",
        "cv2_executed": c.get("cv2_processing_executed") is True,
        "has_candidate": len(surfaces) >= 1 or outs.get("runtime_status_candidate") == "low_confidence_boundary_candidate",
        "candidate_only": True,
        "no_ocr": c.get("validation", {}).get("no_ocr_leak") is True,
    }


def run_case_b() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_b_two_overlapping_papers_controlled")
    if not r.get("fixture_audit", {}).get("execution_fixtures_ready"):
        return {"scenario": "case_b_two_overlapping_papers_controlled", "skipped_missing_fixture": True, "no_merge": True, "no_ocr": True}
    outs = c.get("candidate_outputs") or {}
    return {
        "scenario": "case_b_two_overlapping_papers_controlled",
        "has_surfaces_or_uncertain": bool(outs.get("document_surface_candidates")) or "uncertain" in str(outs.get("runtime_status_candidate", "")),
        "relation_hints": bool(outs.get("relation_hint_candidates")),
        "no_merge": "merged_document" not in str(outs),
        "no_ocr": c.get("validation", {}).get("no_ocr_leak") is True,
    }


def run_case_c() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_c_low_contrast_paper_controlled")
    if not r.get("fixture_audit", {}).get("execution_fixtures_ready"):
        return {"scenario": "case_c_low_contrast_paper_controlled", "skipped_missing_fixture": True, "no_fact": True}
    outs = c.get("candidate_outputs") or {}
    status = outs.get("runtime_status_candidate", "")
    return {
        "scenario": "case_c_low_contrast_paper_controlled",
        "low_conf_or_evidence": "low_confidence" in status or "evidence" in status,
        "no_fact": c.get("validation", {}).get("no_fact_output") is True,
    }


def run_case_d() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_d_receipt_attached_to_package_controlled")
    if not r.get("fixture_audit", {}).get("execution_fixtures_ready"):
        return {"scenario": "case_d_receipt_attached_to_package_controlled", "skipped_missing_fixture": True, "no_package_fact": True}
    rels = (c.get("candidate_outputs") or {}).get("relation_hint_candidates") or []
    rel_types = {x.get("relation_type_candidate") for x in rels}
    return {
        "scenario": "case_d_receipt_attached_to_package_controlled",
        "relation_hint": bool(rel_types & {"attached_to", "uncertain"}),
        "no_package_fact": c.get("validation", {}).get("no_fact_output") is True,
    }


def run_case_e() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_e_document_on_screen_controlled")
    if not r.get("fixture_audit", {}).get("execution_fixtures_ready"):
        return {"scenario": "case_e_document_on_screen_controlled", "skipped_missing_fixture": True, "no_screen_fact": True}
    outs = c.get("candidate_outputs") or {}
    return {
        "scenario": "case_e_document_on_screen_controlled",
        "screen_candidate": "screen" in str(outs.get("runtime_status_candidate", "")).lower() or outs.get("possible_screen_document_content"),
        "no_screen_fact": c.get("validation", {}).get("no_fact_output") is True,
    }


def run_case_f() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_f_attention_blocked_controlled")
    return {
        "scenario": "case_f_attention_blocked_controlled",
        "runtime_call_zero": c.get("runtime_call_count", 1) == 0,
        "no_cv2": c.get("cv2_processing_executed") is False,
        "no_read": c.get("no_image_content_read") is True,
        "skipped": c.get("skipped_by_attention_gate") is True,
    }


def run_case_g() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_g_unsupported_format_controlled")
    return {
        "scenario": "case_g_unsupported_format_controlled",
        "aborted": c.get("abort_status") == "aborted",
        "unsupported": c.get("abort_reason") == "unsupported_image_format",
        "no_fallback": c.get("validation", {}).get("no_fallback") is True,
    }


def run_case_h() -> Dict[str, Any]:
    r = run_controlled_execution_dryrun(write_outputs=False)
    c = _find_case(r.get("case_results", []), "case_h_image_read_failed_controlled")
    return {
        "scenario": "case_h_image_read_failed_controlled",
        "aborted": c.get("abort_status") == "aborted",
        "read_failed": c.get("abort_reason") == "image_read_failed",
        "trace_retained": c.get("failure_trace_retained") is True or bool(c.get("trace")),
        "no_fallback": c.get("validation", {}).get("no_fallback") is True,
    }
