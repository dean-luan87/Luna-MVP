# -*- coding: utf-8 -*-
"""Static Readable Region Discovery Guidance Policy v1 — policy only (no detector/OCR/camera).

Phase-Static-Readable-Region-Discovery-Guidance-Policy-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Readable-Region-Discovery-Guidance-Policy-v1-001"
P3 = "P3_OCR_GUIDANCE"

FOLLOWUPS = [
    "Static-Reading-Task-Scene-Context-Policy-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

ALLOWED_SCOPE = [
    ("ranked_candidate_information_source_area", True, "information_source_ranking_complete"),
    ("user_selected_target_area", True, "user_confirmed_area"),
    ("worldmodel_suggested_anchor_area", True, "wm_anchor_available"),
    ("scene_task_inferred_source_area", True, "task_and_scene_available"),
    ("human_staff_indicated_area", True, "staff_or_user_pointed"),
]

FORBIDDEN_SCOPE = [
    ("full_frame_generic_text_search", False, "always"),
    ("task_irrelevant_advertising_area", False, "ads_only"),
    ("private_sensitive_area_without_user_request", False, "no_consent"),
    ("unsafe_to_approach_area", False, "safety_alert"),
]

REGION_KINDS = [
    "signboard", "doorplate", "screen", "paper_document", "notice_board",
    "package_label", "counter_label", "wayfinding_marker",
]

FILTER_DIMS = [
    ("task_relevance", "matches_target_information_need", "off_task_text", "re_rank_or_exclude", "task_mismatch", True, True),
    ("safety_relevance", "safe_to_approach", "unsafe_area", "stop_approach", "safety_alert", False, False),
    ("expected_text_length", "fits_task_need", "too_long_unrequested", "narrow_scope", "dense_unrequested", True, True),
    ("distance", "within_readable_distance", "too_far", "move_closer", "beyond_safe_range", True, True),
    ("angle", "acceptable_view_angle", "excessive_skew", "adjust_angle", "occluded_view", True, True),
    ("occlusion", "region_visible", "blocked", "change_viewpoint", "permanent_block", True, True),
    ("glare_or_reflection", "low_glare", "strong_glare", "change_angle_or_light", "unfixable_glare", True, True),
    ("text_size", "pixel_height_sufficient", "too_small", "move_closer_or_zoom", "illegible_at_safe_distance", True, True),
    ("contrast", "sufficient_contrast", "low_contrast", "improve_lighting", "faded_text", True, True),
    ("stability", "stable_view_possible", "motion_blur", "hold_still", "user_moving", True, True),
    ("privacy_sensitivity", "user_consent_or_low_sensitivity", "high_privacy_no_consent", "ask_user_or_staff", "private_id_unprompted", False, True),
    ("user_request_specificity", "user_asked_or_task_bound", "unsolicited_read", "exclude", "no_read_intent", True, True),
]

CLASSIFICATIONS = [
    ("READABLE_CANDIDATE", "passes_filters_in_source_area", "proceed_to_static_capture_candidate", "global_ocr", True, True),
    ("UNREADABLE_BUT_REPAIRABLE", "repairable_with_guidance", "apply_view_guidance", "ocr_now", True, False),
    ("UNREADABLE_NOT_REPAIRABLE", "cannot_repair_safely", "exclude_or_human_assist", "force_ocr", False, False),
    ("IRRELEVANT_TEXT_REGION", "off_task", "exclude", "ocr", False, False),
    ("NOT_WORTH_READING", "low_value_for_task", "exclude", "ocr", False, False),
    ("PRIVACY_SENSITIVE_REQUIRES_CONFIRMATION", "sensitive_text", "confirm_with_user", "read_without_consent", False, False),
    ("SAFETY_RELEVANT_SHORT_TEXT", "short_safety_marker", "read_if_task_needs", "long_read", True, True),
    ("TASK_RELEVANT_STATIC_TEXT", "task_bound_static_text", "static_capture_candidate", "dynamic_reocr", True, True),
]

VIEW_GUIDANCE = [
    ("move_left", "region_off_left", "请稍微向左移动，把目标区域移到画面中央。", "centering", "do_not_step_into_traffic"),
    ("move_right", "region_off_right", "请稍微向右移动。", "centering", "do_not_step_into_traffic"),
    ("move_closer", "text_too_small", "请稍微靠近一点，再保持稳定。", "text_size", "maintain_safe_distance"),
    ("move_back", "too_close_or_blur", "请稍微后退一点。", "focus", "watch_obstacles"),
    ("raise_camera", "region_too_low", "请稍微抬高设备。", "framing", "stable_hold"),
    ("lower_camera", "region_too_high", "请稍微放低设备。", "framing", "stable_hold"),
    ("center_region", "off_center", "请把目标文字放在画面中央。", "centering", "hold_still"),
    ("adjust_angle", "skew_detected", "请稍微调整角度，避免斜着拍。", "angle", "no_unsafe_lean"),
    ("hold_still", "motion_blur_risk", "请先停稳，保持画面稳定。", "stability", "safety_first"),
    ("zoom_or_magnify", "text_still_small", "可以尝试放大画面后再读。", "text_size", "optional_hardware_later"),
    ("ask_external_assistance", "cannot_repair_alone", "如果不方便调整，可以请身边人帮忙看一下。", "human_assist", "privacy_respect"),
]

RANKING_DIMS = [
    ("parent_source_priority", 0.2, True, "source_not_ranked"),
    ("task_relevance", 0.2, True, "off_task"),
    ("safety_relevance", 0.15, True, "unsafe"),
    ("distance", 0.1, False, "too_far"),
    ("accessibility", 0.1, True, "blocked"),
    ("visibility", 0.1, True, "occluded"),
    ("expected_readability", 0.05, True, "known_bad"),
    ("user_effort", 0.05, False, "excessive_effort"),
    ("privacy_sensitivity", 0.03, True, "no_consent"),
    ("human_assistance_available", 0.02, True, "privacy_block"),
]

HUMAN_ASSIST = [
    ("ask_staff_where_sign_is", "source_area_ambiguous", "low", True, "请问指示牌/服务台在哪里？"),
    ("ask_staff_confirm_counter_or_room", "hospital_or_office", "low", True, "请帮忙确认柜台或房间位置。"),
    ("ask_nearby_person_point_to_text", "region_hard_to_find", "medium", True, "能帮我指一下那块牌子吗？"),
    ("ask_nearby_person_read_short_text", "short_critical_text", "medium", True, "能帮我看一下上面的字吗？"),
    ("ask_user_manual_input", "ocr_not_viable", "high", False, "如果看不清，您可以口述关键信息。"),
]

EXPIRED_TYPES = [
    ("unresolved_readable_region_candidate", "region_unreadable_after_guidance"),
    ("repeated_unreadable_region_candidate", "multiple_failures_same_area"),
    ("expired_readable_region_candidate", "context_expired"),
    ("user_environment_context_candidate", "scene_layout_hint"),
    ("user_profile_context_candidate", "reading_preference"),
    ("emotional_context_background_candidate", "stress_urgency"),
]

OPTIONAL_PATHS = [
    ("detector_registry", "capabilities/vision/text_detector_dryrun_v1.py"),
    ("task_context_store", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("info_source", roots["isrc"], "static_reading_information_source_localization_policy_v1_summary.json", False),
        ("asm_runtime", roots["asm_rt"], "assisted_static_reading_runtime_dryrun_v1_summary.json", False),
        ("asm_mode", roots["asm"], "assisted_static_reading_mode_v1_summary.json", False),
        ("vc_runtime", roots["vc"], "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("vc_gov", roots["vc_gov"], "vision_capture_governance_v1_summary.json", False),
        ("ocr_act", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
        ("vop", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json", False),
        ("vg_runtime", roots["vg"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json", False),
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
    handoff = _read_json(roots["isrc"] / "static_reading_readable_region_discovery_handoff_policy_v1.json")
    if handoff:
        rows.append(
            {
                "intake_id": "rrd_handoff",
                "input_source": "info_source",
                "source_root_or_path": str(roots["isrc"]),
                "artifact": "static_reading_readable_region_discovery_handoff_policy_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": handoff.get("payload_fields") or [],
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
    return {"schema_version": "static_readable_region_input_intake_matrix_v1", "rows": rows, "fact_status": "not_fact", "write_allowed": False}


def run_static_readable_region_discovery_guidance_policy_v1(
    *,
    information_source_root: str,
    assisted_static_reading_runtime_root: str,
    assisted_static_reading_mode_root: str,
    vision_capture_runtime_root: str,
    vision_capture_governance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    voice_output_plane_adapter_root: str,
    voice_guidance_runtime_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "isrc": Path(information_source_root).resolve(),
        "asm_rt": Path(assisted_static_reading_runtime_root).resolve(),
        "asm": Path(assisted_static_reading_mode_root).resolve(),
        "vc": Path(vision_capture_runtime_root).resolve(),
        "vc_gov": Path(vision_capture_governance_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "vop": Path(voice_output_plane_adapter_root).resolve(),
        "vg": Path(voice_guidance_runtime_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    isrc_case = _read_json(roots["isrc"] / "static_reading_information_source_current_case_dryrun_v1.json") or {}
    handoff = _read_json(roots["isrc"] / "static_reading_readable_region_discovery_handoff_policy_v1.json") or {}

    current = {
        "schema_version": "static_readable_region_current_case_dryrun_v1",
        "current_case_loaded": True,
        "information_source_localization_decision": isrc_case.get(
            "information_source_localization_decision", "WAIT_FOR_TASK_SCENE_CONTEXT"
        ),
        "task_context_available": isrc_case.get("task_context_available", False),
        "scene_context_available": isrc_case.get("scene_context_available", False),
        "readable_region_discovery_policy_ready": True,
        "readable_region_discovery_invoked_now": False,
        "reason_not_invoked": [
            "missing_task_context",
            "missing_scene_context",
            "no_ranked_information_source_area",
        ],
        "mode_entry_decision": "ENTER_ASSISTED_STATIC_READING_CANDIDATE",
        "current_state": "WAITING_FOR_USER_STABILIZATION",
        "handoff_payload_fields_consumed": handoff.get("payload_fields") or [],
        "recommended_next_phase": "Static-Reading-Task-Scene-Context-Policy-v1",
        "alternate_next_phase": "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
        "note": "no_readable_region_fabricated_without_task_scene_and_source_area",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "static_readable_region_discovery_guidance_policy_v1_summary_v0",
            "phase": PHASE_ID,
            "policy_scope": "readable_region_discovery_guidance_policy_only",
            "based_on_information_source_localization": roots["isrc"].is_dir(),
            "based_on_assisted_static_reading_runtime": roots["asm_rt"].is_dir(),
            "candidate_information_source_handoff_consumed": handoff.get("readable_region_discovery_allowed_later") is True,
            "readable_region_candidate_schema_defined": True,
            "discovery_scope_policy_defined": True,
            "readability_filtering_policy_defined": True,
            "user_view_guidance_policy_defined": True,
            "region_ranking_policy_defined": True,
            "static_capture_handoff_policy_defined": True,
            "unresolved_expired_candidate_policy_defined": True,
            "human_staff_assistance_preserved": True,
            "global_text_search_forbidden_by_default": True,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
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
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "discovery_scope": {
            "schema_version": "static_readable_region_discovery_scope_policy_v1",
            "discovery_scope_is_candidate_information_source_only": True,
            "global_text_search_forbidden": True,
            "allowed_search_scope": [
                {"scope_type": s, "allowed": a, "required_context": ctx, "blocked_when": [], "fact_status": "not_fact"}
                for s, a, ctx in ALLOWED_SCOPE
            ],
            "forbidden_search_scope": [
                {"scope_type": s, "allowed": a, "required_context": "n/a", "blocked_when": [blk], "fact_status": "not_fact"}
                for s, a, blk in FORBIDDEN_SCOPE
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "candidate_schema": {
            "schema_version": "static_readable_region_candidate_schema_v1",
            "fields": [
                "readable_region_candidate_id", "parent_information_source_id", "source_area_type",
                "expected_text_type", "expected_region_kind", "approximate_location_hint",
                "visual_semantic_clues", "bbox_candidate_unknown_by_default", "detector_required_later",
                "ocr_required_later", "readability_status_unknown_by_default", "fact_status", "write_allowed",
            ],
            "expected_region_kinds": REGION_KINDS,
            "bbox_candidate_unknown_by_default": True,
            "readability_status_unknown_by_default": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "readability_filter": {
            "schema_version": "static_readable_region_readability_filtering_policy_v1",
            "dimensions": [
                {
                    "filtering_dimension": dim,
                    "pass_condition_placeholder": pass_c,
                    "fail_condition_placeholder": fail_c,
                    "repair_action": repair,
                    "exclude_when": excl,
                    "can_retry_with_guidance": retry,
                    "can_feed_unresolved_candidate": unresolved,
                    "fact_status": "not_fact",
                }
                for dim, pass_c, fail_c, repair, excl, retry, unresolved in FILTER_DIMS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "classification": {
            "schema_version": "static_readable_region_classification_policy_v1",
            "classes": [
                {
                    "class_name": name,
                    "criteria": crit,
                    "allowed_next_action": allowed,
                    "blocked_action": blocked,
                    "user_guidance_needed": guidance,
                    "ocr_allowed_later": ocr_later,
                    "fact_status": "not_fact",
                }
                for name, crit, allowed, blocked, guidance, ocr_later in CLASSIFICATIONS
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "view_guidance": {
            "schema_version": "static_readable_region_user_view_guidance_policy_v1",
            "actions": [
                {
                    "guidance_action": act,
                    "trigger_condition": cond,
                    "prompt_candidate": prompt,
                    "expected_region_improvement": imp,
                    "safety_constraint": safety,
                    "priority": P3,
                    "tts_invoked_now": False,
                    "speech_request_submitted_now": False,
                    "runtime_action_committed_now": False,
                    "fact_status": "not_fact",
                }
                for act, cond, prompt, imp, safety in VIEW_GUIDANCE
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ranking": {
            "schema_version": "static_readable_region_ranking_selection_policy_v1",
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
        "capture_handoff": {
            "schema_version": "static_readable_region_static_capture_handoff_policy_v1",
            "payload_fields": [
                "readable_region_candidate_id",
                "parent_information_source_id",
                "target_information_need",
                "task_type",
                "scene_type",
                "expected_text_type",
                "user_guidance_hint",
                "required_readiness_dimensions",
            ],
            "required_readiness_dimensions": [
                "user_stability", "target_centering", "viewing_angle",
                "distance_and_scale", "lighting_and_clarity",
            ],
            "static_capture_allowed_later": True,
            "static_capture_invoked_now": False,
            "ocrrequest_generated_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ocr_gate_link": {
            "schema_version": "static_readable_region_ocrrequest_future_gate_link_policy_v1",
            "linked_to_assisted_static_reading_ocrrequest_future_gate": True,
            "readable_region_candidate_required_before_ocrrequest": True,
            "static_capture_required_before_ocrrequest": True,
            "stc_freshness_required": True,
            "safety_not_blocking_required": True,
            "task_context_valid_required": True,
            "ocrrequest_eligible_later": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_assist": {
            "schema_version": "static_readable_region_human_staff_assistance_preservation_policy_v1",
            "candidates": [
                {
                    "assistance_type": atype,
                    "trigger_condition": cond,
                    "privacy_safety_considerations": priv,
                    "user_confirmation_required": confirm,
                    "prompt_candidate": prompt,
                    "action_committed_now": False,
                    "fact_status": "not_fact",
                }
                for atype, cond, priv, confirm, prompt in HUMAN_ASSIST
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "expired": {
            "schema_version": "static_readable_region_unresolved_expired_candidate_policy_v1",
            "candidates": [
                {
                    "candidate_type": ctype,
                    "source_signal": sig,
                    "cannot_use_for_action": True,
                    "cannot_write_fact": True,
                    "can_feed_long_term_candidate": True,
                    "required_metadata": [
                        "source_chain", "time_anchor", "spatial_anchor", "parent_information_source",
                        "original_task_context", "stale_or_unresolved_reason", "confidence_decay",
                        "privacy_sensitivity", "future_usage_scope",
                    ],
                    "write_allowed_now": False,
                    "fact_status": "not_fact",
                }
                for ctype, sig in EXPIRED_TYPES
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "current": current,
        "boundary": {
            "schema_version": "static_readable_region_boundary_report_v1",
            "policy_only": True,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
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
            "schema_version": "static_readable_region_metrics_candidate_report_v1",
            "readable_region_candidate_schema_defined": True,
            "discovery_scope_policy_defined": True,
            "readability_filtering_policy_defined": True,
            "classification_policy_defined": True,
            "user_view_guidance_policy_defined": True,
            "region_ranking_policy_defined": True,
            "static_capture_handoff_policy_defined": True,
            "ocrrequest_future_gate_link_defined": True,
            "unresolved_expired_candidate_policy_defined": True,
            "guidance_action_count": len(VIEW_GUIDANCE),
            "classification_count": len(CLASSIFICATIONS),
            "filtering_dimension_count": len(FILTER_DIMS),
            "runtime_action_committed_count": 0,
            "detector_invoked_count": 0,
            "ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_readable_region_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_readable_region_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_readable_region_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "policy_only": True,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
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
            "schema_version": "static_readable_region_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_readable_region_non_claims_report_v1",
            "claims": [
                "no_real_region_detection",
                "no_detector",
                "no_ocr",
                "no_camera",
                "no_map_api",
                "candidate_not_detected_fact",
                "filtering_not_real_quality_judge",
                "view_guidance_policy_not_runtime_prompt",
                "capture_handoff_future_only",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "static_readable_region_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "static_readable_region_audit_report_v1",
            "static_readable_region_discovery_guidance_policy_v1_executed": True,
            "policy_only": True,
            "readable_region_candidate_schema_defined": True,
            "discovery_scope_policy_defined": True,
            "global_text_search_forbidden_by_default": True,
            "static_capture_handoff_policy_defined": True,
            "ocrrequest_future_gate_link_defined": True,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
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
