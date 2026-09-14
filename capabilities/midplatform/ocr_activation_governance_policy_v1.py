# -*- coding: utf-8 -*-
"""OCR Activation Governance Policy v1 — gate, dual trigger, expired information value (policy only).

Phase-OCR-Activation-Governance-Policy-v1-001

Expired Information Value Principle: stale blocks action freshness only, not long-term value.
Four dimensions:
- action_freshness: current task/nav/OCR/TTS/fact write
- world_historical_value: user-world change record
- user_profile_context_value: environment, range, scene, cognition preference
- emotional_context_value: background for future emotional computation
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "OCR-Activation-Governance-Policy-v1-001"
RUNTIME_STEP = "ocr_activation_governance_policy_v1"

FOLLOWUPS = [
    "Vision-Capture-Governance-v1",
    "User-Guidance-Recovery-Runtime-DryRun-v1",
    "OCR-Activation-Runtime-DryRun-v1",
    "Expired-Observation-Candidate-Ingest-v1",
    "World-Change-Hint-Candidate-DryRun-v1",
    "User-Environment-Context-Candidate-Ingest-v1",
    "User-Profile-Context-Candidate-DryRun-v1",
    "Emotional-Context-Background-Candidate-v1",
    "STC-Freshness-Gate-Runtime-DryRun-v1",
    "Safety-Marker-Background-Scan-Policy-v1",
    "Task-Triggered-OCR-PreActivation-Runtime-DryRun-v1",
    "Assisted-Static-Reading-Mode-v1",
    "Hardware-Camera-Control-Contract-v1",
]

LONG_TERM_CANDIDATE_ROUTES = [
    "expired_observation_candidate",
    "world_change_hint_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
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

GATE_DECISIONS = [
    "OCR_NOT_ACTIVATED",
    "SAFETY_SHORT_MARKER_SCAN",
    "TASK_SHORT_TEXT_CONFIRMATION",
    "ASSISTED_STATIC_READING",
    "USER_GUIDANCE_RECOVERY",
    "SYSTEM_SELF_ADJUSTMENT",
    "EXTERNAL_ASSISTANCE",
    "TASK_DOWNGRADE_OR_NON_OCR_PATH",
    "EXPIRED_OBSERVATION_TO_WORLD_HINT",
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _action_freshness_policy() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_action_freshness_policy_v1",
        "action_freshness_definition": "information fresh enough for current navigation, OCR activation, TTS, risk judgment",
        "expired_not_equal_discarded": True,
        "stale_blocks_action_decision": True,
        "stale_blocks_navigation_decision": True,
        "stale_blocks_ocr_activation_for_action": True,
        "stale_blocks_fact_write": True,
        "freshness_dimensions": [
            "frame",
            "region",
            "crop",
            "ocr_result",
            "task_context",
            "route_context",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _expired_information_value_principle() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_expired_information_value_principle_v1",
        "principle_name": "Expired Information Value Principle",
        "one_line_summary": (
            "过期信息不能指挥现在，但可以塑造 Luna 对用户世界、用户生活环境和情绪背景的长期理解"
        ),
        "expired_means_not_for_current_action_not_discard": True,
        "stale_blocks_action_freshness_only": True,
        "stale_does_not_discard_long_term_value": True,
        "forbidden_current_uses": [
            "current_navigation_decision",
            "current_ocr_activation_decision",
            "current_tts_broadcast",
            "current_risk_action",
            "midplatform_fact_write",
            "world_model_write_now",
        ],
        "allowed_long_term_candidate_routes": LONG_TERM_CANDIDATE_ROUTES,
        "four_value_dimensions": [
            {
                "dimension_id": "action_freshness",
                "usable_for_current_task_nav_ocr_tts_fact": True,
                "blocked_when_stale": True,
                "description": "是否可用于当前任务、导航、OCR、播报、事实写入；过期后通常不可用",
            },
            {
                "dimension_id": "world_historical_value",
                "usable_for_current_action_when_stale": False,
                "description": "用户所处世界变化记录：店铺、施工、标识、路径环境变化",
                "example_signals": [
                    "shop_sign_changed",
                    "construction_state",
                    "safety_marker_change",
                    "route_marker_change",
                ],
            },
            {
                "dimension_id": "user_profile_context_value",
                "usable_for_current_action_when_stale": False,
                "description": "用户生活环境、活动范围、常见场景、认知偏好补充",
                "example_signals": [
                    "frequent_hospital_corridor",
                    "frequent_convenience_store",
                    "school_transit_hub",
                    "metro_station_pattern",
                    "retail_district_pattern",
                ],
            },
            {
                "dimension_id": "emotional_context_value",
                "usable_for_current_action_when_stale": False,
                "description": "未来情感计算的环境背景材料",
                "example_signals": [
                    "noisy_environment",
                    "complex_commute_path",
                    "hospital_scene",
                    "consumption_scene",
                    "solitude_pressure_scene",
                ],
            },
        ],
        "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
        "future_usage_scopes": [
            "refine_user_living_environment_profile",
            "supplement_daily_activity_range",
            "supplement_user_cognition_context",
            "emotional_computation_environment_background",
            "record_user_world_changes",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _world_model_historical_value_policy() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_world_model_historical_value_policy_v1",
        "world_historical_value_definition": (
            "expired observation may retain value as user-world change record and historical anchor"
        ),
        "expired_not_equal_discarded": True,
        "not_task_waste": True,
        "stale_allows_world_hint_candidate": True,
        "stale_allows_expired_observation_candidate": True,
        "stale_allows_unresolved_history_slot_candidate": True,
        "stale_allows_user_environment_context_candidate": True,
        "stale_allows_user_profile_context_candidate": True,
        "stale_allows_emotional_context_background_candidate": True,
        "world_model_write_allowed_now": False,
        "fact_write_allowed_now": False,
        "review_required_before_any_world_attach": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _user_profile_context_value_policy() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_user_profile_context_value_policy_v1",
        "user_profile_context_value_definition": (
            "stale/expired may supplement user living environment, activity range, scene habits, cognition preference"
        ),
        "cannot_drive_current_action": True,
        "cannot_write_fact_now": True,
        "candidate_route": "user_profile_context_candidate",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _emotional_context_value_policy() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_emotional_context_value_policy_v1",
        "emotional_context_value_definition": (
            "stale/expired may serve as background material for future emotional computation, not current broadcast"
        ),
        "cannot_drive_current_action": True,
        "cannot_write_fact_now": True,
        "candidate_route": "emotional_context_background_candidate",
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _stale_observation_long_term_routing() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_stale_observation_long_term_routing_policy_v1",
        "anti_pattern": "do_not_simply_discard_stale",
        "pipeline_steps": [
            "stale_observation",
            "block_current_action",
            "keep_source_chain",
            "decay_confidence",
            "attach_time_space_anchor",
            "classify_long_term_value",
            "route_to_candidate_pool",
        ],
        "routing_targets": LONG_TERM_CANDIDATE_ROUTES,
        "value_classification_outputs": [
            "world_historical_value",
            "user_profile_context_value",
            "emotional_context_value",
            "unresolved_history",
        ],
        "required_metadata_on_route": CANDIDATE_METADATA_REQUIRED,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _candidate_metadata_block() -> Dict[str, Any]:
    return {k: True for k in CANDIDATE_METADATA_REQUIRED}


def _activation_gate_table() -> List[Dict[str, Any]]:
    specs = [
        (
            "OCR_NOT_ACTIVATED",
            "default",
            ["world_modeling_only", "generic_environment", "no_task_critical_text"],
            ["safety_marker_present", "task_critical_short_text", "user_explicit_read"],
            "visual_semantic_spatial_poi",
            ["maintain_vision_primary_path"],
            ["ocr_invoke", "full_frame_ocr", "fact_write"],
            "candidate_only",
        ),
        (
            "SAFETY_SHORT_MARKER_SCAN",
            "safety",
            ["safety_marker_detected_or_suspected", "background_scan_enabled"],
            ["full_text_ocr_requested", "stale_frame_for_action"],
            "visual_symbol_then_warning_icon_then_short_ocr",
            ["background_short_marker_scan"],
            ["full_text_ocr", "world_model_fact_from_ocr"],
            "candidate_only",
        ),
        (
            "TASK_SHORT_TEXT_CONFIRMATION",
            "task",
            ["task_active", "midplatform_pre_activation", "task_critical_short_text", "readiness_pass"],
            ["ocr_self_trigger", "stale_for_action", "long_text_dynamic"],
            "visual_semantic_then_short_ocr",
            ["gated_short_text_ocr"],
            ["autonomous_ocr_without_task_chain", "full_scene_ocr"],
            "candidate_only",
        ),
        (
            "ASSISTED_STATIC_READING",
            "task_or_user",
            ["long_text", "dense_layout", "user_explicit_read", "medicine_label"],
            ["fast_motion", "dynamic_while_moving"],
            "static_capture_then_precision_ocr",
            ["assisted_static_reading_mode"],
            ["dynamic_article_read", "tts_without_quality_gate"],
            "candidate_only",
        ),
        (
            "USER_GUIDANCE_RECOVERY",
            "recovery",
            ["repeated_empty", "low_readiness", "same_bbox_retry_exhausted"],
            ["fresh_ready_short_text"],
            "user_guidance_then_resample",
            ["guidance_action_candidates"],
            ["internal_recrop_loop", "fact_write"],
            "candidate_only",
        ),
        (
            "SYSTEM_SELF_ADJUSTMENT",
            "recovery",
            ["hardware_capability_available", "system_repairable_signal"],
            ["user_can_self_repair_alone"],
            "capture_quality_improvement",
            ["zoom_autofocus_resample_candidates"],
            ["direct_hardware_invoke_in_policy_phase"],
            "candidate_only",
        ),
        (
            "EXTERNAL_ASSISTANCE",
            "recovery",
            ["user_unable", "target_unreachable", "accessibility_limit"],
            ["fresh_task_critical_resolved"],
            "external_assistance_candidates",
            ["nearby_read", "staff_confirm", "manual_input"],
            ["forced_ocr_retry"],
            "candidate_only",
        ),
        (
            "TASK_DOWNGRADE_OR_NON_OCR_PATH",
            "routing",
            ["text_not_task_critical", "non_recoverable_by_ocr"],
            ["task_critical_pending"],
            "world_model_or_task_degrade",
            ["skip_ocr_continue_task"],
            ["ocr_retry_loop"],
            "candidate_only",
        ),
        (
            "EXPIRED_OBSERVATION_TO_WORLD_HINT",
            "freshness_split",
            ["stale_frame", "stale_crop", "stale_ocr_result", "stale_route_context"],
            ["fresh_for_action"],
            "stale_observation_long_term_value_routing_pipeline",
            [
                "retain_as_historical_candidate",
                "route_expired_observation_candidate",
                "route_world_change_hint_candidate",
                "route_user_environment_context_candidate",
                "route_user_profile_context_candidate",
                "route_emotional_context_background_candidate",
            ],
            [
                "use_stale_for_navigation",
                "use_stale_for_ocr_action",
                "fact_write_from_stale",
                "discard_stale_without_routing",
            ],
            "candidate_only_not_fact",
        ),
    ]
    return [
        {
            "gate_decision": gd,
            "trigger_class": tc,
            "required_conditions": req,
            "blocked_conditions": blk,
            "preferred_first_path": path,
            "allowed_actions": allowed,
            "forbidden_actions": forbidden,
            "output_status": status,
            "fact_status_after_gate": "not_fact",
            "write_allowed_after_gate": False,
        }
        for gd, tc, req, blk, path, allowed, forbidden, status in specs
    ]


def _dual_trigger_policy() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_dual_trigger_activation_policy_v1",
        "safety_trigger": {
            "trigger_class": "safety",
            "default_background_enabled": True,
            "user_prompt_required": False,
            "visual_symbol_first": True,
            "short_text_ocr_second": True,
            "full_text_ocr_forbidden_by_default": True,
            "priority": "high",
            "allowed_marker_types": [
                "warning_sign",
                "danger_text",
                "forbidden_entry",
                "construction",
                "maintenance",
                "exit_entry",
                "emergency_marker",
            ],
            "activation_output": "SAFETY_SHORT_MARKER_SCAN",
            "fact_status": "not_fact",
        },
        "task_trigger": {
            "trigger_class": "task",
            "midplatform_pre_activation_required": True,
            "task_context_required": True,
            "geolocation_or_route_progress_required": True,
            "ocr_self_activation_allowed": False,
            "activation_output_options": [
                "TASK_SHORT_TEXT_CONFIRMATION",
                "ASSISTED_STATIC_READING",
            ],
            "pre_activation_window_placeholder": {
                "distance_m": 50,
                "time_sec": 35,
            },
            "fact_status": "not_fact",
        },
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _default_off_world_modeling() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_default_off_world_modeling_policy_v1",
        "ocr_default_off_for_world_modeling": True,
        "world_model_primary_inputs": [
            "visual_semantic",
            "spatial_structure",
            "object_relationship",
            "icon_symbol",
            "logo_candidate",
            "poi_map_hint",
            "route_context",
            "task_context",
        ],
        "ocr_allowed_as_auxiliary_evidence": True,
        "ocr_auxiliary_use_cases": [
            "safety_text",
            "doorplate",
            "room_number",
            "window_number",
            "transit_line_number",
            "shop_name_confirmation",
            "user_explicit_reading",
        ],
        "forbidden_default_use": [
            "generic_environment_text",
            "long_article_dynamic_reading",
            "continuous_full_scene_ocr",
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def _visual_semantic_first_routing() -> List[Dict[str, Any]]:
    specs = [
        ("shop_name_confirmation", "visual_logo_poi", "ocr_confirm_short", "task_critical_or_user_confirm", "generic_env_only", "OCR-L1"),
        ("public_facility", "icon_facility_semantic", "ocr_assist_short", "facility_task_active", "full_ocr_default", "OCR-L0"),
        ("safety_marker", "warning_icon_visual", "short_ocr_assist", "safety_path_active", "long_text_safety_article", "SAFETY_SHORT_MARKER_SCAN"),
        ("navigation_path", "spatial_path_risk", "ocr_if_task_critical_only", "critical_marker_in_path", "continuous_scene_ocr", "OCR-L2"),
        ("generic_world_understanding", "vision_semantic_only", "ocr_off", "never_by_default", "any_ocr_default", "OCR_NOT_ACTIVATED"),
    ]
    return [
        {
            "scene_type": st,
            "first_path": first,
            "second_path": second,
            "ocr_activation_condition": cond,
            "ocr_forbidden_when": forb,
            "fallback_path": fb,
            "fact_status": "not_fact",
        }
        for st, first, second, cond, forb, fb in specs
    ]


def _dynamic_vs_static_gate() -> Dict[str, Any]:
    dynamic_types = [
        "doorplate",
        "room_number",
        "window_number",
        "floor_number",
        "exit_entry_sign",
        "safety_short_warning",
        "transit_line_number",
        "shop_short_name_confirmation",
        "public_facility_marker",
    ]
    static_types = [
        "long_notice",
        "menu_full_reading",
        "poster_article",
        "medicine_label_detail",
        "document",
        "contract",
        "dense_text_layout",
    ]
    rows = []
    for t in dynamic_types:
        rows.append(
            {
                "text_task_type": t,
                "dynamic_allowed": True,
                "static_assisted_required": False,
                "user_guidance_required": False,
                "max_text_length_hint": 32,
                "required_capture_quality": "readiness_pass",
                "fallback_policy": "USER_GUIDANCE_RECOVERY_if_empty",
                "fact_status": "not_fact",
            }
        )
    for t in static_types:
        rows.append(
            {
                "text_task_type": t,
                "dynamic_allowed": False,
                "static_assisted_required": True,
                "user_guidance_required": True,
                "max_text_length_hint": 999,
                "required_capture_quality": "static_capture_quality_gate",
                "fallback_policy": "ASSISTED_STATIC_READING",
                "fact_status": "not_fact",
            }
        )
    return {
        "schema_version": "ocr_dynamic_vs_static_reading_gate_v1",
        "dynamic_allowed_types": dynamic_types,
        "static_required_types": static_types,
        "rows": rows,
        "write_allowed": False,
    }


def _readiness_gate() -> Dict[str, Any]:
    dims = [
        ("view_condition", "centering_and_angle_ok", "oblique_or_motion_blur", "user_repairable", "block_ocr_activation", "OCR-L3"),
        ("distance", "text_pixel_height_ok", "too_far_or_too_close", "user_or_system_repairable", "block_or_downgrade", "OCR-L3"),
        ("region_localization", "anchor_known", "projection_drift_high", "system_repairable", "block_task_ocr", "OCR-L4"),
        ("bbox_geometry", "bbox_min_area_ok", "bbox_too_small_or_wrong", "user_or_system", "block_ocr", "OCR-L3"),
        ("text_readability", "brightness_contrast_ok", "low_readability", "user_repairable", "block_or_guidance", "OCR-L3"),
    ]
    return {
        "schema_version": "ocr_readiness_gate_policy_v1",
        "based_on_user_guidance_recovery_policy": True,
        "dimensions": [
            {
                "readiness_dimension": d,
                "pass_condition": p,
                "fail_condition": f,
                "repairability_category": r,
                "gate_effect": e,
                "next_policy_level": n,
                "action_allowed_now": False,
                "fact_status": "not_fact",
            }
            for d, p, f, r, e, n in dims
        ],
        "write_allowed": False,
    }


def _stc_freshness_gate() -> Dict[str, Any]:
    stale_types = [
        "stale_frame",
        "stale_region",
        "stale_crop",
        "stale_ocr_result",
        "stale_task_context",
        "stale_route_context",
    ]
    return {
        "schema_version": "ocr_stc_freshness_gate_policy_v1",
        "frame_freshness_required_for_action": True,
        "region_freshness_required_for_action": True,
        "crop_freshness_required_for_ocr": True,
        "ocr_result_freshness_required_for_decision": True,
        "task_context_freshness_required": True,
        "route_context_freshness_required": True,
        "stale_blocks_action": True,
        "stale_blocks_fact_write": True,
        "stale_blocks_action_freshness_only": True,
        "stale_allows_world_hint_candidate": True,
        "stale_allows_expired_observation_candidate": True,
        "stale_allows_user_environment_context_candidate": True,
        "stale_allows_user_profile_context_candidate": True,
        "stale_allows_emotional_context_background_candidate": True,
        "expired_information_value_principle": _expired_information_value_principle(),
        "action_freshness_policy": _action_freshness_policy(),
        "world_model_historical_value_policy": _world_model_historical_value_policy(),
        "user_profile_context_value_policy": _user_profile_context_value_policy(),
        "emotional_context_value_policy": _emotional_context_value_policy(),
        "stale_observation_long_term_routing": _stale_observation_long_term_routing(),
        "stale_type_rules": [
            {
                "stale_type": st,
                "action_decision_allowed": False,
                "navigation_decision_allowed": False,
                "fact_write_allowed": False,
                "world_hint_candidate_allowed": True,
                "required_governance_path": "EXPIRED_OBSERVATION_TO_WORLD_HINT",
                "fact_status": "not_fact",
            }
            for st in stale_types
        ],
        "write_allowed": False,
    }


def _expired_observation_candidates() -> List[Dict[str, Any]]:
    types = [
        "expired_frame_candidate",
        "expired_region_candidate",
        "expired_crop_candidate",
        "expired_ocr_result_candidate",
        "expired_task_context_candidate",
        "expired_route_context_candidate",
    ]
    meta = _candidate_metadata_block()
    return [
        {
            "expired_candidate_type": t,
            "cannot_use_for_action": True,
            "cannot_write_fact": True,
            "can_feed_world_model_candidate": True,
            "can_feed_world_change_hint": True,
            "can_feed_unresolved_history_slot": True,
            "can_feed_user_environment_context": True,
            "can_feed_user_profile_context": True,
            "can_feed_emotional_context_background": True,
            "long_term_routing_targets": LONG_TERM_CANDIDATE_ROUTES,
            "ttl_required": True,
            "review_required_before_world_write": True,
            **meta,
            "fact_status": "not_fact",
        }
        for t in types
    ]


def _user_environment_context_candidates() -> List[Dict[str, Any]]:
    contexts = [
        ("hospital_corridor_frequent", "healthcare_environment"),
        ("convenience_store_frequent", "daily_retail_environment"),
        ("school_zone_transit", "education_transit_environment"),
        ("metro_station_hub", "transit_hub_environment"),
        ("retail_district_pattern", "commercial_district_environment"),
        ("construction_zone_recurring", "construction_environment"),
    ]
    meta = _candidate_metadata_block()
    return [
        {
            "context_type": ct,
            "environment_category": cat,
            "cannot_use_for_action": True,
            "cannot_write_fact": True,
            "feeds_user_living_environment_profile": True,
            "feeds_activity_range_supplement": True,
            "source_candidate_types": ["expired_observation_candidate", "stale_route_context"],
            **meta,
            "fact_status": "not_fact",
        }
        for ct, cat in contexts
    ]


def _user_profile_context_candidates() -> List[Dict[str, Any]]:
    profiles = [
        ("activity_range_supplement", "user_profile_context_candidate"),
        ("common_scene_habit", "user_profile_context_candidate"),
        ("cognition_preference_hint", "user_profile_context_candidate"),
        ("poi_corridor_pattern", "user_environment_context_candidate"),
    ]
    meta = _candidate_metadata_block()
    return [
        {
            "profile_context_type": pt,
            "candidate_route": route,
            "cannot_use_for_action": True,
            "cannot_write_fact": True,
            "future_usage_scope": [
                "refine_user_living_environment_profile",
                "supplement_daily_activity_range",
                "supplement_user_cognition_context",
            ],
            **meta,
            "fact_status": "not_fact",
        }
        for pt, route in profiles
    ]


def _emotional_context_background_candidates() -> List[Dict[str, Any]]:
    backgrounds = [
        ("noisy_environment_background", "sensory_stress"),
        ("complex_commute_path_background", "mobility_stress"),
        ("hospital_scene_background", "health_anxiety_context"),
        ("consumption_scene_background", "decision_fatigue_context"),
        ("solitude_scene_background", "social_isolation_context"),
        ("pressure_scene_background", "cognitive_load_context"),
    ]
    meta = _candidate_metadata_block()
    return [
        {
            "background_type": bt,
            "emotional_domain": domain,
            "cannot_use_for_current_tts_or_action": True,
            "cannot_write_fact": True,
            "feeds_emotional_computation_background": True,
            "not_immediate_emotion_inference": True,
            **meta,
            "fact_status": "not_fact",
        }
        for bt, domain in backgrounds
    ]


def _world_change_hints() -> List[Dict[str, Any]]:
    hints = [
        ("sign_changed_hint", "expired_ocr_result_candidate"),
        ("shop_sign_changed_hint", "visual_semantic_and_ocr_history"),
        ("safety_marker_appeared_hint", "safety_scan_history"),
        ("safety_marker_disappeared_hint", "safety_scan_history"),
        ("route_marker_changed_hint", "route_context_history"),
        ("facility_marker_changed_hint", "facility_semantic_history"),
        ("repeated_unreadable_text_region_hint", "repeated_empty_ocr_history"),
        ("long_term_unresolved_text_anchor_hint", "unresolved_anchor_history"),
    ]
    return [
        {
            "hint_type": ht,
            "source_candidate": src,
            "required_repeated_observation": True,
            "required_spatial_anchor": True,
            "required_time_anchor": True,
            "fact_write_allowed_now": False,
            "world_model_write_allowed_now": False,
            "future_review_path": "World-Change-Hint-Candidate-DryRun-v1",
            "fact_status": "not_fact",
        }
        for ht, src in hints
    ]


def _retry_recovery_routing() -> Dict[str, Any]:
    return {
        "schema_version": "ocr_retry_recovery_routing_policy_v1",
        "max_internal_recrop_attempts": 2,
        "max_empty_result_before_guidance": 2,
        "repeated_empty_routes_to": "USER_GUIDANCE_RECOVERY",
        "low_readiness_routes_to": "USER_GUIDANCE_RECOVERY",
        "hardware_available_routes_to": "SYSTEM_SELF_ADJUSTMENT",
        "user_unable_routes_to": "EXTERNAL_ASSISTANCE",
        "non_task_critical_routes_to": "TASK_DOWNGRADE_OR_NON_OCR_PATH",
        "stale_but_useful_routes_to": "EXPIRED_OBSERVATION_TO_WORLD_HINT",
        "routing_table": [
            {"condition": "repeated_empty_after_internal_retry", "gate_decision": "USER_GUIDANCE_RECOVERY"},
            {"condition": "low_readiness", "gate_decision": "USER_GUIDANCE_RECOVERY"},
            {"condition": "hardware_repairable", "gate_decision": "SYSTEM_SELF_ADJUSTMENT"},
            {"condition": "user_unable", "gate_decision": "EXTERNAL_ASSISTANCE"},
            {"condition": "non_task_critical", "gate_decision": "TASK_DOWNGRADE_OR_NON_OCR_PATH"},
            {"condition": "stale_but_historical_value", "gate_decision": "EXPIRED_OBSERVATION_TO_WORLD_HINT"},
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_ocr_activation_governance_policy_v1(
    *,
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
    stc = Path(stc_sampling_guidance_root).resolve()
    ug = Path(user_guidance_root).resolve()
    ocr2 = Path(ocr_v2_root).resolve()
    bench = Path(benchmark_smoke_root).resolve()
    health = Path(system_health_root).resolve()
    sim = Path(simulation_root).resolve()

    stc_case = _read_json(stc / "stc_current_case_decision_dryrun_v1.json") or {}
    ug_case = _read_json(ug / "user_guidance_current_case_recovery_decision_v1.json") or {}
    ocr2_sum = _read_json(ocr2 / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}

    v1_empty = int(stc_case.get("v1_empty_count") or ug_case.get("v1_empty_count") or 30)
    v2_empty = int(stc_case.get("v2_empty_count") or ug_case.get("v2_empty_count") or 5)
    same_bbox = int(stc_case.get("same_bbox_risk_count") or 5)
    geom_sig = int(stc_case.get("geometry_change_significant_count") or 0)

    current_case = {
        "schema_version": "ocr_activation_current_case_decision_dryrun_v1",
        "v1_empty_count": v1_empty,
        "v2_empty_count": v2_empty,
        "same_bbox_risk_count": same_bbox,
        "geometry_change_significant_count": geom_sig,
        "internal_retry_should_stop": True,
        "dynamic_reocr_allowed_now": False,
        "ocr_activation_decision": "USER_GUIDANCE_RECOVERY",
        "expired_observation_candidate_allowed": True,
        "world_change_hint_candidate_allowed": True,
        "user_environment_context_candidate_allowed": True,
        "user_profile_context_candidate_allowed": True,
        "emotional_context_background_candidate_allowed": True,
        "stale_blocks_action_freshness_only": True,
        "stale_blocks_action_for_current_ocr": True,
        "recommended_next_phase": "Vision-Capture-Governance-v1",
        "runtime_action_committed": False,
        "tts_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "ocr_activation_governance_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "ocr_activation_governance_policy_only",
            "based_on_stc_sampling_guidance_policy": stc.is_dir(),
            "based_on_user_guidance_recovery_policy": ug.is_dir(),
            "ocr_default_off_for_world_modeling": True,
            "dual_trigger_activation_defined": True,
            "safety_trigger_gate_defined": True,
            "task_trigger_gate_defined": True,
            "ocr_self_activation_allowed": False,
            "visual_semantic_first_policy_defined": True,
            "dynamic_short_text_gate_defined": True,
            "assisted_static_reading_gate_defined": True,
            "user_guidance_recovery_gate_defined": True,
            "system_self_adjustment_gate_defined": True,
            "external_assistance_or_task_downgrade_gate_defined": True,
            "action_freshness_policy_defined": True,
            "world_model_historical_value_policy_defined": True,
            "world_historical_value_policy_defined": True,
            "user_profile_context_value_policy_defined": True,
            "emotional_context_value_policy_defined": True,
            "expired_information_value_principle_defined": True,
            "four_value_dimensions_policy_defined": True,
            "stale_observation_long_term_routing_defined": True,
            "expired_observation_candidate_policy_defined": True,
            "world_change_hint_candidate_policy_defined": True,
            "user_environment_context_candidate_policy_defined": True,
            "user_profile_context_candidate_policy_defined": True,
            "emotional_context_background_candidate_policy_defined": True,
            "runtime_ocr_invoked": False,
            "runtime_sampling_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
            "navigation_decision_invoked": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "runtime_routing_changed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "gate_table": {
            "schema_version": "ocr_activation_gate_decision_table_v1",
            "gate_decision_enum": GATE_DECISIONS,
            "rows": _activation_gate_table(),
        },
        "dual_trigger": _dual_trigger_policy(),
        "default_off": _default_off_world_modeling(),
        "visual_semantic_first": {
            "schema_version": "ocr_visual_semantic_first_routing_policy_v1",
            "rows": _visual_semantic_first_routing(),
        },
        "dynamic_vs_static": _dynamic_vs_static_gate(),
        "readiness_gate": _readiness_gate(),
        "stc_freshness": _stc_freshness_gate(),
        "expired_information_value_principle": _expired_information_value_principle(),
        "stale_long_term_routing": _stale_observation_long_term_routing(),
        "expired_observation": {
            "schema_version": "ocr_expired_observation_candidate_policy_v1",
            "expired_not_equal_discarded_principle": True,
            "not_task_waste": True,
            "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
            "candidates": _expired_observation_candidates(),
        },
        "world_change_hint": {
            "schema_version": "ocr_world_change_hint_candidate_policy_v1",
            "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
            "hints": _world_change_hints(),
        },
        "user_environment_context": {
            "schema_version": "ocr_user_environment_context_candidate_policy_v1",
            "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
            "contexts": _user_environment_context_candidates(),
        },
        "user_profile_context": {
            "schema_version": "ocr_user_profile_context_candidate_policy_v1",
            "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
            "contexts": _user_profile_context_candidates(),
        },
        "emotional_context_background": {
            "schema_version": "ocr_emotional_context_background_candidate_policy_v1",
            "candidate_metadata_required": CANDIDATE_METADATA_REQUIRED,
            "backgrounds": _emotional_context_background_candidates(),
        },
        "retry_recovery": _retry_recovery_routing(),
        "current_case": current_case,
        "boundary": {
            "schema_version": "ocr_activation_governance_boundary_report_v1",
            "policy_only": True,
            "runtime_ocr_invoked": False,
            "runtime_sampling_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
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
            "schema_version": "ocr_activation_governance_metrics_candidate_report_v1",
            "activation_gate_defined": True,
            "dual_trigger_policy_defined": True,
            "default_off_world_modeling_policy_defined": True,
            "visual_semantic_first_policy_defined": True,
            "readiness_gate_defined": True,
            "freshness_gate_defined": True,
            "expired_information_value_principle_defined": True,
            "four_value_dimensions_policy_defined": True,
            "stale_observation_long_term_routing_defined": True,
            "expired_observation_candidate_policy_defined": True,
            "world_change_hint_candidate_policy_defined": True,
            "user_environment_context_candidate_policy_defined": True,
            "user_profile_context_candidate_policy_defined": True,
            "emotional_context_background_candidate_policy_defined": True,
            "runtime_action_committed_count": 0,
            "runtime_ocr_invoked_count": 0,
            "runtime_tts_invoked_count": 0,
            "fact_write_allowed_count": 0,
            "world_model_write_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "ocr_activation_governance_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": bench.is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "ocr_activation_governance_system_health_link_report_v1",
            "system_health_governance_available": health.is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "ocr_activation_governance_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "runtime_ocr_invoked": False,
            "runtime_sampling_invoked": False,
            "runtime_tts_invoked": False,
            "hardware_action_invoked": False,
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
            "schema_version": "ocr_activation_governance_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": sim.is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "ocr_activation_governance_non_claims_report_v1",
            "claims": [
                "no_runtime_ocr",
                "no_sampling",
                "no_tts",
                "no_hardware",
                "activation_decision_is_policy_dryrun_not_routing_change",
                "expired_observation_candidate_not_fact",
                "world_change_hint_not_world_model_write",
                "user_environment_context_candidate_not_fact",
                "user_profile_context_candidate_not_fact",
                "emotional_context_background_not_immediate_inference",
                "stale_blocks_action_freshness_only_not_discard",
                "stale_blocks_action_not_discard",
                "expired_not_equal_discarded",
                "expired_not_task_waste",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "ocr_activation_governance_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "ocr_activation_governance_audit_report_v1",
            "ocr_activation_governance_policy_v1_executed": True,
            "policy_only": True,
            "ocr_default_off_for_world_modeling": True,
            "dual_trigger_activation_defined": True,
            "safety_trigger_gate_defined": True,
            "task_trigger_gate_defined": True,
            "expired_information_value_principle_defined": True,
            "four_value_dimensions_policy_defined": True,
            "stale_observation_long_term_routing_defined": True,
            "expired_observation_candidate_policy_defined": True,
            "world_change_hint_candidate_policy_defined": True,
            "user_environment_context_candidate_policy_defined": True,
            "user_profile_context_candidate_policy_defined": True,
            "emotional_context_background_candidate_policy_defined": True,
            "runtime_ocr_invoked": False,
            "runtime_sampling_invoked": False,
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
    }
