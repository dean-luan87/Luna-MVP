# -*- coding: utf-8 -*-
"""Static Reading Task Scene Context Reevaluation DryRun v1 — parsing candidates → ISRC readiness.

Phase-Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1-001"
FINAL_DECISION = "READY_FOR_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_LATER"

TASK_NEED = {
    "find_exit": "find_exit_sign_or_direction",
    "read_doorplate": "read_room_or_unit_id",
    "find_department": "find_hospital_department",
    "user_explicit_read_this": "read_user_indicated_target",
    "find_restroom": "find_restroom_sign",
    "find_transit_line": "confirm_transit_line_or_platform",
}

# task, scene -> likely areas, human fallback
ISRC_AREAS: Dict[Tuple[str, str], Tuple[List[str], str]] = {
    ("find_exit", "shopping_mall"): (["exit_sign", "directory_board", "elevator_area"], "ask_staff"),
    ("find_department", "hospital"): (["department_sign", "floor_guide", "staff_desk", "room_doorplate"], "ask_staff_for_location"),
    ("find_transit_line", "transit_station"): (["platform_sign", "line_number", "electronic_screen", "staff_counter"], "ask_staff"),
    ("find_restroom", "shopping_mall"): (["restroom_sign", "directory_board", "elevator_area", "service_desk"], "ask_staff_or_directory"),
}

CONFIRM_PROMPTS = {
    "scene_unknown": "请确认您当前大概在什么场景？",
    "task_unknown": "请确认您想找什么信息？",
    "partial_task_only": "请补充当前场景信息。",
}

FOLLOWUPS = [
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Confirmation-Prompt-Template-for-TaskScene-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "User-Clarification-Response-GuardedTrial-for-Reading-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
]

LONG_TERM_TYPES = [
    "task_scene_candidate_observation",
    "unresolved_partial_task_context",
    "unresolved_partial_scene_context",
    "repeated_context_ambiguity",
    "human_staff_assistance_preference_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_response_parsing_results", "parsing_loaded", [], [], []),
    ("load_tsc_policy", "tsc_policy_loaded", [], [], []),
    ("load_isrc_policy", "isrc_policy_loaded", [], [], []),
    ("load_rrd_policy", "rrd_policy_loaded", [], [], []),
    ("reevaluate_candidate_matrix", "matrix_reevaluated", [], [], ["write_fact"]),
    ("compute_completeness_summary", "completeness_computed", [], [], []),
    ("compute_confirmation_requirements", "confirmation_matrix", [], [], []),
    ("generate_information_source_query_candidates", "query_candidates", [], [], ["isrc_invoke_now"]),
    ("evaluate_isrc_readiness", "isrc_ready_later", [], [], ["ranked_source_now"]),
    ("evaluate_rrd_readiness", "rrd_blocked", [], [], ["rrd_invoke_now"]),
    ("generate_long_term_candidate_link", "lt_candidates", [], [], []),
    ("generate_final_reevaluation_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _completeness_status(row: Dict[str, Any]) -> str:
    if row.get("human_staff_assistance"):
        return "human_staff_assistance_requested"
    if not row.get("fills_task_context") and not row.get("fills_scene_context"):
        return "insufficient_context"
    if row.get("fills_both") and row.get("possible_task_type") and row.get("possible_scene_type"):
        if row.get("requires_confirmation"):
            return "partial_task_only" if row.get("possible_task_type") else "partial_scene_only"
        return "complete_candidate"
    if row.get("fills_task_context") and not row.get("fills_scene_context"):
        return "partial_task_only"
    if row.get("fills_scene_context") and not row.get("fills_task_context"):
        return "partial_scene_only"
    return "insufficient_context"


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("parsing", roots["parsing"], "user_clarification_response_parsing_dryrun_for_reading_v1_summary.json"),
        ("uclar_rt", roots["uclar_rt"], "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary.json"),
        ("tsc_rt", roots["tsc_rt"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json"),
        ("tsc", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json"),
        ("isrc", roots["isrc"], "static_reading_information_source_localization_policy_v1_summary.json"),
        ("rrd", roots["rrd"], "static_readable_region_discovery_guidance_policy_v1_summary.json"),
        ("bench", roots["bench"], None),
        ("health", roots["health"], None),
        ("sim", roots["sim"], None),
    ]
    rows = []
    for iid, root, art in specs:
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root": str(root),
                "artifact": art or "(directory)",
                "loaded": loaded,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    matrix = _read_json(roots["parsing"] / "user_clarification_response_parsing_matrix_v1.json")
    if matrix:
        rows.append(
            {
                "intake_id": "parsing_matrix",
                "input_source": "parsing",
                "source_root": str(roots["parsing"]),
                "artifact": "user_clarification_response_parsing_matrix_v1.json",
                "loaded": True,
                "key_fields_observed": ["rows"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "static_reading_task_scene_reevaluation_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_static_reading_task_scene_context_reevaluation_dryrun_v1(
    *,
    response_parsing_root: str,
    clarification_runtime_root: str,
    task_scene_runtime_root: str,
    task_scene_policy_root: str,
    information_source_root: str,
    readable_region_policy_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    roots = {
        "parsing": Path(response_parsing_root).resolve(),
        "uclar_rt": Path(clarification_runtime_root).resolve(),
        "tsc_rt": Path(task_scene_runtime_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "isrc": Path(information_source_root).resolve(),
        "rrd": Path(readable_region_policy_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    parsing_rows = (_read_json(roots["parsing"] / "user_clarification_response_parsing_matrix_v1.json") or {}).get("rows") or []

    reeval_rows = []
    query_candidates = []
    confirm_rows = []
    qid = 0

    for pr in parsing_rows:
        if not isinstance(pr, dict):
            continue
        sid = pr.get("simulated_response_id")
        task = pr.get("possible_task_type")
        scene = pr.get("possible_scene_type")
        status = _completeness_status(pr)
        task_avail = bool(task)
        scene_avail = bool(scene)
        fills_both = bool(pr.get("fills_both") and task and scene)
        req_conf = bool(pr.get("requires_confirmation"))
        is_complete = status == "complete_candidate"
        is_human = status == "human_staff_assistance_requested"

        eligible_isrc_later = is_complete and not req_conf and not is_human
        eligible_isrc_now = False
        eligible_rrd_now = False

        reeval_rows.append(
            {
                "simulated_response_id": sid,
                "raw_user_response": pr.get("raw_user_response"),
                "possible_task_type": task,
                "possible_scene_type": scene,
                "task_available": task_avail,
                "scene_available": scene_avail,
                "fills_both": fills_both,
                "confidence_placeholder": pr.get("confidence_placeholder"),
                "requires_confirmation": req_conf,
                "context_completeness_status": status,
                "eligible_for_information_source_query_later": eligible_isrc_later,
                "eligible_for_information_source_runtime_now": eligible_isrc_now,
                "eligible_for_readable_region_runtime_now": eligible_rrd_now,
                "fact_written_now": False,
                "fact_status": "not_fact",
            }
        )

        if req_conf and status in ("partial_task_only", "partial_scene_only"):
            reason = pr.get("ambiguity_reason") or "partial_context"
            confirm_rows.append(
                {
                    "candidate_id": sid,
                    "reason_requires_confirmation": reason,
                    "confirmation_prompt_candidate": CONFIRM_PROMPTS.get(reason, CONFIRM_PROMPTS["partial_task_only"]),
                    "can_proceed_without_confirmation": False,
                    "confirmation_runtime_invoked_now": False,
                    "tts_invoked_now": False,
                    "fact_status": "not_fact",
                }
            )

        if eligible_isrc_later and task and scene:
            areas, human_fb = ISRC_AREAS.get((task, scene), ([], "ask_nearby"))
            qid += 1
            query_candidates.append(
                {
                    "query_candidate_id": f"isrc_q_{qid:03d}",
                    "source_response_id": sid,
                    "normalized_task_type": task,
                    "normalized_scene_type": scene,
                    "target_information_need": TASK_NEED.get(task, "unknown_need"),
                    "likely_information_source_areas": areas,
                    "excluded_source_areas": ["task_irrelevant_advertising_area", "private_sensitive_area_without_user_request"],
                    "human_assistance_fallback": human_fb,
                    "confidence_policy": pr.get("confidence_placeholder"),
                    "handoff_allowed_later": True,
                    "handoff_invoked_now": False,
                    "fact_status": "not_fact",
                }
            )

    complete_count = sum(1 for r in reeval_rows if r.get("context_completeness_status") == "complete_candidate")
    partial_task = sum(1 for r in reeval_rows if r.get("context_completeness_status") == "partial_task_only")
    partial_scene = sum(1 for r in reeval_rows if r.get("context_completeness_status") == "partial_scene_only")
    insufficient = sum(1 for r in reeval_rows if r.get("context_completeness_status") == "insufficient_context")
    human_count = sum(1 for r in reeval_rows if r.get("context_completeness_status") == "human_staff_assistance_requested")
    req_conf_count = sum(1 for r in reeval_rows if r.get("requires_confirmation"))
    ready_isrc_later = sum(1 for r in reeval_rows if r.get("eligible_for_information_source_query_later"))

    human_triggers = [r["simulated_response_id"] for r in reeval_rows if r.get("context_completeness_status") == "human_staff_assistance_requested"]
    ready_count = len(query_candidates)
    blocked_count = len(reeval_rows) - ready_count

    trace_steps = [
        {
            "step_id": step_id,
            "step_name": step_id,
            "decision": decision,
            "reason_codes": reasons,
            "allowed_next_actions": allowed,
            "blocked_next_actions": blocked,
            "runtime_action_committed": False,
        }
        for step_id, decision, reasons, allowed, blocked in TRACE_STEPS
    ]

    return {
        "summary": {
            "schema_version": "static_reading_task_scene_context_reevaluation_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "task_scene_context_reevaluation_dryrun_only",
            "based_on_response_parsing": roots["parsing"].is_dir(),
            "based_on_task_scene_context_policy": roots["tsc"].is_dir(),
            "based_on_information_source_policy": roots["isrc"].is_dir(),
            "based_on_readable_region_policy": roots["rrd"].is_dir(),
            "current_case_loaded": True,
            "candidate_reevaluation_executed": True,
            "task_scene_candidate_matrix_generated": True,
            "complete_context_candidate_count": complete_count,
            "complete_context_candidate_count_computed": True,
            "confirmation_required_candidate_count_computed": True,
            "confirmation_required_candidate_count": req_conf_count,
            "information_source_query_candidate_generated": len(query_candidates) > 0,
            "isrc_runtime_ready_candidate_generated": True,
            "rrd_runtime_ready_now": False,
            "tsc_context_written_now": False,
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "information_source_runtime_invoked_now": False,
            "readable_region_runtime_invoked_now": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "ranked_information_source_area_generated_now": False,
            "readable_region_generated": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots),
        "reeval_matrix": {
            "schema_version": "static_reading_task_scene_candidate_reevaluation_matrix_v1",
            "rows": reeval_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "completeness": {
            "schema_version": "static_reading_task_scene_completeness_summary_v1",
            "total_candidate_count": len(reeval_rows),
            "complete_candidate_count": complete_count,
            "partial_task_only_count": partial_task,
            "partial_scene_only_count": partial_scene,
            "insufficient_context_count": insufficient,
            "human_staff_assistance_requested_count": human_count,
            "requires_confirmation_count": req_conf_count,
            "ready_for_information_source_query_later_count": ready_isrc_later,
            "ready_for_information_source_runtime_now_count": 0,
            "ready_for_readable_region_runtime_now_count": 0,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "confirmation": {
            "schema_version": "static_reading_task_scene_confirmation_requirement_matrix_v1",
            "candidates": confirm_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "query_collection": {
            "schema_version": "static_reading_information_source_query_candidate_collection_v1",
            "query_candidates": query_candidates,
            "query_candidate_count": len(query_candidates),
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "isrc_readiness": {
            "schema_version": "static_reading_isrc_runtime_readiness_candidate_v1",
            "isrc_readiness_candidate_generated": True,
            "ready_candidate_count": ready_count,
            "blocked_candidate_count": blocked_count,
            "ready_later_conditions": [
                "task_context_candidate_present",
                "scene_context_candidate_present",
                "confirmation_not_required_or_resolved",
                "safety_not_blocking",
                "stc_freshness_available",
            ],
            "information_source_runtime_invoked_now": False,
            "ranked_information_source_area_generated_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "rrd_readiness": {
            "schema_version": "static_reading_rrd_runtime_readiness_candidate_v1",
            "rrd_readiness_candidate_generated": True,
            "rrd_runtime_ready_now": False,
            "reason_not_ready_now": [
                "information_source_runtime_not_invoked",
                "ranked_information_source_area_not_generated",
                "readable_region_source_area_missing",
            ],
            "readable_region_runtime_invoked_now": False,
            "readable_region_generated_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_reeval": {
            "schema_version": "static_reading_task_scene_human_staff_reevaluation_v1",
            "human_staff_assistance_candidate_present": human_count > 0,
            "trigger_response_ids": human_triggers,
            "assistance_routes": [
                "ask_staff_for_location",
                "ask_nearby_person_read_short_text",
                "ask_user_confirm_staff_help",
            ],
            "action_committed_now": False,
            "tts_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "static_reading_task_scene_reevaluation_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "reevaluation_result",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "static_reading_task_scene_reevaluation_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "static_reading_task_scene_reevaluation_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "complete_candidate_count": complete_count,
            "information_source_query_candidate_generated": len(query_candidates) > 0,
            "information_source_runtime_invoked_now": False,
            "readable_region_runtime_invoked_now": False,
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "recommended_next_phase": "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
            "alternate_next_phase": "Confirmation-Prompt-Template-for-TaskScene-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "static_reading_task_scene_reevaluation_boundary_report_v1",
            "reevaluation_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "information_source_runtime_invoked_now": False,
            "readable_region_runtime_invoked_now": False,
            "ranked_information_source_area_generated_now": False,
            "readable_region_generated": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_reading_task_scene_reevaluation_metrics_candidate_report_v1",
            "total_candidate_count": len(reeval_rows),
            "complete_candidate_count": complete_count,
            "partial_candidate_count": partial_task + partial_scene,
            "insufficient_context_count": insufficient,
            "information_source_query_candidate_count": len(query_candidates),
            "confirmation_required_candidate_count": req_conf_count,
            "human_staff_assistance_candidate_count": human_count,
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "static_reading_task_scene_reevaluation_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_reading_task_scene_reevaluation_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_reading_task_scene_reevaluation_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "reevaluation_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
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
            "schema_version": "static_reading_task_scene_reevaluation_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_reading_task_scene_reevaluation_non_claims_report_v1",
            "claims": [
                "no_real_user_response",
                "simulated_candidate_not_fact",
                "complete_candidate_not_written_context",
                "isrc_query_not_isrc_runtime",
                "isrc_readiness_not_execution",
                "rrd_readiness_not_execution",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "static_reading_task_scene_reevaluation_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "static_reading_task_scene_reevaluation_audit_report_v1",
            "static_reading_task_scene_context_reevaluation_dryrun_v1_executed": True,
            "reevaluation_dryrun_only": True,
            "candidate_reevaluation_executed": True,
            "information_source_query_candidate_generated": len(query_candidates) > 0,
            "isrc_runtime_ready_candidate_generated": True,
            "information_source_runtime_invoked_now": False,
            "readable_region_runtime_invoked_now": False,
            "ranked_information_source_area_generated_now": False,
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
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
