# -*- coding: utf-8 -*-
"""STC Sampling Guidance Policy v1 — safety/task dual-trigger, pre-activation, validity (policy only).

Phase-STC-Sampling-Guidance-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "STC-Sampling-Guidance-Policy-v1-001"
RUNTIME_STEP = "stc_sampling_guidance_policy_v1"
POLICY_PLACEHOLDER = True

FOLLOWUPS = [
    "OCR-Activation-Governance-Policy-v1",
    "Vision-Capture-Governance-v1",
    "User-Guidance-Recovery-Runtime-DryRun-v1",
    "Voice-Guidance-Prompt-Template-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Dynamic-Short-Text-Reading-Scope-v1",
    "Safety-Marker-Background-Scan-Policy-v1",
    "Task-Triggered-OCR-PreActivation-Policy-v1",
    "Hardware-Camera-Control-Contract-v1",
]

SAFETY_MARKER_TYPES = [
    "warning_sign",
    "danger_text",
    "forbidden_entry",
    "construction",
    "maintenance",
    "exit_entry",
    "emergency_marker",
    "wet_floor",
    "traffic_warning",
    "platform_warning",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _safety_trigger_policy() -> Dict[str, Any]:
    return {
        "schema_version": "stc_safety_trigger_policy_v1",
        "trigger_class": "safety",
        "default_background_enabled": True,
        "user_prompt_required": False,
        "high_priority": True,
        "target_marker_types": SAFETY_MARKER_TYPES,
        "preferred_detection_path": [
            "visual_symbol_first",
            "warning_icon_first",
            "short_text_ocr_second",
        ],
        "full_text_ocr_forbidden_by_default": True,
        "allowed_activation_level": ["OCR-L1", "OCR-L2"],
        "blocked_actions": [
            "full_frame_ocr",
            "long_text_dynamic_read",
            "world_model_fact_write",
            "autonomous_navigation_from_ocr",
        ],
        "sampling_frequency_hint_hz": 2.0,
        "latency_budget_hint_ms": 500,
        "speech_policy_hint": "safety_alert_candidate_only_no_tts_in_policy_phase",
        "fact_status_after_trigger": "not_fact",
        "runtime_executed_in_this_phase": False,
        "write_allowed": False,
    }


def _task_trigger_scenarios() -> List[Dict[str, Any]]:
    specs = [
        ("destination_arrival_confirmation", 80, 45, ["task_goal", "route_progress", "geolocation"], "visual_semantic_then_ocr_l1", "OCR-L2", "OCR-L3", True, False),
        ("shop_name_confirmation", 50, 30, ["task_goal", "poi_hint", "geolocation"], "visual_logo_poi_then_ocr_l1", "OCR-L1", "OCR-L3", True, False),
        ("hospital_department_room", 60, 40, ["task_goal", "indoor_map", "route_progress"], "visual_landmark_then_ocr_l2", "OCR-L2", "OCR-L3", True, False),
        ("doorplate_room_number", 25, 15, ["task_goal", "proximity"], "short_text_ocr_l2", "OCR-L2", "OCR-L3", True, False),
        ("transit_line_platform", 100, 60, ["task_goal", "route_progress", "transit_context"], "visual_symbol_then_ocr_l2", "OCR-L2", "OCR-L4", True, False),
        ("ticket_window_number", 40, 25, ["task_goal", "facility_type"], "short_text_ocr_l2", "OCR-L2", "OCR-L3", True, False),
        ("elevator_floor_confirmation", 30, 20, ["task_goal", "vertical_navigation"], "short_text_ocr_l2", "OCR-L2", "OCR-L3", True, False),
        ("public_facility_confirmation", 45, 30, ["task_goal", "poi_hint"], "visual_symbol_first", "OCR-L0", "OCR-L1", False, False),
        ("safety_marker_near_task_path", 60, 35, ["route_progress", "safety_corridor"], "safety_trigger_overlay", "OCR-L2", "OCR-L2", False, False),
    ]
    return [
        {
            "task_type": tt,
            "pre_activation_distance_m": dist,
            "pre_activation_time_sec": tsec,
            "required_context": ctx,
            "preferred_first_path": path,
            "ocr_activation_level": level,
            "fallback_path": fb,
            "user_guidance_allowed": ug,
            "static_reading_required": static,
            "fact_status": "not_fact",
        }
        for tt, dist, tsec, ctx, path, level, fb, ug, static in specs
    ]


def _task_trigger_policy() -> Dict[str, Any]:
    return {
        "schema_version": "stc_task_trigger_prediction_policy_v1",
        "trigger_class": "task",
        "user_prompt_required": False,
        "task_context_required": True,
        "geolocation_required_or_optional": "required_or_optional_by_scenario",
        "route_progress_required": True,
        "midplatform_pre_activation_required": True,
        "ocr_self_activation_allowed": False,
        "activation_authority": "midplatform_task_chain_plus_stc_plus_geolocation",
        "scenarios": _task_trigger_scenarios(),
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _geolocation_route_policy() -> Dict[str, Any]:
    return {
        "schema_version": "stc_geolocation_route_pre_activation_policy_v1",
        "threshold_is_policy_placeholder": POLICY_PLACEHOLDER,
        "geolocation_signal_types": [
            "gps",
            "map_poi",
            "indoor_map",
            "route_progress",
            "last_known_location",
            "visual_landmark_anchor",
        ],
        "pre_activation_window": {
            "distance_m_placeholder": {"min": 15, "default": 50, "max": 120},
            "time_sec_placeholder": {"min": 10, "default": 35, "max": 90},
            "confidence_requirement": "location_confidence_min=0.6 (placeholder)",
        },
        "route_progress_pre_activation_policy_defined": True,
        "activation_conditions": [
            "task_active",
            "remaining_distance_m <= pre_activation_distance_m",
            "eta_sec <= pre_activation_time_sec",
            "stc_spatial_temporal_valid",
            "capture_quality_gate_pass_or_degraded_ok",
        ],
        "blocked_when": [
            "stale_location",
            "stale_route_progress",
            "user_motion_fast_walk_or_vehicle",
            "ocr_retry_budget_exhausted",
            "not_recoverable_by_ocr",
        ],
        "stale_location_policy": "invalidate_pre_activation_if_location_age_ms > 30000 (placeholder)",
        "no_real_map_api_invoked": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _sampling_validity_window() -> Dict[str, Any]:
    return {
        "schema_version": "stc_sampling_validity_window_policy_v1",
        "threshold_is_policy_placeholder": POLICY_PLACEHOLDER,
        "frame_validity_ms": 800,
        "region_validity_ms": 1200,
        "crop_validity_ms": 1500,
        "ocr_result_validity_ms": 5000,
        "task_context_validity_ms": 60000,
        "route_progress_validity_ms": 45000,
        "stale_conditions": [
            "frame_age_ms > frame_validity_ms",
            "region_track_age_ms > region_validity_ms",
            "crop_age_ms > crop_validity_ms",
            "ocr_result_age_ms > ocr_result_validity_ms",
            "location_age_ms > stale_location_policy",
            "route_progress_age_ms > route_progress_validity_ms",
        ],
        "refresh_required_conditions": [
            "motion_state_changed_to_unstable",
            "view_angle_exceeded",
            "empty_ocr_after_retry",
            "same_bbox_risk_persisted",
        ],
        "invalidation_reasons": [
            "stale_frame",
            "stale_region",
            "stale_crop",
            "stale_ocr_result",
            "stale_task_context",
            "stale_route_progress",
        ],
        "ocr_decision_blocked_on_stale": True,
        "resampling_required_on_stale_crop": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _motion_downgrade() -> Dict[str, Any]:
    rows = [
        ("stationary", ["OCR-L1", "OCR-L2", "OCR-L3"], True, False, True, []),
        ("slow_walk", ["OCR-L1", "OCR-L2"], True, False, True, ["OCR-L3_long_read"]),
        ("normal_walk", ["OCR-L1", "OCR-L2"], True, False, True, ["dense_text_dynamic"]),
        ("fast_walk", ["OCR-L1"], False, True, True, ["OCR-L2", "OCR-L3", "dynamic_precision"]),
        ("vehicle_motion", ["OCR-L0", "OCR-L1"], False, True, False, ["dynamic_read", "static_without_stop"]),
        ("unstable_camera", ["OCR-L0", "OCR-L1"], False, True, True, ["dynamic_read_until_stable"]),
    ]
    return {
        "schema_version": "stc_motion_aware_ocr_downgrade_policy_v1",
        "user_motion_states": [
            {
                "user_motion_state": state,
                "allowed_ocr_level_by_motion": levels,
                "dynamic_reading_allowed": dyn,
                "static_assisted_reading_required": static_req,
                "user_guidance_allowed": ug,
                "blocked_actions": blocked,
                "recommended_fallback": "static_assisted_reading" if static_req else "safety_background_scan_only",
                "safety_background_scan_still_allowed": state in ("fast_walk", "vehicle_motion", "unstable_camera"),
            }
            for state, levels, dyn, static_req, ug, blocked in rows
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _retry_budget() -> Dict[str, Any]:
    return {
        "schema_version": "stc_ocr_retry_budget_timeout_policy_v1",
        "retry_budget_by_ocr_level": {
            "OCR-L1": {"max_attempts": 2, "max_duration_ms": 1500},
            "OCR-L2": {"max_attempts": 2, "max_duration_ms": 3000},
            "OCR-L3": {"max_attempts": 1, "max_duration_ms": 8000},
            "OCR-L4": {"max_attempts": 0, "max_duration_ms": 0},
        },
        "max_internal_recrop_attempts": 2,
        "max_empty_result_before_guidance": 2,
        "max_dynamic_reading_duration_sec": 8,
        "max_static_reading_duration_sec": 120,
        "timeout_actions": [
            "invalidate_stale_crop",
            "escalate_to_user_guidance",
            "escalate_to_static_assisted_reading",
            "stop_internal_recrop",
        ],
        "escalation_policy": "after max_empty_result_before_guidance -> User-Guidance-Recovery; after max_internal_recrop -> STC resample not re-crop loop",
        "current_case_v1_v2_all_empty_triggers_guidance": True,
        "infinite_internal_recrop_forbidden": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _static_reading_trigger() -> Dict[str, Any]:
    triggers = [
        ("long_text_detected", True, ["ask_user_pause_for_static_reading"], ["request_static_capture_mode"]),
        ("dense_text_layout", True, ["ask_user_pause_for_static_reading"], ["request_high_resolution_still_frame"]),
        ("repeated_dynamic_empty", True, ["ask_user_hold_still"], ["request_resampling", "request_multiframe_stabilization"]),
        ("user_explicit_read_request", True, [], ["request_static_capture_mode"]),
        ("high_precision_text_required", True, ["ask_user_pause_for_static_reading"], ["request_autofocus", "request_zoom"]),
        ("task_critical_but_dynamic_unreadable", True, ["ask_user_confirm_task_importance"], ["request_static_capture_mode"]),
    ]
    return {
        "schema_version": "stc_static_assisted_reading_trigger_policy_v1",
        "low_motion_required": True,
        "triggers": [
            {
                "trigger_id": tid,
                "static_assisted_reading_required": req,
                "suggested_user_guidance": ug,
                "suggested_system_sampling": sys,
                "ocr_activation_level": "OCR-L3",
                "dynamic_reading_blocked": True,
            }
            for tid, req, ug, sys in triggers
        ],
        "complex_text_types": ["long_notice", "menu_full_reading", "poster_article", "medicine_label", "document_snippet"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _dynamic_short_text_scope() -> Dict[str, Any]:
    markers = [
        ("doorplate", True, 24, "short_text_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("room_number", True, 16, "short_text_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("window_number", True, 12, "short_text_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("floor_number", True, 8, "short_text_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("exit_entry_sign", True, 20, "visual_symbol_then_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("safety_short_warning", True, 32, "warning_icon_then_ocr_l1", "OCR-L1", "OCR-L2", "none_if_symbol_detected"),
        ("transit_line_number", True, 20, "short_text_ocr_l2", "OCR-L2", "OCR-L3", "user_guidance_after_empty"),
        ("shop_short_name_confirmation", True, 28, "visual_logo_then_ocr_l1", "OCR-L1", "OCR-L3", "user_guidance_optional"),
        ("public_facility_marker", False, 16, "visual_symbol_first", "OCR-L0", "OCR-L1", "user_guidance_if_needed"),
    ]
    return {
        "schema_version": "stc_dynamic_short_text_scope_policy_v1",
        "markers": [
            {
                "marker_type": mt,
                "dynamic_allowed": dyn,
                "max_text_length_hint": mx,
                "preferred_detection_path": path,
                "ocr_activation_level": level,
                "fallback_path": fb,
                "user_guidance_threshold": thresh,
                "fact_status": "not_fact",
            }
            for mt, dyn, mx, path, level, fb, thresh in markers
        ],
        "write_allowed": False,
    }


def run_stc_sampling_guidance_policy_v1(
    *,
    user_guidance_root: str,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    bbox_adjustment_root: str,
    text_detector_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    multiframe_ocr_v1_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    ug = Path(user_guidance_root).resolve()
    ocr2 = Path(ocr_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    ug_sum = _read_json(ug / "user_guidance_recovery_policy_v1_summary.json") or {}
    ug_case = _read_json(ug / "user_guidance_current_case_recovery_decision_v1.json") or {}
    ocr2_sum = _read_json(ocr2 / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}

    v1_empty = int(ug_case.get("v1_empty_count") or 30)
    v2_empty = int(ug_case.get("v2_empty_count") or ocr2_sum.get("v2_empty_result_count") or 5)
    same_bbox = int(ug_case.get("same_bbox_risk_count") or ocr2_sum.get("same_bbox_risk_count_observed") or 5)
    geom_sig = int(ug_case.get("geometry_change_significant_count") or 0)

    current_case = {
        "schema_version": "stc_current_case_decision_dryrun_v1",
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "geometry_change_significant_count": geom_sig,
        "current_ocr_level": "OCR-L4",
        "recommended_next_policy": "STC-Sampling-Guidance-Policy-v1",
        "internal_retry_should_stop": True,
        "user_guidance_recommended": True,
        "system_self_adjustment_recommended": True,
        "external_assistance_conditionally_recommended": True,
        "dynamic_reocr_allowed_now": False,
        "static_assisted_reading_candidate": True,
        "safety_background_scan_policy_candidate": True,
        "task_pre_activation_policy_candidate": True,
        "runtime_action_committed": False,
        "tts_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "stc_sampling_guidance_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "stc_sampling_guidance_policy_only",
            "based_on_user_guidance_recovery_policy": ug.is_dir(),
            "safety_trigger_policy_defined": True,
            "task_trigger_prediction_policy_defined": True,
            "geolocation_pre_activation_policy_defined": True,
            "route_progress_pre_activation_policy_defined": True,
            "sampling_validity_window_defined": True,
            "ocr_retry_budget_policy_defined": True,
            "stale_policy_defined": True,
            "motion_aware_downgrade_policy_defined": True,
            "static_assisted_reading_trigger_defined": True,
            "vision_capture_governance_link_defined": True,
            "ocr_activation_governance_link_defined": True,
            "runtime_sampling_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "safety_trigger": _safety_trigger_policy(),
        "task_trigger": _task_trigger_policy(),
        "geolocation_route": _geolocation_route_policy(),
        "validity_window": _sampling_validity_window(),
        "motion_downgrade": _motion_downgrade(),
        "retry_budget": _retry_budget(),
        "static_reading": _static_reading_trigger(),
        "dynamic_short_text": _dynamic_short_text_scope(),
        "ocr_activation_link": {
            "schema_version": "stc_ocr_activation_governance_link_report_v1",
            "ocr_activation_governance_required": True,
            "ocr_default_off_for_world_modeling": True,
            "visual_semantic_first": True,
            "ocr_task_oriented": True,
            "safety_trigger_background_scan_allowed": True,
            "task_trigger_pre_activation_required": True,
            "dynamic_reading_scope_limited": True,
            "assisted_static_reading_required_for_complex_text": True,
            "dual_trigger_model": ["safety_triggered", "task_triggered"],
            "future_phase": "OCR-Activation-Governance-Policy-v1",
            "fact_status": "not_fact",
        },
        "vision_capture_link": {
            "schema_version": "stc_vision_capture_governance_link_report_v1",
            "vision_capture_governance_required": True,
            "capture_quality_feedback_required": True,
            "zoom_autofocus_resampling_placeholder_required": True,
            "frame_quality_gate_required": True,
            "capture_pose_quality_required": True,
            "hardware_placeholder_required": True,
            "future_phase": "Vision-Capture-Governance-v1",
            "fact_status": "not_fact",
        },
        "current_case": current_case,
        "boundary": {
            "schema_version": "stc_sampling_guidance_boundary_report_v1",
            "policy_only": True,
            "runtime_sampling_invoked": False,
            "tts_invoked": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "stc_sampling_guidance_metrics_candidate_report_v1",
            "safety_trigger_policy_defined": True,
            "task_trigger_prediction_policy_defined": True,
            "pre_activation_policy_defined": True,
            "sampling_validity_window_defined": True,
            "motion_aware_downgrade_policy_defined": True,
            "retry_budget_policy_defined": True,
            "dynamic_short_text_scope_defined": True,
            "static_assisted_reading_trigger_defined": True,
            "runtime_action_committed_count": 0,
            "tts_invoked_count": 0,
            "ocr_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "stc_sampling_guidance_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "stc_sampling_guidance_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "stc_sampling_guidance_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "runtime_sampling_invoked": False,
            "tts_invoked": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "provider_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
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
            "schema_version": "stc_sampling_guidance_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "stc_sampling_guidance_non_claims_report_v1",
            "claims": [
                "no_runtime_sampling_execution",
                "no_tts",
                "no_hardware_invoke",
                "no_ocr_in_this_phase",
                "safety_trigger_not_runtime_scan",
                "task_trigger_not_real_map_api",
                "pre_activation_windows_are_placeholders",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "stc_sampling_guidance_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "stc_sampling_guidance_audit_report_v1",
            "stc_sampling_guidance_policy_v1_executed": True,
            "policy_only": True,
            "safety_trigger_policy_defined": True,
            "task_trigger_prediction_policy_defined": True,
            "geolocation_pre_activation_policy_defined": True,
            "sampling_validity_window_defined": True,
            "runtime_sampling_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_rerun_invoked": False,
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
