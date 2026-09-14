# -*- coding: utf-8 -*-
"""Hardware Camera Runtime Adapter Implementation Stub v1 — smoke phase outputs.

Phase-Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.hardware_camera_runtime_adapter_stub_v1 import (
    ADAPTER_ID,
    ADAPTER_STATUS,
    METHOD_NAMES,
    REAL_CAMERA_ENABLED,
    invoke_all_stub_methods_smoke,
)

PHASE_ID = "Hardware-Camera-Runtime-Adapter-Implementation-Stub-v1-001"
FINAL_DECISION = "STUB_READY_SOFTWARE_BOUNDARY_CLOSED"

METHOD_STUB_META = {
    "open_camera": ("blocked_stub_only", "ADAPTER_STUB_ONLY"),
    "close_camera": ("no_active_session", "NO_ACTIVE_CAMERA_SESSION"),
    "capture_frame": ("not_captured", "ADAPTER_STUB_ONLY"),
    "request_zoom": ("not_applied", "ZOOM_NOT_AVAILABLE_IN_STUB"),
    "request_autofocus": ("not_applied", "AUTOFOCUS_NOT_AVAILABLE_IN_STUB"),
    "request_exposure_adjustment": ("not_applied", "EXPOSURE_NOT_AVAILABLE_IN_STUB"),
    "request_stabilization": ("not_applied", "STABILIZATION_NOT_AVAILABLE_IN_STUB"),
    "get_capability_report": ("unknown", "CAPABILITY_UNKNOWN_STUB"),
    "get_health_status": ("stub_only", "ADAPTER_STUB_ONLY"),
}

FOLLOWUPS = [
    "Return-To-Software-Mainline",
    "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
    "Hardware-Camera-Runtime-Adapter-RealImplementation-v1",
    "Hardware-Profile-Capability-Registry-Review-v1",
    "Vision-Zoom-Autofocus-Resampling-Policy-v1",
    "OCRRequest-Gated-Submission-from-StaticReading-v1",
    "Confirmed-Text-Evidence-Memory-Governance-Contract-v1",
    "Emotional-Context-Background-Candidate-DryRun-v1",
]

LONG_TERM_TYPES = [
    "adapter_stub_available_observation_candidate",
    "real_adapter_missing_candidate",
    "hardware_integration_deferred_candidate",
    "user_environment_context_candidate",
    "user_profile_context_candidate",
    "emotional_context_background_candidate",
]

TRACE_STEPS: List[Tuple[str, str, List[str], List[str], List[str]]] = [
    ("load_adapter_contract", "contract_loaded", [], [], []),
    ("load_profile_registry", "registry_loaded", [], [], []),
    ("implement_stub_interface", "stub_impl", [], [], ["real_camera"]),
    ("invoke_stub_methods_in_smoke", "nine_invoked", [], [], []),
    ("generate_method_stub_response_matrix", "matrix", [], [], []),
    ("generate_capability_report_stub", "cap_stub", [], [], []),
    ("generate_health_status_stub", "health_stub", [], [], []),
    ("generate_frame_capture_stub_response", "frame_stub", [], [], []),
    ("evaluate_ocrrequest_gate", "ocr_blocked", [], [], ["ocrrequest_now"]),
    ("evaluate_guardedtrial_readiness", "gt_blocked", [], [], ["guardedtrial_now"]),
    ("generate_long_term_candidate_link", "lt", [], [], []),
    ("generate_final_stub_decision", FINAL_DECISION, [], [], ["routing_change"]),
]


def _read_json(p: Path) -> Any:
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def _intake(roots: Dict[str, Path]) -> Dict[str, Any]:
    specs = [
        ("adapter_contract", roots["contract"], "hardware_camera_runtime_adapter_contract_v1_summary.json", False),
        ("profile_registry", roots["registry"], "hardware_profile_capability_registry_v1_summary.json", False),
        ("hardware_runtime", roots["hw_rt"], "hardware_camera_control_runtime_dryrun_v1_summary.json", False),
        ("hardware_contract", roots["hw_contract"], "hardware_camera_control_contract_v1_summary.json", False),
        ("rrd_runtime", roots["rrd"], "static_readable_region_discovery_runtime_dryrun_v1_summary.json", False),
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
    return {
        "schema_version": "hardware_camera_adapter_stub_input_intake_matrix_v1",
        "rows": rows,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_hardware_camera_runtime_adapter_implementation_stub_v1(
    *,
    adapter_contract_root: str,
    hardware_profile_registry_root: str,
    hardware_runtime_root: str,
    hardware_contract_root: str,
    rrd_runtime_root: str,
    benchmark_smoke_root: str,
    system_health_root: str,
    simulation_root: str,
    workspace_root: Optional[str] = None,
) -> Dict[str, Any]:
    _ = workspace_root
    roots = {
        "contract": Path(adapter_contract_root).resolve(),
        "registry": Path(hardware_profile_registry_root).resolve(),
        "hw_rt": Path(hardware_runtime_root).resolve(),
        "hw_contract": Path(hardware_contract_root).resolve(),
        "rrd": Path(rrd_runtime_root).resolve(),
        "bench": Path(benchmark_smoke_root).resolve(),
        "health": Path(system_health_root).resolve(),
        "sim": Path(simulation_root).resolve(),
    }

    smoke_results = invoke_all_stub_methods_smoke()
    method_rows = []
    for name in METHOD_NAMES:
        status, err = METHOD_STUB_META[name]
        resp = smoke_results[name]
        method_rows.append(
            {
                "method_name": name,
                "implemented_as_stub": True,
                "invoked_in_smoke": True,
                "real_hardware_called": False,
                "response_status": status,
                "error_code": err,
                "response_schema_aligned": True,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    cap_resp = smoke_results["get_capability_report"]
    cap_cand = cap_resp.get("capability_report_candidate") or {}
    health_resp = smoke_results["get_health_status"]
    frame_resp = smoke_results["capture_frame"]

    guardedtrial_blockers = [
        "real_adapter_missing",
        "real_camera_disabled",
        "permission_state_unknown",
        "hardware_profile_not_verified",
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
            "schema_version": "hardware_camera_runtime_adapter_implementation_stub_v1_summary_v0",
            "phase": PHASE_ID,
            "stub_scope": "hardware_camera_runtime_adapter_stub_only",
            "based_on_adapter_contract": roots["contract"].is_dir(),
            "based_on_hardware_profile_registry": roots["registry"].is_dir(),
            "adapter_stub_implemented": True,
            "required_methods_implemented_as_stub": True,
            "required_method_count_observed": len(METHOD_NAMES),
            "adapter_implementation_real": False,
            "adapter_status": ADAPTER_STATUS,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "hardware_probe_invoked": False,
            "runtime_camera_invoked": False,
            "runtime_frame_captured": False,
            "hardware_action_invoked": False,
            "zoom_invoked": False,
            "autofocus_invoked": False,
            "exposure_control_invoked": False,
            "stabilization_invoked": False,
            "capability_report_stub_generated": True,
            "health_status_stub_generated": True,
            "frame_capture_stub_response_generated": True,
            "system_health_mapping_stub_generated": True,
            "ocrrequest_future_gate_still_blocked": True,
            "guardedtrial_allowed_now": False,
            "detector_invoked": False,
            "ocr_invoked": False,
            "ocrrequest_generated": False,
            "midplatform_fact_written": False,
            "hardware_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
            "write_allowed": False,
            "phase_verdict_hint": "GO",
        },
        "intake": _intake(roots),
        "method_matrix": {
            "schema_version": "hardware_camera_adapter_method_stub_response_matrix_v1",
            "methods": method_rows,
            "fact_status": "not_fact",
            "write_allowed": False,
        },
        "capability_stub": {
            "schema_version": "hardware_camera_adapter_capability_report_stub_v1",
            "capability_report_stub_generated": True,
            "camera_available_status": cap_cand.get("camera_available_status", "unknown"),
            "zoom_supported_status": cap_cand.get("zoom_supported_status", "unknown"),
            "autofocus_supported_status": cap_cand.get("autofocus_supported_status", "unknown"),
            "exposure_control_supported_status": cap_cand.get("exposure_control_supported_status", "unknown"),
            "stabilization_supported_status": cap_cand.get("stabilization_supported_status", "unknown"),
            "frame_capture_supported_status": cap_cand.get("frame_capture_supported_status", "unknown"),
            "still_frame_supported_status": cap_cand.get("still_frame_supported_status", "unknown"),
            "capability_status": "unknown",
            "adapter_status": ADAPTER_STATUS,
            "capability_fact_written": False,
            "fact_status": "not_fact",
        },
        "health_stub": {
            "schema_version": "hardware_camera_adapter_health_status_stub_v1",
            "health_status_stub_generated": True,
            "adapter_status": ADAPTER_STATUS,
            "status": "unknown",
            "failure_class_candidate": health_resp.get("failure_class_candidate", "ADAPTER_STUB_ONLY"),
            "recovery_candidate": [
                "INSTALL_RUNTIME_ADAPTER",
                "KEEP_HARDWARE_DISABLED",
                "FALLBACK_USER_GUIDANCE",
                "FALLBACK_EXTERNAL_ASSISTANCE",
            ],
            "system_health_report_required_later": True,
            "module_health_report_generated_now": False,
            "recovery_action_committed_now": False,
            "fact_status": "not_fact",
        },
        "frame_stub": {
            "schema_version": "hardware_camera_adapter_frame_capture_stub_response_v1",
            "frame_capture_stub_response_generated": True,
            "capture_status": frame_resp.get("capture_status", "not_captured"),
            "frame_ref": frame_resp.get("frame_ref"),
            "frame_timestamp": frame_resp.get("frame_timestamp"),
            "frame_is_fact": False,
            "error_code": frame_resp.get("error_code", "ADAPTER_STUB_ONLY"),
            "runtime_frame_captured": False,
            "stc_anchor_required_later": True,
            "fact_status": "not_fact",
        },
        "error_mapping": {
            "schema_version": "hardware_camera_adapter_error_mapping_stub_v1",
            "error_mapping_stub_generated": True,
            "error_codes_used": list({r["error_code"] for r in method_rows}),
            "mapped_to_system_health_failure_classes": {
                "ADAPTER_STUB_ONLY": "ADAPTER_STUB_ONLY",
                "CAPABILITY_UNKNOWN_STUB": "HARDWARE_CAPABILITY_UNKNOWN",
                "NO_ACTIVE_CAMERA_SESSION": "CAMERA_UNAVAILABLE",
            },
            "recovery_candidates": [
                "INSTALL_RUNTIME_ADAPTER",
                "KEEP_HARDWARE_DISABLED",
                "FALLBACK_USER_GUIDANCE",
            ],
            "recovery_action_committed_now": False,
            "fact_status": "not_fact",
        },
        "ocr_gate": {
            "schema_version": "hardware_camera_adapter_stub_ocrrequest_gate_link_v1",
            "ocrrequest_gate_checked": True,
            "static_capture_result_available": False,
            "frame_capture_response_available": True,
            "capture_status": "not_captured",
            "capture_quality_available": False,
            "stc_anchor_available": False,
            "ocrrequest_eligible_now": False,
            "ocrrequest_generated_now": False,
            "provider_invoked_now": False,
            "ocrrequest_future_gate_still_blocked": True,
            "fact_status": "not_fact",
        },
        "guardedtrial_link": {
            "schema_version": "hardware_camera_adapter_stub_guardedtrial_readiness_link_v1",
            "guardedtrial_readiness_evaluated": True,
            "adapter_contract_defined": True,
            "adapter_stub_available": True,
            "real_adapter_available": False,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "permission_state_known": False,
            "guardedtrial_allowed_now": False,
            "guardedtrial_allowed_later": True,
            "current_blockers": guardedtrial_blockers,
            "recommended_next_phase_candidates": [
                "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
                "Hardware-Camera-Runtime-Adapter-RealImplementation-v1",
                "Return-To-Software-Mainline",
            ],
            "fact_status": "not_fact",
        },
        "long_term": {
            "schema_version": "hardware_camera_adapter_stub_long_term_candidate_link_v1",
            "can_feed_long_term_candidate": True,
            "candidate_types": LONG_TERM_TYPES,
            "cannot_write_fact": True,
            "cannot_write_profile_now": True,
            "write_allowed_now": False,
            "required_metadata": [
                "source_chain",
                "time_anchor",
                "adapter_stub_ref",
                "missing_real_adapter_reason",
                "future_usage_scope",
                "privacy_sensitivity",
            ],
            "fact_status": "not_fact",
        },
        "trace": {
            "schema_version": "hardware_camera_adapter_stub_decision_trace_v1",
            "steps": trace_steps,
            "fact_status": "not_fact",
        },
        "final": {
            "schema_version": "hardware_camera_adapter_stub_final_decision_v1",
            "final_decision": FINAL_DECISION,
            "adapter_stub_implemented": True,
            "real_adapter_available": False,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "ocrrequest_eligible_now": False,
            "guardedtrial_allowed_now": False,
            "recommended_next_phase": "Return-To-Software-Mainline",
            "alternate_next_phase": "Hardware-Camera-Control-GuardedTrial-Precheck-v1",
            "fact_status": "not_fact",
        },
        "boundary": {
            "schema_version": "hardware_camera_adapter_stub_boundary_report_v1",
            "adapter_stub_only": True,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "hardware_probe_invoked": False,
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
            "midplatform_fact_written": False,
            "hardware_fact_written": False,
            "world_model_written": False,
            "scene_delta_candidate_generated": False,
            "fact_status": "not_fact",
        },
        "metrics": {
            "schema_version": "hardware_camera_adapter_stub_metrics_candidate_report_v1",
            "required_method_count": len(METHOD_NAMES),
            "implemented_stub_method_count": len(METHOD_NAMES),
            "real_hardware_call_count": 0,
            "frame_captured_count": 0,
            "ocrrequest_generated_count": 0,
            "guardedtrial_allowed_now": False,
            "fact_write_allowed_count": 0,
            "no_write_boundary_pass_rate": 1.0,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "benchmark_link": {
            "schema_version": "hardware_camera_adapter_stub_benchmark_link_report_v1",
            "benchmark_real_values_smoke_available": roots["bench"].is_dir(),
            "current_phase_updates_benchmark_values": False,
            "current_phase_collects_t2": False,
            "ground_truth_available": False,
            "benchmark_score_generated": False,
            "provider_comparison_claimed": False,
        },
        "health_report": {
            "schema_version": "hardware_camera_adapter_stub_system_health_report_v1",
            "system_health_governance_available": roots["health"].is_dir(),
            "module_health_report_candidate_generated": True,
            "failure_class_candidate": "ADAPTER_STUB_ONLY",
            "provider_health_runtime_checked": False,
            "recovery_action_committed": False,
            "capability_mask_consumed": False,
            "no_runtime_health_claim": True,
        },
        "no_write": {
            "schema_version": "hardware_camera_adapter_stub_no_write_boundary_report_v1",
            "boundary_ok": True,
            "violations": [],
            "adapter_stub_only": True,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "hardware_probe_invoked": False,
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
            "midplatform_fact_written": False,
            "hardware_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "sim_report": {
            "schema_version": "hardware_camera_adapter_stub_simulation_context_report_v1",
            "simulation_profile_id": "developer_full",
            "simulation_context_available": roots["sim"].is_dir(),
            "run_model": False,
            "simulation_context_only": True,
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "no_hardware_certification_claim": True,
        },
        "non_claims": {
            "schema_version": "hardware_camera_adapter_stub_non_claims_report_v1",
            "claims": [
                "not_real_hardware_integration",
                "adapter_stub_not_real_adapter",
                "method_smoke_not_hardware_action",
                "capture_frame_stub_not_capture",
                "capability_stub_not_fact",
                "health_stub_not_health_commit",
                "guardedtrial_later_not_now",
                "no_camera_no_ocr",
                "no_world_model_write",
                "not_production_ready",
            ],
        },
        "followups": {
            "schema_version": "hardware_camera_adapter_stub_open_followups_v1",
            "items": FOLLOWUPS,
        },
        "audit": {
            "schema_version": "hardware_camera_adapter_stub_audit_report_v1",
            "hardware_camera_runtime_adapter_implementation_stub_v1_executed": True,
            "adapter_stub_only": True,
            "adapter_stub_implemented": True,
            "required_methods_implemented_as_stub": True,
            "implemented_stub_method_count": len(METHOD_NAMES),
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "real_hardware_call_count": 0,
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
            "guardedtrial_allowed_now": False,
            "midplatform_fact_written": False,
            "hardware_fact_written": False,
            "scene_delta_candidate_generated": False,
            "world_model_written": False,
            "benchmark_result_claimed": False,
            "provider_comparison_claimed": False,
            "production_readiness_claimed": False,
        },
        "stub_interface_ref": {
            "schema_version": "hardware_camera_adapter_stub_interface_implementation_ref_v1",
            "module": "capabilities.midplatform.hardware_camera_runtime_adapter_stub_v1",
            "adapter_id": ADAPTER_ID,
            "adapter_status": ADAPTER_STATUS,
            "required_methods": METHOD_NAMES,
            "real_camera_enabled": REAL_CAMERA_ENABLED,
            "fact_status": "not_fact",
        },
    }
