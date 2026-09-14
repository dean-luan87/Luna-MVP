# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.dryrun.document_surface_detector_dryrun_adapter_v1 import (
    run_document_surface_detector_dryrun,
)


def _dryrun(result: Dict[str, Any]) -> Dict[str, Any]:
    return result.get("document_surface_dryrun_result") or {}


def _pkg(result: Dict[str, Any]) -> Dict[str, Any]:
    return _dryrun(result).get("ownership_evidence_package") or {}


def _surface_ids(result: Dict[str, Any]) -> List[str]:
    dr = _dryrun(result)
    return [s.get("surface_id") for s in dr.get("document_surface_candidates") or []]


def run_stacked_papers_occlusion() -> Dict[str, Any]:
    """Case A: paper_A / paper_B + occludes, no OCR, not merged."""
    result = run_document_surface_detector_dryrun(fixture_ref="stacked_papers")
    dr = _dryrun(result)
    relations = dr.get("relation_hint_candidates") or []
    assignments = dr.get("text_owner_assignment_candidates") or []
    return {
        **result,
        "scenario": "case_a_stacked_papers_occlusion",
        "bound": dr.get("runtime_binding_status_candidate") == "bound",
        "paper_a": "paper_A" in _surface_ids(result),
        "paper_b": "paper_B" in _surface_ids(result),
        "occludes": any(r.get("relation_type_candidate") == "occludes" for r in relations),
        "two_entities": len((_pkg(result).get("entity_candidates") or [])) >= 2,
        "no_ocr": all(a.get("no_ocr_text") for a in assignments),
        "not_merged": len(_surface_ids(result)) >= 2,
    }


def run_stacked_menus_no_ocr() -> Dict[str, Any]:
    """Case B: 菜单叠放，next_slot=text_detection_per_surface，禁止 global OCR."""
    result = run_document_surface_detector_dryrun(fixture_ref="stacked_menus")
    dr = _dryrun(result)
    pkg = _pkg(result)
    return {
        **result,
        "scenario": "case_b_stacked_menus_no_ocr",
        "two_surfaces": len(_surface_ids(result)) >= 2,
        "next_slot": dr.get("next_slot_candidate") == "text_detection_per_surface",
        "no_ocr_text": result.get("no_ocr_text_output") is True,
        "owner_candidates_only": all(
            a.get("text_content") is None for a in dr.get("text_owner_assignment_candidates") or []
        ),
        "no_global_ocr": result.get("no_global_ocr") is True,
    }


def run_receipt_attached_to_package() -> Dict[str, Any]:
    """Case C: receipt attached_to package，owner 分离."""
    result = run_document_surface_detector_dryrun(fixture_ref="receipt_on_package")
    dr = _dryrun(result)
    relations = dr.get("relation_hint_candidates") or []
    assignments = dr.get("text_owner_assignment_candidates") or []
    receipt_assign = next((a for a in assignments if a.get("surface_id") == "receipt_surface"), {})
    return {
        **result,
        "scenario": "case_c_receipt_attached_to_package",
        "receipt": "receipt_surface" in _surface_ids(result),
        "package": "package_surface" in _surface_ids(result),
        "attached": any(r.get("relation_type_candidate") == "attached_to" for r in relations),
        "receipt_owner": receipt_assign.get("owner_entity_candidate_ref") == "receipt_001",
        "receipt_basis": receipt_assign.get("assignment_basis") == "attached_to_relation",
        "separate_owners": len(set(a.get("owner_entity_candidate_ref") for a in assignments)) >= 2,
    }


def run_attention_blocked_skip() -> Dict[str, Any]:
    """Case D: attention blocked → runtime_call_count=0."""
    result = run_document_surface_detector_dryrun(
        fixture_ref="stacked_papers",
        attention_gate_status="blocked",
    )
    dr = _dryrun(result)
    return {
        **result,
        "scenario": "case_d_attention_blocked_skip",
        "skipped": dr.get("runtime_binding_status_candidate") == "skipped_by_attention_gate",
        "zero_calls": dr.get("runtime_call_count") == 0,
        "no_surfaces": len(dr.get("document_surface_candidates") or []) == 0,
        "no_evidence": dr.get("ownership_evidence_package") is None,
        "no_text_owner": len(dr.get("text_owner_assignment_candidates") or []) == 0,
    }


def run_uncertain_boundary() -> Dict[str, Any]:
    """Case E: uncertain visibility + needs_more_evidence."""
    result = run_document_surface_detector_dryrun(fixture_ref="uncertain_boundary")
    dr = _dryrun(result)
    surfaces = dr.get("document_surface_candidates") or []
    return {
        **result,
        "scenario": "case_e_uncertain_boundary",
        "uncertain": any(s.get("visibility_status_candidate") == "uncertain" for s in surfaces),
        "more_evidence": dr.get("validation_status_candidate") == "needs_more_evidence",
        "request_flag": dr.get("request_more_evidence_candidate") is True,
        "no_fact": result.get("candidate_only") is True,
    }


def run_runtime_unavailable() -> Dict[str, Any]:
    """Case F: runtime error, no OCR/VLM/segmentation fallback."""
    result = run_document_surface_detector_dryrun(
        fixture_ref="stacked_papers",
        runtime_unavailable=True,
    )
    dr = _dryrun(result)
    err = dr.get("document_surface_runtime_error_candidate") or {}
    return {
        **result,
        "scenario": "case_f_runtime_unavailable",
        "error": err.get("error_type") == "document_surface_runtime_unavailable",
        "handoff": err.get("handoff_to_l2_or_attention_replan") is True,
        "no_ocr_fallback": result.get("no_silent_fallback_to_ocr") is True,
        "no_vlm_fallback": result.get("no_silent_fallback_to_vlm") is True,
        "no_seg_fallback": result.get("no_full_scene_segmentation_fallback") is True,
    }


def run_layout_detector_conflict() -> Dict[str, Any]:
    """Case G: detector_conflict → validation_review."""
    result = run_document_surface_detector_dryrun(fixture_ref="layout_conflict")
    dr = _dryrun(result)
    return {
        **result,
        "scenario": "case_g_layout_detector_conflict",
        "conflict": dr.get("layout_conflict_detected") is True,
        "validation_review": dr.get("validation_status_candidate") == "validation_review",
        "not_auto_accept": dr.get("validation_status_candidate") != "accepted",
        "detector_conflict": dr.get("runtime_status_candidate") == "detector_conflict_candidate",
    }


def run_screen_document_confusion() -> Dict[str, Any]:
    """Case H: screen document — defer to screen_surface_detector."""
    result = run_document_surface_detector_dryrun(fixture_ref="screen_document")
    dr = _dryrun(result)
    return {
        **result,
        "scenario": "case_h_screen_document_confusion",
        "screen_hint": dr.get("possible_screen_document_content") is True,
        "defer_screen": dr.get("validation_status_candidate") == "defer_to_screen_surface_detector",
        "not_paper_fact": result.get("candidate_only") is True,
        "runtime_status": dr.get("runtime_status_candidate") == "possible_screen_document_content_candidate",
    }
