# -*- coding: utf-8 -*-
"""Field simulation readiness assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_simulation_types_v1 import SIMULATION_MODES


def assemble_field_simulation_readiness_candidate(
    *,
    plan: Dict[str, Any],
    eligibility: Dict[str, Any],
    simulation_candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    selected = set(plan.get("selected_modes") or [])
    generated_modes = {
        c["mode"] for c in simulation_candidates
        if c.get("simulation_status") in ("generated", "generated_degraded")
    }
    blockers: List[str] = list(eligibility.get("limitations") or [])
    if not generated_modes:
        blockers.append("no_simulation_candidates_generated")

    readiness_trp = (
        "task_relevance_field_projection" in generated_modes
        and "safety_risk_projection" in generated_modes
        and eligibility.get("eligibility_status") not in ("blocked_no_scene", "blocked_no_entity", "blocked_quality_insufficient")
    )

    return {
        "readiness_id": f"fsrd_{uuid.uuid4().hex[:10]}",
        "simulation_plan_ref": plan["simulation_plan_id"],
        "readiness_for_current_state_simulation": "current_state_simulation" in generated_modes,
        "readiness_for_short_horizon_projection": "short_horizon_motion_projection" in generated_modes,
        "readiness_for_occlusion_missing_info_simulation": "occlusion_and_missing_info_simulation" in generated_modes,
        "readiness_for_task_relevance_projection": "task_relevance_field_projection" in generated_modes,
        "readiness_for_safety_risk_projection": "safety_risk_projection" in generated_modes,
        "readiness_for_field_quality_projection": "field_quality_projection" in generated_modes,
        "readiness_for_task_reasoning_planning": readiness_trp,
        "blockers": blockers,
        "warnings": plan.get("warning_codes") or [],
        "candidate_only": True,
    }


def assemble_field_simulation_skeleton_result(
    *,
    input_view: Dict[str, Any],
    eligibility: Dict[str, Any],
    plan: Dict[str, Any],
    simulation_candidates: List[Dict[str, Any]],
    readiness: Dict[str, Any],
    case_id: str,
) -> Dict[str, Any]:
    return {
        "skeleton_result_id": f"fssr_{uuid.uuid4().hex[:10]}",
        "case_id": case_id,
        "simulation_input_ref": input_view.get("simulation_input_id"),
        "simulation_plan_ref": plan.get("simulation_plan_id"),
        "eligibility_status": eligibility.get("eligibility_status"),
        "simulation_candidate_count": len(simulation_candidates),
        "generated_mode_count": sum(
            1 for c in simulation_candidates
            if c.get("simulation_status") in ("generated", "generated_degraded")
        ),
        "readiness_for_task_reasoning_planning": readiness.get("readiness_for_task_reasoning_planning"),
        "traceability_refs": input_view.get("traceability_refs") or [],
        "candidate_only": True,
    }
