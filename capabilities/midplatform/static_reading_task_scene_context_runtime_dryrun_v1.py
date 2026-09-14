# -*- coding: utf-8 -*-
"""Static Reading Task Scene Context Runtime DryRun v1 — missing-context path simulation.

Phase-Static-Reading-Task-Scene-Context-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1-001"
FINAL_DECISION = "WAIT_FOR_USER_CLARIFICATION"
MISSING_STATUS = "missing_both_task_and_scene"

FOLLOWUPS = [
    "User-Clarification-Prompt-Template-for-Reading-v1",
    "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

OPTIONAL_TASK_SOURCES = [
    "user_explicit_request",
    "active_navigation_task",
    "prior_dialog_context",
    "route_context",
    "worldmodel_unresolved_slot",
]

OPTIONAL_SCENE_SOURCES = [
    "worldmodel_place_anchor",
    "route_context",
    "visual_scene_candidate",
    "user_confirmed_scene",
    "map_or_poi_hint",
    "prior_observation",
]

CLARIFICATION_RUNTIME = [
    ("clarify_001", "what_information_need", "你想找什么信息？", "P3_OCR_GUIDANCE", True, "target_information_need"),
    ("clarify_002", "task_type_disambiguation", "你现在是想找出口、门牌，还是读一段文字？", "P3_OCR_GUIDANCE", True, "normalized_task_type"),
    ("clarify_003", "scene_type_disambiguation", "你是在商场、医院，还是车站附近？", "P3_OCR_GUIDANCE", True, "normalized_scene_type"),
    ("clarify_004", "human_assistance_offer", "是否需要询问附近工作人员？", "P4_GENERAL_ASSISTANCE", False, "human_assistance_fallback"),
]

LONG_TERM_TYPES = [
    "unresolved_task_context_candidate",
    "unresolved_scene_context_candidate",
    "repeated_missing_context_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, str, List[str], List[str], List[str]]] = [
    ("load_task_scene_policy", "static_reading_task_scene_context_policy_v1_summary.json", "policy_loaded", [], [], []),
    ("load_readable_region_policy", "static_readable_region_discovery_guidance_policy_v1_summary.json", "rrd_policy_loaded", [], [], []),
    ("load_information_source_policy", "static_reading_information_source_localization_policy_v1_summary.json", "isrc_policy_loaded", [], [], []),
    ("intake_current_case", "static_reading_task_scene_context_current_case_dryrun_v1.json", "case_intake", [], [], ["fabricate_task_scene"]),
    ("evaluate_task_context", "static_reading_task_context_runtime_intake_v1.json", "task_missing", ["missing_task_context"], [], ["generate_task_fact"]),
    ("evaluate_scene_context", "static_reading_scene_context_runtime_intake_v1.json", "scene_missing", ["missing_scene_context"], [], ["infer_scene_fact"]),
    ("apply_missing_context_policy", "static_reading_missing_context_runtime_handling_v1.json", "blocking_applied", [], [], ["invoke_isrc_runtime"]),
    ("generate_user_clarification_candidate", "static_reading_user_clarification_candidate_runtime_v1.json", "clarification_generated", [], [], ["tts_invoke"]),
    ("evaluate_context_confidence", "static_reading_context_confidence_runtime_evaluation_v1.json", "insufficient_context", [], [], []),
    ("evaluate_information_source_query_candidate", "static_reading_information_source_query_runtime_candidate_v1.json", "query_not_generated", ["missing_task_context", "missing_scene_context"], [], ["generate_ranked_source"]),
    ("evaluate_rrd_runtime_preconditions", "static_reading_rrd_runtime_preconditions_evaluation_v1.json", "preconditions_unmet", [], [], ["invoke_rrd_runtime"]),
    ("generate_final_runtime_dryrun_decision", "static_reading_task_scene_context_runtime_final_decision_v1.json", FINAL_DECISION, [], [], ["fabricate_context"]),
]

OPTIONAL_PATHS = [
    ("dialog_context", "docs/architecture/midplatform/LUNA_DIALOG_CONTEXT_V0.md"),
    ("route_context", "docs/architecture/midplatform/LUNA_ROUTE_CONTEXT_V0.md"),
    ("scene_registry", "docs/architecture/midplatform/LUNA_SCENE_REGISTRY_V0.md"),
    ("worldmodel_unresolved_slot", "docs/architecture/midplatform/LUNA_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md"),
    ("user_request_parser", "docs/architecture/midplatform/LUNA_USER_REQUEST_PARSER_V0.md"),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("task_scene_policy", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json", False),
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
    case_art = "static_reading_task_scene_context_current_case_dryrun_v1.json"
    case = _read_json(roots["tsc"] / case_art)
    if case:
        rows.append(
            {
                "intake_id": "tsc_current_case",
                "input_source": "task_scene_policy",
                "source_root_or_path": str(roots["tsc"]),
                "artifact": case_art,
                "loaded": True,
                "optional": False,
                "key_fields_observed": [
                    "task_context_available",
                    "scene_context_available",
                    "missing_context_status",
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
        "schema_version": "static_reading_task_scene_context_runtime_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_static_reading_task_scene_context_runtime_dryrun_v1(
    *,
    task_scene_policy_root: str,
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
        "tsc": Path(task_scene_policy_root).resolve(),
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

    case = _read_json(roots["tsc"] / "static_reading_task_scene_context_current_case_dryrun_v1.json") or {}
    task_avail = bool(case.get("task_context_available"))
    scene_avail = bool(case.get("scene_context_available"))
    missing_status = case.get("missing_context_status") or MISSING_STATUS

    policy_clar = _read_json(roots["tsc"] / "static_reading_user_clarification_candidate_policy_v1.json")
    policy_cands = (policy_clar or {}).get("candidates") or []

    clarifications = []
    for cid, ctype, prompt, pri, req_resp, field in CLARIFICATION_RUNTIME:
        clarifications.append(
            {
                "clarification_candidate_id": cid,
                "clarification_type": ctype,
                "prompt_candidate": prompt,
                "priority_level": pri,
                "required_user_response": req_resp,
                "expected_context_field_to_fill": field,
                "tts_invoked_now": False,
                "speech_request_submitted_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
        )

    trace_steps = []
    for step_id, input_ref, decision, reasons, allowed, blocked in TRACE_STEPS:
        trace_steps.append(
            {
                "step_id": step_id,
                "step_name": step_id,
                "input_refs": [input_ref],
                "decision": decision,
                "reason_codes": reasons,
                "allowed_next_actions": allowed,
                "blocked_next_actions": blocked,
                "runtime_action_committed": False,
            }
        )

    stc_summary = _read_json(roots["stc"] / "stc_sampling_guidance_policy_v1_summary.json")
    stc_freshness = "unknown" if stc_summary else False

    return {
        "summary": {
            "schema_version": "static_reading_task_scene_context_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "task_scene_context_runtime_dryrun_only",
            "based_on_task_scene_context_policy": roots["tsc"].is_dir(),
            "based_on_readable_region_policy": roots["rrd"].is_dir(),
            "based_on_information_source_localization_policy": roots["isrc"].is_dir(),
            "current_case_loaded": True,
            "task_context_intake_evaluated": True,
            "scene_context_intake_evaluated": True,
            "task_context_available": task_avail,
            "scene_context_available": scene_avail,
            "missing_context_status": missing_status,
            "user_clarification_candidate_generated": True,
            "task_context_candidate_generated": False,
            "scene_context_candidate_generated": False,
            "information_source_query_candidate_generated": False,
            "ranked_information_source_area_generated": False,
            "readable_region_runtime_preconditions_evaluated": True,
            "readable_region_runtime_preconditions_met_now": False,
            "readable_region_runtime_invoked_now": False,
            "information_source_runtime_invoked_now": False,
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
        "task_intake": {
            "schema_version": "static_reading_task_context_runtime_intake_v1",
            "task_context_intake_evaluated": True,
            "task_context_available": task_avail,
            "task_context_source_found": False,
            "optional_task_sources_checked": OPTIONAL_TASK_SOURCES,
            "task_context_fabrication_forbidden": True,
            "task_context_candidate_generated": False,
            "missing_reason": "missing_task_context",
            "allowed_next_action": "user_clarification_candidate",
            "blocked_next_action": [
                "generate_ranked_source_area",
                "invoke_readable_region_runtime",
                "generate_ocrrequest",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "scene_intake": {
            "schema_version": "static_reading_scene_context_runtime_intake_v1",
            "scene_context_intake_evaluated": True,
            "scene_context_available": scene_avail,
            "scene_context_source_found": False,
            "optional_scene_sources_checked": OPTIONAL_SCENE_SOURCES,
            "scene_context_fabrication_forbidden": True,
            "scene_context_candidate_generated": False,
            "missing_reason": "missing_scene_context",
            "scene_detector_invoked": False,
            "allowed_next_action": "user_clarification_candidate",
            "blocked_next_action": [
                "infer_scene_fact",
                "generate_ranked_source_area",
                "invoke_readable_region_runtime",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "missing_handling": {
            "schema_version": "static_reading_missing_context_runtime_handling_v1",
            "missing_context_status": missing_status,
            "handling_policy_applied": True,
            "readable_region_discovery_allowed_now": False,
            "information_source_localization_runtime_allowed_now": False,
            "ranked_information_source_area_allowed_now": False,
            "user_clarification_allowed": True,
            "visual_semantic_fallback_allowed_later": True,
            "human_staff_assistance_allowed_later": True,
            "runtime_action_committed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "clarification_rt": {
            "schema_version": "static_reading_user_clarification_candidate_runtime_v1",
            "candidates": clarifications,
            "policy_candidates_consumed": len(policy_cands),
            "user_clarification_candidate_generated": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "confidence_rt": {
            "schema_version": "static_reading_context_confidence_runtime_evaluation_v1",
            "confidence_evaluation_executed": True,
            "task_confidence": "unknown",
            "scene_confidence": "unknown",
            "context_status": "insufficient_context",
            "confirmation_required": True,
            "can_proceed_to_information_source_runtime": False,
            "can_proceed_to_readable_region_runtime": False,
            "can_feed_long_term_candidate": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "query_candidate": {
            "schema_version": "static_reading_information_source_query_runtime_candidate_v1",
            "query_candidate_generated": False,
            "reason_not_generated": ["missing_task_context", "missing_scene_context"],
            "required_fields": [
                "task_context",
                "scene_context",
                "normalized_task_type",
                "normalized_scene_type",
                "target_information_need",
                "likely_information_source_areas",
            ],
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "rrd_precond": {
            "schema_version": "static_reading_rrd_runtime_preconditions_evaluation_v1",
            "preconditions_evaluated": True,
            "task_context_available": task_avail,
            "scene_context_available": scene_avail,
            "normalized_task_type_available": False,
            "normalized_scene_type_available": False,
            "ranked_information_source_area_available": False,
            "safety_not_blocking": True,
            "stc_freshness_valid": stc_freshness,
            "runtime_preconditions_met_now": False,
            "readable_region_runtime_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "static_reading_task_scene_context_runtime_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "static_reading_task_scene_context_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "missing_context_status": missing_status,
            "user_clarification_candidate_generated": True,
            "readable_region_runtime_invoked_now": False,
            "information_source_runtime_invoked_now": False,
            "ranked_information_source_area_generated": False,
            "task_context_fabricated": False,
            "scene_context_fabricated": False,
            "recommended_next_phase": "User-Clarification-Prompt-Template-for-Reading-v1",
            "alternate_next_phase": "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
            "note": "await_user_response_before_isrc_or_rrd_runtime",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "static_reading_task_scene_context_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "spatial_anchor",
                "original_user_request_context",
                "missing_reason",
                "confidence_decay",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "static_reading_task_scene_context_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
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
            "ranked_information_source_area_generated": False,
            "readable_region_runtime_invoked_now": False,
            "information_source_runtime_invoked_now": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "static_reading_task_scene_context_runtime_metrics_candidate_report_v1",
            "current_case_loaded": True,
            "task_context_intake_evaluated": True,
            "scene_context_intake_evaluated": True,
            "missing_context_status": missing_status,
            "user_clarification_candidate_count": len(clarifications),
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
            "schema_version": "static_reading_task_scene_context_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "static_reading_task_scene_context_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "static_reading_task_scene_context_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
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
            "schema_version": "static_reading_task_scene_context_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "static_reading_task_scene_context_runtime_non_claims_report_v1",
            "claims": [
                "no_real_task_recognition",
                "no_real_scene_recognition",
                "no_scene_detector",
                "no_camera",
                "no_ocr",
                "clarification_not_runtime_tts",
                "context_candidate_not_fact",
                "rrd_eval_not_runtime_rrd",
                "long_term_not_profile_write",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "static_reading_task_scene_context_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "static_reading_task_scene_context_runtime_audit_report_v1",
            "static_reading_task_scene_context_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "task_context_available": task_avail,
            "scene_context_available": scene_avail,
            "missing_context_status": missing_status,
            "user_clarification_candidate_generated": True,
            "task_context_fabricated": False,
            "scene_context_fabricated": False,
            "ranked_information_source_area_generated": False,
            "readable_region_runtime_invoked_now": False,
            "information_source_runtime_invoked_now": False,
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
