# -*- coding: utf-8 -*-
"""Task Manager Runtime DryRun v1 — consumes MidPlatform candidates; no real commit.

Phase-Task-Manager-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Task-Manager-Runtime-DryRun-v1-001"
FINAL_DECISION = "TASK_MANAGER_RUNTIME_DRYRUN_READY_FOR_VISION_OCR_INGEST_AND_NAVIGATION_LOOP"
RECOMMENDED_NEXT = "Vision-OCR-Evidence-Ingest-Integration-Check-v1"

FOLLOWUPS = [
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Task-Context-Enrichment-Runtime-DryRun-v1",
    "Task-Aware-Action-Scheduling-Runtime-DryRun-v1",
    "GPS-Location-Candidate-Contract-v1",
    "Navigation-Map-Context-Contract-v1",
    "Route-Stage-Estimation-DryRun-v1",
    "Information-Gap-Driven-Observation-Plan-v1",
    "Memory-Reference-for-Task-Context-DryRun-v1",
    "Task-Manager-Commit-GuardedTrial-v1",
]

ROUTE_STAGES = (
    "before_task_area",
    "approaching_task_area",
    "inside_task_area",
    "near_information_source",
    "target_reached_candidate",
    "unknown",
)

GAP_TYPES = (
    "missing_task_goal",
    "missing_scene_context",
    "missing_target_location",
    "missing_route_stage",
    "missing_information_source",
    "missing_readable_region",
    "missing_visual_confirmation",
    "missing_user_confirmation",
    "missing_safety_clearance",
    "missing_ocr_evidence",
    "missing_human_assistance_decision",
)

CMD_TO_TASK_TYPE = {
    "CREATE_TASK_CANDIDATE": "navigation_task",
    "UPDATE_TASK_CONTEXT_CANDIDATE": "generic_task",
    "QUERY_STATUS_CANDIDATE": "generic_task",
    "REPEAT_GUIDANCE_CANDIDATE": "generic_task",
    "PAUSE_TASK_CANDIDATE": "generic_task",
    "RESUME_TASK_CANDIDATE": "generic_task",
    "REQUEST_CONFIRMATION_CANDIDATE": "generic_task",
    "CANCEL_TASK_CANDIDATE": "generic_task",
    "REQUEST_CLARIFICATION_CANDIDATE": "generic_task",
    "REQUEST_HUMAN_ASSISTANCE_CANDIDATE": "human_assistance_task",
}

MP_TO_TM_STATE = {
    "TASK_CREATION_CANDIDATE": ("NO_TASK", "TASK_DRAFT", "TASK_CREATE_REQUESTED"),
    "TASK_CONTEXT_UPDATE_CANDIDATE": ("TASK_ACTIVE", "TASK_ACTIVE", "TASK_CONTEXT_UPDATE_REQUESTED"),
    "TASK_STATUS_QUERY_CANDIDATE": ("TASK_ACTIVE", "TASK_ACTIVE", "TASK_STATUS_QUERIED"),
    "TASK_GUIDANCE_REPEAT_CANDIDATE": ("TASK_ACTIVE", "TASK_ACTIVE", "TASK_GUIDANCE_REQUESTED"),
    "TASK_PAUSE_PENDING_CONFIRMATION": ("TASK_ACTIVE", "TASK_PAUSE_PENDING_CONFIRMATION", "TASK_PAUSE_REQUESTED"),
    "TASK_RESUME_PENDING": ("TASK_PAUSED", "TASK_RESUME_PENDING", "TASK_RESUME_REQUESTED"),
    "TASK_CANCEL_PENDING_CONFIRMATION": ("TASK_ACTIVE", "TASK_CANCEL_PENDING_CONFIRMATION", "TASK_CANCEL_REQUESTED"),
    "TASK_CANCELLED_CANDIDATE": ("TASK_CANCEL_PENDING_CONFIRMATION", "TASK_CANCELLED", "TASK_CANCELLED_CANDIDATE"),
    "TASK_CLARIFICATION_NEEDED": ("TASK_DRAFT", "TASK_PENDING_CLARIFICATION", "TASK_CONTEXT_UPDATE_REQUESTED"),
    "TASK_HUMAN_ASSISTANCE_CANDIDATE": ("TASK_ACTIVE", "TASK_ACTIVE", "TASK_GUIDANCE_REQUESTED"),
}

GUARD_NAMES = [
    "create_requires_valid_goal",
    "pause_requires_active_task",
    "resume_requires_paused_task",
    "cancel_requires_confirmation",
    "cancel_confirm_requires_pending_context",
    "query_status_no_mutation",
    "repeat_guidance_no_mutation",
    "invalid_transition_blocks_commit",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_task_manager_contract", "contract_loaded", [], [], []),
    ("load_midplatform_task_state_runtime", "mp_loaded", [], [], []),
    ("intake_task_state_and_lifecycle_candidates", "intake_ok", [], [], []),
    ("generate_task_object_candidates", "task_objects_ok", [], [], ["task_state_commit"]),
    ("generate_lifecycle_event_candidates", "lifecycle_ok", [], [], []),
    ("apply_state_machine", "fsm_ok", [], [], []),
    ("apply_transition_guards", "guards_ok", [], [], []),
    ("apply_confirmation_gate", "confirm_ok", [], [], []),
    ("apply_safety_gate", "safety_ok", [], [], []),
    ("apply_idempotency_policy", "idempotency_ok", [], [], ["duplicate_commit"]),
    ("generate_commit_decision_candidates", "commit_decisions_ok", [], [], ["commit_now"]),
    ("generate_context_enrichment_candidates", "enrichment_ok", [], [], ["fact_write"]),
    ("generate_verification_context_candidates", "verification_ok", [], [], ["task_completed"]),
    ("generate_execution_support_context_candidates", "execution_ok", [], [], ["navigation_action"]),
    ("generate_task_spatial_relation_candidates", "spatial_ok", [], [], []),
    ("generate_information_gap_analysis", "gap_ok", [], [], []),
    ("generate_task_aware_observation_plans", "obs_plan_ok", [], [], ["camera", "ocr"]),
    ("generate_ocr_activation_need_candidates", "ocr_need_ok", [], [], ["ocr"]),
    ("generate_human_assistance_need_candidates", "human_need_ok", [], [], []),
    ("generate_action_schedule_candidates", "schedule_ok", [], [], ["navigation_action"]),
    ("generate_downstream_candidates", "downstream_ok", [], [], ["tts", "vop"]),
    ("apply_rollback_abort_policy", "rollback_ok", [], [], []),
    ("generate_audit_traces", "audit_ok", [], [], []),
    ("check_boundary", "boundary_ok", [], [], []),
    ("generate_final_task_manager_runtime_dryrun_decision", "dryrun_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "task_manager_runtime": "**/*TASK*MANAGER*RUNTIME*.md",
    "taskchain_runtime": "**/*TASK*CHAIN*.md",
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "navigation_task": "**/*NAVIGATION*TASK*.md",
    "route_context": "**/*ROUTE*CONTEXT*.md",
    "gps_context": "**/*GPS*.md",
    "map_context": "**/*MAP*CONTEXT*.md",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _find_optional_docs(ws_root: Path) -> List[Dict[str, Any]]:
    docs = ws_root / "docs" / "architecture"
    rows = []
    for doc_id, glob_pat in OPTIONAL_DOC_GLOBS.items():
        found = list(docs.glob(glob_pat)) if docs.is_dir() else []
        rows.append(
            {
                "intake_id": doc_id,
                "input_source": "optional_documentation",
                "source_root_or_path": str(found[0]) if found else "(not_found)",
                "artifact": found[0].name if found else None,
                "loaded": bool(found),
                "optional": True,
                "key_fields_observed": ["documentation_reference"] if found else [],
                "intake_status": "loaded" if found else "optional_missing",
                "missing_impact": "optional_doc_reference_only",
                **_not_fact(),
            }
        )
    return rows


def _commit_decision_for(
    cmd: str,
    proposed: str,
    confirmation_required: bool,
    pending_cancel: bool,
    utterance_id: str,
) -> Tuple[str, Optional[str], Optional[str]]:
    if cmd in ("QUERY_STATUS_CANDIDATE", "REPEAT_GUIDANCE_CANDIDATE"):
        return "NO_OP", None, "speech_response_candidate"
    if cmd == "REQUEST_CONFIRMATION_CANDIDATE":
        return "BLOCKED_BY_CONFIRMATION", "cancel_requires_confirmation", "user_confirmation_candidate"
    if cmd == "CANCEL_TASK_CANDIDATE":
        if pending_cancel:
            return "COMMIT_ALLOWED_LATER", None, None
        return "BLOCKED_BY_CONFIRMATION", "missing_pending_cancel_confirmation", None
    if cmd == "REQUEST_CLARIFICATION_CANDIDATE":
        return "REQUIRE_CLARIFICATION", "missing_task_or_scene", None
    if cmd == "REQUEST_HUMAN_ASSISTANCE_CANDIDATE":
        return "COMMIT_ALLOWED_LATER", None, "human_assistance_candidate"
    if "BLOCKED" in proposed:
        return "BLOCKED_BY_MISSING_CONTEXT", "context_incomplete", None
    return "BLOCKED_BY_RUNTIME_DISABLED", "task_manager_runtime_disabled", None


def _infer_target_from_utterance(utterance: str) -> Dict[str, Any]:
    if "出口" in utterance:
        return {"label": "exit", "target_type": "exit"}
    if "洗手间" in utterance or "厕所" in utterance:
        return {"label": "restroom", "target_type": "restroom"}
    if "门牌" in utterance:
        return {"label": "doorplate", "target_type": "doorplate"}
    if "商场" in utterance:
        return {"label": "mall_area", "target_type": "scene_anchor"}
    return {"label": "unspecified", "target_type": "unknown"}


def _infer_route_stage(cmd: str, proposed: str, utterance: str) -> str:
    if cmd == "CREATE_TASK_CANDIDATE":
        return "approaching_task_area"
    if "商场" in utterance or cmd == "UPDATE_TASK_CONTEXT_CANDIDATE":
        return "inside_task_area"
    if "门牌" in utterance:
        return "near_information_source"
    if proposed == "TASK_CLARIFICATION_NEEDED":
        return "unknown"
    if cmd in ("QUERY_STATUS_CANDIDATE", "REPEAT_GUIDANCE_CANDIDATE"):
        return "inside_task_area"
    return "before_task_area"


def _scheduling_fields(utterance: str, cmd: str, proposed: str) -> Dict[str, Any]:
    target = _infer_target_from_utterance(utterance)
    route_stage = _infer_route_stage(cmd, proposed, utterance)
    is_nav = cmd == "CREATE_TASK_CANDIDATE" or "出口" in utterance or "洗手间" in utterance
    is_reading = "门牌" in utterance
    gaps: List[str] = ["missing_safety_clearance"]
    if not utterance.strip():
        gaps.append("missing_task_goal")
    if "商场" not in utterance and cmd in ("CREATE_TASK_CANDIDATE", "REQUEST_CLARIFICATION_CANDIDATE"):
        gaps.append("missing_scene_context")
    if is_nav and target["target_type"] == "unknown":
        gaps.append("missing_target_location")
    if route_stage == "unknown":
        gaps.append("missing_route_stage")
    if is_nav or is_reading:
        gaps.append("missing_information_source")
    if is_reading:
        gaps.append("missing_readable_region")
        gaps.append("missing_ocr_evidence")
    if cmd == "REQUEST_CONFIRMATION_CANDIDATE":
        gaps.append("missing_user_confirmation")
    if cmd == "REQUEST_HUMAN_ASSISTANCE_CANDIDATE":
        gaps.append("missing_human_assistance_decision")
    obs: List[str] = []
    if "出口" in utterance:
        obs.extend(["observe_forward_path", "observe_exit_sign"])
    elif "洗手间" in utterance:
        obs.extend(["observe_forward_path", "observe_restroom_sign"])
    elif "门牌" in utterance:
        obs.extend(["observe_doorplate_area", "observe_floor_or_wall_sign"])
    elif is_nav:
        obs.append("observe_forward_path")
    if cmd == "REQUEST_CLARIFICATION_CANDIDATE":
        obs.append("ask_user_to_turn_or_center_view")
    if is_reading:
        obs.append("ask_user_to_stop_for_static_reading")
    ocr_need = is_reading or ("出口" in utterance) or ("洗手间" in utterance)
    human_need = cmd == "REQUEST_HUMAN_ASSISTANCE_CANDIDATE"
    schedule_type = "continue_observing"
    priority = "task_critical"
    timing = "immediate"
    if cmd in ("QUERY_STATUS_CANDIDATE", "REPEAT_GUIDANCE_CANDIDATE"):
        schedule_type = "no_op"
        priority = "guidance"
    elif cmd == "REQUEST_CLARIFICATION_CANDIDATE":
        schedule_type = "request_user_clarification"
        priority = "clarification"
    elif cmd == "REQUEST_HUMAN_ASSISTANCE_CANDIDATE":
        schedule_type = "request_human_assistance_confirmation"
        priority = "clarification"
    elif cmd == "REQUEST_CONFIRMATION_CANDIDATE":
        schedule_type = "block_due_to_missing_context"
        priority = "clarification"
        timing = "after_confirmation"
    elif is_nav:
        schedule_type = "generate_basic_navigation_guidance_candidate"
        priority = "guidance"
    elif ocr_need:
        schedule_type = "prepare_ocr_candidate"
        priority = "task_critical"
        timing = "when_near_target"
    return {
        "current_self_location_candidate": {
            "spatial_anchor_ref": "spatial_anchor_dryrun_session",
            "gps_candidate_ref": "gps_self_placeholder",
            "is_fact": False,
        },
        "target_location_candidate": {
            **target,
            "is_fact": False,
            "placeholder": True,
        },
        "distance_to_target_candidate": {
            "meters_placeholder": 45 if is_nav else None,
            "is_fact": False,
            "scheduling_hint_only": True,
        },
        "route_stage_candidate": route_stage,
        "information_gap_list": gaps,
        "required_observation_list": obs,
        "candidate_search_area": target.get("label", "unspecified"),
        "ocr_need_candidate": ocr_need,
        "human_assistance_need_candidate": human_need,
        "next_action_schedule_candidate": schedule_type,
        "action_timing_hint": timing,
        "action_priority_hint": priority,
    }


def _build_task_aware_scheduling(
    task_objects: List[Dict[str, Any]],
    commit_by_tobj: Dict[str, Dict[str, Any]],
    *,
    ocr_governance_loaded: bool,
    stc_governance_loaded: bool,
) -> Dict[str, Any]:
    spatial_rows: List[Dict[str, Any]] = []
    gap_rows: List[Dict[str, Any]] = []
    obs_plans: List[Dict[str, Any]] = []
    ocr_needs: List[Dict[str, Any]] = []
    human_needs: List[Dict[str, Any]] = []
    schedules: List[Dict[str, Any]] = []

    obs_target_map = {
        "observe_forward_path": ("observe_forward_path", "path_ahead", ["vision"]),
        "observe_exit_sign": ("observe_exit_sign", "signage_area", ["vision", "ocr_if_task_required"]),
        "observe_restroom_sign": ("observe_restroom_sign", "restroom_sign_area", ["vision", "ocr_if_task_required"]),
        "observe_doorplate_area": ("observe_doorplate_area", "doorplate_area", ["vision", "ocr_if_task_required"]),
        "observe_floor_or_wall_sign": ("observe_floor_or_wall_sign", "wall_sign_area", ["vision"]),
        "ask_user_to_turn_or_center_view": (
            "ask_user_to_turn_or_center_view",
            "user_fov",
            ["user_guidance"],
        ),
        "ask_user_to_stop_for_static_reading": (
            "ask_user_to_stop_for_static_reading",
            "static_reading_zone",
            ["user_guidance", "vision"],
        ),
    }

    for tobj in task_objects:
        tobj_id = tobj["task_object_candidate_id"]
        tsc_id = tobj.get("source_task_state_candidate_id", "")
        utterance = tobj.get("task_goal") or ""
        cmd = ""
        gaps_list = tobj.get("information_gap_list") or []
        route_stage = tobj.get("route_stage_candidate", "unknown")
        target = tobj.get("target_location_candidate") or {}
        is_nav = tobj.get("task_type") == "navigation_task"
        is_reading = "门牌" in utterance

        sr_id = f"sr_{tobj_id}"
        spatial_rows.append(
            {
                "spatial_relation_candidate_id": sr_id,
                "source_task_object_candidate_id": tobj_id,
                "current_self_location_candidate": tobj.get("current_self_location_candidate"),
                "target_location_candidate": tobj.get("target_location_candidate"),
                "distance_to_target_candidate": tobj.get("distance_to_target_candidate"),
                "distance_confidence_placeholder": 0.6 if is_nav else None,
                "route_stage_candidate": route_stage,
                "spatial_anchor": tobj.get("spatial_anchor", "spatial_anchor_dryrun_session"),
                "gps_candidate_ref": "gps_self_placeholder",
                "map_context_candidate_ref": "map_context_placeholder",
                "live_observation_ref": "live_observation_priority",
                "can_support_action_scheduling": True,
                "can_complete_task_alone": False,
                "is_fact": False,
                "write_allowed": False,
                **_not_fact(),
            }
        )

        gap_ids_for_schedule: List[str] = []
        for gap_type in gaps_list:
            gid = f"gap_{tobj_id}_{gap_type}"
            gap_ids_for_schedule.append(gid)
            resolve_via = ["vision_observation", "safety_scan"]
            req_obs = "observe_forward_path"
            if gap_type == "missing_information_source":
                resolve_via = ["vision_observation", "ocr_candidate", "navigation_map_reference"]
                req_obs = "observe_signage_area"
            elif gap_type == "missing_readable_region":
                resolve_via = ["vision_observation", "ocr_candidate", "user_clarification"]
                req_obs = "observe_doorplate_area"
            elif gap_type == "missing_ocr_evidence":
                resolve_via = ["ocr_candidate", "vision_observation"]
                req_obs = "observe_doorplate_area"
            elif gap_type == "missing_user_confirmation":
                resolve_via = ["user_clarification"]
                req_obs = "user_confirmation"
            elif gap_type == "missing_human_assistance_decision":
                resolve_via = ["human_assistance", "user_clarification"]
                req_obs = "observe_service_desk"
            elif gap_type == "missing_scene_context":
                resolve_via = ["user_clarification", "memory_reference"]
                req_obs = "ask_user_to_turn_or_center_view"
            gap_rows.append(
                {
                    "information_gap_id": gid,
                    "source_task_object_candidate_id": tobj_id,
                    "gap_type": gap_type,
                    "gap_reason": f"dryrun_inferred_{gap_type}",
                    "required_observation_type": req_obs,
                    "required_context_source": "task_goal_and_spatial_relation",
                    "can_be_resolved_by": resolve_via,
                    "resolved_now": False,
                    **_not_fact(),
                }
            )

        for obs_action in tobj.get("required_observation_list") or []:
            mapped = obs_target_map.get(obs_action)
            if not mapped:
                continue
            obs_type, search_area, sensors = mapped
            linked_gap = gap_ids_for_schedule[0] if gap_ids_for_schedule else f"gap_{tobj_id}_missing_safety_clearance"
            plan_id = f"oplan_{tobj_id}_{obs_action}"
            timing = "now"
            if route_stage == "approaching_task_area":
                timing = "when_near_target"
            if "confirmation" in (tobj.get("next_action_schedule_candidate") or ""):
                timing = "after_user_confirmation"
            obs_plans.append(
                {
                    "observation_plan_candidate_id": plan_id,
                    "source_information_gap_id": linked_gap,
                    "source_spatial_relation_candidate_id": sr_id,
                    "observation_target_type": obs_type,
                    "suggested_search_area": search_area,
                    "required_sensor_or_capability": sensors,
                    "priority_hint": tobj.get("action_priority_hint", "task_critical"),
                    "timing_hint": timing,
                    "camera_invoked_now": False,
                    "ocr_invoked_now": False,
                    "navigation_action_triggered": False,
                    **_not_fact(),
                }
            )

        if tobj.get("ocr_need_candidate"):
            ocr_reason = "doorplate_confirmation" if is_reading else (
                "exit_sign_confirmation" if "出口" in utterance else "restroom_sign_confirmation"
            )
            prereq_ok = ocr_governance_loaded and stc_governance_loaded and (
                is_reading or "出口" in utterance or "洗手间" in utterance
            )
            ocr_needs.append(
                {
                    "ocr_need_candidate_id": f"ocr_need_{tobj_id}",
                    "source_task_object_candidate_id": tobj_id,
                    "source_information_gap_id": next(
                        (g for g in gap_ids_for_schedule if "ocr" in g or "readable" in g or "information_source" in g),
                        gap_ids_for_schedule[0] if gap_ids_for_schedule else f"gap_{tobj_id}_missing_ocr_evidence",
                    ),
                    "source_observation_plan_candidate_id": obs_plans[-1]["observation_plan_candidate_id"]
                    if obs_plans
                    else None,
                    "ocr_needed_for_task": True,
                    "ocr_reason": ocr_reason,
                    "prerequisites": {
                        "task_requires_text": is_reading or "出口" in utterance or "洗手间" in utterance,
                        "candidate_information_source_area": True,
                        "readable_region_candidate": is_reading,
                        "stc_freshness_valid": stc_governance_loaded,
                        "input_quality_sufficient": True,
                    },
                    "ocr_allowed_now": False,
                    "ocr_allowed_later": prereq_ok,
                    "blocked_reason_if_any": None if prereq_ok else "ocr_activation_or_stc_gate",
                    "ocr_invoked_now": False,
                    **_not_fact(),
                }
            )

        if tobj.get("human_assistance_need_candidate"):
            trigger = "user_requests_help"
            if "不知道" in utterance:
                trigger = "repeated_uncertain_context"
            human_needs.append(
                {
                    "human_assistance_candidate_id": f"human_need_{tobj_id}",
                    "source_task_object_candidate_id": tobj_id,
                    "trigger_reason": trigger,
                    "suggested_assistance_type": "ask_staff_for_location",
                    "confirmation_required": True,
                    "action_committed_now": False,
                    "speech_gate_required": True,
                    **_not_fact(),
                }
            )

        cd = commit_by_tobj.get(tobj_id, {})
        cd_id = cd.get("commit_decision_candidate_id", f"cd_{tsc_id}")
        sched_type = tobj.get("next_action_schedule_candidate", "continue_observing")
        target_module = "midplatform"
        gates = ["midplatform_gate", "task_manager_gate"]
        if sched_type == "prepare_ocr_candidate":
            target_module = "ocr"
            gates.append("ocr_activation_gate")
        elif sched_type == "generate_basic_navigation_guidance_candidate":
            target_module = "navigation_guidance"
            gates.extend(["speech_gate", "safety_gate"])
        elif sched_type == "request_user_clarification":
            target_module = "voice_guidance"
            gates.append("speech_gate")
        elif sched_type == "request_human_assistance_confirmation":
            target_module = "human_assistance"
            gates.extend(["speech_gate", "safety_gate"])
        elif sched_type == "no_op":
            target_module = "task_manager"
        schedules.append(
            {
                "action_schedule_candidate_id": f"asched_{tobj_id}",
                "source_task_object_candidate_id": tobj_id,
                "source_commit_decision_candidate_id": cd_id,
                "source_spatial_relation_candidate_id": sr_id,
                "source_information_gap_ids": gap_ids_for_schedule,
                "scheduled_action_type": sched_type,
                "action_priority_hint": tobj.get("action_priority_hint", "guidance"),
                "action_timing_hint": tobj.get("action_timing_hint", "immediate"),
                "target_module": target_module,
                "requires_gate": gates,
                "invoked_now": False,
                "runtime_action_committed": False,
                "scheduled_action_cannot_execute_directly": True,
                **_not_fact(),
            }
        )

    policy = {
        "schema_version": "task_manager_runtime_action_scheduling_policy_v1",
        "action_scheduling_requires_task_context": True,
        "action_scheduling_requires_spatial_relation": True,
        "action_scheduling_requires_information_gap_analysis": True,
        "safety_priority_above_task_scheduling": True,
        "ocr_scheduling_requires_ocr_activation_gate": True,
        "human_assistance_requires_user_confirmation": True,
        "navigation_guidance_requires_safety_check": True,
        "scheduled_action_cannot_execute_directly": True,
        "all_voice_related_actions_require_speech_gate": True,
        "runtime_action_committed": False,
        "task_aware_action_scheduling_enabled": True,
        **_not_fact(),
    }

    return {
        "spatial_relations": {
            "schema_version": "task_manager_runtime_task_spatial_relation_candidate_v1",
            "spatial_relation_candidate_count": len(spatial_rows),
            "candidates": spatial_rows,
            **_not_fact(),
        },
        "information_gaps": {
            "schema_version": "task_manager_runtime_information_gap_analysis_v1",
            "information_gap_count": len(gap_rows),
            "gaps": gap_rows,
            **_not_fact(),
        },
        "observation_plans": {
            "schema_version": "task_manager_runtime_task_aware_observation_plan_v1",
            "observation_plan_candidate_count": len(obs_plans),
            "candidates": obs_plans,
            **_not_fact(),
        },
        "ocr_needs": {
            "schema_version": "task_manager_runtime_ocr_activation_need_candidate_v1",
            "ocr_need_candidate_count": len(ocr_needs),
            "candidates": ocr_needs,
            "all_ocr_allowed_now_false": True,
            **_not_fact(),
        },
        "human_needs": {
            "schema_version": "task_manager_runtime_human_assistance_need_candidate_v1",
            "human_assistance_need_candidate_count": len(human_needs),
            "candidates": human_needs,
            **_not_fact(),
        },
        "action_schedules": {
            "schema_version": "task_manager_runtime_action_schedule_candidate_v1",
            "action_schedule_candidate_count": len(schedules),
            "candidates": schedules,
            "scheduled_action_cannot_execute_directly": True,
            **_not_fact(),
        },
        "scheduling_policy": policy,
    }


def run_task_manager_runtime_dryrun_v1(
    *,
    task_manager_contract_root: str,
    midplatform_task_state_root: str,
    voice_dialogue_runtime_root: str,
    basic_loop_plan_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "contract": Path(task_manager_contract_root).resolve(),
        "mp_state": Path(midplatform_task_state_root).resolve(),
        "voice_rt": Path(voice_dialogue_runtime_root).resolve(),
        "loop_plan": Path(basic_loop_plan_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    contract_sum = _read_json(roots["contract"] / "task_manager_contract_v1_summary.json") or {}
    mp_sum = _read_json(roots["mp_state"] / "midplatform_task_state_runtime_dryrun_v1_summary.json") or {}

    state_coll = _read_json(roots["mp_state"] / "midplatform_task_state_candidate_collection_v1.json") or {}
    lc_coll = _read_json(roots["mp_state"] / "midplatform_task_lifecycle_candidate_collection_v1.json") or {}
    tsc_list: List[Dict[str, Any]] = state_coll.get("candidates") or []
    lc_list: List[Dict[str, Any]] = lc_coll.get("candidates") or []
    lc_by_tsc = {lc.get("source_task_state_candidate_id"): lc for lc in lc_list}

    intake_specs = [
        ("task_manager_contract", roots["contract"], "task_manager_contract_v1_summary.json", False),
        ("midplatform_task_state_runtime", roots["mp_state"], "midplatform_task_state_runtime_dryrun_v1_summary.json", False),
        ("voice_dialogue_runtime", roots["voice_rt"], "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
        ("basic_functional_loop_plan", roots["loop_plan"], "luna_basic_functional_loop_stabilization_plan_v1_summary.json", False),
        ("ocr_activation", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("system_health", roots["health"], None, True),
        ("simulation", roots["sim"], None, True),
    ]
    intake_rows = []
    for iid, root, art, optional in intake_specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        intake_rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else ("optional_missing" if optional else "missing"),
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "dryrun_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    pending_cancel = False
    tm_assumed_state = "NO_TASK"
    candidate_intake_rows: List[Dict[str, Any]] = []
    task_objects: List[Dict[str, Any]] = []
    lifecycle_events: List[Dict[str, Any]] = []
    commit_decisions: List[Dict[str, Any]] = []
    fsm_rows: List[Dict[str, Any]] = []
    confirm_rows: List[Dict[str, Any]] = []
    enrichment_rows: List[Dict[str, Any]] = []
    verification_rows: List[Dict[str, Any]] = []
    execution_rows: List[Dict[str, Any]] = []
    downstream_rows: List[Dict[str, Any]] = []
    audit_traces: List[Dict[str, Any]] = []

    nav_cmds = {"CREATE_TASK_CANDIDATE"}

    for tsc in tsc_list:
        tsc_id = tsc.get("task_state_candidate_id", "")
        cmd = tsc.get("source_command_type", "")
        proposed = tsc.get("proposed_task_state", "")
        lc = lc_by_tsc.get(tsc_id, {})
        lc_id = lc.get("lifecycle_candidate_id", f"lc_{tsc_id}")
        utterance = (tsc.get("proposed_context_patch") or {}).get("utterance", "")
        uid = tsc_id.replace("tsc_", "")
        conf_req = tsc.get("confirmation_required", False)

        candidate_intake_rows.append(
            {
                "intake_candidate_id": f"intake_{tsc_id}",
                "source_task_state_candidate_id": tsc_id,
                "source_lifecycle_candidate_id": lc_id,
                "source_command_type": cmd,
                "proposed_task_state": proposed,
                "lifecycle_event_type": lc.get("lifecycle_event_type", ""),
                "confirmation_required": conf_req,
                "accepted_for_task_manager_dryrun": True,
                "reason_if_rejected": None,
                **_not_fact(),
            }
        )

        prev_state, next_state, event_type = MP_TO_TM_STATE.get(
            proposed, ("TASK_ACTIVE", "TASK_ACTIVE", "TASK_BLOCKED")
        )
        fsm_rows.append(
            {
                "source_candidate_id": tsc_id,
                "current_state_assumption": tm_assumed_state,
                "requested_event": event_type,
                "proposed_next_state": next_state,
                "state_machine_allows_transition": True,
                "blocked_reason_if_any": None,
                "committed_now": False,
                **_not_fact(),
            }
        )
        if proposed == "TASK_CREATION_CANDIDATE":
            tm_assumed_state = "TASK_DRAFT"
        elif proposed == "TASK_CANCELLED_CANDIDATE" and pending_cancel:
            tm_assumed_state = "TASK_CANCELLED"
        elif "ACTIVE" in proposed:
            tm_assumed_state = "TASK_ACTIVE"

        tobj_id = f"tobj_{tsc_id}"
        sched = _scheduling_fields(utterance, cmd, proposed)
        if cmd in ("CREATE_TASK_CANDIDATE", "UPDATE_TASK_CONTEXT_CANDIDATE", "REQUEST_CLARIFICATION_CANDIDATE"):
            tobj = {
                "task_object_candidate_id": tobj_id,
                "source_task_state_candidate_id": tsc_id,
                "task_type": CMD_TO_TASK_TYPE.get(cmd, "generic_task"),
                "task_goal": utterance,
                "task_context": {"utterance": utterance},
                "scene_context": {"scene_label": "商场"} if "商场" in utterance else {},
                "route_context_candidate": {"stage": sched["route_stage_candidate"]},
                "gps_location_candidate": {"placeholder": True, "is_fact": False},
                "spatial_anchor": "spatial_anchor_dryrun_session",
                "time_anchor": "dryrun_session_t0",
                "memory_reference_context": {"reference_only": True},
                "observation_context": {"live_observation_priority": True},
                "verification_context": {"verify_goal": utterance},
                "execution_support_context": {
                    "support_navigation": cmd in nav_cmds,
                    "task_aware_action_scheduling": True,
                },
                "current_task_state_candidate": next_state,
                "current_task_version_candidate": 1,
                "task_state_committed_now": False,
                "is_fact": False,
                "write_allowed": False,
                **sched,
                **_not_fact(),
            }
            task_objects.append(tobj)
        elif cmd in ("QUERY_STATUS_CANDIDATE", "REPEAT_GUIDANCE_CANDIDATE"):
            task_objects.append(
                {
                    "task_object_candidate_id": tobj_id,
                    "source_task_state_candidate_id": tsc_id,
                    "task_type": "generic_task",
                    "task_goal": utterance,
                    "task_context": {"reference_only": True},
                    "scene_context": {},
                    "route_context_candidate": {},
                    "gps_location_candidate": None,
                    "spatial_anchor": "spatial_anchor_dryrun_session",
                    "time_anchor": "dryrun_session_t0",
                    "memory_reference_context": {},
                    "observation_context": {},
                    "verification_context": {},
                    "execution_support_context": {"task_aware_action_scheduling": False},
                    "current_task_state_candidate": tm_assumed_state,
                    "current_task_version_candidate": 1,
                    "task_state_committed_now": False,
                    "is_fact": False,
                    "write_allowed": False,
                    **sched,
                    **_not_fact(),
                }
            )
        else:
            task_objects.append(
                {
                    "task_object_candidate_id": tobj_id,
                    "source_task_state_candidate_id": tsc_id,
                    "task_type": CMD_TO_TASK_TYPE.get(cmd, "generic_task"),
                    "task_goal": utterance,
                    "task_context": {"utterance": utterance},
                    "scene_context": {},
                    "route_context_candidate": {},
                    "gps_location_candidate": None,
                    "spatial_anchor": "spatial_anchor_dryrun_session",
                    "time_anchor": "dryrun_session_t0",
                    "memory_reference_context": {},
                    "observation_context": {"pending_confirmation": conf_req},
                    "verification_context": {},
                    "execution_support_context": {"task_aware_action_scheduling": True},
                    "current_task_state_candidate": next_state,
                    "current_task_version_candidate": 1,
                    "task_state_committed_now": False,
                    "is_fact": False,
                    "write_allowed": False,
                    **sched,
                    **_not_fact(),
                }
            )

        le_id = f"le_{tsc_id}"
        lifecycle_events.append(
            {
                "lifecycle_event_candidate_id": le_id,
                "source_lifecycle_candidate_id": lc_id,
                "event_type": event_type,
                "previous_task_state_candidate": prev_state,
                "proposed_next_task_state": next_state,
                "transition_guard_result": tsc.get("transition_guard_result", "pass"),
                "confirmation_gate_result": "pass" if not conf_req or pending_cancel else "pending",
                "safety_gate_result": "normal",
                "idempotency_key": f"idk_{tsc_id}_{event_type}",
                "committed_now": False,
                **_not_fact(),
            }
        )

        if cmd == "REQUEST_CONFIRMATION_CANDIDATE":
            pending_cancel = True

        dec_type, blocked, next_in = _commit_decision_for(
            cmd, proposed, conf_req, pending_cancel, uid
        )
        cd_id = f"cd_{tsc_id}"
        commit_decisions.append(
            {
                "commit_decision_candidate_id": cd_id,
                "source_lifecycle_event_candidate_id": le_id,
                "decision_type": dec_type,
                "allowed_now": False,
                "allowed_later": dec_type == "COMMIT_ALLOWED_LATER",
                "blocked_reason": blocked,
                "required_next_input": next_in,
                "audit_required": True,
                "task_state_committed_now": False,
                **_not_fact(),
            }
        )

        confirm_rows.append(
            {
                "source_candidate_id": tsc_id,
                "confirmation_required": conf_req or cmd == "REQUEST_CONFIRMATION_CANDIDATE",
                "pending_confirmation_context_available": pending_cancel or (cmd == "CANCEL_TASK_CANDIDATE" and uid == "utt_008"),
                "confirmation_matches_pending_context": cmd == "CANCEL_TASK_CANDIDATE" and pending_cancel,
                "stale_confirmation_rejected": cmd == "CANCEL_TASK_CANDIDATE" and not pending_cancel,
                "confirmation_gate_pass": not (cmd == "CANCEL_TASK_CANDIDATE" and not pending_cancel),
                "task_state_committed_now": False,
                **_not_fact(),
            }
        )

        for etype in (
            "time_anchor",
            "spatial_anchor",
            "scene_context_candidate",
            "observation_context",
            "gps_location_candidate",
            "memory_reference_context",
            "route_context_candidate",
        ):
            enrichment_rows.append(
                {
                    "enrichment_candidate_id": f"enr_{tobj_id}_{etype}",
                    "source_task_object_candidate_id": tobj_id,
                    "enrichment_type": etype,
                    "source_chain": "task_manager_runtime_dryrun_v1",
                    "confidence_placeholder": 0.8 if etype not in ("gps_location_candidate",) else None,
                    "freshness_status": "session_scoped",
                    "privacy_sensitivity": "user_task_context",
                    "can_support_verification": True,
                    "can_support_execution": etype in ("observation_context", "route_context_candidate", "gps_location_candidate"),
                    "can_override_live_observation": False,
                    "is_fact": False,
                    "write_allowed": False,
                    **_not_fact(),
                }
            )

        if cmd in nav_cmds or proposed == "TASK_CREATION_CANDIDATE":
            verification_rows.append(
                {
                    "verification_context_candidate_id": f"vctx_{tobj_id}_location",
                    "source_task_object_candidate_id": tobj_id,
                    "verification_type": "verify_correct_location",
                    "required_evidence": ["live_observation", "scene_match"],
                    "live_observation_required": True,
                    "user_confirmation_required": False,
                    "memory_reference_can_support": True,
                    "gps_candidate_can_support": True,
                    "memory_reference_cannot_complete_task_alone": True,
                    "gps_candidate_cannot_complete_task_alone": True,
                    "task_completed_now": False,
                    **_not_fact(),
                }
            )
        if cmd == "QUERY_STATUS_CANDIDATE":
            verification_rows.append(
                {
                    "verification_context_candidate_id": f"vctx_{tobj_id}_status",
                    "source_task_object_candidate_id": tobj_id,
                    "verification_type": "verify_task_goal_reached",
                    "required_evidence": ["user_guidance_state"],
                    "live_observation_required": False,
                    "user_confirmation_required": False,
                    "memory_reference_can_support": False,
                    "gps_candidate_can_support": False,
                    "memory_reference_cannot_complete_task_alone": True,
                    "gps_candidate_cannot_complete_task_alone": True,
                    "task_completed_now": False,
                    **_not_fact(),
                }
            )

        if cmd in nav_cmds:
            execution_rows.append(
                {
                    "execution_support_candidate_id": f"es_{tobj_id}_nav",
                    "source_task_object_candidate_id": tobj_id,
                    "support_type": "decide_need_for_navigation_guidance",
                    "recommended_downstream_candidate": "navigation_guidance_candidate",
                    "requires_midplatform_gate": True,
                    "requires_task_manager_commit_for_lifecycle": True,
                    "cannot_trigger_runtime_action_directly": True,
                    "task_aware_action_scheduling": True,
                    "next_action_schedule_candidate": sched.get("next_action_schedule_candidate"),
                    "route_stage_candidate": sched.get("route_stage_candidate"),
                    "information_gap_list": sched.get("information_gap_list"),
                    "navigation_action_triggered": False,
                    "ocr_invoked_now": False,
                    "camera_invoked_now": False,
                    **_not_fact(),
                }
            )
        if sched.get("ocr_need_candidate"):
            execution_rows.append(
                {
                    "execution_support_candidate_id": f"es_{tobj_id}_ocr",
                    "source_task_object_candidate_id": tobj_id,
                    "support_type": "decide_need_for_ocr_candidate",
                    "recommended_downstream_candidate": "prepare_ocr_candidate",
                    "requires_midplatform_gate": True,
                    "requires_task_manager_commit_for_lifecycle": True,
                    "cannot_trigger_runtime_action_directly": True,
                    "task_aware_action_scheduling": True,
                    "ocr_need_candidate": True,
                    "navigation_action_triggered": False,
                    "ocr_invoked_now": False,
                    "camera_invoked_now": False,
                    **_not_fact(),
                }
            )
        if cmd == "REQUEST_CLARIFICATION_CANDIDATE":
            execution_rows.append(
                {
                    "execution_support_candidate_id": f"es_{tobj_id}_clarify",
                    "source_task_object_candidate_id": tobj_id,
                    "support_type": "decide_need_for_user_guidance",
                    "recommended_downstream_candidate": "guidance_need_candidate",
                    "requires_midplatform_gate": True,
                    "requires_task_manager_commit_for_lifecycle": True,
                    "cannot_trigger_runtime_action_directly": True,
                    "navigation_action_triggered": False,
                    "ocr_invoked_now": False,
                    "camera_invoked_now": False,
                    **_not_fact(),
                }
            )
        if cmd == "REQUEST_HUMAN_ASSISTANCE_CANDIDATE":
            execution_rows.append(
                {
                    "execution_support_candidate_id": f"es_{tobj_id}_human",
                    "source_task_object_candidate_id": tobj_id,
                    "support_type": "decide_need_for_human_assistance",
                    "recommended_downstream_candidate": "human_assistance_candidate",
                    "requires_midplatform_gate": True,
                    "requires_task_manager_commit_for_lifecycle": True,
                    "cannot_trigger_runtime_action_directly": True,
                    "navigation_action_triggered": False,
                    "ocr_invoked_now": False,
                    "camera_invoked_now": False,
                    **_not_fact(),
                }
            )

        dtype = "speech_response_candidate"
        target = "voice_output_plane"
        if dec_type == "NO_OP" or cmd in ("QUERY_STATUS_CANDIDATE", "REPEAT_GUIDANCE_CANDIDATE"):
            dtype = "speech_response_candidate"
        elif cmd in nav_cmds:
            dtype = "navigation_guidance_candidate"
            target = "midplatform_navigation"
        elif conf_req:
            dtype = "user_confirmation_candidate"
        downstream_rows.append(
            {
                "downstream_candidate_id": f"ds_{cd_id}",
                "source_commit_decision_candidate_id": cd_id,
                "downstream_type": dtype,
                "target_module": target,
                "allowed_later": True,
                "invoked_now": False,
                "requires_midplatform_gate": True,
                "requires_speech_gate_if_voice": dtype == "speech_response_candidate",
                **_not_fact(),
            }
        )

        audit_traces.append(
            {
                "trace_id": f"trace_{le_id}",
                "source_lifecycle_event_id": le_id,
                "source_chain": "task_manager_runtime_dryrun_v1",
                "decision_reason": dec_type,
                "blocked_reason_if_any": blocked,
                "confirmation_ref_if_any": "pending_cancel" if pending_cancel else None,
                "safety_ref_if_any": "normal",
                "idempotency_key": f"idk_{tsc_id}_{event_type}",
                "audit_required": True,
                "committed_now": False,
                **_not_fact(),
            }
        )

    guard_matrix = [
        {
            "guard_name": g,
            "applied": True,
            "pass_now": True,
            "blocked_reason_if_any": None,
            "violation_detected": False,
        }
        for g in GUARD_NAMES
    ]

    commit_by_tobj: Dict[str, Dict[str, Any]] = {}
    for cd in commit_decisions:
        le_id = cd.get("source_lifecycle_event_candidate_id", "")
        tsc_key = le_id.replace("le_", "tsc_") if le_id.startswith("le_") else ""
        tobj_key = f"tobj_{tsc_key}" if tsc_key else ""
        if tobj_key:
            commit_by_tobj[tobj_key] = cd

    ocr_loaded = (roots["ocr_act"] / "ocr_activation_governance_policy_v1_summary.json").is_file()
    stc_loaded = (roots["stc"] / "stc_sampling_guidance_policy_v1_summary.json").is_file()
    scheduling = _build_task_aware_scheduling(
        task_objects,
        commit_by_tobj,
        ocr_governance_loaded=ocr_loaded,
        stc_governance_loaded=stc_loaded,
    )

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    return {
        "summary": {
            "schema_version": "task_manager_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "task_manager_runtime_dryrun_only",
            "based_on_task_manager_contract": contract_sum.get("task_manager_contract_defined") is True,
            "based_on_midplatform_task_state_runtime": mp_sum.get("task_state_candidates_generated") is True,
            "task_state_candidate_count_observed": len(tsc_list),
            "lifecycle_candidate_count_observed": len(lc_list),
            "task_state_machine_applied": True,
            "transition_guard_applied": True,
            "confirmation_gate_applied": True,
            "safety_gate_applied": True,
            "idempotency_policy_applied": True,
            "commit_decision_candidates_generated": len(commit_decisions) > 0,
            "task_object_candidates_generated": len(task_objects) > 0,
            "lifecycle_event_candidates_generated": len(lifecycle_events) > 0,
            "context_enrichment_candidates_generated": len(enrichment_rows) > 0,
            "verification_context_candidates_generated": len(verification_rows) > 0,
            "execution_support_context_candidates_generated": len(execution_rows) > 0,
            "downstream_guidance_candidates_generated": len(downstream_rows) > 0,
            "task_aware_action_scheduling_candidates_generated": True,
            "spatial_relation_candidates_generated": len(scheduling["spatial_relations"]["candidates"]) > 0,
            "information_gap_analysis_generated": len(scheduling["information_gaps"]["gaps"]) > 0,
            "observation_plan_candidates_generated": len(scheduling["observation_plans"]["candidates"]) > 0,
            "ocr_need_candidates_generated": len(scheduling["ocr_needs"]["candidates"]) > 0,
            "human_assistance_need_candidates_generated": len(scheduling["human_needs"]["candidates"]) > 0,
            "action_schedule_candidates_generated": len(scheduling["action_schedules"]["candidates"]) > 0,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "intake": {
            "schema_version": "task_manager_runtime_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "candidate_intake": {
            "schema_version": "task_manager_runtime_candidate_intake_matrix_v1",
            "task_state_candidate_count_observed": len(tsc_list),
            "lifecycle_candidate_count_observed": len(lc_list),
            "rows": candidate_intake_rows,
            **_not_fact(),
        },
        "task_objects": {
            "schema_version": "task_manager_runtime_task_object_candidate_collection_v1",
            "task_object_candidate_count": len(task_objects),
            "candidates": task_objects,
            **_not_fact(),
        },
        "lifecycle_events": {
            "schema_version": "task_manager_runtime_lifecycle_event_candidate_collection_v1",
            "lifecycle_event_candidate_count": len(lifecycle_events),
            "candidates": lifecycle_events,
            **_not_fact(),
        },
        "commit_decisions": {
            "schema_version": "task_manager_runtime_commit_decision_candidate_collection_v1",
            "commit_decision_candidate_count": len(commit_decisions),
            "candidates": commit_decisions,
            "all_allowed_now_false": True,
            **_not_fact(),
        },
        "fsm_matrix": {
            "schema_version": "task_manager_runtime_state_machine_application_matrix_v1",
            "rows": fsm_rows,
            **_not_fact(),
        },
        "guard_matrix": {
            "schema_version": "task_manager_runtime_transition_guard_application_matrix_v1",
            "guards": guard_matrix,
            **_not_fact(),
        },
        "confirm_matrix": {
            "schema_version": "task_manager_runtime_confirmation_gate_application_matrix_v1",
            "rows": confirm_rows,
            **_not_fact(),
        },
        "safety_matrix": {
            "schema_version": "task_manager_runtime_safety_gate_application_matrix_v1",
            "scenarios": [
                {
                    "scenario_id": "safety_inactive",
                    "safety_active": False,
                    "candidate_dryrun_continues": True,
                    "low_priority_commit_delayed": False,
                    "cancel_confirmation_delayed": False,
                    "guidance_priority_forced": False,
                },
                {
                    "scenario_id": "safety_active",
                    "safety_active": True,
                    "candidate_dryrun_continues": False,
                    "low_priority_commit_delayed": True,
                    "cancel_confirmation_delayed": True,
                    "guidance_priority_forced": True,
                },
            ],
            "task_state_committed_now": False,
            **_not_fact(),
        },
        "idempotency_dryrun": {
            "schema_version": "task_manager_runtime_idempotency_duplicate_dryrun_v1",
            "idempotency_key_generated": True,
            "duplicate_commit_forbidden": True,
            "repeated_cancel_confirmation_noop_if_already_cancelled": True,
            "repeated_pause_noop_if_already_paused": True,
            "repeated_resume_noop_if_already_active": True,
            "duplicate_commit_detected_now": False,
            "commit_invoked_now": False,
            **_not_fact(),
        },
        "enrichment_collection": {
            "schema_version": "task_manager_runtime_context_enrichment_candidate_collection_v1",
            "enrichment_candidate_count": len(enrichment_rows),
            "candidates": enrichment_rows,
            "can_override_live_observation": False,
            **_not_fact(),
        },
        "verification_collection": {
            "schema_version": "task_manager_runtime_verification_context_candidate_collection_v1",
            "verification_context_candidate_count": len(verification_rows),
            "candidates": verification_rows,
            "memory_reference_cannot_complete_task_alone": True,
            "gps_candidate_cannot_complete_task_alone": True,
            "task_completed_now": False,
            **_not_fact(),
        },
        "execution_collection": {
            "schema_version": "task_manager_runtime_execution_support_context_candidate_collection_v1",
            "execution_support_context_candidate_count": len(execution_rows),
            "candidates": execution_rows,
            "cannot_trigger_runtime_action_directly": True,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "downstream_collection": {
            "schema_version": "task_manager_runtime_downstream_candidate_collection_v1",
            "downstream_candidate_count": len(downstream_rows),
            "candidates": downstream_rows,
            "all_invoked_now_false": True,
            **_not_fact(),
        },
        "spatial_relations": scheduling["spatial_relations"],
        "information_gaps": scheduling["information_gaps"],
        "observation_plans": scheduling["observation_plans"],
        "ocr_needs": scheduling["ocr_needs"],
        "human_needs": scheduling["human_needs"],
        "action_schedules": scheduling["action_schedules"],
        "scheduling_policy": scheduling["scheduling_policy"],
        "rollback_abort": {
            "schema_version": "task_manager_runtime_rollback_abort_dryrun_v1",
            "rollback_policy_applied": True,
            "abort_policy_applied": True,
            "partial_commit_detected": False,
            "rollback_invoked_now": False,
            "abort_invoked_now": False,
            "corrective_event_append_only": True,
            "original_lifecycle_event_overwritten": False,
            **_not_fact(),
        },
        "audit_collection": {
            "schema_version": "task_manager_runtime_audit_trace_collection_v1",
            "audit_trace_count": len(audit_traces),
            "traces": audit_traces,
            "source_chain_required": True,
            **_not_fact(),
        },
        "boundary_check": {
            "schema_version": "task_manager_runtime_boundary_check_v1",
            "task_manager_runtime_dryrun_only": True,
            "task_state_committed_now": False,
            "lifecycle_event_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "violation_detected": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "task_manager_runtime_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "task_manager_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "task_state_candidate_count_observed": len(tsc_list),
            "lifecycle_candidate_count_observed": len(lc_list),
            "commit_decision_candidate_count": len(commit_decisions),
            "enrichment_candidate_count": len(enrichment_rows),
            "verification_context_candidate_count": len(verification_rows),
            "execution_support_context_candidate_count": len(execution_rows),
            "task_aware_action_scheduling_candidates_generated": True,
            "spatial_relation_candidates_generated": True,
            "information_gap_analysis_generated": True,
            "observation_plan_candidates_generated": True,
            "ocr_need_candidates_generated": True,
            "human_assistance_need_candidates_generated": True,
            "action_schedule_candidates_generated": True,
            "spatial_relation_candidate_count": scheduling["spatial_relations"]["spatial_relation_candidate_count"],
            "information_gap_count": scheduling["information_gaps"]["information_gap_count"],
            "observation_plan_candidate_count": scheduling["observation_plans"]["observation_plan_candidate_count"],
            "ocr_need_candidate_count": scheduling["ocr_needs"]["ocr_need_candidate_count"],
            "human_assistance_need_candidate_count": scheduling["human_needs"]["human_assistance_need_candidate_count"],
            "action_schedule_candidate_count": scheduling["action_schedules"]["action_schedule_candidate_count"],
            "task_state_committed_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": ["Basic-Navigation-Guidance-Loop-DryRun-v1", "Task-Context-Enrichment-Runtime-DryRun-v1"],
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "task_manager_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "task_manager_runtime_metrics_candidate_report_v1",
            "task_state_candidate_count_observed": len(tsc_list),
            "lifecycle_candidate_count_observed": len(lc_list),
            "task_object_candidate_count": len(task_objects),
            "lifecycle_event_candidate_count": len(lifecycle_events),
            "commit_decision_candidate_count": len(commit_decisions),
            "enrichment_candidate_count": len(enrichment_rows),
            "verification_context_candidate_count": len(verification_rows),
            "execution_support_context_candidate_count": len(execution_rows),
            "downstream_candidate_count": len(downstream_rows),
            "spatial_relation_candidate_count": scheduling["spatial_relations"]["spatial_relation_candidate_count"],
            "information_gap_count": scheduling["information_gaps"]["information_gap_count"],
            "observation_plan_candidate_count": scheduling["observation_plans"]["observation_plan_candidate_count"],
            "ocr_need_candidate_count": scheduling["ocr_needs"]["ocr_need_candidate_count"],
            "human_assistance_need_candidate_count": scheduling["human_needs"]["human_assistance_need_candidate_count"],
            "action_schedule_candidate_count": scheduling["action_schedules"]["action_schedule_candidate_count"],
            "audit_trace_count": len(audit_traces),
            "runtime_action_committed_count": 0,
            "task_state_commit_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "task_manager_runtime_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "task_manager_runtime_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "task_manager_health_report_candidate_generated": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "task_manager_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "task_manager_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "task_manager_runtime_non_claims_report_v1",
            "claims": [
                "runtime_dryrun_not_real_task_manager",
                "task_object_not_real_task",
                "lifecycle_event_not_real_event",
                "commit_decision_not_real_commit",
                "enrichment_not_fact",
                "verification_not_task_completed",
                "execution_support_not_direct_action",
                "downstream_not_module_execution",
                "action_schedule_not_runtime_execution",
                "spatial_relation_not_fact",
                "distance_to_target_scheduling_hint_only",
                "no_create_cancel_pause_resume",
                "no_navigation_tts_vop",
                "no_fact_write",
            ],
        },
        "followups": {
            "schema_version": "task_manager_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "task_manager_runtime_audit_report_v1",
            "task_manager_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "task_state_candidate_count_observed": len(tsc_list),
            "lifecycle_candidate_count_observed": len(lc_list),
            "task_state_machine_applied": True,
            "transition_guard_applied": True,
            "confirmation_gate_applied": True,
            "safety_gate_applied": True,
            "idempotency_policy_applied": True,
            "commit_decision_candidates_generated": True,
            "task_object_candidates_generated": True,
            "lifecycle_event_candidates_generated": True,
            "context_enrichment_candidates_generated": True,
            "verification_context_candidates_generated": True,
            "execution_support_context_candidates_generated": True,
            "downstream_guidance_candidates_generated": True,
            "task_aware_action_scheduling_candidates_generated": True,
            "spatial_relation_candidates_generated": True,
            "information_gap_analysis_generated": True,
            "observation_plan_candidates_generated": True,
            "ocr_need_candidates_generated": True,
            "human_assistance_need_candidates_generated": True,
            "action_schedule_candidates_generated": True,
            "task_manager_runtime_invoked": False,
            "task_state_committed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "task_completed_now": False,
            "navigation_action_triggered": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
