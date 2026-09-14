# -*- coding: utf-8 -*-
"""Luna Ownership Real Runtime Integration — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_real_runtime_planning_processor_v1 import (
    run_attention_blocked_no_ownership,
    run_glass_reflection_separation,
    run_occluded_title_not_absent,
    run_runtime_unavailable_no_fallback,
    run_shelf_distinct_owners,
    run_stacked_papers_per_owner_ocr,
)
from capabilities.midplatform.model_manager.luna_model_manager_region_intelligence_ownership_real_runtime_planning_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_stacked_papers_per_owner_ocr()
    return _wrap("case_a_stacked_papers_per_owner_ocr", r, {
        "two": r.get("two_entities") is True,
        "paper_a": r.get("has_paper_a") is True,
        "paper_b": r.get("has_paper_b") is True,
        "per_owner": r.get("per_owner_text") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_shelf_distinct_owners()
    return _wrap("case_b_shelf_distinct_owners", r, {
        "three": r.get("three_entities") is True,
        "product": r.get("product_owner") is True,
        "price": r.get("price_tag_owner") is True,
        "distinct": r.get("distinct_text_owners") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_glass_reflection_separation()
    return _wrap("case_c_glass_reflection_separation", r, {
        "real": r.get("real_sign") is True,
        "reflection": r.get("reflection_entity") is True,
        "relation": r.get("reflection_relation") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_attention_blocked_no_ownership()
    return _wrap("case_d_attention_blocked_no_ownership", r, {
        "blocked": r.get("has_blocked_region") is True,
        "no_ad": r.get("bg_ad_not_in_entities") is True,
        "product_ok": r.get("product_still_processed") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_occluded_title_not_absent()
    return _wrap("case_e_occluded_title_not_absent", r, {
        "missing": r.get("has_missing_candidate") is True,
        "occluded": r.get("occluded_reason") is True,
        "not_absent": r.get("not_assume_absent") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_runtime_unavailable_no_fallback()
    return _wrap("case_f_runtime_unavailable_no_fallback", r, {
        "error": r.get("runtime_error") is True,
        "replan": r.get("replan_target") is True,
        "no_fallback": r.get("no_full_ocr_fallback") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(), smoke_case_e(), smoke_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
