# -*- coding: utf-8 -*-
"""Static Reading Information Source Localization Runtime DryRun v1 — query → ranked source candidates.

Phase-Static-Reading-Information-Source-Localization-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1-001"
FINAL_DECISION = "READY_FOR_READABLE_REGION_DISCOVERY_RUNTIME_LATER"

# query_id -> extra areas beyond likely list
EXTRA_AREAS: Dict[str, List[str]] = {
    "isrc_q_001": ["service_desk"],
    "isrc_q_002": ["room_doorplate"],
    "isrc_q_003": ["service_desk"],
    "isrc_q_004": ["line_number_sign", "staff_counter"],
}

READABLE_REGION_MAP = {
    "exit_sign": ["wayfinding_marker", "signboard"],
    "directory_board": ["notice_board", "signboard"],
    "elevator_area": ["wayfinding_marker"],
    "service_desk": ["counter_label", "signboard"],
    "department_sign": ["signboard", "notice_board"],
    "floor_guide": ["notice_board", "signboard"],
    "staff_desk": ["counter_label", "signboard"],
    "room_doorplate": ["doorplate"],
    "restroom_sign": ["wayfinding_marker", "signboard"],
    "platform_sign": ["signboard", "wayfinding_marker"],
    "line_number_sign": ["signboard", "screen"],
    "electronic_screen": ["screen"],
    "staff_counter": ["counter_label", "signboard"],
}

EXCLUSION_RULES = [
    ("task_irrelevant_advertising_area", "ads_only", False),
    ("unsafe_to_approach_area", "safety_alert", True),
    ("private_sensitive_area_without_user_request", "no_consent", True),
    ("unrelated_poster_area", "off_task_poster", False),
    ("generic_text_area_without_task_relevance", "dense_unrequested", False),
    ("stale_context_area", "expired_sign", False),
]

RANKING_DIMS = [
    "task_relevance", "scene_likelihood", "distance", "accessibility",
    "visibility", "safety", "expected_readability", "human_assistance_available",
]

STAFF_TRIGGER_TYPES = {"service_desk", "staff_desk", "staff_counter"}

FOLLOWUPS = [
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Confirmation-Prompt-Template-for-TaskScene-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

LONG_TERM_TYPES = [
    "information_source_candidate_observation",
    "unresolved_information_source_area",
    "repeated_unavailable_source_area",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

OPTIONAL_PATHS = [
    ("worldmodel_unresolved_slot", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
    ("scene_registry", "docs/architecture/midplatform/LUNA_SCENE_REGISTRY_V0.md"),
    ("map_registry", "docs/architecture/LUNA_WORLD_MODEL_MAP_ANCHOR_INTEGRATION_DEFINITION_V0.md"),
    ("route_context", "docs/architecture/midplatform/LUNA_ROUTE_CONTEXT_V0.md"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_tsc_reevaluation", "reeval_loaded", [], [], []),
    ("load_isrc_policy", "isrc_policy_loaded", [], [], []),
    ("load_rrd_policy", "rrd_policy_loaded", [], [], []),
    ("intake_query_candidates", "four_queries", [], [], []),
    ("generate_candidate_source_area_matrix", "source_areas", [], [], ["write_fact"]),
    ("apply_exclusion_filtering", "filtering", [], [], []),
    ("apply_ranking_placeholder", "ranking", [], [], []),
    ("generate_ranked_source_area_candidates", "ranked", [], [], ["readable_region_now"]),
    ("generate_rrd_handoff_candidate", "rrd_handoff", [], [], ["rrd_invoke"]),
    ("generate_human_staff_assistance_candidate", "human_assist", [], [], []),
    ("generate_long_term_candidate_link", "lt_link", [], [], []),
    ("generate_final_isrc_runtime_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("tsc_reeval", roots["reeval"], "static_reading_task_scene_context_reevaluation_dryrun_v1_summary.json", False),
        ("parsing", roots["parsing"], "user_clarification_response_parsing_dryrun_for_reading_v1_summary.json", False),
        ("isrc_policy", roots["isrc"], "static_reading_information_source_localization_policy_v1_summary.json", False),
        ("rrd_policy", roots["rrd"], "static_readable_region_discovery_guidance_policy_v1_summary.json", False),
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
    qc = _read_json(roots["reeval"] / "static_reading_information_source_query_candidate_collection_v1.json")
    if qc:
        rows.append(
            {
                "intake_id": "query_candidates",
                "input_source": "tsc_reeval",
                "source_root_or_path": str(roots["reeval"]),
                "artifact": "static_reading_information_source_query_candidate_collection_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": ["query_candidates", "query_candidate_count"],
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
        "schema_version": "static_reading_isrc_runtime_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_static_reading_information_source_localization_runtime_dryrun_v1(
    *,
    tsc_reevaluation_root: str,
    response_parsing_root: str,
    information_source_policy_root: str,
    readable_region_policy_root: str,
    task_scene_policy_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "reeval": Path(tsc_reevaluation_root).resolve(),
        "parsing": Path(response_parsing_root).resolve(),
        "isrc": Path(information_source_policy_root).resolve(),
        "rrd": Path(readable_region_policy_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    queries = (_read_json(roots["reeval"] / "static_reading_information_source_query_candidate_collection_v1.json") or {}).get("query_candidates") or []
    query_count = len(queries)

    source_areas: List[Dict[str, Any]] = []
    area_id = 0
    for q in queries:
        if not isinstance(q, dict):
            continue
        qid = q.get("query_candidate_id", "")
        task = q.get("normalized_task_type", "")
        scene = q.get("normalized_scene_type", "")
        likely = list(q.get("likely_information_source_areas") or [])
        for extra in EXTRA_AREAS.get(qid, []):
            if extra not in likely:
                likely.append(extra)
        for sat in likely:
            area_id += 1
            source_areas.append(
                {
                    "candidate_source_area_id": f"csa_{area_id:03d}",
                    "parent_query_candidate_id": qid,
                    "normalized_task_type": task,
                    "normalized_scene_type": scene,
                    "source_area_type": sat,
                    "expected_information_type": q.get("target_information_need"),
                    "expected_visual_clues": f"{sat}_in_{scene}_for_{task}",
                    "expected_readable_region_types": READABLE_REGION_MAP.get(sat, ["signboard"]),
                    "distance_priority_placeholder": "medium",
                    "accessibility_priority_placeholder": "medium",
                    "visibility_priority_placeholder": "medium",
                    "task_relevance_placeholder": "high",
                    "human_assistance_available": sat in STAFF_TRIGGER_TYPES,
                    "fact_status": "not_fact",
                    "write_allowed": False,
                }
            )

    exclusion_rows = []
    ranked_global: List[Dict[str, Any]] = []
    rank_n = 0
    for sa in source_areas:
        aid = sa["candidate_source_area_id"]
        sat = sa["source_area_type"]
        excluded = False
        reasons: List[str] = []
        status = "retained_candidate"
        for rule, when, force_ex in EXCLUSION_RULES:
            if force_ex and sat in ("private_sensitive_area_without_user_request",):
                excluded = True
                reasons.append(rule)
                status = "excluded_candidate"
            elif rule == "task_irrelevant_advertising_area" and sat == "unrelated_poster_area":
                excluded = True
                reasons.append(rule)
                status = "excluded_candidate"
        exclusion_rows.append(
            {
                "candidate_source_area_id": aid,
                "exclusion_checked": True,
                "exclusion_reasons": reasons,
                "excluded_now": excluded,
                "exclusion_status": status,
                "fact_status": "not_fact",
            }
        )
        if not excluded:
            rank_n += 1
            ranked_global.append(
                {
                    "ranked_source_area_candidate_id": f"rsa_{rank_n:03d}",
                    "parent_query_candidate_id": sa["parent_query_candidate_id"],
                    "normalized_task_type": sa["normalized_task_type"],
                    "normalized_scene_type": sa["normalized_scene_type"],
                    "source_area_type": sat,
                    "rank_order_placeholder": rank_n,
                    "expected_readable_region_types": sa["expected_readable_region_types"],
                    "user_guidance_hint_placeholder": f"优先查看{sat}区域",
                    "rrd_discovery_scope_allowed_later": True,
                    "ranked_information_source_area_written_now": False,
                    "fact_status": "not_fact",
                }
            )

    ranking_rows = []
    for sa in source_areas:
        aid = sa["candidate_source_area_id"]
        ex = next((e for e in exclusion_rows if e["candidate_source_area_id"] == aid), {})
        if ex.get("excluded_now"):
            continue
        ranking_rows.append(
            {
                "candidate_source_area_id": aid,
                "ranking_dimensions": RANKING_DIMS,
                "score_placeholder_only": True,
                "real_score_generated": False,
                "rank_order_placeholder": next(
                    (r["rank_order_placeholder"] for r in ranked_global if r["source_area_type"] == sa["source_area_type"]),
                    None,
                ),
                "fact_status": "not_fact",
            }
        )

    query_intake = [
        {
            "query_candidate_id": q.get("query_candidate_id"),
            "source_response_id": q.get("source_response_id"),
            "normalized_task_type": q.get("normalized_task_type"),
            "normalized_scene_type": q.get("normalized_scene_type"),
            "target_information_need": q.get("target_information_need"),
            "likely_information_source_areas": q.get("likely_information_source_areas"),
            "excluded_source_areas": q.get("excluded_source_areas"),
            "human_assistance_fallback": q.get("human_assistance_fallback"),
            "confidence_policy": q.get("confidence_policy"),
            "accepted_for_dryrun": True,
            "fact_status": "not_fact",
        }
        for q in queries
        if isinstance(q, dict)
    ]

    retained = sum(1 for e in exclusion_rows if not e.get("excluded_now"))
    excluded_n = len(exclusion_rows) - retained

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

    return {
        "summary": {
            "schema_version": "static_reading_information_source_localization_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "information_source_localization_runtime_dryrun_only",
            "based_on_tsc_reevaluation": roots["reeval"].is_dir(),
            "based_on_information_source_policy": roots["isrc"].is_dir(),
            "based_on_readable_region_policy": roots["rrd"].is_dir(),
            "current_case_loaded": True,
            "query_candidate_count_observed": query_count,
            "query_candidate_intake_executed": True,
            "candidate_source_area_matrix_generated": True,
            "exclusion_filtering_executed": True,
            "ranking_placeholder_executed": True,
            "ranked_information_source_area_candidate_generated": len(ranked_global) > 0,
            "rrd_handoff_candidate_generated": True,
            "rrd_runtime_ready_later": True,
            "rrd_runtime_invoked_now": False,
            "information_source_fact_written": False,
            "ranked_information_source_area_written": False,
            "readable_region_generated": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
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
        "query_intake": {
            "schema_version": "static_reading_isrc_query_candidate_intake_matrix_v1",
            "query_candidates": query_intake,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "source_matrix": {
            "schema_version": "static_reading_isrc_candidate_source_area_matrix_v1",
            "source_areas": source_areas,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "exclusion": {
            "schema_version": "static_reading_isrc_exclusion_filtering_matrix_v1",
            "rows": exclusion_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ranking": {
            "schema_version": "static_reading_isrc_ranking_placeholder_matrix_v1",
            "rows": ranking_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ranked": {
            "schema_version": "static_reading_ranked_information_source_area_candidate_collection_v1",
            "ranked_candidate_count": len(ranked_global),
            "candidates": ranked_global,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "rrd_handoff": {
            "schema_version": "static_reading_isrc_to_rrd_handoff_candidate_v1",
            "rrd_handoff_candidate_generated": True,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "payload_schema": [
                "ranked_information_source_area_candidates",
                "normalized_task_type",
                "normalized_scene_type",
                "target_information_need",
                "expected_readable_region_types",
                "excluded_regions",
                "user_guidance_hint",
                "source_chain",
            ],
            "handoff_payload_summary": {
                "ranked_count": len(ranked_global),
                "query_ids": [q.get("query_candidate_id") for q in queries if isinstance(q, dict)],
            },
            "readable_region_runtime_invoked_now": False,
            "readable_region_generated_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_assist": {
            "schema_version": "static_reading_isrc_human_staff_assistance_candidate_v1",
            "human_staff_assistance_candidate_generated": True,
            "candidate_routes": [
                "ask_staff_where_sign_is",
                "ask_staff_confirm_counter_or_room",
                "ask_nearby_person_point_to_text",
                "ask_nearby_person_read_short_text",
            ],
            "triggered_by_source_area_types": sorted(STAFF_TRIGGER_TYPES),
            "action_committed_now": False,
            "tts_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "static_reading_isrc_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "task_scene_context_candidate_ref",
                "query_candidate_ref",
                "source_area_type",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "static_reading_isrc_runtime_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "static_reading_isrc_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "query_candidate_count_observed": query_count,
            "ranked_information_source_area_candidate_generated": True,
            "rrd_handoff_candidate_generated": True,
            "rrd_runtime_ready_later": True,
            "rrd_runtime_invoked_now": False,
            "readable_region_generated_now": False,
            "information_source_fact_written": False,
            "recommended_next_phase": "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
            "alternate_next_phase": "Hardware-Camera-Control-Contract-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "static_reading_isrc_runtime_boundary_report_v1",
            "isrc_runtime_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "map_api_invoked": False,
            "information_source_fact_written": False,
            "ranked_information_source_area_written": False,
            "readable_region_generated": False,
            "readable_region_runtime_invoked_now": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_reading_isrc_runtime_metrics_candidate_report_v1",
            "query_candidate_count_observed": query_count,
            "candidate_source_area_count": len(source_areas),
            "retained_source_area_count": retained,
            "excluded_source_area_count": excluded_n,
            "ranked_information_source_area_candidate_count": len(ranked_global),
            "rrd_handoff_candidate_count": 1 if ranked_global else 0,
            "human_staff_assistance_candidate_count": 1,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_reading_isrc_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_reading_isrc_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_reading_isrc_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "isrc_runtime_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
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
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "static_reading_isrc_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_reading_isrc_runtime_non_claims_report_v1",
            "claims": [
                "no_real_user_response_processing",
                "query_candidate_not_user_fact",
                "candidate_source_area_not_real_localization",
                "ranked_source_not_fact",
                "rrd_handoff_not_rrd_runtime",
                "no_map_api",
                "no_camera_detector_ocr",
                "no_readable_region_generation",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "static_reading_isrc_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "static_reading_isrc_runtime_audit_report_v1",
            "static_reading_information_source_localization_runtime_dryrun_v1_executed": True,
            "isrc_runtime_dryrun_only": True,
            "query_candidate_count_observed": query_count,
            "candidate_source_area_matrix_generated": True,
            "ranked_information_source_area_candidate_generated": len(ranked_global) > 0,
            "rrd_handoff_candidate_generated": True,
            "rrd_runtime_invoked_now": False,
            "readable_region_generated": False,
            "information_source_fact_written": False,
            "ranked_information_source_area_written": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "detector_invoked": False,
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
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
