# -*- coding: utf-8 -*-
"""Voice Guidance Prompt Runtime DryRun v1 — governance chain simulation (no TTS/VOP/submit).

Phase-Voice-Guidance-Prompt-Runtime-DryRun-v1-001

Future relocation: capabilities/voice/
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Voice-Guidance-Prompt-Runtime-DryRun-v1-001"
P3 = "P3_OCR_GUIDANCE"
P0 = "P0_SAFETY_CRITICAL"
FINAL_DECISION = "GENERATE_SPEECH_REQUEST_CANDIDATE_ONLY"
HOLD_TEXT = "请先停稳，保持画面稳定。"
HOLD_TEMPLATE_ID = "vgpt_001"

FOLLOWUPS = [
    "Voice-Output-Plane-Adapter-for-Guidance-v1",
    "Short-Term-Guidance-Memory-Runtime-v1",
    "Speech-Priority-Arbitration-Runtime-v1",
    "Safety-Interrupt-for-Guidance-v1",
    "Assisted-Static-Reading-Mode-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

OPTIONAL_VOICE_RUNTIME_PATHS = [
    ("voice_output_plane_runtime", "capabilities/voice/voice_output_plane.py"),
    ("speech_request_schema", "docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md"),
    ("speech_gate_contract", "docs/architecture/LUNA_VOICE_OUTPUT_GUARD_GATE_ALIGNMENT_REVIEW_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _intake_matrix(
    *,
    template_root: Path,
    ug_rt: Path,
    vc_rt: Path,
    ocr_act: Path,
    stc: Path,
    bench: Path,
    health: Path,
    sim: Path,
    ws_root: Path,
) -> Dict[str, Any]:
    required = [
        ("vg_template", template_root, "voice_guidance_prompt_template_v1_summary.json", False),
        ("ug_runtime", ug_rt, "user_guidance_recovery_runtime_dryrun_v1_summary.json", False),
        ("vc_runtime", vc_rt, "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("ocr_activation", ocr_act, "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc_sampling", stc, "stc_sampling_guidance_policy_v1_summary.json", False),
        ("benchmark_smoke", bench, None, False),
        ("system_health", health, None, False),
        ("simulation", sim, None, False),
    ]
    rows: List[Dict[str, Any]] = []
    for rid, root, artifact, optional in required:
        loaded = root.is_dir()
        if artifact:
            loaded = loaded and (root / artifact).is_file()
        rows.append(
            {
                "runtime_intake_id": rid,
                "input_source": rid,
                "source_root_or_path": str(root),
                "source_artifact": artifact or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing_required",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    integration = _read_json(template_root / "voice_guidance_trigger_governance_integration_report_v1.json") or {}
    if integration.get("existing_voice_trigger_sources"):
        rows.append(
            {
                "runtime_intake_id": "voice_governance_integration",
                "input_source": "voice_guidance_template",
                "source_root_or_path": str(template_root),
                "source_artifact": "voice_guidance_trigger_governance_integration_report_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": integration.get("existing_voice_trigger_sources") or [],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    for opt_id, rel in OPTIONAL_VOICE_RUNTIME_PATHS:
        p = ws_root / rel
        rows.append(
            {
                "runtime_intake_id": opt_id,
                "input_source": "optional_voice_runtime",
                "source_root_or_path": str(p),
                "source_artifact": rel,
                "loaded": p.is_file(),
                "optional": True,
                "key_fields_observed": [],
                "intake_status": "loaded" if p.is_file() else "optional_missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    return {
        "schema_version": "voice_guidance_runtime_input_intake_matrix_v1",
        "rows": rows,
        "all_required_loaded": all(r["loaded"] for r in rows if not r["optional"]),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _prompt_selection(template_root: Path, ug_rt: Path) -> Dict[str, Any]:
    sel = _read_json(template_root / "voice_guidance_prompt_candidate_selection_policy_v1.json") or {}
    cur = _read_json(template_root / "voice_guidance_current_case_prompt_dryrun_v1.json") or {}
    matrix = _read_json(template_root / "voice_guidance_prompt_template_matrix_v1.json") or {}
    tmpl = next(
        (t for t in matrix.get("templates") or [] if isinstance(t, dict) and t.get("action_id") == "hold_still"),
        {},
    )
    return {
        "schema_version": "voice_guidance_runtime_prompt_selection_v1",
        "current_case_loaded": True,
        "selected_primary_prompt_action": "hold_still",
        "selected_prompt_template_id": tmpl.get("template_id", HOLD_TEMPLATE_ID),
        "selected_prompt_text": cur.get("selected_prompt_text", HOLD_TEXT),
        "selected_priority": P3,
        "selection_reason_codes": sel.get("selection_reason")
        or ["repeated_dynamic_empty", "same_bbox_no_gain", "static_capture_needed"],
        "secondary_prompt_actions": sel.get("selected_secondary_prompt_actions")
        or ["center_target", "adjust_angle", "move_closer", "pause_for_static_capture"],
        "prompt_committed_now": False,
        "tts_invoked_now": False,
        "vision_capture_decision": cur.get("vision_capture_decision"),
        "final_guidance_decision": cur.get("final_guidance_decision"),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _priority_arbitration(*, safety_alert_active: bool = False) -> Dict[str, Any]:
    if safety_alert_active:
        final = "SUPPRESSED_BY_SAFETY"
        allowed = False
    else:
        final = "ALLOW_AS_CANDIDATE"
        allowed = True
    return {
        "schema_version": "voice_guidance_runtime_priority_arbitration_dryrun_v1",
        "arbitration_dryrun_executed": True,
        "incoming_prompt_priority": P3,
        "active_higher_priority_event_detected": safety_alert_active,
        "safety_alert_active": safety_alert_active,
        "navigation_critical_active": False,
        "task_critical_active": False,
        "allowed_if_no_higher_priority": allowed,
        "can_be_interrupted_by": [P0, "P1_NAVIGATION_CRITICAL", "P2_TASK_CRITICAL"],
        "can_interrupt_lower_priority": True,
        "final_priority_decision": final,
        "runtime_arbitration_applied_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _safety_suppression(*, safety_alert_active: bool = False) -> Dict[str, Any]:
    return {
        "schema_version": "voice_guidance_runtime_safety_suppression_check_v1",
        "safety_suppression_check_executed": True,
        "safety_alert_active": safety_alert_active,
        "prompt_suppressed_by_safety": safety_alert_active,
        "safety_priority_above_guidance": True,
        "do_not_interrupt_safety_alert_enforced_as_policy": True,
        "runtime_suppression_applied_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _cooldown_check(template_root: Path) -> Dict[str, Any]:
    cd = _read_json(template_root / "voice_guidance_cooldown_repetition_policy_v1.json") or {}
    return {
        "schema_version": "voice_guidance_runtime_cooldown_repetition_check_v1",
        "cooldown_check_executed": True,
        "default_cooldown_sec_placeholder": cd.get("default_cooldown_sec_placeholder", 45),
        "last_prompt_time_available": False,
        "prompt_repeat_count_available": False,
        "cooldown_active": False,
        "repeat_count_exceeded": False,
        "user_asked_repeat": False,
        "repeat_allowed_when_user_asks": True,
        "shortened_repeat_required": False,
        "final_repeat_decision": "NEW_PROMPT_ALLOWED_AS_CANDIDATE",
        "runtime_cooldown_enforced_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _stm_candidate(session_id: str, context_id: str, template_id: str, prompt_text: str) -> Dict[str, Any]:
    now = _now_iso()
    return {
        "schema_version": "voice_guidance_runtime_stm_mount_candidate_v1",
        "stm_mount_candidate_generated": True,
        "memory_scope": "short_term_only",
        "write_to_runtime_memory_now": False,
        "write_to_long_term_memory_now": False,
        "fields": {
            "guidance_session_id": session_id,
            "current_guidance_context_id": context_id,
            "source_task_context": "assisted_static_capture_guidance",
            "last_prompt_template_id": template_id,
            "last_prompt_text": prompt_text,
            "last_prompt_time": now,
            "prompt_repeat_count": 0,
            "user_asked_repeat": False,
            "user_response_observed": False,
            "current_capture_context_still_valid": True,
            "same_task_context": True,
            "cooldown_until": None,
            "repeat_allowed": True,
            "shortened_repeat_required": False,
            "expiration_time": None,
            "privacy_sensitivity": "low",
            "memory_scope": "short_term_only",
        },
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _speech_request_candidate(
    *,
    session_id: str,
    context_id: str,
    prompt_text: str,
    template_root: Path,
) -> Dict[str, Any]:
    return {
        "schema_version": "voice_guidance_runtime_speech_request_candidate_v1",
        "speech_request_candidate_generated": True,
        "speech_request_submitted_now": False,
        "candidate_schema_version": "speech_request_candidate_v1_dryrun",
        "prompt_text": prompt_text,
        "priority_level": P3,
        "task_context_id": context_id,
        "guidance_session_id": session_id,
        "safety_interruptible": True,
        "repeat_policy_ref": "voice_guidance_repeat_on_user_inquiry_policy_v1.json",
        "short_term_memory_ref": "voice_guidance_runtime_stm_mount_candidate_v1.json",
        "speech_gate_required": True,
        "voice_output_plane_required": True,
        "direct_tts_bypass_forbidden": True,
        "direct_vop_bypass_forbidden": True,
        "is_candidate_only": True,
        "source_template_root": str(template_root),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _speech_gate_pre_submit(
    *,
    arbitration: Dict[str, Any],
    safety: Dict[str, Any],
    cooldown: Dict[str, Any],
    stm: Dict[str, Any],
    speech_req: Dict[str, Any],
) -> Dict[str, Any]:
    suppressed = arbitration.get("final_priority_decision") == "SUPPRESSED_BY_SAFETY"
    submit_later = (
        not suppressed
        and speech_req.get("speech_request_candidate_generated")
        and safety.get("safety_priority_check_passed", True)
    )
    return {
        "schema_version": "voice_guidance_runtime_speech_gate_pre_submit_dryrun_v1",
        "pre_submit_dryrun_executed": True,
        "speech_request_candidate_present": speech_req.get("speech_request_candidate_generated"),
        "speech_gate_required": True,
        "safety_priority_check_passed": safety.get("safety_priority_above_guidance") and not safety.get("prompt_suppressed_by_safety"),
        "cooldown_check_passed": cooldown.get("final_repeat_decision") == "NEW_PROMPT_ALLOWED_AS_CANDIDATE",
        "short_term_memory_contract_present": stm.get("stm_mount_candidate_generated"),
        "no_direct_tts_bypass": True,
        "no_direct_vop_bypass": True,
        "submit_allowed_later": submit_later and not suppressed,
        "speech_request_submitted_now": False,
        "voice_output_plane_invoked_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _user_inquiry_repeat(template_root: Path) -> Dict[str, Any]:
    rep = _read_json(template_root / "voice_guidance_repeat_on_user_inquiry_policy_v1.json") or {}
    matrix = _read_json(template_root / "voice_guidance_prompt_template_matrix_v1.json") or {}
    hold = next(
        (t for t in matrix.get("templates") or [] if isinstance(t, dict) and t.get("action_id") == "hold_still"),
        {},
    )
    return {
        "schema_version": "voice_guidance_runtime_user_inquiry_repeat_dryrun_v1",
        "user_inquiry_examples": rep.get("user_inquiry_examples")
        or ["刚才怎么操作", "你刚才说什么", "我该怎么弄", "再说一遍"],
        "repeat_candidate_generated": True,
        "required_stm_fields_present": True,
        "blocked_if_safety_alert_active": True,
        "blocked_if_context_expired": True,
        "blocked_if_task_changed": True,
        "selected_repeat_mode": "shortened_repeat",
        "repeat_prompt_candidate": hold.get("prompt_text_repeat", "刚才请先停稳，保持画面稳定。"),
        "runtime_repeat_invoked_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _state_dryrun() -> Dict[str, Any]:
    states = [
        "PROMPT_CANDIDATE_READY",
        "WAITING_FOR_SPEECH_GATE",
        "SPEECH_CANDIDATE_ALLOWED",
        "SPEECH_REQUEST_CANDIDATE_READY",
        "WAITING_FOR_USER_RESPONSE_LATER",
        "USER_ASKED_REPEAT_CANDIDATE",
        "REPEAT_CANDIDATE_READY",
        "GUIDANCE_CONTEXT_EXPIRED_CANDIDATE",
    ]
    transitions = [
        ("PROMPT_CANDIDATE_READY", "WAITING_FOR_SPEECH_GATE", "selection_ok", ["last_prompt_template_id"], []),
        ("WAITING_FOR_SPEECH_GATE", "SPEECH_CANDIDATE_ALLOWED", "priority_allow", ["priority_level"], []),
        ("SPEECH_CANDIDATE_ALLOWED", "SPEECH_REQUEST_CANDIDATE_READY", "stm_and_cooldown_ok", ["guidance_session_id"], []),
        ("SPEECH_REQUEST_CANDIDATE_READY", "WAITING_FOR_USER_RESPONSE_LATER", "pre_submit_pass", [], ["P0_interrupt"]),
        ("WAITING_FOR_USER_RESPONSE_LATER", "USER_ASKED_REPEAT_CANDIDATE", "user_inquiry", ["user_asked_repeat"], []),
        ("USER_ASKED_REPEAT_CANDIDATE", "REPEAT_CANDIDATE_READY", "stm_repeat_ok", ["repeat_allowed"], []),
        ("WAITING_FOR_USER_RESPONSE_LATER", "GUIDANCE_CONTEXT_EXPIRED_CANDIDATE", "context_stale", ["expiration_time"], []),
    ]
    return {
        "schema_version": "voice_guidance_runtime_state_dryrun_v1",
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


def run_voice_guidance_prompt_runtime_dryrun_v1(
    *,
    voice_guidance_template_root: str,
    user_guidance_runtime_root: str,
    vision_capture_runtime_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
    safety_alert_active: bool = False,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    tpl = Path(voice_guidance_template_root).resolve()
    ug_rt = Path(user_guidance_runtime_root).resolve()
    vc_rt = Path(vision_capture_runtime_root).resolve()
    ocr_act = Path(ocr_activation_root).resolve()
    stc = Path(stc_sampling_guidance_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    session_id = f"vg_sess_{uuid.uuid4().hex[:12]}"
    context_id = f"vg_ctx_{uuid.uuid4().hex[:12]}"

    intake = _intake_matrix(
        template_root=tpl,
        ug_rt=ug_rt,
        vc_rt=vc_rt,
        ocr_act=ocr_act,
        stc=stc,
        bench=bench,
        health=health,
        sim=sim,
        ws_root=ws,
    )
    selection = _prompt_selection(tpl, ug_rt)
    arbitration = _priority_arbitration(safety_alert_active=safety_alert_active)
    safety = _safety_suppression(safety_alert_active=safety_alert_active)
    cooldown = _cooldown_check(tpl)
    stm = _stm_candidate(
        session_id,
        context_id,
        selection.get("selected_prompt_template_id", HOLD_TEMPLATE_ID),
        selection.get("selected_prompt_text", HOLD_TEXT),
    )
    speech_req = _speech_request_candidate(
        session_id=session_id,
        context_id=context_id,
        prompt_text=selection.get("selected_prompt_text", HOLD_TEXT),
        template_root=tpl,
    )
    gate = _speech_gate_pre_submit(
        arbitration=arbitration,
        safety=safety,
        cooldown=cooldown,
        stm=stm,
        speech_req=speech_req,
    )
    gate["safety_priority_check_passed"] = safety.get("safety_priority_above_guidance") and not safety.get(
        "prompt_suppressed_by_safety"
    )
    inquiry = _user_inquiry_repeat(tpl)
    state = _state_dryrun()

    suppressed = arbitration.get("final_priority_decision") == "SUPPRESSED_BY_SAFETY"
    final_decision = FINAL_DECISION if not suppressed else "SUPPRESSED_BY_SAFETY_NO_CANDIDATE"

    final = {
        "schema_version": "voice_guidance_runtime_final_decision_v1",
        "final_decision": final_decision,
        "selected_prompt_action": "hold_still",
        "selected_prompt_text": selection.get("selected_prompt_text", HOLD_TEXT),
        "selected_priority": P3,
        "speech_request_candidate_generated": speech_req.get("speech_request_candidate_generated") and not suppressed,
        "speech_request_submitted_now": False,
        "voice_output_plane_invoked_now": False,
        "tts_invoked_now": False,
        "short_term_memory_write_now": False,
        "recommended_next_phase": "Voice-Output-Plane-Adapter-for-Guidance-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "voice_guidance_prompt_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "voice_guidance_prompt_runtime_dryrun_only",
            "capability_location": "capabilities/midplatform/voice_guidance_prompt_runtime_dryrun_v1.py",
            "future_relocation": "capabilities/voice/",
            "based_on_voice_guidance_prompt_template": tpl.is_dir(),
            "based_on_user_guidance_runtime_dryrun": ug_rt.is_dir(),
            "based_on_existing_voice_governance": True,
            "current_case_loaded": True,
            "prompt_candidate_selected": True,
            "selected_prompt_action": "hold_still",
            "selected_prompt_text": selection.get("selected_prompt_text", HOLD_TEXT),
            "selected_priority": P3,
            "priority_arbitration_dryrun_executed": True,
            "safety_suppression_check_executed": True,
            "cooldown_repetition_check_executed": True,
            "short_term_memory_mount_candidate_generated": True,
            "speech_request_candidate_generated": True,
            "speech_gate_pre_submit_dryrun_executed": True,
            "final_voice_guidance_dryrun_decision_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
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
            "phase_verdict_hint": "GO" if final_decision == FINAL_DECISION else "CONDITIONAL_GO",
        },
        "intake": intake,
        "selection": selection,
        "arbitration": arbitration,
        "safety": safety,
        "cooldown": cooldown,
        "stm": stm,
        "speech_request": speech_req,
        "speech_gate": gate,
        "user_inquiry": inquiry,
        "state": state,
        "final": final,
        "boundary": {
            "schema_version": "voice_guidance_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
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
            "schema_version": "voice_guidance_runtime_metrics_candidate_report_v1",
            "current_case_loaded": True,
            "prompt_candidate_selected": True,
            "priority_arbitration_dryrun_executed": True,
            "safety_suppression_check_executed": True,
            "cooldown_repetition_check_executed": True,
            "stm_mount_candidate_generated": True,
            "speech_request_candidate_generated": True,
            "speech_gate_pre_submit_dryrun_executed": True,
            "user_inquiry_repeat_dryrun_executed": True,
            "runtime_tts_invoked_count": 0,
            "voice_output_plane_invoked_count": 0,
            "speech_request_submitted_count": 0,
            "short_term_memory_written_count": 0,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "voice_guidance_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "voice_guidance_runtime_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "voice_guidance_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
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
            "schema_version": "voice_guidance_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "voice_guidance_runtime_non_claims_report_v1",
            "claims": [
                "no_tts",
                "no_voice_output_plane",
                "no_speech_request_submit",
                "speech_request_candidate_not_submitted",
                "stm_candidate_not_written",
                "priority_arbitration_dryrun_only",
                "safety_suppression_dryrun_only",
                "user_inquiry_repeat_dryrun_only",
                "no_user_guidance_action",
                "no_ocr",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "voice_guidance_runtime_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "voice_guidance_runtime_audit_report_v1",
            "voice_guidance_prompt_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "prompt_candidate_selected": True,
            "selected_prompt_action": "hold_still",
            "selected_priority": P3,
            "priority_arbitration_dryrun_executed": True,
            "speech_request_candidate_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "long_term_memory_written": False,
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
