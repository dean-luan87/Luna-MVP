# -*- coding: utf-8 -*-
"""Static Reading Task Scene Context Policy v1 — policy only (no scene detector/OCR/camera).

Phase-Static-Reading-Task-Scene-Context-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PHASE_ID = "Static-Reading-Task-Scene-Context-Policy-v1-001"
P3 = "P3_OCR_GUIDANCE"
P4 = "P4_GENERAL_ASSISTANCE"

FOLLOWUPS = [
    "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1",
    "User-Clarification-Prompt-Template-for-Reading-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

TASK_CONTEXT_SOURCES = [
    "user_explicit_request",
    "active_navigation_task",
    "assisted_static_reading_request",
    "safety_trigger",
    "prior_dialog_context",
    "route_context",
    "worldmodel_unresolved_slot",
]

SCENE_CONTEXT_SOURCES = [
    "worldmodel_place_anchor",
    "route_context",
    "visual_scene_candidate",
    "user_confirmed_scene",
    "map_or_poi_hint",
    "prior_observation",
]

SCENE_TYPES = [
    "street",
    "shopping_mall",
    "park",
    "hospital",
    "transit_station",
    "office_building",
    "residential_building",
    "shopfront",
    "indoor_corridor",
    "service_counter_area",
    "unknown_scene",
]

TASK_NORMALIZATION = [
    ("我想找出口", "find_exit", "find_exit_sign_or_direction", "navigation_failed_or_static_needed", "exit_sign_visible", "exit_text_unclear", True),
    ("洗手间在哪", "find_restroom", "find_restroom_sign", "restroom_not_found_semantically", "restroom_icon_or_sign", "small_wc_text", True),
    ("这是几号线", "find_transit_line", "confirm_transit_line_or_platform", "platform_sign_ambiguous", "platform_board", "electronic_screen_glare", True),
    ("哪个科室", "find_department", "find_hospital_department", "department_not_identified", "department_board", "doorplate_small", True),
    ("门牌号是多少", "read_doorplate", "read_room_or_unit_id", "doorplate_unreadable", "doorplate_region", "occluded_plate", True),
    ("这家店叫什么", "confirm_place_name", "confirm_shop_or_place_name", "logo_unclear", "signboard_or_logo", "name_partial", True),
    ("我要去某地", "find_destination", "confirm_destination_direction", "arrival_uncertain", "directory_or_wayfinding", "dense_map_text", True),
    ("读一下这个", "user_explicit_read_this", "read_user_indicated_target", "user_pointed_region", "user_indicated_area", "always_if_confirmed", True),
    ("读药盒", "read_medicine_label", "read_medicine_label_text", "label_requested", "medicine_label_area", "small_label", True),
    ("读菜单价格", "read_menu_or_price", "read_menu_or_price_board", "menu_task", "menu_or_price_board", "glare", True),
    ("读票口/柜台", "read_ticket_or_counter", "find_ticket_or_service_counter", "counter_not_found", "counter_sign", "queue_area", True),
    ("注意警示牌", "read_warning_marker", "confirm_warning_or_safety_marker", "safety_marker_ambiguous", "warning_sign", "short_marker_text", False),
    ("帮我读一段字", "generic_reading_request", "read_static_text_in_scope", "unspecified_target", "user_bounded_region", "full_frame", True),
]

SCENE_NORMALIZATION = [
    ("outdoor_road_context", "street", True, ["road_sign", "building_number", "warning_marker"], ["hospital_department"], "unknown_scene"),
    ("mall_interior_cue", "shopping_mall", True, ["directory_board", "restroom_sign", "service_desk"], ["platform_sign"], "ask_user_confirm_scene"),
    ("hospital_entrance_cue", "hospital", True, ["department_sign", "floor_guide", "staff_desk"], ["transit_line"], "unknown_scene"),
    ("station_platform_cue", "transit_station", True, ["platform_sign", "exit_sign", "electronic_screen"], ["medicine_label"], "unknown_scene"),
    ("office_lobby_cue", "office_building", True, ["lobby_directory", "room_doorplate"], ["restroom_sign_mall"], "indoor_corridor"),
    ("storefront_visible", "shopfront", False, ["signboard", "logo_area"], ["hospital_floor_guide"], "shopping_mall"),
    ("park_path_cue", "park", True, ["entrance_map", "facility_sign"], ["department_sign"], "street"),
    ("residential_entrance", "residential_building", True, ["building_number", "unit_doorplate"], ["platform_sign"], "unknown_scene"),
    ("corridor_indoor", "indoor_corridor", True, ["room_doorplate", "direction_sign"], ["road_sign"], "office_building"),
    ("counter_area_visible", "service_counter_area", False, ["staff_desk", "counter_sign"], ["park_map"], "unknown_scene"),
    ("no_scene_signal", "unknown_scene", True, [], ["all_specific_sources"], "user_clarification_required"),
]

TASK_SCENE_MATRIX = [
    ("find_restroom", "shopping_mall", ["restroom_sign", "directory_board", "elevator_area", "service_desk"], "follow_restroom_icon", ["restroom_sign", "wc_icon"], "ask_staff_or_directory", ["other_floor", "service_desk"]),
    ("find_department", "hospital", ["department_sign", "floor_guide", "staff_desk", "room_doorplate"], "ask_staff_first", ["department_board", "doorplate"], "ask_staff_for_location", ["registration", "elevator_area"]),
    ("find_transit_line", "transit_station", ["platform_sign", "line_number", "electronic_screen", "staff_counter"], "platform_board_semantic", ["platform_board", "line_display"], "ask_staff", ["exit_sign_only"]),
    ("confirm_place_name", "shopfront", ["logo_area", "signboard", "doorfront"], "logo_semantic_first", ["main_sign", "window_poster"], "ask_nearby", ["unrelated_poster"]),
    ("read_doorplate", "office_building", ["room_doorplate", "floor_guide", "reception"], "static_reading_on_plate", ["door_plate"], "ask_reception", ["lobby_ads"]),
    ("read_warning_marker", "street", ["warning_marker", "road_sign", "construction_sign"], "visual_semantic_first", ["warning_sign"], "maintain_distance", ["shop_menu"]),
    ("find_exit", "shopping_mall", ["exit_sign", "directory_board", "elevator_area"], "exit_icon_first", ["exit_arrow_sign"], "ask_staff", ["shop_ads"]),
    ("find_destination", "transit_station", ["platform_sign", "directory_board", "staff_counter"], "semantic_then_static", ["wayfinding_board"], "ask_staff", ["advertising"]),
    ("read_medicine_label", "hospital", ["medicine_label_area", "pharmacy_counter"], "static_reading", ["label_region"], "ask_pharmacist", ["unrelated_poster"]),
    ("user_explicit_read_this", "unknown_scene", ["user_pointed_region"], "confirm_target_first", ["user_bounded_area"], "ask_user_confirm", ["global_scan"]),
    ("generic_reading_request", "indoor_corridor", ["room_doorplate", "direction_sign", "notice_board"], "narrow_to_user_area", ["doorplate", "notice"], "ask_user_which", ["full_corridor_scan"]),
    ("read_menu_or_price", "shopfront", ["menu_board", "price_board", "window_poster"], "static_if_requested", ["menu_region"], "move_closer", ["road_sign"]),
]

MISSING_CONTEXT = [
    ("missing_task_context", "emit_clarification_candidates", "information_source_localization", True, False, False),
    ("missing_scene_context", "emit_clarification_candidates", "readable_region_discovery", True, False, False),
    ("missing_both_task_and_scene", "emit_clarification_then_wait", "isrc_and_rrd_runtime", True, False, False),
    ("low_confidence_task", "confirm_with_user", "rank_sources", True, False, False),
    ("low_confidence_scene", "confirm_scene_type", "scene_specific_matrix", True, False, False),
    ("stale_scene_context", "refresh_or_reconfirm", "use_stale_for_action", True, False, False),
    ("conflicting_context", "resolve_via_user", "auto_merge_context", True, False, False),
]

CLARIFICATIONS = [
    ("what_information_need", "missing_task_context", "你想找什么信息？", P3, "low"),
    ("task_type_disambiguation", "ambiguous_task", "你现在是想找出口、门牌，还是读一段文字？", P3, "low"),
    ("scene_type_disambiguation", "missing_or_low_confidence_scene", "你是在商场、医院，还是车站附近？", P3, "medium"),
    ("proactive_area_search", "task_known_scene_unknown", "要不要我先帮你找附近可能有信息的位置？", P4, "medium"),
    ("human_assistance_offer", "context_hard_to_resolve", "是否需要询问附近工作人员？", P4, "low"),
]

CONFIDENCE_LEVELS = [
    ("high_confidence_context", "user_confirmed_and_sources_agree", "handoff_information_source_query", "auto_assume_scene", False, False),
    ("medium_confidence_context", "single_strong_signal", "handoff_with_confirmation_flag", "skip_confirmation", True, False),
    ("low_confidence_context", "weak_or_single_unconfirmed", "clarification_candidates", "isrc_runtime", True, True),
    ("conflict_context", "task_scene_signals_disagree", "user_resolution", "merge_automatically", True, True),
    ("stale_context", "ttl_exceeded", "reconfirm_scene", "use_for_localization", True, True),
]

OPTIONAL_PATHS = [
    ("scene_registry", "docs/architecture/midplatform/LUNA_SCENE_REGISTRY_V0.md"),
    ("route_context", "docs/architecture/midplatform/LUNA_ROUTE_CONTEXT_V0.md"),
    ("map_registry", "docs/architecture/LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md"),
    ("user_request_parser", "docs/architecture/midplatform/LUNA_USER_REQUEST_PARSER_V0.md"),
    ("worldmodel_unresolved_slot", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("rrd_policy", roots["rrd"], "static_readable_region_discovery_guidance_policy_v1_summary.json", False),
        ("info_source", roots["isrc"], "static_reading_information_source_localization_policy_v1_summary.json", False),
        ("asm_runtime", roots["asm_rt"], "assisted_static_reading_runtime_dryrun_v1_summary.json", False),
        ("asm_mode", roots["asm"], "assisted_static_reading_mode_v1_summary.json", False),
        ("vc_runtime", roots["vc"], "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("vc_gov", roots["vc_gov"], "vision_capture_governance_v1_summary.json", False),
        ("ocr_act", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("vop", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
        ("bench", roots["bench"], None, False),
        ("health", roots["health"], None, False),
        ("sim", roots["sim"], None, False),
    ]
    rows = []
    for iid, root, art, optional in specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root_or_path": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "optional": optional,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    rrd_current = _read_json(roots["rrd"] / "static_readable_region_current_case_dryrun_v1.json")
    if rrd_current:
        rows.append(
            {
                "intake_id": "rrd_current_case",
                "input_source": "rrd_policy",
                "source_root_or_path": str(roots["rrd"]),
                "artifact": "static_readable_region_current_case_dryrun_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": [
                    "task_context_available",
                    "scene_context_available",
                    "reason_not_invoked",
                ],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    for oid, rel in OPTIONAL_PATHS:
        p = ws / rel
        rows.append(
            {
                "intake_id": oid,
                "input_source": "optional",
                "source_root_or_path": str(p),
                "artifact": rel,
                "loaded": p.is_file(),
                "optional": True,
                "key_fields_observed": [],
                "intake_status": "loaded" if p.is_file() else "optional_missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "static_reading_task_scene_context_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_static_reading_task_scene_context_policy_v1(
    *,
    readable_region_policy_root: str,
    information_source_root: str,
    assisted_static_reading_runtime_root: str,
    assisted_static_reading_mode_root: str,
    vision_capture_runtime_root: str,
    vision_capture_governance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    voice_output_plane_adapter_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "rrd": Path(readable_region_policy_root).resolve(),
        "isrc": Path(information_source_root).resolve(),
        "asm_rt": Path(assisted_static_reading_runtime_root).resolve(),
        "asm": Path(assisted_static_reading_mode_root).resolve(),
        "vc": Path(vision_capture_runtime_root).resolve(),
        "vc_gov": Path(vision_capture_governance_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "vop": Path(voice_output_plane_adapter_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    rrd_current = _read_json(roots["rrd"] / "static_readable_region_current_case_dryrun_v1.json") or {}
    task_avail = rrd_current.get("task_context_available", False)
    scene_avail = rrd_current.get("scene_context_available", False)

    clarifications = [
        {
            "clarification_type": ct,
            "trigger_condition": trig,
            "prompt_candidate": prompt,
            "priority_level": pri,
            "user_effort_level": effort,
            "tts_invoked_now": False,
            "speech_request_submitted_now": False,
            "runtime_action_committed": False,
            "fact_status": "not_fact",
        }
        for ct, trig, prompt, pri, effort in CLARIFICATIONS
    ]

    current = {
        "schema_version": "static_reading_task_scene_context_current_case_dryrun_v1",
        "current_case_loaded": True,
        "task_context_available": task_avail,
        "scene_context_available": scene_avail,
        "missing_context_status": "missing_both_task_and_scene",
        "user_clarification_candidate_generated": True,
        "clarification_candidates": clarifications,
        "readable_region_runtime_preconditions_met_now": False,
        "readable_region_runtime_invoked_now": False,
        "information_source_runtime_invoked_now": False,
        "ranked_information_source_area_generated": False,
        "task_context_fabricated": False,
        "scene_context_fabricated": False,
        "information_source_localization_decision": "WAIT_FOR_TASK_SCENE_CONTEXT",
        "readable_region_discovery_invoked_now": False,
        "recommended_next_phase": "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1",
        "alternate_next_phase": "User-Clarification-Prompt-Template-for-Reading-v1",
        "note": "no_task_scene_or_ranked_source_fabricated_in_policy_phase",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    preconditions = {
        "schema_version": "static_reading_readable_region_runtime_preconditions_v1",
        "preconditions": [
            {"name": "task_context_available", "required_value": True},
            {"name": "scene_context_available", "required_value": True},
            {"name": "normalized_task_type_available", "required_value": True},
            {"name": "normalized_scene_type_available", "required_value": True},
            {"name": "ranked_information_source_area_available", "required_value": True},
            {"name": "safety_not_blocking", "required_value": True},
            {"name": "stc_freshness_valid", "required_value": True},
        ],
        "preconditions_defined": True,
        "runtime_preconditions_met_now": False,
        "readable_region_runtime_invoked_now": False,
        "information_source_localization_runtime_allowed_when_met": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    handoff = {
        "schema_version": "static_reading_information_source_query_handoff_policy_v1",
        "payload_fields": [
            "task_context",
            "scene_context",
            "normalized_task_type",
            "normalized_scene_type",
            "target_information_need",
            "likely_information_source_areas",
            "excluded_source_areas",
            "human_assistance_fallback",
            "confidence_policy",
            "readable_region_discovery_preconditions",
        ],
        "handoff_allowed_later": True,
        "handoff_invoked_now": False,
        "information_source_query_example": {
            "normalized_task_type": None,
            "normalized_scene_type": None,
            "target_information_need": None,
            "likely_information_source_areas": [],
            "note": "populated_only_when_context_available",
        },
        "readable_region_discovery_preconditions": preconditions["preconditions"],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "static_reading_task_scene_context_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "task_scene_context_policy_only",
            "based_on_readable_region_policy": roots["rrd"].is_dir(),
            "based_on_information_source_localization_policy": roots["isrc"].is_dir(),
            "task_context_schema_defined": True,
            "scene_context_schema_defined": True,
            "task_scene_matrix_defined": True,
            "missing_context_handling_defined": True,
            "user_clarification_candidate_policy_defined": True,
            "context_confidence_policy_defined": True,
            "information_source_query_handoff_defined": True,
            "readable_region_runtime_precondition_defined": True,
            "task_context_fabrication_forbidden": True,
            "scene_context_fabrication_forbidden": True,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "task_schema": {
            "schema_version": "static_reading_task_context_schema_v1",
            "fields": [
                "task_context_id",
                "source",
                "task_type",
                "target_information_need",
                "urgency_level",
                "safety_relevance",
                "user_confirmed",
                "confidence_placeholder",
                "ttl_policy",
                "privacy_sensitivity",
            ],
            "allowed_sources": TASK_CONTEXT_SOURCES,
            "fabrication_forbidden": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_schema": {
            "schema_version": "static_reading_scene_context_schema_v1",
            "fields": [
                "scene_context_id",
                "source",
                "scene_type",
                "scene_confidence_placeholder",
                "confirmation_required",
                "stale_policy",
                "spatial_anchor",
            ],
            "allowed_sources": SCENE_CONTEXT_SOURCES,
            "scene_types": SCENE_TYPES,
            "fabrication_forbidden": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "task_norm": {
            "schema_version": "static_reading_task_normalization_policy_v1",
            "entries": [
                {
                    "raw_user_intent_example": raw,
                    "normalized_task_type": ntype,
                    "target_information_need": need,
                    "static_reading_required_when": static_when,
                    "visual_semantic_preferred_when": vis_when,
                    "ocr_needed_when": ocr_when,
                    "human_assistance_allowed": human,
                    "fact_status": "not_fact",
                }
                for raw, ntype, need, static_when, vis_when, ocr_when, human in TASK_NORMALIZATION
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_norm": {
            "schema_version": "static_reading_scene_normalization_policy_v1",
            "entries": [
                {
                    "raw_scene_signal": raw,
                    "normalized_scene_type": ntype,
                    "confirmation_signal_required": confirm,
                    "likely_information_sources": likely,
                    "unlikely_information_sources": unlikely,
                    "fallback_if_uncertain": fallback,
                    "scene_detector_not_invoked": True,
                    "fact_status": "not_fact",
                }
                for raw, ntype, confirm, likely, unlikely, fallback in SCENE_NORMALIZATION
            ],
            "policy_only_no_scene_detector": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "matrix": {
            "schema_version": "static_reading_task_scene_matrix_v1",
            "rows": [
                {
                    "normalized_task_type": task,
                    "normalized_scene_type": scene,
                    "likely_information_source_areas": areas,
                    "preferred_non_ocr_path": non_ocr,
                    "readable_region_expected": readable,
                    "human_assistance_fallback": human,
                    "if_not_found_next_search_area": next_areas,
                    "fact_status": "not_fact",
                }
                for task, scene, areas, non_ocr, readable, human, next_areas in TASK_SCENE_MATRIX
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "missing": {
            "schema_version": "static_reading_missing_context_handling_policy_v1",
            "cases": [
                {
                    "missing_or_invalid_condition": cond,
                    "allowed_action": allowed,
                    "blocked_action": blocked,
                    "user_clarification_allowed": clar,
                    "readable_region_discovery_allowed_now": rrd,
                    "information_source_localization_runtime_allowed_now": isrc,
                    "fact_status": "not_fact",
                }
                for cond, allowed, blocked, clar, rrd, isrc in MISSING_CONTEXT
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "clarification": {
            "schema_version": "static_reading_user_clarification_candidate_policy_v1",
            "candidates": clarifications,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "confidence": {
            "schema_version": "static_reading_context_confidence_uncertainty_policy_v1",
            "levels": [
                {
                    "level": level,
                    "criteria": crit,
                    "allowed_next_action": allowed,
                    "blocked_next_action": blocked,
                    "confirmation_required": confirm,
                    "can_feed_long_term_candidate": lt,
                    "fact_status": "not_fact",
                }
                for level, crit, allowed, blocked, confirm, lt in CONFIDENCE_LEVELS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "handoff": handoff,
        "preconditions": preconditions,
        "current": current,
        "boundary": {
            "schema_version": "static_reading_task_scene_context_boundary_report_v1",
            "policy_only": True,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_reading_task_scene_context_metrics_candidate_report_v1",
            "task_context_schema_defined": True,
            "scene_context_schema_defined": True,
            "task_normalization_policy_count": len(TASK_NORMALIZATION),
            "scene_normalization_policy_count": len(SCENE_NORMALIZATION),
            "task_scene_matrix_count": len(TASK_SCENE_MATRIX),
            "missing_context_handling_count": len(MISSING_CONTEXT),
            "user_clarification_candidate_count": len(CLARIFICATIONS),
            "readable_region_preconditions_defined": True,
            "runtime_action_committed_count": 0,
            "scene_detector_invoked_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_reading_task_scene_context_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_reading_task_scene_context_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_reading_task_scene_context_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
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
            "schema_version": "static_reading_task_scene_context_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_reading_task_scene_context_non_claims_report_v1",
            "claims": [
                "no_real_scene_recognition",
                "no_real_task_understanding",
                "task_schema_not_task_fact",
                "scene_schema_not_scene_fact",
                "clarification_not_runtime_tts",
                "matrix_not_runtime_inference",
                "no_ocr",
                "no_camera",
                "no_map_api",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "static_reading_task_scene_context_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "static_reading_task_scene_context_audit_report_v1",
            "static_reading_task_scene_context_policy_v1_executed": True,
            "policy_only": True,
            "task_context_schema_defined": True,
            "scene_context_schema_defined": True,
            "task_scene_matrix_defined": True,
            "task_context_fabrication_forbidden": True,
            "scene_context_fabrication_forbidden": True,
            "readable_region_runtime_precondition_defined": True,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "map_api_invoked": False,
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
