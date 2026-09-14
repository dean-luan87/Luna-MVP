# -*- coding: utf-8 -*-
"""Voice Dialogue Task Control Contract v1 — contract/schema/policy only; no runtime.

Phase-Voice-Dialogue-Task-Control-Contract-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Voice-Dialogue-Task-Control-Contract-v1-001"
FINAL_DECISION = "VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_READY"
RECOMMENDED_NEXT = "Voice-Dialogue-Task-Control-Runtime-DryRun-v1"

FOLLOWUPS = [
    "Voice-Dialogue-Task-Control-Runtime-DryRun-v1",
    "MidPlatform-Task-State-Runtime-DryRun-v1",
    "Vision-OCR-Evidence-Ingest-Integration-Check-v1",
    "Voice-Guidance-Runtime-GuardedTrial-v1",
    "Basic-Navigation-Guidance-Loop-DryRun-v1",
    "Dialogue-Driven-Task-Clarification-Runtime-v1",
]

INTENT_TYPES = [
    "START_TASK",
    "CLARIFY_TASK",
    "QUERY_TASK_STATUS",
    "REPEAT_LAST_GUIDANCE",
    "PAUSE_TASK",
    "RESUME_TASK",
    "CANCEL_TASK",
    "CONFIRM_TARGET",
    "CONFIRM_SCENE",
    "CONFIRM_CONTINUE",
    "ASK_WHAT_TO_DO",
    "USER_DOES_NOT_KNOW",
    "REQUEST_HUMAN_ASSISTANCE",
]

COMMAND_TYPES = [
    "CREATE_TASK_CANDIDATE",
    "UPDATE_TASK_CONTEXT_CANDIDATE",
    "PAUSE_TASK_CANDIDATE",
    "RESUME_TASK_CANDIDATE",
    "CANCEL_TASK_CANDIDATE",
    "QUERY_STATUS_CANDIDATE",
    "REPEAT_GUIDANCE_CANDIDATE",
    "REQUEST_CLARIFICATION_CANDIDATE",
    "REQUEST_CONFIRMATION_CANDIDATE",
    "REQUEST_HUMAN_ASSISTANCE_CANDIDATE",
]

DIALOGUE_STATES = [
    ("IDLE", "no active dialogue session", [], ["LISTENING_FOR_TASK"], []),
    ("LISTENING_FOR_TASK", "awaiting user utterance", ["START_TASK", "ASK_WHAT_TO_DO"], ["TASK_INTENT_CANDIDATE_READY"], []),
    ("TASK_INTENT_CANDIDATE_READY", "intent parsed", ["CLARIFY_TASK"], ["WAITING_FOR_CLARIFICATION", "TASK_CONTROL_COMMAND_CANDIDATE_READY"], []),
    ("WAITING_FOR_CLARIFICATION", "missing task/scene", ["CLARIFY_TASK", "CONFIRM_TARGET", "CONFIRM_SCENE"], ["TASK_CONTROL_COMMAND_CANDIDATE_READY"], []),
    ("WAITING_FOR_CONFIRMATION", "pending user confirm", ["CONFIRM_CONTINUE", "CANCEL_TASK"], ["TASK_CONTROL_COMMAND_CANDIDATE_READY", "CANCELLED_CANDIDATE"], ["direct_state_change"]),
    ("TASK_CONTROL_COMMAND_CANDIDATE_READY", "command candidate emitted", [], ["WAITING_FOR_TASK_MANAGER_DECISION"], ["voice_direct_cancel"]),
    ("WAITING_FOR_TASK_MANAGER_DECISION", "midplatform decides", ["QUERY_TASK_STATUS"], ["GUIDANCE_REPEAT_CANDIDATE_READY"], []),
    ("GUIDANCE_REPEAT_CANDIDATE_READY", "repeat requested", ["REPEAT_LAST_GUIDANCE"], ["LISTENING_FOR_TASK"], []),
    ("PAUSED_DIALOGUE_CONTEXT", "task pause dialogue", ["RESUME_TASK", "QUERY_TASK_STATUS"], ["LISTENING_FOR_TASK"], []),
    ("CANCELLED_CANDIDATE", "cancel candidate", [], ["IDLE"], []),
    ("ESCALATED_TO_HUMAN_ASSISTANCE_CANDIDATE", "human help", ["REQUEST_HUMAN_ASSISTANCE"], ["IDLE"], []),
]

TEMPLATES = [
    ("start_task_ack_candidate", "start_task", "好的，我先记录你的任务。", "P3"),
    ("ask_task_clarification", "clarification", "你想完成什么任务？", "P3"),
    ("ask_scene_clarification", "clarification", "你现在在什么场景？", "P3"),
    ("confirm_cancel_task", "confirmation", "确认要取消当前任务吗？", "P2"),
    ("confirm_pause_task", "confirmation", "确认要暂停当前任务吗？", "P3"),
    ("confirm_resume_task", "confirmation", "确认要继续当前任务吗？", "P3"),
    ("repeat_last_guidance", "repeat", "我再重复一次刚才的提示。", "P3"),
    ("report_task_status", "status", "当前任务还在进行中。", "P3"),
    ("ask_continue", "confirmation", "需要我继续引导吗？", "P3"),
    ("request_human_assistance_confirm", "escalation", "是否需要人工协助？", "P2"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_basic_functional_loop_plan", "loop_plan_loaded", [], [], []),
    ("load_voice_guidance_chain", "voice_chain_loaded", [], [], ["direct_tts"]),
    ("load_vop_adapter", "vop_loaded", [], [], ["vop_runtime"]),
    ("load_task_context_chain", "task_context_loaded", [], [], []),
    ("define_voice_intent_candidate_schema", "intent_schema_ok", [], [], ["direct_task_state_change"]),
    ("define_task_control_command_schema", "command_schema_ok", [], [], []),
    ("define_dialogue_to_task_handoff_policy", "handoff_ok", [], [], []),
    ("define_short_term_dialogue_context_policy", "stm_ok", [], [], ["memory_write"]),
    ("define_repeat_pause_resume_cancel_policy", "rpc_ok", [], [], []),
    ("define_query_status_policy", "query_ok", [], [], []),
    ("define_task_clarification_policy", "clarify_ok", [], [], []),
    ("define_safety_priority_suppression_policy", "safety_ok", [], [], []),
    ("define_speech_gate_vop_output_policy", "speech_gate_ok", [], [], ["tts_bypass"]),
    ("define_dialogue_state_machine", "fsm_ok", [], [], []),
    ("define_midplatform_task_manager_boundary", "boundary_ok", [], [], ["voice_cancel_direct"]),
    ("define_navigation_guidance_link", "nav_link_ok", [], [], ["nav_action_direct"]),
    ("generate_final_contract_decision", "contract_ready", [], [], ["production_ready"]),
]

OPTIONAL_DOC_GLOBS = {
    "voice_mainline": "**/LUNA_VOICE*MAINLINE*.md",
    "asr_contract": "**/*ASR*.md",
    "dialogue_manager": "**/*DIALOGUE*MANAGER*.md",
    "task_chain": "**/*TASK*CHAIN*.md",
    "task_manager": "**/*TASK*MANAGER*.md",
    "session_state_anchor": "**/*SESSION*STATE*.md",
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


def run_voice_dialogue_task_control_contract_v1(
    *,
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

    loop_sum = _read_json(roots["loop_plan"] / "luna_basic_functional_loop_stabilization_plan_v1_summary.json") or {}
    voice_sum = _read_json(roots["voice_guidance"] / "voice_guidance_prompt_runtime_dryrun_v1_summary.json") or {}

    intake_specs = [
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
                "missing_impact": "none" if loaded else ("optional_reference_only" if optional else "contract_partial"),
                **_not_fact(),
            }
        )
    intake_rows.extend(_find_optional_docs(ws))

    state_rows = [
        {
            "state": state,
            "entry_condition": cond,
            "allowed_intents": allowed,
            "allowed_transitions": transitions,
            "blocked_transitions": blocked,
            "task_state_changed_now": False,
            **_not_fact(),
        }
        for state, cond, allowed, transitions, blocked in DIALOGUE_STATES
    ]

    template_rows = [
        {
            "template_id": tid,
            "template_type": ttype,
            "short_prompt_zh": prompt,
            "priority_level": pri,
            "requires_speech_gate": True,
            "tts_invoked_now": False,
            "prohibited_wording": ["已取消任务", "任务已暂停", "事实已确认"],
            **_not_fact(),
        }
        for tid, ttype, prompt, pri in TEMPLATES
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

    return {
        "summary": {
            "schema_version": "voice_dialogue_task_control_contract_v1_summary_v0",
            "phase": PHASE_ID,
            "contract_scope": "voice_dialogue_task_control_contract_only",
            "based_on_basic_functional_loop_plan": roots["loop_plan"].is_dir(),
            "based_on_voice_guidance_chain": roots["voice_guidance"].is_dir() and roots["vop"].is_dir(),
            "based_on_task_context_chain": roots["task_scene"].is_dir(),
            "voice_dialogue_contract_defined": True,
            "voice_intent_candidate_schema_defined": True,
            "task_control_command_schema_defined": True,
            "dialogue_to_task_handoff_policy_defined": True,
            "short_term_dialogue_context_policy_defined": True,
            "repeat_pause_resume_cancel_policy_defined": True,
            "speech_gate_vop_output_policy_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
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
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
            "all_voice_output_requires_speech_gate": loop_sum.get("voice_plan", {}).get("all_voice_output_requires_speech_gate", True)
            if isinstance(loop_sum.get("voice_plan"), dict)
            else True,
        },
        "intake": {
            "schema_version": "voice_dialogue_task_control_input_intake_matrix_v1",
            "rows": intake_rows,
            **_not_fact(),
        },
        "intent_schema": {
            "schema_version": "voice_dialogue_intent_candidate_schema_v1",
            "schema_only": True,
            "intent_types": INTENT_TYPES,
            "field_definitions": {
                "intent_candidate_id": "string",
                "raw_user_utterance_ref": "ref",
                "normalized_intent_type": "enum",
                "confidence_placeholder": "number_or_null",
                "task_context_candidate": "object",
                "scene_context_candidate": "object",
                "target_information_need_candidate": "string",
                "requires_confirmation": "boolean",
                "requires_midplatform_decision": True,
                "direct_task_state_change_allowed": False,
            },
            "requires_midplatform_decision": True,
            "direct_task_state_change_allowed": False,
            **_not_fact(),
        },
        "command_schema": {
            "schema_version": "voice_dialogue_task_control_command_candidate_schema_v1",
            "schema_only": True,
            "command_types": COMMAND_TYPES,
            "field_definitions": {
                "command_candidate_id": "string",
                "source_intent_candidate_id": "ref",
                "command_type": "enum",
                "target_task_ref": "ref",
                "proposed_task_state": "candidate_state",
                "proposed_context_patch": "object",
                "confirmation_required": "boolean",
                "midplatform_task_manager_required": True,
                "task_state_changed_now": False,
            },
            "midplatform_task_manager_required": True,
            "task_state_changed_now": False,
            **_not_fact(),
        },
        "handoff_policy": {
            "schema_version": "voice_dialogue_to_task_handoff_policy_v1",
            "voice_intent_can_feed_task_context_candidate": True,
            "voice_intent_cannot_mutate_task_state_directly": True,
            "task_manager_must_validate_command": True,
            "midplatform_must_apply_transition_guard": True,
            "confirmation_required_for_cancel": True,
            "confirmation_required_for_high_risk_navigation": True,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "handoff_payload_fields": [
                "intent_candidate",
                "command_candidate",
                "current_task_state_ref",
                "dialogue_context_ref",
                "source_chain",
                "time_anchor",
                "safety_priority_state",
                "confirmation_requirement",
            ],
            **_not_fact(),
        },
        "short_term_context": {
            "schema_version": "voice_dialogue_short_term_context_policy_v1",
            "short_term_context_required": True,
            "used_for": [
                "repeat_last_guidance",
                "continue_task_dialogue",
                "remember_pending_confirmation",
                "prevent_repeated_prompt",
                "preserve_current_task_reference",
            ],
            "memory_scope": "short_term_only",
            "long_term_memory_write_allowed": False,
            "memory_system_invoked_now": False,
            "retention_placeholder": "session_scoped",
            "privacy_sensitivity": "user_dialogue_context",
            **_not_fact(),
        },
        "repeat_pause_resume_cancel": {
            "schema_version": "voice_dialogue_repeat_pause_resume_cancel_policy_v1",
            "repeat_last_guidance_allowed_when_user_asks": True,
            "repeat_blocked_when_safety_alert_active": True,
            "pause_task_requires_active_task": True,
            "resume_task_requires_paused_task": True,
            "cancel_task_requires_confirmation": True,
            "cancel_high_risk_navigation_requires_extra_confirmation": True,
            "state_change_committed_now": False,
            "output_prompt_requires_speech_gate": True,
            **_not_fact(),
        },
        "query_status": {
            "schema_version": "voice_dialogue_query_status_policy_v1",
            "query_status_allowed": True,
            "status_response_must_be_candidate": True,
            "status_response_must_not_expose_internal_debug": True,
            "status_response_should_use_user_safe_language": True,
            "status_response_requires_speech_gate": True,
            "task_status_fact_write_allowed": False,
            **_not_fact(),
        },
        "task_clarification": {
            "schema_version": "voice_dialogue_task_clarification_policy_v1",
            "clarification_required_when_task_missing": True,
            "clarification_required_when_scene_missing": True,
            "clarification_required_when_target_ambiguous": True,
            "clarification_prompt_candidate_allowed": True,
            "user_response_can_feed_task_context_candidate": True,
            "user_response_is_not_fact_by_default": True,
            "clarification_output_requires_speech_gate": True,
            **_not_fact(),
        },
        "safety_priority": {
            "schema_version": "voice_dialogue_safety_priority_suppression_policy_v1",
            "safety_alert_priority_above_dialogue": True,
            "p0_p1_can_interrupt_dialogue": True,
            "dialogue_prompt_suppressed_when_safety_active": True,
            "repeat_prompt_suppressed_when_safety_active": True,
            "task_cancel_confirmation_can_be_delayed_by_safety": True,
            "runtime_arbitration_invoked_now": False,
            **_not_fact(),
        },
        "speech_gate_vop": {
            "schema_version": "voice_dialogue_speech_gate_vop_output_policy_v1",
            "all_dialogue_outputs_require_speech_gate": True,
            "direct_tts_bypass_forbidden": True,
            "direct_vop_bypass_forbidden": True,
            "speech_request_candidate_schema_required": True,
            "vop_submit_allowed_later": True,
            "vop_invoked_now": False,
            "tts_invoked_now": False,
            **_not_fact(),
        },
        "template_matrix": {
            "schema_version": "voice_dialogue_minimal_template_matrix_v1",
            "templates": template_rows,
            "template_count": len(template_rows),
            **_not_fact(),
        },
        "state_machine": {
            "schema_version": "voice_dialogue_state_machine_contract_v1",
            "states": state_rows,
            "state_count": len(state_rows),
            **_not_fact(),
        },
        "future_dryrun": {
            "schema_version": "voice_dialogue_task_control_future_runtime_dryrun_entrypoint_v1",
            "future_runtime_dryrun_entrypoint_defined": True,
            "recommended_next_phase": RECOMMENDED_NEXT,
            "required_before_dryrun": [
                "contract_defined",
                "task_state_policy_available",
                "dialogue_template_matrix_available",
                "speech_gate_policy_available",
                "simulation_profile_available",
            ],
            "dryrun_allowed_later": True,
            "dryrun_invoked_now": False,
            **_not_fact(),
        },
        "midplatform_boundary": {
            "schema_version": "voice_dialogue_midplatform_task_manager_boundary_v1",
            "midplatform_owns_task_state": True,
            "task_manager_owns_task_lifecycle": True,
            "voice_owns_intent_candidate_only": True,
            "voice_cannot_create_task_directly": True,
            "voice_cannot_cancel_task_directly": True,
            "voice_cannot_pause_task_directly": True,
            "voice_cannot_resume_task_directly": True,
            "dialogue_manager_can_hold_pending_confirmation": True,
            "task_transition_guard_required": True,
            **_not_fact(),
        },
        "nav_link": {
            "schema_version": "voice_dialogue_navigation_guidance_link_policy_v1",
            "dialogue_can_request_navigation_guidance_candidate": True,
            "navigation_guidance_requires_task_context": True,
            "navigation_guidance_requires_safety_check": True,
            "navigation_guidance_output_requires_speech_gate": True,
            "dialogue_cannot_trigger_navigation_action_directly": True,
            "basic_navigation_loop_runtime_invoked_now": False,
            **_not_fact(),
        },
        "trace": {
            "schema_version": "voice_dialogue_task_control_decision_trace_v1",
            "steps": trace_steps,
            **_not_fact(),
        },
        "final": {
            "schema_version": "voice_dialogue_task_control_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "contract_defined": True,
            "runtime_invoked_now": False,
            "task_state_changed_now": False,
            "recommended_next_phase": RECOMMENDED_NEXT,
            **_not_fact(),
        },
        "boundary": {
            "schema_version": "voice_dialogue_task_control_boundary_report_v1",
            "contract_only": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
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
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            **_not_fact(),
        },
        "metrics": {
            "schema_version": "voice_dialogue_task_control_metrics_candidate_report_v1",
            "intent_type_count": len(INTENT_TYPES),
            "command_type_count": len(COMMAND_TYPES),
            "dialogue_template_count": len(TEMPLATES),
            "dialogue_state_count": len(DIALOGUE_STATES),
            "policy_defined_count": 8,
            "runtime_action_committed_count": 0,
            "task_state_change_count": 0,
            "tts_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            **_not_fact(),
        },
        "benchmark_link": {
            "schema_version": "voice_dialogue_task_control_benchmark_link_report_v1",
            "benchmark_available": False,
            "current_phase_updates_benchmark_values": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "voice_dialogue_task_control_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_dialogue_task_control_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "contract_only": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "task_state_changed_now": False,
            "tts_invoked": False,
            "voice_output_plane_invoked": False,
            "memory_system_invoked": False,
            "world_model_written": False,
            "scene_delta_written": False,
            "ocr_invoked": False,
            "camera_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "voice_dialogue_task_control_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
        },
        "non_claims": {
            "schema_version": "voice_dialogue_task_control_non_claims_report_v1",
            "claims": [
                "contract_not_runtime",
                "intent_candidate_not_user_fact",
                "command_candidate_not_task_state_change",
                "template_not_real_voice_output",
                "short_term_context_not_memory_write",
                "dialogue_fsm_not_task_manager_runtime",
                "navigation_link_not_navigation_execution",
                "no_asr_llm_tts_vop",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "voice_dialogue_task_control_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "voice_dialogue_task_control_audit_report_v1",
            "voice_dialogue_task_control_contract_v1_executed": True,
            "contract_only": True,
            "voice_dialogue_contract_defined": True,
            "voice_intent_candidate_schema_defined": True,
            "task_control_command_schema_defined": True,
            "dialogue_to_task_handoff_policy_defined": True,
            "short_term_dialogue_context_policy_defined": True,
            "repeat_pause_resume_cancel_policy_defined": True,
            "speech_gate_vop_output_policy_defined": True,
            "future_runtime_dryrun_entrypoint_defined": True,
            "voice_input_runtime_invoked": False,
            "asr_invoked": False,
            "llm_invoked": False,
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
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "benchmark_result_claimed": False,
            "production_readiness_claimed": False,
            "final_decision_recorded": FINAL_DECISION,
        },
    }
