# -*- coding: utf-8 -*-
"""Field simulation candidate generator v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.field_simulation_types_v1 import SIMULATION_MODES


def _base_candidate(
    *,
    plan: Dict[str, Any],
    input_view: Dict[str, Any],
    mode: str,
    status: str,
    confidence: str,
    blocked_reason: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "simulation_candidate_id": f"fsc_{uuid.uuid4().hex[:12]}",
        "simulation_plan_ref": plan["simulation_plan_id"],
        "mode": mode,
        "input_scene_ref": input_view.get("enhanced_field_scene_ref"),
        "projected_entities": [],
        "projected_zones": [],
        "projected_risks": [],
        "projected_missing_information": [],
        "projected_quality_status": None,
        "confidence_level": confidence,
        "simulation_status": status,
        "blocked_reason": blocked_reason,
        "no_action_output": True,
        "no_fact_output": True,
        "no_navigation_instruction": True,
        "source_refs": [input_view.get("simulation_input_id"), plan["simulation_plan_id"]],
        "evidence_refs": list(input_view.get("traceability_refs") or [])[:3],
        "traceability_refs": list(input_view.get("traceability_refs") or []),
        "candidate_only": True,
    }


def generate_current_state_simulation_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any], degraded: bool = False,
) -> Dict[str, Any]:
    entities = input_view.get("entity_candidates") or []
    zone = input_view.get("zone_summary") or {}
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="current_state_simulation",
        status="generated_degraded" if degraded else "generated",
        confidence="medium" if degraded else "high",
    )
    c["current_entities"] = [{"entity_ref": e.get("entity_id") or e.get("observation_id"), "label": e.get("label")} for e in entities]
    c["current_zones"] = zone
    c["current_quality"] = {
        "scene": input_view.get("scene_quality_summary"),
        "depth": input_view.get("depth_quality_summary"),
        "geometry": input_view.get("geometry_quality_summary"),
    }
    c["current_missing_information"] = input_view.get("missing_information") or []
    c["current_warnings"] = (input_view.get("warning_summary") or {}).get("warnings") or []
    c["projected_entities"] = c["current_entities"]
    c["projected_zones"] = [zone] if zone else []
    return c


def generate_short_horizon_motion_projection_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any], blocked: bool = False,
) -> Dict[str, Any]:
    if blocked or "short_horizon_motion_projection" not in (plan.get("selected_modes") or []):
        c = _base_candidate(
            plan=plan, input_view=input_view, mode="short_horizon_motion_projection",
            status="blocked_insufficient_input", confidence="low",
            blocked_reason="geometry_or_timestamp_insufficient",
        )
        c["projected_motion_candidates"] = []
        c["projection_confidence"] = "blocked"
        return c
    entities = input_view.get("entity_candidates") or []
    motions = []
    for e in entities:
        zone_hint = e.get("field_zone_hint") or "unknown_zone"
        motions.append({
            "entity_ref": e.get("entity_id") or e.get("observation_id"),
            "motion_hypothesis": "stationary_placeholder",
            "zone_hint": zone_hint,
            "geometry_status": e.get("entity_status", "unknown"),
        })
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="short_horizon_motion_projection",
        status="generated_degraded", confidence="low",
    )
    c["projected_motion_candidates"] = motions
    c["projection_confidence"] = "low"
    c["projected_entities"] = motions
    return c


def generate_occlusion_missing_info_simulation_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any],
) -> Dict[str, Any]:
    entities = input_view.get("entity_candidates") or []
    missing = input_view.get("missing_information") or []
    impacts = []
    for e in entities:
        if e.get("entity_status") in ("entity_geometry_unknown", "entity_2d_only"):
            impacts.append({
                "entity_ref": e.get("entity_id") or e.get("observation_id"),
                "impact_type": "geometry_unknown_or_2d_only",
                "required_followup": "additional_depth_or_multi_view",
            })
    if missing:
        impacts.append({"impact_type": "depth_or_alignment_missing", "missing": missing})
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="occlusion_and_missing_info_simulation",
        status="generated_degraded" if impacts else "generated",
        confidence="medium",
    )
    c["missing_info_impact_candidates"] = impacts
    c["occlusion_hypothesis_candidates"] = [{"hypothesis": "partial_occlusion_or_missing_depth", "confidence": "low"}] if impacts else []
    c["affected_entities"] = [i.get("entity_ref") for i in impacts if i.get("entity_ref")]
    c["required_followup_observation"] = ["depth_observation", "additional_frame"] if impacts else []
    c["projected_missing_information"] = missing
    return c


def generate_task_relevance_field_projection_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any],
) -> Dict[str, Any]:
    entities = input_view.get("entity_candidates") or []
    zone = input_view.get("zone_summary") or {}
    zone_cands = []
    for key in ("inner_zone_entity_count", "working_zone_entity_count", "forecast_zone_entity_count", "unknown_zone_entity_count"):
        if zone.get(key, 0) > 0:
            zone_cands.append({"zone_key": key.replace("_entity_count", ""), "entity_count": zone[key]})
    entity_cands = [
        {"entity_ref": e.get("entity_id") or e.get("observation_id"), "label": e.get("label"), "relevance_reason": "entity_in_active_field"}
        for e in entities
    ]
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="task_relevance_field_projection",
        status="generated", confidence="medium",
    )
    c["task_relevant_zone_candidates"] = zone_cands
    c["task_relevant_entity_candidates"] = entity_cands
    c["relevance_reason_codes"] = ["entity_and_zone_present"]
    c["projected_entities"] = entity_cands
    c["projected_zones"] = zone_cands
    return c


def generate_safety_risk_projection_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any],
) -> Dict[str, Any]:
    entities = input_view.get("entity_candidates") or []
    zone = input_view.get("zone_summary") or {}
    risks = []
    if zone.get("inner_zone_entity_count", 0) > 0:
        risks.append({"risk_type": "inner_zone_entity_present", "risk_zone": "inner_zone", "risk_confidence": "medium"})
    if zone.get("unknown_zone_entity_count", 0) > 0:
        risks.append({"risk_type": "unknown_zone_entity_present", "risk_zone": "unknown_zone", "risk_confidence": "low"})
    for e in entities:
        if float(e.get("confidence", 1.0)) < 0.6:
            risks.append({
                "risk_type": "low_confidence_entity",
                "entity_ref": e.get("entity_id") or e.get("observation_id"),
                "risk_confidence": "low",
            })
        if e.get("entity_status") == "entity_geometry_unknown":
            risks.append({
                "risk_type": "geometry_unknown_in_field",
                "entity_ref": e.get("entity_id") or e.get("observation_id"),
                "risk_zone": e.get("field_zone_hint", "working_zone"),
                "risk_confidence": "low",
            })
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="safety_risk_projection",
        status="generated_degraded" if risks else "generated",
        confidence="medium" if risks else "low",
    )
    c["safety_risk_candidates"] = risks
    c["risk_reason_codes"] = [r["risk_type"] for r in risks]
    c["projected_risks"] = risks
    return c


def generate_field_quality_projection_candidate(
    input_view: Dict[str, Any], plan: Dict[str, Any],
) -> Dict[str, Any]:
    sq = input_view.get("scene_quality_summary") or {}
    dq = input_view.get("depth_quality_summary") or {}
    gq = input_view.get("geometry_quality_summary") or {}
    blockers = []
    warnings = []
    if sq.get("scene_quality") == "degraded":
        warnings.extend(sq.get("degraded_reasons") or [])
    if dq.get("depth_quality") == "degraded":
        blockers.append("depth_quality_degraded")
    if gq.get("geometry_unknown_count", 0) > 0:
        blockers.append("geometry_unknown_present")
    status = "degraded_usable" if warnings or blockers else "usable"
    c = _base_candidate(
        plan=plan, input_view=input_view, mode="field_quality_projection",
        status="generated_degraded" if blockers else "generated",
        confidence="medium",
    )
    c["field_quality_projection_status"] = status
    c["blockers"] = blockers
    c["warnings"] = warnings
    c["readiness_for_next_stage"] = status in ("usable", "degraded_usable")
    c["projected_quality_status"] = status
    return c


_GENERATORS = {
    "current_state_simulation": generate_current_state_simulation_candidate,
    "short_horizon_motion_projection": generate_short_horizon_motion_projection_candidate,
    "occlusion_and_missing_info_simulation": generate_occlusion_missing_info_simulation_candidate,
    "task_relevance_field_projection": generate_task_relevance_field_projection_candidate,
    "safety_risk_projection": generate_safety_risk_projection_candidate,
    "field_quality_projection": generate_field_quality_projection_candidate,
}


def generate_field_simulation_candidates(
    *,
    input_view: Dict[str, Any],
    plan: Dict[str, Any],
    eligibility: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Generate FieldSimulationCandidate per selected/blocked modes."""
    candidates: List[Dict[str, Any]] = []
    selected = set(plan.get("selected_modes") or [])
    blocked = set(plan.get("blocked_modes") or [])
    degraded = eligibility.get("eligibility_status") in ("eligible_degraded", "eligible_full")

    if not input_view.get("enhanced_field_scene_ref"):
        for mode in SIMULATION_MODES:
            c = _base_candidate(
                plan=plan, input_view=input_view, mode=mode,
                status="blocked_no_scene", confidence="blocked",
                blocked_reason="no_enhanced_field_scene",
            )
            candidates.append(c)
        return candidates

    if not (input_view.get("entity_candidates") or []):
        for mode in SIMULATION_MODES:
            c = _base_candidate(
                plan=plan, input_view=input_view, mode=mode,
                status="blocked_no_entity", confidence="blocked",
                blocked_reason="no_entity_candidates",
            )
            candidates.append(c)
        return candidates

    if eligibility.get("eligibility_status") == "blocked_quality_insufficient":
        for mode in SIMULATION_MODES:
            c = _base_candidate(
                plan=plan, input_view=input_view, mode=mode,
                status="blocked_quality_insufficient", confidence="blocked",
                blocked_reason="failure_localization_baseline",
            )
            candidates.append(c)
        return candidates

    for mode in selected:
        gen = _GENERATORS.get(mode)
        if not gen:
            continue
        if mode == "current_state_simulation":
            candidates.append(gen(input_view, plan, degraded=degraded))
        elif mode == "short_horizon_motion_projection":
            candidates.append(gen(input_view, plan, blocked=False))
        else:
            candidates.append(gen(input_view, plan))

    if "short_horizon_motion_projection" in blocked and "short_horizon_motion_projection" not in selected:
        candidates.append(
            generate_short_horizon_motion_projection_candidate(input_view, plan, blocked=True)
        )

    return candidates
