# -*- coding: utf-8 -*-
"""Luna Attention-Gated RI — dryrun smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.situation_understanding.luna_situation_understanding_attention_gated_ri_dryrun_processor_v1 import (
    run_attention_gate_blocks_models,
    run_goal_assess_danger,
    run_goal_find_coffee_shop,
    run_goal_find_exit_budget,
    run_information_efficiency_score,
    run_scene_graph_ownership_attention,
)
from capabilities.midplatform.situation_understanding.luna_situation_understanding_attention_gated_ri_dryrun_types_v1 import (
    DRYRUN_CASE_IDS,
    FINAL_BLOCKED,
    FINAL_GO,
)


def _wrap(case_id: str, result: Dict[str, Any], checks: Dict[str, bool]) -> Dict[str, Any]:
    return {"case_id": case_id, "passed": all(checks.values()), "result": result, "checks": checks}


def dryrun_case_a() -> Dict[str, Any]:
    r = run_attention_gate_blocks_models()
    return _wrap("case_a_attention_gate_blocks_models", r, {
        "dir_allowed": r.get("direction_allowed") is True,
        "ad_blocked": r.get("ad_blocked") is True,
        "skip_reason": r.get("ad_skip_reason") is True,
        "blocked_ocr": r.get("ad_blocked_ocr") is True,
        "gate_controls": r.get("gate_controls_activation") is True,
    })


def dryrun_case_b() -> Dict[str, Any]:
    r = run_goal_find_exit_budget()
    return _wrap("case_b_goal_find_exit_budget", r, {
        "dir_budget": r.get("direction_budget_high") is True,
        "ad_budget": r.get("ad_budget_low") is True,
        "ad_skipped": r.get("ad_skipped") is True,
        "goal_drives": r.get("goal_drives_attention") is True,
    })


def dryrun_case_c() -> Dict[str, Any]:
    r = run_goal_find_coffee_shop()
    return _wrap("case_c_goal_find_coffee_shop", r, {
        "shop_budget": r.get("shop_budget_high") is True,
        "shop_allowed": r.get("shop_allowed") is True,
        "not_image": r.get("not_image_decides") is True,
    })


def dryrun_case_d() -> Dict[str, Any]:
    r = run_goal_assess_danger()
    return _wrap("case_d_goal_assess_danger", r, {
        "dynamic_budget": r.get("people_budget_high") is True,
        "ad_low": r.get("ad_budget_low") is True,
        "dynamic_allowed": r.get("dynamic_allowed") is True,
        "ad_blocked": r.get("ad_blocked") is True,
    })


def dryrun_case_e() -> Dict[str, Any]:
    r = run_scene_graph_ownership_attention()
    return _wrap("case_e_scene_graph_ownership_attention", r, {
        "scene_graph": r.get("has_scene_graph") is True,
        "ownership": r.get("entities_have_ownership") is True,
        "attention": r.get("entities_have_attention") is True,
        "ad_blocked": r.get("ad_attention_low") is True,
    })


def dryrun_case_f() -> Dict[str, Any]:
    r = run_information_efficiency_score()
    return _wrap("case_f_information_efficiency_score", r, {
        "more_efficient": r.get("luna_more_efficient") is True,
        "cost_reduction": r.get("cost_reduction") is True,
        "fewer_regions": r.get("luna_fewer_regions") is True,
    })


def run_all_dryrun_cases() -> Dict[str, Any]:
    cases = [dryrun_case_a(), dryrun_case_b(), dryrun_case_c(), dryrun_case_d(), dryrun_case_e(), dryrun_case_f()]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Situation-Understanding-Attention-Gated-Region-Intelligence-DryRun-v1-001",
        "dryrun_only": True,
        "attention_gated_region_intelligence": True,
        "dryrun_case_ids": list(DRYRUN_CASE_IDS),
        "dryrun_cases": cases,
        "dryrun_passed": sum(1 for c in cases if c.get("passed")),
        "dryrun_case_count": len(cases),
        "failed_checks": failed,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
