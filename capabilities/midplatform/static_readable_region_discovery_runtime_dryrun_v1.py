# -*- coding: utf-8 -*-
"""Static Readable Region Discovery Runtime DryRun v1 — ranked source areas → readable region candidates.

Phase-Static-Readable-Region-Discovery-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Readable-Region-Discovery-Runtime-DryRun-v1-001"
FINAL_DECISION = "READY_FOR_STATIC_CAPTURE_HANDOFF_LATER"

STAFF_SOURCE_AREAS = {"service_desk", "staff_desk", "staff_counter"}

# source_area_type -> list of (expected_region_kind, expected_text_type, class_name)
REGION_EXPANSION: Dict[str, List[Tuple[str, str, str]]] = {
    "exit_sign": [
        ("wayfinding_marker", "short_text_sign", "TASK_RELEVANT_STATIC_TEXT"),
        ("short_text_sign", "exit_direction", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "directory_board": [
        ("notice_board", "floor_directory", "TASK_RELEVANT_STATIC_TEXT"),
        ("floor_directory", "mall_directory", "TASK_RELEVANT_STATIC_TEXT"),
        ("dense_text_board", "dense_directory", "READABLE_CANDIDATE"),
    ],
    "elevator_area": [
        ("wayfinding_marker", "elevator_label", "TASK_RELEVANT_STATIC_TEXT"),
        ("floor_guide", "floor_indicator", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "service_desk": [
        ("counter_label", "service_counter", "HUMAN_ASSISTANCE_REGION"),
        ("staff_assistance_region", "staff_help", "HUMAN_ASSISTANCE_REGION"),
    ],
    "department_sign": [
        ("signboard", "department_name", "TASK_RELEVANT_STATIC_TEXT"),
        ("room_label", "department_room", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "floor_guide": [
        ("floor_directory", "hospital_floor", "TASK_RELEVANT_STATIC_TEXT"),
        ("direction_sign", "department_direction", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "staff_desk": [
        ("counter_label", "staff_counter", "HUMAN_ASSISTANCE_REGION"),
        ("staff_assistance_region", "staff_help", "HUMAN_ASSISTANCE_REGION"),
    ],
    "room_doorplate": [
        ("doorplate", "room_number", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "restroom_sign": [
        ("wayfinding_marker", "restroom_icon", "TASK_RELEVANT_STATIC_TEXT"),
        ("icon_text_marker", "restroom_label", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "platform_sign": [
        ("wayfinding_marker", "platform_label", "TASK_RELEVANT_STATIC_TEXT"),
        ("platform_label", "line_platform", "TASK_RELEVANT_STATIC_TEXT"),
    ],
    "line_number_sign": [
        ("short_text_sign", "line_number", "TASK_RELEVANT_STATIC_TEXT"),
        ("line_number_marker", "transit_line", "SAFETY_RELEVANT_SHORT_TEXT"),
    ],
    "line_number": [
        ("short_text_sign", "line_number", "TASK_RELEVANT_STATIC_TEXT"),
        ("line_number_marker", "transit_line", "SAFETY_RELEVANT_SHORT_TEXT"),
    ],
    "electronic_screen": [
        ("screen_text_region", "departure_board", "READABLE_CANDIDATE"),
    ],
    "staff_counter": [
        ("counter_label", "transit_counter", "HUMAN_ASSISTANCE_REGION"),
        ("staff_assistance_region", "staff_help", "HUMAN_ASSISTANCE_REGION"),
    ],
}

FILTERING_DIMS = [
    "task_relevance", "safety_relevance", "expected_text_length", "distance", "angle",
    "occlusion", "glare_or_reflection", "text_size", "contrast", "stability",
    "privacy_sensitivity", "user_request_specificity",
]

GUIDANCE_ACTIONS = [
    ("center_region", "请将目标文字区域置于画面中央"),
    ("move_closer", "请靠近一些以便看清文字"),
    ("adjust_angle", "请调整手机角度减少反光"),
    ("hold_still", "请保持稳定，便于后续静态采集"),
    ("zoom_or_magnify", "可尝试放大查看小字区域"),
    ("ask_external_assistance", "可询问附近工作人员协助"),
]

FOLLOWUPS = [
    "Hardware-Camera-Control-Contract-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

LONG_TERM_TYPES = [
    "unresolved_readable_region_candidate",
    "repeated_unreadable_region_candidate",
    "expired_readable_region_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

OPTIONAL_PATHS = [
    ("detector_registry", "docs/architecture/vision/LUNA_VISION_DETECTION_EVIDENCE_SCHEMA_V0.md"),
    ("vision_region_proposal", "docs/architecture/vision/LUNA_VISION_FRAME_ROI_PROPOSAL_AND_SEGMENTATION_STUB_V0.md"),
    ("worldmodel_unresolved_slot", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
    ("scene_registry", "docs/architecture/midplatform/LUNA_SCENE_REGISTRY_V0.md"),
    ("map_registry", "docs/architecture/LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md"),
    ("route_context", "docs/architecture/midplatform/LUNA_ROUTE_CONTEXT_V0.md"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_isrc_runtime", "isrc_loaded", [], [], []),
    ("load_rrd_policy", "rrd_policy_loaded", [], [], []),
    ("intake_ranked_source_area_candidates", "seventeen_ranked", [], [], []),
    ("generate_readable_region_candidates", "rr_candidates", [], [], ["real_bbox"]),
    ("classify_region_candidates", "classified", [], [], []),
    ("apply_readability_filtering", "filtering", [], [], []),
    ("generate_user_view_guidance_candidates", "guidance", [], [], ["tts_now"]),
    ("generate_static_capture_handoff_candidates", "capture_handoff", [], [], ["capture_now"]),
    ("generate_ocrrequest_future_gate_candidates", "ocr_gate", [], [], ["ocrrequest_now"]),
    ("generate_human_staff_assistance_region_candidates", "human_assist", [], [], []),
    ("generate_unresolved_expired_candidate_link", "lt_link", [], [], []),
    ("generate_final_rrd_runtime_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _classification_meta(class_name: str) -> Tuple[str, str, str, bool, bool]:
    if class_name == "HUMAN_ASSISTANCE_REGION":
        return (
            "human_assistance_preferred",
            "ask_staff_or_nearby",
            "force_ocr",
            False,
            False,
        )
    if class_name in ("UNREADABLE_BUT_REPAIRABLE",):
        return ("repairable_with_guidance", "apply_view_guidance", "ocr_now", True, False)
    if class_name in ("UNREADABLE_NOT_REPAIRABLE", "NOT_WORTH_READING", "IRRELEVANT_TEXT_REGION"):
        return ("exclude_region", "exclude_or_human", "force_ocr", False, False)
    return ("proceed_to_static_capture_candidate", "static_capture_later", "ocr_after_capture", True, True)


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("isrc_runtime", roots["isrc"], "static_reading_information_source_localization_runtime_dryrun_v1_summary.json", False),
        ("tsc_reeval", roots["reeval"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("rrd_policy", roots["rrd"], "static_readable_region_discovery_guidance_policy_v1_summary.json", False),
        ("isrc_policy", roots["isrc_policy"], "static_reading_information_source_localization_policy_v1_summary.json", False),
        ("tsc_policy", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json", False),
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
    ranked = _read_json(roots["isrc"] / "static_reading_ranked_information_source_area_candidate_collection_v1.json")
    if ranked:
        rows.append(
            {
                "intake_id": "ranked_source_areas",
                "input_source": "isrc_runtime",
                "source_root_or_path": str(roots["isrc"]),
                "artifact": "static_reading_ranked_information_source_area_candidate_collection_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": ["candidates", "ranked_candidate_count"],
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
        "schema_version": "static_readable_region_runtime_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_static_readable_region_discovery_runtime_dryrun_v1(
    *,
    isrc_runtime_root: str,
    tsc_reevaluation_root: str,
    readable_region_policy_root: str,
    information_source_policy_root: str,
    task_scene_policy_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "isrc": Path(isrc_runtime_root).resolve(),
        "reeval": Path(tsc_reevaluation_root).resolve(),
        "rrd": Path(readable_region_policy_root).resolve(),
        "isrc_policy": Path(information_source_policy_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    ranked_data = _read_json(roots["isrc"] / "static_reading_ranked_information_source_area_candidate_collection_v1.json") or {}
    ranked_list = [r for r in (ranked_data.get("candidates") or []) if isinstance(r, dict)]
    ranked_count = len(ranked_list)

    ranked_intake = [
        {
            "ranked_source_area_candidate_id": r.get("ranked_source_area_candidate_id"),
            "parent_query_candidate_id": r.get("parent_query_candidate_id"),
            "normalized_task_type": r.get("normalized_task_type"),
            "normalized_scene_type": r.get("normalized_scene_type"),
            "source_area_type": r.get("source_area_type"),
            "expected_readable_region_types": r.get("expected_readable_region_types"),
            "user_guidance_hint_placeholder": r.get("user_guidance_hint_placeholder"),
            "accepted_for_rrd_dryrun": True,
            "fact_status": "not_fact",
        }
        for r in ranked_list
    ]

    rr_candidates: List[Dict[str, Any]] = []
    classifications: List[Dict[str, Any]] = []
    filtering_rows: List[Dict[str, Any]] = []
    guidance_list: List[Dict[str, Any]] = []
    capture_handoff_items: List[Dict[str, Any]] = []
    ocr_gate_items: List[Dict[str, Any]] = []

    rr_id = 0
    g_id = 0
    for r in ranked_list:
        rsa_id = r.get("ranked_source_area_candidate_id", "")
        sat = r.get("source_area_type", "")
        task = r.get("normalized_task_type", "")
        scene = r.get("normalized_scene_type", "")
        expansions = REGION_EXPANSION.get(sat)
        if not expansions:
            kinds = r.get("expected_readable_region_types") or ["signboard"]
            expansions = [(k, "generic_text", "READABLE_CANDIDATE") for k in kinds]
        is_staff = sat in STAFF_SOURCE_AREAS
        for region_kind, text_type, class_name in expansions:
            rr_id += 1
            rr_cid = f"rrc_{rr_id:03d}"
            ocr_later = class_name != "HUMAN_ASSISTANCE_REGION"
            det_later = class_name not in ("HUMAN_ASSISTANCE_REGION",) and region_kind != "staff_assistance_region"
            rr_candidates.append(
                {
                    "readable_region_candidate_id": rr_cid,
                    "parent_ranked_source_area_candidate_id": rsa_id,
                    "source_area_type": sat,
                    "expected_region_kind": region_kind,
                    "expected_text_type": text_type,
                    "expected_task_relevance": "high" if task else "medium",
                    "approximate_location_hint": f"{sat}_within_{scene}",
                    "visual_semantic_clues": f"{region_kind}_{text_type}_for_{task}",
                    "bbox_candidate_unknown_by_default": True,
                    "detector_required_later": det_later,
                    "ocr_required_later": ocr_later,
                    "readability_status_unknown_by_default": True,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )
            reason, allowed, blocked, ocr_later_flag, cap_later = _classification_meta(class_name)
            classifications.append(
                {
                    "readable_region_candidate_id": rr_cid,
                    "class_name": class_name,
                    "classification_reason": reason,
                    "allowed_next_action": allowed,
                    "blocked_action": blocked,
                    "ocr_allowed_later": ocr_later_flag,
                    "static_capture_allowed_later": cap_later,
                    "fact_status": "not_fact",
                }
            )
            filtering_rows.append(
                {
                    "readable_region_candidate_id": rr_cid,
                    "filtering_dimension_results": {d: "unknown_placeholder" for d in FILTERING_DIMS},
                    "pass_status_placeholder": "unknown",
                    "repair_action_candidates": ["adjust_angle", "move_closer"] if class_name == "UNREADABLE_BUT_REPAIRABLE" else [],
                    "exclude_now": class_name in ("NOT_WORTH_READING", "IRRELEVANT_TEXT_REGION"),
                    "can_retry_with_guidance": class_name in ("UNREADABLE_BUT_REPAIRABLE", "READABLE_CANDIDATE"),
                    "can_feed_unresolved_candidate": True,
                    "real_quality_measured": False,
                    "fact_status": "not_fact",
                }
            )
            if class_name != "NOT_WORTH_READING":
                for action, prompt in GUIDANCE_ACTIONS[:3 if is_staff else 4]:
                    g_id += 1
                    guidance_list.append(
                        {
                            "guidance_candidate_id": f"ugc_{g_id:03d}",
                            "parent_readable_region_candidate_id": rr_cid,
                            "guidance_action": action,
                            "prompt_candidate": prompt,
                            "expected_region_improvement": f"improve_{action}",
                            "priority": "P3_OCR_GUIDANCE",
                            "safety_constraint": "no_unsafe_approach",
                            "tts_invoked_now": False,
                            "speech_request_submitted_now": False,
                            "runtime_action_committed_now": False,
                            "fact_status": "not_fact",
                        }
                    )
            if cap_later and class_name not in ("HUMAN_ASSISTANCE_REGION", "NOT_WORTH_READING"):
                capture_handoff_items.append(
                    {
                        "readable_region_candidate_id": rr_cid,
                        "parent_source_area_id": rsa_id,
                        "required_readiness_dimensions": [
                            "user_stability",
                            "target_centering",
                            "viewing_angle",
                            "distance_and_scale",
                            "lighting_and_clarity",
                        ],
                        "static_capture_allowed_later": True,
                        "static_capture_invoked_now": False,
                    }
                )
            if ocr_later_flag:
                ocr_gate_items.append(
                    {
                        "readable_region_candidate_id": rr_cid,
                        "ocrrequest_eligible_later": True,
                        "ocrrequest_eligible_now": False,
                        "ocrrequest_generated_now": False,
                        "provider_invoked_now": False,
                    }
                )

    trace_steps = [
        {
            "step_id": sid,
            "step_name": sid,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for sid, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    rr_count = len(rr_candidates)
    human_assist_generated = any(c.get("class_name") == "HUMAN_ASSISTANCE_REGION" for c in classifications)

    return {
        "summary": {
            "schema_version": "static_readable_region_discovery_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "readable_region_discovery_runtime_dryrun_only",
            "based_on_isrc_runtime": roots["isrc"].is_dir(),
            "based_on_rrd_guidance_policy": roots["rrd"].is_dir(),
            "based_on_tsc_reevaluation": roots["reeval"].is_dir(),
            "current_case_loaded": True,
            "ranked_source_area_candidate_count_observed": ranked_count,
            "ranked_source_area_intake_executed": True,
            "readable_region_candidate_generated": rr_count > 0,
            "readable_region_candidate_count_computed": True,
            "classification_matrix_generated": len(classifications) > 0,
            "readability_filtering_executed": len(filtering_rows) > 0,
            "user_view_guidance_candidate_generated": len(guidance_list) > 0,
            "static_capture_handoff_candidate_generated": len(capture_handoff_items) > 0,
            "ocrrequest_future_gate_candidate_generated": len(ocr_gate_items) > 0,
            "static_capture_ready_now": False,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated": False,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "real_bbox_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "ocr_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "information_source_fact_written": False,
            "readable_region_fact_written": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "ranked_intake": {
            "schema_version": "static_readable_region_ranked_source_area_intake_matrix_v1",
            "ranked_source_areas": ranked_intake,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "collection": {
            "schema_version": "static_readable_region_candidate_collection_v1",
            "readable_region_candidate_count": rr_count,
            "candidates": rr_candidates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "classification": {
            "schema_version": "static_readable_region_runtime_classification_matrix_v1",
            "rows": classifications,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "filtering": {
            "schema_version": "static_readable_region_runtime_readability_filtering_matrix_v1",
            "rows": filtering_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "guidance": {
            "schema_version": "static_readable_region_user_view_guidance_candidate_collection_v1",
            "guidance_candidate_count": len(guidance_list),
            "candidates": guidance_list,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capture_handoff": {
            "schema_version": "static_readable_region_static_capture_handoff_candidate_v1",
            "static_capture_handoff_candidate_generated": True,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "candidates": capture_handoff_items,
            "static_capture_ready_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ocr_gate": {
            "schema_version": "static_readable_region_ocrrequest_future_gate_candidate_v1",
            "ocrrequest_future_gate_candidate_generated": True,
            "readable_region_candidate_required": True,
            "static_capture_required": True,
            "stc_freshness_required": True,
            "task_context_valid_required": True,
            "safety_not_blocking_required": True,
            "ocrrequest_eligible_later": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "provider_invoked_now": False,
            "per_candidate_gates": ocr_gate_items,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_assist": {
            "schema_version": "static_readable_region_human_staff_assistance_region_candidate_v1",
            "human_staff_assistance_region_candidate_generated": human_assist_generated,
            "trigger_source_area_types": sorted(STAFF_SOURCE_AREAS),
            "assistance_actions": [
                "ask_staff_where_sign_is",
                "ask_staff_confirm_counter_or_room",
                "ask_nearby_person_point_to_text",
                "ask_nearby_person_read_short_text",
            ],
            "action_committed_now": False,
            "tts_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "unresolved_link": {
            "schema_version": "static_readable_region_runtime_unresolved_expired_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "parent_ranked_source_area",
                "readable_region_candidate_ref",
                "unresolved_or_stale_reason",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "static_readable_region_runtime_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "static_readable_region_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "ranked_source_area_candidate_count_observed": ranked_count,
            "readable_region_candidate_generated": rr_count > 0,
            "static_capture_handoff_candidate_generated": True,
            "ocrrequest_future_gate_candidate_generated": True,
            "static_capture_ready_now": False,
            "ocrrequest_eligible_now": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "recommended_next_phase": "Hardware-Camera-Control-Contract-v1",
            "alternate_next_phase": "Assisted-Static-Reading-GuardedTrial-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "static_readable_region_runtime_boundary_report_v1",
            "rrd_runtime_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "real_bbox_generated": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "information_source_fact_written": False,
            "readable_region_fact_written": False,
            "static_capture_invoked_now": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_readable_region_runtime_metrics_candidate_report_v1",
            "ranked_source_area_candidate_count_observed": ranked_count,
            "readable_region_candidate_count": rr_count,
            "classification_count": len(classifications),
            "guidance_candidate_count": len(guidance_list),
            "static_capture_handoff_candidate_count": len(capture_handoff_items),
            "ocrrequest_future_gate_candidate_count": len(ocr_gate_items),
            "human_staff_assistance_region_candidate_count": 1 if human_assist_generated else 0,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_readable_region_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_readable_region_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_readable_region_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "rrd_runtime_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "real_bbox_generated": False,
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
            "schema_version": "static_readable_region_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_readable_region_runtime_non_claims_report_v1",
            "claims": [
                "no_real_visual_input",
                "readable_region_candidate_not_detected_region",
                "bbox_unknown_not_bbox",
                "readability_filtering_not_real_quality",
                "user_guidance_not_actual_guidance",
                "static_capture_handoff_not_capture",
                "ocrrequest_gate_not_ocrrequest",
                "no_camera_detector_ocr",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "static_readable_region_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "static_readable_region_runtime_audit_report_v1",
            "static_readable_region_discovery_runtime_dryrun_v1_executed": True,
            "rrd_runtime_dryrun_only": True,
            "ranked_source_area_candidate_count_observed": ranked_count,
            "readable_region_candidate_generated": rr_count > 0,
            "static_capture_handoff_candidate_generated": len(capture_handoff_items) > 0,
            "ocrrequest_future_gate_candidate_generated": len(ocr_gate_items) > 0,
            "static_capture_ready_now": False,
            "ocrrequest_eligible_now": False,
            "detector_invoked": False,
            "text_detector_invoked": False,
            "real_bbox_generated": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "information_source_fact_written": False,
            "readable_region_fact_written": False,
            "midplatform_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
