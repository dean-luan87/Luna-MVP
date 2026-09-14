# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_planning_adapter_v1 import (
    run_document_surface_detector_planning,
)


def _pkg(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("ownership_evidence_package") or {}


def _surface_ids(pkg: Dict[str, Any]) -> List[str]:
    return [s.get("surface_id") for s in pkg.get("document_surface_candidates") or []]


def run_stacked_papers_occlusion() -> Dict[str, Any]:
    """Case A: paper_A / paper_B + occludes, no OCR."""
    result = run_document_surface_detector_planning(fixture_ref="stacked_papers")
    pkg = _pkg(result)
    relations = pkg.get("relation_hint_candidates") or []
    assignments = pkg.get("text_owner_assignment_candidates") or []
    return {
        **result,
        "scenario": "case_a_stacked_papers_occlusion",
        "paper_a": "paper_A" in _surface_ids(pkg),
        "paper_b": "paper_B" in _surface_ids(pkg),
        "occludes": any(r.get("relation_type_candidate") == "occludes" for r in relations),
        "no_ocr": all(a.get("no_ocr_text") for a in assignments),
        "not_merged": len(_surface_ids(pkg)) >= 2,
    }


def run_stacked_menus_no_ocr() -> Dict[str, Any]:
    """Case B: 菜单叠放，text_detection_per_surface 建议，禁止 global OCR."""
    result = run_document_surface_detector_planning(fixture_ref="stacked_menus")
    pkg = _pkg(result)
    resp = result.get("runtime_response") or {}
    return {
        **result,
        "scenario": "case_b_stacked_menus_no_ocr",
        "two_surfaces": len(_surface_ids(pkg)) >= 2,
        "next_slot": pkg.get("next_slot_suggestion") == "text_detection_per_surface",
        "no_ocr_text": resp.get("no_ocr_text") is True,
        "owner_candidates_only": all(
            a.get("text_content") is None for a in pkg.get("text_owner_assignment_candidates") or []
        ),
    }


def run_receipt_attached_to_package() -> Dict[str, Any]:
    """Case C: receipt attached_to package，分离 surface."""
    result = run_document_surface_detector_planning(fixture_ref="receipt_on_package")
    pkg = _pkg(result)
    relations = pkg.get("relation_hint_candidates") or []
    return {
        **result,
        "scenario": "case_c_receipt_attached_to_package",
        "receipt": "receipt_surface" in _surface_ids(pkg),
        "package": "package_surface" in _surface_ids(pkg),
        "attached": any(r.get("relation_type_candidate") == "attached_to" for r in relations),
        "separate_owners": len(set(
            a.get("owner_entity_candidate_ref")
            for a in pkg.get("text_owner_assignment_candidates") or []
        )) >= 2,
    }


def run_attention_blocked_skip() -> Dict[str, Any]:
    """Case D: attention blocked → runtime_call_count=0."""
    result = run_document_surface_detector_planning(
        fixture_ref="stacked_papers",
        attention_gate_status="blocked",
    )
    return {
        **result,
        "scenario": "case_d_attention_blocked_skip",
        "skipped": result.get("skipped_by_attention_gate") is True,
        "zero_calls": result.get("runtime_call_count") == 0,
        "no_surfaces": result.get("no_surface_candidates") is True,
    }


def run_uncertain_boundary() -> Dict[str, Any]:
    """Case E: uncertain visibility + request_more_evidence."""
    result = run_document_surface_detector_planning(fixture_ref="uncertain_boundary")
    pkg = _pkg(result)
    surfaces = pkg.get("document_surface_candidates") or []
    return {
        **result,
        "scenario": "case_e_uncertain_boundary",
        "uncertain": any(s.get("visibility_status_candidate") == "uncertain" for s in surfaces),
        "more_evidence": pkg.get("validation_status_candidate") == "request_more_evidence",
        "no_fact": result.get("candidate_only") is True,
    }


def run_runtime_unavailable() -> Dict[str, Any]:
    """Case F: runtime error, no OCR/VLM/segmentation fallback."""
    result = run_document_surface_detector_planning(
        fixture_ref="stacked_papers",
        runtime_unavailable=True,
    )
    err = result.get("document_surface_runtime_error_candidate") or {}
    return {
        **result,
        "scenario": "case_f_runtime_unavailable",
        "error": err.get("error_type") == "document_surface_runtime_unavailable",
        "handoff": err.get("handoff_to") == "L2_or_attention_replan",
        "no_ocr_fallback": result.get("no_silent_fallback_to_ocr") is True,
        "no_vlm_fallback": result.get("no_silent_fallback_to_vlm") is True,
    }


def run_layout_detector_conflict() -> Dict[str, Any]:
    """Case G: detector_conflict → validation_review."""
    result = run_document_surface_detector_planning(fixture_ref="layout_conflict")
    pkg = _pkg(result)
    resp = result.get("runtime_response") or {}
    return {
        **result,
        "scenario": "case_g_layout_detector_conflict",
        "conflict": resp.get("layout_conflict_detected") is True,
        "validation_review": pkg.get("validation_status_candidate") == "validation_review",
        "not_auto_accept": pkg.get("validation_status_candidate") != "accepted",
    }


def run_screen_document_confusion() -> Dict[str, Any]:
    """Case H: screen document — defer to screen_surface_detector."""
    result = run_document_surface_detector_planning(fixture_ref="screen_document")
    pkg = _pkg(result)
    resp = result.get("runtime_response") or {}
    return {
        **result,
        "scenario": "case_h_screen_document_confusion",
        "screen_hint": resp.get("possible_screen_document_content") is True,
        "defer_screen": pkg.get("validation_status_candidate") == "defer_to_screen_surface_detector",
        "not_paper_fact": result.get("candidate_only") is True,
    }
