# -*- coding: utf-8 -*-
"""Document Surface — Option B case mapping reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


CASES_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_option_b_candidate_route_dryrun_v1/"
    "option_b_case_mapping_summary.json"
)


def _route(cases: List[Dict[str, Any]], profile: str) -> Dict[str, Any]:
    c = next((x for x in cases if x.get("case_profile") == profile), {})
    return c.get("route_selection") or {}


def review_option_b_case_mapping(*, repo_root: Path) -> Dict[str, Any]:
    cases: List[Dict[str, Any]] = json.loads((repo_root / CASES_REL).read_text(encoding="utf-8")) if (repo_root / CASES_REL).is_file() else []

    reviews = [
        {
            "case_profile": "case_a_clear_edges",
            "passed": _route(cases, "case_a_clear_edges").get("selected_route_candidate") == "option_b_segmentation_candidate_route"
            and _route(cases, "case_a_clear_edges").get("route_reason_candidate") == "surface_separation_needed",
            "note": "Option A under-separated; B route recommended; no execution",
        },
        {
            "case_profile": "case_b_low_overlap",
            "passed": _route(cases, "case_b_low_overlap").get("selected_route_candidate") == "option_a_baseline_with_optional_b",
            "conflict_review": next((x.get("conflict_policy") for x in cases if x.get("case_profile") == "case_b_low_overlap"), {}).get("validation_review_required") is True,
            "note": "A over-segmentation risk; B optional; conflict review",
        },
        {
            "case_profile": "case_c_high_overlap",
            "passed": _route(cases, "case_c_high_overlap").get("selected_route_candidate") == "option_b_segmentation_candidate_route"
            and _route(cases, "case_c_high_overlap").get("route_reason_candidate") == "partial_surface_or_mask_needed",
            "note": "Option A surface missed",
        },
        {
            "case_profile": "case_e_texture_false_positive",
            "passed": _route(cases, "case_e_texture_false_positive").get("selected_route_candidate") == "option_a_baseline_only"
            and _route(cases, "case_e_texture_false_positive").get("option_b_recommended") is False,
            "note": "B not default; field/attention gate required",
        },
        {
            "case_profile": "case_f_receipt_clear",
            "passed": _route(cases, "case_f_receipt_clear").get("selected_route_candidate") == "option_b_segmentation_candidate_route"
            and _route(cases, "case_f_receipt_clear").get("route_reason_candidate") == "attached_surface_mask_needed",
            "note": "Option A receipt surface missed",
        },
        {
            "case_profile": "case_h_screen_control",
            "passed": _route(cases, "case_h_screen_control").get("selected_route_candidate") == "defer_screen_surface_detector",
            "note": "B cannot solve fixture semantic mismatch; fixture correction required",
        },
    ]
    for r in reviews:
        if r["case_profile"] == "case_b_low_overlap":
            r["passed"] = r["passed"] and r.get("conflict_review") is True

    return {
        "review_id": "option_b_case_mapping_review",
        "passed": all(r.get("passed") for r in reviews),
        "review_passed_count": sum(1 for r in reviews if r.get("passed")),
        "review_failed_count": sum(1 for r in reviews if not r.get("passed")),
        "case_reviews": reviews,
        "candidate_only": True,
        "not_fact": True,
    }
