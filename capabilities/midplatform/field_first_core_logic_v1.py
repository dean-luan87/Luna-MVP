# -*- coding: utf-8 -*-
"""Field-First Core Logic — main pipeline v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.field_continuity_detection_decision_builder_v1 import build_field_continuity_decision_candidate
from capabilities.midplatform.field_continuity_detection_signal_scoring_v1 import score_all_signals
from capabilities.midplatform.field_first_core_logic_types_v1 import INPUT_PACKAGE_FIELDS, NON_EXECUTION_FLAGS, PIPELINE_STAGES
from capabilities.midplatform.field_first_core_pipeline_v1 import (
    derive_continuity_evaluation_context,
    infer_depth_source_from_scene,
    scene_to_tracking_summary,
)
from capabilities.midplatform.field_first_core_result_assembler_v1 import assemble_field_first_core_logic_result
from capabilities.midplatform.field_scene_small_range_builder_v1 import construct_small_range_field_scene
from capabilities.midplatform.static_dynamic_target_tracking_core_v1 import run_controlled_target_locking_tracking
from capabilities.midplatform.trajectory_analysis_task_impact_core_v1 import run_controlled_trajectory_analysis_task_impact


def build_field_first_core_input_package(
    *,
    current_observation_candidates: List[Dict[str, Any]],
    previous_field_scene_candidate: Optional[Dict[str, Any]] = None,
    previous_field_session_state: str = "active",
    previous_target_tracking_plan_candidate: Optional[Dict[str, Any]] = None,
    camera_state_candidate: Optional[Dict[str, Any]] = None,
    user_state_candidate: Optional[Dict[str, Any]] = None,
    task_goal_ref: Optional[str] = None,
    timestamp: str = "2026-06-11T00:00:00Z",
    source_refs: Optional[List[str]] = None,
    traceability_refs: Optional[List[str]] = None,
    field_session_ref: str = "fsess_core",
) -> Dict[str, Any]:
    pkg = {
        "input_package_id": f"ffip_{uuid.uuid4().hex[:12]}",
        "current_observation_candidates": current_observation_candidates,
        "previous_field_scene_candidate": previous_field_scene_candidate,
        "previous_field_session_state": previous_field_session_state,
        "previous_target_tracking_plan_candidate": previous_target_tracking_plan_candidate,
        "camera_state_candidate": camera_state_candidate or {
            "camera_ref": "camera_mock", "frame_width": 640, "frame_height": 480, "timestamp": timestamp,
        },
        "user_state_candidate": user_state_candidate or {"user_ref": "user_self_ref", "timestamp": timestamp},
        "task_goal_ref": task_goal_ref,
        "timestamp": timestamp,
        "source_refs": source_refs or ["field_first_core_pipeline_v1"],
        "traceability_refs": traceability_refs or [field_session_ref],
        "candidate_only": True,
        "_field_session_ref": field_session_ref,
    }
    for f in INPUT_PACKAGE_FIELDS:
        if f not in pkg and not f.startswith("_"):
            raise ValueError(f"missing_field:{f}")
    return pkg


def run_field_first_core_pipeline(
    input_package: Dict[str, Any],
    *,
    continuity_evaluation_context: Optional[Dict[str, Any]] = None,
    previous_observations: Optional[List[Dict[str, Any]]] = None,
    depth_candidate: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    stage_results: List[Dict[str, Any]] = []
    warnings: List[str] = []
    field_session_ref = input_package.get("_field_session_ref") or "fsess_core"
    camera = input_package["camera_state_candidate"]
    user = input_package["user_state_candidate"]

    # step 1: build field scene
    construction = construct_small_range_field_scene(
        observations=input_package["current_observation_candidates"],
        user_state=user,
        camera_state=camera,
        depth_candidate=depth_candidate,
        field_session_ref=field_session_ref,
    )
    current_scene = construction["field_scene"]
    warnings.extend(construction.get("warnings") or [])
    stage_results.append({
        "stage": PIPELINE_STAGES[0],
        "status": "completed" if construction.get("construction_pass") else "partial",
        "field_scene_ref": current_scene.get("field_scene_id"),
        "entity_count": len(current_scene.get("entity_candidates") or []),
        "reason_codes": ["field_scene_constructed"],
    })

    # previous scene
    previous_scene = input_package.get("previous_field_scene_candidate")
    if previous_scene is None and previous_observations:
        prev_construction = construct_small_range_field_scene(
            observations=previous_observations,
            user_state=user,
            camera_state=camera,
            depth_candidate=depth_candidate,
            field_session_ref=field_session_ref,
        )
        previous_scene = prev_construction["field_scene"]
        warnings.extend(prev_construction.get("warnings") or [])

    prev_summary = scene_to_tracking_summary(previous_scene) if previous_scene else {"field_scene_id": "fs_none", "entities": []}
    curr_summary = scene_to_tracking_summary(current_scene)

    # step 2: continuity
    eval_ctx = derive_continuity_evaluation_context(
        previous_scene=previous_scene,
        current_scene=current_scene,
        override=continuity_evaluation_context,
    )
    eval_ctx["previous_session_state"] = input_package.get("previous_field_session_state", "active")
    signals = score_all_signals(eval_ctx)
    continuity_decision = build_field_continuity_decision_candidate(
        previous_field_scene_summary=prev_summary,
        current_field_scene_summary=curr_summary,
        signal_results=signals,
        previous_field_session_state=input_package.get("previous_field_session_state", "active"),
        previous_field_session_ref=field_session_ref,
    )
    stage_results.append({
        "stage": PIPELINE_STAGES[1],
        "status": "completed",
        "continuity_status": continuity_decision.get("continuity_status"),
        "reason_codes": continuity_decision.get("reason_codes") or [],
    })

    # step 3: target locking / tracking
    tracking_plan = run_controlled_target_locking_tracking(
        previous_field_scene_summary=prev_summary,
        current_field_scene_summary=curr_summary,
        continuity_decision={"continuity_status": continuity_decision["continuity_status"]},
        field_session_ref=field_session_ref,
    )
    stage_results.append({
        "stage": PIPELINE_STAGES[2],
        "status": "completed",
        "tracking_allowed": tracking_plan.get("tracking_allowed"),
        "tracking_frozen": tracking_plan.get("tracking_frozen"),
        "tracking_reset": tracking_plan.get("tracking_reset"),
        "static_lock_count": len(tracking_plan.get("static_locks") or []),
        "dynamic_track_count": len(tracking_plan.get("dynamic_tracks") or []),
    })

    # step 4: trajectory / task impact
    depth_source = infer_depth_source_from_scene(current_scene)
    trajectory_analysis = run_controlled_trajectory_analysis_task_impact(
        tracking_plan=tracking_plan,
        task_goal_ref=input_package.get("task_goal_ref"),
        depth_source=depth_source,
    )
    stage_results.append({
        "stage": PIPELINE_STAGES[3],
        "status": "completed",
        "trajectory_count": len(trajectory_analysis.get("trajectory_candidates") or []),
        "task_impact_count": len(trajectory_analysis.get("task_impact_analysis_candidates") or []),
        "missing_count": len(trajectory_analysis.get("missing_information_candidates") or []),
    })

    # step 5: assemble
    result = assemble_field_first_core_logic_result(
        input_package=input_package,
        field_scene=current_scene,
        continuity_decision=continuity_decision,
        tracking_plan=tracking_plan,
        trajectory_analysis=trajectory_analysis,
        pipeline_stage_results=stage_results,
        warnings=warnings,
    )
    stage_results.append({
        "stage": PIPELINE_STAGES[4],
        "status": "completed",
        "result_candidate_id": result.get("result_candidate_id"),
    })
    result["pipeline_stage_results"] = stage_results
    return {
        "input_package": input_package,
        "pipeline_stage_results": stage_results,
        "final_result_candidate": result,
        "warnings": warnings,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
    }


def run_field_first_core_pipeline_dryrun(case: Dict[str, Any]) -> Dict[str, Any]:
    pkg = build_field_first_core_input_package(
        current_observation_candidates=case["current_observations"],
        previous_field_scene_candidate=case.get("previous_field_scene_candidate"),
        previous_field_session_state=case.get("previous_field_session_state", "active"),
        task_goal_ref=case.get("task_goal_ref"),
        field_session_ref=case.get("field_session_ref", f"fsess_{case['case_id']}"),
        camera_state_candidate=case.get("camera_state_candidate"),
        user_state_candidate=case.get("user_state_candidate"),
    )
    pipeline_out = run_field_first_core_pipeline(
        pkg,
        continuity_evaluation_context=case.get("continuity_evaluation_context"),
        previous_observations=case.get("previous_observations"),
        depth_candidate=case.get("depth_candidate"),
    )
    result = pipeline_out["final_result_candidate"]
    continuity_status = result["field_continuity_decision_candidate"]["continuity_status"]
    static_locks = result.get("static_target_lock_candidates") or []
    dynamic_tracks = result.get("dynamic_target_track_candidates") or []
    trajectories = result.get("trajectory_candidates") or []
    impacts = result.get("task_impact_analysis_candidates") or []
    missing = result.get("missing_information_candidates") or []
    missing_types = {m.get("missing_type") for m in missing}
    impact_types = {i.get("task_impact_type") for i in impacts}

    passed = True
    if case.get("expected_field_status") and continuity_status != case["expected_field_status"]:
        passed = False
    if len(static_locks) != case.get("expected_static_locks", len(static_locks)):
        passed = False
    if len(dynamic_tracks) != case.get("expected_dynamic_tracks", len(dynamic_tracks)):
        passed = False
    if len(trajectories) != case.get("expected_trajectory_candidates", len(trajectories)):
        passed = False
    if case.get("expected_task_impacts_min") is not None and len(impacts) < case["expected_task_impacts_min"]:
        passed = False
    for it in case.get("expected_task_impact_types") or ():
        if it not in impact_types:
            passed = False
    for mt in case.get("expected_missing_information") or ():
        if mt not in missing_types:
            passed = False
    if case.get("expect_no_trajectory") and trajectories:
        passed = False
    if case.get("expect_tracking_frozen") and not result["target_tracking_plan_candidate"].get("tracking_frozen"):
        passed = False
    if case.get("expect_low_confidence_retained"):
        scene = result.get("field_scene_candidate") or {}
        if not any((e.get("confidence") or 1) < 0.4 for e in scene.get("entity_candidates") or []):
            passed = False
    if case.get("expect_duplicate_count"):
        labels = [e.get("label") for e in (result.get("field_scene_candidate") or {}).get("entity_candidates") or []]
        if labels.count(case["expect_duplicate_count"]["label"]) < case["expect_duplicate_count"]["min"]:
            passed = False

    prohibited_absent = True
    if continuity_status == "new_field_required" and (static_locks or dynamic_tracks or trajectories):
        prohibited_absent = False
    if continuity_status == "field_occluded" and trajectories:
        prohibited_absent = False
    if result.get("non_execution_flags", {}).get("no_final_action_output") is not True:
        prohibited_absent = False

    return {
        "case_id": case["case_id"],
        "pipeline_stage_results": pipeline_out["pipeline_stage_results"],
        "final_result_candidate": result,
        "expected_field_status": case.get("expected_field_status"),
        "expected_static_locks": case.get("expected_static_locks"),
        "expected_dynamic_tracks": case.get("expected_dynamic_tracks"),
        "expected_trajectory_candidates": case.get("expected_trajectory_candidates"),
        "expected_task_impacts": case.get("expected_task_impacts_min"),
        "expected_missing_information": list(case.get("expected_missing_information") or ()),
        "prohibited_behavior_absent": prohibited_absent,
        "case_passed": passed and prohibited_absent,
    }


def run_all_core_pipeline_dryrun_cases(cases: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], bool]:
    results = [run_field_first_core_pipeline_dryrun(c) for c in cases]
    return results, all(r["case_passed"] for r in results)
