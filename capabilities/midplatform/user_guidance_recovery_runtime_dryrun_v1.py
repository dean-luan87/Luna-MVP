# -*- coding: utf-8 -*-
"""User Guidance Recovery Runtime DryRun v1 — guidance plan / prompts (no TTS/hardware/OCR).

Phase-User-Guidance-Recovery-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "User-Guidance-Recovery-Runtime-DryRun-v1-001"
VISION_CAPTURE_DECISION = "USER_GUIDANCE_OR_STATIC_CAPTURE"
PRIMARY_PATH = "ASSISTED_STATIC_CAPTURE_GUIDANCE"

FOLLOWUPS = [
    "Voice-Guidance-Prompt-Template-v1",
    "Assisted-Static-Reading-Mode-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCR-Activation-Runtime-DryRun-v1",
    "STC-Freshness-Gate-Runtime-DryRun-v1",
    "Expired-Observation-Candidate-Ingest-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

CANDIDATE_METADATA = [
    "source_chain",
    "time_anchor",
    "spatial_anchor",
    "original_task_context",
    "stale_reason",
    "confidence_decay",
    "privacy_sensitivity",
    "future_usage_scope",
]

PROMPT_TEMPLATES = [
    ("ask_user_hold_still", "stability", "请先停稳，把文字放在画面中央。", "hold_still", 1),
    ("ask_user_center_target", "centering", "请将目标文字移到画面中央。", "center_target", 2),
    ("ask_user_adjust_angle", "angle", "请调整角度，避免斜着拍文字。", "adjust_angle", 3),
    ("ask_user_move_closer", "distance", "请稍微靠近一点，并保持画面稳定。", "move_closer", 4),
    ("ask_user_pause_for_static_capture", "static", "当前动态画面无法稳定读取，建议停下后再读。", "pause_static", 5),
    ("request_external_assistance_if_needed", "external", "如果不方便调整，请让身边人帮忙确认文字。", "external_help", 6),
]

STATES = [
    "GUIDANCE_NOT_STARTED",
    "GUIDANCE_PROMPT_CANDIDATE_READY",
    "WAITING_FOR_USER_ACTION",
    "USER_ACTION_OBSERVED_CANDIDATE",
    "CAPTURE_RETRY_CANDIDATE",
    "STATIC_CAPTURE_CANDIDATE",
    "SYSTEM_SELF_ADJUSTMENT_CANDIDATE",
    "EXTERNAL_ASSISTANCE_CANDIDATE",
    "VISUAL_SEMANTIC_FALLBACK_CANDIDATE",
    "STOP_OCR_RETRY",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _pick_keys(obj: Any, keys: List[str]) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    return {k: obj[k] for k in keys if k in obj}


def _intake(iid: str, root: Path, artifact: str, keys: List[str]) -> Dict[str, Any]:
    data = _read_json(root / artifact)
    loaded = data is not None
    return {
        "runtime_intake_id": iid,
        "input_source": iid,
        "source_root": str(root),
        "source_artifact": artifact,
        "loaded": loaded,
        "key_fields_observed": _pick_keys(data, keys) if loaded else {},
        "intake_status": "loaded" if loaded else "missing",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _load_case(vc_runtime: Path, ug_root: Path) -> Dict[str, Any]:
    vc_sum = _read_json(vc_runtime / "vision_capture_runtime_dryrun_v1_summary.json") or {}
    vc_final = _read_json(vc_runtime / "vision_capture_runtime_decision_matrix_v1.json") or {}
    ug_case = _read_json(ug_root / "user_guidance_current_case_recovery_decision_v1.json") or {}
    return {
        "vision_capture_decision": vc_sum.get("recommended_capture_decision", VISION_CAPTURE_DECISION),
        "internal_recrop_should_stop": bool(vc_sum.get("internal_recrop_should_stop", True)),
        "dynamic_reocr_allowed_now": bool(vc_sum.get("dynamic_reocr_allowed_now", False)),
        "v1_empty_count": int(ug_case.get("v1_empty_count") or 30),
        "v2_empty_count": int(ug_case.get("v2_empty_count") or 5),
        "same_bbox_risk_count": int(ug_case.get("same_bbox_risk_count") or 5),
        "user_guidance_recovery_recommended": bool(ug_case.get("user_guidance_recovery_recommended", True)),
        "capture_matrix_loaded": bool(vc_final),
    }


def _trigger_matrix(case: Dict[str, Any]) -> Dict[str, Any]:
    triggers = [
        ("repeated_dynamic_empty", "v1_v2_empty", "ask_user_pause_for_static_capture", "static_capture_entry", True),
        ("same_bbox_no_gain", "same_bbox_risk_count", "ask_user_center_target", "system_self_adjustment", True),
        ("capture_quality_problem_likely", "capture_quality", "ask_user_increase_light", "request_exposure", True),
        ("projection_or_region_alignment_problem_likely", "projection_drift", "ask_user_adjust_angle", "static_capture", True),
        ("text_region_not_detected", "no_detected_text_region", "ask_user_pause_for_static_capture", "heavy_detector_placeholder", True),
        ("internal_retry_limit_reached", "internal_recrop_should_stop", "ask_user_hold_still", "STOP_OCR_RETRY", True),
        ("static_capture_needed", "USER_GUIDANCE_OR_STATIC_CAPTURE", "ask_user_pause_for_static_capture", "static_capture_entry", True),
        ("user_action_required", "readiness_fail", "ask_user_move_closer", "WAITING_FOR_USER_ACTION", True),
    ]
    rows = []
    pri = 1
    for tid, sig, action, esc, default_active in triggers:
        active = default_active
        if tid == "capture_quality_problem_likely":
            active = True
        if tid in ("repeated_dynamic_empty", "same_bbox_no_gain", "internal_retry_limit_reached", "static_capture_needed"):
            active = True
        rows.append(
            {
                "trigger_id": tid,
                "trigger_reason": tid,
                "observed_signal": sig,
                "active": active,
                "priority": pri,
                "recommended_guidance_action": action,
                "recommended_escalation": esc,
                "action_committed_now": False,
                "fact_status": "not_fact",
            }
        )
        pri += 1
    return {
        "schema_version": "user_guidance_trigger_evaluation_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _guidance_plan() -> Dict[str, Any]:
    actions = [
        "ask_user_hold_still",
        "ask_user_center_target",
        "ask_user_adjust_angle",
        "ask_user_move_closer",
        "ask_user_pause_for_static_capture",
    ]
    return {
        "schema_version": "user_guidance_runtime_plan_v1",
        "guidance_plan_id": "ug_runtime_plan_current_case_v1",
        "plan_status": "dryrun_candidate",
        "primary_goal": "improve_capture_condition_for_static_or_short_text_reading",
        "target_mode": "assisted_static_capture_or_user_guided_short_text",
        "selected_guidance_actions": actions,
        "action_order": actions,
        "stop_conditions": [
            "unsafe_to_continue",
            "user_declines_guidance",
            "static_capture_quality_pass",
        ],
        "escalation_conditions": [
            "repeated_guidance_no_improvement",
            "user_unable_to_adjust",
        ],
        "fallback_paths": [
            "VISUAL_SEMANTIC_FALLBACK_CANDIDATE",
            "EXTERNAL_ASSISTANCE_CANDIDATE",
            "EXPIRED_LONG_TERM_CONTEXT_CANDIDATE",
        ],
        "tts_allowed_now": False,
        "voice_output_plane_allowed_now": False,
        "runtime_action_committed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _prompt_matrix() -> Dict[str, Any]:
    rows = []
    for i, (aid, ptype, text, trigger, pri) in enumerate(PROMPT_TEMPLATES, 1):
        rows.append(
            {
                "prompt_candidate_id": f"prompt_{i:03d}",
                "action_id": aid,
                "prompt_type": ptype,
                "prompt_text_candidate": text,
                "trigger_reason": trigger,
                "priority": pri,
                "expected_user_action": aid.replace("ask_user_", "").replace("request_", ""),
                "expected_signal_improvement": ptype,
                "safety_risk_level": "low" if "external" not in aid else "medium",
                "user_effort_level": "medium" if "static" in aid or "external" in aid else "low",
                "speech_allowed_later": True,
                "tts_invoked_now": False,
                "voice_output_plane_invoked_now": False,
                "prompt_committed_now": False,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "user_guidance_prompt_candidate_matrix_v1",
        "rows": rows,
        "reuse_by_voice_guidance_prompt_template_v1": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _state_transitions() -> Dict[str, Any]:
    transitions = [
        ("GUIDANCE_NOT_STARTED", "GUIDANCE_PROMPT_CANDIDATE_READY", "plan_built", [], ["tts_invoke"]),
        ("GUIDANCE_PROMPT_CANDIDATE_READY", "WAITING_FOR_USER_ACTION", "prompts_ready", [], ["tts_invoke"]),
        ("WAITING_FOR_USER_ACTION", "USER_ACTION_OBSERVED_CANDIDATE", "user_adjusted_simulated", [], []),
        ("USER_ACTION_OBSERVED_CANDIDATE", "CAPTURE_RETRY_CANDIDATE", "retry_allowed_if_not_stopped", [], ["internal_recrop"]),
        ("CAPTURE_RETRY_CANDIDATE", "STOP_OCR_RETRY", "internal_recrop_should_stop", [], ["dynamic_reocr"]),
        ("WAITING_FOR_USER_ACTION", "STATIC_CAPTURE_CANDIDATE", "static_capture_needed", [], []),
        ("STATIC_CAPTURE_CANDIDATE", "SYSTEM_SELF_ADJUSTMENT_CANDIDATE", "hardware_placeholder", [], ["hardware_invoke"]),
        ("WAITING_FOR_USER_ACTION", "EXTERNAL_ASSISTANCE_CANDIDATE", "user_unable", [], []),
        ("STOP_OCR_RETRY", "VISUAL_SEMANTIC_FALLBACK_CANDIDATE", "ocr_path_exhausted", [], ["ocr_invoke"]),
    ]
    return {
        "schema_version": "user_guidance_response_state_transition_dryrun_v1",
        "states": STATES,
        "transitions": [
            {
                "from_state": f,
                "to_state": t,
                "trigger_condition": cond,
                "required_signal": req,
                "allowed_next_action": ["dryrun_advance"],
                "blocked_action": blocked,
                "runtime_state_changed_now": False,
                "fact_status": "not_fact",
            }
            for f, t, cond, req, blocked in transitions
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _static_capture_entry() -> Dict[str, Any]:
    return {
        "schema_version": "user_guidance_static_capture_entry_candidate_v1",
        "static_capture_entry_candidate_generated": True,
        "entry_reason": [
            "repeated_dynamic_empty",
            "same_bbox_no_gain",
            "text_region_not_detected",
            "task_critical_or_user_requested",
        ],
        "required_user_state": "stationary_or_slow_approach",
        "required_capture_condition": "high_resolution_still_low_motion_centered",
        "suggested_guidance_actions": [
            "ask_user_hold_still",
            "ask_user_center_target",
            "ask_user_pause_for_static_capture",
        ],
        "expected_next_phase": "Assisted-Static-Reading-Mode-v1",
        "runtime_capture_invoked": False,
        "tts_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _system_escalation(vc_runtime: Path) -> Dict[str, Any]:
    pol = _read_json(vc_runtime / "vision_capture_runtime_system_self_adjustment_candidate_v1.json") or {}
    out = []
    pri = 1
    for a in pol.get("candidates") or []:
        if not isinstance(a, dict):
            continue
        out.append(
            {
                "action_id": a.get("action_id"),
                "trigger_reason": a.get("trigger_reason"),
                "required_hardware_capability": a.get("required_hardware_capability"),
                "hardware_capability_known": a.get("hardware_capability_known", False),
                "expected_signal_improvement": a.get("expected_signal_improvement"),
                "escalation_priority": pri,
                "hardware_action_invoked_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
        )
        pri += 1
    return {
        "schema_version": "user_guidance_system_self_adjustment_escalation_candidate_v1",
        "candidates": out,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _external_escalation() -> Dict[str, Any]:
    specs = [
        ("request_nearby_person_adjust_angle", "user_unable_angle", "safe_public_setting", "请身边人帮忙调整拍摄角度。", 1),
        ("request_nearby_person_read_short_text", "static_failed", "user_consent_required", "请身边人帮忙看一下这段文字。", 2),
        ("request_staff_confirm_location", "facility_navigation", "staff_available", "可向工作人员确认位置信息。", 3),
        ("request_user_manual_input", "ocr_exhausted", "privacy_ok", "您也可以手动输入需要确认的文字。", 4),
    ]
    return {
        "schema_version": "user_guidance_external_assistance_escalation_candidate_v1",
        "candidates": [
            {
                "action_id": aid,
                "trigger_reason": reason,
                "when_allowed": reason,
                "privacy_safety_considerations": privacy_safety,
                "prompt_candidate": prompt_candidate,
                "escalation_priority": pri,
                "action_committed_now": False,
                "fact_status": "not_fact",
            }
            for aid, reason, privacy_safety, prompt_candidate, pri in specs
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _visual_fallback(vc_runtime: Path) -> Dict[str, Any]:
    pol = _read_json(vc_runtime / "vision_capture_runtime_visual_semantic_fallback_v1.json") or {}
    return {
        "schema_version": "user_guidance_visual_semantic_fallback_candidate_v1",
        "visual_semantic_fallback_allowed": bool(pol.get("return_to_visual_semantic_path_allowed", True)),
        "ocr_default_off_for_world_modeling_respected": bool(
            pol.get("ocr_default_off_for_world_modeling_respected", True)
        ),
        "fallback_reason": pol.get("fallback_reason", "ocr_capture_guidance_exhausted"),
        "allowed_paths": pol.get("allowed_paths")
        or [
            "visual_symbol",
            "logo_candidate",
            "public_facility_semantic",
            "spatial_structure",
            "poi_hint",
            "route_context",
            "task_context",
        ],
        "blocked_paths": ["dynamic_reocr", "internal_recrop_loop"],
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _expired_long_term() -> Dict[str, Any]:
    types = [
        ("expired_guidance_attempt_candidate", "guidance_retry_exhausted"),
        ("repeated_unreadable_region_candidate", "same_bbox_no_gain"),
        ("user_environment_context_candidate", "capture_context_recurring"),
        ("user_profile_context_candidate", "task_habit_hint"),
        ("emotional_context_background_candidate", "stressful_reading_context"),
    ]
    meta = {k: True for k in CANDIDATE_METADATA}
    return {
        "schema_version": "user_guidance_expired_long_term_context_candidate_v1",
        "candidates": [
            {
                "candidate_type": t,
                "source_signal": sig,
                "cannot_use_for_action": True,
                "cannot_write_fact": True,
                "can_feed_long_term_candidate": True,
                "required_metadata": CANDIDATE_METADATA,
                **meta,
                "write_allowed_now": False,
                "fact_status": "not_fact",
            }
            for t, sig in types
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _decision_trace(case: Dict[str, Any]) -> Dict[str, Any]:
    def step(sid: int, name: str, decision: str, reasons: List[str], allowed: List[str], blocked: List[str]) -> Dict[str, Any]:
        return {
            "step_id": sid,
            "step_name": name,
            "input_refs": ["vision_capture_runtime_dryrun"],
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
            "fact_status": "not_fact",
        }

    steps = [
        step(1, "load_vision_capture_runtime_decision", case["vision_capture_decision"], ["vc_runtime_summary"], ["evaluate_triggers"], []),
        step(2, "load_user_guidance_policy", "policy_loaded", ["ug_policy_v1"], ["build_plan"], []),
        step(3, "evaluate_guidance_triggers", "triggers_active", ["repeated_empty", "same_bbox", "retry_limit"], ["build_plan"], []),
        step(4, "build_guidance_plan", PRIMARY_PATH, ["static_or_guided_short_text"], ["tts"], ["hardware"]),
        step(5, "build_prompt_candidates", "prompts_ready", ["short_non_promissory"], ["voice_template_v1"], ["tts_now"]),
        step(6, "build_response_state_transitions", "fsm_dryrun", [], ["simulate_only"], ["real_user_response"]),
        step(7, "evaluate_static_capture_entry", "static_entry", ["repeated_dynamic_empty"], ["assisted_static"], ["dynamic_reocr"]),
        step(8, "evaluate_system_self_adjustment", "optional_escalation", ["hardware_placeholder"], ["candidate_only"], ["hardware_invoke"]),
        step(9, "evaluate_external_assistance", "conditional", ["user_unable"], ["nearby_help"], []),
        step(10, "evaluate_visual_semantic_fallback", "allowed", ["ocr_default_off"], ["visual_paths"], ["internal_recrop"]),
        step(11, "evaluate_expired_long_term_context", "route_candidates", ["stale_not_discard"], ["long_term_pools"], ["fact_write"]),
        step(
            12,
            "generate_final_guidance_dryrun_decision",
            PRIMARY_PATH,
            ["USER_GUIDANCE_OR_STATIC_CAPTURE", "internal_recrop_should_stop"],
            ["Voice-Guidance-Prompt-Template-v1"],
            ["dynamic_reocr", "tts_now"],
        ),
    ]
    return {
        "schema_version": "user_guidance_runtime_decision_trace_v1",
        "steps": steps,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _final_decision(case: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "user_guidance_final_dryrun_decision_v1",
        "final_guidance_decision": PRIMARY_PATH,
        "selected_primary_path": PRIMARY_PATH,
        "selected_secondary_paths": [
            "SYSTEM_SELF_ADJUSTMENT_CANDIDATE",
            "VISUAL_SEMANTIC_FALLBACK_CANDIDATE",
            "EXPIRED_LONG_TERM_CONTEXT_CANDIDATE",
        ],
        "internal_recrop_should_stop": case["internal_recrop_should_stop"],
        "dynamic_reocr_allowed_now": case["dynamic_reocr_allowed_now"],
        "tts_allowed_now": False,
        "voice_output_plane_allowed_now": False,
        "runtime_guidance_action_committed": False,
        "recommended_next_phase": "Voice-Guidance-Prompt-Template-v1",
        "alternate_next_phase": "Assisted-Static-Reading-Mode-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_user_guidance_recovery_runtime_dryrun_v1(
    *,
    vision_capture_runtime_root: str,
    vision_capture_governance_root: str,
    user_guidance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    bbox_adjustment_root: str,
    text_detector_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    vc_rt = Path(vision_capture_runtime_root).resolve()
    vc_gov = Path(vision_capture_governance_root).resolve()
    ug = Path(user_guidance_root).resolve()
    ocr_act = Path(ocr_activation_root).resolve()
    stc = Path(stc_sampling_guidance_root).resolve()
    ocr2 = Path(ocr_v2_root).resolve()
    crop_v2 = Path(multiframe_crop_v2_root).resolve()
    bbox = Path(bbox_adjustment_root).resolve()
    td = Path(text_detector_root).resolve()
    cq = Path(crop_quality_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    case = _load_case(vc_rt, ug)
    plan = _guidance_plan()
    prompts = _prompt_matrix()
    triggers = _trigger_matrix(case)
    transitions = _state_transitions()
    static_entry = _static_capture_entry()
    sys_esc = _system_escalation(vc_rt)
    ext_esc = _external_escalation()
    vis_fb = _visual_fallback(vc_rt)
    expired_lt = _expired_long_term()
    trace = _decision_trace(case)
    final = _final_decision(case)

    intake_specs: List[Tuple[str, Path, str, List[str]]] = [
        ("vision_capture_runtime", vc_rt, "vision_capture_runtime_dryrun_v1_summary.json", ["recommended_capture_decision", "internal_recrop_should_stop"]),
        ("vision_capture_governance", vc_gov, "vision_capture_governance_v1_summary.json", ["governance_scope"]),
        ("user_guidance_policy", ug, "user_guidance_recovery_policy_v1_summary.json", ["phase", "user_guidance_recovery_recommended"]),
        ("ocr_activation", ocr_act, "ocr_activation_governance_policy_v1_summary.json", ["ocr_self_activation_allowed"]),
        ("stc_sampling", stc, "stc_sampling_guidance_policy_v1_summary.json", ["phase"]),
        ("ocr_v2", ocr2, "ocrrequest_gated_submission_from_multiframe_v2_summary.json", ["v2_empty_result_count"]),
        ("crop_quality", cq, "crop_quality_diagnosis_v2_multiframe_summary.json", ["empty_ocr_result_count_observed"]),
        ("multiframe_crop_v2", crop_v2, "multiframe_crop_v2_textdetector_adjusted_summary.json", ["adjusted_crop_artifact_count"]),
        ("text_detector", td, "text_detector_dryrun_v1_summary.json", ["bbox_adjustment_candidate_count"]),
        ("bbox_proposal", bbox, "bbox_adjustment_proposal_v2_multiframe_summary.json", ["bbox_adjustment_proposal_count"]),
    ]
    intake_rows = [_intake(iid, root, art, keys) for iid, root, art, keys in intake_specs]

    return {
        "summary": {
            "schema_version": "user_guidance_recovery_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "user_guidance_recovery_runtime_decision_dryrun_only",
            "based_on_vision_capture_runtime_dryrun": vc_rt.is_dir(),
            "based_on_user_guidance_recovery_policy": ug.is_dir(),
            "based_on_ocr_activation_governance": ocr_act.is_dir(),
            "based_on_stc_sampling_guidance": stc.is_dir(),
            "current_case_loaded": bool(vc_rt.is_dir() and case["vision_capture_decision"] == VISION_CAPTURE_DECISION),
            "vision_capture_decision_observed": case["vision_capture_decision"],
            "internal_recrop_should_stop": case["internal_recrop_should_stop"],
            "dynamic_reocr_allowed_now": case["dynamic_reocr_allowed_now"],
            "guidance_plan_generated": True,
            "prompt_candidate_generated": len(prompts.get("rows") or []) > 0,
            "user_response_state_transition_generated": len(transitions.get("transitions") or []) > 0,
            "static_capture_entry_candidate_generated": True,
            "system_self_adjustment_escalation_candidate_generated": len(sys_esc.get("candidates") or []) > 0,
            "external_assistance_escalation_candidate_generated": len(ext_esc.get("candidates") or []) > 0,
            "visual_semantic_fallback_candidate_generated": True,
            "expired_long_term_candidate_generated": len(expired_lt.get("candidates") or []) > 0,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": {
            "schema_version": "user_guidance_runtime_input_intake_matrix_v1",
            "rows": intake_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "triggers": triggers,
        "plan": plan,
        "prompts": prompts,
        "transitions": transitions,
        "static_entry": static_entry,
        "system_escalation": sys_esc,
        "external_escalation": ext_esc,
        "visual_fallback": vis_fb,
        "expired_long_term": expired_lt,
        "trace": trace,
        "final": final,
        "boundary": {
            "schema_version": "user_guidance_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "user_guidance_runtime_metrics_candidate_report_v1",
            "current_case_loaded": bool(vc_rt.is_dir()),
            "guidance_plan_generated": True,
            "prompt_candidate_count": len(prompts.get("rows") or []),
            "response_transition_count": len(transitions.get("transitions") or []),
            "static_capture_entry_candidate_count": 1,
            "system_self_adjustment_candidate_count": len(sys_esc.get("candidates") or []),
            "external_assistance_candidate_count": len(ext_esc.get("candidates") or []),
            "visual_semantic_fallback_candidate_count": 1,
            "expired_long_term_candidate_count": len(expired_lt.get("candidates") or []),
            "runtime_action_committed_count": 0,
            "runtime_tts_invoked_count": 0,
            "voice_output_plane_invoked_count": 0,
            "runtime_camera_invoked_count": 0,
            "runtime_ocr_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "user_guidance_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "user_guidance_runtime_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "user_guidance_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
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
            "schema_version": "user_guidance_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "user_guidance_runtime_non_claims_report_v1",
            "claims": [
                "not_real_user_guidance",
                "no_tts",
                "no_voice_output_plane",
                "prompt_not_broadcast",
                "response_transition_simulated",
                "static_not_real_capture",
                "system_not_hardware",
                "external_not_actual_help",
                "expired_not_fact_or_profile_write",
                "no_ocr",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "user_guidance_runtime_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "user_guidance_runtime_audit_report_v1",
            "user_guidance_recovery_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "vision_capture_decision_observed": case["vision_capture_decision"],
            "guidance_plan_generated": True,
            "prompt_candidate_generated": True,
            "static_capture_entry_candidate_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "runtime_guidance_action_committed": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
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
