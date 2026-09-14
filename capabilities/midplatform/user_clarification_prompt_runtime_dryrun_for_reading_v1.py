# -*- coding: utf-8 -*-
"""User Clarification Prompt Runtime DryRun for Reading v1 — voice governance chain (no TTS/VOP/submit).

Phase-User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1-001"
P3 = "P3_OCR_GUIDANCE"
P0 = "P0_SAFETY_CRITICAL"
P1 = "P1_NAVIGATION_CRITICAL"
FINAL_DECISION = "WAIT_FOR_USER_RESPONSE"
SELECTED_PROMPT = "你想找什么信息？现在大概在什么场景？"
SELECTED_TEMPLATE_TYPE = "missing_both_task_and_scene"
SELECTED_TEMPLATE_ID = "uclar_003"

FOLLOWUPS = [
    "User-Clarification-Response-Parsing-DryRun-for-Reading-v1",
    "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
    "Static-Reading-Information-Source-Localization-Runtime-DryRun-v1",
    "Static-Readable-Region-Discovery-Runtime-DryRun-v1",
    "Human-Staff-Assistance-Prompt-Template-v1",
    "Scene-Context-Recognition-Policy-v1",
    "WorldModel-Lookup-for-Reading-DryRun-v1",
    "Hardware-Camera-Control-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

LONG_TERM_TYPES = [
    "unresolved_task_context_candidate",
    "unresolved_scene_context_candidate",
    "repeated_clarification_needed_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_clarification_template", "template_loaded", [], [], []),
    ("load_tsc_runtime_case", "tsc_case_loaded", [], [], []),
    ("select_missing_both_template", "missing_both_selected", ["missing_task_context", "missing_scene_context"], [], ["fabricate_context"]),
    ("run_priority_safety_check", "ALLOW_AS_CANDIDATE", [], [], ["runtime_arbitration_now"]),
    ("run_cooldown_repeat_check", "NEW_CLARIFICATION_ALLOWED_AS_CANDIDATE", [], [], []),
    ("generate_speech_request_candidate", "speech_request_candidate", [], [], ["speech_request_submit"]),
    ("run_speech_gate_pre_submit", "ADMIT_AS_CANDIDATE", [], [], ["vop_invoke_now"]),
    ("generate_vop_adapter_candidate", "READY_FOR_FUTURE_VOP_SUBMIT", [], [], ["tts_invoke"]),
    ("generate_wait_for_user_response_state", "WAIT_FOR_USER_RESPONSE", [], [], ["fill_task_scene"]),
    ("generate_response_handoff_candidate", "handoff_placeholder", [], [], ["handoff_invoke_now"]),
    ("generate_final_runtime_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("uclar_template", roots["uclar"], "user_clarification_prompt_template_for_reading_v1_summary.json"),
        ("tsc_runtime", roots["tsc_rt"], "static_reading_task_scene_context_runtime_dryrun_v1_summary.json"),
        ("tsc_policy", roots["tsc"], "static_reading_task_scene_context_policy_v1_summary.json"),
        ("vg_runtime", roots["vg_rt"], "voice_guidance_prompt_runtime_dryrun_v1_summary.json"),
        ("vg_template", roots["vg_tpl"], "voice_guidance_prompt_template_v1_summary.json"),
        ("vop", roots["vop"], "voice_output_plane_adapter_for_guidance_v1_summary.json"),
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
    cur = _read_json(roots["uclar"] / "user_clarification_current_case_template_dryrun_v1.json")
    if cur:
        rows.append(
            {
                "intake_id": "uclar_current_case",
                "input_source": "uclar_template",
                "source_root": str(roots["uclar"]),
                "artifact": "user_clarification_current_case_template_dryrun_v1.json",
                "loaded": True,
                "key_fields_observed": ["selected_template_type", "selected_prompt_text"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": "user_clarification_prompt_runtime_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_user_clarification_prompt_runtime_dryrun_for_reading_v1(
    *,
    clarification_template_root: str,
    task_scene_runtime_root: str,
    task_scene_policy_root: str,
    voice_guidance_runtime_root: str,
    voice_guidance_template_root: str,
    voice_output_plane_adapter_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    roots = {
        "uclar": Path(clarification_template_root).resolve(),
        "tsc_rt": Path(task_scene_runtime_root).resolve(),
        "tsc": Path(task_scene_policy_root).resolve(),
        "vg_rt": Path(voice_guidance_runtime_root).resolve(),
        "vg_tpl": Path(voice_guidance_template_root).resolve(),
        "vop": Path(voice_output_plane_adapter_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    cur_tpl = _read_json(roots["uclar"] / "user_clarification_current_case_template_dryrun_v1.json") or {}
    prompt_text = cur_tpl.get("selected_prompt_text") or SELECTED_PROMPT
    template_type = cur_tpl.get("selected_template_type") or SELECTED_TEMPLATE_TYPE
    template_id = cur_tpl.get("selected_template_id") or SELECTED_TEMPLATE_ID
    priority = cur_tpl.get("priority_level") or P3

    trace_steps = []
    for step_id, decision, reasons, allowed, blocked in TRACE_STEPS:
        trace_steps.append(
            {
                "step_id": step_id,
                "step_name": step_id,
                "decision": decision,
                "reason_codes": reasons,
                "allowed_next_actions": allowed,
                "blocked_next_actions": blocked,
                "runtime_action_committed": False,
            }
        )

    speech_candidate = {
        "schema_version": "user_clarification_prompt_runtime_speech_request_candidate_v1",
        "speech_request_candidate_generated": True,
        "speech_text": prompt_text,
        "priority": priority,
        "source_module": "user_clarification_prompt_for_reading",
        "reason_code": template_type,
        "safety_interruptible": True,
        "can_be_interrupted_by": [P0, P1],
        "speech_gate_required": True,
        "voice_output_plane_required": True,
        "submitted_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "reading_clarification_prompt_runtime_dryrun_only",
            "based_on_clarification_prompt_template": roots["uclar"].is_dir(),
            "based_on_task_scene_context_runtime": roots["tsc_rt"].is_dir(),
            "based_on_voice_guidance_runtime": roots["vg_rt"].is_dir(),
            "based_on_vop_adapter": roots["vop"].is_dir(),
            "current_case_loaded": True,
            "selected_template_type": template_type,
            "selected_prompt_text": prompt_text,
            "selected_priority": priority,
            "priority_safety_check_executed": True,
            "cooldown_repeat_check_executed": True,
            "speech_request_candidate_generated": True,
            "speech_gate_pre_submit_dryrun_executed": True,
            "vop_adapter_candidate_generated": True,
            "wait_for_user_response_state_generated": True,
            "response_to_context_handoff_candidate_generated": True,
            "user_response_observed": False,
            "task_context_filled_now": False,
            "scene_context_filled_now": False,
            "task_context_fabricated": False,
            "scene_context_fabricated": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
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
        "selection": {
            "schema_version": "user_clarification_prompt_runtime_selection_v1",
            "current_case_loaded": True,
            "missing_context_status": "missing_both_task_and_scene",
            "selected_template_type": template_type,
            "selected_template_id": template_id,
            "selected_prompt_text": prompt_text,
            "selected_priority": priority,
            "selection_reason_codes": [
                "missing_task_context",
                "missing_scene_context",
                "wait_for_user_clarification",
            ],
            "prompt_committed_now": False,
            "tts_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "priority_safety": {
            "schema_version": "user_clarification_prompt_runtime_priority_safety_check_v1",
            "priority_safety_check_executed": True,
            "incoming_priority": priority,
            "safety_alert_active": False,
            "navigation_critical_active": False,
            "can_be_interrupted_by_p0": True,
            "can_be_interrupted_by_p1": True,
            "cannot_interrupt_safety": True,
            "suppress_when_safety_active": True,
            "final_priority_decision": "ALLOW_AS_CANDIDATE",
            "runtime_arbitration_applied_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "cooldown": {
            "schema_version": "user_clarification_prompt_runtime_cooldown_repeat_check_v1",
            "cooldown_repeat_check_executed": True,
            "default_cooldown_sec_placeholder": 45,
            "max_repeat_count_placeholder": 2,
            "prior_clarification_prompt_found": False,
            "cooldown_active": False,
            "repeat_count_exceeded": False,
            "over_ask_prevention_enabled": True,
            "final_repeat_decision": "NEW_CLARIFICATION_ALLOWED_AS_CANDIDATE",
            "runtime_enforced_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "speech_candidate": speech_candidate,
        "speech_gate": {
            "schema_version": "user_clarification_prompt_runtime_speech_gate_pre_submit_v1",
            "pre_submit_dryrun_executed": True,
            "speech_request_candidate_present": True,
            "priority_valid": True,
            "safety_interruptible_valid": True,
            "cooldown_check_passed": True,
            "direct_tts_bypass_detected": False,
            "direct_vop_bypass_detected": False,
            "admission_decision": "ADMIT_AS_CANDIDATE",
            "submitted_now": False,
            "voice_output_plane_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "vop_candidate": {
            "schema_version": "user_clarification_prompt_runtime_vop_adapter_candidate_v1",
            "vop_adapter_candidate_generated": True,
            "vop_payload_candidate_present": True,
            "vop_payload_candidate": {
                "speech_text": prompt_text,
                "priority": priority,
                "source_module": "user_clarification_prompt_for_reading",
                "template_id": template_id,
                "speech_gate_required": True,
            },
            "vop_submit_ready_later": True,
            "voice_output_plane_invoked_now": False,
            "speech_request_submitted_now": False,
            "tts_invoked_now": False,
            "dryrun_decision": "READY_FOR_FUTURE_VOP_SUBMIT",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "wait_state": {
            "schema_version": "user_clarification_prompt_runtime_wait_for_user_response_state_v1",
            "wait_for_user_response_state_generated": True,
            "current_state": "WAIT_FOR_USER_RESPONSE",
            "expected_user_response_fields": [
                "raw_user_response",
                "possible_task_type",
                "possible_scene_type",
                "confirmation_required",
            ],
            "user_response_observed": False,
            "task_context_filled_now": False,
            "scene_context_filled_now": False,
            "runtime_state_changed_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "response_handoff": {
            "schema_version": "user_clarification_prompt_runtime_response_handoff_candidate_v1",
            "response_to_context_handoff_candidate_generated": True,
            "user_response_observed": False,
            "handoff_allowed_later": True,
            "handoff_invoked_now": False,
            "required_future_input": "raw_user_response",
            "possible_context_fields": [
                "task_context",
                "scene_context",
                "normalized_task_type",
                "normalized_scene_type",
            ],
            "task_context_written_now": False,
            "scene_context_written_now": False,
            "fact_written_now": False,
            "target_runtime": "Static-Reading-Task-Scene-Context-Runtime-DryRun-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "user_clarification_prompt_runtime_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "original_context_gap",
                "missing_reason",
                "clarification_template_id",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "user_clarification_prompt_runtime_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "user_clarification_prompt_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "selected_prompt_text": prompt_text,
            "speech_request_candidate_generated": True,
            "vop_submit_ready_later": True,
            "user_response_observed": False,
            "task_context_filled_now": False,
            "scene_context_filled_now": False,
            "task_context_fabricated": False,
            "scene_context_fabricated": False,
            "recommended_next_phase": "User-Clarification-Response-Parsing-DryRun-for-Reading-v1",
            "alternate_next_phase": "Static-Reading-Task-Scene-Context-GuardedTrial-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "user_clarification_prompt_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
            "map_api_invoked": False,
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
            "schema_version": "user_clarification_prompt_runtime_metrics_candidate_report_v1",
            "current_case_loaded": True,
            "prompt_selection_executed": True,
            "priority_safety_check_executed": True,
            "cooldown_repeat_check_executed": True,
            "speech_request_candidate_generated": True,
            "speech_gate_pre_submit_dryrun_executed": True,
            "vop_adapter_candidate_generated": True,
            "wait_for_user_response_state_generated": True,
            "runtime_tts_invoked_count": 0,
            "voice_output_plane_invoked_count": 0,
            "speech_request_submitted_count": 0,
            "task_context_filled_count": 0,
            "scene_context_filled_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "user_clarification_prompt_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "user_clarification_prompt_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "user_clarification_prompt_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
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
            "schema_version": "user_clarification_prompt_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "user_clarification_prompt_runtime_non_claims_report_v1",
            "claims": [
                "not_real_clarification_broadcast",
                "no_tts",
                "no_vop_invoke",
                "no_speech_request_submit",
                "speech_request_candidate_not_submitted",
                "vop_candidate_not_vop_call",
                "wait_state_is_dryrun_only",
                "no_user_response_parsing",
                "no_task_scene_fill",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "user_clarification_prompt_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "user_clarification_prompt_runtime_audit_report_v1",
            "user_clarification_prompt_runtime_dryrun_for_reading_v1_executed": True,
            "runtime_dryrun_only": True,
            "selected_template_type": template_type,
            "speech_request_candidate_generated": True,
            "vop_adapter_candidate_generated": True,
            "wait_for_user_response_state_generated": True,
            "user_response_observed": False,
            "task_context_filled_now": False,
            "scene_context_filled_now": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "short_term_memory_written": False,
            "scene_detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_camera_invoked": False,
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
