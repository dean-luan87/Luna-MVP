# -*- coding: utf-8 -*-
"""User Guidance Recovery Policy v1 — OCR input readiness, repairability, action candidates (policy only).

Phase-User-Guidance-Recovery-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "User-Guidance-Recovery-Policy-v1-001"
RUNTIME_STEP = "user_guidance_recovery_policy_v1"
POLICY_PLACEHOLDER = True

FOLLOWUPS = [
    "STC-Sampling-Guidance-Policy-v1",
    "Vision-Capture-Governance-v1",
    "OCR-Activation-Governance-Policy-v1",
    "User-Guidance-Recovery-Runtime-DryRun-v1",
    "Voice-Guidance-Prompt-Template-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Dynamic-Short-Text-Reading-Scope-v1",
    "Hardware-Camera-Control-Contract-v1",
    "External-Assistance-Policy-v1",
]

FUTURE_STC_PHASES = [
    "STC-Sampling-Guidance-Policy-v1",
    "Vision-Capture-Governance-v1",
    "OCR-Activation-Governance-Policy-v1",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _ocr_activation_levels() -> List[Dict[str, Any]]:
    return [
        {
            "level": "OCR-L0",
            "trigger_condition": "world_model_path_sufficient; task_not_ocr_critical",
            "allowed_action": "vision_semantic_spatial_poi_only",
            "blocked_action": "ocr_invoke;dynamic_reading",
            "required_input_quality": "any",
            "latency_budget_hint_ms": 0,
            "user_interrupt_cost": "none",
            "fallback_next_level": "OCR-L1",
            "fact_status_after_level": "not_fact",
        },
        {
            "level": "OCR-L1",
            "trigger_condition": "short_text_marker; stable_view; task_confirmation_light",
            "allowed_action": "lightweight_short_text_ocr",
            "blocked_action": "full_frame_ocr;static_long_read",
            "required_input_quality": "readiness_partial_ok",
            "latency_budget_hint_ms": 800,
            "user_interrupt_cost": "low",
            "fallback_next_level": "OCR-L2",
            "fact_status_after_level": "not_fact",
        },
        {
            "level": "OCR-L2",
            "trigger_condition": "safety_sign|doorplate|exit_entry|task_critical_short_text",
            "allowed_action": "task_confirmation_ocr_gated",
            "blocked_action": "unbounded_internal_recrop",
            "required_input_quality": "bbox_and_readability_ok",
            "latency_budget_hint_ms": 2000,
            "user_interrupt_cost": "medium",
            "fallback_next_level": "OCR-L3",
            "fact_status_after_level": "not_fact",
        },
        {
            "level": "OCR-L3",
            "trigger_condition": "user_active_read_request|long_notice|menu|medicine_label",
            "allowed_action": "user_guided_static_precision_read",
            "blocked_action": "dynamic_read_while_moving",
            "required_input_quality": "static_capture_quality_gate_pass",
            "latency_budget_hint_ms": 5000,
            "user_interrupt_cost": "high",
            "fallback_next_level": "OCR-L4",
            "fact_status_after_level": "not_fact",
        },
        {
            "level": "OCR-L4",
            "trigger_condition": "repeated_empty_after_internal_retry; same_bbox_risk; input_not_ready",
            "allowed_action": "dynamic_reading_recovery_chain_policy_only",
            "blocked_action": "infinite_internal_recrop;fact_write",
            "required_input_quality": "recovery_policy_decision",
            "latency_budget_hint_ms": 0,
            "user_interrupt_cost": "medium",
            "fallback_next_level": "OCR-L5",
            "fact_status_after_level": "not_fact",
        },
        {
            "level": "OCR-L5",
            "trigger_condition": "not_recoverable|hardware_insufficient|user_cannot_repair",
            "allowed_action": "external_assistance_or_task_degrade",
            "blocked_action": "ocr_retry_loop",
            "required_input_quality": "n/a",
            "latency_budget_hint_ms": 0,
            "user_interrupt_cost": "high",
            "fallback_next_level": "OCR-L0",
            "fact_status_after_level": "not_fact",
        },
    ]


def _task_criticality_rows() -> List[Dict[str, Any]]:
    def row(
        task_type: str,
        ocr_needed: bool,
        dynamic: bool,
        static_req: bool,
        ug: bool,
        ext: bool,
        wm_path: str,
        level: str,
        reason: str,
    ) -> Dict[str, Any]:
        return {
            "task_type": task_type,
            "ocr_needed": ocr_needed,
            "dynamic_reading_allowed": dynamic,
            "static_assisted_reading_required": static_req,
            "user_guidance_allowed": ug,
            "external_assistance_allowed": ext,
            "default_world_model_path": wm_path,
            "ocr_activation_level": level,
            "reason": reason,
            "fact_status": "not_fact",
            "write_allowed": False,
        }

    return [
        row("safety_sign", True, True, False, True, True, "vision_then_ocr_confirm", "OCR-L2", "safety_critical_short_text"),
        row("doorplate", True, True, False, True, True, "vision_then_ocr_confirm", "OCR-L2", "task_completion"),
        row("room_number", True, True, False, True, False, "vision_then_ocr_confirm", "OCR-L2", "navigation_task"),
        row("window_number", True, True, False, True, False, "vision_then_ocr_confirm", "OCR-L2", "task_completion"),
        row("floor_number", True, True, False, True, False, "vision_then_ocr_confirm", "OCR-L2", "task_completion"),
        row("exit_entry_sign", True, True, False, True, True, "vision_then_ocr_confirm", "OCR-L2", "safety_navigation"),
        row("public_facility_marker", False, False, False, True, False, "icon_logo_poi_primary", "OCR-L0", "prefer_visual_symbol"),
        row(
            "shop_name_confirmation",
            False,
            False,
            False,
            True,
            False,
            "visual_semantic_logo_poi_then_ocr_confirm",
            "OCR-L1",
            "ocr_as_confirmation_only",
        ),
        row("transit_line_number", True, True, False, True, False, "vision_then_ocr_confirm", "OCR-L2", "task_completion"),
        row("medicine_label", True, False, True, True, True, "static_reading_required", "OCR-L3", "precision_and_safety"),
        row("long_notice", False, False, True, True, True, "static_assisted_reading", "OCR-L3", "long_text_not_dynamic"),
        row("menu_full_reading", False, False, True, True, True, "static_assisted_reading", "OCR-L3", "long_text_not_dynamic"),
        row("poster_article", False, False, True, True, True, "static_assisted_reading", "OCR-L3", "long_text_not_dynamic"),
        row(
            "generic_environment_text",
            False,
            False,
            False,
            False,
            False,
            "vision_semantic_only",
            "OCR-L0",
            "default_no_ocr",
        ),
    ]


def _failure_reason_taxonomy() -> List[Dict[str, Any]]:
    codes = [
        ("view_not_centered", "Target not centered in frame", ["offset_from_center_high"], "ask_user_center_text", "request_higher_quality_frame", None, False, "OCR-L3"),
        ("view_angle_too_oblique", "Viewing angle too oblique", ["perspective_skew_high"], "ask_user_adjust_angle_left", None, None, False, "OCR-L3"),
        ("target_too_far", "Target too far; text too small in pixels", ["crop_height_below_min", "text_pixel_height_low"], "ask_user_move_closer", "request_zoom", None, False, "OCR-L3"),
        ("target_too_close", "Target too close; crop clipped or oversized", ["bbox_clipped", "crop_fills_frame"], "ask_user_step_back", "request_resampling", None, False, "OCR-L3"),
        ("motion_blur", "Motion blur degrades readability", ["blur_score_high", "frame_unstable"], "ask_user_hold_still", "request_multiframe_stabilization", None, False, "OCR-L3"),
        ("low_brightness", "Insufficient brightness", ["brightness_below_min"], "ask_user_increase_light", "request_exposure_adjustment", None, False, "OCR-L3"),
        ("low_contrast", "Low contrast text/background", ["contrast_below_min"], "ask_user_increase_light", "request_exposure_adjustment", None, False, "OCR-L3"),
        ("occlusion", "Target occluded", ["occlusion_ratio_high"], "ask_user_adjust_angle", None, "request_nearby_person_adjust_angle", False, "OCR-L5"),
        ("projection_drift", "Static projection drift from true text region", ["projection_is_approximate", "detected_region_false"], None, "request_heavy_text_detector", None, False, "OCR-L4"),
        ("bbox_too_small", "BBox area below minimum", ["bbox_area_below_min", "crop_width_height_small"], "ask_user_move_closer", "request_zoom", None, False, "OCR-L3"),
        ("bbox_too_large", "BBox covers non-text clutter", ["bbox_area_above_max"], "ask_user_center_text", "request_resampling", None, False, "OCR-L3"),
        ("bbox_wrong_region", "BBox anchored on wrong region", ["iou_with_text_region_low"], "ask_user_center_text", "request_heavy_text_detector", None, False, "OCR-L4"),
        ("text_too_dense", "Text density too high for dynamic OCR", ["line_count_high", "char_density_high"], "ask_user_pause_for_static_reading", "request_static_capture_mode", None, False, "OCR-L3"),
        ("text_too_long", "Text too long for dynamic mode", ["char_count_above_dynamic_limit"], "ask_user_pause_for_static_reading", "request_high_resolution_still_frame", None, True, "OCR-L3"),
        ("text_not_task_critical", "Text not task-critical", ["task_type_generic_environment"], "ask_user_confirm_task_importance", None, None, True, "OCR-L0"),
        ("repeated_empty_after_internal_retry", "Repeated empty OCR after internal retry", ["v1_empty", "v2_empty", "same_bbox_risk"], None, "request_resampling", "request_nearby_person_read_short_text", False, "OCR-L4"),
        ("hardware_capability_insufficient", "Required hardware capability unavailable", ["zoom_unavailable", "autofocus_unavailable"], None, None, "request_user_manual_input", True, "OCR-L5"),
        ("user_action_required", "Repair requires user physical adjustment", ["distance_or_angle_failure"], "ask_user_move_closer", None, None, False, "OCR-L3"),
        ("external_assistance_required", "User cannot self-repair", ["accessibility_limit", "target_unreachable"], None, None, "request_staff_confirm_location", True, "OCR-L5"),
        ("not_recoverable_by_ocr", "OCR cannot recover under policy", ["privacy_sensitive", "unsafe_to_read"], None, None, "request_user_manual_input", True, "OCR-L5"),
    ]
    rows = []
    for code, desc, signals, user_act, sys_act, ext_act, impossible, nxt in codes:
        rows.append(
            {
                "reason_code": code,
                "description": desc,
                "detectable_signals": signals,
                "user_repair_action": user_act,
                "system_repair_action": sys_act,
                "external_assistance_action": ext_act,
                "impossible_condition": impossible,
                "next_policy_level": nxt,
                "fact_status": "not_fact",
            }
        )
    return rows


def _repairability_policy() -> Dict[str, Any]:
    categories = [
        {
            "category": "user_repairable",
            "reason_codes": [
                "target_too_far",
                "view_not_centered",
                "view_angle_too_oblique",
                "motion_blur",
                "low_brightness",
                "user_action_required",
            ],
            "allowed_actions": ["user_guidance_action_candidates"],
            "blocked_actions": ["auto_ocr_retry_without_guidance"],
            "escalation_policy": "try_user_guidance_before_system_hardware",
            "runtime_action_allowed_now": False,
        },
        {
            "category": "system_repairable",
            "reason_codes": [
                "projection_drift",
                "bbox_wrong_region",
                "target_too_far",
                "motion_blur",
            ],
            "allowed_actions": ["system_self_adjustment_candidates"],
            "blocked_actions": ["direct_hardware_invoke_in_policy_phase"],
            "escalation_policy": "system_self_adjustment_after_user_guidance_or_parallel",
            "runtime_action_allowed_now": False,
        },
        {
            "category": "externally_repairable",
            "reason_codes": [
                "external_assistance_required",
                "occlusion",
                "hardware_capability_insufficient",
            ],
            "allowed_actions": ["external_assistance_candidates"],
            "blocked_actions": ["forced_ocr_loop"],
            "escalation_policy": "external_after_user_and_system_exhausted",
            "runtime_action_allowed_now": False,
        },
        {
            "category": "not_recoverable_or_not_worth_ocr",
            "reason_codes": [
                "text_not_task_critical",
                "text_too_long",
                "not_recoverable_by_ocr",
                "repeated_empty_after_internal_retry",
            ],
            "allowed_actions": ["task_degrade", "world_model_path_only"],
            "blocked_actions": ["ocr_retry", "internal_recrop_loop"],
            "escalation_policy": "stop_ocr_enter_L0_or_L5",
            "runtime_action_allowed_now": False,
        },
    ]
    return {
        "schema_version": "ocr_repairability_classification_policy_v1",
        "categories": categories,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _user_guidance_actions() -> List[Dict[str, Any]]:
    specs = [
        ("ask_user_move_closer", ["target_too_far", "bbox_too_small"], "请靠近一些，让文字在画面中更大、更清晰。", "text_pixel_height", "medium", "low", ["target_unreachable"]),
        ("ask_user_step_back", ["target_too_close"], "请稍后退，避免文字被裁切或占满画面。", "bbox_clip_reduction", "low", "low", []),
        ("ask_user_center_text", ["view_not_centered", "bbox_wrong_region"], "请将目标文字移到画面中央。", "centering_score", "low", "low", []),
        ("ask_user_adjust_angle_left", ["view_angle_too_oblique"], "请向左微调手机角度，减少斜视。", "perspective_skew", "medium", "low", []),
        ("ask_user_adjust_angle_right", ["view_angle_too_oblique"], "请向右微调手机角度，减少斜视。", "perspective_skew", "medium", "low", []),
        ("ask_user_raise_camera", ["view_angle_too_oblique"], "请略微抬高镜头对准文字。", "vertical_alignment", "low", "low", []),
        ("ask_user_lower_camera", ["view_angle_too_oblique"], "请略微降低镜头对准文字。", "vertical_alignment", "low", "low", []),
        ("ask_user_hold_still", ["motion_blur"], "请保持手机稳定片刻。", "blur_reduction", "low", "low", []),
        ("ask_user_increase_light", ["low_brightness", "low_contrast"], "请改善光线或避开强逆光。", "brightness_contrast", "low", "low", []),
        ("ask_user_zoom_or_enable_magnification", ["target_too_far", "bbox_too_small"], "如设备支持，可打开放大/变焦后再对准文字。", "text_pixel_height", "medium", "low", ["zoom_unavailable"]),
        ("ask_user_pause_for_static_reading", ["text_too_dense", "text_too_long"], "内容较长，请停下并稳定对准后再阅读。", "static_readiness", "high", "low", []),
        ("ask_user_confirm_task_importance", ["text_not_task_critical"], "请确认是否需要读取这段文字以完成任务。", "task_criticality", "low", "none", []),
    ]
    return [
        {
            "action_id": aid,
            "action_type": "user_guidance",
            "trigger_reason_codes": triggers,
            "suggested_prompt_template": tmpl,
            "expected_signal_improvement": sig,
            "user_effort_level": effort,
            "safety_risk_level": safety,
            "blocked_when": blocked,
            "runtime_tts_allowed_now": False,
            "action_committed_now": False,
            "fact_status": "not_fact",
        }
        for aid, triggers, tmpl, sig, effort, safety, blocked in specs
    ]


def _system_self_adjustments() -> List[Dict[str, Any]]:
    specs = [
        ("request_higher_quality_frame", ["motion_blur", "low_brightness"], "better_frame_capture", "camera_permission", "frame_quality", "low", "low", []),
        ("request_zoom", ["target_too_far", "bbox_too_small"], "zoom_control", "camera_zoom", "text_pixel_height", "medium", "medium", ["zoom_unavailable"]),
        ("request_autofocus", ["target_too_far", "motion_blur"], "autofocus", "camera_autofocus", "focus_sharpness", "medium", "low", ["autofocus_unavailable"]),
        ("request_exposure_adjustment", ["low_brightness", "low_contrast"], "exposure", "camera_exposure", "brightness_contrast", "low", "low", []),
        ("request_resampling", ["projection_drift", "bbox_wrong_region"], "resampling", "capture_pipeline", "localization_stability", "high", "high", []),
        ("request_multiframe_stabilization", ["motion_blur"], "stabilization", "multiframe_buffer", "blur_reduction", "medium", "medium", []),
        ("request_heavy_text_detector", ["projection_drift", "bbox_wrong_region"], "text_detector_heavy", "vision_text_detector", "bbox_alignment", "high", "high", []),
        ("request_static_capture_mode", ["text_too_dense", "text_too_long"], "static_capture", "capture_mode", "static_readiness", "medium", "medium", []),
        ("request_high_resolution_still_frame", ["text_too_long"], "still_capture", "high_res_still", "ocr_readability", "high", "high", []),
    ]
    return [
        {
            "action_id": aid,
            "action_type": "system_self_adjustment",
            "trigger_reason_codes": triggers,
            "required_hardware_capability": hw,
            "required_permission": perm,
            "expected_signal_improvement": sig,
            "latency_cost": lat,
            "battery_compute_cost": bat,
            "blocked_when": blocked,
            "hardware_action_invoked_now": False,
            "action_committed_now": False,
            "fact_status": "not_fact",
        }
        for aid, triggers, hw, perm, sig, lat, bat, blocked in specs
    ]


def _external_assistance_actions() -> List[Dict[str, Any]]:
    specs = [
        ("request_nearby_person_adjust_angle", ["occlusion", "view_angle_too_oblique"], "user_cannot_see_target", "low", "请附近的人帮忙调整角度或遮挡。", 2),
        ("request_nearby_person_read_short_text", ["repeated_empty_after_internal_retry"], "short_text_task_critical", "medium", "请他人帮忙念出标识上的短文字。", 3),
        ("request_staff_confirm_location", ["external_assistance_required"], "indoor_facility", "low", "请咨询工作人员确认位置。", 2),
        ("request_user_take_photo_and_share", ["hardware_capability_insufficient"], "async_ok", "low", "可拍照保存后稍后查看或请人协助。", 1),
        ("request_user_manual_input", ["not_recoverable_by_ocr", "hardware_capability_insufficient"], "always_allowed", "none", "请手动输入已知信息以继续任务。", 4),
    ]
    return [
        {
            "action_id": aid,
            "action_type": "external_assistance",
            "trigger_reason_codes": triggers,
            "when_allowed": when,
            "privacy_safety_considerations": priv,
            "suggested_prompt_template": tmpl,
            "escalation_threshold": thresh,
            "action_committed_now": False,
            "fact_status": "not_fact",
        }
        for aid, triggers, when, priv, tmpl, thresh in specs
    ]


def _not_worth_ocr_policy() -> List[Dict[str, Any]]:
    stops = [
        ("repeated_empty_after_internal_retry_limit", "v1_and_v2_empty_with_same_bbox_risk", "OCR-L4_user_guidance", "internal_retry_exhausted_try_guidance", "vision_semantic_primary"),
        ("geometry_change_insufficient_after_adjustment", "geometry_change_significant_count=0", "OCR-L4", "stop_internal_recrop", "vision_semantic_primary"),
        ("text_not_task_critical", "task_type=generic_environment_text", "OCR-L0", "skip_ocr", "world_model_only"),
        ("long_text_in_dynamic_mode", "task_requires_static_reading", "OCR-L3", "switch_static_assisted", "static_reading_path"),
        ("region_not_visible", "target_not_in_frame", "OCR-L5", "relocate_or_external", "navigation_assist"),
        ("target_unreachable", "physical_access_blocked", "OCR-L5", "external_assistance", "task_degrade"),
        ("privacy_sensitive_text", "privacy_policy_blocks", "OCR-L5", "no_read", "manual_confirm"),
        ("unsafe_to_continue_reading", "safety_policy_blocks", "OCR-L5", "stop", "safety_first"),
        ("user_is_moving_fast", "motion_stability_fail", "OCR-L3", "ask_hold_still", "pause_until_stable"),
        ("hardware_capability_insufficient", "required_hw_missing", "OCR-L5", "manual_or_external", "degrade"),
        ("no_available_user_or_system_repair", "all_repair_paths_blocked", "OCR-L5", "task_degrade", "world_model_fallback"),
    ]
    return [
        {
            "stop_reason": reason,
            "stop_condition": cond,
            "recommended_fallback": fallback,
            "user_message_candidate": msg,
            "world_model_path": wm,
            "ocr_retry_allowed": False,
            "fact_status": "not_fact",
        }
        for reason, cond, fallback, msg, wm in stops
    ]


def _readiness_scope() -> Dict[str, Any]:
    ph = {
        "threshold_is_policy_placeholder": POLICY_PLACEHOLDER,
        "not_production_threshold": True,
        "fact_status": "not_fact",
    }
    return {
        "schema_version": "ocr_input_readiness_scope_v1",
        "threshold_is_policy_placeholder": POLICY_PLACEHOLDER,
        "view_condition_scope": {
            "target_centering_requirement": "target_text_region_center_offset_ratio_max=0.25 (placeholder)",
            "viewing_angle_requirement": "max_oblique_angle_deg=25 (placeholder)",
            "perspective_distortion_limit": "skew_score_max=0.35 (placeholder)",
            "motion_stability_requirement": "inter_frame_motion_px_max=8 (placeholder)",
            "occlusion_limit": "occluded_area_ratio_max=0.20 (placeholder)",
            "frame_quality_requirement": "min_sharpness_score=0.55 (placeholder)",
            "failure_reason_codes": [
                "view_not_centered",
                "view_angle_too_oblique",
                "motion_blur",
                "occlusion",
            ],
            **ph,
        },
        "distance_scope": {
            "too_far_indicator": "estimated_text_pixel_height < min OR crop_height < 24px",
            "too_close_indicator": "bbox_clipped OR subject_fill_ratio > 0.85",
            "estimated_text_pixel_height_min": 12,
            "estimated_text_pixel_height_target": 24,
            "distance_repair_actions": ["ask_user_move_closer", "ask_user_step_back", "request_zoom"],
            "unrecoverable_distance_cases": ["target_unreachable", "hardware_capability_insufficient"],
            **ph,
        },
        "region_localization_scope": {
            "target_region_known": True,
            "region_anchor_required": True,
            "projected_region_allowed": True,
            "detected_region_preferred": True,
            "projection_drift_limit": "iou_with_detected_min=0.5 when detector available (placeholder)",
            "localization_failure_reason_codes": [
                "projection_drift",
                "bbox_wrong_region",
            ],
            **ph,
        },
        "bbox_geometry_scope": {
            "bbox_min_width": 48,
            "bbox_min_height": 16,
            "bbox_min_area": 768,
            "bbox_aspect_ratio_range": [0.15, 12.0],
            "bbox_overlap_requirement": "text_region_overlap_min=0.3 (placeholder)",
            "bbox_stability_requirement": "inter_frame_iou_min=0.85 across multiframe (placeholder)",
            "bbox_failure_reason_codes": [
                "bbox_too_small",
                "bbox_too_large",
                "bbox_wrong_region",
            ],
            **ph,
        },
        "text_readability_scope": {
            "brightness_requirement": "mean_luma_min=40 (placeholder 0-255)",
            "blur_requirement": "laplacian_var_min=50 (placeholder)",
            "contrast_requirement": "michelson_contrast_min=0.15 (placeholder)",
            "text_density_requirement": "max_lines_dynamic=3 (placeholder)",
            "short_text_marker_preferred": True,
            "long_text_requires_static_reading": True,
            "readability_failure_reason_codes": [
                "low_brightness",
                "low_contrast",
                "motion_blur",
                "text_too_dense",
                "text_too_long",
            ],
            **ph,
        },
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _hardware_placeholder() -> Dict[str, Any]:
    caps = [
        "zoom_available",
        "autofocus_available",
        "exposure_control_available",
        "resolution_control_available",
        "frame_rate_control_available",
        "high_quality_still_capture_available",
        "stabilization_available",
        "camera_pose_estimation_available",
    ]
    rows = [
        {
            "capability_name": c,
            "current_phase_invoked": False,
            "future_interface_hint": f"camera.{c.replace('_available', '')}",
            "required_signal": "policy_gate_pass",
            "governance_gate_required": True,
        }
        for c in caps
    ]
    return {
        "schema_version": "ocr_guidance_hardware_placeholder_contract_v1",
        "hardware_capability_unknown_allowed": True,
        "capabilities": {c: None for c in caps},
        "capability_rows": rows,
        "zoom_available": None,
        "autofocus_available": None,
        "exposure_control_available": None,
        "resolution_control_available": None,
        "frame_rate_control_available": None,
        "high_quality_still_capture_available": None,
        "stabilization_available": None,
        "camera_pose_estimation_available": None,
        "fact_status": "not_fact",
    }


def run_user_guidance_recovery_policy_v1(
    *,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    bbox_adjustment_root: str,
    text_detector_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    multiframe_ocr_v1_root: str,
    multiframe_crop_v1_root: str,
    text_region_tracklet_root: str,
    better_frame_root: str,
    multiframe_merge_proposal_root: str,
    source_validation_v2_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ocr2 = Path(ocr_v2_root).resolve()
    crop2 = Path(multiframe_crop_v2_root).resolve()
    cq = Path(crop_quality_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    ocr2_sum = _read_json(ocr2 / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}
    v1v2 = _read_json(ocr2 / "multiframe_ocr_v1_v2_comparison_report.json") or {}
    crop2_sum = _read_json(crop2 / "multiframe_crop_v2_textdetector_adjusted_summary.json") or {}

    v2_empty = int(ocr2_sum.get("v2_empty_result_count") or 0)
    v2_non_empty = int(ocr2_sum.get("v2_non_empty_result_count") or 0)
    v1_empty = int(v1v2.get("v1_empty_count") or 30)
    same_bbox = int(ocr2_sum.get("same_bbox_risk_count_observed") or 0)
    geom_sig = int(ocr2_sum.get("geometry_change_significant_count_observed") or 0)

    failure_rows = _failure_reason_taxonomy()
    ug_actions = _user_guidance_actions()
    sys_actions = _system_self_adjustments()
    ext_actions = _external_assistance_actions()
    stop_rows = _not_worth_ocr_policy()
    readiness = _readiness_scope()

    likely_reasons = [
        "repeated_empty_after_internal_retry",
        "projection_drift",
        "bbox_too_small",
        "view_not_centered",
        "target_too_far",
    ]
    if same_bbox >= v2_empty and v2_empty > 0:
        likely_reasons.insert(0, "geometry_change_insufficient_after_adjustment")

    current_case = {
        "schema_version": "user_guidance_current_case_recovery_decision_v1",
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "geometry_change_significant_count": geom_sig,
        "internal_recrop_retry_limit_reached_candidate": True,
        "ocr_input_not_readiness_confirmed": False,
        "likely_failure_reasons": likely_reasons,
        "recommended_policy_level": "OCR-L4",
        "recommended_next_phase": "STC-Sampling-Guidance-Policy-v1",
        "user_guidance_recovery_recommended": True,
        "system_self_adjustment_recommended": True,
        "external_assistance_recommended_conditionally": True,
        "runtime_action_committed": False,
        "tts_invoked": False,
        "provider_bridge_not_blocking": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    phase_hint = "GO"

    return {
        "summary": {
            "schema_version": "user_guidance_recovery_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "user_guidance_recovery_policy_only",
            "based_on_ocr_v2_result": ocr2.is_dir(),
            "based_on_crop_quality_diagnosis": cq.is_dir(),
            "ocr_v2_empty_result_count_observed": v2_empty,
            "ocr_v2_non_empty_result_count_observed": v2_non_empty,
            "user_guidance_recovery_policy_generated": True,
            "ocr_input_readiness_scope_defined": True,
            "view_condition_scope_defined": True,
            "distance_scope_defined": True,
            "region_localization_scope_defined": True,
            "bbox_geometry_scope_defined": True,
            "text_readability_scope_defined": True,
            "repairability_policy_defined": True,
            "hardware_control_placeholder_defined": True,
            "user_guidance_candidate_generated": True,
            "system_self_adjustment_candidate_generated": True,
            "external_assistance_candidate_generated": True,
            "runtime_tts_invoked": False,
            "runtime_guidance_action_committed": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": phase_hint,
        },
        "readiness_scope": readiness,
        "activation_levels": {
            "schema_version": "ocr_activation_recovery_level_policy_v1",
            "levels": _ocr_activation_levels(),
            "fact_status": "not_fact",
        },
        "task_criticality": {
            "schema_version": "user_guidance_task_criticality_matrix_v1",
            "row_count": len(_task_criticality_rows()),
            "rows": _task_criticality_rows(),
        },
        "failure_taxonomy": {
            "schema_version": "ocr_input_failure_reason_taxonomy_v1",
            "reason_count": len(failure_rows),
            "reasons": failure_rows,
        },
        "repairability": _repairability_policy(),
        "user_guidance_actions": {
            "schema_version": "user_guidance_action_candidate_policy_v1",
            "action_count": len(ug_actions),
            "actions": ug_actions,
        },
        "system_self_adjustment": {
            "schema_version": "system_self_adjustment_candidate_policy_v1",
            "action_count": len(sys_actions),
            "actions": sys_actions,
        },
        "external_assistance": {
            "schema_version": "external_assistance_candidate_policy_v1",
            "action_count": len(ext_actions),
            "actions": ext_actions,
        },
        "not_worth_ocr": {
            "schema_version": "ocr_not_recoverable_or_not_worth_policy_v1",
            "stop_reason_count": len(stop_rows),
            "stops": stop_rows,
        },
        "current_case": current_case,
        "hardware_placeholder": _hardware_placeholder(),
        "stc_link": {
            "schema_version": "ocr_guidance_stc_vision_capture_link_report_v1",
            "stc_link_required": True,
            "vision_capture_governance_link_required": True,
            "spatial_temporal_validity_required": True,
            "capture_quality_feedback_required": True,
            "ocr_timeout_and_retry_budget_required": True,
            "future_phase_candidates": FUTURE_STC_PHASES,
            "fact_status": "not_fact",
        },
        "boundary": {
            "schema_version": "user_guidance_recovery_boundary_report_v1",
            "policy_only": True,
            "tts_invoked": False,
            "runtime_guidance_action_committed": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "review_decision_committed": False,
            "approval_granted": False,
            "fact_write_allowed": False,
            "world_model_attach_allowed": False,
            "scene_delta_candidate_allowed": False,
            "navigation_decision_allowed": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "user_guidance_recovery_metrics_candidate_report_v1",
            "recovery_policy_generated": True,
            "readiness_scope_defined": True,
            "failure_reason_count": len(failure_rows),
            "user_guidance_action_count": len(ug_actions),
            "system_self_adjustment_action_count": len(sys_actions),
            "external_assistance_action_count": len(ext_actions),
            "not_recoverable_stop_reason_count": len(stop_rows),
            "hardware_placeholder_count": 8,
            "runtime_action_committed_count": 0,
            "tts_invoked_count": 0,
            "ocr_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
            "can_feed_future_t1_collector": True,
        },
        "benchmark_link": {
            "schema_version": "user_guidance_recovery_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "user_guidance_recovery_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "user_guidance_recovery_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "tts_invoked": False,
            "runtime_guidance_action_committed": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "user_guidance_recovery_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "user_guidance_recovery_non_claims_report_v1",
            "claims": [
                "no_runtime_user_guidance_execution",
                "no_tts",
                "no_hardware_invoke",
                "readiness_scope_is_policy_placeholder",
                "guidance_actions_are_candidates_not_runtime",
                "system_adjustment_is_candidate_not_hardware",
                "external_assistance_is_candidate_not_request",
                "no_ocr_in_this_phase",
                "no_world_model_write",
                "no_scene_delta",
                "not_benchmark",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "user_guidance_recovery_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "user_guidance_recovery_audit_report_v1",
            "user_guidance_recovery_policy_v1_executed": True,
            "policy_only": True,
            "ocr_input_readiness_scope_defined": True,
            "repairability_policy_defined": True,
            "hardware_control_placeholder_defined": True,
            "runtime_tts_invoked": False,
            "runtime_guidance_action_committed": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "new_crop_generated": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "decision_committed": False,
            "approval_granted": False,
            "auto_approve_invoked": False,
            "fact_review_generated": False,
            "world_model_attach_executed": False,
            "scene_delta_candidate_generated": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "model_selection_claimed": False,
            "production_readiness_claimed": False,
        },
    }
