# -*- coding: utf-8 -*-
"""Static Reading Information Source Localization Policy v1 — policy only (no OCR/detector/camera).

Phase-Static-Reading-Information-Source-Localization-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Reading-Information-Source-Localization-Policy-v1-001"

FOLLOWUPS = [
    "Static-Readable-Region-Discovery-Guidance-Policy-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

OPTIONAL_WM_PATHS = [
    ("worldmodel_unresolved_slot_contract", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
    ("worldmodel_map_anchor", "docs/architecture/LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md"),
    ("worldmodel_unresolved_slot_smoke", "_eval_out/worldmodel_unresolved_observation_slot_contract_v0/worldmodel_unresolved_slot_contract_summary.json"),
]

WM_LOOKUP_SOURCES = [
    ("world_model_spatial_anchor", "destination_arrival_confirmation", "known_sign_location"),
    ("known_place_memory", "shop_name_confirmation", "known_shopfront_or_logo_area"),
    ("route_context", "exit_search", "known_elevator_or_floor_guide"),
    ("task_context", "user_explicit_read_this", "task_bound_region"),
    ("repeated_observation_history", "room_or_doorplate_reading", "known_doorplate_location"),
    ("unresolved_history_slot", "warning_or_safety_marker", "candidate_anchor_unresolved"),
    ("user_environment_context_candidate", "restroom_search", "known_facility_sign"),
]

SCENES = [
    ("street", ["road_sign", "building_number"], ["shopfront", "bus_stop_sign", "warning_marker"], ["menu_detail"], True),
    ("shopping_mall", ["directory_board"], ["elevator_area", "restroom_sign", "shopfront", "service_desk"], ["medicine_label"], True),
    ("park", ["entrance_map"], ["warning_sign", "facility_sign", "service_board"], ["ticket_window"], False),
    ("hospital", ["department_sign", "floor_guide"], ["room_doorplate", "registration_counter", "staff_desk"], ["shop_name"], True),
    ("transit_station", ["platform_sign", "exit_sign"], ["line_number", "electronic_screen", "staff_counter"], ["room_doorplate"], True),
    ("office_building", ["lobby_directory"], ["elevator_board", "room_doorplate", "reception"], ["transit_line"], False),
    ("residential_building", ["building_number"], ["unit_doorplate", "notice_board"], ["hospital_department"], False),
    ("shopfront", ["logo_area", "signboard"], ["window_poster", "price_board"], ["platform_sign"], False),
    ("indoor_corridor", ["room_doorplate"], ["direction_sign", "elevator_board"], ["outdoor_road"], False),
    ("service_counter_area", ["staff_desk", "service_desk"], ["counter_sign", "queue_board"], ["park_map"], True),
    ("unknown_scene", [], [], ["all_specific"], True),
]

TASKS = [
    ("destination_arrival_confirmation", "confirm_target_place_or_entrance", "visual_semantic_first", ["directory_board", "shopfront", "building_number"], "static_sign_unclear", True, "ask_human_or_reorient"),
    ("shop_name_confirmation", "confirm_shop_identity", "visual_semantic_first", ["shopfront", "logo_area", "signboard"], "name_not_visible", True, "ask_nearby_or_move"),
    ("room_or_doorplate_reading", "read_room_or_unit_id", "static_reading", ["room_doorplate", "unit_doorplate"], "doorplate_unreadable", True, "ask_staff"),
    ("hospital_department_or_room", "find_department_or_room", "visual_semantic_first", ["department_sign", "floor_guide", "staff_desk"], "sign_missing", True, "ask_staff_for_location"),
    ("transit_line_or_platform", "confirm_line_or_platform", "visual_semantic_first", ["platform_sign", "electronic_screen", "line_number"], "screen_too_small", False, "ask_staff"),
    ("restroom_search", "find_restroom", "visual_semantic_first", ["restroom_sign", "directory_board"], "sign_not_found", True, "ask_human_or_staff"),
    ("exit_search", "find_exit", "visual_semantic_first", ["exit_sign", "directory_board"], "exit_unclear", True, "ask_human"),
    ("warning_or_safety_marker", "confirm_safety_marker", "visual_semantic_first", ["warning_marker", "warning_sign"], "marker_ambiguous", False, "maintain_distance"),
    ("ticket_window_or_counter", "find_ticket_or_service_counter", "visual_semantic_first", ["staff_counter", "service_desk", "ticket_window_sign"], "counter_not_visible", True, "ask_staff"),
    ("medicine_label_or_document", "read_label_or_document", "static_reading", ["medicine_label_area", "document_holder"], "text_too_small", True, "ask_pharmacist"),
    ("menu_or_price_reading", "read_menu_or_price", "static_reading", ["menu_board", "price_board"], "glare_or_distance", True, "move_closer"),
    ("user_explicit_read_this", "read_user_indicated_target", "static_reading", ["user_pointed_region"], "region_not_identified", True, "confirm_with_user"),
]

MATRIX_ROWS = [
    ("street", "shopfront", ["shop_name"], ["storefront_logo"], True, "medium", "sign_visible", "decorative_only"),
    ("street", "road_sign", ["destination", "warning"], ["pole_sign"], True, "high", "task_needs_direction", "unrelated_ad"),
    ("shopping_mall", "directory_board", ["destination", "restroom", "shop"], ["mall_map"], True, "high", "navigation_task", "ads_only"),
    ("shopping_mall", "restroom_sign", ["restroom_search"], ["wc_icon_sign"], True, "high", "restroom_task", "wrong_floor"),
    ("shopping_mall", "service_desk", ["ticket_window", "info"], ["counter_area"], True, "medium", "need_staff_help", "closed_counter"),
    ("hospital", "department_sign", ["hospital_department"], ["dept_board"], True, "high", "hospital_task", "unrelated_poster"),
    ("hospital", "room_doorplate", ["room_reading"], ["door_plate"], True, "high", "static_reading_task", "private_room"),
    ("transit_station", "platform_sign", ["transit_line"], ["platform_board"], True, "high", "transit_task", "old_schedule"),
    ("transit_station", "exit_sign", ["exit_search"], ["exit_arrow_sign"], True, "high", "exit_task", "maintenance_cover"),
    ("office_building", "lobby_directory", ["destination"], ["directory_panel"], True, "medium", "office_navigation", "tenant_ads"),
    ("residential_building", "building_number", ["destination_arrival"], ["entrance_number"], True, "medium", "arrival_confirm", "neighbor_notice"),
    ("shopfront", "signboard", ["shop_name"], ["main_sign"], True, "high", "shop_confirm", "decorative_window"),
]

EXCLUSIONS = [
    ("advertising_unrelated_to_task", "poster_not_matching_task", "visual_semantic_fallback", True),
    ("decorative_text", "ornamental_only", "skip_region", False),
    ("dense_text_not_requested", "user_did_not_ask_full_read", "summarize_or_skip", True),
    ("far_small_text_low_value", "low_expected_gain", "move_closer_or_skip", False),
    ("unsafe_to_approach", "safety_risk", "stop_reading", False),
    ("private_sensitive_text", "privacy_block", "external_assistance", True),
    ("task_irrelevant_poster", "no_task_link", "exclude_region", True),
    ("stale_context_not_actionable", "expired_sign", "long_term_candidate", True),
    ("route_unrelated_signage", "off_route", "re_rank_sources", True),
    ("user_not_requesting_reading", "no_read_intent", "defer_ocr", False),
]

HUMAN_ASSIST = [
    ("ask_nearby_person_where_to_find_information", "source_not_found_in_scene", "low", "请问附近哪里有指示牌/服务台？", True),
    ("ask_nearby_person_read_short_text", "short_critical_text", "medium", "可以帮我看一下这块牌子吗？", True),
    ("ask_staff_for_location", "hospital_or_transit_or_mall", "low", "请问服务台/咨询台在哪里？", True),
    ("ask_service_counter", "counter_visible", "low", "请到服务台确认位置。", False),
    ("ask_user_confirm_whether_to_search_nearby", "scene_unlikely_has_info", "low", "当前场景可能没有目标信息，要去附近找吗？", True),
]

RANKING_DIMS = [
    ("task_relevance", 0.35, True, "task_mismatch"),
    ("scene_likelihood", 0.2, True, "scene_mismatch"),
    ("distance", 0.1, False, "too_far_unsafe"),
    ("accessibility", 0.1, True, "blocked_path"),
    ("visibility", 0.1, True, "occluded"),
    ("safety", 0.1, True, "safety_alert"),
    ("expected_readability", 0.05, True, "known_unreadable"),
    ("non_ocr_path_available", 0.0, True, "none"),
    ("human_assistance_available", 0.0, True, "privacy_block"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
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
    for oid, rel in OPTIONAL_WM_PATHS:
        p = ws / rel
        rows.append(
            {
                "intake_id": oid,
                "input_source": "optional_worldmodel",
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
    rows.append(
        {
            "intake_id": "scene_registry",
            "input_source": "optional_scene_registry",
            "source_root_or_path": str(ws / "docs/architecture"),
            "artifact": "(not_found_in_repo)",
            "loaded": False,
            "optional": True,
            "key_fields_observed": [],
            "intake_status": "optional_missing",
            "fact_status": "not_fact",
            "write_allowed": False,
        }
    )
    return {"schema_version": "static_reading_information_source_input_intake_matrix_v1", "rows": rows, "fact_status": "not_fact", "write_allowed": False}


def run_static_reading_information_source_localization_policy_v1(
    *,
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

    asm_rt = _read_json(roots["asm_rt"] / "assisted_static_reading_runtime_final_decision_v1.json") or {}
    wm_any = any((ws / rel).is_file() for _, rel in OPTIONAL_WM_PATHS)

    current = {
        "schema_version": "static_reading_information_source_current_case_dryrun_v1",
        "current_case_loaded": True,
        "task_context_available": False,
        "scene_context_available": False,
        "worldmodel_lookup_available": wm_any,
        "if_task_scene_missing_then_policy_status": "requires_task_and_scene_context",
        "mode_entry_decision": "ENTER_ASSISTED_STATIC_READING_CANDIDATE",
        "information_source_localization_decision": "WAIT_FOR_TASK_SCENE_CONTEXT",
        "current_state_from_asm_runtime": asm_rt.get("current_state", "WAITING_FOR_USER_STABILIZATION"),
        "first_guidance_action": "hold_still",
        "note": "OCR_failure_chain_case_lacks_explicit_task_and_scene; do_not_fabricate_scene_type",
        "readable_region_discovery_invoked_now": False,
        "recommended_next_phase": "Static-Readable-Region-Discovery-Guidance-Policy-v1",
        "runtime_action_committed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "static_reading_information_source_localization_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "information_source_localization_policy_only",
            "based_on_assisted_static_reading_runtime": roots["asm_rt"].is_dir(),
            "based_on_assisted_static_reading_mode": roots["asm"].is_dir(),
            "worldmodel_first_lookup_policy_defined": True,
            "scene_recognition_fallback_policy_defined": True,
            "task_to_information_need_mapping_defined": True,
            "scene_to_information_source_matrix_defined": True,
            "candidate_information_source_ranking_defined": True,
            "human_or_staff_assistance_fallback_defined": True,
            "readable_region_discovery_handoff_defined": True,
            "global_text_search_forbidden_by_default": True,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "hardware_action_invoked": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "wm_lookup": {
            "schema_version": "static_reading_worldmodel_first_lookup_policy_v1",
            "use_worldmodel_first": True,
            "lookup_sources": [s[0] for s in WM_LOOKUP_SOURCES],
            "lookup_targets": list({s[2] for s in WM_LOOKUP_SOURCES}),
            "entries": [
                {
                    "lookup_source": src,
                    "target_information_type": tgt,
                    "candidate_source_area": area,
                    "confidence_policy": "candidate_only_not_fact",
                    "staleness_policy": "respect_expired_information_value",
                    "action_allowed_now": False,
                    "fact_status": "not_fact",
                }
                for src, tgt, area in WM_LOOKUP_SOURCES
            ],
            "worldmodel_runtime_available": wm_any,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_fallback": {
            "schema_version": "static_reading_scene_recognition_fallback_policy_v1",
            "scenes": [
                {
                    "scene_type": st,
                    "scene_confirmation_signals": [f"scene_hint_{st}"],
                    "likely_information_types": likely,
                    "likely_information_source_areas": areas,
                    "unlikely_information_types": unlikely,
                    "first_search_strategy": "worldmodel_then_local_sources",
                    "ask_human_or_staff_likely": ask_h,
                    "scene_confirmation_required_before_reading": True,
                    "fact_status": "not_fact",
                }
                for st, likely, areas, unlikely, ask_h in SCENES
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "task_mapping": {
            "schema_version": "static_reading_task_information_need_mapping_v1",
            "tasks": [
                {
                    "task_type": tt,
                    "target_information_need": need,
                    "preferred_non_ocr_path": pref,
                    "likely_information_sources": sources,
                    "ocr_needed_when": ocr_when,
                    "static_reading_required_when": "label_or_dense_text" in tt,
                    "human_assistance_allowed": human,
                    "fallback_if_not_found": fb,
                    "fact_status": "not_fact",
                }
                for tt, need, pref, sources, ocr_when, human, fb in TASKS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_matrix": {
            "schema_version": "static_reading_scene_information_source_matrix_v1",
            "rows": [
                {
                    "scene_type": scene,
                    "information_source_area": area,
                    "likely_information_types": types,
                    "visual_semantic_clues": clues,
                    "readable_region_expected": rr,
                    "priority": pri,
                    "ocr_activation_condition": ocr_cond,
                    "not_worth_reading_condition": nw,
                    "fact_status": "not_fact",
                }
                for scene, area, types, clues, rr, pri, ocr_cond, nw in MATRIX_ROWS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "candidate_schema": {
            "schema_version": "static_reading_candidate_information_source_schema_v1",
            "fields": [
                "candidate_source_id",
                "source_type",
                "scene_type",
                "task_type",
                "target_information_need",
                "expected_physical_location",
                "expected_visual_clues",
                "expected_readable_regions",
                "distance_priority",
                "accessibility_priority",
                "visibility_priority",
                "task_relevance_score_placeholder",
                "reading_value_score_placeholder",
                "ocr_readiness_unknown_by_default",
                "fact_status",
                "write_allowed",
            ],
            "ocr_readiness_unknown_by_default": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ranking": {
            "schema_version": "static_reading_candidate_source_ranking_policy_v1",
            "dimensions": [
                {
                    "ranking_dimension": dim,
                    "weight_placeholder": w,
                    "higher_is_better": hib,
                    "blocking_condition": block,
                    "notes": "placeholder_only_no_runtime_score",
                    "fact_status": "not_fact",
                }
                for dim, w, hib, block in RANKING_DIMS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "exclusion": {
            "schema_version": "static_reading_not_worth_reading_exclusion_policy_v1",
            "rules": [
                {
                    "exclusion_reason": reason,
                    "applies_when": when,
                    "allowed_fallback": fb,
                    "can_feed_long_term_candidate": lt,
                    "ocr_forbidden_now": True,
                    "fact_status": "not_fact",
                }
                for reason, when, fb, lt in EXCLUSIONS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_assist": {
            "schema_version": "static_reading_human_staff_assistance_fallback_policy_v1",
            "candidates": [
                {
                    "assistance_type": atype,
                    "trigger_condition": cond,
                    "privacy_safety_considerations": priv,
                    "prompt_candidate": prompt,
                    "user_confirmation_required": confirm,
                    "runtime_action_committed_now": False,
                    "fact_status": "not_fact",
                }
                for atype, cond, priv, prompt, confirm in HUMAN_ASSIST
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "handoff": {
            "schema_version": "static_reading_readable_region_discovery_handoff_policy_v1",
            "next_phase": "Static-Readable-Region-Discovery-Guidance-Policy-v1",
            "payload_fields": [
                "candidate_information_sources",
                "target_information_need",
                "scene_type",
                "task_type",
                "search_priority_order",
                "excluded_regions",
                "distance_priority",
                "expected_readable_region_types",
                "user_guidance_hint",
            ],
            "readable_region_discovery_allowed_later": True,
            "readable_region_discovery_invoked_now": False,
            "detector_invoked_now": False,
            "ocr_invoked_now": False,
            "global_text_search_forbidden": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "current": current,
        "boundary": {
            "schema_version": "static_reading_information_source_boundary_report_v1",
            "policy_only": True,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "detector_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "hardware_action_invoked": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_reading_information_source_metrics_candidate_report_v1",
            "worldmodel_first_lookup_policy_defined": True,
            "scene_recognition_fallback_policy_defined": True,
            "task_information_mapping_count": len(TASKS),
            "scene_information_source_matrix_count": len(MATRIX_ROWS),
            "exclusion_policy_count": len(EXCLUSIONS),
            "assistance_fallback_count": len(HUMAN_ASSIST),
            "readable_region_handoff_defined": True,
            "runtime_action_committed_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_reading_information_source_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_reading_information_source_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_reading_information_source_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "detector_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "hardware_action_invoked": False,
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
            "schema_version": "static_reading_information_source_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_reading_information_source_non_claims_report_v1",
            "claims": [
                "no_global_text_search",
                "no_readable_region_detection",
                "no_ocr",
                "no_camera",
                "no_map_api",
                "no_scene_fact_confirmation",
                "no_source_fact_confirmation",
                "candidate_not_fact",
                "scene_matrix_not_runtime_recognition",
                "wm_lookup_policy_not_wm_write",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "static_reading_information_source_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "static_reading_information_source_audit_report_v1",
            "static_reading_information_source_localization_policy_v1_executed": True,
            "policy_only": True,
            "worldmodel_first_lookup_policy_defined": True,
            "scene_recognition_fallback_policy_defined": True,
            "task_to_information_need_mapping_defined": True,
            "readable_region_discovery_handoff_defined": True,
            "global_text_search_forbidden_by_default": True,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "detector_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "hardware_action_invoked": False,
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
