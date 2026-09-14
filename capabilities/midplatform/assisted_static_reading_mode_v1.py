# -*- coding: utf-8 -*-
"""Assisted Static Reading Mode v1 — mode policy, FSM, gates (no capture/OCR/TTS).

Phase-Assisted-Static-Reading-Mode-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Assisted-Static-Reading-Mode-v1-001"
HOLD_TEXT = "请先停稳，保持画面稳定。"
MODE_ENTRY = "ENTER_ASSISTED_STATIC_READING_CANDIDATE"

FOLLOWUPS = [
    "Assisted-Static-Reading-Runtime-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Voice-Output-Plane-Adapter-GuardedTrial-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Vision-Capture-Runtime-GuardedTrial-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

ENTRY_CONDITIONS = [
    ("repeated_dynamic_empty", ["v1_empty_count>=threshold"], True, ["safety_alert_active"], "user_can_hold_device", "static_capture", "hold_still"),
    ("same_bbox_no_gain", ["same_bbox_risk_count>=1"], True, ["dynamic_reocr_allowed"], "user_can_reposition", "static_capture", "center_target"),
    ("dynamic_reocr_blocked", ["internal_recrop_should_stop", "dynamic_reocr_allowed_now=false"], True, [], "user_can_pause", "static_capture", "hold_still"),
    ("user_explicit_read_request", ["user_asks_read_text"], True, ["unsafe_motion"], "user_intent_clear", "static_capture", "hold_still"),
    ("long_text_or_dense_text_detected", ["text_density_high"], True, [], "user_available", "static_capture", "pause_for_static_capture"),
    ("high_precision_text_required", ["task_requires_exact_text"], True, [], "user_available", "static_capture", "center_target"),
    ("task_critical_text_unreadable", ["ocr_empty_after_guidance"], True, [], "user_available", "static_capture", "hold_still"),
    ("medicine_label_or_document", ["document_class_signal"], True, ["privacy_block"], "user_consent_context", "static_capture", "pause_for_static_capture"),
    ("ocr_l3_l4_from_activation", ["activation_route=L3_or_L4"], True, [], "activation_allows_static", "static_capture", "hold_still"),
]

READINESS_DIMS = [
    ("user_stability", "device_motion_below_threshold", "shake_or_walk_detected", "hold_still", "request_stabilization", "ask_external_assistance"),
    ("target_centering", "text_bbox_centered_in_frame", "text_off_center", "center_target", "suggest_reframe", "ask_external_assistance"),
    ("viewing_angle", "perspective_angle_within_limit", "excessive_skew", "adjust_angle", "suggest_angle_hint", "ask_external_assistance"),
    ("distance_and_scale", "text_pixel_height_readable", "too_far_or_too_small", "move_closer_or_zoom", "request_zoom", "ask_external_assistance"),
    ("lighting_and_clarity", "brightness_contrast_blur_ok", "low_light_or_blur", "increase_light", "request_exposure_adjustment", "ask_external_assistance"),
]

GUIDANCE_STEPS = [
    (1, "hold_still", "vgpt_001", HOLD_TEXT, "hold_device_steady", "motion_reduced"),
    (2, "center_target", "vgpt_002", "请把文字放在画面中央。", "center_text_in_frame", "centering_improved"),
    (3, "adjust_angle", "vgpt_003", "请稍微调整角度，避免斜着拍。", "reduce_skew", "angle_improved"),
    (4, "move_closer_or_zoom", "vgpt_004", "请稍微靠近一点，再保持稳定。", "increase_text_scale", "scale_improved"),
    (5, "pause_for_static_capture", "vgpt_005", "当前动态画面不稳定，建议停下后再读。", "pause_motion", "static_ready_signal"),
    (6, "confirm_ready_or_retry", "vgpt_confirm", "如果已经对准，请保持不动，我再尝试读取。", "confirm_readiness", "readiness_confirmed"),
]

SELF_ADJ = [
    ("request_high_resolution_still_frame", "blur_or_low_resolution", "high_res_still", False),
    ("request_zoom", "text_too_small", "zoom", True),
    ("request_autofocus", "focus_unstable", "autofocus", True),
    ("request_exposure_adjustment", "low_light", "exposure", True),
    ("request_resampling", "scale_mismatch", "resampling", False),
    ("request_stabilization", "motion_detected", "stabilization", False),
    ("request_static_capture_mode", "dynamic_capture_failed", "static_capture_mode", True),
]

OCR_GATE_CONDITIONS = [
    ("static_mode_active", "mode_entry_decision=ENTER", True),
    ("user_stability_passed", "readiness.user_stability=pass", True),
    ("target_centering_passed", "readiness.target_centering=pass", True),
    ("angle_passed", "readiness.viewing_angle=pass", True),
    ("distance_scale_passed", "readiness.distance_and_scale=pass", True),
    ("lighting_clarity_passed", "readiness.lighting_and_clarity=pass", True),
    ("stc_freshness_passed", "stc_within_freshness_window", True),
    ("task_context_valid", "same_task_context", True),
    ("safety_not_blocking", "not safety_alert_active", True),
]

PIPELINE_STEPS = [
    ("static_capture", "guarded_trial_static_frame", "static_frame_artifact"),
    ("OCRRequest-Gated-Submission-from-StaticReading-v1", "static_frame_artifact", "ocr_result_candidate"),
    ("Evidence-Pack-Adapter-v5-StaticReading", "ocr_result_candidate", "evidence_pack_candidate"),
    ("Semantic-Candidate-v5-StaticReading", "evidence_pack_candidate", "semantic_candidate"),
    ("Source-Validation-v3-StaticReading", "semantic_candidate", "validated_candidate"),
    ("Review / User confirmation", "validated_candidate", "user_confirmed_reading"),
    ("optional WorldModel candidate", "validated_candidate", "world_model_long_term_candidate"),
]

EXIT_ROUTES = [
    ("user_cancelled", "STOP_READING", "已停止读取。"),
    ("safety_alert_active", "STOP_READING", "安全提醒优先，先暂停读取。"),
    ("motion_state_unsafe", "STOP_READING", "当前环境不适合继续对准。"),
    ("repeated_static_capture_failure", "EXTERNAL_ASSISTANCE_CANDIDATE", "可以请身边人帮忙看一下文字。"),
    ("hardware_capability_insufficient", "SYSTEM_SELF_ADJUSTMENT_CANDIDATE", "我会尝试调整采集方式。"),
    ("task_no_longer_relevant", "TASK_DOWNGRADE_NON_OCR_PATH", "这项读取可以先放下。"),
    ("context_expired", "EXPIRED_STATIC_READING_CANDIDATE", "读取上下文已过期。"),
    ("privacy_sensitive_text", "EXTERNAL_ASSISTANCE_CANDIDATE", "敏感内容建议由您本人或信任的人确认。"),
    ("user_unable_to_adjust", "VISUAL_SEMANTIC_FALLBACK", "当前不适合继续读字，我会先按环境继续判断。"),
]

EXPIRED_CANDIDATES = [
    ("expired_static_reading_attempt", "context_expired"),
    ("repeated_unreadable_static_region", "ocr_empty_after_static"),
    ("unresolved_text_anchor", "bbox_no_text"),
    ("user_environment_context_candidate", "scene_context_stale"),
    ("user_profile_context_candidate", "preference_hint_stale"),
    ("emotional_context_background_candidate", "stress_or_urgency_signal"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_rows(roots: Dict[str, Path]) -> List[Dict[str, Any]]:
    specs: List[Tuple[str, str, Optional[str]]] = [
        ("vop_adapter", "vop_adapter", "voice_output_plane_adapter_for_guidance_v1_summary.json"),
        ("vg_runtime", "vg_runtime", "voice_guidance_prompt_runtime_dryrun_v1_summary.json"),
        ("ug_runtime", "ug_runtime", "user_guidance_recovery_runtime_dryrun_v1_summary.json"),
        ("vc_runtime", "vc_runtime", "vision_capture_runtime_dryrun_v1_summary.json"),
        ("vc_governance", "vc_governance", "vision_capture_governance_v1_summary.json"),
        ("ocr_activation", "ocr_activation", "ocr_activation_governance_policy_v1_summary.json"),
        ("stc_sampling", "stc_sampling", "stc_sampling_guidance_policy_v1_summary.json"),
        ("ocr_v2", "ocr_v2", "ocrrequest_gated_submission_from_multiframe_v2_summary.json"),
        ("crop_v2", "crop_v2", "multiframe_crop_v2_textdetector_adjusted_summary.json"),
        ("crop_quality", "crop_quality", "crop_quality_diagnosis_v2_multiframe_summary.json"),
        ("ep_v4", "ep_v4", "evidence_pack_adapter_v4_multiframe_summary.json"),
        ("benchmark", "benchmark", None),
        ("system_health", "health", None),
        ("simulation", "sim", None),
    ]
    rows = []
    for iid, key, artifact in specs:
        root = roots[key]
        loaded = root.is_dir()
        if artifact:
            loaded = loaded and (root / artifact).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root": str(root),
                "source_artifact": artifact or "(directory)",
                "loaded": loaded,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    ug_pol = roots.get("ug_policy")
    if ug_pol and ug_pol.is_dir():
        art = "user_guidance_recovery_policy_v1_summary.json"
        rows.append(
            {
                "intake_id": "ug_policy",
                "input_source": "ug_policy",
                "source_root": str(ug_pol),
                "source_artifact": art,
                "loaded": (ug_pol / art).is_file(),
                "key_fields_observed": [],
                "intake_status": "loaded" if (ug_pol / art).is_file() else "optional",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return rows


def run_assisted_static_reading_mode_v1(
    *,
    voice_output_plane_adapter_root: str,
    voice_guidance_runtime_root: str,
    user_guidance_runtime_root: str,
    vision_capture_runtime_root: str,
    vision_capture_governance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    user_guidance_policy_root: str,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    roots = {
        "vop_adapter": Path(voice_output_plane_adapter_root).resolve(),
        "vg_runtime": Path(voice_guidance_runtime_root).resolve(),
        "ug_runtime": Path(user_guidance_runtime_root).resolve(),
        "vc_runtime": Path(vision_capture_runtime_root).resolve(),
        "vc_governance": Path(vision_capture_governance_root).resolve(),
        "ocr_activation": Path(ocr_activation_root).resolve(),
        "stc_sampling": Path(stc_sampling_guidance_root).resolve(),
        "ug_policy": Path(user_guidance_policy_root).resolve(),
        "ocr_v2": Path(ocr_v2_root).resolve(),
        "crop_v2": Path(multiframe_crop_v2_root).resolve(),
        "crop_quality": Path(crop_quality_root).resolve(),
        "ep_v4": Path(evidence_pack_v4_root).resolve(),
        "benchmark": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    vc_sum = _read_json(roots["vc_runtime"] / "vision_capture_runtime_dryrun_v1_summary.json") or {}
    vop_final = _read_json(roots["vop_adapter"] / "voice_output_plane_adapter_final_dryrun_decision_v1.json") or {}
    ocr_v2 = _read_json(roots["ocr_v2"] / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}

    v1_empty = ocr_v2.get("v1_empty_count", ocr_v2.get("empty_count_v1", 30))
    v2_empty = ocr_v2.get("v2_empty_count", ocr_v2.get("empty_count_v2", 5))
    same_bbox = ocr_v2.get("same_bbox_risk_count", 5)

    entry_rows = []
    for cond, signals, allowed, blocked, user_state, capture_mode, action in ENTRY_CONDITIONS:
        if cond in ("repeated_dynamic_empty", "same_bbox_no_gain", "dynamic_reocr_blocked"):
            allowed = True
        entry_rows.append(
            {
                "entry_condition": cond,
                "required_signals": signals,
                "allowed_entry": allowed,
                "blocked_when": blocked,
                "required_user_state": user_state,
                "required_capture_mode": capture_mode,
                "initial_guidance_action": action,
                "fact_status_after_entry": "not_fact",
            }
        )

    states = [
        "STATIC_READING_NOT_STARTED",
        "ENTRY_CANDIDATE_READY",
        "GUIDANCE_PROMPT_READY",
        "WAITING_FOR_USER_STABILIZATION",
        "WAITING_FOR_TARGET_CENTERING",
        "WAITING_FOR_ANGLE_ADJUSTMENT",
        "STATIC_CAPTURE_READY_CANDIDATE",
        "SYSTEM_SELF_ADJUSTMENT_CANDIDATE",
        "OCRREQUEST_READY_CANDIDATE",
        "OCR_EXECUTION_FUTURE",
        "REVIEW_RESULT_FUTURE",
        "EXTERNAL_ASSISTANCE_CANDIDATE",
        "VISUAL_SEMANTIC_FALLBACK",
        "STATIC_READING_ABORTED",
        "STATIC_READING_EXPIRED_CANDIDATE",
    ]
    transitions = [
        ("STATIC_READING_NOT_STARTED", "ENTRY_CANDIDATE_READY", "entry_signals_met", "repeated_dynamic_empty"),
        ("ENTRY_CANDIDATE_READY", "GUIDANCE_PROMPT_READY", "voice_guidance_ready", "speech_candidate"),
        ("GUIDANCE_PROMPT_READY", "WAITING_FOR_USER_STABILIZATION", "first_prompt_hold_still", "hold_still"),
        ("WAITING_FOR_USER_STABILIZATION", "WAITING_FOR_TARGET_CENTERING", "stability_improved", "user_stability"),
        ("WAITING_FOR_TARGET_CENTERING", "WAITING_FOR_ANGLE_ADJUSTMENT", "centering_improved", "target_centering"),
        ("WAITING_FOR_ANGLE_ADJUSTMENT", "STATIC_CAPTURE_READY_CANDIDATE", "angle_improved", "viewing_angle"),
        ("STATIC_CAPTURE_READY_CANDIDATE", "OCRREQUEST_READY_CANDIDATE", "all_readiness_pass", "readiness_gate"),
        ("OCRREQUEST_READY_CANDIDATE", "OCR_EXECUTION_FUTURE", "ocrrequest_gate_pass", "future_only"),
        ("STATIC_CAPTURE_READY_CANDIDATE", "SYSTEM_SELF_ADJUSTMENT_CANDIDATE", "hardware_adjust_needed", "quality_fail"),
        ("WAITING_FOR_USER_STABILIZATION", "EXTERNAL_ASSISTANCE_CANDIDATE", "user_unable", "escalation"),
        ("GUIDANCE_PROMPT_READY", "VISUAL_SEMANTIC_FALLBACK", "ocr_not_viable", "fallback"),
        ("OCR_EXECUTION_FUTURE", "REVIEW_RESULT_FUTURE", "ocr_complete_future", "result"),
        ("ENTRY_CANDIDATE_READY", "STATIC_READING_EXPIRED_CANDIDATE", "context_expired", "expiry"),
        ("WAITING_FOR_USER_STABILIZATION", "STATIC_READING_ABORTED", "user_cancelled", "cancel"),
    ]

    readiness = {
        "schema_version": "assisted_static_reading_readiness_gate_v1",
        "dimensions": [
            {
                "readiness_dimension": dim,
                "pass_condition": pass_c,
                "fail_condition": fail_c,
                "user_repair_action": user_a,
                "system_repair_action": sys_a,
                "external_assistance_action": ext_a,
                "ocrrequest_eligible_if_passed": True,
                "action_committed_now": False,
                "fact_status": "not_fact",
            }
            for dim, pass_c, fail_c, user_a, sys_a, ext_a in READINESS_DIMS
        ],
        "all_pass_required_for_ocrrequest": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    quality = {
        "schema_version": "assisted_static_capture_quality_requirement_v1",
        "min_text_pixel_height_placeholder": 24,
        "target_text_pixel_height_placeholder": 48,
        "max_perspective_angle_placeholder": 15,
        "min_brightness_placeholder": 0.35,
        "min_contrast_placeholder": 0.25,
        "max_blur_placeholder": 0.4,
        "min_stable_duration_ms_placeholder": 800,
        "target_centering_requirement": "text_bbox_center_offset_ratio<=0.2",
        "crop_bbox_requirement": "stable_bbox_with_margin",
        "threshold_is_policy_placeholder": True,
        "not_production_threshold_claim": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    guidance_seq = {
        "schema_version": "assisted_static_reading_user_guidance_sequence_v1",
        "steps": [
            {
                "step_order": order,
                "action_id": aid,
                "prompt_template_ref": ref,
                "prompt_text_candidate": text,
                "expected_user_action": exp,
                "expected_signal_improvement": sig,
                "blocked_when": ["safety_alert_active"],
                "tts_invoked_now": False,
                "speech_request_submitted_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
            for order, aid, ref, text, exp, sig in GUIDANCE_STEPS
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    self_adj = {
        "schema_version": "assisted_static_reading_system_self_adjustment_policy_v1",
        "candidates": [
            {
                "action_id": aid,
                "trigger_reason": reason,
                "required_hardware_capability": cap,
                "hardware_capability_known": known,
                "expected_signal_improvement": "capture_quality_improved",
                "blocked_when": ["safety_alert_active", "privacy_block"],
                "hardware_action_invoked_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
            for aid, reason, cap, known in SELF_ADJ
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    ocr_gate = {
        "schema_version": "assisted_static_reading_ocrrequest_future_gate_v1",
        "future_gate_only": True,
        "conditions": [
            {
                "gate_condition": cond,
                "required_signal": sig,
                "ocrrequest_eligible_later": eligible,
                "ocrrequest_generated_now": False,
                "provider_invoked_now": False,
                "fact_status_after_gate": "not_fact",
            }
            for cond, sig, eligible in OCR_GATE_CONDITIONS
        ],
        "all_conditions_required": True,
        "ocrrequest_generated_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    pipeline = {
        "schema_version": "assisted_static_reading_result_pipeline_plan_v1",
        "steps": [
            {
                "future_phase": phase,
                "input_requirement": inp,
                "output_candidate": out,
                "write_allowed_now": False,
                "fact_status": "not_fact",
            }
            for phase, inp, out in PIPELINE_STEPS
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    exit_pol = {
        "schema_version": "assisted_static_reading_exit_fallback_escalation_policy_v1",
        "routes": [
            {
                "exit_condition": cond,
                "route_to": route,
                "user_message_candidate": msg,
                "runtime_action_committed_now": False,
                "fact_status": "not_fact",
            }
            for cond, route, msg in EXIT_ROUTES
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    expired = {
        "schema_version": "assisted_static_reading_expired_candidate_policy_v1",
        "candidates": [
            {
                "candidate_type": ctype,
                "source_signal": sig,
                "cannot_use_for_action": True,
                "cannot_write_fact": True,
                "can_feed_long_term_candidate": True,
                "required_metadata": [
                    "source_chain",
                    "time_anchor",
                    "spatial_anchor",
                    "original_task_context",
                    "stale_reason",
                    "confidence_decay",
                    "privacy_sensitivity",
                    "future_usage_scope",
                ],
                "write_allowed_now": False,
                "fact_status": "not_fact",
            }
            for ctype, sig in EXPIRED_CANDIDATES
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    current = {
        "schema_version": "assisted_static_reading_current_case_decision_v1",
        "current_case_loaded": True,
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "internal_recrop_should_stop": vc_sum.get("internal_recrop_should_stop", True),
        "dynamic_reocr_allowed_now": vc_sum.get("dynamic_reocr_allowed_now", False),
        "voice_guidance_ready_for_future_submit": vop_final.get("final_decision") == "READY_FOR_FUTURE_VOP_SUBMIT",
        "assisted_static_reading_entry_recommended": True,
        "mode_entry_decision": MODE_ENTRY,
        "first_guidance_action": "hold_still",
        "first_prompt_text": vop_final.get("selected_prompt_text", HOLD_TEXT),
        "ocrrequest_generated_now": False,
        "runtime_capture_invoked_now": False,
        "tts_invoked_now": False,
        "recommended_next_phase": "Assisted-Static-Reading-Runtime-DryRun-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "assisted_static_reading_mode_v1_summary_v0",
            "phase": PHASE_ID,
            "mode_scope": "assisted_static_reading_mode_policy_only",
            "based_on_voice_output_plane_adapter": roots["vop_adapter"].is_dir(),
            "based_on_voice_guidance_prompt_runtime": roots["vg_runtime"].is_dir(),
            "based_on_user_guidance_runtime": roots["ug_runtime"].is_dir(),
            "based_on_vision_capture_runtime": roots["vc_runtime"].is_dir(),
            "based_on_ocr_activation_governance": roots["ocr_activation"].is_dir(),
            "current_case_loaded": True,
            "assisted_static_reading_mode_defined": True,
            "mode_entry_policy_defined": True,
            "mode_state_machine_defined": True,
            "static_reading_readiness_gate_defined": True,
            "static_capture_quality_requirement_defined": True,
            "user_guidance_sequence_defined": True,
            "system_self_adjustment_policy_defined": True,
            "ocrrequest_future_gate_defined": True,
            "exit_fallback_escalation_policy_defined": True,
            "expired_static_reading_candidate_policy_defined": True,
            "current_case_mode_decision_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
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
            "schema_version": "assisted_static_reading_input_intake_matrix_v1",
            "rows": _intake_rows(roots),
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "entry_policy": {
            "schema_version": "assisted_static_reading_mode_entry_policy_v1",
            "entries": entry_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "state_machine": {
            "schema_version": "assisted_static_reading_state_machine_v1",
            "states": states,
            "transitions": [
                {
                    "from_state": f,
                    "to_state": t,
                    "trigger_condition": cond,
                    "required_signal": sig,
                    "blocked_when": [],
                    "runtime_state_changed_now": False,
                    "fact_status": "not_fact",
                }
                for f, t, cond, sig in transitions
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "readiness": readiness,
        "quality": quality,
        "guidance_seq": guidance_seq,
        "self_adj": self_adj,
        "ocr_gate": ocr_gate,
        "pipeline": pipeline,
        "exit_pol": exit_pol,
        "expired": expired,
        "current": current,
        "ocr_link": {
            "schema_version": "assisted_static_reading_ocr_activation_link_report_v1",
            "linked_to_ocr_activation_governance": True,
            "activation_decision_source": "USER_GUIDANCE_RECOVERY / ASSISTED_STATIC_READING",
            "dynamic_reocr_blocked": True,
            "ocr_default_off_for_world_modeling_respected": True,
            "visual_semantic_fallback_preserved": True,
            "fact_status": "not_fact",
        },
        "voice_link": {
            "schema_version": "assisted_static_reading_voice_guidance_link_report_v1",
            "linked_to_voice_guidance_prompt_template": True,
            "linked_to_voice_guidance_prompt_runtime": True,
            "linked_to_vop_adapter_for_guidance": True,
            "first_prompt_ready_as_speech_request_candidate": True,
            "vop_submit_ready_later": True,
            "current_phase_vop_invoked": False,
            "current_phase_tts_invoked": False,
            "fact_status": "not_fact",
        },
        "vc_link": {
            "schema_version": "assisted_static_reading_vision_capture_link_report_v1",
            "linked_to_vision_capture_governance": True,
            "linked_to_vision_capture_runtime": True,
            "recommended_capture_decision": vc_sum.get("recommended_capture_decision", "USER_GUIDANCE_OR_STATIC_CAPTURE"),
            "capture_quality_problem_likely": True,
            "static_capture_required": True,
            "current_phase_camera_invoked": False,
            "current_phase_frame_captured": False,
            "fact_status": "not_fact",
        },
        "boundary": {
            "schema_version": "assisted_static_reading_boundary_report_v1",
            "mode_policy_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
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
            "schema_version": "assisted_static_reading_metrics_candidate_report_v1",
            "mode_defined": True,
            "entry_policy_defined": True,
            "state_machine_defined": True,
            "readiness_gate_defined": True,
            "quality_requirement_defined": True,
            "guidance_sequence_step_count": len(GUIDANCE_STEPS),
            "system_self_adjustment_action_count": len(SELF_ADJ),
            "ocrrequest_future_gate_defined": True,
            "result_pipeline_plan_defined": True,
            "exit_fallback_policy_defined": True,
            "expired_candidate_policy_defined": True,
            "runtime_action_committed_count": 0,
            "runtime_tts_invoked_count": 0,
            "runtime_camera_invoked_count": 0,
            "runtime_ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "assisted_static_reading_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["benchmark"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "assisted_static_reading_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "assisted_static_reading_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "mode_policy_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
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
            "schema_version": "assisted_static_reading_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "assisted_static_reading_non_claims_report_v1",
            "claims": [
                "not_real_static_reading",
                "no_tts",
                "no_vop",
                "no_camera",
                "no_new_frames",
                "no_ocr",
                "no_ocrrequest",
                "readiness_not_production_judge",
                "quality_threshold_placeholder",
                "static_capture_not_real",
                "pipeline_plan_not_executed",
                "expired_not_fact_or_profile",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "assisted_static_reading_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "assisted_static_reading_audit_report_v1",
            "assisted_static_reading_mode_v1_executed": True,
            "mode_policy_only": True,
            "assisted_static_reading_mode_defined": True,
            "static_reading_readiness_gate_defined": True,
            "ocrrequest_future_gate_defined": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
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
