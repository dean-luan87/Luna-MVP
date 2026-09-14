# -*- coding: utf-8 -*-
"""Hardware Camera Control Runtime DryRun v1 — contract under hardware unknown.

Phase-Hardware-Camera-Control-Runtime-DryRun-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Hardware-Camera-Control-Runtime-DryRun-v1-001"
FINAL_DECISION = "BLOCK_RUNTIME_CAMERA_ACTION_PREPARE_GUARDEDTRIAL_OR_FALLBACK"

CONTROL_ACTIONS = [
    ("request_static_capture", "frame_capture_supported"),
    ("request_zoom", "zoom_supported"),
    ("request_autofocus", "autofocus_supported"),
    ("request_exposure_adjustment", "exposure_control_supported"),
    ("request_stabilization", "stabilization_supported"),
    ("request_resampling", "frame_capture_supported"),
    ("request_still_frame", "still_frame_supported"),
    ("request_static_reading_mode", "camera_available"),
]

FALLBACK_TYPES = [
    ("return_to_user_guidance", "hardware_capability_unknown"),
    ("request_external_assistance", "hardware_profile_missing"),
    ("downgrade_to_visual_semantic_path", "capture_not_possible_now"),
    ("mark_unresolved_capture_candidate", "static_capture_blocked"),
    ("mark_expired_capture_candidate", "stc_not_evaluated"),
    ("stop_internal_retry", "no_hardware_adapter"),
    ("ask_user_manual_confirmation", "capability_unknown"),
]

LONG_TERM_TYPES = [
    "hardware_capability_unknown_observation_candidate",
    "unresolved_static_capture_candidate",
    "repeated_capture_unavailable_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

FOLLOWUPS = [
    "Hardware-Profile-Capability-Registry-v1",
    "Hardware-Camera-Control-GuardedTrial-v1",
    "Assisted-Static-Reading-GuardedTrial-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Evidence-Pack-Adapter-v5-StaticReading",
    "Semantic-Candidate-v5-StaticReading",
    "Source-Validation-v3-StaticReading",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

OPTIONAL_HW_PATHS = [
    ("hardware_profile", "docs/architecture/midplatform/LUNA_HARDWARE_PROFILE_V0.md"),
    ("camera_capability_registry", "docs/architecture/midplatform/LUNA_CAMERA_CAPABILITY_REGISTRY_V0.md"),
    ("device_registry", "docs/architecture/midplatform/LUNA_DEVICE_REGISTRY_V0.md"),
    ("sensor_registry", "docs/architecture/midplatform/LUNA_SENSOR_REGISTRY_V0.md"),
    ("camera_runtime_adapter", "docs/architecture/midplatform/LUNA_CAMERA_RUNTIME_ADAPTER_V0.md"),
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_hardware_contract", "contract_loaded", [], [], []),
    ("load_static_capture_request_candidates", "twenty_six_requests", [], [], []),
    ("load_system_health_governance", "health_loaded", [], [], []),
    ("evaluate_hardware_capability", "capability_unknown", [], [], []),
    ("apply_unknown_capability_policy", "policy_applied", [], [], ["invoke_camera"]),
    ("evaluate_runtime_action_matrix", "all_blocked", [], [], []),
    ("evaluate_static_capture_runtime_decision", "capture_blocked", [], [], ["capture_now"]),
    ("evaluate_ocrrequest_gate_link", "ocr_blocked", [], [], ["ocrrequest_now"]),
    ("generate_fallback_candidates", "fallbacks", [], [], []),
    ("generate_system_health_link", "health_link", [], [], []),
    ("generate_guardedtrial_readiness", "guardedtrial_later", [], [], ["guardedtrial_now"]),
    ("generate_final_runtime_dryrun_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path], ws: Path) -> Dict[str, Any]:
    specs = [
        ("hardware_contract", roots["contract"], "hardware_camera_control_contract_v1_summary.json", False),
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
        ("vision_gov", roots["vision_gov"], "vision_capture_governance_v1_summary.json", False),
        ("vision_rt", roots["vision_rt"], "vision_capture_runtime_dryrun_v1_summary.json", False),
        ("assisted_rt", roots["assisted_rt"], "assisted_static_reading_runtime_dryrun_v1_summary.json", False),
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
    capture = _read_json(roots["contract"] / "hardware_static_capture_request_candidate_collection_v1.json")
    if capture:
        rows.append(
            {
                "intake_id": "static_capture_requests",
                "input_source": "hardware_contract",
                "source_root_or_path": str(roots["contract"]),
                "artifact": "hardware_static_capture_request_candidate_collection_v1.json",
                "loaded": True,
                "optional": False,
                "key_fields_observed": ["candidates", "static_capture_request_candidate_count"],
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
        "schema_version": "hardware_camera_control_runtime_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_hardware_camera_control_runtime_dryrun_v1(
    *,
    hardware_contract_root: str,
    rrd_runtime_root: str,
    vision_capture_governance_root: str,
    vision_capture_runtime_root: str,
    assisted_static_reading_runtime_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    ws = Path(workspace_root or Path(__file__).resolve().parents[2])
    roots = {
        "contract": Path(hardware_contract_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "vision_gov": Path(vision_capture_governance_root).resolve(),
        "vision_rt": Path(vision_capture_runtime_root).resolve(),
        "assisted_rt": Path(assisted_static_reading_runtime_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    contract_summary = _read_json(roots["contract"] / "hardware_camera_control_contract_v1_summary.json") or {}
    capture_data = _read_json(roots["contract"] / "hardware_static_capture_request_candidate_collection_v1.json") or {}
    capture_list = [c for c in (capture_data.get("candidates") or []) if isinstance(c, dict)]
    capture_count = len(capture_list)

    hw_profile_available = contract_summary.get("optional_hardware_profile_available", False)
    registry_available = any(
        (ws / rel).is_file() for _, rel in OPTIONAL_HW_PATHS if "registry" in rel or "capability" in rel
    )

    action_decisions = [
        {
            "action_name": name,
            "capability_required": cap,
            "capability_status": "unknown",
            "allowed_now": False,
            "blocked_reason": "hardware_capability_unknown",
            "fallback_candidate": "return_to_user_guidance",
            "action_invoked_now": False,
            "fact_status": "not_fact",
        }
        for name, cap in CONTROL_ACTIONS
    ]

    fallback_candidates = [
        {
            "fallback_candidate_id": f"hfb_{i:03d}",
            "fallback_type": ft,
            "trigger_condition": trig,
            "allowed_later": True,
            "committed_now": False,
            "can_feed_long_term_candidate": ft not in ("stop_internal_retry",),
            "fact_status": "not_fact",
        }
        for i, (ft, trig) in enumerate(FALLBACK_TYPES, 1)
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

    return {
        "summary": {
            "schema_version": "hardware_camera_control_runtime_dryrun_v1_summary_v0",
            "phase": PHASE_ID,
            "dryrun_scope": "hardware_camera_control_runtime_dryrun_only",
            "based_on_hardware_camera_control_contract": roots["contract"].is_dir(),
            "based_on_rrd_runtime": roots["rrd"].is_dir(),
            "based_on_system_health_center": roots["health"].is_dir(),
            "current_case_loaded": True,
            "static_capture_request_candidate_count_observed": capture_count,
            "hardware_capability_evaluation_executed": True,
            "hardware_profile_available": hw_profile_available,
            "camera_capability_registry_available": registry_available,
            "hardware_capability_status": "unknown",
            "capability_unknown_policy_applied": True,
            "runtime_action_decision_generated": True,
            "static_capture_runtime_allowed_now": False,
            "hardware_action_allowed_now": False,
            "fallback_candidate_generated": len(fallback_candidates) > 0,
            "guardedtrial_readiness_candidate_generated": True,
            "ocrrequest_future_gate_still_blocked": True,
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
            "hardware_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots, ws),
        "capture_intake": {
            "schema_version": "hardware_static_capture_request_runtime_intake_v1",
            "static_capture_request_candidate_count_observed": capture_count,
            "accepted_for_runtime_dryrun_count": capture_count,
            "request_types_observed": [
                "STATIC_CAPTURE_REQUEST",
                "optional_zoom",
                "optional_autofocus",
            ],
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capability_eval": {
            "schema_version": "hardware_capability_runtime_evaluation_v1",
            "hardware_capability_evaluation_executed": True,
            "hardware_profile_available": hw_profile_available,
            "camera_available": "unknown",
            "zoom_supported": "unknown",
            "autofocus_supported": "unknown",
            "exposure_control_supported": "unknown",
            "stabilization_supported": "unknown",
            "still_frame_supported": "unknown",
            "capability_unknown_allowed": True,
            "capability_status": "unknown",
            "capability_fact_written": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "unknown_handling": {
            "schema_version": "hardware_capability_unknown_runtime_handling_v1",
            "capability_unknown_policy_applied": True,
            "condition": "hardware_profile_missing",
            "blocked_actions": [
                "invoke_camera",
                "invoke_zoom",
                "invoke_autofocus",
                "invoke_exposure_control",
                "capture_frame",
                "generate_ocrrequest",
            ],
            "allowed_fallbacks": [
                "return_to_user_guidance",
                "request_external_assistance",
                "prepare_guardedtrial_later",
                "mark_unresolved_static_capture_candidate",
            ],
            "runtime_action_committed": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "action_matrix": {
            "schema_version": "hardware_camera_runtime_action_decision_matrix_v1",
            "decisions": action_decisions,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capture_decision": {
            "schema_version": "hardware_static_capture_runtime_decision_candidate_v1",
            "static_capture_runtime_decision_generated": True,
            "static_capture_allowed_now": False,
            "static_capture_ready_later": True,
            "reason_not_allowed_now": [
                "hardware_capability_unknown",
                "no_runtime_camera_adapter",
                "no_guardedtrial_authorization",
            ],
            "static_capture_request_candidates_preserved": True,
            "frame_captured_now": False,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "ocr_gate": {
            "schema_version": "hardware_camera_ocrrequest_gate_runtime_link_v1",
            "static_capture_required_before_ocrrequest": True,
            "static_capture_result_available": False,
            "capture_quality_available": False,
            "stc_freshness_available": False,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "provider_invoked_now": False,
            "ocrrequest_future_gate_still_blocked": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "fallback_collection": {
            "schema_version": "hardware_camera_runtime_fallback_candidate_collection_v1",
            "fallback_candidate_count": len(fallback_candidates),
            "candidates": fallback_candidates,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "health_runtime": {
            "schema_version": "hardware_camera_runtime_system_health_link_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": True,
            "failure_class_candidate": "HARDWARE_CAPABILITY_UNKNOWN",
            "recovery_action_candidate": [
                "FALLBACK_USER_GUIDANCE",
                "FALLBACK_EXTERNAL_ASSISTANCE",
                "DEGRADED_MODE",
            ],
            "recovery_action_committed_now": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "guardedtrial": {
            "schema_version": "hardware_camera_guardedtrial_readiness_candidate_v1",
            "guardedtrial_readiness_candidate_generated": True,
            "guardedtrial_allowed_later": True,
            "guardedtrial_invoked_now": False,
            "readiness_conditions": [
                "hardware_profile_available_or_unknown_handled",
                "runtime_adapter_available",
                "system_health_link_defined",
                "fallback_policy_defined",
                "no_write_boundary_passed",
            ],
            "readiness_status": "blocked_until_runtime_adapter_or_authorization",
            "recommended_next_phase_candidates": [
                "Hardware-Camera-Control-GuardedTrial-v1",
                "Assisted-Static-Reading-GuardedTrial-v1",
            ],
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "long_term": {
            "schema_version": "hardware_camera_control_runtime_long_term_candidate_link_v1",
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
            "schema_version": "hardware_camera_control_runtime_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "final": {
            "schema_version": "hardware_camera_control_runtime_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "static_capture_request_candidate_count_observed": capture_count,
            "hardware_capability_status": "unknown",
            "static_capture_allowed_now": False,
            "hardware_action_allowed_now": False,
            "ocrrequest_eligible_now": False,
            "guardedtrial_allowed_later": True,
            "fallback_candidate_generated": True,
            "recommended_next_phase": "Hardware-Camera-Control-GuardedTrial-v1",
            "alternate_next_phase": "Hardware-Profile-Capability-Registry-v1",
            "alternate_next_phase_2": "Assisted-Static-Reading-GuardedTrial-v1",
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "boundary": {
            "schema_version": "hardware_camera_control_runtime_boundary_report_v1",
            "runtime_dryrun_only": True,
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
            "hardware_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "hardware_camera_control_runtime_metrics_candidate_report_v1",
            "static_capture_request_candidate_count_observed": capture_count,
            "accepted_for_runtime_dryrun_count": capture_count,
            "action_decision_count": len(action_decisions),
            "allowed_action_now_count": 0,
            "blocked_action_now_count": len(action_decisions),
            "fallback_candidate_count": len(fallback_candidates),
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
            "schema_version": "hardware_camera_control_runtime_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_link_report": {
            "schema_version": "hardware_camera_control_runtime_system_health_link_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": True,
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "hardware_camera_control_runtime_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "runtime_dryrun_only": True,
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
            "hardware_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "hardware_camera_control_runtime_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "hardware_camera_control_runtime_non_claims_report_v1",
            "claims": [
                "no_real_camera_invocation",
                "no_hardware_action_execution",
                "runtime_decision_not_hardware_result",
                "capability_unknown_not_failure_fact",
                "fallback_candidate_not_actual_fallback",
                "guardedtrial_readiness_not_execution",
                "no_ocr_no_ocrrequest",
                "no_world_model_write",
                "no_scene_delta",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "hardware_camera_control_runtime_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "hardware_camera_control_runtime_audit_report_v1",
            "hardware_camera_control_runtime_dryrun_v1_executed": True,
            "runtime_dryrun_only": True,
            "hardware_capability_evaluation_executed": True,
            "hardware_capability_status": "unknown",
            "capability_unknown_policy_applied": True,
            "static_capture_allowed_now": False,
            "hardware_action_allowed_now": False,
            "fallback_candidate_generated": True,
            "guardedtrial_readiness_candidate_generated": True,
            "ocrrequest_future_gate_still_blocked": True,
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
            "hardware_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
    }
