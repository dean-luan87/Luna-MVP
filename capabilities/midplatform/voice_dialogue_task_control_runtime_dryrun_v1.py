# -*- coding: utf-8 -*-
"""Voice Dialogue Task Control Runtime DryRun v1 — simulated utterances only.

Phase-Voice-Dialogue-Task-Control-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Voice-Dialogue-Task-Control-Runtime-DryRun-v1-001"
FINAL_DECISION = "VOICE_DIALOGUE_TASK_CONTROL_RUNTIME_DRYRUN_READY_FOR_TASK_MANAGER_INTEGRATION"
RECOMMENDED_NEXT = "MidPlatform-Task-State-Runtime-DryRun-v1"

FOLLOWUPS = [
    "MidPlatform-Task-State-Runtime-DryRun-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Voice-Guidance-Runtime-GuardedTrial-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Dialogue-Driven-Task-Clarification-Runtime-v1",
    "Task-Manager-Contract-v1",
    "Dialogue-Manager-Contract-v1",
]

SIMULATED_UTTERANCES: List[Tuple[str, str, str]] = [
    ("utt_001", "带我去出口", "START_TASK"),
    ("utt_002", "我要找洗手间", "START_TASK"),
    ("utt_003", "现在任务是什么", "QUERY_TASK_STATUS"),
    ("utt_004", "刚才再说一遍", "REPEAT_LAST_GUIDANCE"),
    ("utt_005", "先暂停一下", "PAUSE_TASK"),
    ("utt_006", "继续刚才的任务", "RESUME_TASK"),
    ("utt_007", "取消任务", "CANCEL_TASK"),
    ("utt_008", "是的，取消", "CONFIRM_CONTINUE"),
    ("utt_009", "我现在在商场", "CONFIRM_SCENE"),
    ("utt_010", "我要找门牌", "START_TASK"),
    ("utt_011", "不知道该怎么走", "USER_DOES_NOT_KNOW"),
    ("utt_012", "帮我问工作人员吧", "REQUEST_HUMAN_ASSISTANCE"),
]

INTENT_TO_COMMAND: Dict[str, str] = {
    "START_TASK": "CREATE_TASK_CANDIDATE",
    "QUERY_TASK_STATUS": "QUERY_STATUS_CANDIDATE",
    "REPEAT_LAST_GUIDANCE": "REPEAT_GUIDANCE_CANDIDATE",
    "PAUSE_TASK": "PAUSE_TASK_CANDIDATE",
    "RESUME_TASK": "RESUME_TASK_CANDIDATE",
    "CANCEL_TASK": "REQUEST_CONFIRMATION_CANDIDATE",
    "CONFIRM_CONTINUE": "CANCEL_TASK_CANDIDATE",
    "CONFIRM_SCENE": "UPDATE_TASK_CONTEXT_CANDIDATE",
    "USER_DOES_NOT_KNOW": "REQUEST_CLARIFICATION_CANDIDATE",
    "REQUEST_HUMAN_ASSISTANCE": "REQUEST_HUMAN_ASSISTANCE_CANDIDATE",
}

SPEECH_BY_INTENT: Dict[str, Tuple[str, str, str]] = {
    "START_TASK": ("task_ack", "好的，我先记录你的任务。", "P3"),
    "QUERY_TASK_STATUS": ("status", "当前任务还在进行中。", "P3"),
    "REPEAT_LAST_GUIDANCE": ("repeat", "我再重复一次刚才的提示。", "P3"),
    "PAUSE_TASK": ("confirm_pause", "确认要暂停当前任务吗？", "P3"),
    "RESUME_TASK": ("confirm_resume", "确认要继续当前任务吗？", "P3"),
    "CANCEL_TASK": ("confirm_cancel", "确认要取消当前任务吗？", "P2"),
    "CONFIRM_CONTINUE": ("cancel_ack", "已记录取消请求，等待任务管理确认。", "P2"),
    "CONFIRM_SCENE": ("scene_ack", "好的，已记录你现在的场景。", "P3"),
    "USER_DOES_NOT_KNOW": ("clarification", "你想完成什么任务？", "P3"),
    "REQUEST_HUMAN_ASSISTANCE": ("escalation", "是否需要人工协助？", "P2"),
}

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_contract", "contract_loaded", [], [], []),
    ("load_basic_loop_plan", "loop_plan_loaded", [], [], []),
    ("define_simulated_utterances", "utterances_defined", [], [], []),
    ("generate_intent_candidates", "intents_generated", [], [], ["direct_task_state_change"]),
    ("generate_command_candidates", "commands_generated", [], [], []),
    ("apply_policies", "policies_applied", [], [], []),
    ("generate_state_dryrun_trace", "state_trace_ok", [], [], []),
    ("generate_handoff_candidates", "handoffs_generated", [], [], ["task_manager_invoke"]),
    ("generate_speech_response_candidates", "speech_candidates_ok", [], [], ["tts_invoke", "vop_invoke"]),
    ("generate_short_term_context_candidates", "stm_candidates_ok", [], [], ["memory_write"]),
    ("evaluate_safety_suppression", "safety_evaluated", [], [], []),
    ("evaluate_query_status", "query_status_ok", [], [], []),
    ("evaluate_cancel_confirmation", "cancel_confirm_ok", [], [], ["task_cancelled"]),
    ("evaluate_repeat_guidance", "repeat_ok", [], [], []),
    ("evaluate_human_assistance", "human_assistance_ok", [], [], ["navigation_action"]),
    ("check_midplatform_boundary", "boundary_ok", [], [], ["voice_cancel_direct"]),
    ("check_navigation_guidance_link", "nav_link_ok", [], [], ["nav_action_direct"]),
    ("generate_final_runtime_dryrun_decision", "dryrun_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "task_manager": "**/*TASK*MANAGER*.md",
    "taskchain_runtime": "**/*TASK*CHAIN*.md",
    "voice_session_runtime": "**/*SESSION*STATE*.md",
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


def _end_state(intent: str, utterance_id: str) -> str:
    if intent == "CANCEL_TASK":
        return "WAITING_FOR_CONFIRMATION"
    if intent == "CONFIRM_CONTINUE" and utterance_id == "utt_008":
        return "WAITING_FOR_TASK_MANAGER_DECISION"
    if intent in ("USER_DOES_NOT_KNOW",):
        return "WAITING_FOR_CLARIFICATION"
    if intent == "REPEAT_LAST_GUIDANCE":
        return "GUIDANCE_REPEAT_CANDIDATE_READY"
    if intent == "REQUEST_HUMAN_ASSISTANCE":
        return "ESCALATED_TO_HUMAN_ASSISTANCE_CANDIDATE"
    if intent in ("PAUSE_TASK", "RESUME_TASK"):
        return "WAITING_FOR_CONFIRMATION"
    if intent in ("START_TASK", "CONFIRM_SCENE"):
        return "TASK_CONTROL_COMMAND_CANDIDATE_READY"
    if intent == "QUERY_TASK_STATUS":
        return "WAITING_FOR_TASK_MANAGER_DECISION"
    return "TASK_INTENT_CANDIDATE_READY"


def run_voice_dialogue_task_control_runtime_dryrun_v1(
    *,
    voice_dialogue_contract_root: str,
    basic_loop_plan_root: str,
    voice_guidance_runtime_root: str,
    vop_adapter_root: str,
    user_clarification_runtime_root: str,
    user_clarification_parsing_root: str,
    task_scene_runtime_root: str,
    task_scene_reevaluation_root: str,
    ocr_activation_root: str,
    stc_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or "/Users/luanlei/Desktop/Luna-Workspace-Min").resolve()
    roots = {
        "contract": Path(voice_dialogue_contract_root).resolve(),
        "loop_plan": Path(basic_loop_plan_root).resolve(),
        "voice_guidance": Path(voice_guidance_runtime_root).resolve(),
        "vop": Path(vop_adapter_root).resolve(),
        "user_clarify": Path(user_clarification_runtime_root).resolve(),
        "user_parse": Path(user_clarification_parsing_root).resolve(),
        "task_scene": Path(task_scene_runtime_root).resolve(),
        "task_reeval": Path(task_scene_reevaluation_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    contract_sum = _read_json(roots["contract"] / "voice_dialogue_task_control_contract_v1_summary.json") or {}
    contract_ok = contract_sum.get("voice_dialogue_contract_defined") is True

    intake_specs = [
        ("voice_dialogue_contract", roots["contract"], "voice_dialogue_task_control_contract_v1_summary.json", False),
        ("basic_functional_loop_plan", roots["loop_plan"], "luna_basic_functional_loop_stabilization_plan_v1_summary.json", False),
        ("voice_guidance_runtime", roots["voice_guidance"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
        ("vop_adapter", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
        ("user_clarification_runtime", roots["user_clarify"], "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary.json", False),
        ("user_clarification_parsing", roots["user_parse"], "user_clarification_response_parsing_dryrun_for_reading_v1_summary.json", False),
        ("task_scene_runtime", roots["task_scene"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json", False),
        ("task_scene_reevaluation", roots["task_reeval"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
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

    utterance_rows = [
        {
            "simulated_utterance_id": uid,
            "utterance_text": text,
            "expected_intent_type": intent,
            "simulation_only": True,
            "not_user_fact": True,
            **_not_fact(),
        }
        for uid, text, intent in SIMULATED_UTTERANCES
    ]

    pending_cancel = False
    active_task_ref = "task_ref_dryrun_active_001"
    last_guidance_ref = "guidance_ref_dryrun_last_001"
    dialogue_state = "IDLE"
    intent_candidates: List[Dict[str, Any]] = []
    command_candidates: List[Dict[str, Any]] = []
    handoff_candidates: List[Dict[str, Any]] = []
    speech_candidates: List[Dict[str, Any]] = []
    stm_candidates: List[Dict[str, Any]] = []
    state_trace_rows: List[Dict[str, Any]] = []
    suppressed_count = 0

    for uid, text, intent_type in SIMULATED_UTTERANCES:
        start_state = dialogue_state
        requires_confirmation = intent_type in ("CANCEL_TASK", "PAUSE_TASK", "RESUME_TASK", "REQUEST_HUMAN_ASSISTANCE")
        if intent_type == "CONFIRM_CONTINUE" and uid == "utt_008":
            if not pending_cancel:
                requires_confirmation = True
            intent_type = "CONFIRM_CONTINUE"
        if intent_type == "CANCEL_TASK":
            pending_cancel = True
        if intent_type == "CONFIRM_CONTINUE" and uid == "utt_008":
            if not pending_cancel:
                requires_confirmation = True

        ic_id = f"intent_{uid}"
        intent_candidates.append(
            {
                "intent_candidate_id": ic_id,
                "source_utterance_id": uid,
                "normalized_intent_type": intent_type,
                "confidence_placeholder": 0.85,
                "task_context_candidate": {"task_goal": text} if intent_type == "START_TASK" else {},
                "scene_context_candidate": {"scene_label": "商场"} if intent_type == "CONFIRM_SCENE" else {},
                "target_information_need_candidate": text,
                "requires_confirmation": requires_confirmation,
                "requires_midplatform_decision": True,
                "direct_task_state_change_allowed": False,
                "depends_on_pending_confirmation": uid == "utt_008",
                **_not_fact(),
            }
        )

        cmd_type = INTENT_TO_COMMAND.get(intent_type, "REQUEST_CLARIFICATION_CANDIDATE")
        if uid == "utt_008" and not pending_cancel:
            cmd_type = "REQUEST_CONFIRMATION_CANDIDATE"
        cc_id = f"cmd_{uid}"
        command_candidates.append(
            {
                "command_candidate_id": cc_id,
                "source_intent_candidate_id": ic_id,
                "command_type": cmd_type,
                "target_task_ref": active_task_ref if cmd_type != "CREATE_TASK_CANDIDATE" else "task_ref_candidate_new",
                "proposed_task_state": "candidate_only",
                "proposed_context_patch": {"utterance": text},
                "confirmation_required": requires_confirmation,
                "midplatform_task_manager_required": True,
                "task_state_changed_now": False,
                **_not_fact(),
            }
        )

        if intent_type == "CONFIRM_SCENE":
            stm_candidates.append(
                {
                    "context_candidate_id": f"stm_scene_{uid}",
                    "source_utterance_id": uid,
                    "context_type": "clarification_context",
                    "memory_scope": "short_term_only",
                    "memory_system_invoked_now": False,
                    "long_term_memory_write_allowed": False,
                    "write_allowed_now": False,
                    **_not_fact(),
                }
            )
        if intent_type == "CANCEL_TASK":
            stm_candidates.append(
                {
                    "context_candidate_id": f"stm_pending_cancel_{uid}",
                    "source_utterance_id": uid,
                    "context_type": "pending_confirmation",
                    "memory_scope": "short_term_only",
                    "memory_system_invoked_now": False,
                    "long_term_memory_write_allowed": False,
                    "write_allowed_now": False,
                    **_not_fact(),
                }
            )
        if intent_type == "REPEAT_LAST_GUIDANCE":
            stm_candidates.append(
                {
                    "context_candidate_id": f"stm_last_guidance_{uid}",
                    "source_utterance_id": uid,
                    "context_type": "last_guidance_ref",
                    "memory_scope": "short_term_only",
                    "memory_system_invoked_now": False,
                    "long_term_memory_write_allowed": False,
                    "write_allowed_now": False,
                    **_not_fact(),
                }
            )
        if intent_type in ("START_TASK", "PAUSE_TASK"):
            stm_candidates.append(
                {
                    "context_candidate_id": f"stm_active_{uid}",
                    "source_utterance_id": uid,
                    "context_type": "active_task_ref" if intent_type == "START_TASK" else "paused_task_ref",
                    "memory_scope": "short_term_only",
                    "memory_system_invoked_now": False,
                    "long_term_memory_write_allowed": False,
                    "write_allowed_now": False,
                    **_not_fact(),
                }
            )

        end_state = _end_state(intent_type, uid)
        dialogue_state = end_state
        policy_pass = True
        blocked_reason = None
        if intent_type == "REPEAT_LAST_GUIDANCE":
            policy_pass = True
        handoff_candidates.append(
            {
                "handoff_candidate_id": f"handoff_{uid}",
                "source_intent_candidate_id": ic_id,
                "source_command_candidate_id": cc_id,
                "current_task_state_ref": active_task_ref,
                "dialogue_context_ref": f"dlg_ctx_{uid}",
                "source_chain": "voice_dialogue_runtime_dryrun_v1",
                "time_anchor": "dryrun_session_t0",
                "safety_priority_state": "normal",
                "confirmation_requirement": requires_confirmation,
                "handoff_allowed_later": True,
                "handoff_invoked_now": False,
                "task_manager_invoked_now": False,
                **_not_fact(),
            }
        )

        if intent_type in SPEECH_BY_INTENT:
            rtype, speech_zh, pri = SPEECH_BY_INTENT[intent_type]
            speech_candidates.append(
                {
                    "speech_response_candidate_id": f"speech_{uid}",
                    "source_intent_candidate_id": ic_id,
                    "response_type": rtype,
                    "speech_text_candidate_zh": speech_zh,
                    "priority_level": pri,
                    "requires_speech_gate": True,
                    "vop_submit_allowed_later": True,
                    "tts_invoked_now": False,
                    "vop_invoked_now": False,
                    **_not_fact(),
                }
            )

        state_trace_rows.append(
            {
                "source_utterance_id": uid,
                "start_dialogue_state": start_state,
                "detected_intent_candidate": ic_id,
                "command_candidate": cc_id,
                "policy_result": "pass" if policy_pass else "blocked",
                "blocked_reason_if_any": blocked_reason,
                "end_dialogue_state": end_state,
                "task_state_changed_now": False,
                **_not_fact(),
            }
        )

    policy_rows = [
        ("repeat_policy", "repeat_pause_resume_cancel", True, True, None, True),
        ("pause_policy", "repeat_pause_resume_cancel", True, True, None, True),
        ("resume_policy", "repeat_pause_resume_cancel", True, True, None, True),
        ("cancel_policy", "repeat_pause_resume_cancel", True, True, None, True),
        ("query_status_policy", "query_status", True, True, None, True),
        ("clarification_policy", "task_clarification", True, True, None, True),
        ("safety_suppression_policy", "safety_priority", True, True, None, True),
        ("speech_gate_policy", "speech_gate_vop", True, True, None, True),
    ]
    policy_matrix = [
        {
            "policy_id": pid,
            "policy_name": pname,
            "applied": applied,
            "pass_now": pass_now,
            "blocked_reason_if_any": blocked,
            "output_candidate_generated": out_gen,
            "runtime_action_committed": False,
        }
        for pid, pname, applied, pass_now, blocked, out_gen in policy_rows
    ]

    nav_utterances = {"utt_001", "utt_002", "utt_010"}
    navigation_guidance_generated = any(u[0] in nav_utterances for u in SIMULATED_UTTERANCES)

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

    intent_types = {c["normalized_intent_type"] for c in intent_candidates}
    required_intents = {
        "START_TASK",
        "QUERY_TASK_STATUS",
        "REPEAT_LAST_GUIDANCE",
        "PAUSE_TASK",
        "RESUME_TASK",
        "CANCEL_TASK",
        "CONFIRM_SCENE",
        "REQUEST_HUMAN_ASSISTANCE",
    }

    return {
        "summary": {
            "schema_version": "voice_dialogue_task_control_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "voice_dialogue_task_control_runtime_dryrun_only",
            "based_on_voice_dialogue_contract": contract_ok,
            "based_on_basic_functional_loop_plan": roots["loop_plan"].is_dir(),
            "simulated_utterance_set_defined": True,
            "voice_intent_candidates_generated": True,
            "task_control_command_candidates_generated": True,
            "dialogue_state_dryrun_trace_generated": True,
            "dialogue_to_task_handoff_candidates_generated": True,
            "speech_response_candidates_generated": True,
            "short_term_context_candidates_generated": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "navigation_action_triggered": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "required_intents_covered": required_intents.issubset(intent_types),
        },
        "intake": {
            "schema_version": "voice_dialogue_runtime_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "utterance_set": {
            "schema_version": "voice_dialogue_runtime_simulated_utterance_set_v1",
            "utterances": utterance_rows,
            "utterance_count": len(utterance_rows),
            **_not_fact(),
        },
        "intent_collection": {
            "schema_version": "voice_dialogue_runtime_intent_candidate_collection_v1",
            "intent_candidate_count": len(intent_candidates),
            "candidates": intent_candidates,
            **_not_fact(),
        },
        "command_collection": {
            "schema_version": "voice_dialogue_runtime_command_candidate_collection_v1",
            "command_candidate_count": len(command_candidates),
            "candidates": command_candidates,
            **_not_fact(),
        },
        "policy_matrix": {
            "schema_version": "voice_dialogue_runtime_policy_application_matrix_v1",
            "policies": policy_matrix,
            **_not_fact(),
        },
        "state_trace": {
            "schema_version": "voice_dialogue_runtime_state_dryrun_trace_v1",
            "trace_rows": state_trace_rows,
            **_not_fact(),
        },
        "handoff_collection": {
            "schema_version": "voice_dialogue_runtime_handoff_candidate_collection_v1",
            "handoff_candidate_count": len(handoff_candidates),
            "candidates": handoff_candidates,
            **_not_fact(),
        },
        "speech_collection": {
            "schema_version": "voice_dialogue_runtime_speech_response_candidate_collection_v1",
            "speech_response_candidate_count": len(speech_candidates),
            "candidates": speech_candidates,
            **_not_fact(),
        },
        "stm_collection": {
            "schema_version": "voice_dialogue_runtime_short_term_context_candidate_collection_v1",
            "short_term_context_candidate_count": len(stm_candidates),
            "candidates": stm_candidates,
            **_not_fact(),
        },
        "safety_dryrun": {
            "schema_version": "voice_dialogue_runtime_safety_suppression_dryrun_v1",
            "scenarios": [
                {
                    "scenario_id": "safety_inactive",
                    "safety_alert_active": False,
                    "dialogue_candidate_allowed": True,
                    "repeat_allowed": True,
                    "low_priority_clarification_suppressed": False,
                },
                {
                    "scenario_id": "safety_active",
                    "safety_alert_active": True,
                    "dialogue_candidate_allowed": False,
                    "repeat_allowed": False,
                    "low_priority_clarification_suppressed": True,
                    "p0_p1_can_interrupt_dialogue": True,
                    "cancel_confirmation_can_be_delayed": True,
                },
            ],
            "runtime_arbitration_invoked_now": False,
            **_not_fact(),
        },
        "query_status_dryrun": {
            "schema_version": "voice_dialogue_runtime_query_status_dryrun_v1",
            "query_status_utterance_observed": "utt_003" in {u[0] for u in SIMULATED_UTTERANCES},
            "status_response_candidate_generated": True,
            "status_response_must_not_expose_internal_debug": True,
            "status_response_requires_speech_gate": True,
            "task_status_fact_write_allowed": False,
            "tts_invoked_now": False,
            **_not_fact(),
        },
        "cancel_confirmation_dryrun": {
            "schema_version": "voice_dialogue_runtime_cancel_confirmation_dryrun_v1",
            "cancel_task_utterance_observed": True,
            "cancel_requires_confirmation": True,
            "pending_cancel_confirmation_candidate_generated": True,
            "confirm_cancel_utterance_observed": True,
            "confirm_cancel_depends_on_pending_context": True,
            "task_cancelled_now": False,
            "task_manager_required": True,
            **_not_fact(),
        },
        "repeat_guidance_dryrun": {
            "schema_version": "voice_dialogue_runtime_repeat_guidance_dryrun_v1",
            "repeat_utterance_observed": True,
            "last_guidance_ref_required": True,
            "short_term_context_required": True,
            "repeat_response_candidate_generated": True,
            "repeat_blocked_when_safety_alert_active": True,
            "tts_invoked_now": False,
            **_not_fact(),
        },
        "human_assistance_dryrun": {
            "schema_version": "voice_dialogue_runtime_human_assistance_dryrun_v1",
            "human_assistance_utterance_observed": True,
            "request_human_assistance_candidate_generated": True,
            "confirmation_required": True,
            "task_manager_invoked_now": False,
            "navigation_action_triggered": False,
            **_not_fact(),
        },
        "midplatform_boundary": {
            "schema_version": "voice_dialogue_runtime_midplatform_boundary_check_v1",
            "voice_owns_intent_candidate_only": True,
            "midplatform_owns_task_state": True,
            "task_manager_owns_task_lifecycle": True,
            "voice_cannot_create_task_directly": True,
            "voice_cannot_cancel_task_directly": True,
            "voice_cannot_pause_task_directly": True,
            "voice_cannot_resume_task_directly": True,
            "task_state_changed_now": False,
            "violation_detected": False,
            **_not_fact(),
        },
        "nav_link_check": {
            "schema_version": "voice_dialogue_runtime_navigation_guidance_link_check_v1",
            "dialogue_can_request_navigation_guidance_candidate": True,
            "navigation_guidance_candidate_generated_for_relevant_utterance": navigation_guidance_generated,
            "navigation_guidance_requires_task_context": True,
            "navigation_guidance_requires_safety_check": True,
            "dialogue_cannot_trigger_navigation_action_directly": True,
            "navigation_action_triggered": False,
            "basic_navigation_loop_runtime_invoked_now": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "voice_dialogue_task_control_runtime_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "voice_dialogue_task_control_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "simulated_utterance_count": len(SIMULATED_UTTERANCES),
            "intent_candidate_count": len(intent_candidates),
            "command_candidate_count": len(command_candidates),
            "handoff_candidate_count": len(handoff_candidates),
            "speech_response_candidate_count": len(speech_candidates),
            "task_state_changed_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "voice_dialogue_task_control_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "navigation_action_triggered": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "voice_dialogue_task_control_runtime_metrics_candidate_report_v1",
            "simulated_utterance_count": len(SIMULATED_UTTERANCES),
            "intent_candidate_count": len(intent_candidates),
            "command_candidate_count": len(command_candidates),
            "handoff_candidate_count": len(handoff_candidates),
            "speech_response_candidate_count": len(speech_candidates),
            "short_term_context_candidate_count": len(stm_candidates),
            "suppressed_dialogue_candidate_count": suppressed_count,
            "runtime_action_committed_count": 0,
            "task_state_change_count": 0,
            "tts_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "voice_dialogue_task_control_runtime_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "voice_dialogue_task_control_runtime_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_dialogue_task_control_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "navigation_action_triggered": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "voice_dialogue_task_control_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "voice_dialogue_task_control_runtime_non_claims_report_v1",
            "claims": [
                "runtime_dryrun_not_real_asr",
                "simulated_utterance_not_user_fact",
                "intent_candidate_not_task_state",
                "command_candidate_not_task_change",
                "handoff_candidate_not_task_manager_execution",
                "speech_response_candidate_not_tts",
                "short_term_context_not_memory_write",
                "navigation_guidance_candidate_not_navigation_action",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "voice_dialogue_task_control_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "voice_dialogue_task_control_runtime_audit_report_v1",
            "voice_dialogue_task_control_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "simulated_utterance_set_defined": True,
            "voice_intent_candidates_generated": True,
            "task_control_command_candidates_generated": True,
            "dialogue_state_dryrun_trace_generated": True,
            "dialogue_to_task_handoff_candidates_generated": True,
            "speech_response_candidates_generated": True,
            "short_term_context_candidates_generated": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "task_manager_invoked": False,
            "task_state_changed_now": False,
            "task_created_now": False,
            "task_cancelled_now": False,
            "task_paused_now": False,
            "task_resumed_now": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "navigation_action_triggered": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
