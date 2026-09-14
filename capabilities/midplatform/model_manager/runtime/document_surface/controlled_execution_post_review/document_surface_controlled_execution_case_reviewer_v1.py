# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — case reviewer v1 (A–H)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

CASE_RESULTS_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"
    "controlled_execution_case_results.json"
)


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def review_controlled_execution_cases(*, repo_root: Path) -> Dict[str, Any]:
    path = repo_root / CASE_RESULTS_REL
    cases: List[Dict[str, Any]] = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else []

    def _outs(cid: str) -> Dict[str, Any]:
        return (_case(cases, cid).get("candidate_outputs") or {})

    reviews: List[Dict[str, Any]] = []

    ca = _case(cases, "case_a_single_flat_paper_controlled")
    reviews.append({
        "case_id": "case_a_single_flat_paper_controlled",
        "passed": ca.get("abort_status") == "none" and len(_outs("case_a_single_flat_paper_controlled").get("document_surface_candidates") or []) >= 1,
        "surface_count": len(_outs("case_a_single_flat_paper_controlled").get("document_surface_candidates") or []),
        "status": _outs("case_a_single_flat_paper_controlled").get("runtime_status_candidate"),
        "no_ocr": (ca.get("validation") or {}).get("no_ocr_leak") is True,
        "blocker": False,
    })

    cb = _case(cases, "case_b_two_overlapping_papers_controlled")
    b_surfaces = len(_outs("case_b_two_overlapping_papers_controlled").get("document_surface_candidates") or [])
    b_rels = len(_outs("case_b_two_overlapping_papers_controlled").get("relation_hint_candidates") or [])
    reviews.append({
        "case_id": "case_b_two_overlapping_papers_controlled",
        "passed": cb.get("abort_status") == "none" and (cb.get("validation") or {}).get("schema_compliant") is True,
        "surface_count": b_surfaces,
        "relation_count": b_rels,
        "watch": ["overlapping_documents_under_separated", "relation_hint_missing_for_overlap_case"],
        "watch_note": "边界测试通过，但未实现 paper_A/paper_B 分离；不得视为分离成功，不得补假 relation",
        "separation_success": False,
        "blocker": False,
    })

    cc = _case(cases, "case_c_low_contrast_paper_controlled")
    c_surfaces = len(_outs("case_c_low_contrast_paper_controlled").get("document_surface_candidates") or [])
    reviews.append({
        "case_id": "case_c_low_contrast_paper_controlled",
        "passed": cc.get("abort_status") == "none",
        "surface_count": c_surfaces,
        "relation_count": len(_outs("case_c_low_contrast_paper_controlled").get("relation_hint_candidates") or []),
        "status": _outs("case_c_low_contrast_paper_controlled").get("runtime_status_candidate"),
        "watch": ["low_contrast_false_surface_risk", "candidate_count_noise_in_low_contrast_case"],
        "blocker": False,
    })

    cd = _case(cases, "case_d_receipt_attached_to_package_controlled")
    reviews.append({
        "case_id": "case_d_receipt_attached_to_package_controlled",
        "passed": cd.get("abort_status") == "none",
        "surface_count": len(_outs("case_d_receipt_attached_to_package_controlled").get("document_surface_candidates") or []),
        "status": _outs("case_d_receipt_attached_to_package_controlled").get("runtime_status_candidate"),
        "watch": ["receipt_attachment_boundary_uncertain"],
        "blocker": False,
    })

    ce = _case(cases, "case_e_document_on_screen_controlled")
    reviews.append({
        "case_id": "case_e_document_on_screen_controlled",
        "passed": _outs("case_e_document_on_screen_controlled").get("runtime_status_candidate") == "possible_screen_document_content_candidate",
        "status": _outs("case_e_document_on_screen_controlled").get("runtime_status_candidate"),
        "defer_to_screen": True,
        "screen_not_fact": (ce.get("validation") or {}).get("no_fact_output") is True,
        "watch": ["screen_vs_document_ambiguity_continues"],
        "blocker": False,
    })

    cf = _case(cases, "case_f_attention_blocked_controlled")
    reviews.append({
        "case_id": "case_f_attention_blocked_controlled",
        "passed": cf.get("runtime_call_count", 1) == 0 and cf.get("cv2_processing_executed") is False,
        "runtime_call_count": cf.get("runtime_call_count"),
        "no_image_read": cf.get("no_image_content_read") is True,
        "blocker": False,
    })

    cg = _case(cases, "case_g_unsupported_format_controlled")
    reviews.append({
        "case_id": "case_g_unsupported_format_controlled",
        "passed": cg.get("abort_reason") == "unsupported_image_format",
        "abort_reason": cg.get("abort_reason"),
        "no_fallback": (cg.get("validation") or {}).get("no_fallback") is True,
        "blocker": False,
    })

    ch = _case(cases, "case_h_image_read_failed_controlled")
    reviews.append({
        "case_id": "case_h_image_read_failed_controlled",
        "passed": ch.get("abort_reason") == "image_read_failed" and bool(ch.get("trace")),
        "abort_reason": ch.get("abort_reason"),
        "failure_trace_retained": ch.get("failure_trace_retained") is True or bool(ch.get("trace")),
        "no_fallback": (ch.get("validation") or {}).get("no_fallback") is True,
        "blocker": False,
    })

    passed_count = sum(1 for r in reviews if r.get("passed"))
    return {
        "review_id": "controlled_execution_case_review_v1",
        "case_reviews": reviews,
        "review_passed_count": passed_count,
        "review_failed_count": len(reviews) - passed_count,
        "passed": passed_count == len(reviews),
        "watch_cases": [r["case_id"] for r in reviews if r.get("watch")],
        "candidate_only": True,
        "not_fact": True,
    }
