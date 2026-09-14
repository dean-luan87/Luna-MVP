# -*- coding: utf-8 -*-
"""Field simulation plan builder v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.field_simulation_planning_items_v1 import (
    SIMULATION_MODES,
    build_simulation_plan as _build_plan,
)


def build_field_simulation_plan_candidate(
    *,
    input_view: Dict[str, Any],
    eligibility: Dict[str, Any],
    reusable_case: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    plan = _build_plan(
        input_view=input_view,
        eligibility=eligibility,
        reusable_case=reusable_case,
    )
    plan["simulation_scope"] = "skeleton_candidate_generation_only"
    assumptions = list(plan.get("assumptions") or [])
    if "planning_only_no_simulation_execution" in assumptions:
        assumptions.remove("planning_only_no_simulation_execution")
    assumptions.append("skeleton_candidate_generation_no_runtime")
    assumptions.append("no_action_no_fact_output")
    plan["assumptions"] = assumptions
    plan["readiness_for_simulation_result_generation"] = (
        len(plan.get("selected_modes") or []) > 0
        and eligibility.get("eligibility_status") not in ("blocked_no_scene", "blocked_no_entity")
    )
    if "readiness_for_simulation_skeleton" in plan:
        del plan["readiness_for_simulation_skeleton"]
    return plan
