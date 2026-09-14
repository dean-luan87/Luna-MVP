#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Controlled Shadow Trial v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

MIN_CHECKS = 80


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
        "controlled_trial_input_trace": "controlled_trial_input_trace.json",
        "shadow_execution_steps": "shadow_execution_steps.json",
        "shadow_candidate_trace": "shadow_candidate_trace.json",
        "speech_gate_shadow_decisions": "speech_gate_shadow_decisions.json",
        "vop_shadow_events": "vop_shadow_events.json",
        "controlled_shadow_abort_checks": "controlled_shadow_abort_checks.json",
        "observability_trace": "observability_trace.json",
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
            "phase": "Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    input_cases = data["controlled_trial_input_trace"].get("rows") or []
    steps = data["shadow_execution_steps"].get("rows") or []
    traces = data["shadow_candidate_trace"].get("rows") or []
    speech_gate = data["speech_gate_shadow_decisions"].get("rows") or []
    vop_events = data["vop_shadow_events"].get("rows") or []
    abort_checks = data["controlled_shadow_abort_checks"].get("rows") or []
    observability = data["observability_trace"]

    input_case_by_key = {row.get("input_case_key"): row for row in input_cases}
    trace_by_case = {row.get("input_case_id"): row for row in traces}
    gate_by_case = {row.get("input_case_id"): row for row in speech_gate}
    vop_by_case = {row.get("input_case_id"): row for row in vop_events}
    abort_by_case = {row.get("input_case_id"): row for row in abort_checks}

    ok(summary.get("trial_scope") == "minimal_runtime_integration_controlled_shadow_trial_only", "trial_scope")
    ok(summary.get("trial_mode") == "CONTROLLED_SHADOW_TRIAL", "trial_mode")
    ok(summary.get("trial_definition_input_loaded") is True, "trial_definition_input_loaded")
    ok(summary.get("stabilization_input_loaded") is True, "stabilization_input_loaded")
    ok(summary.get("basic_navigation_loop_input_loaded") is True, "basic_navigation_loop_input_loaded")
    ok(summary.get("safety_task_arbitration_input_loaded") is True, "safety_task_arbitration_input_loaded")
    ok(summary.get("ownership_gate_input_loaded") is True, "ownership_gate_input_loaded")
    ok(summary.get("interruption_governance_input_loaded") is True, "interruption_governance_input_loaded")
    ok((summary.get("controlled_input_case_count") or 0) >= 8, "controlled_input_case_count")
    ok((summary.get("shadow_execution_step_count") or 0) >= 8, "shadow_execution_step_count")
    ok((summary.get("shadow_candidate_trace_count") or 0) >= 8, "shadow_candidate_trace_count")
    ok((summary.get("speech_gate_shadow_decision_count") or 0) >= 8, "speech_gate_shadow_decision_count")
    ok((summary.get("vop_shadow_event_count") or 0) >= 8, "vop_shadow_event_count")
    ok((summary.get("abort_check_count") or 0) >= 8, "abort_check_count")
    ok(
        summary.get("final_decision")
        == "MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_READY_FOR_POST_SHADOW_REVIEW",
        "final_decision",
    )

    for flag in [
        "runtime_camera_invoked",
        "runtime_microphone_invoked",
        "runtime_asr_invoked",
        "runtime_tts_invoked",
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

    ok(len(input_cases) >= 8, "input_case_rows")
    ok(len(steps) >= 8, "shadow_steps_rows")
    ok(len(traces) >= 8, "shadow_trace_rows")
    ok(len(speech_gate) >= 8, "speech_gate_rows")
    ok(len(vop_events) >= 8, "vop_rows")
    ok(len(abort_checks) >= 8, "abort_rows")

    for case_key in [
        "baseline_safety_only",
        "navigation_guidance_only",
        "safety_overrides_navigation",
        "ocr_guidance_delayed_by_safety",
        "owner_confirmed_repeat_request",
        "non_owner_interruption_blocked",
        "emergency_user_interruption_candidate",
        "stale_safety_repeat_blocked",
    ]:
        ok(case_key in input_case_by_key, f"case_key_{case_key}")

    step_names = {row.get("step_name") for row in steps}
    for step_name in [
        "load_controlled_input",
        "generate_safety_candidate",
        "generate_task_navigation_candidate",
        "generate_ocr_guidance_candidate",
        "apply_ownership_gate_shadow",
        "apply_interruption_governance_shadow",
        "apply_safety_task_arbitration_shadow",
        "generate_speech_request_candidate",
        "apply_speech_gate_shadow",
        "generate_vop_shadow_event",
        "run_abort_checks",
        "generate_boundary_reports",
        "generate_final_shadow_decision",
    ]:
        ok(step_name in step_names, f"step_{step_name}")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        for flag in [
            "runtime_camera_invoked",
            "runtime_microphone_invoked",
            "runtime_asr_invoked",
            "runtime_tts_invoked",
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

    baseline_case = input_case_by_key["baseline_safety_only"]
    ok(baseline_case.get("simulated_task_context") is None, "baseline_case_no_task")
    baseline_trace = trace_by_case[baseline_case["input_case_id"]]
    ok(baseline_trace.get("safety_candidate") == "baseline_loop_001", "baseline_trace_safety_candidate")
    ok(baseline_trace.get("final_case_status") == "SHADOW_PASS", "baseline_trace_status")

    nav_case = input_case_by_key["navigation_guidance_only"]
    nav_trace = trace_by_case[nav_case["input_case_id"]]
    ok(nav_trace.get("task_navigation_candidate") == "task_loop_007", "nav_trace_candidate")
    ok(nav_trace.get("task_context_preserved") is True, "nav_trace_task_context")
    ok(nav_trace.get("final_case_status") == "SHADOW_PASS", "nav_trace_status")

    safety_override_case = input_case_by_key["safety_overrides_navigation"]
    safety_override_trace = trace_by_case[safety_override_case["input_case_id"]]
    ok(
        safety_override_trace.get("final_case_status") == "SHADOW_PASS_WITH_SUPPRESSION",
        "safety_override_status",
    )
    safety_override_gate = gate_by_case[safety_override_case["input_case_id"]]
    ok(safety_override_gate.get("output_allowed_shadow") is True, "safety_override_gate_allowed")

    ocr_delay_case = input_case_by_key["ocr_guidance_delayed_by_safety"]
    ocr_delay_trace = trace_by_case[ocr_delay_case["input_case_id"]]
    ocr_delay_gate = gate_by_case[ocr_delay_case["input_case_id"]]
    ok(ocr_delay_trace.get("ocr_guidance_candidate") == "task_loop_009", "ocr_delay_candidate")
    ok(ocr_delay_gate.get("delayed_by_safety") is True, "ocr_delay_gate_delayed")
    ok(ocr_delay_trace.get("final_case_status") == "SHADOW_PASS_WITH_DELAY", "ocr_delay_status")

    repeat_case = input_case_by_key["owner_confirmed_repeat_request"]
    repeat_trace = trace_by_case[repeat_case["input_case_id"]]
    repeat_gate = gate_by_case[repeat_case["input_case_id"]]
    ok(repeat_trace.get("ownership_gate_shadow_result") == "ogd_case_02", "repeat_ownership_ref")
    ok(repeat_trace.get("interruption_shadow_result") == "idc_case_02", "repeat_interruption_ref")
    ok(repeat_gate.get("output_allowed_shadow") is True, "repeat_output_allowed")
    ok(repeat_trace.get("task_context_preserved") is True, "repeat_task_context")
    ok(repeat_trace.get("pending_confirmation_preserved") is True, "repeat_pending_confirmation")

    non_owner_case = input_case_by_key["non_owner_interruption_blocked"]
    non_owner_trace = trace_by_case[non_owner_case["input_case_id"]]
    non_owner_gate = gate_by_case[non_owner_case["input_case_id"]]
    ok(non_owner_trace.get("ownership_gate_shadow_result") == "ogd_case_06", "non_owner_ownership_ref")
    ok(non_owner_trace.get("interruption_shadow_result") == "idc_case_06", "non_owner_interruption_ref")
    ok(non_owner_gate.get("suppressed_by_ownership") is True, "non_owner_suppressed_by_ownership")
    ok(non_owner_gate.get("output_allowed_shadow") is False, "non_owner_output_blocked")

    emergency_case = input_case_by_key["emergency_user_interruption_candidate"]
    emergency_trace = trace_by_case[emergency_case["input_case_id"]]
    emergency_gate = gate_by_case[emergency_case["input_case_id"]]
    ok(emergency_trace.get("interruption_shadow_result") == "idc_case_05", "emergency_interruption_ref")
    ok(emergency_trace.get("task_context_preserved") is True, "emergency_task_context_preserved")
    ok(emergency_trace.get("pending_confirmation_preserved") is True, "emergency_pending_preserved")
    ok(emergency_gate.get("output_allowed_shadow") is False, "emergency_no_direct_output")

    stale_case = input_case_by_key["stale_safety_repeat_blocked"]
    stale_trace = trace_by_case[stale_case["input_case_id"]]
    stale_gate = gate_by_case[stale_case["input_case_id"]]
    ok(stale_trace.get("interruption_shadow_result") == "idc_case_24", "stale_interruption_ref")
    ok(stale_gate.get("stale_blocked") is True, "stale_gate_blocked")
    ok(stale_gate.get("output_allowed_shadow") is False, "stale_output_blocked")

    # Governance checks
    ok(all(row.get("task_context_preserved") is True for row in traces if row.get("task_navigation_candidate") or row.get("ocr_guidance_candidate") or row.get("ownership_gate_shadow_result")), "all_task_context_preserved_when_relevant")
    ok(all(row.get("pending_confirmation_preserved") is True for row in traces if row.get("ownership_gate_shadow_result") or row.get("interruption_shadow_result")), "all_pending_confirmation_preserved_when_present")
    ok(all(row.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1" for row in traces), "trace_source_chain")
    ok(all(row.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1" for row in speech_gate), "gate_source_chain")
    ok(all(row.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1" for row in vop_events), "vop_source_chain")
    ok(all(row.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1" for row in abort_checks), "abort_source_chain")
    ok(all(row.get("abort_triggered") is False for row in abort_checks), "abort_not_triggered")
    ok(all(row.get("forbidden_runtime_invoked") is False for row in abort_checks), "abort_no_forbidden_runtime")
    ok(all(row.get("forbidden_write_occurred") is False for row in abort_checks), "abort_no_forbidden_write")
    ok(all(row.get("missing_source_chain") is False for row in abort_checks), "abort_no_missing_source_chain")
    ok(all(row.get("task_state_committed") is False for row in abort_checks), "abort_no_task_commit")
    ok(all(row.get("navigation_action_triggered") is False for row in abort_checks), "abort_no_navigation_action")
    ok(all(row.get("map_api_invoked") is False for row in abort_checks), "abort_no_map_api")
    ok(all(row.get("gps_runtime_invoked") is False for row in abort_checks), "abort_no_gps")
    ok(all(row.get("real_ocr_provider_invoked") is False for row in abort_checks), "abort_no_ocr_provider")
    ok(all(row.get("real_camera_invoked") is False for row in abort_checks), "abort_no_camera")
    ok(all(row.get("real_microphone_invoked") is False for row in abort_checks), "abort_no_microphone")
    ok(all(row.get("real_tts_invoked") is False for row in abort_checks), "abort_no_tts")
    ok(all(row.get("real_speech_gate_runtime_invoked") is False for row in abort_checks), "abort_no_speech_gate_runtime")
    ok(all(row.get("real_vop_runtime_invoked") is False for row in abort_checks), "abort_no_vop_runtime")
    ok(all(row.get("world_model_written") is False for row in abort_checks), "abort_no_world_model")
    ok(all(row.get("memory_written") is False for row in abort_checks), "abort_no_memory")
    ok(all(row.get("scene_delta_generated") is False for row in abort_checks), "abort_no_scene_delta")
    ok(all(row.get("stale_safety_speech_treated_as_current_fact") is False for row in abort_checks), "abort_no_stale_as_current_fact")
    ok(all(row.get("non_owner_voice_triggers_task_control") is False for row in abort_checks), "abort_no_non_owner_task_control")
    ok(all(row.get("p0_safety_speech_cancelled_by_ordinary_stop") is False for row in abort_checks), "abort_no_p0_cancel")
    ok(all(row.get("violations") == [] for row in abort_checks), "abort_violations_empty")

    ok(all(row.get("runtime_invoked") is False for row in steps), "steps_runtime_not_invoked")
    ok(all(row.get("write_occurred") is False for row in steps), "steps_write_not_occurred")
    ok(all(row.get("shadow_only") is True for row in steps), "steps_shadow_only")
    ok(all(row.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1" for row in steps), "steps_source_chain")

    ok(all(row.get("runtime_speech_gate_invoked") is False for row in speech_gate), "speech_gate_runtime_false")
    ok(all(row.get("tts_invoked") is False for row in vop_events), "vop_tts_false")
    ok(all(row.get("audio_output_invoked") is False for row in vop_events), "vop_audio_false")
    ok(all(row.get("runtime_vop_invoked") is False for row in vop_events), "vop_runtime_false")

    run = observability.get("run") or {}
    ok(run.get("run_id") == "csrun_mrit_v1_001", "observability_run_id")
    ok(run.get("trial_mode") == "CONTROLLED_SHADOW_TRIAL", "observability_trial_mode")
    ok(run.get("source_chain") == "minimal_runtime_integration_controlled_shadow_trial_v1", "observability_source_chain")
    ok(run.get("final_shadow_status") == "SHADOW_PASS_WITH_SUPPRESSION", "observability_final_shadow_status")
    summary_metrics = observability.get("summary_metrics") or {}
    ok(summary_metrics.get("source_chain_complete") is True, "observability_source_chain_complete")
    ok((summary_metrics.get("controlled_input_case_count") or 0) >= 8, "observability_case_count")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Controlled-Shadow-Trial-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
