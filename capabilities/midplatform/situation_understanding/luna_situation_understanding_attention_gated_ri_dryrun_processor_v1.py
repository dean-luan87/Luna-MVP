# -*- coding: utf-8 -*-
"""Luna Attention-Gated Region Intelligence — dryrun processor v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.attention_gated_ri_dryrun_adapter_v1 import (
    run_attention_gated_ri_dryrun,
)
from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.attention_gated_ri_dryrun_metrics_v1 import (
    reset_attention_gated_ri_dryrun_metrics,
)


def _blocked(gate: Dict[str, Any], region_type: str) -> Dict[str, Any]:
    return next(
        (b for b in gate.get("blocked_regions") or [] if b.get("region") == region_type),
        {},
    )


def _allowed_ids(gate: Dict[str, Any]) -> List[str]:
    return gate.get("region_intelligence_allowed_for") or []


def run_attention_gate_blocks_models() -> Dict[str, Any]:
    """Case A: 地铁站 — direction allowed OCR, advertisement blocked."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="subway_platform", goal_type="find_subway_exit")
    gate = result.get("attention_gate") or {}
    ad_blocked = _blocked(gate, "advertisement_screen")
    return {
        **result,
        "scenario": "case_a_attention_gate_blocks_models",
        "direction_allowed": "reg_direction" in _allowed_ids(gate),
        "ad_blocked": "reg_ad" in (gate.get("region_intelligence_blocked_for") or []),
        "ad_skip_reason": ad_blocked.get("skip_reason") == "low_task_value",
        "ad_blocked_ocr": "text_recognition" in (ad_blocked.get("blocked_capabilities") or []),
        "ad_blocked_visual": "visual_reasoning" in (ad_blocked.get("blocked_capabilities") or []),
        "gate_controls_activation": result.get("attention_gates_region_intelligence") is True,
    }


def run_goal_find_exit_budget() -> Dict[str, Any]:
    """Case B: Goal find_exit — exit/direction high, ad low."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="subway_platform", goal_type="find_subway_exit")
    gate = result.get("attention_gate") or {}
    budget = gate.get("observation_budget") or {}
    allocations = {a.get("region_id"): a.get("budget_share", 0) for a in budget.get("budget_allocations") or []}
    return {
        **result,
        "scenario": "case_b_goal_find_exit_budget",
        "direction_budget_high": allocations.get("reg_direction", 0) >= 0.35,
        "ad_budget_low": allocations.get("reg_ad", 0) <= 0.10,
        "ad_skipped": "reg_ad" in (budget.get("skipped_regions") or []),
        "goal_drives_attention": True,
    }


def run_goal_find_coffee_shop() -> Dict[str, Any]:
    """Case C: 同图 Goal B — find coffee shop, shop_sign high."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="shopping_mall", goal_type="find_coffee_shop")
    gate = result.get("attention_gate") or {}
    budget = gate.get("observation_budget") or {}
    allocations = {a.get("region_id"): a.get("budget_share", 0) for a in budget.get("budget_allocations") or []}
    return {
        **result,
        "scenario": "case_c_goal_find_coffee_shop",
        "shop_budget_high": allocations.get("reg_shop", 0) >= 0.80,
        "shop_allowed": "reg_shop" in _allowed_ids(gate),
        "not_image_decides": (result.get("observation_priority_graph") or {}).get("not_image_decides_attention") is True,
    }


def run_goal_assess_danger() -> Dict[str, Any]:
    """Case D: Goal C — assess danger, people/vehicle high, sign low."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="street_scene", goal_type="assess_danger")
    gate = result.get("attention_gate") or {}
    budget = gate.get("observation_budget") or {}
    allocations = {a.get("region_id"): a.get("budget_share", 0) for a in budget.get("budget_allocations") or []}
    return {
        **result,
        "scenario": "case_d_goal_assess_danger",
        "people_budget_high": allocations.get("reg_dynamic", 0) >= 0.60,
        "ad_budget_low": allocations.get("reg_ad", 0) <= 0.10,
        "dynamic_allowed": "reg_dynamic" in _allowed_ids(gate),
        "ad_blocked": "reg_ad" in (gate.get("region_intelligence_blocked_for") or []),
    }


def run_scene_graph_ownership_attention() -> Dict[str, Any]:
    """Case E: Scene Graph — Ownership + Attention merged."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="subway_platform", goal_type="find_subway_exit")
    sg = result.get("scene_graph") or {}
    entities = sg.get("entities") or []
    ad_entity = next((e for e in entities if e.get("region_id") == "reg_ad"), {})
    return {
        **result,
        "scenario": "case_e_scene_graph_ownership_attention",
        "has_scene_graph": sg.get("ownership_plus_attention") is True,
        "entities_have_ownership": all("ownership" in e for e in entities),
        "entities_have_attention": all("attention" in e for e in entities),
        "ad_attention_low": ad_entity.get("attention", {}).get("gate_status") == "blocked",
        "ad_has_reason": ad_entity.get("reason") == "low_task_value",
    }


def run_information_efficiency_score() -> Dict[str, Any]:
    """Case F: Information Efficiency — Luna cost << traditional baseline."""
    reset_attention_gated_ri_dryrun_metrics()
    result = run_attention_gated_ri_dryrun(scan_fixture="subway_platform", goal_type="find_subway_exit")
    eff = result.get("information_efficiency") or {}
    return {
        **result,
        "scenario": "case_f_information_efficiency_score",
        "luna_more_efficient": eff.get("luna_more_efficient") is True,
        "cost_reduction": (eff.get("cost_reduction_ratio") or 0) > 1,
        "luna_fewer_regions": (eff.get("luna") or {}).get("regions_processed", 100) < 10,
        "traditional_100_regions": (eff.get("traditional_baseline") or {}).get("regions_processed") == 100,
    }
