# -*- coding: utf-8 -*-
"""Vision Capture Governance v1 — input quality, readiness, capture routing (policy only).

Phase-Vision-Capture-Governance-v1-001

Governance after OCR activation: how to obtain usable capture input without runtime camera/OCR.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Vision-Capture-Governance-v1-001"

FOLLOWUPS = [
    "OCR-Activation-Runtime-DryRun-v1",
    "User-Guidance-Recovery-Runtime-DryRun-v1",
    "Vision-Capture-Runtime-DryRun-v1",
    "STC-Freshness-Gate-Runtime-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Expired-Capture-Candidate-Ingest-v1",
    "World-Change-Hint-Candidate-DryRun-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

QUALITY_DIMENSIONS = [
    "blur",
    "brightness",
    "contrast",
    "occlusion",
    "motion_stability",
    "target_centering",
    "perspective_angle",
    "text_pixel_height",
    "bbox_size",
    "bbox_stability",
    "region_confidence",
]

CANDIDATE_METADATA_REQUIRED = [
    "source_chain",
    "time_anchor",
    "spatial_anchor",
    "original_task_context",
    "stale_reason",
    "confidence_decay",
    "privacy_sensitivity",
    "future_usage_scope",
]

LONG_TERM_POOLS = [
    "expired_observation_candidate",
    "world_change_hint_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _gate_row(
    gate_name: str,
    required: List[str],
    pass_cond: str,
    fail_cond: str,
    repair: str,
    allowed: List[str],
    blocked: List[str],
) -> Dict[str, Any]:
    return {
        "gate_name": gate_name,
        "required_signals": required,
        "quality_dimensions": QUALITY_DIMENSIONS,
        "pass_condition": pass_cond,
        "fail_condition": fail_cond,
        "repairability_category": repair,
        "allowed_next_action": allowed,
        "blocked_next_action": blocked,
        "fact_status_after_gate": "not_fact",
        "write_allowed_after_gate": False,
    }


def _capture_quality_gate() -> Dict[str, Any]:
    gates = [
        _gate_row(
            "frame_quality_gate",
            ["blur_score", "brightness_score", "motion_stability", "frame_time_anchor"],
            "blur_acceptable_and_brightness_in_range_and_motion_stable",
            "frame_blurry_or_dark_or_unstable",
            "user_or_system_repairable",
            ["continue_sampling", "request_higher_quality_frame", "system_self_adjustment"],
            ["ocr_invoke", "fact_write"],
        ),
        _gate_row(
            "region_quality_gate",
            ["region_confidence", "bbox_stability", "spatial_anchor"],
            "region_localized_and_confidence_above_threshold",
            "region_low_confidence_or_unstable_bbox",
            "user_repairable",
            ["recenter_target", "user_guidance", "request_resampling"],
            ["crop_for_ocr_without_region_pass"],
        ),
        _gate_row(
            "crop_quality_gate",
            ["bbox_size", "text_pixel_height", "perspective_angle", "occlusion"],
            "crop_large_enough_and_readable_angle",
            "bbox_too_small_or_oblique_or_occluded",
            "user_or_system_repairable",
            ["request_zoom", "user_guidance", "static_capture"],
            ["dynamic_ocr_on_bad_crop"],
        ),
        _gate_row(
            "text_region_quality_gate",
            ["text_region_detected", "detected_region_preferred_over_projection"],
            "detected_text_region_available",
            "projection_only_without_detected_text_region",
            "system_or_user_repairable",
            ["request_heavy_text_detector_capture", "static_capture"],
            ["treat_projection_crop_as_ground_truth"],
        ),
        _gate_row(
            "task_capture_quality_gate",
            ["task_context", "capture_mode_match", "readiness_aggregate"],
            "task_critical_and_capture_mode_matches_task_type",
            "task_not_critical_or_wrong_capture_mode",
            "routing",
            ["task_triggered_capture", "assisted_static_reading", "visual_semantic_first"],
            ["force_dynamic_on_dense_text"],
        ),
    ]
    return {
        "schema_version": "vision_capture_quality_gate_policy_v1",
        "gates": gates,
        "capture_readiness_not_ocr_success": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _frame_readiness_gate() -> Dict[str, Any]:
    return {
        "schema_version": "vision_frame_readiness_gate_v1",
        "frame_id_or_ref": "placeholder_current_multiframe_frame_ref",
        "source_phase": "Multiframe-Crop-Execution-DryRun-v2-TextDetectorAdjusted-001",
        "policy_only_no_new_frame": True,
        "available_signals": ["blur_score_available", "brightness_score_available", "crop_quality_placeholder"],
        "blur_score_available": True,
        "brightness_score_available": True,
        "frame_time_anchor_required": True,
        "spatial_anchor_required": True,
        "freshness_required_for_action": True,
        "stale_blocks_action": True,
        "stale_allows_long_term_candidate": True,
        "readiness_status": "policy_defined_placeholder",
        "better_frame_reference_placeholder": "crop_quality_diagnosis_v2_multiframe",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _region_crop_text_readiness() -> Dict[str, Any]:
    layer_common = {
        "staleness_policy": "stale_blocks_action_allows_long_term_candidate",
        "heuristic_candidate_not_fact": True,
        "fact_status": "not_fact",
    }

    region = {
        "layer": "region_readiness",
        "required_inputs": ["frame_pass", "region_bbox", "region_confidence"],
        "quality_signals": ["region_confidence", "bbox_stability", "alignment_requirements"],
        "bbox_requirements": ["min_size", "stability_across_frames", "same_bbox_risk_limit"],
        "alignment_requirements": ["target_centered", "perspective_within_limit"],
        "confidence_requirements": ["above_region_threshold"],
        "projection_crop_is_not_detected_text_region": True,
        "detected_region_preferred": True,
        "same_bbox_risk_limits_improvement_expectation": True,
        "failure_routes": ["user_guidance", "system_self_adjustment", "expired_capture_candidate"],
        "repair_routes": ["recenter", "resample", "request_detected_region"],
        **layer_common,
    }
    crop = {
        "layer": "crop_readiness",
        "required_inputs": ["region_pass", "crop_bbox", "crop_source_type"],
        "quality_signals": ["bbox_size", "text_pixel_height", "blur", "occlusion"],
        "bbox_requirements": ["not_projection_only_when_detection_available"],
        "alignment_requirements": ["text_region_aligned"],
        "confidence_requirements": ["crop_quality_gate_pass"],
        "projection_crop_note": "projection crop is not detected text region",
        "detected_region_preferred": True,
        "same_bbox_risk_limits_improvement_expectation": True,
        "failure_routes": ["static_capture", "user_guidance", "abandon_ocr_action"],
        "repair_routes": ["zoom", "autofocus", "static_capture"],
        **layer_common,
    }
    text_region = {
        "layer": "text_region_readiness",
        "required_inputs": ["crop_pass", "text_detector_signal_optional"],
        "quality_signals": ["text_region_detected", "readability_hint"],
        "bbox_requirements": ["detected_text_bbox_preferred"],
        "alignment_requirements": ["text_upright_readable"],
        "confidence_requirements": ["text_region_confidence_if_available"],
        "failure_routes": [
            "text_region_not_detected",
            "assisted_static_reading",
            "visual_semantic_first",
        ],
        "repair_routes": ["heavy_text_detector_capture", "static_capture"],
        **layer_common,
    }
    return {
        "schema_version": "vision_region_crop_text_readiness_gate_v1",
        "region_readiness": region,
        "crop_readiness": crop,
        "text_region_readiness": text_region,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _dynamic_vs_static_capture() -> Dict[str, Any]:
    dynamic_types = [
        "safety_short_marker",
        "doorplate",
        "room_number",
        "exit_entry_sign",
        "transit_line_number",
        "shop_short_name_confirmation",
    ]
    static_types = [
        "long_notice",
        "menu_full_reading",
        "medicine_label_detail",
        "document",
        "dense_text_layout",
        "repeated_dynamic_empty",
        "high_precision_required",
    ]
    rows = []
    for t in dynamic_types:
        rows.append(
            {
                "capture_mode": "dynamic",
                "allowed_task_types": [t],
                "blocked_task_types": static_types,
                "required_motion_state": "brief_hold_or_slow_approach",
                "required_capture_quality": "crop_and_text_region_pass",
                "user_guidance_required": False,
                "system_self_adjustment_allowed": True,
                "fallback_policy": "user_guidance_then_static_if_empty",
                "fact_status": "not_fact",
            }
        )
    for t in static_types:
        rows.append(
            {
                "capture_mode": "static",
                "allowed_task_types": [],
                "blocked_task_types": [],
                "required_motion_state": "hold_still_or_tripod_assist",
                "required_capture_quality": "high_resolution_still",
                "user_guidance_required": t in ("repeated_dynamic_empty", "dense_text_layout"),
                "system_self_adjustment_allowed": True,
                "fallback_policy": "assisted_static_reading_or_visual_semantic_first",
                "static_required_for": t,
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "vision_dynamic_vs_static_capture_policy_v1",
        "dynamic_capture_allowed_for": dynamic_types,
        "static_capture_required_for": static_types,
        "rows": rows,
        "dynamic_not_for_complex_reading": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _hardware_placeholder() -> Dict[str, Any]:
    caps = [
        ("zoom_available", "medium", "request_zoom"),
        ("optical_zoom_available", "medium", "request_optical_zoom"),
        ("digital_zoom_available", "low", "request_digital_zoom"),
        ("autofocus_available", "low", "request_autofocus"),
        ("exposure_control_available", "low", "request_exposure"),
        ("resolution_control_available", "low", "request_high_resolution_still"),
        ("frame_rate_control_available", "low", "request_resampling"),
        ("high_quality_still_capture_available", "medium", "static_capture"),
        ("stabilization_available", "low", "multiframe_stabilization"),
        ("camera_pose_estimation_available", "medium", "pose_guidance"),
        ("depth_or_tof_available", "high", "depth_assist_capture"),
    ]
    return {
        "schema_version": "vision_capture_hardware_placeholder_contract_v1",
        "hardware_capability_unknown_allowed": True,
        "capabilities": [
            {
                "capability_name": name,
                "current_phase_invoked": False,
                "future_interface_hint": hint,
                "required_input_signal": "capture_quality_gate_fail_or_task_requirement",
                "governance_gate_required": True,
                "privacy_or_safety_risk": risk,
            }
            for name, risk, hint in caps
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _system_self_adjustment() -> Dict[str, Any]:
    actions = [
        ("request_zoom", "bbox_too_small", "zoom_available", "text_pixel_height", "medium", "low"),
        ("request_autofocus", "blur_or_misfocus", "autofocus_available", "blur_score", "low", "low"),
        ("request_exposure_adjustment", "frame_too_dark_or_overexposed", "exposure_control_available", "brightness", "low", "low"),
        ("request_high_resolution_still_frame", "high_precision_required", "high_quality_still_capture_available", "detail", "high", "medium"),
        ("request_resampling", "low_region_confidence", "frame_rate_control_available", "region_confidence", "medium", "medium"),
        ("request_multiframe_stabilization", "motion_unstable", "stabilization_available", "motion_stability", "medium", "medium"),
        ("request_camera_pose_estimation", "perspective_oblique", "camera_pose_estimation_available", "perspective_angle", "medium", "low"),
        ("request_heavy_text_detector_capture", "text_region_not_detected", "resolution_control_available", "detection", "high", "high"),
        ("request_static_capture_mode", "repeated_dynamic_empty", "high_quality_still_capture_available", "readability", "high", "medium"),
    ]
    return {
        "schema_version": "vision_capture_system_self_adjustment_policy_v1",
        "actions": [
            {
                "action_id": aid,
                "trigger_reason": reason,
                "required_hardware_capability": cap,
                "expected_signal_improvement": sig,
                "latency_cost": lat,
                "power_cost": pwr,
                "blocked_when": ["unsafe_to_continue_capture", "not_task_critical"],
                "hardware_action_invoked_now": False,
                "runtime_action_committed_now": False,
                "fact_status": "not_fact",
            }
            for aid, reason, cap, sig, lat, pwr in actions
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _user_guidance_capture() -> Dict[str, Any]:
    actions = [
        ("ask_user_move_closer", "target_too_far", "请靠近一些，让文字更大更清晰", "distance", "low", "low"),
        ("ask_user_center_target", "target_not_centered", "请将目标移到画面中央", "centering", "low", "low"),
        ("ask_user_adjust_angle", "perspective_too_oblique", "请稍微调整手机角度", "angle", "low", "low"),
        ("ask_user_hold_still", "user_motion_unstable", "请保持稳定，避免晃动", "motion", "low", "low"),
        ("ask_user_raise_camera", "target_too_low_in_frame", "请稍微抬高手机", "pose", "low", "low"),
        ("ask_user_lower_camera", "target_too_high_in_frame", "请稍微放低手机", "pose", "low", "low"),
        ("ask_user_increase_light", "frame_too_dark", "请增加光线或避开逆光", "brightness", "low", "low"),
        ("ask_user_pause_for_static_capture", "static_capture_required", "请停稳后我再读取", "static", "medium", "low"),
        ("ask_user_try_zoom_or_magnification", "text_too_small", "可尝试放大或靠近", "zoom", "medium", "low"),
        ("request_external_assistance_if_needed", "user_unable", "需要时请寻求旁人帮助", "external", "high", "medium"),
    ]
    return {
        "schema_version": "vision_capture_user_guidance_policy_v1",
        "actions": [
            {
                "action_id": aid,
                "trigger_reason": reason,
                "suggested_prompt_template": tmpl,
                "expected_capture_improvement": imp,
                "user_effort_level": effort,
                "safety_risk_level": risk,
                "blocked_when": ["unsafe_to_continue_capture"],
                "tts_allowed_now": False,
                "runtime_action_committed_now": False,
                "fact_status": "not_fact",
            }
            for aid, reason, tmpl, imp, effort, risk in actions
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _failure_taxonomy() -> Dict[str, Any]:
    reasons = [
        ("frame_blurry", ["blur_high"], "hold_still", "request_autofocus", "external_assistance", "retry_then_ug"),
        ("frame_too_dark", ["brightness_low"], "increase_light", "request_exposure", None, "retry"),
        ("frame_overexposed", ["brightness_high"], "reduce_glare", "request_exposure", None, "retry"),
        ("low_contrast", ["contrast_low"], "adjust_angle", "request_exposure", None, "retry"),
        ("target_not_centered", ["centering_fail"], "center_target", "resample", None, "retry"),
        ("target_too_far", ["text_pixel_small"], "move_closer", "request_zoom", None, "retry"),
        ("target_too_close", ["bbox_clip"], "move_back", None, None, "retry"),
        ("perspective_too_oblique", ["angle_high"], "adjust_angle", "pose_estimation", None, "retry"),
        ("target_occluded", ["occlusion"], "clear_view", None, "external", "stop_or_ug"),
        ("user_motion_unstable", ["motion_user"], "hold_still", "stabilization", None, "retry"),
        ("camera_motion_unstable", ["motion_camera"], "hold_still", "stabilization", None, "retry"),
        ("bbox_too_small", ["bbox_area_small"], "move_closer", "request_zoom", None, "retry"),
        ("bbox_wrong_region", ["region_mismatch"], "recenter", "redetect", None, "ug"),
        ("projection_drift", ["projection_not_detected"], "static_capture", "heavy_detector", None, "static"),
        ("text_region_not_detected", ["no_text_region"], "static_capture", "heavy_detector", None, "static_or_semantic"),
        ("text_too_dense_for_dynamic", ["dense_layout"], "static_capture", None, None, "static"),
        ("repeated_empty_after_capture_retry", ["ocr_empty_repeat"], "static_or_ug", None, "external", "stop_recrop"),
        ("hardware_capability_insufficient", ["cap_missing"], None, None, "external", "downgrade"),
        ("unsafe_to_continue_capture", ["safety_block"], None, None, "external", "stop"),
        ("not_task_critical", ["task_low"], None, None, None, "visual_semantic_first"),
    ]
    return {
        "schema_version": "vision_capture_failure_reason_taxonomy_v1",
        "reasons": [
            {
                "reason_code": code,
                "detectable_signals": sigs,
                "user_repair_action": u,
                "system_repair_action": s,
                "external_assistance_action": e,
                "stop_condition": stop,
                "long_term_candidate_allowed": code
                in ("projection_drift", "repeated_empty_after_capture_retry", "text_region_not_detected"),
                "fact_status": "not_fact",
            }
            for code, sigs, u, s, e, stop in reasons
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _retry_timeout_stale() -> Dict[str, Any]:
    return {
        "schema_version": "vision_capture_retry_timeout_stale_policy_v1",
        "max_dynamic_capture_retry": 2,
        "max_static_capture_retry": 2,
        "max_repeated_empty_after_capture_retry": 2,
        "max_capture_window_sec": 45,
        "frame_stale_ms": 3000,
        "region_stale_ms": 2500,
        "crop_stale_ms": 2000,
        "text_region_stale_ms": 2000,
        "stale_blocks_action": True,
        "stale_blocks_fact_write": True,
        "stale_allows_long_term_candidate": True,
        "retry_exhausted_routes_to": [
            "user_guidance_recovery",
            "system_self_adjustment",
            "external_assistance",
            "expired_capture_candidate",
            "task_downgrade_non_ocr_path",
        ],
        "capture_decision_options": [
            "continue_sampling",
            "request_higher_quality_frame",
            "request_zoom_autofocus_exposure_resampling",
            "user_guidance",
            "assisted_static_reading",
            "abandon_current_ocr_action",
            "expired_historical_candidate",
            "visual_semantic_first_path",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _expired_capture_candidates() -> List[Dict[str, Any]]:
    types = [
        "expired_frame_candidate",
        "expired_region_candidate",
        "expired_crop_candidate",
        "expired_text_region_candidate",
        "expired_capture_attempt_candidate",
    ]
    meta = {k: True for k in CANDIDATE_METADATA_REQUIRED}
    return [
        {
            "candidate_type": t,
            "cannot_use_for_action": True,
            "cannot_write_fact": True,
            "can_feed_expired_observation_candidate": True,
            "can_feed_world_change_hint_candidate": True,
            "can_feed_user_environment_context_candidate": True,
            "can_feed_user_profile_context_candidate": True,
            "can_feed_emotional_context_background_candidate": True,
            "required_metadata": CANDIDATE_METADATA_REQUIRED,
            **meta,
            "fact_status": "not_fact",
        }
        for t in types
    ]


def _long_term_routing() -> List[Dict[str, Any]]:
    routes = [
        ("expired_capture", "expired_observation_candidate", "historical_anchor", "current_action"),
        ("repeated_unreadable_region", "unresolved_history_slot", "change_tracking", "fact_write"),
        ("safety_marker_seen_then_stale", "world_change_hint_candidate", "safety_env_change", "immediate_tts"),
        ("recurring_place_context", "user_environment_context_candidate", "living_environment", "profile_write_now"),
        ("recurring_task_context", "user_profile_context_candidate", "activity_habit", "fact_write"),
        ("emotionally_relevant_environment", "emotional_context_background_candidate", "emotion_background", "immediate_inference"),
    ]
    return [
        {
            "source_signal": src,
            "target_candidate_pool": pool,
            "allowed_use": allowed,
            "forbidden_use": forbidden,
            "review_required": True,
            "write_allowed_now": False,
            "fact_status": "not_fact",
        }
        for src, pool, allowed, forbidden in routes
    ]


def _safety_marker_capture_path() -> Dict[str, Any]:
    return {
        "schema_version": "vision_safety_marker_capture_path_policy_v1",
        "safety_marker_background_capture_allowed": True,
        "visual_symbol_first": True,
        "warning_icon_first": True,
        "short_text_ocr_later": True,
        "full_text_ocr_forbidden_by_default": True,
        "capture_quality_requirement": "low_latency_short_marker",
        "latency_budget_hint_ms": 800,
        "staleness_tolerance": "short_for_action_long_for_hint",
        "speech_escalation_hint": "safety_only_not_general_narration",
        "current_phase_runtime_action": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _task_triggered_capture_path() -> Dict[str, Any]:
    scenarios = [
        "destination_arrival_confirmation",
        "shop_name_confirmation",
        "doorplate_room_number",
        "hospital_department_room",
        "transit_line_platform",
        "ticket_window_number",
        "elevator_floor_confirmation",
        "public_facility_confirmation",
    ]
    return {
        "schema_version": "vision_task_triggered_capture_path_policy_v1",
        "midplatform_pre_activation_required": True,
        "task_context_required": True,
        "geolocation_or_route_progress_required": True,
        "capture_pre_activation_window_placeholder": {"distance_m": 50, "time_sec": 35},
        "capture_target_prediction_required": True,
        "visual_semantic_first": True,
        "ocr_confirm_later": True,
        "current_phase_runtime_action": False,
        "task_scenarios": scenarios,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_vision_capture_governance_v1(
    *,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    user_guidance_root: str,
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
    ocr_act = Path(ocr_activation_root).resolve()
    stc = Path(stc_sampling_guidance_root).resolve()
    ug = Path(user_guidance_root).resolve()
    ocr2 = Path(ocr_v2_root).resolve()
    crop_v2 = Path(multiframe_crop_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    ocr_current = _read_json(ocr_act / "ocr_activation_current_case_decision_dryrun_v1.json") or {}
    stc_case = _read_json(stc / "stc_current_case_decision_dryrun_v1.json") or {}

    v1_empty = int(ocr_current.get("v1_empty_count") or stc_case.get("v1_empty_count") or 30)
    v2_empty = int(ocr_current.get("v2_empty_count") or stc_case.get("v2_empty_count") or 5)
    same_bbox = int(ocr_current.get("same_bbox_risk_count") or 5)

    hw = _hardware_placeholder()
    sys_adj = _system_self_adjustment()
    ug_cap = _user_guidance_capture()
    fail_tax = _failure_taxonomy()
    expired = _expired_capture_candidates()
    lt_route = _long_term_routing()

    current_case = {
        "schema_version": "vision_capture_current_case_decision_dryrun_v1",
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "geometry_change_significant_count": 0,
        "dynamic_reocr_allowed_now": False,
        "capture_quality_problem_likely": True,
        "projection_or_region_alignment_problem_likely": True,
        "internal_recrop_should_stop": True,
        "recommended_capture_decision": "USER_GUIDANCE_OR_STATIC_CAPTURE",
        "system_self_adjustment_candidate_allowed": True,
        "expired_capture_candidate_allowed": True,
        "long_term_context_candidate_allowed": True,
        "runtime_action_committed": False,
        "tts_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "vision_capture_governance_v1_summary_v0",
            "phase": PHASE_ID,
            "governance_scope": "vision_capture_governance_policy_only",
            "based_on_ocr_activation_governance": ocr_act.is_dir(),
            "based_on_stc_sampling_guidance": stc.is_dir(),
            "based_on_user_guidance_recovery": ug.is_dir(),
            "capture_quality_gate_defined": True,
            "frame_readiness_gate_defined": True,
            "region_readiness_gate_defined": True,
            "crop_readiness_gate_defined": True,
            "text_region_capture_readiness_defined": True,
            "dynamic_capture_policy_defined": True,
            "static_capture_policy_defined": True,
            "zoom_autofocus_exposure_resampling_placeholder_defined": True,
            "hardware_capability_placeholder_defined": True,
            "capture_failure_reason_taxonomy_defined": True,
            "capture_retry_timeout_stale_policy_defined": True,
            "expired_capture_candidate_policy_defined": True,
            "long_term_context_candidate_routing_defined": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
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
        "quality_gate": _capture_quality_gate(),
        "frame_readiness": _frame_readiness_gate(),
        "region_crop_text": _region_crop_text_readiness(),
        "dynamic_vs_static": _dynamic_vs_static_capture(),
        "hardware": hw,
        "system_self_adjustment": sys_adj,
        "user_guidance": ug_cap,
        "failure_taxonomy": fail_tax,
        "retry_stale": _retry_timeout_stale(),
        "expired_capture": {
            "schema_version": "vision_expired_capture_candidate_policy_v1",
            "candidates": expired,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term_routing": {
            "schema_version": "vision_long_term_context_candidate_routing_policy_v1",
            "routes": lt_route,
            "target_pools": LONG_TERM_POOLS,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "safety_path": _safety_marker_capture_path(),
        "task_path": _task_triggered_capture_path(),
        "current_case": current_case,
        "ocr_activation_link": {
            "schema_version": "vision_capture_ocr_activation_link_report_v1",
            "linked_to_ocr_activation_governance": ocr_act.is_dir(),
            "ocr_default_off_for_world_modeling": True,
            "visual_semantic_first": True,
            "safety_task_dual_trigger_respected": True,
            "action_freshness_vs_historical_value_respected": True,
            "expired_information_value_principle_respected": True,
            "future_phase": "OCR-Activation-Runtime-DryRun-v1",
            "alternate_future_phase": "User-Guidance-Recovery-Runtime-DryRun-v1",
        },
        "stc_link": {
            "schema_version": "vision_capture_stc_link_report_v1",
            "linked_to_stc_sampling_guidance": stc.is_dir(),
            "freshness_gate_required": True,
            "sampling_window_required": True,
            "stale_policy_required": True,
            "route_progress_pre_activation_supported": True,
            "no_runtime_sampling_now": True,
        },
        "boundary": {
            "schema_version": "vision_capture_governance_boundary_report_v1",
            "governance_policy_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
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
            "schema_version": "vision_capture_governance_metrics_candidate_report_v1",
            "capture_quality_gate_defined": True,
            "frame_readiness_gate_defined": True,
            "region_readiness_gate_defined": True,
            "crop_readiness_gate_defined": True,
            "text_region_capture_readiness_defined": True,
            "hardware_placeholder_count": len(hw.get("capabilities") or []),
            "system_self_adjustment_action_count": len(sys_adj.get("actions") or []),
            "user_guidance_action_count": len(ug_cap.get("actions") or []),
            "capture_failure_reason_count": len(fail_tax.get("reasons") or []),
            "expired_capture_candidate_type_count": len(expired),
            "long_term_context_routing_count": len(lt_route),
            "runtime_action_committed_count": 0,
            "runtime_camera_invoked_count": 0,
            "ocr_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "vision_capture_governance_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "vision_capture_governance_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "vision_capture_governance_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "governance_policy_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
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
            "schema_version": "vision_capture_governance_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "vision_capture_governance_non_claims_report_v1",
            "claims": [
                "no_runtime_camera",
                "no_new_frame_capture",
                "no_runtime_ocr",
                "no_tts",
                "no_hardware_invoke",
                "capture_readiness_is_policy_not_image_certification",
                "hardware_placeholder_not_capability_certification",
                "expired_capture_candidate_not_fact",
                "long_term_context_not_profile_write",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "vision_capture_governance_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "vision_capture_governance_audit_report_v1",
            "vision_capture_governance_v1_executed": True,
            "governance_policy_only": True,
            "capture_quality_gate_defined": True,
            "hardware_capability_placeholder_defined": True,
            "expired_capture_candidate_policy_defined": True,
            "long_term_context_candidate_routing_defined": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "runtime_tts_invoked": False,
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
        "input_refs": {
            "ocr_activation_root": str(ocr_act),
            "multiframe_crop_v2_root": str(crop_v2),
            "ocr_v2_root": str(ocr2),
        },
    }
