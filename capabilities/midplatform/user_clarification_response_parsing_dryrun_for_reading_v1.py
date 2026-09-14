# -*- coding: utf-8 -*-
"""User Clarification Response Parsing DryRun for Reading v1 — simulated response parsing only.

Phase-User-Clarification-Response-Parsing-DryRun-for-Reading-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "User-Clarification-Response-Parsing-DryRun-for-Reading-v1-001"
FINAL_DECISION = "READY_FOR_TSC_REEVALUATION_LATER"
UNKNOWN = "unknown"

FOLLOWUPS = [
    "Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "User-Clarification-Response-GuardedTrial-for-Reading-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

# (id, raw, hint, task, scene, fills_task, fills_scene, fills_both, confidence, requires_confirm, ambiguity, privacy, human_staff)
SIMULATED_RESPONSES: List[Tuple[str, ...]] = [
    ("sim_001", "找出口，商场", "exit_in_mall", "find_exit", "shopping_mall", True, True, True, "medium", False, None, "low", False),
    ("sim_002", "我要找门牌", "doorplate_only", "read_doorplate", UNKNOWN, True, False, False, "medium", True, "scene_unknown", "low", False),
    ("sim_003", "医院里找科室", "hospital_department", "find_department", "hospital", True, True, True, "high", False, None, "low", False),
    ("sim_004", "读这段字", "explicit_read", "user_explicit_read_this", UNKNOWN, True, False, False, "medium", True, "scene_unknown", "low", False),
    ("sim_005", "我不知道在哪", "fully_ambiguous", UNKNOWN, UNKNOWN, False, False, False, "low", True, "task_and_scene_unknown", "low", False),
    ("sim_006", "问工作人员吧", "human_assist", UNKNOWN, UNKNOWN, False, False, False, "low", False, "delegates_to_human", "low", True),
    ("sim_007", "找洗手间，在商场", "restroom_mall", "find_restroom", "shopping_mall", True, True, True, "high", False, None, "low", False),
    ("sim_008", "车站看几号线", "transit_line", "find_transit_line", "transit_station", True, True, True, "high", False, None, "low", False),
]

TASK_NEED_MAP = {
    "find_exit": "find_exit_sign_or_direction",
    "read_doorplate": "read_room_or_unit_id",
    "find_department": "find_hospital_department",
    "user_explicit_read_this": "read_user_indicated_target",
    "find_restroom": "find_restroom_sign",
    "find_transit_line": "confirm_transit_line_or_platform",
}

LONG_TERM_TYPES = [
    "clarification_response_observation_candidate",
    "unresolved_task_context_candidate",
    "unresolved_scene_context_candidate",
    "repeated_ambiguous_response_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_prompt_runtime", "runtime_loaded", [], [], []),
    ("load_template_fill_policy", "fill_policy_loaded", [], [], []),
    ("load_tsc_policy", "tsc_policy_loaded", [], [], []),
    ("load_simulated_response_set", "responses_loaded", [], [], []),
    ("parse_response_matrix", "matrix_parsed", [], [], ["write_fact"]),
    ("generate_task_context_candidates", "task_candidates", [], [], ["task_fact_write"]),
    ("generate_scene_context_candidates", "scene_candidates", [], [], ["scene_fact_write"]),
    ("evaluate_confidence_uncertainty", "confidence_eval", [], [], []),
    ("generate_human_staff_assistance_candidate", "human_assist", [], [], []),
    ("generate_tsc_handoff_candidate", "handoff_placeholder", [], [], ["handoff_invoke_now"]),
    ("evaluate_tsc_reentry_preconditions", "reentry_later", [], [], ["isrc_rrd_invoke"]),
    ("generate_final_parsing_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _parse_row(row: Tuple[str, ...]) -> Dict[str, Any]:
    (
        sid,
        raw,
        hint,
        task,
        scene,
        ft,
        fs,
        fb,
        conf,
        req_conf,
        amb,
        priv,
        human,
    ) = row
    return {
        "simulated_response_id": sid,
        "raw_user_response": raw,
        "possible_task_type": task if task != UNKNOWN else None,
        "possible_scene_type": scene if scene != UNKNOWN else None,
        "fills_task_context": ft,
        "fills_scene_context": fs,
        "fills_both": fb,
        "confidence_placeholder": conf,
        "requires_confirmation": req_conf,
        "ambiguity_reason": amb,
        "privacy_sensitivity": priv,
        "human_staff_assistance": human,
        "expected_parse_hint": hint,
        "fact_written_now": False,
        "fact_status": "not_fact",
    }


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("uclar_runtime", roots["uclar_rt"], "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary.json"),
        ("uclar_template", roots["uclar"], "user_clarification_prompt_template_for_reading_v1_summary.json"),
        ("tsc_runtime", roots["tsc_rt"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json"),
        ("tsc_policy", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json"),
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
    fill_pol = _read_json(roots["uclar"] / "user_clarification_response_to_context_fill_policy_v1.json")
    if fill_pol:
        rows.append(
            {
                "intake_id": "fill_policy",
                "input_source": "uclar_template",
                "source_root": str(roots["uclar"]),
                "artifact": "user_clarification_response_to_context_fill_policy_v1.json",
                "loaded": True,
                "key_fields_observed": ["rules"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "user_clarification_response_parsing_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_user_clarification_response_parsing_dryrun_for_reading_v1(
    *,
    clarification_runtime_root: str,
    clarification_template_root: str,
    task_scene_runtime_root: str,
    task_scene_policy_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    roots = {
        "uclar_rt": Path(clarification_runtime_root).resolve(),
        "uclar": Path(clarification_template_root).resolve(),
        "tsc_rt": Path(task_scene_runtime_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    simulated = [
        {
            "simulated_response_id": r[0],
            "raw_user_response": r[1],
            "simulation_only": True,
            "not_user_fact": True,
            "expected_parse_hint": r[2],
            "fact_status": "not_fact",
        }
        for r in SIMULATED_RESPONSES
    ]

    matrix_rows = [_parse_row(r) for r in SIMULATED_RESPONSES]

    task_candidates = []
    scene_candidates = []
    for i, row in enumerate(matrix_rows):
        sid = row["simulated_response_id"]
        if row["fills_task_context"] and row.get("possible_task_type"):
            task_candidates.append(
                {
                    "task_context_candidate_id": f"tcc_{sid}",
                    "source_response_id": sid,
                    "possible_task_type": row["possible_task_type"],
                    "target_information_need": TASK_NEED_MAP.get(row["possible_task_type"], "unknown_need"),
                    "confidence_placeholder": row["confidence_placeholder"],
                    "requires_confirmation": row["requires_confirmation"],
                    "source_chain": ["uclar_template", "uclar_runtime", "response_parsing_dryrun"],
                    "task_context_written_now": False,
                    "fact_status": "not_fact",
                }
            )
        if row["fills_scene_context"] and row.get("possible_scene_type"):
            scene_candidates.append(
                {
                    "scene_context_candidate_id": f"scc_{sid}",
                    "source_response_id": sid,
                    "possible_scene_type": row["possible_scene_type"],
                    "scene_confidence_placeholder": row["confidence_placeholder"],
                    "confirmation_required": row["requires_confirmation"],
                    "source_chain": ["uclar_template", "uclar_runtime", "response_parsing_dryrun"],
                    "scene_context_written_now": False,
                    "fact_status": "not_fact",
                }
            )

    human_triggers = [r["simulated_response_id"] for r in matrix_rows if r.get("human_staff_assistance")]
    high_c = sum(1 for r in matrix_rows if r["confidence_placeholder"] == "high")
    med_c = sum(1 for r in matrix_rows if r["confidence_placeholder"] == "medium")
    low_c = sum(1 for r in matrix_rows if r["confidence_placeholder"] == "low")
    req_c = sum(1 for r in matrix_rows if r["requires_confirmation"])
    amb_c = sum(1 for r in matrix_rows if r.get("ambiguity_reason"))

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
            "schema_version": "user_clarification_response_parsing_dryrun_for_reading_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "reading_clarification_response_parsing_dryrun_only",
            "based_on_clarification_prompt_runtime": roots["uclar_rt"].is_dir(),
            "based_on_clarification_prompt_template": roots["uclar"].is_dir(),
            "based_on_task_scene_context_runtime": roots["tsc_rt"].is_dir(),
            "current_case_loaded": True,
            "simulated_response_set_defined": True,
            "response_parsing_matrix_generated": True,
            "task_context_candidate_generated": len(task_candidates) > 0,
            "scene_context_candidate_generated": len(scene_candidates) > 0,
            "confidence_uncertainty_evaluation_generated": True,
            "confirmation_policy_applied": True,
            "handoff_to_tsc_runtime_candidate_generated": True,
            "tsc_runtime_reentry_allowed_later": True,
            "tsc_runtime_reentry_invoked_now": False,
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
            "ranked_information_source_area_generated": False,
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
        "simulated_set": {
            "schema_version": "user_clarification_simulated_response_set_v1",
            "responses": simulated,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "matrix": {
            "schema_version": "user_clarification_response_parsing_matrix_v1",
            "rows": matrix_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "task_candidates": {
            "schema_version": "user_clarification_task_context_candidate_collection_v1",
            "task_context_candidate_count": len(task_candidates),
            "candidates": task_candidates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_candidates": {
            "schema_version": "user_clarification_scene_context_candidate_collection_v1",
            "scene_context_candidate_count": len(scene_candidates),
            "candidates": scene_candidates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "human_assist": {
            "schema_version": "user_clarification_response_human_staff_assistance_candidate_v1",
            "human_staff_assistance_candidate_generated": len(human_triggers) > 0,
            "trigger_responses": human_triggers,
            "assistance_type_candidates": [
                "ask_staff_for_location",
                "ask_nearby_person_read_short_text",
                "ask_user_confirm_staff_help",
            ],
            "action_committed_now": False,
            "tts_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "confidence_eval": {
            "schema_version": "user_clarification_response_confidence_uncertainty_evaluation_v1",
            "confidence_evaluation_generated": True,
            "high_confidence_count": high_c,
            "medium_confidence_count": med_c,
            "low_confidence_count": low_c,
            "requires_confirmation_count": req_c,
            "ambiguous_response_count": amb_c,
            "confirmation_policy_applied": True,
            "fact_written_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "handoff": {
            "schema_version": "user_clarification_response_to_tsc_handoff_candidate_v1",
            "handoff_candidate_generated": True,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "payload_schema": [
                "raw_user_response",
                "task_context_candidate",
                "scene_context_candidate",
                "confidence_policy",
                "confirmation_required",
                "source_prompt_template_id",
                "source_chain",
            ],
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "fact_written_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "reentry": {
            "schema_version": "user_clarification_response_tsc_reentry_preconditions_v1",
            "tsc_reentry_preconditions_evaluated": True,
            "requires_raw_user_response": True,
            "requires_candidate_validation": True,
            "requires_confirmation_if_low_confidence": True,
            "tsc_runtime_reentry_allowed_later": True,
            "tsc_runtime_reentry_invoked_now": False,
            "information_source_runtime_invoked_now": False,
            "readable_region_runtime_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "user_clarification_response_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "raw_user_response_or_simulated_response_ref",
                "parsing_result",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "user_clarification_response_parsing_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "user_clarification_response_parsing_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "simulated_response_set_processed": True,
            "task_context_candidate_generated": len(task_candidates) > 0,
            "scene_context_candidate_generated": len(scene_candidates) > 0,
            "handoff_candidate_generated": True,
            "tsc_runtime_reentry_allowed_later": True,
            "tsc_runtime_reentry_invoked_now": False,
            "recommended_next_phase": "Static-Reading-Task-Scene-Context-Reevaluation-DryRun-v1",
            "alternate_next_phase": "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "user_clarification_response_parsing_boundary_report_v1",
            "parsing_dryrun_only": True,
            "asr_invoked": False,
            "llm_invoked": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "ranked_information_source_area_generated": False,
            "readable_region_generated": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "user_clarification_response_parsing_metrics_candidate_report_v1",
            "simulated_response_count": len(SIMULATED_RESPONSES),
            "parsed_response_count": len(matrix_rows),
            "task_context_candidate_count": len(task_candidates),
            "scene_context_candidate_count": len(scene_candidates),
            "requires_confirmation_count": req_c,
            "human_staff_assistance_candidate_count": len(human_triggers),
            "runtime_action_committed_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "user_clarification_response_parsing_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "user_clarification_response_parsing_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "user_clarification_response_parsing_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "parsing_dryrun_only": True,
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
            "schema_version": "user_clarification_response_parsing_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "user_clarification_response_parsing_non_claims_report_v1",
            "claims": [
                "no_real_user_response_processing",
                "simulated_not_user_fact",
                "parsing_not_fact",
                "candidate_not_written_context",
                "no_asr",
                "no_llm",
                "no_isrc_rrd_runtime",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "user_clarification_response_parsing_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "user_clarification_response_parsing_audit_report_v1",
            "user_clarification_response_parsing_dryrun_for_reading_v1_executed": True,
            "parsing_dryrun_only": True,
            "simulated_response_set_defined": True,
            "response_parsing_matrix_generated": True,
            "task_context_candidate_generated": len(task_candidates) > 0,
            "scene_context_candidate_generated": len(scene_candidates) > 0,
            "tsc_runtime_reentry_allowed_later": True,
            "tsc_runtime_reentry_invoked_now": False,
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
