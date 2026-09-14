#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Text-Only Controlled Output Trial v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

MIN_CHECKS = 80
ALLOWED_OUTPUT_MODES = {
    "TEXT_ONLY",
    "STRUCTURED_LOG_ONLY",
    "DRY_SPEECH_PREVIEW",
    "SHADOW_COMPATIBLE_TEXT_OUTPUT",
}


def _require_abs(path_str: str, label: str) -> Path:
    p = Path(path_str).expanduser()
    if not p.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {path_str}")
    return p.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _index_by(rows: List[Dict[str, Any]], key: str) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        value = row.get(key)
        if value:
            out[value] = row
    return out


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
        "controlled_output_trial_cases": "controlled_output_trial_cases.json",
        "speech_gate_controlled_decisions": "speech_gate_controlled_decisions.json",
        "controlled_text_output_events": "controlled_text_output_events.json",
        "vop_controlled_event_candidates": "vop_controlled_event_candidates.json",
        "text_only_output_abort_checks": "text_only_output_abort_checks.json",
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
            "phase": "Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    case_payload = data["controlled_output_trial_cases"]
    decision_payload = data["speech_gate_controlled_decisions"]
    event_payload = data["controlled_text_output_events"]
    vop_payload = data["vop_controlled_event_candidates"]
    abort_payload = data["text_only_output_abort_checks"]
    observability = data["observability_trace"]

    case_rows = case_payload.get("rows") or []
    decision_rows = decision_payload.get("rows") or []
    event_rows = event_payload.get("rows") or []
    vop_rows = vop_payload.get("rows") or []
    abort_rows = abort_payload.get("rows") or []
    observability_case_rows = observability.get("case_traces") or []

    cases_by_key = _index_by(case_rows, "case_key")
    decisions_by_case = _index_by(decision_rows, "trial_case_id")
    events_by_case = _index_by(event_rows, "trial_case_id")
    vop_by_case = _index_by(vop_rows, "trial_case_id")
    aborts_by_case = _index_by(abort_rows, "trial_case_id")
    obs_by_case = _index_by(observability_case_rows, "trial_case_id")

    ok(
        summary.get("trial_scope") == "minimal_runtime_integration_text_only_controlled_output_trial_only",
        "trial_scope",
    )
    ok(summary.get("text_only_controlled_output_trial_executed") is True, "trial_executed")
    ok(summary.get("controlled_output_definition_input_loaded") is True, "controlled_output_definition_input_loaded")
    ok(summary.get("post_shadow_review_input_loaded") is True, "post_shadow_review_input_loaded")
    ok(summary.get("controlled_shadow_trial_input_loaded") is True, "controlled_shadow_trial_input_loaded")
    ok(summary.get("trial_case_count", 0) >= 8, "trial_case_count")
    ok(summary.get("controlled_text_output_event_count", 0) >= 8, "controlled_text_output_event_count")
    ok(summary.get("speech_gate_controlled_decision_count", 0) >= 8, "speech_gate_controlled_decision_count")
    ok(summary.get("vop_controlled_event_candidate_count", 0) >= 8, "vop_controlled_event_candidate_count")
    ok(summary.get("abort_check_count", 0) >= 8, "abort_check_count")
    ok(summary.get("output_mode_limited_to_text_only") is True, "output_mode_limited_to_text_only")

    for flag in [
        "real_audio_output_invoked",
        "runtime_tts_invoked",
        "runtime_audio_output_invoked",
        "speech_gate_runtime_invoked",
        "vop_runtime_invoked",
        "runtime_camera_invoked",
        "runtime_microphone_invoked",
        "runtime_asr_invoked",
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
        "external_tts_api_invoked",
        "audio_device_invoked",
    ]:
        ok(summary.get(flag) is False, f"summary_{flag}")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(summary.get("violations") == [], "summary_violations")
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")
    ok(
        summary.get("final_decision") == "TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_READY_FOR_POST_TRIAL_REVIEW",
        "summary_final_decision",
    )
    ok(
        summary.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001",
        "summary_next_phase",
    )
    ok(summary.get("must_not_recommend_real_tts") is True, "must_not_recommend_real_tts")
    ok(summary.get("must_not_recommend_live_audio") is True, "must_not_recommend_live_audio")
    ok(summary.get("must_not_recommend_camera_enablement") is True, "must_not_recommend_camera_enablement")
    ok(summary.get("must_not_recommend_map_api_enablement") is True, "must_not_recommend_map_api_enablement")
    ok(
        summary.get("must_not_recommend_memory_or_worldmodel_write") is True,
        "must_not_recommend_memory_or_worldmodel_write",
    )

    ok(case_payload.get("trial_case_count") == len(case_rows), "case_payload_count_matches")
    ok(decision_payload.get("speech_gate_controlled_decision_count") == len(decision_rows), "decision_payload_count_matches")
    ok(event_payload.get("controlled_text_output_event_count") == len(event_rows), "event_payload_count_matches")
    ok(vop_payload.get("vop_controlled_event_candidate_count") == len(vop_rows), "vop_payload_count_matches")
    ok(abort_payload.get("abort_check_count") == len(abort_rows), "abort_payload_count_matches")
    ok(len(case_rows) >= 8, "case_rows_count")
    ok(len(decision_rows) >= 8, "decision_rows_count")
    ok(len(event_rows) >= 8, "event_rows_count")
    ok(len(vop_rows) >= 8, "vop_rows_count")
    ok(len(abort_rows) >= 8, "abort_rows_count")
    ok(len(observability_case_rows) >= 8, "observability_case_rows_count")

    required_case_keys = {
        "p0_safety_text_only_allowed",
        "p2_navigation_text_only_allowed",
        "p3_ocr_guidance_delayed_by_safety",
        "owner_confirmed_repeat_preview",
        "stale_p0_historical_only",
        "non_owner_interruption_suppressed",
        "emergency_safety_observation_preview",
        "cancel_with_pending_confirmation",
    }
    for case_key in required_case_keys:
        ok(case_key in cases_by_key, f"case_exists_{case_key}")

    case_01 = cases_by_key.get("p0_safety_text_only_allowed", {})
    case_02 = cases_by_key.get("p2_navigation_text_only_allowed", {})
    case_03 = cases_by_key.get("p3_ocr_guidance_delayed_by_safety", {})
    case_04 = cases_by_key.get("owner_confirmed_repeat_preview", {})
    case_05 = cases_by_key.get("stale_p0_historical_only", {})
    case_06 = cases_by_key.get("non_owner_interruption_suppressed", {})
    case_07 = cases_by_key.get("emergency_safety_observation_preview", {})
    case_08 = cases_by_key.get("cancel_with_pending_confirmation", {})

    ok(case_01.get("expected_decision") == "ALLOW_TEXT_ONLY", "case01_expected_decision")
    ok(case_02.get("expected_decision") == "ALLOW_TEXT_ONLY", "case02_expected_decision")
    ok(case_03.get("expected_decision") == "DELAY", "case03_expected_decision")
    ok(case_04.get("expected_decision") == "ALLOW_DRY_SPEECH_PREVIEW", "case04_expected_decision")
    ok(case_05.get("expected_decision") == "ALLOW_TEXT_ONLY", "case05_expected_decision")
    ok(case_06.get("expected_decision") == "SUPPRESS", "case06_expected_decision")
    ok(case_07.get("expected_decision") == "ALLOW_DRY_SPEECH_PREVIEW", "case07_expected_decision")
    ok(case_08.get("expected_decision") == "REQUIRE_CONFIRMATION", "case08_expected_decision")

    for row in case_rows:
        case_id = row.get("trial_case_id")
        ok(bool(case_id), f"case_id_present_{case_id}")
        ok(bool(row.get("source_chain")), f"case_source_chain_{case_id}")
        ok(case_id in decisions_by_case, f"decision_exists_{case_id}")
        ok(case_id in events_by_case, f"event_exists_{case_id}")
        ok(case_id in vop_by_case, f"vop_exists_{case_id}")
        ok(case_id in aborts_by_case, f"abort_exists_{case_id}")
        ok(case_id in obs_by_case, f"observability_exists_{case_id}")

    for row in decision_rows:
        case_id = row.get("trial_case_id")
        ok(bool(row.get("controlled_decision_id")), f"decision_id_present_{case_id}")
        ok(bool(row.get("speech_request_candidate_id")), f"decision_speech_request_present_{case_id}")
        ok(bool(row.get("priority")), f"decision_priority_present_{case_id}")
        ok(
            row.get("decision")
            in {
                "ALLOW_TEXT_ONLY",
                "ALLOW_DRY_SPEECH_PREVIEW",
                "DELAY",
                "SUPPRESS",
                "REQUIRE_CONFIRMATION",
                "ABORT_OUTPUT",
            },
            f"decision_enum_{case_id}",
        )
        ok(bool(row.get("decision_reason")), f"decision_reason_present_{case_id}")
        ok(row.get("allowed_output_mode") in ALLOWED_OUTPUT_MODES, f"decision_allowed_output_mode_{case_id}")
        ok(bool(row.get("source_chain")), f"decision_source_chain_{case_id}")

    for row in event_rows:
        case_id = row.get("trial_case_id")
        ok(bool(row.get("output_event_id")), f"event_id_present_{case_id}")
        ok(bool(row.get("source_speech_request_candidate_id")), f"event_source_request_present_{case_id}")
        ok(bool(row.get("source_speech_gate_decision_id")), f"event_source_decision_present_{case_id}")
        ok(row.get("output_mode") in ALLOWED_OUTPUT_MODES, f"event_output_mode_allowed_{case_id}")
        ok(bool(row.get("output_text_ref")), f"event_text_ref_present_{case_id}")
        ok(bool(row.get("output_text_preview")), f"event_text_preview_present_{case_id}")
        ok(bool(row.get("priority")), f"event_priority_present_{case_id}")
        ok(bool(row.get("safety_status")), f"event_safety_status_present_{case_id}")
        ok(bool(row.get("ownership_status")), f"event_ownership_status_present_{case_id}")
        ok(bool(row.get("interruption_status")), f"event_interruption_status_present_{case_id}")
        ok(bool(row.get("freshness_status")), f"event_freshness_status_present_{case_id}")
        ok(row.get("user_visible") is True, f"event_user_visible_{case_id}")
        ok(row.get("user_heard_assumed") is False, f"event_user_heard_not_assumed_{case_id}")
        ok(row.get("audio_output") is False, f"event_audio_output_false_{case_id}")
        ok(row.get("tts_invoked") is False, f"event_tts_false_{case_id}")
        ok(row.get("vop_runtime_invoked") is False, f"event_vop_runtime_false_{case_id}")
        ok(bool(row.get("source_chain")), f"event_source_chain_{case_id}")

    for row in vop_rows:
        case_id = row.get("trial_case_id")
        ok(bool(row.get("vop_controlled_event_id")), f"vop_event_id_present_{case_id}")
        ok(bool(row.get("controlled_decision_id")), f"vop_decision_ref_present_{case_id}")
        ok(row.get("output_mode") in ALLOWED_OUTPUT_MODES, f"vop_output_mode_allowed_{case_id}")
        ok(bool(row.get("output_text_ref")), f"vop_text_ref_present_{case_id}")
        ok(row.get("audio_output_invoked") is False, f"vop_audio_output_false_{case_id}")
        ok(row.get("runtime_vop_invoked") is False, f"vop_runtime_false_{case_id}")
        ok(bool(row.get("source_chain")), f"vop_source_chain_{case_id}")

    for row in abort_rows:
        case_id = row.get("trial_case_id")
        ok(bool(row.get("abort_check_id")), f"abort_id_present_{case_id}")
        ok(row.get("real_tts_invoked") is False, f"abort_real_tts_false_{case_id}")
        ok(row.get("audio_output_invoked") is False, f"abort_audio_output_false_{case_id}")
        ok(row.get("speech_gate_runtime_invoked") is False, f"abort_sg_runtime_false_{case_id}")
        ok(row.get("vop_runtime_invoked") is False, f"abort_vop_runtime_false_{case_id}")
        ok(row.get("output_without_source_chain") is False, f"abort_no_source_chain_violation_{case_id}")
        ok(
            row.get("p0_p1_safety_suppressed_by_lower_priority") is False,
            f"abort_no_p0p1_suppression_{case_id}",
        )
        ok(
            row.get("stale_safety_speech_output_as_current_fact") is False,
            f"abort_no_stale_as_current_{case_id}",
        )
        ok(row.get("non_owner_voice_triggers_output") is False, f"abort_non_owner_no_output_{case_id}")
        ok(row.get("task_state_committed") is False, f"abort_task_commit_false_{case_id}")
        ok(row.get("navigation_action_triggered") is False, f"abort_navigation_false_{case_id}")
        ok(row.get("map_api_invoked") is False, f"abort_map_api_false_{case_id}")
        ok(row.get("memory_written") is False, f"abort_memory_false_{case_id}")
        ok(row.get("world_model_written") is False, f"abort_world_model_false_{case_id}")
        ok(row.get("fact_written") is False, f"abort_fact_false_{case_id}")
        ok(row.get("violations") == [], f"abort_violations_empty_{case_id}")
        ok(row.get("abort_triggered") is False, f"abort_not_triggered_{case_id}")
        ok(bool(row.get("source_chain")), f"abort_source_chain_{case_id}")

    for row in observability_case_rows:
        case_id = row.get("trial_case_id")
        ok(bool(row.get("speech_request_id")), f"obs_speech_request_present_{case_id}")
        ok(bool(row.get("speech_gate_decision_id")), f"obs_decision_present_{case_id}")
        ok(bool(row.get("output_event_id")), f"obs_output_event_present_{case_id}")
        ok(bool(row.get("vop_event_id")), f"obs_vop_event_present_{case_id}")
        ok(row.get("output_mode") in ALLOWED_OUTPUT_MODES, f"obs_output_mode_allowed_{case_id}")
        ok(bool(row.get("priority")), f"obs_priority_present_{case_id}")
        ok(bool(row.get("safety_status")), f"obs_safety_status_present_{case_id}")
        ok(bool(row.get("ownership_status")), f"obs_ownership_status_present_{case_id}")
        ok(bool(row.get("interruption_status")), f"obs_interruption_status_present_{case_id}")
        ok(bool(row.get("freshness_status")), f"obs_freshness_status_present_{case_id}")
        ok(isinstance(row.get("output_length"), int) and row.get("output_length", 0) > 0, f"obs_output_length_{case_id}")
        ok(row.get("output_event_count") == 1, f"obs_output_event_count_{case_id}")
        ok(bool(row.get("final_output_decision")), f"obs_final_output_decision_{case_id}")
        ok(bool(row.get("source_chain")), f"obs_source_chain_{case_id}")

    decision_case_01 = decisions_by_case.get(case_01.get("trial_case_id", ""), {})
    event_case_01 = events_by_case.get(case_01.get("trial_case_id", ""), {})
    decision_case_02 = decisions_by_case.get(case_02.get("trial_case_id", ""), {})
    event_case_02 = events_by_case.get(case_02.get("trial_case_id", ""), {})
    decision_case_03 = decisions_by_case.get(case_03.get("trial_case_id", ""), {})
    event_case_03 = events_by_case.get(case_03.get("trial_case_id", ""), {})
    decision_case_04 = decisions_by_case.get(case_04.get("trial_case_id", ""), {})
    event_case_04 = events_by_case.get(case_04.get("trial_case_id", ""), {})
    decision_case_05 = decisions_by_case.get(case_05.get("trial_case_id", ""), {})
    event_case_05 = events_by_case.get(case_05.get("trial_case_id", ""), {})
    decision_case_06 = decisions_by_case.get(case_06.get("trial_case_id", ""), {})
    event_case_06 = events_by_case.get(case_06.get("trial_case_id", ""), {})
    decision_case_07 = decisions_by_case.get(case_07.get("trial_case_id", ""), {})
    event_case_07 = events_by_case.get(case_07.get("trial_case_id", ""), {})
    decision_case_08 = decisions_by_case.get(case_08.get("trial_case_id", ""), {})
    event_case_08 = events_by_case.get(case_08.get("trial_case_id", ""), {})

    ok(decision_case_01.get("decision") == "ALLOW_TEXT_ONLY", "case01_decision")
    ok(event_case_01.get("output_mode") == "TEXT_ONLY", "case01_output_mode")
    ok(decision_case_01.get("safety_priority_guard_applied") is True, "case01_safety_priority_guard")

    ok(decision_case_02.get("decision") == "ALLOW_TEXT_ONLY", "case02_decision")
    ok(event_case_02.get("output_mode") == "TEXT_ONLY", "case02_output_mode")

    ok(decision_case_03.get("decision") == "DELAY", "case03_decision")
    ok(event_case_03.get("output_mode") == "SHADOW_COMPATIBLE_TEXT_OUTPUT", "case03_output_mode")
    ok(decision_case_03.get("safety_priority_guard_applied") is True, "case03_safety_guard")

    ok(decision_case_04.get("decision") == "ALLOW_DRY_SPEECH_PREVIEW", "case04_decision")
    ok(event_case_04.get("output_mode") == "DRY_SPEECH_PREVIEW", "case04_output_mode")

    ok(decision_case_05.get("decision") == "ALLOW_TEXT_ONLY", "case05_decision")
    ok(event_case_05.get("historical_only") is True, "case05_historical_only")
    ok(event_case_05.get("freshness_status") == "STALE_HISTORICAL_ONLY", "case05_freshness_status")
    ok(decision_case_05.get("stale_guard_applied") is True, "case05_stale_guard")

    ok(decision_case_06.get("decision") == "SUPPRESS", "case06_decision")
    ok(event_case_06.get("output_mode") == "STRUCTURED_LOG_ONLY", "case06_output_mode")
    ok(decision_case_06.get("ownership_guard_applied") is True, "case06_ownership_guard")

    ok(decision_case_07.get("decision") == "ALLOW_DRY_SPEECH_PREVIEW", "case07_decision")
    ok(event_case_07.get("output_mode") == "DRY_SPEECH_PREVIEW", "case07_output_mode")
    ok(decision_case_07.get("safety_priority_guard_applied") is True, "case07_safety_guard")

    ok(decision_case_08.get("decision") == "REQUIRE_CONFIRMATION", "case08_decision")
    ok(event_case_08.get("requires_confirmation") is True, "case08_requires_confirmation")
    ok(event_case_08.get("output_mode") == "SHADOW_COMPATIBLE_TEXT_OUTPUT", "case08_output_mode")

    ok(all(row.get("source_chain") for row in case_rows), "all_cases_have_source_chain")
    ok(all(row.get("source_chain") for row in decision_rows), "all_decisions_have_source_chain")
    ok(all(row.get("source_chain") for row in event_rows), "all_events_have_source_chain")
    ok(all(row.get("source_chain") for row in vop_rows), "all_vop_have_source_chain")
    ok(all(row.get("source_chain") for row in abort_rows), "all_abort_rows_have_source_chain")
    ok(all(row.get("source_chain") for row in observability_case_rows), "all_observability_rows_have_source_chain")
    ok(
        all(row.get("output_mode") in ALLOWED_OUTPUT_MODES for row in event_rows),
        "all_events_limited_to_allowed_modes",
    )
    ok(
        all(row.get("output_mode") in ALLOWED_OUTPUT_MODES for row in vop_rows),
        "all_vop_limited_to_allowed_modes",
    )
    ok(all(row.get("audio_output") is False for row in event_rows), "all_events_no_audio_output")
    ok(all(row.get("tts_invoked") is False for row in event_rows), "all_events_no_tts")
    ok(all(row.get("vop_runtime_invoked") is False for row in event_rows), "all_events_no_vop_runtime")
    ok(all(row.get("user_heard_assumed") is False for row in event_rows), "all_events_not_assumed_heard")
    ok(all(row.get("audio_output_invoked") is False for row in vop_rows), "all_vop_no_audio_output")
    ok(all(row.get("runtime_vop_invoked") is False for row in vop_rows), "all_vop_no_runtime")
    ok(all(row.get("abort_triggered") is False for row in abort_rows), "all_abort_checks_pass")
    ok(all(row.get("violations") == [] for row in abort_rows), "all_abort_violations_empty")
    ok(
        all(row.get("stale_safety_speech_output_as_current_fact") is False for row in abort_rows),
        "no_stale_safety_as_current_fact",
    )
    ok(
        all(row.get("non_owner_voice_triggers_output") is False for row in abort_rows),
        "non_owner_does_not_trigger_output",
    )
    ok(
        all(row.get("p0_p1_safety_suppressed_by_lower_priority") is False for row in abort_rows),
        "p0_p1_not_suppressed_by_lower_priority",
    )

    run = observability.get("run") or {}
    ok(run.get("trial_run_id") == "text_only_controlled_output_trial_run_v1_001", "run_id")
    ok(run.get("source_definition_id") == "cod_v1_001", "run_source_definition")
    ok(run.get("trial_scope") == "minimal_runtime_integration_text_only_controlled_output_trial", "run_trial_scope")
    ok(run.get("output_mode") == "TEXT_ONLY_FAMILY_ONLY", "run_output_mode")
    ok(run.get("input_case_count") == len(case_rows), "run_input_case_count")
    ok(run.get("controlled_output_event_count") == len(event_rows), "run_output_event_count")
    ok(run.get("speech_gate_controlled_decision_count") == len(decision_rows), "run_decision_count")
    ok(run.get("vop_controlled_event_count") == len(vop_rows), "run_vop_count")
    ok(run.get("abort_check_count") == len(abort_rows), "run_abort_count")
    ok(run.get("dry_speech_preview_count") == 2, "run_dry_preview_count")
    ok(
        run.get("final_trial_status") in {
            "TEXT_ONLY_OUTPUT_PASS",
            "TEXT_ONLY_OUTPUT_PASS_WITH_DELAY",
            "TEXT_ONLY_OUTPUT_PASS_WITH_SUPPRESSION",
            "TEXT_ONLY_OUTPUT_ABORTED",
            "TEXT_ONLY_OUTPUT_NEEDS_REVIEW",
        },
        "run_final_trial_status_enum",
    )
    ok(bool(run.get("source_chain")), "run_source_chain")

    summary_metrics = observability.get("summary_metrics") or {}
    ok(summary_metrics.get("trial_case_count") == len(case_rows), "obs_trial_case_count")
    ok(summary_metrics.get("controlled_text_output_event_count") == len(event_rows), "obs_event_count")
    ok(summary_metrics.get("speech_gate_controlled_decision_count") == len(decision_rows), "obs_decision_count")
    ok(summary_metrics.get("vop_controlled_event_candidate_count") == len(vop_rows), "obs_vop_count")
    ok(summary_metrics.get("abort_check_count") == len(abort_rows), "obs_abort_count")
    ok(summary_metrics.get("output_mode_limited_to_text_only") is True, "obs_output_mode_limited")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        ok(report.get("boundary_ok") is True, f"{report_key}_boundary_ok")
        ok(report.get("violations") == [], f"{report_key}_violations")
        ok(report.get("fact_status") == "not_fact", f"{report_key}_fact_status")
        ok(report.get("write_allowed") is False, f"{report_key}_write_allowed")
        for flag in [
            "real_audio_output_invoked",
            "runtime_tts_invoked",
            "runtime_audio_output_invoked",
            "speech_gate_runtime_invoked",
            "vop_runtime_invoked",
            "runtime_camera_invoked",
            "runtime_microphone_invoked",
            "runtime_asr_invoked",
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
            "external_tts_api_invoked",
            "audio_device_invoked",
        ]:
            ok(report.get(flag) is False, f"{report_key}_{flag}")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
