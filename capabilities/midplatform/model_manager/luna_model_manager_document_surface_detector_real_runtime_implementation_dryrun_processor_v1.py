# -*- coding: utf-8 -*-
"""Luna Document Surface Detector — implementation dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_dryrun.document_surface_option_a_dryrun_adapter_v1 import (
    RECOMMENDED_NEXT_PHASE,
    run_option_a_implementation_dryrun,
)


def _pipeline(r: Dict[str, Any]) -> Dict[str, Any]:
    return r.get("pipeline_output") or {}


def _surfaces(r: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _pipeline(r).get("document_surface_candidates") or []


def run_single_flat_paper() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="single_flat_paper")
    p = _pipeline(r)
    return {
        **r,
        "scenario": "case_a_single_flat_paper",
        "quadrilateral": p.get("quadrilateral_candidate") is not None,
        "surface": len(_surfaces(r)) >= 1,
        "visible": all(s.get("visibility_status_candidate") == "visible" for s in _surfaces(r)),
        "ownership_ok": r.get("ownership_package_compatible") is True,
        "no_ocr": r.get("no_ocr_text") is True,
    }


def run_two_overlapping_papers() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="two_overlapping_papers")
    relations = _pipeline(r).get("relation_hint_candidates") or []
    sids = [s.get("surface_id") for s in _surfaces(r)]
    return {
        **r,
        "scenario": "case_b_two_overlapping_papers",
        "paper_a": "paper_A" in sids,
        "paper_b": "paper_B" in sids,
        "overlap_or_occludes": any(
            rel.get("relation_type_candidate") in ("overlaps", "occludes") for rel in relations
        ),
        "not_merged": len(sids) >= 2,
        "text_ready": r.get("text_owner_assignment_ready") is True,
    }


def run_folded_or_curved_paper() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="folded_or_curved_paper")
    p = _pipeline(r)
    val = r.get("validation") or {}
    return {
        **r,
        "scenario": "case_c_folded_or_curved_paper",
        "polygon": p.get("polygon_candidate") is not None,
        "needs_evidence": val.get("validation_status_candidate") == "needs_more_evidence",
        "no_fact": r.get("not_fact") is True,
    }


def run_receipt_attached_to_package() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="receipt_attached_to_package")
    relations = _pipeline(r).get("relation_hint_candidates") or []
    readiness = r.get("text_owner_assignment_readiness_candidates") or []
    receipt_ready = next((x for x in readiness if x.get("surface_id") == "receipt_surface"), {})
    sids = [s.get("surface_id") for s in _surfaces(r)]
    return {
        **r,
        "scenario": "case_d_receipt_attached_to_package",
        "receipt": "receipt_surface" in sids,
        "package": "package_surface" in sids,
        "attached": any(rel.get("relation_type_candidate") == "attached_to" for rel in relations),
        "receipt_owner": receipt_ready.get("owner_entity_candidate_ref") == "receipt_001",
    }


def run_document_on_screen() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="document_on_screen")
    val = r.get("validation") or {}
    return {
        **r,
        "scenario": "case_e_document_on_screen",
        "screen_hint": _pipeline(r).get("possible_screen_document_content") is True,
        "defer": val.get("validation_status_candidate") == "defer_to_screen_surface_detector",
        "not_paper_fact": val.get("screen_surface_not_document_surface_fact") is True,
    }


def run_low_contrast_paper_on_desk() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(fixture_ref="low_contrast_paper_on_desk")
    val = r.get("validation") or {}
    return {
        **r,
        "scenario": "case_f_low_contrast_paper_on_desk",
        "low_contrast": _pipeline(r).get("low_contrast_boundary") is True,
        "needs_evidence": val.get("validation_status_candidate") == "needs_more_evidence",
        "next_action": val.get("next_action_candidate") == "request_better_view_or_lighting",
        "no_fallback": r.get("no_ocr_text") is True,
    }


def run_attention_blocked() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        attention_gate_status="blocked",
    )
    return {
        **r,
        "scenario": "case_g_attention_blocked",
        "zero_calls": r.get("runtime_call_count") == 0,
        "skipped": r.get("skipped_by_attention_gate") is True,
        "no_surfaces": len(_surfaces(r)) == 0,
    }


def run_runtime_error() -> Dict[str, Any]:
    r = run_option_a_implementation_dryrun(
        fixture_ref="single_flat_paper",
        runtime_error_mode="runtime_dependency_missing",
    )
    return {
        **r,
        "scenario": "case_h_runtime_error",
        "error": r.get("runtime_error") is True,
        "handled": r.get("runtime_error_handled") is True,
        "handoff": (r.get("runtime_error_candidate") or {}).get("handoff_to_l2_or_attention_replan") is True,
        "no_silent": r.get("no_silent_fallback") is True,
        "next_post_review": RECOMMENDED_NEXT_PHASE.endswith("Implementation-Post-Review-v1-001"),
    }
