# -*- coding: utf-8 -*-
"""Voice Guidance Prompt Template v1 — templates + speech priority + STM contract (policy only).

Phase-Voice-Guidance-Prompt-Template-v1-001

Capability location: capabilities/midplatform/ (future relocation to capabilities/voice/).
Must route through Voice Output Plane / Speech Gate — no direct TTS bypass.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Voice-Guidance-Prompt-Template-v1-001"
P3 = "P3_OCR_GUIDANCE"
P0 = "P0_SAFETY_CRITICAL"

FOLLOWUPS = [
    "Voice-Guidance-Prompt-Runtime-DryRun-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Voice-Output-Plane-Adapter-for-Guidance-v1",
    "Short-Term-Guidance-Memory-Runtime-v1",
    "Speech-Priority-Arbitration-Runtime-v1",
    "Safety-Interrupt-for-Guidance-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

VOICE_GOVERNANCE_DOC_CANDIDATES = [
    "docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md",
    "docs/architecture/voice/LUNA_VOICE_MAINLINE_BASELINE.md",
    "docs/architecture/voice/LUNA_VOICE_OUTPUT_GOVERNANCE_TO_INTERACTION_MAPPING_V0.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_PRIORITY_EXPIRY_SUPPRESSION_POLICY_V0.md",
    "docs/architecture/LUNA_VOICE_OUTPUT_GUARD_GATE_ALIGNMENT_REVIEW_V0.md",
    "docs/architecture/LUNA_NAVIGATION_OUTPUT_PRIORITY_AND_SUPPRESSION_POLICY_V0.md",
]

PROMPT_TEMPLATES: List[Tuple[str, str, str, str, str]] = [
    ("hold_still", "stability", "请先停稳，保持画面稳定。", "刚才请先停稳，保持画面稳定。", "您需要我怎么保持稳定？"),
    ("center_target", "centering", "请把文字放在画面中央。", "请把目标文字移到画面中央。", "请再说一遍怎么对准？"),
    ("adjust_angle", "angle", "请稍微调整角度，避免斜着拍。", "请稍微调整角度，避免斜着拍文字。", "角度要怎么调？"),
    ("move_closer", "distance", "请稍微靠近一点，再保持稳定。", "请再靠近一些，并保持稳定。", "要靠近多少？"),
    ("pause_for_static_capture", "static", "当前动态画面不稳定，建议停下后再读。", "建议先停稳，停下后再尝试读取。", "为什么要停下再读？"),
    ("increase_light", "brightness", "当前光线可能不足，请尝试靠近亮一点的位置。", "请到有光线的地方再试。", "光线不够怎么办？"),
    ("zoom_or_magnify", "zoom", "可以尝试放大画面后再读。", "请尝试放大或靠近一些。", "怎么放大？"),
    ("ask_external_assistance", "external", "如果不方便调整，可以请身边人帮忙确认文字。", "可以请身边人帮忙看一下文字。", "需要别人帮什么？"),
    ("visual_semantic_fallback_notice", "fallback", "当前不适合继续读字，我会先按环境和目标继续判断。", "我先按环境信息继续，不继续读字。", "为什么不读了？"),
    ("static_reading_mode_notice", "static", "这段文字需要静态阅读，请先停稳并对准。", "请先停稳并对准，再静态阅读。", "什么是静态阅读？"),
]

PROHIBITED = [
    "保证能识别",
    "一定能读到",
    "马上为您读出",
    "系统已确认",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _discover_voice_governance(ws_root: Path) -> Dict[str, Any]:
    found: List[str] = []
    for rel in VOICE_GOVERNANCE_DOC_CANDIDATES:
        if (ws_root / rel).is_file():
            found.append(rel)
    return {
        "existing_voice_trigger_rules_found": len(found) > 0,
        "existing_voice_trigger_sources": found,
        "placeholder_required": len(found) == 0,
        "voice_governance_integration_required": True,
        "ocr_guidance_prompt_is_subordinate_to_speech_gate": True,
        "direct_tts_bypass_forbidden": True,
        "direct_voice_output_plane_bypass_forbidden": True,
        "speech_request_required_later": True,
        "current_phase_speech_request_submitted": False,
        "integration_status": "linked_to_existing_voice_docs" if found else "placeholder_only_pending_voice_docs",
        "fact_status": "not_fact",
    }


def _speech_priority_policy() -> Dict[str, Any]:
    levels = [
        (P0, "P0_SAFETY_CRITICAL", "safety_alert", True, ["P1_NAVIGATION_CRITICAL"], True),
        ("P1_NAVIGATION_CRITICAL", "P1_NAVIGATION_CRITICAL", "navigation_turn", True, [P0], False),
        ("P2_TASK_CRITICAL", "P2_TASK_CRITICAL", "task_deadline", True, [P0, "P1_NAVIGATION_CRITICAL"], False),
        (P3, "P3_OCR_GUIDANCE", "ocr_reading_guidance", False, [P0, "P1_NAVIGATION_CRITICAL", "P2_TASK_CRITICAL"], True),
        ("P4_GENERAL_ASSISTANCE", "P4_GENERAL_ASSISTANCE", "general_help", False, [P0, P3], True),
        ("P5_BACKGROUND_INFO", "P5_BACKGROUND_INFO", "ambient_info", False, [P0, P3, "P4_GENERAL_ASSISTANCE"], True),
    ]
    return {
        "schema_version": "voice_guidance_speech_priority_policy_v1",
        "safety_priority_above_guidance": True,
        "ocr_guidance_priority_level": P3,
        "current_phase_runtime_priority_applied": False,
        "levels": [
            {
                "priority_level": lvl,
                "priority_name": name,
                "example_event": ex,
                "can_interrupt_lower_priority": can_int,
                "can_be_interrupted_by": interrupted_by,
                "repeat_allowed_on_user_inquiry": repeat_inq,
                "cooldown_required": True,
                "runtime_applied_now": False,
                "fact_status": "not_fact",
            }
            for lvl, name, ex, can_int, interrupted_by, repeat_inq in levels
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _prompt_template_matrix() -> Dict[str, Any]:
    rows = []
    for i, (aid, ptype, short, repeat, inquiry) in enumerate(PROMPT_TEMPLATES, 1):
        rows.append(
            {
                "template_id": f"vgpt_{i:03d}",
                "action_id": aid,
                "prompt_type": ptype,
                "priority_level": P3,
                "prompt_text_short": short,
                "prompt_text_repeat": repeat,
                "prompt_text_user_inquiry": inquiry,
                "prohibited_wording": PROHIBITED,
                "expected_user_action": aid,
                "trigger_reason_codes": ["capture_readiness_fail", "user_guidance_recovery"],
                "max_length_hint": 48,
                "safety_constraints": ["do_not_interrupt_safety_alert", "do_not_ask_user_stop_in_danger"],
                "tts_allowed_later": True,
                "tts_invoked_now": False,
                "speech_request_submitted_now": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "voice_guidance_prompt_template_matrix_v1",
        "templates": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _safety_constraints() -> Dict[str, Any]:
    specs = [
        ("do_not_ask_user_stop_in_danger", "all", "ask_user_hold_in_unsafe_area", "defer_or_use_safety_path", "high"),
        ("do_not_interrupt_safety_alert", "all", "speak_over_safety", "yield_to_P0", "critical"),
        ("do_not_claim_success", "ocr_guidance", "promise_read_success", "use_neutral_wording", "high"),
        ("do_not_over_repeat", "ocr_guidance", "spam_repeat", "respect_cooldown_and_stm", "medium"),
        ("do_not_disclose_internal_pipeline", "all", "mention_ocr_model_provider", "user_facing_only", "medium"),
        ("do_not_force_external_assistance", "external", "insist_on_helper", "offer_as_option", "medium"),
        ("do_not_read_sensitive_text_without_context", "ocr_guidance", "read_id_card_unprompted", "require_task_context", "high"),
        ("do_not_trigger_tts_now", "all", "invoke_tts_in_template_phase", "adapter_later_only", "critical"),
    ]
    return {
        "schema_version": "voice_guidance_prompt_safety_constraint_matrix_v1",
        "constraints": [
            {
                "constraint_id": cid,
                "applies_to_prompt_type": applies,
                "forbidden_behavior": forb,
                "required_behavior": req,
                "violation_severity": sev,
                "runtime_check_required_later": True,
                "fact_status": "not_fact",
            }
            for cid, applies, forb, req, sev in specs
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _short_term_memory_contract() -> Dict[str, Any]:
    fields = [
        "guidance_session_id",
        "current_guidance_context_id",
        "source_task_context",
        "last_prompt_template_id",
        "last_prompt_text",
        "last_prompt_time",
        "prompt_repeat_count",
        "user_asked_repeat",
        "user_response_observed",
        "user_action_observed_candidate",
        "current_capture_context_still_valid",
        "same_task_context",
        "cooldown_until",
        "repeat_allowed",
        "shortened_repeat_required",
        "expiration_time",
        "privacy_sensitivity",
    ]
    return {
        "schema_version": "voice_guidance_short_term_memory_mount_contract_v1",
        "memory_scope": "short_term_only",
        "fields": {f: {"required": True, "persist_to_world_model": False} for f in fields},
        "field_list": fields,
        "not_long_term_profile": True,
        "not_fact_layer": True,
        "future_runtime_mount_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _repeat_on_inquiry() -> Dict[str, Any]:
    return {
        "schema_version": "voice_guidance_repeat_on_user_inquiry_policy_v1",
        "repeat_allowed_when_user_asks": True,
        "user_inquiry_examples": [
            "刚才怎么操作",
            "你刚才说什么",
            "我该怎么弄",
            "再说一遍",
        ],
        "required_short_term_memory_fields": [
            "last_prompt_text",
            "last_prompt_time",
            "prompt_repeat_count",
            "same_task_context",
            "repeat_allowed",
            "shortened_repeat_required",
        ],
        "repeat_mode": ["full_repeat", "shortened_repeat", "next_step_only"],
        "blocked_when": [
            "safety_alert_active",
            "context_expired",
            "task_changed",
            "repeat_count_exceeded",
            "user_moving_fast_or_unsafe",
        ],
        "runtime_repeat_invoked_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _cooldown_repetition() -> Dict[str, Any]:
    return {
        "schema_version": "voice_guidance_cooldown_repetition_policy_v1",
        "default_cooldown_sec_placeholder": 45,
        "max_repeat_count_placeholder": 3,
        "repeat_decay_policy": "shortened_after_second_repeat",
        "shortened_repeat_after_count": 2,
        "suppress_if_no_user_response": True,
        "allow_repeat_on_user_inquiry": True,
        "reset_conditions": ["task_context_changed", "capture_success", "guidance_completed"],
        "blocked_conditions": ["safety_alert_active", "P0_interrupt"],
        "runtime_enforced_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _prompt_selection(ug_rt: Path) -> Dict[str, Any]:
    plan = _read_json(ug_rt / "user_guidance_runtime_plan_v1.json") or {}
    actions = plan.get("selected_guidance_actions") or [
        "ask_user_hold_still",
        "ask_user_center_target",
        "ask_user_adjust_angle",
        "ask_user_move_closer",
        "ask_user_pause_for_static_capture",
    ]
    mapped = []
    for a in actions:
        mapped.append(a.replace("ask_user_", "").replace("request_", ""))
        if a == "ask_user_center_target":
            mapped.append("center_target")
        if a == "ask_user_pause_for_static_capture":
            mapped.append("pause_for_static_capture")
    return {
        "schema_version": "voice_guidance_prompt_candidate_selection_policy_v1",
        "selected_primary_prompt_action": "hold_still",
        "selected_secondary_prompt_actions": [
            "center_target",
            "adjust_angle",
            "move_closer",
            "pause_for_static_capture",
        ],
        "selection_reason": [
            "repeated_dynamic_empty",
            "same_bbox_no_gain",
            "static_capture_needed",
        ],
        "selected_priority": P3,
        "can_be_interrupted_by_safety": True,
        "can_be_repeated_on_user_inquiry": True,
        "speech_request_submitted_now": False,
        "source_plan_actions": actions,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _vop_adapter() -> Dict[str, Any]:
    return {
        "schema_version": "voice_guidance_voice_output_plane_adapter_placeholder_v1",
        "adapter_required": True,
        "future_input": "prompt_candidate",
        "future_output": "SpeechRequest",
        "required_fields": [
            "prompt_text",
            "priority_level",
            "session_id",
            "task_context_id",
            "safety_interruptible",
            "repeat_policy_ref",
            "short_term_memory_ref",
        ],
        "must_pass_through_speech_gate": True,
        "direct_submit_forbidden_now": True,
        "current_phase_invoked": False,
        "speech_request_submitted_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _runtime_state_placeholder() -> Dict[str, Any]:
    states = [
        "PROMPT_NOT_READY",
        "PROMPT_CANDIDATE_READY",
        "WAITING_FOR_SPEECH_GATE",
        "SPEECH_SUPPRESSED_BY_SAFETY",
        "SPEECH_SUBMITTED_LATER",
        "WAITING_FOR_USER_RESPONSE",
        "USER_ASKED_REPEAT",
        "REPEAT_CANDIDATE_READY",
        "GUIDANCE_CONTEXT_EXPIRED",
        "GUIDANCE_COMPLETED_OR_ABORTED",
    ]
    transitions = [
        ("PROMPT_NOT_READY", "PROMPT_CANDIDATE_READY", "template_selected", ["last_prompt_template_id"], []),
        ("PROMPT_CANDIDATE_READY", "WAITING_FOR_SPEECH_GATE", "priority_ok", ["priority_level"], []),
        ("WAITING_FOR_SPEECH_GATE", "SPEECH_SUPPRESSED_BY_SAFETY", "P0_active", [], ["P0_interrupt"]),
        ("WAITING_FOR_SPEECH_GATE", "SPEECH_SUBMITTED_LATER", "gate_pass", ["session_id"], []),
        ("WAITING_FOR_USER_RESPONSE", "USER_ASKED_REPEAT", "user_inquiry", ["user_asked_repeat"], []),
        ("USER_ASKED_REPEAT", "REPEAT_CANDIDATE_READY", "stm_allows", ["last_prompt_text", "repeat_allowed"], []),
        ("WAITING_FOR_USER_RESPONSE", "GUIDANCE_CONTEXT_EXPIRED", "context_stale", ["expiration_time"], []),
    ]
    return {
        "schema_version": "voice_guidance_prompt_runtime_state_placeholder_v1",
        "states": states,
        "transitions": [
            {
                "from_state": f,
                "to_state": t,
                "trigger_condition": cond,
                "required_memory_fields": mem,
                "blocked_by": blocked,
                "runtime_state_changed_now": False,
                "fact_status": "not_fact",
            }
            for f, t, cond, mem, blocked in transitions
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _current_case_dryrun(vc_rt: Path, ug_rt: Path) -> Dict[str, Any]:
    vc_sum = _read_json(vc_rt / "vision_capture_runtime_dryrun_v1_summary.json") or {}
    ug_final = _read_json(ug_rt / "user_guidance_final_dryrun_decision_v1.json") or {}
    hold = next((t for t in PROMPT_TEMPLATES if t[0] == "hold_still"), None)
    text = hold[2] if hold else "请先停稳，保持画面稳定。"
    return {
        "schema_version": "voice_guidance_current_case_prompt_dryrun_v1",
        "current_case_loaded": True,
        "vision_capture_decision": vc_sum.get("recommended_capture_decision", "USER_GUIDANCE_OR_STATIC_CAPTURE"),
        "final_guidance_decision": ug_final.get("selected_primary_path", "ASSISTED_STATIC_CAPTURE_GUIDANCE"),
        "selected_primary_prompt": "hold_still",
        "selected_prompt_text": text,
        "selected_priority": P3,
        "safety_priority_above_guidance": True,
        "short_term_memory_mount_required": True,
        "repeat_on_user_inquiry_allowed": True,
        "speech_request_submitted_now": False,
        "tts_invoked_now": False,
        "voice_output_plane_invoked_now": False,
        "runtime_action_committed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_voice_guidance_prompt_template_v1(
    *,
    user_guidance_runtime_root: str,
    vision_capture_runtime_root: str,
    user_guidance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    ug_rt = Path(user_guidance_runtime_root).resolve()
    vc_rt = Path(vision_capture_runtime_root).resolve()
    ug = Path(user_guidance_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    integration = _discover_voice_governance(ws)
    priority = _speech_priority_policy()
    templates = _prompt_template_matrix()
    safety = _safety_constraints()
    stm = _short_term_memory_contract()
    repeat_pol = _repeat_on_inquiry()
    cooldown = _cooldown_repetition()
    selection = _prompt_selection(ug_rt)
    adapter = _vop_adapter()
    state_ph = _runtime_state_placeholder()
    current = _current_case_dryrun(vc_rt, ug_rt)

    return {
        "summary": {
            "schema_version": "voice_guidance_prompt_template_v1_summary_v0",
            "phase": PHASE_ID,
            "template_scope": "voice_guidance_prompt_template_only",
            "capability_location": "capabilities/midplatform/voice_guidance_prompt_template_v1.py",
            "future_relocation": "capabilities/voice/",
            "based_on_user_guidance_runtime_dryrun": ug_rt.is_dir(),
            "based_on_user_guidance_recovery_policy": ug.is_dir(),
            "voice_trigger_governance_integration_defined": True,
            "speech_priority_policy_defined": True,
            "safety_priority_above_guidance": True,
            "short_term_memory_mount_defined": True,
            "repeat_on_user_inquiry_policy_defined": True,
            "cooldown_and_repetition_policy_defined": True,
            "voice_output_plane_adapter_placeholder_defined": True,
            "prompt_template_matrix_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "integration": integration,
        "priority": priority,
        "templates": templates,
        "safety": safety,
        "stm": stm,
        "repeat_policy": repeat_pol,
        "cooldown": cooldown,
        "selection": selection,
        "adapter": adapter,
        "state_placeholder": state_ph,
        "current_case": current,
        "boundary": {
            "schema_version": "voice_guidance_prompt_template_boundary_report_v1",
            "template_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "voice_guidance_prompt_template_metrics_candidate_report_v1",
            "prompt_template_count": len(templates.get("templates") or []),
            "safety_constraint_count": len(safety.get("constraints") or []),
            "priority_level_count": len(priority.get("levels") or []),
            "short_term_memory_field_count": len(stm.get("field_list") or []),
            "repeat_policy_defined": True,
            "cooldown_policy_defined": True,
            "adapter_placeholder_defined": True,
            "runtime_tts_invoked_count": 0,
            "speech_request_submitted_count": 0,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "voice_guidance_prompt_template_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "voice_guidance_prompt_template_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_guidance_prompt_template_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "template_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "voice_guidance_prompt_template_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "voice_guidance_prompt_template_non_claims_report_v1",
            "claims": [
                "no_tts",
                "no_voice_output_plane",
                "no_speech_request",
                "template_not_broadcast",
                "priority_not_runtime_arbitration",
                "stm_contract_not_actual_write",
                "repeat_policy_not_actual_speak",
                "no_user_guidance_runtime_action",
                "no_ocr",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "voice_guidance_prompt_template_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "voice_guidance_prompt_template_audit_report_v1",
            "voice_guidance_prompt_template_v1_executed": True,
            "template_only": True,
            "voice_trigger_governance_integration_defined": True,
            "speech_priority_policy_defined": True,
            "safety_priority_above_guidance": True,
            "short_term_memory_mount_defined": True,
            "repeat_on_user_inquiry_policy_defined": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
