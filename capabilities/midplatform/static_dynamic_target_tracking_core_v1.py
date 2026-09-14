# -*- coding: utf-8 -*-
"""Static/Dynamic target locking tracking core v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.dynamic_target_tracking_builder_v1 import build_dynamic_target_track_candidates
from capabilities.midplatform.static_dynamic_target_locking_builder_v1 import build_static_target_lock_candidates
from capabilities.midplatform.static_dynamic_target_locking_tracking_types_v1 import (
    CONTINUITY_ALLOWED,
    CONTINUITY_FREEZE,
    CONTINUITY_RESET,
    NON_EXECUTION_FLAGS,
)
from capabilities.midplatform.static_dynamic_target_tracking_static_validators_v1 import (
    validate_dryrun_result_candidate,
    validate_dynamic_target_track_candidate,
    validate_static_target_lock_candidate,
    validate_target_impact_candidate,
    validate_target_tracking_plan_candidate,
)
from capabilities.midplatform.target_task_impact_scorer_v1 import score_target_task_impact


def run_controlled_target_locking_tracking(
    *,
    previous_field_scene_summary: Dict[str, Any],
    current_field_scene_summary: Dict[str, Any],
    continuity_decision: Dict[str, Any],
    field_session_ref: str = "fsess_mock",
    tracker_hint_id: str | None = None,
) -> Dict[str, Any]:
    status = continuity_decision.get("continuity_status", "uncertain_need_recheck")
    static_locks = build_static_target_lock_candidates(
        previous_field_scene_summary=previous_field_scene_summary,
        current_field_scene_summary=current_field_scene_summary,
        continuity_decision=continuity_decision,
        field_session_ref=field_session_ref,
    )
    dynamic_tracks = build_dynamic_target_track_candidates(
        previous_field_scene_summary=previous_field_scene_summary,
        current_field_scene_summary=current_field_scene_summary,
        continuity_decision=continuity_decision,
        field_session_ref=field_session_ref,
        tracker_hint_id=tracker_hint_id,
    )
    impacts: List[Dict[str, Any]] = []
    for lock in static_locks:
        impacts.append(score_target_task_impact(
            target_ref=lock["entity_candidate_ref"], label=lock["label"],
            field_zone=lock.get("field_zone", "unknown"),
            visibility_status=lock.get("visibility_status", "visible"),
        ))
    for track in dynamic_tracks:
        impacts.append(score_target_task_impact(
            target_ref=track["current_entity_candidate_ref"], label=track["label"],
            field_zone="unknown", motion_status=track.get("motion_status", "unknown"),
        ))
    plan = {
        "plan_candidate_id": f"ttp_{uuid.uuid4().hex[:12]}",
        "field_session_ref": field_session_ref,
        "continuity_status": status,
        "static_locks": static_locks,
        "dynamic_tracks": dynamic_tracks,
        "target_impacts": impacts,
        "tracking_allowed": status in CONTINUITY_ALLOWED,
        "tracking_frozen": status in CONTINUITY_FREEZE,
        "tracking_reset": status in CONTINUITY_RESET,
        "reason_codes": [f"plan_{status}"],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }
    for lock in static_locks:
        validate_static_target_lock_candidate(lock)
    for track in dynamic_tracks:
        validate_dynamic_target_track_candidate(track)
    for imp in impacts:
        validate_target_impact_candidate(imp)
    validate_target_tracking_plan_candidate(plan)
    return plan


def run_target_locking_tracking_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    continuity = {"continuity_status": case["continuity_status"]}
    plan = run_controlled_target_locking_tracking(
        previous_field_scene_summary=case["prev_scene"],
        current_field_scene_summary=case["curr_scene"],
        continuity_decision=continuity,
        field_session_ref=case["field_session_ref"],
        tracker_hint_id=case.get("tracker_hint_id"),
    )
    static_locks = plan["static_locks"]
    dynamic_tracks = plan["dynamic_tracks"]
    hints = tuple({i["task_impact_hint"] for i in plan["target_impacts"]})
    passed = True
    if len(static_locks) != case["expected_static_lock_count"]:
        passed = False
    if len(dynamic_tracks) != case["expected_dynamic_track_count"]:
        passed = False
    for h in case.get("expected_task_impact_hints") or ():
        if h not in hints:
            passed = False
    if case.get("expected_lock_status"):
        if not any(l.get("lock_status") == case["expected_lock_status"] for l in static_locks):
            passed = False
    if case.get("expected_visibility"):
        if not any(l.get("visibility_status") == case["expected_visibility"] for l in static_locks):
            passed = False
    if case.get("expected_motion"):
        if not any(t.get("motion_status") == case["expected_motion"] for t in dynamic_tracks):
            passed = False
    if case.get("expected_weak_track"):
        if not any(t.get("lock_status") == "weak_locked" for t in dynamic_tracks):
            passed = False
    if case.get("expected_low_stability"):
        if not any((l.get("stability_score") or 1) < 0.7 for l in static_locks):
            passed = False
    if case.get("expected_priority") == "P0":
        if not any(i.get("priority_level") == "P0" for i in plan["target_impacts"]):
            passed = False
    prohibited_absent = True
    if case["continuity_status"] == "new_field_required" and static_locks:
        prohibited_absent = False
    result = {
        "case_id": case["case_id"],
        "expected_static_lock_count": case["expected_static_lock_count"],
        "actual_static_lock_count": len(static_locks),
        "expected_dynamic_track_count": case["expected_dynamic_track_count"],
        "actual_dynamic_track_count": len(dynamic_tracks),
        "expected_task_impact_hints": list(case.get("expected_task_impact_hints") or ()),
        "actual_task_impact_hints": list(hints),
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
        "reason_codes": plan["reason_codes"],
        "plan": plan,
    }
    validate_dryrun_result_candidate(result)
    return result


def run_all_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_target_locking_tracking_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
