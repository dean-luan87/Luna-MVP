# -*- coding: utf-8 -*-
"""Hardware Camera Control Contract v1 — contract-only; no hardware invocation.

Phase-Hardware-Camera-Control-Contract-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Hardware-Camera-Control-Contract-v1-001"
FINAL_DECISION = "READY_FOR_HARDWARE_CAMERA_RUNTIME_DRYRUN_LATER"

REQUEST_TYPES = [
    "STATIC_CAPTURE_REQUEST",
    "ZOOM_REQUEST",
    "AUTOFOCUS_REQUEST",
    "EXPOSURE_ADJUST_REQUEST",
    "STABILIZATION_REQUEST",
    "RESAMPLING_REQUEST",
    "STILL_FRAME_REQUEST",
    "STATIC_READING_MODE_REQUEST",
]

READINESS_DIMS = [
    "user_stability",
    "target_centering",
    "viewing_angle",
    "distance_and_scale",
    "lighting_and_clarity",
]

CONTROL_ACTIONS = [
    ("request_static_capture", "static_capture_handoff_ready", "frame_capture_supported", "stable_frame_for_ocr", "return_to_user_guidance", "FRAME_CAPTURE_FAILED", 2),
    ("request_zoom", "small_text_or_distance", "zoom_supported", "improved_text_scale", "skip_zoom_use_guidance", "ZOOM_UNSUPPORTED", 1),
    ("request_autofocus", "blur_or_misfocus_expected", "autofocus_supported", "sharper_text_edges", "return_to_user_guidance", "AUTOFOCUS_FAILED", 2),
    ("request_exposure_adjustment", "glare_or_underexposure", "exposure_control_supported", "better_contrast", "return_to_user_guidance", "EXPOSURE_CONTROL_FAILED", 1),
    ("request_stabilization", "hand_shake_risk", "stabilization_supported", "reduced_motion_blur", "hold_still_guidance", "FRAME_CAPTURE_FAILED", 1),
    ("request_resampling", "resolution_mismatch", "frame_capture_supported", "ocr_friendly_resolution", "return_to_user_guidance", "FRAME_CAPTURE_FAILED", 1),
    ("request_still_frame", "static_reading_ready", "still_frame_supported", "single_high_quality_frame", "return_to_user_guidance", "FRAME_CAPTURE_FAILED", 2),
    ("request_static_reading_mode", "assisted_static_reading_enter", "camera_available", "mode_aligned_capture", "degraded_mode", "CAMERA_UNAVAILABLE", 0),
]

UNKNOWN_CONDITIONS = [
    ("hardware_profile_missing", "all_hardware_control", "contract_only_continue", "return_to_user_guidance", "request_external_assistance", True),
    ("camera_unavailable", "frame_capture_and_still", "external_assistance_fallback", "return_to_user_guidance", "request_external_assistance", True),
    ("zoom_unsupported", "request_zoom", "skip_zoom_use_guidance", "move_closer", "ask_nearby_person_point_to_text", True),
    ("autofocus_unsupported", "request_autofocus", "manual_focus_guidance", "adjust_angle", "request_external_assistance", True),
    ("exposure_control_unsupported", "request_exposure_adjustment", "lighting_guidance_only", "adjust_angle", "request_external_assistance", False),
    ("stabilization_unsupported", "request_stabilization", "hold_still_guidance", "hold_still", "request_external_assistance", False),
    ("still_frame_unsupported", "request_still_frame", "stream_frame_fallback_candidate", "hold_still", "return_to_user_guidance", True),
    ("capability_stale", "all_hardware_control", "refresh_capability_report_later", "return_to_user_guidance", "safe_freeze", True),
    ("capability_conflict", "conflicting_control", "use_conservative_defaults", "ask_user_manual_confirmation", "safe_freeze", True),
]

FAILBACK_TYPES = [
    ("return_to_user_guidance", "hardware_action_failed_or_timeout", "apply_P3_guidance", "force_ocr_now", True),
    ("request_external_assistance", "camera_unavailable_or_repeated_failure", "ask_staff_or_nearby", "retry_hardware", True),
    ("downgrade_to_visual_semantic_path", "capture_not_possible", "semantic_only_later", "ocrrequest_now", False),
    ("mark_unresolved_capture_candidate", "capture_aborted", "feed_lt_unresolved", "write_fact", True),
    ("mark_expired_capture_candidate", "stc_stale_or_timeout", "feed_lt_expired", "ocrrequest_now", True),
    ("stop_internal_retry", "retry_limit_reached", "user_guidance_only", "auto_retry", False),
    ("ask_user_manual_confirmation", "capability_unknown_or_conflict", "confirm_before_capture", "auto_capture", False),
]

HEALTH_FAILURE_CLASSES = [
    "CAMERA_UNAVAILABLE",
    "CAMERA_TIMEOUT",
    "CAMERA_PERMISSION_DENIED",
    "ZOOM_UNSUPPORTED",
    "AUTOFOCUS_FAILED",
    "EXPOSURE_CONTROL_FAILED",
    "FRAME_CAPTURE_FAILED",
    "DEVICE_OVERHEAT",
    "BATTERY_LOW",
]

HEALTH_RECOVERY = [
    "FALLBACK_USER_GUIDANCE",
    "FALLBACK_EXTERNAL_ASSISTANCE",
    "REDUCE_CAPTURE_ATTEMPT",
    "SAFE_FREEZE",
    "DEGRADED_MODE",
]

FOLLOWUPS = [
    "Hardware-Camera-Control-Runtime-DryRun-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

LONG_TERM_TYPES = [
    "unresolved_static_capture_candidate",
    "repeated_capture_failure_candidate",
    "hardware_capability_observation_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

OPTIONAL_HW_PATHS = [
    ("hardware_profile", "docs/architecture/midplatform/LUNA_HARDWARE_PROFILE_V0.md"),
    ("camera_capability", "docs/architecture/midplatform/LUNA_CAMERA_CAPABILITY_REGISTRY_V0.md"),
    ("device_registry", "docs/architecture/midplatform/LUNA_DEVICE_REGISTRY_V0.md"),
    ("sensor_registry", "docs/architecture/midplatform/LUNA_SENSOR_REGISTRY_V0.md"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_rrd_runtime", "rrd_loaded", [], [], []),
    ("load_static_capture_handoff_candidates", "twenty_six_handoff", [], [], []),
    ("load_vision_capture_governance", "vision_gov_loaded", [], [], []),
    ("load_system_health_governance", "health_loaded", [], [], []),
    ("define_camera_control_request_schema", "request_schema", [], [], []),
    ("define_hardware_capability_report_schema", "capability_schema", [], [], []),
    ("define_control_action_matrix", "action_matrix", [], [], ["invoke_hardware"]),
    ("generate_static_capture_request_candidates", "capture_candidates", [], [], ["capture_now"]),
    ("define_unknown_unsupported_policy", "unknown_policy", [], [], []),
    ("define_failure_fallback_policy", "fallback_policy", [], [], []),
    ("define_guardedtrial_handoff", "guardedtrial", [], [], ["guardedtrial_now"]),
    ("generate_final_contract_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
        ("isrc_runtime", roots["isrc"], "static_reading_information_source_localization_runtime_dryrun_v1_summary.json", False),
        ("assisted_rt", roots["assisted_rt"], "assisted_static_reading_runtime_dryrun_v1_summary.json", False),
        ("assisted_mode", roots["assisted_mode"], "assisted_static_reading_mode_v1_summary.json", False),
        ("vision_gov", roots["vision_gov"], "vision_capture_governance_v1_summary.json", False),
        ("vision_rt", roots["vision_rt"], "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("ocr_activation", roots["ocr_act"], "ocr_activation_governance_policy_v1_summary.json", False),
        ("stc", roots["stc"], "stc_sampling_guidance_policy_v1_summary.json", False),
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
    handoff = _read_json(roots["rrd"] / "static_readable_region_static_capture_handoff_candidate_v1.json")
    if handoff:
        rows.append(
            {
                "intake_id": "static_capture_handoff",
                "input_source": "rrd_runtime",
                "source_root_or_path": str(roots["rrd"]),
                "artifact": "static_readable_region_static_capture_handoff_candidate_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": ["candidates", "static_capture_handoff_candidate_generated"],
                "intake_status": "loaded",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    for oid, rel in OPTIONAL_HW_PATHS:
        p = ws / rel
        rows.append(
            {
                "intake_id": oid,
                "input_source": "optional_hardware",
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
        "schema_version": "hardware_camera_control_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_hardware_camera_control_contract_v1(
    *,
    rrd_runtime_root: str,
    isrc_runtime_root: str,
    assisted_static_reading_runtime_root: str,
    assisted_static_reading_mode_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    ocr_activation_root: str,
    stc_sampling_guidance_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "rrd": Path(rrd_runtime_root).resolve(),
        "isrc": Path(isrc_runtime_root).resolve(),
        "assisted_rt": Path(assisted_static_reading_runtime_root).resolve(),
        "assisted_mode": Path(assisted_static_reading_mode_root).resolve(),
        "vision_gov": Path(vision_capture_governance_root).resolve(),
        "vision_rt": Path(vision_capture_runtime_root).resolve(),
        "ocr_act": Path(ocr_activation_root).resolve(),
        "stc": Path(stc_sampling_guidance_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    handoff_data = _read_json(roots["rrd"] / "static_readable_region_static_capture_handoff_candidate_v1.json") or {}
    handoff_list = [h for h in (handoff_data.get("candidates") or []) if isinstance(h, dict)]
    handoff_count = len(handoff_list)

    request_schema_examples = []
    for i, rt in enumerate(REQUEST_TYPES, 1):
        request_schema_examples.append(
            {
                "request_id": f"ccr_schema_example_{i:03d}",
                "request_type": rt,
                "parent_readable_region_candidate_id": "rrc_001",
                "parent_static_capture_handoff_id": "sch_001",
                "target_readiness_dimensions": READINESS_DIMS,
                "priority": "P2_CAPTURE" if rt == "STATIC_CAPTURE_REQUEST" else "P3_OPTIONAL",
                "safety_interruptible": True,
                "timeout_policy": "contract_placeholder_timeout",
                "retry_policy": "contract_placeholder_retry",
                "hardware_capability_required": _capability_for_request(rt),
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    action_rows = [
        {
            "action_name": name,
            "trigger_condition": trigger,
            "required_capability": cap,
            "expected_input_improvement": improvement,
            "fallback_if_unsupported": fallback,
            "system_health_failure_class": health_cls,
            "retry_limit_placeholder": retry,
            "action_invoked_now": False,
            "fact_status": "not_fact",
        }
        for name, trigger, cap, improvement, fallback, health_cls, retry in CONTROL_ACTIONS
    ]

    capture_candidates = []
    for idx, h in enumerate(handoff_list, 1):
        sch_id = f"sch_{idx:03d}"
        rrc_id = h.get("readable_region_candidate_id", "")
        capture_candidates.append(
            {
                "request_candidate_id": f"scr_{idx:03d}",
                "parent_readable_region_candidate_id": rrc_id,
                "parent_static_capture_handoff_id": sch_id,
                "required_readiness_dimensions": h.get("required_readiness_dimensions") or READINESS_DIMS,
                "requested_actions": [
                    "hold_still",
                    "center_region",
                    "static_capture",
                    "optional_zoom",
                    "optional_autofocus",
                ],
                "hardware_action_invoked_now": False,
                "runtime_camera_invoked_now": False,
                "frame_captured_now": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    unknown_rows = [
        {
            "condition": cond,
            "blocked_action": blocked,
            "allowed_fallback": allowed,
            "user_guidance_fallback": ug,
            "external_assistance_fallback": ext,
            "system_health_report_required": sh_req,
            "runtime_action_committed": False,
            "fact_status": "not_fact",
        }
        for cond, blocked, allowed, ug, ext, sh_req in UNKNOWN_CONDITIONS
    ]

    fallback_rows = [
        {
            "fallback_type": ft,
            "trigger_condition": trig,
            "allowed_next_action": allowed,
            "blocked_next_action": blocked,
            "can_feed_long_term_candidate": lt,
            "fact_status": "not_fact",
        }
        for ft, trig, allowed, blocked, lt in FAILBACK_TYPES
    ]

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

    optional_hw_loaded = any((ws / rel).is_file() for _, rel in OPTIONAL_HW_PATHS)

    return {
        "summary": {
            "schema_version": "hardware_camera_control_contract_v1_summary_v0",
            "phase": PHASE_ID,
            "contract_scope": "hardware_camera_control_contract_only",
            "based_on_rrd_runtime": roots["rrd"].is_dir(),
            "based_on_static_capture_handoff": handoff_count > 0,
            "based_on_vision_capture_governance": roots["vision_gov"].is_dir(),
            "based_on_system_health_center": roots["health"].is_dir(),
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "camera_control_request_schema_defined": True,
            "hardware_capability_report_schema_defined": True,
            "camera_control_action_matrix_defined": True,
            "static_capture_request_candidate_schema_defined": True,
            "hardware_failure_fallback_policy_defined": True,
            "system_health_link_defined": True,
            "guarded_trial_handoff_defined": True,
            "hardware_capability_unknown_allowed": True,
            "optional_hardware_profile_available": optional_hw_loaded,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "zoom_invoked": False,
            "autofocus_invoked": False,
            "exposure_control_invoked": False,
            "stabilization_invoked": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "request_schema": {
            "schema_version": "hardware_camera_control_request_schema_v1",
            "request_types": REQUEST_TYPES,
            "field_definitions": [
                "request_id",
                "request_type",
                "parent_readable_region_candidate_id",
                "parent_static_capture_handoff_id",
                "target_readiness_dimensions",
                "priority",
                "safety_interruptible",
                "timeout_policy",
                "retry_policy",
                "hardware_capability_required",
            ],
            "examples": request_schema_examples,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capability_schema": {
            "schema_version": "hardware_capability_report_schema_v1",
            "hardware_profile_id": "unknown_placeholder",
            "camera_available": "unknown",
            "zoom_supported": "unknown",
            "autofocus_supported": "unknown",
            "exposure_control_supported": "unknown",
            "stabilization_supported": "unknown",
            "frame_capture_supported": "unknown",
            "still_frame_supported": "unknown",
            "depth_or_tof_supported": "unknown",
            "torch_or_light_supported": "unknown",
            "max_zoom_level": None,
            "focus_mode": "unknown",
            "capability_confidence": "unknown",
            "capability_source": "contract_placeholder_not_device_probe",
            "stale_policy": "refresh_before_guarded_trial",
            "capability_unknown_allowed": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "action_matrix": {
            "schema_version": "hardware_camera_control_action_matrix_v1",
            "actions": action_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capture_collection": {
            "schema_version": "hardware_static_capture_request_candidate_collection_v1",
            "static_capture_request_candidate_count": len(capture_candidates),
            "candidates": capture_candidates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "unknown_policy": {
            "schema_version": "hardware_capability_unknown_unsupported_policy_v1",
            "conditions": unknown_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "fallback_policy": {
            "schema_version": "hardware_camera_failure_fallback_policy_v1",
            "fallbacks": fallback_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "health_link_policy": {
            "schema_version": "hardware_camera_system_health_link_policy_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_required_later": True,
            "failure_classes": HEALTH_FAILURE_CLASSES,
            "recovery_actions": HEALTH_RECOVERY,
            "recovery_action_committed_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ocr_gate_link": {
            "schema_version": "hardware_static_capture_to_ocrrequest_future_gate_link_v1",
            "static_capture_required_before_ocrrequest": True,
            "readable_region_candidate_required": True,
            "static_capture_result_required": True,
            "stc_freshness_required": True,
            "capture_quality_required": True,
            "ocrrequest_eligible_later": True,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "provider_invoked_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "guardedtrial": {
            "schema_version": "hardware_camera_guardedtrial_handoff_policy_v1",
            "guardedtrial_handoff_defined": True,
            "guardedtrial_allowed_later": True,
            "guardedtrial_invoked_now": False,
            "required_before_guardedtrial": [
                "hardware_profile_available_or_unknown_handled",
                "system_health_link_defined",
                "fallback_policy_defined",
                "static_capture_request_candidate_available",
                "no_write_boundary_passed",
            ],
            "recommended_next_phase_candidates": [
                "Hardware-Camera-Control-Runtime-DryRun-v1",
                "Assisted-Static-Reading-GuardedTrial-v1",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "hardware_camera_control_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "hardware_profile_ref",
                "capture_candidate_ref",
                "failure_or_unknown_reason",
                "confidence_policy",
                "privacy_sensitivity",
                "future_usage_scope",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "trace": {
            "schema_version": "hardware_camera_control_contract_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "hardware_camera_control_contract_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "static_capture_request_candidate_count": len(capture_candidates),
            "hardware_capability_unknown_allowed": True,
            "runtime_camera_invoked": False,
            "hardware_action_invoked": False,
            "ocrrequest_generated": False,
            "recommended_next_phase": "Hardware-Camera-Control-Runtime-DryRun-v1",
            "alternate_next_phase": "Assisted-Static-Reading-GuardedTrial-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "hardware_camera_control_boundary_report_v1",
            "contract_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "zoom_invoked": False,
            "autofocus_invoked": False,
            "exposure_control_invoked": False,
            "stabilization_invoked": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "midplatform_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "hardware_camera_control_metrics_candidate_report_v1",
            "static_capture_handoff_candidate_count_observed": handoff_count,
            "static_capture_request_candidate_count": len(capture_candidates),
            "camera_control_action_count": len(action_rows),
            "hardware_failure_class_count": len(HEALTH_FAILURE_CLASSES),
            "fallback_policy_count": len(fallback_rows),
            "runtime_action_committed_count": 0,
            "hardware_action_invoked_count": 0,
            "runtime_camera_invoked_count": 0,
            "ocrrequest_generated_count": 0,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "hardware_camera_control_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link_report": {
            "schema_version": "hardware_camera_control_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_generated": False,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "hardware_camera_control_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "contract_only": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "zoom_invoked": False,
            "autofocus_invoked": False,
            "exposure_control_invoked": False,
            "stabilization_invoked": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "hardware_camera_control_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "hardware_camera_control_non_claims_report_v1",
            "claims": [
                "no_real_camera_invocation",
                "no_hardware_action_execution",
                "request_schema_not_hardware_control",
                "capability_report_not_hardware_certification",
                "static_capture_request_not_capture",
                "hardware_unknown_not_failure_fact",
                "no_ocr_no_ocrrequest",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "hardware_camera_control_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "hardware_camera_control_audit_report_v1",
            "hardware_camera_control_contract_v1_executed": True,
            "contract_only": True,
            "camera_control_request_schema_defined": True,
            "hardware_capability_report_schema_defined": True,
            "camera_control_action_matrix_defined": True,
            "static_capture_request_candidate_schema_defined": True,
            "hardware_failure_fallback_policy_defined": True,
            "system_health_link_defined": True,
            "guardedtrial_handoff_defined": True,
            "hardware_capability_unknown_allowed": True,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "zoom_invoked": False,
            "autofocus_invoked": False,
            "exposure_control_invoked": False,
            "stabilization_invoked": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "runtime_tts_invoked": False,
            "voice_output_plane_invoked": False,
            "speech_request_submitted": False,
            "midplatform_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }


def _capability_for_request(request_type: str) -> str:
    mapping = {
        "STATIC_CAPTURE_REQUEST": "frame_capture_supported",
        "ZOOM_REQUEST": "zoom_supported",
        "AUTOFOCUS_REQUEST": "autofocus_supported",
        "EXPOSURE_ADJUST_REQUEST": "exposure_control_supported",
        "STABILIZATION_REQUEST": "stabilization_supported",
        "RESAMPLING_REQUEST": "frame_capture_supported",
        "STILL_FRAME_REQUEST": "still_frame_supported",
        "STATIC_READING_MODE_REQUEST": "camera_available",
    }
    return mapping.get(request_type, "camera_available")
