#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Trial Definition v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

MIN_CHECKS = 72


def _require_abs(path_str: str, label: str) -> Path:
    p = Path(path_str).expanduser()
    if not p.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {path_str}")
    return p.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    smoke_root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks_passed = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks_passed
        if cond:
            checks_passed += 1
        else:
            blockers.append(name)

    files = {
        "summary": "summary.json",
        "input_root_matrix": "input_root_matrix.json",
        "minimal_runtime_trial_definition": "minimal_runtime_trial_definition.json",
        "runtime_module_boundary_matrix": "runtime_module_boundary_matrix.json",
        "trial_input_plan": "trial_input_plan.json",
        "trial_output_plan": "trial_output_plan.json",
        "trial_safety_envelope": "trial_safety_envelope.json",
        "abort_conditions": "abort_conditions.json",
        "rollback_plan": "rollback_plan.json",
        "observability_requirements": "observability_requirements.json",
        "go_no_go_criteria": "go_no_go_criteria.json",
        "future_trial_execution_contract": "future_trial_execution_contract.json",
        "no_runtime_boundary_report": "no_runtime_boundary_report.json",
        "no_write_boundary_report": "no_write_boundary_report.json",
    }

    data: Dict[str, Any] = {}
    for key, filename in files.items():
        path = smoke_root / filename
        if not path.is_file():
            blockers.append(f"missing:{key}")
        else:
            data[key] = json.loads(path.read_text(encoding="utf-8"))

    if blockers:
        report = {
            "verdict": "NO_GO",
            "checks_passed": 0,
            "checks_expected": MIN_CHECKS,
            "blockers": blockers,
            "phase": "Minimal-Runtime-Integration-Trial-Definition-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    trial_definition = data["minimal_runtime_trial_definition"]
    boundary_matrix = data["runtime_module_boundary_matrix"]
    trial_input_plan = data["trial_input_plan"]
    trial_output_plan = data["trial_output_plan"]
    safety_envelope = data["trial_safety_envelope"]
    abort_conditions = data["abort_conditions"]
    rollback_plan = data["rollback_plan"]
    observability = data["observability_requirements"]
    go_no_go = data["go_no_go_criteria"]
    future_contract = data["future_trial_execution_contract"]

    ok(summary.get("definition_scope") == "minimal_runtime_integration_trial_definition_only", "definition_scope")
    ok(summary.get("runtime_trial_executed") is False, "runtime_trial_executed")
    ok(summary.get("stabilization_input_loaded") is True, "stabilization_input_loaded")
    ok(summary.get("basic_navigation_loop_input_loaded") is True, "basic_navigation_loop_input_loaded")
    ok(summary.get("safety_task_arbitration_input_loaded") is True, "safety_task_arbitration_input_loaded")
    ok(summary.get("ownership_gate_input_loaded") is True, "ownership_gate_input_loaded")
    ok(summary.get("interruption_governance_input_loaded") is True, "interruption_governance_input_loaded")
    ok(summary.get("trial_definition_generated") is True, "trial_definition_generated")
    ok(summary.get("runtime_module_boundary_matrix_defined") is True, "runtime_module_boundary_matrix_defined")
    ok(summary.get("trial_input_plan_defined") is True, "trial_input_plan_defined")
    ok(summary.get("trial_output_plan_defined") is True, "trial_output_plan_defined")
    ok(summary.get("trial_safety_envelope_defined") is True, "trial_safety_envelope_defined")
    ok(summary.get("abort_conditions_defined") is True, "abort_conditions_defined")
    ok(summary.get("rollback_plan_defined") is True, "rollback_plan_defined")
    ok(summary.get("observability_requirements_defined") is True, "observability_requirements_defined")
    ok(summary.get("go_no_go_criteria_defined") is True, "go_no_go_criteria_defined")
    ok(
        summary.get("future_trial_execution_contract_defined") is True,
        "future_trial_execution_contract_defined",
    )
    ok(
        summary.get("final_decision")
        == "MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_READY_FOR_CONTROLLED_SHADOW_TRIAL",
        "final_decision",
    )

    for flag in [
        "runtime_camera_invoked",
        "runtime_microphone_invoked",
        "runtime_asr_invoked",
        "runtime_voiceprint_invoked",
        "runtime_face_recognition_invoked",
        "runtime_tts_invoked",
        "runtime_tts_stopped",
        "speech_gate_runtime_invoked",
        "vop_runtime_invoked",
        "map_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "detector_invoked",
        "segmentation_invoked",
        "tracking_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "memory_written",
        "world_model_written",
        "scene_delta_generated",
        "fact_written",
        "benchmark_accuracy_updated",
        "runtime_routing_changed",
    ]:
        ok(summary.get(flag) is False, f"summary_{flag}")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")

    ok(trial_definition.get("trial_mode") == "DEFINITION_ONLY", "trial_mode_definition_only")
    ok(trial_definition.get("source_chain") == "minimal_runtime_integration_trial_definition_v1", "trial_source_chain")
    ok("controlled_sample_input" in (trial_definition.get("allowed_runtime_modules") or []), "allowed_controlled_sample_input")
    ok("speech_gate" in (trial_definition.get("shadow_only_modules") or []), "shadow_speech_gate")
    forbidden_modules = set(trial_definition.get("forbidden_modules") or [])
    for item in [
        "worldmodel_write",
        "memory_write",
        "scene_delta_commit",
        "navigation_action_execution",
        "route_modification",
        "face_runtime",
        "voiceprint_runtime",
        "emotion_fact_write",
        "external_api_side_effects",
    ]:
        ok(item in forbidden_modules, f"forbidden_{item}")

    allowed_rows = boundary_matrix.get("allowed_in_future_minimal_trial") or []
    shadow_rows = boundary_matrix.get("shadow_only_in_future_minimal_trial") or []
    forbidden_definition_rows = boundary_matrix.get("forbidden_in_current_definition_phase") or []
    forbidden_first_rows = boundary_matrix.get("forbidden_even_in_first_minimal_trial") or []

    allowed_ids = {row.get("module_id") for row in allowed_rows}
    shadow_ids = {row.get("module_id") for row in shadow_rows}
    forbidden_definition_ids = {row.get("module_id") for row in forbidden_definition_rows}
    forbidden_first_ids = {row.get("module_id") for row in forbidden_first_rows}

    ok("external_api_side_effects" not in allowed_ids, "allowed_no_external_api_side_effects")
    ok("map_api_runtime" not in allowed_ids, "allowed_no_map_api")
    ok("gps_runtime" not in allowed_ids, "allowed_no_gps_runtime")
    ok("task_manager_commit" not in allowed_ids, "allowed_no_task_commit")
    ok("uncontrolled_tts_interruption" not in allowed_ids, "allowed_no_uncontrolled_tts")
    for item in [
        "speech_gate",
        "voice_output_plane",
        "tts",
        "ocr_provider",
        "asr",
        "camera",
        "gps",
        "map_context",
        "task_manager_commit",
        "system_health_recovery",
    ]:
        ok(item in shadow_ids, f"shadow_{item}")
    for item in [
        "worldmodel_write",
        "memory_write",
        "scene_delta_commit",
        "navigation_action_execution",
        "route_modification",
        "face_runtime",
        "voiceprint_runtime",
        "emotion_fact_write",
        "external_api_side_effects",
    ]:
        ok(item in forbidden_first_ids, f"forbidden_first_{item}")
    ok("map_api_runtime" in forbidden_definition_ids, "forbidden_definition_map_api")
    ok("gps_runtime" in forbidden_first_ids, "forbidden_first_gps_runtime")

    input_sources = trial_input_plan.get("allowed_future_input_sources") or []
    for item in [
        "static_fixture_trace",
        "recorded_stub_frame_sequence",
        "simulated_task_context",
        "simulated_safety_event",
        "simulated_user_voice_text",
        "simulated_ocr_candidate",
        "simulated_navigation_guidance_candidate",
    ]:
        ok(item in input_sources, f"trial_input_{item}")
    ok(trial_input_plan.get("live_camera_recommended") is False, "trial_input_live_camera_false")
    ok(trial_input_plan.get("live_microphone_recommended") is False, "trial_input_live_microphone_false")

    outputs = trial_output_plan.get("allowed_future_outputs") or []
    forbidden_outputs = set(trial_output_plan.get("forbidden_future_outputs") or [])
    for item in [
        "guidance_candidate",
        "arbitration_decision_candidate",
        "speech_request_candidate",
        "speech_gate_shadow_decision",
        "vop_shadow_event",
        "boundary_report",
        "runtime_trace_log",
        "abort_report_if_triggered",
    ]:
        ok(item in outputs, f"trial_output_{item}")
    for item in [
        "real_navigation_action",
        "fact_write",
        "worldmodel_write",
        "memory_write",
        "scene_delta_commit",
    ]:
        ok(item in forbidden_outputs, f"forbidden_output_{item}")

    ok(safety_envelope.get("abort_on_boundary_violation") is True, "safety_envelope_abort_on_boundary")
    ok(safety_envelope.get("no_write_boundary_required") is True, "safety_envelope_no_write")
    ok(safety_envelope.get("p0_p1_safety_protection_required") is True, "safety_envelope_p0_p1")
    ok(isinstance(safety_envelope.get("max_trial_duration_seconds"), int), "safety_envelope_max_duration_defined")
    ok(isinstance(safety_envelope.get("max_error_count_before_abort"), int), "safety_envelope_max_error_defined")
    ok(safety_envelope.get("max_trial_duration_seconds") == 60, "safety_envelope_duration_60")
    ok(safety_envelope.get("max_error_count_before_abort") == 1, "safety_envelope_error_1")

    abort_list = set(abort_conditions.get("conditions") or [])
    for item in [
        "any_write_boundary_violation",
        "any_runtime_module_invoked_outside_allowlist",
        "task_state_committed_now_true",
        "world_model_written_true",
        "memory_written_true",
        "scene_delta_generated_true",
        "navigation_action_triggered_true",
        "map_api_invoked_true",
        "uncontrolled_tts_invoked_true",
        "speech_gate_runtime_invoked_when_shadow_only",
        "vop_runtime_invoked_when_shadow_only",
        "missing_source_chain",
        "stale_safety_speech_treated_as_current_fact",
        "non_owner_voice_triggers_task_control",
        "p0_safety_speech_cancelled_by_ordinary_stop",
    ]:
        ok(item in abort_list, f"abort_condition_{item}")
    ok(abort_conditions.get("abort_on_boundary_violation") is True, "abort_conditions_boundary_true")

    rollback_steps = set(rollback_plan.get("steps") or [])
    for item in [
        "return_to_stabilization_test_outputs",
        "disable_runtime_trial_flag",
        "preserve_logs",
        "write_abort_report",
        "no_state_rollback_needed_because_no_state_commit_allowed",
        "require_manual_review_before_retry",
    ]:
        ok(item in rollback_steps, f"rollback_{item}")

    required_fields = set(observability.get("required_fields") or [])
    for item in [
        "run_id",
        "build_id",
        "source_chain",
        "runtime_invocation_flags",
        "write_boundary_flags",
        "priority_trace",
        "ownership_trace",
        "interruption_trace",
        "arbitration_trace",
        "speech_handoff_trace",
        "error_trace",
        "abort_trace",
        "summary_metrics",
    ]:
        ok(item in required_fields, f"observability_{item}")

    go_conditions = set(go_no_go.get("go_conditions") or [])
    no_go_conditions = set(go_no_go.get("no_go_conditions") or [])
    for item in [
        "trial_definition_generated",
        "trial_input_plan_defined",
        "trial_output_plan_defined",
        "trial_safety_envelope_defined",
        "abort_conditions_defined",
        "rollback_plan_defined",
        "observability_requirements_defined",
        "no_runtime_executed",
        "no_write_executed",
        "boundary_ok_true",
        "verifier_go",
    ]:
        ok(item in go_conditions, f"go_condition_{item}")
    for item in [
        "any_runtime_executed_in_definition_phase",
        "any_write_occurred",
        "any_forbidden_module_marked_as_allowed",
        "abort_conditions_missing",
        "rollback_plan_missing",
        "observability_plan_missing",
        "missing_source_chain",
        "unclear_distinction_between_definition_and_execution",
        "external_api_allowed",
        "map_api_allowed",
        "worldmodel_or_memory_write_allowed",
    ]:
        ok(item in no_go_conditions, f"no_go_condition_{item}")

    ok(future_contract.get("trial_mode") == "DEFINITION_ONLY", "future_contract_trial_mode")
    ok(
        future_contract.get("future_trial_mode") == "FUTURE_CONTROLLED_TRIAL",
        "future_contract_future_trial_mode",
    )
    future_chain = future_contract.get("future_allowed_chain") or []
    for item in [
        "controlled_sample_input_or_stub_frame",
        "basic_navigation_or_ocr_or_safety_candidate_generation",
        "safety_task_arbitration",
        "speech_candidate_generation",
        "speech_gate_shadow",
        "vop_shadow_or_controlled_output_placeholder",
        "structured_logging_and_boundary_check",
    ]:
        ok(item in future_chain, f"future_chain_{item}")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        for flag in [
            "runtime_trial_executed",
            "runtime_camera_invoked",
            "runtime_microphone_invoked",
            "runtime_asr_invoked",
            "runtime_voiceprint_invoked",
            "runtime_face_recognition_invoked",
            "runtime_tts_invoked",
            "runtime_tts_stopped",
            "speech_gate_runtime_invoked",
            "vop_runtime_invoked",
            "map_api_invoked",
            "gps_runtime_invoked",
            "ocr_provider_invoked",
            "detector_invoked",
            "segmentation_invoked",
            "tracking_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "route_modified",
            "memory_written",
            "world_model_written",
            "scene_delta_generated",
            "fact_written",
            "benchmark_accuracy_updated",
            "runtime_routing_changed",
        ]:
            ok(report.get(flag) is False, f"{report_key}_{flag}")
        ok(report.get("boundary_ok") is True, f"{report_key}_boundary_ok")
        ok(report.get("violations") == [], f"{report_key}_violations")
        ok(report.get("fact_status") == "not_fact", f"{report_key}_fact_status")
        ok(report.get("write_allowed") is False, f"{report_key}_write_allowed")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Trial-Definition-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
