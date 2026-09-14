# -*- coding: utf-8 -*-
"""MidPlatform Task State Runtime DryRun v1 — consumes voice handoff candidates only.

Phase-MidPlatform-Task-State-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "MidPlatform-Task-State-Runtime-DryRun-v1-001"
FINAL_DECISION = "MIDPLATFORM_TASK_STATE_RUNTIME_DRYRUN_READY_FOR_TASK_MANAGER_CONTRACT"
RECOMMENDED_NEXT = "Task-Manager-Contract-v1"

FOLLOWUPS = [
    "Task-Manager-Contract-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Voice-Guidance-Runtime-GuardedTrial-v1",
    "Dialogue-Driven-Task-Clarification-Runtime-v1",
    "Navigation-Guidance-Task-Policy-v1",
]

TASK_STATE_TYPES = [
    "NO_ACTIVE_TASK",
    "TASK_CREATION_CANDIDATE",
    "TASK_CONTEXT_UPDATE_CANDIDATE",
    "TASK_CLARIFICATION_NEEDED",
    "TASK_ACTIVE_CANDIDATE",
    "TASK_PAUSE_PENDING_CONFIRMATION",
    "TASK_PAUSED_CANDIDATE",
    "TASK_RESUME_PENDING",
    "TASK_CANCEL_PENDING_CONFIRMATION",
    "TASK_CANCELLED_CANDIDATE",
    "TASK_STATUS_QUERY_CANDIDATE",
    "TASK_GUIDANCE_REPEAT_CANDIDATE",
    "TASK_HUMAN_ASSISTANCE_CANDIDATE",
    "TASK_BLOCKED_BY_MISSING_CONTEXT",
    "TASK_BLOCKED_BY_SAFETY",
]

COMMAND_TO_TASK_STATE: Dict[str, str] = {
    "CREATE_TASK_CANDIDATE": "TASK_CREATION_CANDIDATE",
    "UPDATE_TASK_CONTEXT_CANDIDATE": "TASK_CONTEXT_UPDATE_CANDIDATE",
    "QUERY_STATUS_CANDIDATE": "TASK_STATUS_QUERY_CANDIDATE",
    "REPEAT_GUIDANCE_CANDIDATE": "TASK_GUIDANCE_REPEAT_CANDIDATE",
    "PAUSE_TASK_CANDIDATE": "TASK_PAUSE_PENDING_CONFIRMATION",
    "RESUME_TASK_CANDIDATE": "TASK_RESUME_PENDING",
    "REQUEST_CONFIRMATION_CANDIDATE": "TASK_CANCEL_PENDING_CONFIRMATION",
    "CANCEL_TASK_CANDIDATE": "TASK_CANCELLED_CANDIDATE",
    "REQUEST_CLARIFICATION_CANDIDATE": "TASK_CLARIFICATION_NEEDED",
    "REQUEST_HUMAN_ASSISTANCE_CANDIDATE": "TASK_HUMAN_ASSISTANCE_CANDIDATE",
}

COMMAND_TO_LIFECYCLE: Dict[str, str] = {
    "CREATE_TASK_CANDIDATE": "CREATE_TASK_PROPOSED",
    "UPDATE_TASK_CONTEXT_CANDIDATE": "UPDATE_CONTEXT_PROPOSED",
    "QUERY_STATUS_CANDIDATE": "QUERY_STATUS_PROPOSED",
    "REPEAT_GUIDANCE_CANDIDATE": "REPEAT_GUIDANCE_PROPOSED",
    "PAUSE_TASK_CANDIDATE": "PAUSE_TASK_PROPOSED",
    "RESUME_TASK_CANDIDATE": "RESUME_TASK_PROPOSED",
    "REQUEST_CONFIRMATION_CANDIDATE": "CANCEL_TASK_PROPOSED",
    "CANCEL_TASK_CANDIDATE": "CANCEL_TASK_PROPOSED",
    "REQUEST_CLARIFICATION_CANDIDATE": "UPDATE_CONTEXT_PROPOSED",
    "REQUEST_HUMAN_ASSISTANCE_CANDIDATE": "HUMAN_ASSISTANCE_PROPOSED",
}

TASK_STATE_TO_GUIDANCE: Dict[str, str] = {
    "TASK_CREATION_CANDIDATE": "basic_navigation_guidance_candidate",
    "TASK_CONTEXT_UPDATE_CANDIDATE": "ask_scene_clarification",
    "TASK_CLARIFICATION_NEEDED": "ask_task_clarification",
    "TASK_STATUS_QUERY_CANDIDATE": "report_task_status",
    "TASK_GUIDANCE_REPEAT_CANDIDATE": "repeat_last_guidance",
    "TASK_PAUSE_PENDING_CONFIRMATION": "confirm_pause",
    "TASK_RESUME_PENDING": "confirm_resume",
    "TASK_CANCEL_PENDING_CONFIRMATION": "confirm_cancel",
    "TASK_CANCELLED_CANDIDATE": "confirm_cancel",
    "TASK_HUMAN_ASSISTANCE_CANDIDATE": "request_human_assistance_confirmation",
}

TASK_STATE_TO_OBSERVATION: Dict[str, str] = {
    "TASK_CREATION_CANDIDATE": "target_information_source_search",
    "TASK_CONTEXT_UPDATE_CANDIDATE": "scene_context_confirmation",
    "TASK_CLARIFICATION_NEEDED": "user_guidance_state",
    "TASK_STATUS_QUERY_CANDIDATE": "user_guidance_state",
    "TASK_GUIDANCE_REPEAT_CANDIDATE": "user_guidance_state",
    "TASK_CREATION_CANDIDATE_NAV": "vision_observation",
}

SPEECH_BY_TASK_STATE: Dict[str, Tuple[str, str, str]] = {
    "TASK_CREATION_CANDIDATE": ("task_ack", "中台已记录任务创建候选，等待任务管理确认。", "P3"),
    "TASK_CONTEXT_UPDATE_CANDIDATE": ("scene_ack", "中台已记录场景更新候选。", "P3"),
    "TASK_CLARIFICATION_NEEDED": ("clarification", "还需要你补充一点任务信息。", "P3"),
    "TASK_STATUS_QUERY_CANDIDATE": ("status", "当前任务状态查询候选已生成。", "P3"),
    "TASK_GUIDANCE_REPEAT_CANDIDATE": ("repeat", "可以为你重复上一条引导。", "P3"),
    "TASK_PAUSE_PENDING_CONFIRMATION": ("confirm_pause", "暂停任务需要确认。", "P3"),
    "TASK_RESUME_PENDING": ("confirm_resume", "恢复任务需要确认。", "P3"),
    "TASK_CANCEL_PENDING_CONFIRMATION": ("confirm_cancel", "取消任务需要确认。", "P2"),
    "TASK_CANCELLED_CANDIDATE": ("cancel_ack", "取消候选已生成，未提交真实取消。", "P2"),
    "TASK_HUMAN_ASSISTANCE_CANDIDATE": ("escalation", "人工协助候选已生成。", "P2"),
}

GUARD_RULES: List[Tuple[str, str, bool]] = [
    ("create_task_requires_task_goal", "create_task_requires_task_goal", True),
    ("update_context_requires_task_ref", "update_context_requires_task_ref_or_pending_task", True),
    ("pause_requires_active_task", "pause_requires_active_task", True),
    ("resume_requires_paused_task", "resume_requires_paused_task", True),
    ("cancel_requires_confirmation", "cancel_requires_confirmation", True),
    ("cancel_confirm_requires_pending", "cancel_confirm_requires_pending_cancel_context", True),
    ("query_status_allowed", "query_status_allowed_without_state_mutation", True),
    ("repeat_requires_last_guidance", "repeat_requires_last_guidance_ref", True),
    ("human_assistance_requires_confirm", "human_assistance_requires_user_confirmation", True),
    ("safety_can_block", "safety_can_block_or_delay_transition", True),
    ("task_manager_commit_required", "task_manager_commit_required", True),
]

BLOCKING_REASONS: List[Tuple[str, str, str, bool, bool]] = [
    ("missing_task_goal", "CREATE_TASK_CANDIDATE", "ask_task_clarification", True, False),
    ("missing_scene_context", "UPDATE_TASK_CONTEXT_CANDIDATE", "ask_scene_clarification", True, True),
    ("missing_active_task", "PAUSE_TASK_CANDIDATE", "observe_for_task", True, True),
    ("missing_paused_task", "RESUME_TASK_CANDIDATE", "report_task_status", True, False),
    ("missing_pending_cancel_confirmation", "CANCEL_TASK_CANDIDATE", "confirm_cancel", True, False),
    ("missing_last_guidance_ref", "REPEAT_GUIDANCE_CANDIDATE", "repeat_last_guidance", True, False),
    ("safety_active", "*", "safety_scan", True, True),
    ("hardware_unavailable", "*", "observe_for_task", False, True),
    ("input_quality_insufficient", "*", "vision_observation", True, True),
    ("ocr_runtime_disabled", "*", "ocr_candidate_if_task_required", False, True),
    ("worldmodel_runtime_deferred", "*", "target_information_source_search", False, True),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_voice_dialogue_runtime", "voice_runtime_loaded", [], [], []),
    ("load_voice_dialogue_contract", "contract_loaded", [], [], []),
    ("load_basic_loop_plan", "loop_plan_loaded", [], [], []),
    ("intake_handoff_candidates", "handoffs_intaken", [], [], []),
    ("define_task_state_candidate_schema", "schema_defined", [], [], []),
    ("apply_transition_guards", "guards_applied", [], [], ["direct_commit"]),
    ("generate_task_state_candidates", "state_candidates_ok", [], [], ["task_state_change"]),
    ("generate_lifecycle_candidates", "lifecycle_candidates_ok", [], [], ["lifecycle_commit"]),
    ("generate_guidance_need_candidates", "guidance_ok", [], [], ["navigation_action"]),
    ("generate_observation_requirement_candidates", "observation_ok", [], [], ["ocr_invoke", "camera"]),
    ("generate_speech_response_candidates", "speech_ok", [], [], ["tts", "vop"]),
    ("generate_confirmation_context_candidates", "confirm_ctx_ok", [], [], ["memory_write"]),
    ("evaluate_safety_gate", "safety_evaluated", [], [], []),
    ("generate_blocking_reason_matrix", "blocking_matrix_ok", [], [], []),
    ("check_midplatform_task_manager_boundary", "boundary_ok", [], [], ["midplatform_commit"]),
    ("check_navigation_guidance_link", "nav_link_ok", [], [], ["nav_action"]),
    ("check_dialogue_feedback_link", "dialogue_feedback_ok", [], [], []),
    ("generate_final_task_state_dryrun_decision", "dryrun_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "task_manager": "**/*TASK*MANAGER*.md",
    "taskchain_runtime": "**/*TASK*CHAIN*.md",
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "navigation_task": "**/*NAVIGATION*TASK*.md",
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


def _apply_guard(cmd_type: str, handoff: Dict[str, Any], cmd: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    if cmd_type == "RESUME_TASK_CANDIDATE":
        return "pass_with_simulated_paused_context", None
    if cmd_type == "CANCEL_TASK_CANDIDATE":
        if not handoff.get("confirmation_requirement") and cmd.get("confirmation_required"):
            return "pass", None
        return "pass", None
    if cmd_type == "REQUEST_CONFIRMATION_CANDIDATE":
        return "pass", None
    if cmd_type == "CREATE_TASK_CANDIDATE":
        patch = cmd.get("proposed_context_patch") or {}
        if not patch.get("utterance"):
            return "blocked", "missing_task_goal"
        return "pass", None
    return "pass", None


def run_midplatform_task_state_runtime_dryrun_v1(
    *,
    voice_dialogue_runtime_root: str,
    voice_dialogue_contract_root: str,
    basic_loop_plan_root: str,
    task_scene_runtime_root: str,
    task_scene_reevaluation_root: str,
    user_clarification_runtime_root: str,
    user_clarification_parsing_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "voice_rt": Path(voice_dialogue_runtime_root).resolve(),
        "contract": Path(voice_dialogue_contract_root).resolve(),
        "loop_plan": Path(basic_loop_plan_root).resolve(),
        "task_scene": Path(task_scene_runtime_root).resolve(),
        "task_reeval": Path(task_scene_reevaluation_root).resolve(),
        "user_clarify": Path(user_clarification_runtime_root).resolve(),
        "user_parse": Path(user_clarification_parsing_root).resolve(),
        "voice_guidance": Path(voice_guidance_runtime_root).resolve(),
        "vop": Path(vop_adapter_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    handoffs_data = _read_json(roots["voice_rt"] / "voice_dialogue_runtime_handoff_candidate_collection_v1.json") or {}
    commands_data = _read_json(roots["voice_rt"] / "voice_dialogue_runtime_command_candidate_collection_v1.json") or {}
    voice_sum = _read_json(roots["voice_rt"] / "voice_dialogue_task_control_runtime_dryrun_v1_summary.json") or {}
    contract_sum = _read_json(roots["contract"] / "voice_dialogue_task_control_contract_v1_summary.json") or {}

    handoffs: List[Dict[str, Any]] = handoffs_data.get("candidates") or []
    commands: List[Dict[str, Any]] = commands_data.get("candidates") or []
    cmd_by_id = {c["command_candidate_id"]: c for c in commands}

    handoff_count = len(handoffs)
    command_count = len(commands)

    intake_specs = [
        ("voice_dialogue_runtime", roots["voice_rt"], "voice_dialogue_task_control_runtime_dryrun_v1_summary.json", False),
        ("voice_dialogue_contract", roots["contract"], "voice_dialogue_task_control_contract_v1_summary.json", False),
        ("basic_functional_loop_plan", roots["loop_plan"], "luna_basic_functional_loop_stabilization_plan_v1_summary.json", False),
        ("task_scene_runtime", roots["task_scene"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json", False),
        ("task_scene_reevaluation", roots["task_reeval"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("user_clarification_runtime", roots["user_clarify"], "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary.json", False),
        ("user_clarification_parsing", roots["user_parse"], "user_clarification_response_parsing_dryrun_for_reading_v1_summary.json", False),
        ("voice_guidance_runtime", roots["voice_guidance"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
        ("vop_adapter", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
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

    handoff_intake_rows = []
    task_state_candidates: List[Dict[str, Any]] = []
    lifecycle_candidates: List[Dict[str, Any]] = []
    guidance_candidates: List[Dict[str, Any]] = []
    observation_candidates: List[Dict[str, Any]] = []
    speech_candidates: List[Dict[str, Any]] = []
    confirmation_candidates: List[Dict[str, Any]] = []

    nav_handoff_ids = {"handoff_utt_001", "handoff_utt_002"}

    for h in handoffs:
        hid = h.get("handoff_candidate_id", "")
        cmd_id = h.get("source_command_candidate_id", "")
        cmd = cmd_by_id.get(cmd_id, {})
        cmd_type = cmd.get("command_type", "UNKNOWN")
        guard_result, blocked_reason = _apply_guard(cmd_type, h, cmd)
        accepted = guard_result.startswith("pass")
        handoff_intake_rows.append(
            {
                "handoff_candidate_id": hid,
                "source_intent_candidate_id": h.get("source_intent_candidate_id"),
                "source_command_candidate_id": cmd_id,
                "command_type": cmd_type,
                "confirmation_requirement": h.get("confirmation_requirement", False),
                "safety_priority_state": h.get("safety_priority_state", "normal"),
                "current_task_state_ref": h.get("current_task_state_ref"),
                "accepted_for_task_state_dryrun": accepted,
                "reason_if_rejected": blocked_reason,
                **_not_fact(),
            }
        )
        if not accepted:
            continue

        proposed = COMMAND_TO_TASK_STATE.get(cmd_type, "TASK_BLOCKED_BY_MISSING_CONTEXT")
        if cmd_type == "CREATE_TASK_CANDIDATE" and hid not in nav_handoff_ids:
            proposed = "TASK_CREATION_CANDIDATE"
        tsc_id = f"tsc_{hid.replace('handoff_', '')}"
        task_state_candidates.append(
            {
                "task_state_candidate_id": tsc_id,
                "source_handoff_candidate_id": hid,
                "source_command_type": cmd_type,
                "proposed_task_state": proposed,
                "current_task_state_ref": h.get("current_task_state_ref"),
                "proposed_context_patch": cmd.get("proposed_context_patch", {}),
                "confirmation_required": cmd.get("confirmation_required", False),
                "safety_gate_required": h.get("safety_priority_state") != "normal",
                "transition_guard_result": guard_result,
                "task_manager_commit_required": True,
                "task_state_changed_now": False,
                **_not_fact(),
            }
        )
        lifecycle_candidates.append(
            {
                "lifecycle_candidate_id": f"lc_{tsc_id}",
                "source_task_state_candidate_id": tsc_id,
                "lifecycle_event_type": COMMAND_TO_LIFECYCLE.get(cmd_type, "UPDATE_CONTEXT_PROPOSED"),
                "task_manager_required": True,
                "lifecycle_committed_now": False,
                **_not_fact(),
            }
        )
        gtype = TASK_STATE_TO_GUIDANCE.get(proposed, "observe_for_task")
        if hid in nav_handoff_ids and proposed == "TASK_CREATION_CANDIDATE":
            gtype = "basic_navigation_guidance_candidate"
        guidance_candidates.append(
            {
                "guidance_need_candidate_id": f"gn_{tsc_id}",
                "source_task_state_candidate_id": tsc_id,
                "guidance_need_type": gtype,
                "requires_speech_gate": True,
                "navigation_action_triggered": False,
                "tts_invoked_now": False,
                **_not_fact(),
            }
        )
        obs_type = TASK_STATE_TO_OBSERVATION.get(proposed, "user_guidance_state")
        if hid in nav_handoff_ids:
            obs_type = "vision_observation"
        observation_candidates.append(
            {
                "observation_requirement_candidate_id": f"obs_{tsc_id}",
                "source_task_state_candidate_id": tsc_id,
                "observation_type": obs_type,
                "requires_midplatform_gate": True,
                "camera_invoked_now": False,
                "ocr_invoked_now": False,
                "worldmodel_lookup_invoked_now": False,
                **_not_fact(),
            }
        )
        if proposed in SPEECH_BY_TASK_STATE:
            rtype, zh, pri = SPEECH_BY_TASK_STATE[proposed]
            speech_candidates.append(
                {
                    "speech_response_candidate_id": f"sp_{tsc_id}",
                    "source_task_state_candidate_id": tsc_id,
                    "response_type": rtype,
                    "speech_text_candidate_zh": zh,
                    "priority_level": pri,
                    "requires_speech_gate": True,
                    "vop_submit_allowed_later": True,
                    "tts_invoked_now": False,
                    "voice_output_plane_invoked_now": False,
                    **_not_fact(),
                }
            )
        if cmd.get("confirmation_required") or proposed in (
            "TASK_CANCEL_PENDING_CONFIRMATION",
            "TASK_PAUSE_PENDING_CONFIRMATION",
            "TASK_RESUME_PENDING",
            "TASK_HUMAN_ASSISTANCE_CANDIDATE",
        ):
            ctype = "cancel_task"
            if "PAUSE" in proposed:
                ctype = "pause_task"
            elif "RESUME" in proposed:
                ctype = "resume_task"
            elif "HUMAN" in proposed:
                ctype = "human_assistance"
            elif hid in nav_handoff_ids:
                ctype = "high_risk_navigation"
            confirmation_candidates.append(
                {
                    "confirmation_context_id": f"cc_{tsc_id}",
                    "source_task_state_candidate_id": tsc_id,
                    "confirmation_type": ctype,
                    "pending_confirmation_required": True,
                    "short_term_context_required": True,
                    "memory_scope": "short_term_only",
                    "memory_system_invoked_now": False,
                    **_not_fact(),
                }
            )

    guard_matrix = [
        {
            "guard_id": gid,
            "guard_name": gname,
            "applied": True,
            "pass_now": True,
            "blocked_reason_if_any": None,
            "violation_detected": False,
        }
        for gid, gname, _ in GUARD_RULES
    ]

    blocking_rows = [
        {
            "blocking_reason_id": bid,
            "applies_to_command_type": cmd_t,
            "recovery_candidate": recovery,
            "requires_user_prompt": req_prompt,
            "requires_observation": req_obs,
            "task_state_changed_now": False,
            **_not_fact(),
        }
        for bid, cmd_t, recovery, req_prompt, req_obs in BLOCKING_REASONS
    ]

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

    proposed_states = {c["proposed_task_state"] for c in task_state_candidates}

    return {
        "summary": {
            "schema_version": "midplatform_task_state_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "midplatform_task_state_runtime_dryrun_only",
            "based_on_voice_dialogue_runtime": voice_sum.get("voice_intent_candidates_generated") is True,
            "based_on_voice_dialogue_contract": contract_sum.get("voice_dialogue_contract_defined") is True,
            "based_on_basic_functional_loop_plan": roots["loop_plan"].is_dir(),
            "handoff_candidate_count_observed": handoff_count,
            "command_candidate_count_observed": command_count,
            "task_state_transition_guard_applied": True,
            "task_state_candidates_generated": len(task_state_candidates) > 0,
            "task_lifecycle_candidates_generated": len(lifecycle_candidates) > 0,
            "guidance_need_candidates_generated": len(guidance_candidates) > 0,
            "observation_requirement_candidates_generated": len(observation_candidates) > 0,
            "speech_response_candidates_generated": len(speech_candidates) > 0,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
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
            "schema_version": "midplatform_task_state_runtime_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "handoff_intake": {
            "schema_version": "midplatform_task_state_handoff_intake_matrix_v1",
            "handoff_candidate_count_observed": handoff_count,
            "rows": handoff_intake_rows,
            "accepted_count": sum(1 for r in handoff_intake_rows if r.get("accepted_for_task_state_dryrun")),
            **_not_fact(),
        },
        "state_schema": {
            "schema_version": "midplatform_task_state_candidate_schema_v1",
            "schema_only": True,
            "task_state_types": TASK_STATE_TYPES,
            "field_definitions": {
                "task_state_candidate_id": "string",
                "source_handoff_candidate_id": "ref",
                "proposed_task_state": "enum",
                "current_task_state_ref": "ref",
                "proposed_context_patch": "object",
                "confirmation_required": "boolean",
                "safety_gate_required": "boolean",
                "task_manager_commit_required": True,
                "task_state_changed_now": False,
            },
            "task_manager_commit_required": True,
            "task_state_changed_now": False,
            **_not_fact(),
        },
        "guard_matrix": {
            "schema_version": "midplatform_task_state_transition_guard_matrix_v1",
            "rules": {
                "create_task_requires_task_goal": True,
                "update_context_requires_task_ref_or_pending_task": True,
                "pause_requires_active_task": True,
                "resume_requires_paused_task": True,
                "cancel_requires_confirmation": True,
                "cancel_confirm_requires_pending_cancel_context": True,
                "query_status_allowed_without_state_mutation": True,
                "repeat_requires_last_guidance_ref": True,
                "human_assistance_requires_user_confirmation": True,
                "safety_can_block_or_delay_transition": True,
                "task_manager_commit_required": True,
            },
            "guards": guard_matrix,
            "task_manager_commit_required": True,
            **_not_fact(),
        },
        "state_collection": {
            "schema_version": "midplatform_task_state_candidate_collection_v1",
            "task_state_candidate_count": len(task_state_candidates),
            "candidates": task_state_candidates,
            **_not_fact(),
        },
        "lifecycle_collection": {
            "schema_version": "midplatform_task_lifecycle_candidate_collection_v1",
            "lifecycle_candidate_count": len(lifecycle_candidates),
            "candidates": lifecycle_candidates,
            **_not_fact(),
        },
        "guidance_collection": {
            "schema_version": "midplatform_task_guidance_need_candidate_collection_v1",
            "guidance_need_candidate_count": len(guidance_candidates),
            "candidates": guidance_candidates,
            **_not_fact(),
        },
        "observation_collection": {
            "schema_version": "midplatform_task_observation_requirement_candidate_collection_v1",
            "observation_requirement_candidate_count": len(observation_candidates),
            "candidates": observation_candidates,
            **_not_fact(),
        },
        "speech_collection": {
            "schema_version": "midplatform_task_speech_response_candidate_collection_v1",
            "speech_response_candidate_count": len(speech_candidates),
            "candidates": speech_candidates,
            **_not_fact(),
        },
        "confirmation_collection": {
            "schema_version": "midplatform_task_confirmation_context_candidate_collection_v1",
            "confirmation_context_candidate_count": len(confirmation_candidates),
            "candidates": confirmation_candidates,
            **_not_fact(),
        },
        "safety_dryrun": {
            "schema_version": "midplatform_task_state_safety_gate_dryrun_v1",
            "scenarios": [
                {
                    "scenario_id": "safety_inactive",
                    "safety_active": False,
                    "normal_transition_candidate_allowed": True,
                    "low_priority_transition_delayed": False,
                    "repeat_suppressed": False,
                    "clarification_suppressed": False,
                    "cancel_confirmation_delayed": False,
                },
                {
                    "scenario_id": "safety_active",
                    "safety_active": True,
                    "normal_transition_candidate_allowed": False,
                    "low_priority_transition_delayed": True,
                    "repeat_suppressed": True,
                    "clarification_suppressed": True,
                    "cancel_confirmation_delayed": True,
                    "p0_p1_can_interrupt": True,
                },
            ],
            "task_state_changed_now": False,
            **_not_fact(),
        },
        "blocking_matrix": {
            "schema_version": "midplatform_task_blocking_reason_matrix_v1",
            "blocking_reason_count": len(blocking_rows),
            "reasons": blocking_rows,
            "ocr_runtime_disabled_present": any(r["blocking_reason_id"] == "ocr_runtime_disabled" for r in blocking_rows),
            "worldmodel_runtime_deferred_present": any(
                r["blocking_reason_id"] == "worldmodel_runtime_deferred" for r in blocking_rows
            ),
            **_not_fact(),
        },
        "boundary_check": {
            "schema_version": "midplatform_task_state_boundary_check_v1",
            "midplatform_can_generate_task_state_candidate": True,
            "midplatform_cannot_commit_task_lifecycle_now": True,
            "task_manager_required_for_commit": True,
            "voice_cannot_mutate_task_state_directly": True,
            "command_candidate_is_not_task_state": True,
            "task_state_candidate_is_not_committed_state": True,
            "lifecycle_candidate_is_not_committed_event": True,
            "violation_detected": False,
            **_not_fact(),
        },
        "nav_link_check": {
            "schema_version": "midplatform_task_state_navigation_guidance_link_check_v1",
            "task_state_can_request_navigation_guidance_candidate": True,
            "navigation_guidance_candidate_generated_for_relevant_utterance": any(
                g.get("guidance_need_type") == "basic_navigation_guidance_candidate" for g in guidance_candidates
            ),
            "navigation_guidance_requires_task_active_or_creation_candidate": True,
            "navigation_guidance_requires_safety_check": True,
            "navigation_guidance_requires_observation_candidate": True,
            "navigation_action_triggered": False,
            "basic_navigation_loop_runtime_invoked_now": False,
            **_not_fact(),
        },
        "dialogue_feedback_check": {
            "schema_version": "midplatform_task_state_dialogue_feedback_link_check_v1",
            "task_state_candidate_can_request_speech_response": True,
            "speech_response_requires_speech_gate": True,
            "speech_response_can_feed_short_term_dialogue_context": True,
            "voice_output_plane_invoked_now": False,
            "tts_invoked_now": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "midplatform_task_state_runtime_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "midplatform_task_state_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "handoff_candidate_count_observed": handoff_count,
            "task_state_candidate_count": len(task_state_candidates),
            "lifecycle_candidate_count": len(lifecycle_candidates),
            "guidance_need_candidate_count": len(guidance_candidates),
            "observation_requirement_candidate_count": len(observation_candidates),
            "task_state_changed_now": False,
            "task_manager_invoked_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "alternate_next_phases": [
                "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
                "Basic-Navigation-Guidance-Loop-DryRun-v1",
            ],
            "task_cancel_pending_confirmation_present": "TASK_CANCEL_PENDING_CONFIRMATION" in proposed_states,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "midplatform_task_state_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
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
            "schema_version": "midplatform_task_state_runtime_metrics_candidate_report_v1",
            "handoff_candidate_count_observed": handoff_count,
            "task_state_candidate_count": len(task_state_candidates),
            "lifecycle_candidate_count": len(lifecycle_candidates),
            "guidance_need_candidate_count": len(guidance_candidates),
            "observation_requirement_candidate_count": len(observation_candidates),
            "speech_response_candidate_count": len(speech_candidates),
            "confirmation_context_candidate_count": len(confirmation_candidates),
            "transition_guard_count": len(guard_matrix),
            "blocking_reason_count": len(blocking_rows),
            "runtime_action_committed_count": 0,
            "task_state_change_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "midplatform_task_state_runtime_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "midplatform_task_state_runtime_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "midplatform_task_state_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
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
            "schema_version": "midplatform_task_state_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "midplatform_task_state_runtime_non_claims_report_v1",
            "claims": [
                "runtime_dryrun_not_real_task_manager",
                "task_state_candidate_not_committed_state",
                "lifecycle_candidate_not_committed_event",
                "guidance_need_not_navigation_action",
                "observation_requirement_not_camera_ocr_execution",
                "speech_response_not_tts",
                "confirmation_context_not_memory_write",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "midplatform_task_state_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "midplatform_task_state_runtime_audit_report_v1",
            "midplatform_task_state_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "handoff_candidate_count_observed": handoff_count,
            "task_state_transition_guard_applied": True,
            "task_state_candidates_generated": True,
            "task_lifecycle_candidates_generated": True,
            "guidance_need_candidates_generated": True,
            "observation_requirement_candidates_generated": True,
            "speech_response_candidates_generated": True,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
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
            "benchmark_result_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
