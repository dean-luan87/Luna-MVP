#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Basic Navigation Guidance Loop Stabilization Test v1."""

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
        "stabilization_policy": "stabilization_policy.json",
        "stabilization_scenarios": "stabilization_scenarios.json",
        "stabilization_decision_candidates": "stabilization_decision_candidates.json",
        "baseline_vs_task_matrix": "baseline_vs_task_matrix.json",
        "safety_vs_navigation_matrix": "safety_vs_navigation_matrix.json",
        "safety_vs_ocr_matrix": "safety_vs_ocr_matrix.json",
        "voice_ownership_vs_interruption_matrix": "voice_ownership_vs_interruption_matrix.json",
        "speech_priority_vs_interruption_matrix": "speech_priority_vs_interruption_matrix.json",
        "freshness_repeat_resume_matrix": "freshness_repeat_resume_matrix.json",
        "context_preservation_matrix": "context_preservation_matrix.json",
        "handoff_boundary_matrix": "handoff_boundary_matrix.json",
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
            "phase": "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    scenarios = data["stabilization_scenarios"].get("rows") or []
    decisions = data["stabilization_decision_candidates"].get("candidates") or []
    policy = data["stabilization_policy"]

    scenario_by_key = {row.get("scenario_key"): row for row in scenarios}
    decision_by_key = {row.get("scenario_key"): row for row in decisions}
    scenario_types = {row.get("scenario_type") for row in scenarios}

    ok(summary.get("stabilization_scope") == "basic_navigation_guidance_loop_stabilization_test_only", "scope")
    ok(summary.get("basic_navigation_loop_input_loaded") is True, "basic_navigation_loop_input_loaded")
    ok(summary.get("safety_task_arbitration_input_loaded") is True, "safety_task_arbitration_input_loaded")
    ok(
        summary.get("voice_command_ownership_gate_input_loaded") is True,
        "voice_command_ownership_gate_input_loaded",
    )
    ok(
        summary.get("voice_interruption_governance_input_loaded") is True,
        "voice_interruption_governance_input_loaded",
    )
    ok(summary.get("stabilization_policy_defined") is True, "stabilization_policy_defined")
    ok((summary.get("stabilization_scenario_count") or 0) >= 20, "stabilization_scenario_count")
    ok(
        (summary.get("stabilization_decision_candidate_count") or 0) >= 20,
        "stabilization_decision_candidate_count",
    )
    ok(summary.get("baseline_vs_task_matrix_defined") is True, "baseline_vs_task_matrix_defined")
    ok(summary.get("safety_vs_navigation_matrix_defined") is True, "safety_vs_navigation_matrix_defined")
    ok(summary.get("safety_vs_ocr_matrix_defined") is True, "safety_vs_ocr_matrix_defined")
    ok(
        summary.get("voice_ownership_vs_interruption_matrix_defined") is True,
        "voice_ownership_vs_interruption_matrix_defined",
    )
    ok(
        summary.get("speech_priority_vs_interruption_matrix_defined") is True,
        "speech_priority_vs_interruption_matrix_defined",
    )
    ok(
        summary.get("freshness_repeat_resume_matrix_defined") is True,
        "freshness_repeat_resume_matrix_defined",
    )
    ok(summary.get("context_preservation_matrix_defined") is True, "context_preservation_matrix_defined")
    ok(summary.get("handoff_boundary_matrix_defined") is True, "handoff_boundary_matrix_defined")

    for flag in [
        "runtime_camera_invoked",
        "runtime_asr_invoked",
        "runtime_audio_recorded",
        "runtime_voiceprint_invoked",
        "runtime_face_recognition_invoked",
        "runtime_tts_stopped",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
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
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(
        summary.get("final_decision")
        == "BASIC_NAVIGATION_GUIDANCE_LOOP_STABILIZATION_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_TRIAL",
        "summary_final_decision",
    )

    ok(len(scenarios) >= 20, "scenario_rows_len")
    ok(len(decisions) >= 20, "decision_rows_len")
    ok("baseline_safety_only" in scenario_types, "scenario_type_baseline_safety_only")
    ok("task_navigation_guidance" in scenario_types, "scenario_type_task_navigation_guidance")
    ok(
        "task_navigation_with_safety_conflict" in scenario_types,
        "scenario_type_task_navigation_with_safety_conflict",
    )
    ok(
        "ocr_guidance_with_safety_conflict" in scenario_types,
        "scenario_type_ocr_guidance_with_safety_conflict",
    )
    ok("user_question_during_navigation" in scenario_types, "scenario_type_user_question_during_navigation")
    ok("user_interruption_during_speech" in scenario_types, "scenario_type_user_interruption_during_speech")
    ok("non_owner_interruption_attempt" in scenario_types, "scenario_type_non_owner_interruption_attempt")
    ok("phone_call_false_interruption" in scenario_types, "scenario_type_phone_call_false_interruption")
    ok(
        "human_conversation_false_interruption" in scenario_types,
        "scenario_type_human_conversation_false_interruption",
    )
    ok("emergency_user_interruption" in scenario_types, "scenario_type_emergency_user_interruption")
    ok("repeat_stale_safety_speech" in scenario_types, "scenario_type_repeat_stale_safety_speech")
    ok("resume_paused_navigation" in scenario_types, "scenario_type_resume_paused_navigation")
    ok("cancel_task_during_safety_active" in scenario_types, "scenario_type_cancel_task_during_safety_active")
    ok("correction_during_ocr_guidance" in scenario_types, "scenario_type_correction_during_ocr_guidance")
    ok("new_task_during_navigation" in scenario_types, "scenario_type_new_task_during_navigation")
    ok(
        "pending_confirmation_preservation" in scenario_types,
        "scenario_type_pending_confirmation_preservation",
    )

    required_keys = [
        "baseline_p0_safety_no_task",
        "baseline_low_risk_prompt_no_task",
        "task_navigation_p2_candidate",
        "task_navigation_suppressed_by_safety",
        "ocr_guidance_delayed_by_safety",
        "owner_repeat_during_navigation",
        "repeat_stale_p0_safety",
        "owner_stop_p4_explanation",
        "owner_stop_blocked_on_p0_safety",
        "owner_emergency_interrupt",
        "non_owner_interruption_blocked",
        "phone_call_false_interruption",
        "human_conversation_false_interruption",
        "media_playback_false_interruption",
        "public_announcement_false_interruption",
        "correction_during_ocr_guidance",
        "new_task_during_navigation",
        "cancel_task_during_safety_active",
        "resume_paused_navigation",
        "resume_paused_ocr_guidance",
        "human_assistance_delayed_by_safety",
        "clarification_suppressed_by_safety",
        "task_context_preservation_after_interruption",
        "pending_confirmation_preserved_after_safety_interrupt",
    ]
    for key in required_keys:
        ok(key in scenario_by_key, f"scenario_key_{key}")
        ok(key in decision_by_key, f"decision_key_{key}")

    ok(
        policy.get("baseline_loop_policy", {}).get("baseline_safety_loop_allowed_without_task") is True,
        "policy_baseline_without_task",
    )
    ok(
        policy.get("baseline_loop_policy", {}).get("baseline_safety_must_not_generate_task_goal") is True,
        "policy_baseline_no_task_goal",
    )
    ok(
        policy.get("task_driven_loop_policy", {}).get("task_driven_loop_requires_task_context") is True,
        "policy_task_requires_context",
    )
    ok(
        policy.get("safety_task_conflict_policy", {}).get("P0_P1_safety_preempts_lower_priority_task_guidance")
        is True,
        "policy_safety_preempts",
    )
    ok(
        policy.get("ocr_navigation_conflict_policy", {}).get("safety_active_delays_non_safety_ocr_guidance")
        is True,
        "policy_ocr_delay",
    )
    ok(
        policy.get("voice_interruption_conflict_policy", {}).get("ordinary_interruption_cannot_cancel_P0_safety_warning")
        is True,
        "policy_p0_stop_blocked",
    )
    ok(
        policy.get("ownership_gate_conflict_policy", {}).get(
            "non_owner_phone_human_conversation_media_public_announcement_block_ordinary_interruption"
        )
        is True,
        "policy_ownership_block",
    )
    ok(
        policy.get("speech_priority_stabilization_policy", {}).get(
            "P2_pause_resume_require_route_and_stc_freshness"
        )
        is True,
        "policy_p2_resume",
    )
    ok(
        policy.get("speech_priority_stabilization_policy", {}).get(
            "P3_resume_requires_frame_region_freshness"
        )
        is True,
        "policy_p3_resume",
    )
    ok(
        policy.get("context_preservation_policy", {}).get("task_context_preserved_after_interruption") is True,
        "policy_task_context_preserved",
    )
    ok(
        policy.get("context_preservation_policy", {}).get("pending_confirmation_preserved_after_interruption")
        is True,
        "policy_pending_confirmation_preserved",
    )
    ok(
        policy.get("freshness_stabilization_policy", {}).get("repeat_requires_freshness_check") is True,
        "policy_repeat_freshness",
    )
    ok(
        policy.get("freshness_stabilization_policy", {}).get("stale_safety_repeat_must_not_be_current_fact")
        is True,
        "policy_stale_safety_not_fact",
    )
    ok(
        policy.get("handoff_only_policy", {}).get("speech_gate_handoff_candidate_only") is True,
        "policy_handoff_speech_gate",
    )

    d = decision_by_key["baseline_p0_safety_no_task"]
    ok(d.get("final_stabilization_status") == "STABLE_PASS", "decision_baseline_pass")
    ok(d.get("speech_gate_handoff_required") is True, "decision_baseline_handoff")

    d = decision_by_key["task_navigation_p2_candidate"]
    ok(d.get("final_stabilization_status") == "STABLE_PASS", "decision_task_nav_pass")
    ok(d.get("preserved_contexts", {}).get("task_context") is True, "decision_task_nav_task_context")

    d = decision_by_key["task_navigation_suppressed_by_safety"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_SAFETY_PRIORITY", "decision_nav_safety_block")
    ok("arb_trace_task_loop_007" in (d.get("suppressed_candidates") or []), "decision_nav_suppressed")

    d = decision_by_key["ocr_guidance_delayed_by_safety"]
    ok(d.get("final_stabilization_status") == "STABLE_WITH_DELAY", "decision_ocr_delay_status")
    ok("arb_trace_task_loop_009" in (d.get("delayed_candidates") or []), "decision_ocr_delay_candidate")

    d = decision_by_key["owner_repeat_during_navigation"]
    ok("repeat_freshness_check" in (d.get("freshness_checks") or []), "decision_repeat_freshness")
    ok(d.get("final_stabilization_status") == "STABLE_PASS", "decision_repeat_pass")

    d = decision_by_key["repeat_stale_p0_safety"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_STALENESS", "decision_stale_block")
    ok(
        "stale_safety_rewrite_check" in (d.get("freshness_checks") or []),
        "decision_stale_rewrite_check",
    )

    d = decision_by_key["owner_stop_blocked_on_p0_safety"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_SAFETY_PRIORITY", "decision_p0_blocked")

    d = decision_by_key["owner_emergency_interrupt"]
    ok(
        d.get("final_stabilization_status") == "STABLE_WITH_SAFETY_ESCALATION_CANDIDATE",
        "decision_emergency_escalation",
    )
    ok(d.get("speech_gate_handoff_required") is False, "decision_emergency_no_direct_gate")

    d = decision_by_key["non_owner_interruption_blocked"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_OWNERSHIP_GATE", "decision_non_owner_blocked")

    d = decision_by_key["phone_call_false_interruption"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_OWNERSHIP_GATE", "decision_phone_blocked")

    d = decision_by_key["human_conversation_false_interruption"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_OWNERSHIP_GATE", "decision_human_blocked")

    d = decision_by_key["media_playback_false_interruption"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_OWNERSHIP_GATE", "decision_media_blocked")

    d = decision_by_key["public_announcement_false_interruption"]
    ok(d.get("final_stabilization_status") == "BLOCKED_BY_OWNERSHIP_GATE", "decision_public_blocked")

    d = decision_by_key["correction_during_ocr_guidance"]
    ok(d.get("selected_output_candidate") == "idc_case_04", "decision_correction_selected")
    ok(d.get("speech_gate_handoff_required") is False, "decision_correction_no_gate")

    d = decision_by_key["new_task_during_navigation"]
    ok(d.get("final_stabilization_status") == "STABLE_WITH_DELAY", "decision_new_task_delay")
    ok(d.get("preserved_contexts", {}).get("task_context") is True, "decision_new_task_preserve_task")

    d = decision_by_key["cancel_task_during_safety_active"]
    ok(
        d.get("final_stabilization_status") == "STABLE_WITH_CONFIRMATION_REQUIRED",
        "decision_cancel_confirmation",
    )
    ok(d.get("speech_gate_handoff_required") is False, "decision_cancel_no_gate")

    d = decision_by_key["resume_paused_navigation"]
    ok(d.get("final_stabilization_status") == "NEEDS_FUTURE_RUNTIME_CHECK", "decision_resume_nav_future")
    ok(
        "route_freshness_check" in (d.get("freshness_checks") or []),
        "decision_resume_nav_route_check",
    )

    d = decision_by_key["resume_paused_ocr_guidance"]
    ok(d.get("final_stabilization_status") == "NEEDS_FUTURE_RUNTIME_CHECK", "decision_resume_ocr_future")
    ok(
        "region_freshness_check" in (d.get("freshness_checks") or []),
        "decision_resume_ocr_region_check",
    )

    d = decision_by_key["human_assistance_delayed_by_safety"]
    ok(d.get("final_stabilization_status") == "STABLE_WITH_DELAY", "decision_human_delay")

    d = decision_by_key["clarification_suppressed_by_safety"]
    ok(d.get("final_stabilization_status") == "STABLE_WITH_SUPPRESSION", "decision_clarify_suppressed")

    d = decision_by_key["task_context_preservation_after_interruption"]
    ok(d.get("preserved_contexts", {}).get("task_context") is True, "decision_task_context_preserved")

    d = decision_by_key["pending_confirmation_preserved_after_safety_interrupt"]
    ok(
        d.get("preserved_contexts", {}).get("pending_confirmation") is True,
        "decision_pending_confirmation_preserved",
    )

    for matrix_key in [
        "baseline_vs_task_matrix",
        "safety_vs_navigation_matrix",
        "safety_vs_ocr_matrix",
        "voice_ownership_vs_interruption_matrix",
        "speech_priority_vs_interruption_matrix",
        "freshness_repeat_resume_matrix",
        "context_preservation_matrix",
        "handoff_boundary_matrix",
    ]:
        matrix = data[matrix_key]
        ok((matrix.get("row_count") or 0) > 0, f"{matrix_key}_rows")
        ok(isinstance(matrix.get("rows"), list), f"{matrix_key}_list")

    handoff_rows = data["handoff_boundary_matrix"].get("rows") or []
    handoff_modules = {row.get("target_module") for row in handoff_rows}
    for module in [
        "speech_gate",
        "voice_output_plane",
        "task_manager",
        "stc",
        "ocr_activation",
        "navigation_guidance",
        "safety_task_arbitration",
    ]:
        ok(module in handoff_modules, f"handoff_module_{module}")
    ok(all(row.get("invoked_now") is False for row in handoff_rows), "handoff_invoked_now_false")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        for flag in [
            "runtime_camera_invoked",
            "runtime_asr_invoked",
            "runtime_audio_recorded",
            "runtime_voiceprint_invoked",
            "runtime_face_recognition_invoked",
            "runtime_tts_stopped",
            "speech_gate_invoked",
            "vop_invoked",
            "tts_invoked",
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

    ok(all(row.get("source_chain") == "basic_navigation_guidance_loop_stabilization_test_v1" for row in scenarios), "scenario_source_chain")
    ok(all(row.get("source_chain") == "basic_navigation_guidance_loop_stabilization_test_v1" for row in decisions), "decision_source_chain")
    ok(
        all((row.get("no_runtime_boundary") or {}).get("boundary_ok") is True for row in decisions),
        "decision_no_runtime_ok",
    )
    ok(
        all((row.get("no_write_boundary") or {}).get("boundary_ok") is True for row in decisions),
        "decision_no_write_ok",
    )
    ok(
        all(row.get("fact_status") == "not_fact" for row in scenarios + decisions),
        "all_fact_status_not_fact",
    )
    ok(all(row.get("write_allowed") is False for row in scenarios + decisions), "all_write_allowed_false")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Basic-Navigation-Guidance-Loop-Stabilization-Test-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
