# -*- coding: utf-8 -*-
"""Trajectory analysis & task impact core v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.risk_projection_builder_v1 import build_risk_projection_candidates
from capabilities.midplatform.static_dynamic_target_tracking_core_v1 import run_controlled_target_locking_tracking
from capabilities.midplatform.task_impact_analyzer_v1 import (
    analyze_dynamic_task_impacts,
    analyze_static_task_impacts,
    collect_missing_information,
)
from capabilities.midplatform.trajectory_analysis_static_validators_v1 import (
    validate_analysis_result,
    validate_missing_information_candidate,
    validate_risk_projection_candidate,
    validate_task_impact_analysis_candidate,
    validate_trajectory_candidate,
    validate_trajectory_dryrun_result,
)
from capabilities.midplatform.trajectory_analysis_task_impact_types_v1 import NON_EXECUTION_FLAGS
from capabilities.midplatform.trajectory_builder_v1 import build_trajectory_candidates


def run_controlled_trajectory_analysis_task_impact(
    *,
    tracking_plan: Dict[str, Any],
    task_goal_ref: str | None = None,
    depth_source: str = "estimated",
) -> Dict[str, Any]:
    trajectories = build_trajectory_candidates(tracking_plan=tracking_plan, depth_source=depth_source)
    static_impacts = analyze_static_task_impacts(tracking_plan=tracking_plan, task_goal_ref=task_goal_ref)
    dynamic_impacts = analyze_dynamic_task_impacts(
        tracking_plan=tracking_plan, trajectories=trajectories, task_goal_ref=task_goal_ref,
    )
    impacts = static_impacts + dynamic_impacts
    risks = build_risk_projection_candidates(task_impacts=impacts, trajectories=trajectories)
    missing = collect_missing_information(
        tracking_plan=tracking_plan, trajectories=trajectories, depth_source=depth_source,
    )
    result = {
        "analysis_result_id": f"tai_{uuid.uuid4().hex[:12]}",
        "field_session_ref": tracking_plan.get("field_session_ref", "fsess_mock"),
        "trajectory_candidates": trajectories,
        "task_impact_analysis_candidates": impacts,
        "risk_projection_candidates": risks,
        "missing_information_candidates": missing,
        "tracking_allowed": tracking_plan.get("tracking_allowed"),
        "tracking_frozen": tracking_plan.get("tracking_frozen"),
        "tracking_reset": tracking_plan.get("tracking_reset"),
        "reason_codes": list(tracking_plan.get("reason_codes") or []) + ["trajectory_analysis_complete"],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }
    for t in trajectories:
        validate_trajectory_candidate(t)
    for i in impacts:
        validate_task_impact_analysis_candidate(i)
    for r in risks:
        validate_risk_projection_candidate(r)
    for m in missing:
        validate_missing_information_candidate(m)
    validate_analysis_result(result)
    return result


def run_trajectory_analysis_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    continuity = {"continuity_status": case["continuity_status"]}
    plan = run_controlled_target_locking_tracking(
        previous_field_scene_summary=case["prev_scene"],
        current_field_scene_summary=case["curr_scene"],
        continuity_decision=continuity,
        field_session_ref=case.get("field_session_ref", "fsess_mock"),
        tracker_hint_id=case.get("tracker_hint_id"),
    )
    if case.get("inject_track_without_prev"):
        for track in plan.get("dynamic_tracks") or []:
            track.pop("previous_pseudo_3d_position", None)
            track.pop("previous_bbox", None)
    analysis = run_controlled_trajectory_analysis_task_impact(
        tracking_plan=plan,
        task_goal_ref=case.get("task_goal_ref"),
        depth_source=case.get("depth_source", "estimated"),
    )
    trajectories = analysis["trajectory_candidates"]
    impacts = analysis["task_impact_analysis_candidates"]
    risks = analysis["risk_projection_candidates"]
    missing = analysis["missing_information_candidates"]
    motions = {t.get("motion_pattern") for t in trajectories}
    impact_types = {i.get("task_impact_type") for i in impacts}
    missing_types = {m.get("missing_type") for m in missing}

    passed = True
    if len(trajectories) != case.get("expected_trajectory_count", 0):
        passed = False
    if len(impacts) < case.get("expected_task_impact_min", case.get("expected_task_impact_count", 0)):
        passed = False
    for mp in case.get("expected_motion_patterns") or ():
        if mp not in motions:
            passed = False
    for it in case.get("expected_task_impact_types") or ():
        if it not in impact_types:
            passed = False
    for mt in case.get("expected_missing_types") or ():
        if mt not in missing_types:
            passed = False
    if case.get("expect_no_trajectory") and trajectories:
        passed = False
    if case.get("max_trajectory_confidence"):
        levels = ("high", "medium", "low", "unknown")
        max_idx = levels.index(case["max_trajectory_confidence"])
        for t in trajectories:
            if levels.index(t.get("trajectory_confidence", "unknown")) < max_idx:
                passed = False

    prohibited_absent = True
    if "final_action" in (case.get("prohibited") or ()):
        prohibited_absent = True
    if case.get("continuity_status") == "field_occluded" and trajectories:
        prohibited_absent = False
    if case.get("continuity_status") == "new_field_required" and trajectories:
        prohibited_absent = False

    result = {
        "case_id": case["case_id"],
        "expected_trajectory_count": case.get("expected_trajectory_count", 0),
        "actual_trajectory_count": len(trajectories),
        "expected_task_impact_count": case.get("expected_task_impact_count", case.get("expected_task_impact_min", 0)),
        "actual_task_impact_count": len(impacts),
        "expected_risk_count": case.get("expected_risk_count", 0),
        "actual_risk_count": len(risks),
        "expected_motion_patterns": list(case.get("expected_motion_patterns") or ()),
        "actual_motion_patterns": list(motions),
        "expected_task_impact_types": list(case.get("expected_task_impact_types") or ()),
        "actual_task_impact_types": list(impact_types),
        "expected_missing_types": list(case.get("expected_missing_types") or ()),
        "actual_missing_types": list(missing_types),
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": analysis["reason_codes"],
        "analysis": analysis,
        "plan": plan,
    }
    validate_trajectory_dryrun_result(result)
    return result


def run_all_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_trajectory_analysis_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
