#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Text-Only Output Post-Trial Review v1."""

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
FORBIDDEN_OUTPUT_MODES = {
    "REAL_AUDIO_PLAYBACK",
    "REAL_TTS_STREAM",
    "UNCONTROLLED_AUDIO",
    "DEVICE_AUDIO_OUTPUT",
    "EXTERNAL_TTS_OUTPUT",
    "VOP_RUNTIME_OUTPUT",
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
        "text_only_output_post_trial_review_report": "text_only_output_post_trial_review_report.json",
        "text_only_output_stability_review": "text_only_output_stability_review.json",
        "output_mode_boundary_review": "output_mode_boundary_review.json",
        "user_heard_assumption_review": "user_heard_assumption_review.json",
        "audio_runtime_boundary_review": "audio_runtime_boundary_review.json",
        "source_chain_review": "source_chain_review.json",
        "safety_priority_review": "safety_priority_review.json",
        "ownership_guard_review": "ownership_guard_review.json",
        "freshness_review": "freshness_review.json",
        "abort_coverage_review": "abort_coverage_review.json",
        "closure_readiness_decision": "closure_readiness_decision.json",
        "risk_register": "risk_register.json",
        "next_phase_recommendation": "next_phase_recommendation.json",
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
            "phase": "Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    report_payload = data["text_only_output_post_trial_review_report"]
    stability = data["text_only_output_stability_review"]
    output_mode_review = data["output_mode_boundary_review"]
    user_heard_review = data["user_heard_assumption_review"]
    audio_review = data["audio_runtime_boundary_review"]
    source_chain_review = data["source_chain_review"]
    safety_review = data["safety_priority_review"]
    ownership_review = data["ownership_guard_review"]
    freshness_review = data["freshness_review"]
    abort_review = data["abort_coverage_review"]
    closure = data["closure_readiness_decision"]
    next_phase = data["next_phase_recommendation"]
    risk_register = data["risk_register"]

    ok(
        summary.get("review_scope") == "minimal_runtime_integration_text_only_output_post_trial_review_only",
        "review_scope",
    )
    ok(summary.get("review_only") is True, "review_only")
    ok(summary.get("text_only_trial_input_loaded") is True, "text_only_trial_input_loaded")
    ok(summary.get("controlled_output_definition_input_loaded") is True, "controlled_output_definition_input_loaded")
    ok(summary.get("post_shadow_review_input_loaded") is True, "post_shadow_review_input_loaded")
    ok(summary.get("reviewed_trial_case_count") == 8, "reviewed_trial_case_count")
    ok(summary.get("reviewed_controlled_text_output_event_count") == 8, "reviewed_controlled_text_output_event_count")
    ok(summary.get("reviewed_speech_gate_controlled_decision_count") == 8, "reviewed_speech_gate_controlled_decision_count")
    ok(summary.get("reviewed_vop_controlled_event_candidate_count") == 8, "reviewed_vop_controlled_event_candidate_count")
    ok(summary.get("reviewed_abort_check_count") == 8, "reviewed_abort_check_count")
    ok(summary.get("output_mode_boundary_review_completed") is True, "output_mode_boundary_review_completed")
    ok(summary.get("user_heard_assumption_review_completed") is True, "user_heard_assumption_review_completed")
    ok(summary.get("audio_runtime_boundary_review_completed") is True, "audio_runtime_boundary_review_completed")
    ok(summary.get("source_chain_review_completed") is True, "source_chain_review_completed")
    ok(summary.get("safety_priority_review_completed") is True, "safety_priority_review_completed")
    ok(summary.get("ownership_guard_review_completed") is True, "ownership_guard_review_completed")
    ok(summary.get("freshness_review_completed") is True, "freshness_review_completed")
    ok(summary.get("abort_coverage_review_completed") is True, "abort_coverage_review_completed")
    ok(summary.get("closure_readiness_decision_generated") is True, "closure_readiness_decision_generated")
    ok(summary.get("output_boundary_weakness_found") is False, "output_boundary_weakness_found")
    ok(summary.get("user_heard_assumption_violation_found") is False, "user_heard_assumption_violation_found")
    ok(summary.get("audio_runtime_violation_found") is False, "audio_runtime_violation_found")
    ok(summary.get("source_chain_gap_found") is False, "source_chain_gap_found")
    ok(summary.get("safety_priority_gap_found") is False, "safety_priority_gap_found")
    ok(summary.get("ownership_guard_gap_found") is False, "ownership_guard_gap_found")
    ok(summary.get("freshness_gap_found") is False, "freshness_gap_found")
    ok(summary.get("abort_coverage_gap_found") is False, "abort_coverage_gap_found")

    for flag in [
        "controlled_output_trial_executed",
        "new_controlled_output_executed",
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
        summary.get("final_decision") == "TEXT_ONLY_OUTPUT_POST_TRIAL_REVIEW_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "summary_final_decision",
    )

    ok(report_payload.get("review_id") == "toptr_mrit_v1_001", "report_review_id")
    ok(
        report_payload.get("source_text_only_trial_run_id") == "text_only_controlled_output_trial_run_v1_001",
        "report_source_trial_run_id",
    )
    ok(
        report_payload.get("review_scope") == "minimal_runtime_integration_text_only_output_post_trial_review",
        "report_scope",
    )
    ok(report_payload.get("reviewed_trial_case_count") == 8, "report_trial_case_count")
    ok(report_payload.get("reviewed_controlled_text_output_event_count") == 8, "report_event_count")
    ok(report_payload.get("reviewed_speech_gate_controlled_decision_count") == 8, "report_decision_count")
    ok(report_payload.get("reviewed_vop_controlled_event_candidate_count") == 8, "report_vop_count")
    ok(report_payload.get("reviewed_abort_check_count") == 8, "report_abort_count")
    ok(report_payload.get("output_mode_review_result") == "OUTPUT_MODE_BOUNDARY_OK", "report_output_mode_result")
    ok(report_payload.get("user_heard_assumption_review_result") == "USER_HEARD_ASSUMPTION_OK", "report_user_heard_result")
    ok(report_payload.get("audio_boundary_review_result") == "AUDIO_RUNTIME_BOUNDARY_OK", "report_audio_result")
    ok(report_payload.get("source_chain_review_result") == "SOURCE_CHAIN_COMPLETE", "report_source_chain_result")
    ok(report_payload.get("safety_priority_review_result") == "SAFETY_PRIORITY_GUARD_OK", "report_safety_result")
    ok(report_payload.get("ownership_guard_review_result") == "OWNERSHIP_GUARD_OK", "report_ownership_result")
    ok(report_payload.get("freshness_review_result") == "FRESHNESS_GUARD_OK", "report_freshness_result")
    ok(report_payload.get("abort_coverage_review_result") == "ABORT_COVERAGE_COMPLETE", "report_abort_result")
    ok(
        report_payload.get("readiness_decision") == "READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "report_readiness_decision",
    )
    ok(
        report_payload.get("next_phase_recommendation") == "Phase-Minimal-Runtime-Integration-Closure-v1-001",
        "report_next_phase",
    )
    ok(
        report_payload.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "report_source_chain",
    )

    ok(stability.get("trial_case_count_is_expected") is True, "stability_trial_case_count_is_expected")
    ok(stability.get("controlled_text_output_event_count_is_expected") is True, "stability_event_count_is_expected")
    ok(
        stability.get("speech_gate_controlled_decision_count_is_expected") is True,
        "stability_decision_count_is_expected",
    )
    ok(stability.get("vop_controlled_event_candidate_count_is_expected") is True, "stability_vop_count_is_expected")
    ok(stability.get("abort_check_count_is_expected") is True, "stability_abort_count_is_expected")
    ok(stability.get("missing_decision_cases") == [], "stability_missing_decision_cases")
    ok(stability.get("missing_output_event_cases") == [], "stability_missing_output_event_cases")
    ok(stability.get("missing_vop_cases") == [], "stability_missing_vop_cases")
    ok(stability.get("missing_abort_cases") == [], "stability_missing_abort_cases")
    ok(stability.get("missing_observability_cases") == [], "stability_missing_observability_cases")
    ok(stability.get("missing_terminal_decision_cases") == [], "stability_missing_terminal_decision_cases")
    ok(stability.get("unexpected_output_modes") == [], "stability_unexpected_output_modes")
    ok(stability.get("inconsistent_output_decision_cases") == [], "stability_inconsistent_output_decision_cases")
    ok(stability.get("all_cases_explainable") is True, "stability_all_cases_explainable")
    ok(stability.get("stability_gap_found") is False, "stability_gap_found")
    ok(stability.get("stability_review_result") == "TEXT_ONLY_TRIAL_STABLE", "stability_review_result")
    ok(
        stability.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "stability_source_chain",
    )

    output_checks = output_mode_review.get("checks") or {}
    for key in [
        "events_only_use_allowed_modes",
        "vop_only_use_allowed_modes",
        "no_real_audio_playback_mode",
        "no_real_tts_stream_mode",
        "no_uncontrolled_audio_mode",
        "no_device_audio_output_mode",
        "no_external_tts_output_mode",
        "no_vop_runtime_output_mode",
    ]:
        ok(output_checks.get(key) is True, f"output_mode_check_{key}")
    ok(set(output_mode_review.get("allowed_output_modes") or []) == ALLOWED_OUTPUT_MODES, "allowed_output_modes")
    ok(set(output_mode_review.get("forbidden_output_modes") or []) == FORBIDDEN_OUTPUT_MODES, "forbidden_output_modes")
    ok(output_mode_review.get("forbidden_modes_detected") == [], "forbidden_modes_detected")
    ok(output_mode_review.get("output_boundary_weakness_found") is False, "output_mode_boundary_weakness_found")
    ok(output_mode_review.get("output_mode_review_result") == "OUTPUT_MODE_BOUNDARY_OK", "output_mode_review_result")
    ok(
        output_mode_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "output_mode_source_chain",
    )

    user_heard_checks = user_heard_review.get("checks") or {}
    for key in [
        "every_output_event_has_user_heard_assumed_false",
        "no_output_event_claims_user_heard_output",
        "no_output_event_claims_audio_was_played",
        "dry_speech_preview_not_treated_as_heard_speech",
        "text_only_output_not_treated_as_delivered_voice",
    ]:
        ok(user_heard_checks.get(key) is True, f"user_heard_check_{key}")
    ok(user_heard_review.get("violating_output_event_ids") == [], "user_heard_violating_output_event_ids")
    ok(user_heard_review.get("user_heard_assumption_violation_found") is False, "user_heard_violation_found")
    ok(
        user_heard_review.get("user_heard_assumption_review_result") == "USER_HEARD_ASSUMPTION_OK",
        "user_heard_review_result",
    )
    ok(
        user_heard_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "user_heard_source_chain",
    )

    audio_checks = audio_review.get("checks") or {}
    for key in [
        "every_output_event_audio_output_false",
        "every_output_event_tts_invoked_false",
        "summary_runtime_tts_invoked_false",
        "summary_runtime_audio_output_invoked_false",
        "every_output_event_vop_runtime_invoked_false",
        "every_vop_event_runtime_false",
        "summary_speech_gate_runtime_invoked_false",
        "summary_vop_runtime_invoked_false",
        "summary_external_tts_api_invoked_false",
        "summary_audio_device_invoked_false",
        "no_runtime_report_tts_false",
        "no_runtime_report_audio_false",
    ]:
        ok(audio_checks.get(key) is True, f"audio_check_{key}")
    ok(audio_review.get("audio_runtime_violation_found") is False, "audio_runtime_violation_found")
    ok(audio_review.get("audio_boundary_review_result") == "AUDIO_RUNTIME_BOUNDARY_OK", "audio_boundary_review_result")
    ok(
        audio_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "audio_review_source_chain",
    )

    source_checks = source_chain_review.get("checks") or {}
    for key in [
        "every_speech_gate_controlled_decision_has_source_chain",
        "every_controlled_text_output_event_has_source_chain",
        "every_vop_controlled_event_candidate_has_source_chain",
        "every_text_only_output_abort_check_has_source_chain",
        "every_final_review_decision_has_source_chain",
        "every_observability_case_has_source_chain",
    ]:
        ok(source_checks.get(key) is True, f"source_check_{key}")
    ok(source_chain_review.get("source_chain_gap_found") is False, "source_chain_gap_found")
    ok(source_chain_review.get("gap_items") == [], "source_chain_gap_items")
    ok(source_chain_review.get("source_chain_review_result") == "SOURCE_CHAIN_COMPLETE", "source_chain_review_result")
    ok(
        source_chain_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "source_chain_review_source_chain",
    )

    safety_checks = safety_review.get("checks") or {}
    for key in [
        "p0_p1_output_not_suppressed_by_lower_priority",
        "p0_safety_text_only_case_exists",
        "p1_p0_protection_inherited_from_definition",
        "stale_p0_safety_repeat_not_output_as_current_fact",
        "emergency_safety_observation_preview_stays_candidate_text_only",
    ]:
        ok(safety_checks.get(key) is True, f"safety_check_{key}")
    ok(safety_review.get("gap_items") == [], "safety_gap_items")
    ok(safety_review.get("safety_priority_gap_found") is False, "safety_priority_gap_found")
    ok(safety_review.get("safety_priority_review_result") == "SAFETY_PRIORITY_GUARD_OK", "safety_priority_review_result")
    ok(
        safety_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "safety_review_source_chain",
    )

    ownership_checks = ownership_review.get("checks") or {}
    for key in [
        "non_owner_interruption_attempt_does_not_trigger_output",
        "phone_human_media_public_voice_protections_inherited_where_applicable",
        "ownership_guard_applied_to_relevant_output_events",
        "no_non_owner_output_control",
    ]:
        ok(ownership_checks.get(key) is True, f"ownership_check_{key}")
    ok(ownership_review.get("gap_items") == [], "ownership_gap_items")
    ok(ownership_review.get("ownership_guard_gap_found") is False, "ownership_guard_gap_found")
    ok(ownership_review.get("ownership_guard_review_result") == "OWNERSHIP_GUARD_OK", "ownership_guard_review_result")
    ok(
        ownership_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "ownership_review_source_chain",
    )

    freshness_checks = freshness_review.get("checks") or {}
    for key in [
        "stale_safety_speech_output_is_historical_only",
        "repeat_output_has_freshness_guard",
        "resume_output_if_present_requires_future_freshness_check",
        "no_stale_route_ocr_safety_content_presented_as_current_fact",
    ]:
        ok(freshness_checks.get(key) is True, f"freshness_check_{key}")
    ok(freshness_review.get("gap_items") == [], "freshness_gap_items")
    ok(freshness_review.get("freshness_gap_found") is False, "freshness_gap_found")
    ok(freshness_review.get("freshness_review_result") == "FRESHNESS_GUARD_OK", "freshness_review_result")
    ok(
        freshness_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "freshness_review_source_chain",
    )

    coverage_rows = abort_review.get("coverage_rows") or []
    ok(len(coverage_rows) == 13, "abort_coverage_row_count")
    coverage_by_key = _index_by(coverage_rows, "review_key")
    for key in [
        "real_tts_invoked",
        "audio_output_invoked",
        "speech_gate_runtime_invoked",
        "vop_runtime_invoked",
        "output_without_source_chain",
        "p0_p1_safety_suppressed_by_lower_priority",
        "stale_safety_speech_output_as_current_fact",
        "non_owner_voice_triggers_output",
        "task_state_committed",
        "navigation_action_triggered",
        "map_api_invoked",
        "memory_worldmodel_fact_write",
        "user_heard_assumed_true",
    ]:
        ok(key in coverage_by_key, f"abort_coverage_row_exists_{key}")
        row = coverage_by_key.get(key, {})
        ok(row.get("covered_in_trial_artifacts") is True, f"abort_covered_in_trial_{key}")
        ok(row.get("covered_in_post_trial_review_guard") is True, f"abort_covered_in_review_guard_{key}")
        ok(row.get("coverage_sufficient_for_closure") is True, f"abort_coverage_sufficient_{key}")
    ok(coverage_by_key.get("user_heard_assumed_true", {}).get("covered_in_definition") is False, "user_heard_not_in_definition")
    ok(abort_review.get("abort_coverage_gap_found") is False, "abort_coverage_gap_found")
    ok(abort_review.get("gap_items") == [], "abort_coverage_gap_items")
    ok(abort_review.get("abort_coverage_review_result") == "ABORT_COVERAGE_COMPLETE", "abort_coverage_review_result")
    ok(
        abort_review.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "abort_review_source_chain",
    )

    ok(
        closure.get("readiness_decision") == "READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "closure_readiness_decision",
    )
    ok(
        closure.get("next_phase_recommendation") == "Phase-Minimal-Runtime-Integration-Closure-v1-001",
        "closure_next_phase_recommendation",
    )
    ok(closure.get("must_not_recommend_real_tts") is True, "closure_must_not_recommend_real_tts")
    ok(closure.get("must_not_recommend_live_audio") is True, "closure_must_not_recommend_live_audio")
    ok(closure.get("must_not_recommend_camera_enablement") is True, "closure_must_not_recommend_camera_enablement")
    ok(closure.get("must_not_recommend_map_api_enablement") is True, "closure_must_not_recommend_map_api_enablement")
    ok(
        closure.get("must_not_recommend_memory_or_worldmodel_write") is True,
        "closure_must_not_recommend_memory_or_worldmodel_write",
    )
    ok(
        closure.get("allowed_next_scope") == "minimal_runtime_integration_closure_only",
        "closure_allowed_next_scope",
    )
    forbidden_next_scope = set(closure.get("forbidden_next_scope") or [])
    for item in [
        "real_tts_enablement",
        "live_audio_enablement",
        "camera_enablement",
        "microphone_enablement",
        "map_api_enablement",
        "ocr_provider_enablement",
        "memory_write_enablement",
        "worldmodel_write_enablement",
        "task_commit_enablement",
        "navigation_action_enablement",
    ]:
        ok(item in forbidden_next_scope, f"closure_forbidden_next_scope_{item}")
    ok(
        closure.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "closure_source_chain",
    )

    ok(
        next_phase.get("next_phase_recommendation") == "Phase-Minimal-Runtime-Integration-Closure-v1-001",
        "next_phase_recommendation",
    )
    ok(
        next_phase.get("rationale")
        == "text-only trial is stable and boundary-safe, so the next step can only be minimal runtime integration closure",
        "next_phase_rationale",
    )
    ok(
        next_phase.get("alternative_if_regression_found")
        == "Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-002",
        "next_phase_alternative",
    )
    ok(next_phase.get("must_not_recommend_real_tts") is True, "next_phase_must_not_real_tts")
    ok(next_phase.get("must_not_recommend_live_audio") is True, "next_phase_must_not_live_audio")
    ok(
        next_phase.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "next_phase_source_chain",
    )

    risk_items = risk_register.get("items") or []
    ok(len(risk_items) >= 3, "risk_register_item_count")
    ok(
        risk_register.get("source_chain") == "minimal_runtime_integration_text_only_output_post_trial_review_v1",
        "risk_register_source_chain",
    )

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        ok(report.get("boundary_ok") is True, f"{report_key}_boundary_ok")
        ok(report.get("violations") == [], f"{report_key}_violations")
        ok(report.get("fact_status") == "not_fact", f"{report_key}_fact_status")
        ok(report.get("write_allowed") is False, f"{report_key}_write_allowed")
        for flag in [
            "review_only",
            "controlled_output_trial_executed",
            "new_controlled_output_executed",
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
            expected = True if flag == "review_only" else False
            ok(report.get(flag) is expected, f"{report_key}_{flag}")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Text-Only-Output-Post-Trial-Review-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
