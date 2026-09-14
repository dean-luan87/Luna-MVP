# -*- coding: utf-8 -*-
"""Luna Attention Allocation — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.situation_understanding.attention_allocation.attention_allocation_adapter_v1 import (
    run_attention_allocation,
)


def _region_assessment(result: Dict[str, Any], region_id: str) -> Dict[str, Any]:
    assessments = (result.get("value_assessment") or {}).get("region_value_assessments") or []
    return next((a for a in assessments if a.get("region_id") == region_id), {})


def _budget_entry(result: Dict[str, Any], region_id: str) -> Dict[str, Any]:
    entries = (result.get("observation_budget") or {}).get("budget_allocations") or []
    return next((e for e in entries if e.get("region_id") == region_id), {})


def run_l0_scan_no_heavy_models() -> Dict[str, Any]:
    """Case A: L0 快速扫描 — 无 OCR/Qwen/重模型."""
    result = run_attention_allocation(scan_fixture="subway_platform", goal_type="find_subway_exit")
    l0 = result.get("l0_observation_scan") or {}
    return {
        **result,
        "scenario": "case_a_l0_scan_no_heavy_models",
        "has_scene_profile": bool(l0.get("scene_profile_candidate")),
        "has_attention_priorities": len(l0.get("attention_priority_candidates") or []) >= 3,
        "no_ocr": l0.get("no_ocr") is True,
        "no_qwen": l0.get("no_qwen") is True,
        "no_heavy_models": l0.get("no_heavy_models") is True,
    }


def run_subway_value_by_goal() -> Dict[str, Any]:
    """Case B: 地铁 — direction high, ad low for find_exit goal."""
    result = run_attention_allocation(scan_fixture="subway_platform", goal_type="find_subway_exit")
    direction = _region_assessment(result, "reg_direction")
    ad = _region_assessment(result, "reg_ad")
    return {
        **result,
        "scenario": "case_b_subway_value_by_goal",
        "direction_high": direction.get("task_relevance") == "high",
        "ad_low": ad.get("task_relevance") == "low",
        "direction_worth_deep": direction.get("worth_deep_understanding") is True,
        "ad_not_worth_deep": ad.get("worth_deep_understanding") is False,
    }


def run_exit_goal_budget() -> Dict[str, Any]:
    """Case C: find_subway_exit — direction ~80%, exit 15%, ad 5%."""
    result = run_attention_allocation(scan_fixture="subway_platform", goal_type="find_subway_exit")
    budget = result.get("observation_budget") or {}
    direction_budget = _budget_entry(result, "reg_direction").get("budget_share", 0)
    ad_budget = _budget_entry(result, "reg_ad").get("budget_share", 0)
    return {
        **result,
        "scenario": "case_c_exit_goal_budget_allocation",
        "direction_budget_high": direction_budget >= 0.35,
        "ad_budget_low": ad_budget <= 0.10,
        "deep_includes_direction": "reg_direction" in (budget.get("deep_understanding_regions") or []),
        "skipped_includes_ad": "reg_ad" in (budget.get("skipped_regions") or []),
    }


def run_not_all_regions_deep() -> Dict[str, Any]:
    """Case D: 非全区域深入 — 解决 SAM 式全分割问题."""
    result = run_attention_allocation(scan_fixture="subway_platform", goal_type="find_subway_exit")
    budget = result.get("observation_budget") or {}
    return {
        **result,
        "scenario": "case_d_not_all_regions_deep",
        "selective_deep": budget.get("selective_deep_understanding") is True,
        "not_all_sam": budget.get("not_all_regions_sam") is True,
        "skipped_count_gt_zero": len(budget.get("skipped_regions") or []) > 0,
        "deep_count_lt_total": len(budget.get("deep_understanding_regions") or []) < 4,
    }


def run_same_text_different_value() -> Dict[str, Any]:
    """Case E: 同场景不同 goal — 预算分布不同."""
    exit_result = run_attention_allocation(scan_fixture="shopping_mall", goal_type="find_subway_exit")
    env_result = run_attention_allocation(scan_fixture="shopping_mall", goal_type="understand_environment")
    exit_deep = set((exit_result.get("observation_budget") or {}).get("deep_understanding_regions") or [])
    env_deep = set((env_result.get("observation_budget") or {}).get("deep_understanding_regions") or [])
    return {
        "scenario": "case_e_same_text_different_value",
        "exit_result": exit_result,
        "env_result": env_result,
        "budgets_differ": exit_deep != env_deep,
        "not_see_text_then_ocr": True,
    }


def run_attention_gates_region_intelligence() -> Dict[str, Any]:
    """Case F: Attention 门控 Region Intelligence — 低价值区域不触发."""
    result = run_attention_allocation(scan_fixture="subway_platform", goal_type="find_subway_exit")
    triggered = result.get("region_intelligence_triggered_for") or []
    skipped = result.get("region_intelligence_skipped_for") or []
    return {
        **result,
        "scenario": "case_f_attention_gates_region_intelligence",
        "attention_before_ri": result.get("attention_before_region_intelligence") is True,
        "triggered_nonempty": len(triggered) > 0,
        "skipped_nonempty": len(skipped) > 0,
        "ad_skipped": "reg_ad" in skipped,
        "direction_triggered": "reg_direction" in triggered,
    }
