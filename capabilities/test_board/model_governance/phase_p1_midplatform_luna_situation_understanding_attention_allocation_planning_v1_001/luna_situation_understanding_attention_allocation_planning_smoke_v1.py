# -*- coding: utf-8 -*-
"""Luna Attention Allocation — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.situation_understanding.luna_situation_understanding_attention_allocation_processor_v1 import (
    run_attention_gates_region_intelligence,
    run_exit_goal_budget,
    run_l0_scan_no_heavy_models,
    run_not_all_regions_deep,
    run_same_text_different_value,
    run_subway_value_by_goal,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_attention_allocation_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def smoke_case_a() -> Dict[str, Any]:
    r = run_l0_scan_no_heavy_models()
    return _wrap("case_a_l0_scan_no_heavy_models", r, {
        "scene": r.get("has_scene_profile") is True,
        "priorities": r.get("has_attention_priorities") is True,
        "no_ocr": r.get("no_ocr") is True,
        "no_qwen": r.get("no_qwen") is True,
    })


def smoke_case_b() -> Dict[str, Any]:
    r = run_subway_value_by_goal()
    return _wrap("case_b_subway_value_by_goal", r, {
        "dir_high": r.get("direction_high") is True,
        "ad_low": r.get("ad_low") is True,
        "dir_deep": r.get("direction_worth_deep") is True,
        "ad_not_deep": r.get("ad_not_worth_deep") is True,
    })


def smoke_case_c() -> Dict[str, Any]:
    r = run_exit_goal_budget()
    return _wrap("case_c_exit_goal_budget_allocation", r, {
        "dir_budget": r.get("direction_budget_high") is True,
        "ad_budget": r.get("ad_budget_low") is True,
        "deep_dir": r.get("deep_includes_direction") is True,
        "skip_ad": r.get("skipped_includes_ad") is True,
    })


def smoke_case_d() -> Dict[str, Any]:
    r = run_not_all_regions_deep()
    return _wrap("case_d_not_all_regions_deep", r, {
        "selective": r.get("selective_deep") is True,
        "not_sam": r.get("not_all_sam") is True,
        "skipped": r.get("skipped_count_gt_zero") is True,
    })


def smoke_case_e() -> Dict[str, Any]:
    r = run_same_text_different_value()
    return _wrap("case_e_same_text_different_value", r, {
        "budgets_differ": r.get("budgets_differ") is True,
        "not_auto_ocr": r.get("not_see_text_then_ocr") is True,
    })


def smoke_case_f() -> Dict[str, Any]:
    r = run_attention_gates_region_intelligence()
    return _wrap("case_f_attention_gates_region_intelligence", r, {
        "gates": r.get("attention_before_ri") is True,
        "ad_skipped": r.get("ad_skipped") is True,
        "dir_triggered": r.get("direction_triggered") is True,
    })


def run_smoke_cases() -> Dict[str, Any]:
    cases = [smoke_case_a(), smoke_case_b(), smoke_case_c(), smoke_case_d(), smoke_case_e(), smoke_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Allocation-Planning-v1-001",
        "planning_only": True,
        "active_perception": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
