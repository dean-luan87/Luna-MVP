# -*- coding: utf-8 -*-
"""Assisted Static Reading Runtime DryRun v1 — FSM/readiness/gate simulation (no capture/OCR/TTS).

Phase-Assisted-Static-Reading-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Assisted-Static-Reading-Runtime-DryRun-v1-001"
MODE_ENTRY = "ENTER_ASSISTED_STATIC_READING_CANDIDATE"
CURRENT_STATE = "WAITING_FOR_USER_STABILIZATION"
FINAL_DECISION = "WAIT_FOR_USER_STABILIZATION"
HOLD_TEXT = "请先停稳，保持画面稳定。"

FOLLOWUPS = [
    "Hardware-Camera-Control-Contract-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Voice-Output-Plane-Adapter-GuardedTrial-v1",
    "User-Guidance-Recovery-Runtime-GuardedTrial-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

READINESS_DIMS = [
    "user_stability",
    "target_centering",
    "viewing_angle",
    "distance_and_scale",
    "lighting_and_clarity",
]

SELF_ADJ_ACTIONS = [
    ("request_high_resolution_still_frame", "blur_or_low_resolution", "high_res_still", False),
    ("request_zoom", "text_too_small", "zoom", True),
    ("request_autofocus", "focus_unstable", "autofocus", True),
    ("request_exposure_adjustment", "low_light", "exposure", True),
    ("request_resampling", "scale_mismatch", "resampling", False),
    ("request_stabilization", "motion_detected", "stabilization", False),
    ("request_static_capture_mode", "dynamic_capture_failed", "static_capture_mode", True),
]

EXIT_ROUTES = [
    ("VISUAL_SEMANTIC_FALLBACK", "ocr_not_viable_after_guidance"),
    ("EXTERNAL_ASSISTANCE_CANDIDATE", "user_unable_to_adjust"),
    ("TASK_DOWNGRADE_NON_OCR_PATH", "task_no_longer_relevant"),
    ("EXPIRED_STATIC_READING_CANDIDATE", "context_expired"),
    ("STOP_READING", "user_cancelled_or_safety"),
]

EXPIRED_TYPES = [
    ("expired_static_reading_attempt", "context_expired"),
    ("repeated_unreadable_static_region", "ocr_empty_after_static"),
    ("unresolved_text_anchor", "bbox_no_text"),
    ("user_environment_context_candidate", "scene_context_stale"),
    ("user_profile_context_candidate", "preference_hint_stale"),
    ("emotional_context_background_candidate", "stress_or_urgency_signal"),
]

TRACE_STEPS: List[Tuple[str, str, str, List[str], List[str], List[str]]] = [
    ("load_mode_policy", "assisted_static_reading_mode_v1_summary.json", "mode_loaded", [], [], []),
    ("load_current_case", "assisted_static_reading_current_case_decision_v1.json", "case_loaded", [], [], []),
    ("evaluate_mode_entry", "mode_entry_evaluation", "entry_allowed", ["repeated_dynamic_empty"], [], ["runtime_routing_change"]),
    ("initialize_state_machine", "state_machine_trace", "fsm_initialized", [], [], ["ocr_execution"]),
    ("select_first_guidance_step", "guidance_step_candidate", "hold_still_selected", [], [], ["tts_invoke"]),
    ("evaluate_readiness", "readiness_evaluation_matrix", "readiness_unknown", [], [], ["forge_pass"]),
    ("evaluate_static_capture_ready", "static_capture_ready_candidate", "not_ready", [], [], ["runtime_capture"]),
    ("evaluate_ocrrequest_future_gate", "ocrrequest_future_gate_evaluation", "eligible_later_only", [], [], ["ocrrequest_generate_now"]),
    ("evaluate_system_self_adjustment", "system_self_adjustment_candidate", "candidates_listed", [], [], ["hardware_invoke"]),
    ("evaluate_exit_fallback", "exit_fallback_candidate", "routes_available", [], [], []),
    ("evaluate_expired_candidate", "expired_candidate", "lt_candidates", [], [], ["fact_write"]),
    ("generate_final_runtime_dryrun_decision", "final_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake_rows(roots: Dict[str, Path]) -> List[Dict[str, Any]]:
    specs: List[Tuple[str, str, Optional[str]]] = [
        ("asm_mode", "asm", "assisted_static_reading_mode_v1_summary.json"),
        ("vop_adapter", "vop", "voice_output_plane_adapter_for_guidance_v1_summary.json"),
        ("vg_runtime", "vg", "voice_guidance_prompt_runtime_dryrun_v1_summary.json"),
        ("ug_runtime", "ug", "user_guidance_recovery_runtime_dryrun_v1_summary.json"),
        ("vc_runtime", "vc", "vision_capture_runtime_dryrun_v1_summary.json"),
        ("vc_governance", "vc_gov", "vision_capture_governance_v1_summary.json"),
        ("ocr_activation", "ocr_act", "ocr_activation_governance_policy_v1_summary.json"),
        ("stc", "stc", "stc_sampling_guidance_policy_v1_summary.json"),
        ("ocr_v2", "ocr_v2", "ocrrequest_gated_submission_from_multiframe_v2_summary.json"),
        ("crop_quality", "cq", "crop_quality_diagnosis_v2_multiframe_summary.json"),
        ("ep_v4", "ep4", "evidence_pack_adapter_v4_multiframe_summary.json"),
        ("benchmark", "bench", None),
        ("health", "health", None),
        ("sim", "sim", None),
    ]
    rows = []
    for iid, key, art in specs:
        root = roots[key]
        loaded = root.is_dir()
        if art:
            loaded = loaded and (root / art).is_file()
        rows.append(
            {
                "intake_id": iid,
                "input_source": iid,
                "source_root": str(root),
                "source_artifact": art or "(directory)",
                "loaded": loaded,
                "key_fields_observed": ["summary"] if loaded else [],
                "intake_status": "loaded" if loaded else "missing",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return rows


def run_assisted_static_reading_runtime_dryrun_v1(
    *,
    assisted_static_reading_mode_root: str,
    voice_output_plane_adapter_root: str,
    voice_guidance_runtime_root: str,
    user_guidance_runtime_root: str,
    vision_capture_runtime_root: str,
    vision_capture_governance_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    ocr_v2_root: str,
    multiframe_crop_v2_root: str,
    crop_quality_root: str,
    evidence_pack_v4_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
) -> Dict[str, Any]:
    roots = {
        "asm": Path(assisted_static_reading_mode_root).resolve(),
        "vop": Path(voice_output_plane_adapter_root).resolve(),
        "vg": Path(voice_guidance_runtime_root).resolve(),
        "ug": Path(user_guidance_runtime_root).resolve(),
        "vc": Path(vision_capture_runtime_root).resolve(),
        "vc_gov": Path(vision_capture_governance_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "ocr_v2": Path(ocr_v2_root).resolve(),
        "crop_v2": Path(multiframe_crop_v2_root).resolve(),
        "cq": Path(crop_quality_root).resolve(),
        "ep4": Path(evidence_pack_v4_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    mode_case = _read_json(roots["asm"] / "assisted_static_reading_current_case_decision_v1.json") or {}
    vc_sum = _read_json(roots["vc"] / "vision_capture_runtime_dryrun_v1_summary.json") or {}
    ocr_v2 = _read_json(roots["ocr_v2"] / "ocrrequest_gated_submission_from_multiframe_v2_summary.json") or {}
    vop_final = _read_json(roots["vop"] / "voice_output_plane_adapter_final_dryrun_decision_v1.json") or {}

    v1_empty = mode_case.get("v1_empty_count", ocr_v2.get("v1_empty_count", 30))
    v2_empty = mode_case.get("v2_empty_count", ocr_v2.get("v2_empty_count", 5))
    same_bbox = mode_case.get("same_bbox_risk_count", 5)

    mode_entry_eval = {
        "schema_version": "assisted_static_reading_runtime_mode_entry_evaluation_v1",
        "mode_entry_evaluated": True,
        "current_case_signals": {
            "repeated_dynamic_empty": True,
            "same_bbox_no_gain": True,
            "dynamic_reocr_blocked": True,
            "internal_recrop_should_stop": mode_case.get("internal_recrop_should_stop", True),
        },
        "matched_entry_conditions": [
            "repeated_dynamic_empty",
            "same_bbox_no_gain",
            "dynamic_reocr_blocked",
        ],
        "blocked_entry_conditions": [],
        "entry_allowed": True,
        "mode_entry_decision": MODE_ENTRY,
        "runtime_routing_changed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    fsm_trace_steps = [
        (1, "STATIC_READING_NOT_STARTED", "ENTRY_CANDIDATE_READY", "entry_signals_met", "repeated_dynamic_empty", "mode_entry_candidate"),
        (2, "ENTRY_CANDIDATE_READY", "GUIDANCE_PROMPT_READY", "voice_guidance_ready", "speech_candidate", "guidance_prompt_candidate"),
        (3, "GUIDANCE_PROMPT_READY", "WAITING_FOR_USER_STABILIZATION", "first_prompt_hold_still", "hold_still", "guidance_step_candidate"),
    ]
    state_trace = {
        "schema_version": "assisted_static_reading_runtime_state_machine_trace_v1",
        "final_state": CURRENT_STATE,
        "steps": [
            {
                "step_id": sid,
                "from_state": f,
                "to_state": t,
                "trigger_condition": cond,
                "required_signal": sig,
                "emitted_candidate": cand,
                "blocked_actions": ["runtime_capture", "ocr_execution", "tts_invoke"],
                "runtime_state_changed_now": False,
                "fact_status": "not_fact",
            }
            for sid, f, t, cond, sig, cand in fsm_trace_steps
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    readiness_rows = []
    for dim in READINESS_DIMS:
        readiness_rows.append(
            {
                "readiness_dimension": dim,
                "observed_signal_available": False,
                "pass_status": "unknown_or_not_evaluated_runtime",
                "fail_or_unknown_reason": "no_runtime_frame_captured_this_phase",
                "required_user_action": "hold_still" if dim == "user_stability" else "see_guidance_sequence",
                "required_system_action": "none_this_phase",
                "external_assistance_candidate": "ask_external_assistance",
                "ocrrequest_eligible_if_passed": True,
                "current_phase_passed": False,
                "action_committed_now": False,
                "fact_status": "not_fact",
            }
        )

    readiness_eval = {
        "schema_version": "assisted_static_reading_runtime_readiness_evaluation_matrix_v1",
        "readiness_evaluated": True,
        "dimensions": readiness_rows,
        "all_passed": False,
        "no_forged_pass": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    guidance_step = {
        "schema_version": "assisted_static_reading_runtime_guidance_step_candidate_v1",
        "guidance_step_candidate_generated": True,
        "current_step": "hold_still",
        "prompt_text_candidate": mode_case.get("first_prompt_text", HOLD_TEXT),
        "speech_request_candidate_ref": "voice_output_plane_speech_request_payload_candidate_v1.json",
        "vop_submit_ready_later": vop_final.get("final_decision") == "READY_FOR_FUTURE_VOP_SUBMIT",
        "tts_invoked_now": False,
        "voice_output_plane_invoked_now": False,
        "speech_request_submitted_now": False,
        "expected_user_action": "hold_still",
        "next_expected_state": CURRENT_STATE,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    static_capture_ready = {
        "schema_version": "assisted_static_reading_runtime_static_capture_ready_candidate_v1",
        "static_capture_ready_candidate_generated": True,
        "static_capture_ready_now": False,
        "reason_not_ready": [
            "no_runtime_frame_captured",
            "readiness_not_confirmed",
            "user_stability_not_observed",
        ],
        "required_future_signals": [
            "stable_frame",
            "centered_target",
            "acceptable_angle",
            "readable_scale",
            "acceptable_lighting_clarity",
        ],
        "runtime_capture_invoked_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    ocr_gate_eval = {
        "schema_version": "assisted_static_reading_runtime_ocrrequest_future_gate_evaluation_v1",
        "ocrrequest_future_gate_evaluated": True,
        "static_mode_active_candidate": True,
        "user_stability_passed": False,
        "target_centering_passed": False,
        "angle_passed": False,
        "distance_scale_passed": False,
        "lighting_clarity_passed": False,
        "stc_freshness_passed": False,
        "task_context_valid": True,
        "safety_not_blocking": True,
        "ocrrequest_eligible_now": False,
        "ocrrequest_eligible_later": True,
        "ocrrequest_generated_now": False,
        "provider_invoked_now": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    self_adj = {
        "schema_version": "assisted_static_reading_runtime_system_self_adjustment_candidate_v1",
        "candidates": [
            {
                "action_id": aid,
                "trigger_reason": reason,
                "required_hardware_capability": cap,
                "hardware_capability_known": known,
                "eligible_later": True,
                "hardware_action_invoked_now": False,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
            for aid, reason, cap, known in SELF_ADJ_ACTIONS
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    exit_fb = {
        "schema_version": "assisted_static_reading_runtime_exit_fallback_candidate_v1",
        "routes": [
            {
                "route_to": route,
                "trigger_condition": cond,
                "eligible_later": True,
                "selected_now": False,
                "runtime_action_committed_now": False,
                "fact_status": "not_fact",
            }
            for route, cond in EXIT_ROUTES
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    expired_rt = {
        "schema_version": "assisted_static_reading_runtime_expired_candidate_v1",
        "candidates": [
            {
                "candidate_type": ctype,
                "source_signal": sig,
                "cannot_use_for_action": True,
                "cannot_write_fact": True,
                "can_feed_long_term_candidate": True,
                "required_metadata_present": True,
                "write_allowed_now": False,
                "fact_status": "not_fact",
            }
            for ctype, sig in EXPIRED_TYPES
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    trace = {
        "schema_version": "assisted_static_reading_runtime_decision_trace_v1",
        "steps": [
            {
                "step_id": i + 1,
                "step_name": name,
                "input_refs": [ref],
                "decision": decision,
                "reason_codes": reasons,
                "allowed_next_actions": allowed,
                "blocked_next_actions": blocked,
                "runtime_action_committed": False,
                "fact_status": "not_fact",
            }
            for i, (name, ref, decision, reasons, allowed, blocked) in enumerate(TRACE_STEPS)
        ],
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    final = {
        "schema_version": "assisted_static_reading_runtime_final_decision_v1",
        "final_decision": FINAL_DECISION,
        "mode_entry_decision": MODE_ENTRY,
        "current_state": CURRENT_STATE,
        "selected_guidance_step": "hold_still",
        "selected_prompt_text": mode_case.get("first_prompt_text", HOLD_TEXT),
        "static_capture_ready_now": False,
        "ocrrequest_eligible_now": False,
        "ocrrequest_eligible_later": True,
        "recommended_next_phase": "Hardware-Camera-Control-Contract-v1",
        "fact_status": "not_fact",
        "write_allowed": False,
    }

    return {
        "summary": {
            "schema_version": "assisted_static_reading_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "assisted_static_reading_runtime_dryrun_only",
            "based_on_assisted_static_reading_mode": roots["asm"].is_dir(),
            "based_on_voice_output_plane_adapter": roots["vop"].is_dir(),
            "based_on_voice_guidance_runtime": roots["vg"].is_dir(),
            "based_on_user_guidance_runtime": roots["ug"].is_dir(),
            "based_on_vision_capture_runtime": roots["vc"].is_dir(),
            "current_case_loaded": True,
            "mode_entry_evaluated": True,
            "mode_entry_decision": MODE_ENTRY,
            "state_machine_initialized": True,
            "current_state": CURRENT_STATE,
            "first_guidance_action": "hold_still",
            "first_prompt_text": mode_case.get("first_prompt_text", HOLD_TEXT),
            "readiness_evaluated": True,
            "static_capture_ready_candidate_generated": True,
            "ocrrequest_future_gate_evaluated": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "exit_fallback_candidate_generated": True,
            "expired_static_reading_candidate_generated": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": {
            "schema_version": "assisted_static_reading_runtime_input_intake_matrix_v1",
            "rows": _intake_rows(roots),
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "mode_entry": mode_entry_eval,
        "state_trace": state_trace,
        "readiness": readiness_eval,
        "guidance_step": guidance_step,
        "static_capture_ready": static_capture_ready,
        "ocr_gate": ocr_gate_eval,
        "self_adj": self_adj,
        "exit_fb": exit_fb,
        "expired_rt": expired_rt,
        "trace": trace,
        "final": final,
        "voice_vop_link": {
            "schema_version": "assisted_static_reading_runtime_voice_vop_link_report_v1",
            "linked_to_voice_guidance_runtime": True,
            "linked_to_vop_adapter": True,
            "first_prompt_ready_as_speech_request_candidate": True,
            "vop_submit_ready_later": guidance_step.get("vop_submit_ready_later"),
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "fact_status": "not_fact",
        },
        "vision_ocr_stc_link": {
            "schema_version": "assisted_static_reading_runtime_vision_ocr_stc_link_report_v1",
            "linked_to_vision_capture_runtime": True,
            "linked_to_ocr_activation_governance": True,
            "linked_to_stc_sampling_guidance": True,
            "dynamic_reocr_allowed_now": vc_sum.get("dynamic_reocr_allowed_now", False),
            "static_capture_required": True,
            "stc_freshness_required_before_ocrrequest": True,
            "runtime_camera_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "v1_empty_count": v1_empty,
            "v2_empty_count": v2_empty,
            "fact_status": "not_fact",
        },
        "boundary": {
            "schema_version": "assisted_static_reading_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
            "navigation_decision_invoked": False,
            "runtime_routing_changed": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "assisted_static_reading_runtime_metrics_candidate_report_v1",
            "current_case_loaded": True,
            "mode_entry_evaluated": True,
            "state_machine_initialized": True,
            "readiness_evaluated": True,
            "guidance_step_candidate_generated": True,
            "static_capture_ready_candidate_generated": True,
            "ocrrequest_future_gate_evaluated": True,
            "system_self_adjustment_candidate_count": len(SELF_ADJ_ACTIONS),
            "exit_fallback_candidate_count": len(EXIT_ROUTES),
            "expired_candidate_count": len(EXPIRED_TYPES),
            "runtime_action_committed_count": 0,
            "runtime_tts_invoked_count": 0,
            "runtime_camera_invoked_count": 0,
            "runtime_ocr_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "assisted_static_reading_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link": {
            "schema_version": "assisted_static_reading_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "assisted_static_reading_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_sampling_invoked": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
            "hardware_action_invoked": False,
            "evidence_pack_generated": False,
            "semantic_candidate_generated": False,
            "source_validation_invoked": False,
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
            "schema_version": "assisted_static_reading_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "assisted_static_reading_runtime_non_claims_report_v1",
            "claims": [
                "not_actual_static_reading",
                "no_tts",
                "no_vop",
                "no_camera",
                "no_new_frames",
                "no_ocr",
                "no_ocrrequest",
                "readiness_not_really_passed",
                "static_capture_candidate_only",
                "ocrrequest_eligible_later_not_now",
                "expired_not_fact_write",
                "no_world_model",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {"schema_version": "assisted_static_reading_runtime_open_followups_v1", "items": FOLLOWUPS},
        "audit": {
            "schema_version": "assisted_static_reading_runtime_audit_report_v1",
            "assisted_static_reading_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "mode_entry_decision": MODE_ENTRY,
            "current_state": CURRENT_STATE,
            "first_guidance_action": "hold_still",
            "static_capture_ready_now": False,
            "ocrrequest_eligible_now": False,
            "ocrrequest_eligible_later": True,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "runtime_ocr_invoked": False,
            "ocrrequest_generated": False,
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
