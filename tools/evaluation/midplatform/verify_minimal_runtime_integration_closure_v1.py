#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

MIN_CHECKS = 80
EXPECTED_PHASES = {
    "Trial Definition": "MINIMAL_RUNTIME_INTEGRATION_TRIAL_DEFINITION_READY_FOR_CONTROLLED_SHADOW_TRIAL",
    "Controlled Shadow Trial": "MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_READY_FOR_POST_SHADOW_REVIEW",
    "Post-Shadow Review": "POST_SHADOW_REVIEW_READY_FOR_CONTROLLED_OUTPUT_DEFINITION",
    "Controlled Output Definition": "CONTROLLED_OUTPUT_DEFINITION_READY_FOR_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL",
    "Text-Only Controlled Output Trial": "TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL_READY_FOR_POST_TRIAL_REVIEW",
    "Text-Only Output Post-Trial Review": "TEXT_ONLY_OUTPUT_POST_TRIAL_REVIEW_READY_FOR_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
}
EXPECTED_NON_CLAIMS = {
    "Minimal Runtime Integration closure does not equal live runtime.",
    "text-only output does not equal real voice output.",
    "dry speech preview does not equal TTS.",
    "VOP controlled event candidate does not equal VOP runtime.",
    "Speech Gate controlled decision candidate does not equal Speech Gate runtime.",
    "controlled shadow trial does not equal real sensor runtime.",
    "no Memory / WorldModel / Fact write occurred.",
    "no navigation action was executed.",
    "no real map / GPS runtime was enabled.",
    "no camera / microphone / ASR / TTS runtime was enabled.",
}
EXPECTED_DEFERRED = {
    "real_tts_controlled_enablement",
    "real_vop_runtime",
    "real_speech_gate_runtime",
    "real_camera_runtime",
    "real_microphone_asr_runtime",
    "map_gps_integration",
    "ocr_provider_runtime_integration",
    "object_tracking_runtime",
    "segmentation_runtime",
    "face_recognition",
    "voiceprint_runtime",
    "facial_expression_or_audio_emotion_runtime",
    "memory_worldmodel_fact_write",
}
EXPECTED_NEXT_FOCUS = {
    "ocr_closure_or_ocr_final_boundary_review",
    "return_to_vision_mainline",
    "viewpoint_segmentation_or_view_slicing",
    "object_tracking",
    "visual_candidate_stabilization",
    "map_route_location_context_integration",
    "basic_navigation_loop_strengthening",
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
        "minimal_runtime_integration_closure_report": "minimal_runtime_integration_closure_report.json",
        "completed_phase_matrix": "completed_phase_matrix.json",
        "validated_capability_summary": "validated_capability_summary.json",
        "output_baseline_summary": "output_baseline_summary.json",
        "remaining_runtime_disabled_summary": "remaining_runtime_disabled_summary.json",
        "non_claims_register": "non_claims_register.json",
        "deferred_capability_pool": "deferred_capability_pool.json",
        "vision_mainline_handoff_plan": "vision_mainline_handoff_plan.json",
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
            "phase": "Minimal-Runtime-Integration-Closure-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    closure_report = data["minimal_runtime_integration_closure_report"]
    phase_matrix = data["completed_phase_matrix"]
    validated = data["validated_capability_summary"]
    baseline = data["output_baseline_summary"]
    disabled = data["remaining_runtime_disabled_summary"]
    non_claims = data["non_claims_register"]
    deferred = data["deferred_capability_pool"]
    handoff = data["vision_mainline_handoff_plan"]
    next_phase = data["next_phase_recommendation"]

    ok(summary.get("closure_scope") == "minimal_runtime_integration_closure_only", "closure_scope")
    ok(summary.get("closure_only") is True, "closure_only")
    ok(summary.get("completed_phase_count") == 6, "completed_phase_count")
    ok(summary.get("all_required_phases_loaded") is True, "all_required_phases_loaded")
    ok(summary.get("all_required_phases_go") is True, "all_required_phases_go")
    ok(summary.get("validated_loop_summary_generated") is True, "validated_loop_summary_generated")
    ok(summary.get("output_baseline_summary_generated") is True, "output_baseline_summary_generated")
    ok(summary.get("remaining_runtime_disabled_summary_generated") is True, "remaining_runtime_disabled_summary_generated")
    ok(summary.get("non_claims_register_generated") is True, "non_claims_register_generated")
    ok(summary.get("deferred_capability_pool_generated") is True, "deferred_capability_pool_generated")
    ok(summary.get("vision_mainline_handoff_plan_generated") is True, "vision_mainline_handoff_plan_generated")
    ok(summary.get("current_output_baseline") == "text_only_controlled_output_baseline", "current_output_baseline")
    ok(summary.get("real_audio_output_allowed") is False, "real_audio_output_allowed")
    ok(summary.get("real_tts_allowed") is False, "real_tts_allowed")
    ok(summary.get("user_heard_assumed") is False, "user_heard_assumed")
    ok(summary.get("live_runtime_enabled") is False, "live_runtime_enabled")
    ok(summary.get("memory_write_allowed") is False, "memory_write_allowed")
    ok(summary.get("worldmodel_write_allowed") is False, "worldmodel_write_allowed")
    ok(summary.get("fact_write_allowed") is False, "fact_write_allowed")

    for flag in [
        "new_runtime_enabled",
        "controlled_output_expanded",
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
        "memory_written",
        "world_model_written",
        "fact_written",
        "route_modified",
        "benchmark_accuracy_updated",
        "runtime_routing_changed",
    ]:
        ok(summary.get(flag) is False, f"summary_{flag}")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(summary.get("violations") == [], "summary_violations")
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")
    ok(
        summary.get("final_decision") == "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE",
        "summary_final_decision",
    )

    ok(closure_report.get("closure_id") == "mric_v1_001", "closure_report_id")
    ok(closure_report.get("closure_scope") == "minimal_runtime_integration_closure", "closure_report_scope")
    ok(closure_report.get("completed_phase_count") == 6, "closure_report_completed_phase_count")
    ok(len(closure_report.get("completed_phase_refs") or []) == 6, "closure_report_completed_phase_refs")
    ok(
        closure_report.get("completed_capability_summary") == "validated_capability_summary.json",
        "closure_report_completed_capability_summary",
    )
    ok(
        closure_report.get("validated_loop_summary") == "validated_capability_summary.json",
        "closure_report_validated_loop_summary",
    )
    ok(
        closure_report.get("output_baseline_summary") == "output_baseline_summary.json",
        "closure_report_output_baseline_summary",
    )
    ok(
        closure_report.get("remaining_runtime_disabled_summary") == "remaining_runtime_disabled_summary.json",
        "closure_report_disabled_summary_ref",
    )
    no_write_summary = closure_report.get("no_write_boundary_summary") or {}
    ok(no_write_summary.get("memory_write_allowed") is False, "closure_report_memory_write_allowed")
    ok(no_write_summary.get("worldmodel_write_allowed") is False, "closure_report_worldmodel_write_allowed")
    ok(no_write_summary.get("fact_write_allowed") is False, "closure_report_fact_write_allowed")
    ok(no_write_summary.get("scene_delta_commit_allowed") is False, "closure_report_scene_delta_commit_allowed")
    ok(set(closure_report.get("known_non_claims") or []) == EXPECTED_NON_CLAIMS, "closure_report_known_non_claims")
    ok(
        set(closure_report.get("deferred_capability_pool") or []) == EXPECTED_DEFERRED,
        "closure_report_deferred_capability_pool",
    )
    ok(
        closure_report.get("mainline_handoff_decision")
        == "RETURN_TO_VISION_MAINLINE_AFTER_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "closure_report_mainline_handoff_decision",
    )
    ok(set(closure_report.get("next_mainline_focus") or []) == EXPECTED_NEXT_FOCUS, "closure_report_next_mainline_focus")
    ok(
        closure_report.get("final_closure_decision") == "MINIMAL_RUNTIME_INTEGRATION_CLOSED_RETURN_TO_VISION_MAINLINE",
        "closure_report_final_decision",
    )
    ok(
        closure_report.get("source_chain") == "minimal_runtime_integration_closure_v1",
        "closure_report_source_chain",
    )

    phase_rows = phase_matrix.get("rows") or []
    ok(phase_matrix.get("completed_phase_count") == 6, "phase_matrix_completed_phase_count")
    ok(len(phase_rows) == 6, "phase_matrix_row_count")
    phase_by_name = _index_by(phase_rows, "phase_name")
    for phase_name, final_decision in EXPECTED_PHASES.items():
        ok(phase_name in phase_by_name, f"phase_matrix_row_exists_{phase_name}")
        row = phase_by_name.get(phase_name, {})
        ok(row.get("verdict") == "GO", f"phase_matrix_verdict_{phase_name}")
        ok(row.get("final_decision") == final_decision, f"phase_matrix_final_decision_{phase_name}")
        ok(bool(row.get("output_dir")), f"phase_matrix_output_dir_{phase_name}")
        ok(isinstance(row.get("core_artifacts"), list) and len(row.get("core_artifacts")) >= 3, f"phase_matrix_core_artifacts_{phase_name}")
        ok(row.get("boundary_status") == "BOUNDARY_OK", f"phase_matrix_boundary_status_{phase_name}")
        ok(row.get("source_chain") == "minimal_runtime_integration_closure_v1", f"phase_matrix_source_chain_{phase_name}")

    for key in [
        "minimal_runtime_trial_contract_defined",
        "controlled_shadow_loop_executed",
        "post_shadow_review_passed",
        "controlled_output_contract_defined",
        "text_only_controlled_output_trial_passed",
        "text_only_post_trial_review_passed",
        "speech_gate_shadow_controlled_decision_candidate_path_validated",
        "vop_shadow_controlled_event_candidate_path_validated",
        "abort_checks_validated",
        "source_chain_validated",
        "p0_p1_safety_protection_validated",
        "non_owner_output_protection_validated",
        "stale_safety_speech_historical_only_protection_validated",
    ]:
        ok(validated.get(key) is True, f"validated_{key}")
    ok(validated.get("source_chain") == "minimal_runtime_integration_closure_v1", "validated_source_chain")

    ok(baseline.get("current_output_baseline") == "text_only_controlled_output_baseline", "baseline_current_output_baseline")
    ok(set(baseline.get("allowed_output_modes") or []) == {"TEXT_ONLY", "STRUCTURED_LOG_ONLY", "DRY_SPEECH_PREVIEW", "SHADOW_COMPATIBLE_TEXT_OUTPUT"}, "baseline_allowed_output_modes")
    ok(baseline.get("real_audio_output_allowed") is False, "baseline_real_audio_output_allowed")
    ok(baseline.get("real_tts_allowed") is False, "baseline_real_tts_allowed")
    ok(baseline.get("user_heard_assumed") is False, "baseline_user_heard_assumed")
    ok(baseline.get("vop_runtime_allowed") is False, "baseline_vop_runtime_allowed")
    ok(baseline.get("speech_gate_runtime_allowed") is False, "baseline_speech_gate_runtime_allowed")
    ok(baseline.get("source_chain") == "minimal_runtime_integration_closure_v1", "baseline_source_chain")

    for key in [
        "camera_runtime",
        "microphone_runtime",
        "asr_runtime",
        "tts_runtime",
        "audio_output_runtime",
        "speech_gate_runtime",
        "vop_runtime",
        "map_api",
        "gps_runtime",
        "ocr_provider_runtime",
        "detector_runtime",
        "segmentation_runtime",
        "tracking_runtime",
        "navigation_action",
        "task_commit",
        "memory_write",
        "worldmodel_write",
        "fact_write",
        "scene_delta_commit",
        "face_recognition",
        "voiceprint_runtime",
        "facial_expression_runtime",
    ]:
        ok(disabled.get(key) == "disabled", f"disabled_{key}")
    ok(disabled.get("source_chain") == "minimal_runtime_integration_closure_v1", "disabled_source_chain")

    statements = set(non_claims.get("statements") or [])
    ok(statements == EXPECTED_NON_CLAIMS, "non_claims_statements")
    ok(non_claims.get("source_chain") == "minimal_runtime_integration_closure_v1", "non_claims_source_chain")

    deferred_rows = deferred.get("deferred_capabilities") or []
    ok(len(deferred_rows) == len(EXPECTED_DEFERRED), "deferred_row_count")
    deferred_names = {row.get("capability") for row in deferred_rows}
    ok(deferred_names == EXPECTED_DEFERRED, "deferred_capability_names")
    for row in deferred_rows:
        capability = row.get("capability")
        ok(row.get("deferred_from_next_mainline_priority") is True, f"deferred_priority_{capability}")
        ok(row.get("requires_separate_phase") is True, f"deferred_requires_phase_{capability}")
    ok(deferred.get("source_chain") == "minimal_runtime_integration_closure_v1", "deferred_source_chain")

    next_focus = set(handoff.get("next_mainline_focus") or [])
    ok(
        handoff.get("mainline_handoff_decision")
        == "RETURN_TO_VISION_MAINLINE_AFTER_MINIMAL_RUNTIME_INTEGRATION_CLOSURE",
        "handoff_decision",
    )
    ok(next_focus == EXPECTED_NEXT_FOCUS, "handoff_next_mainline_focus")
    ok(
        handoff.get("primary_next_phase_recommendation") == "Phase-Return-To-Vision-Mainline-Planning-v1-001",
        "handoff_primary_next_phase",
    )
    ok(
        handoff.get("alternative_if_ocr_final_closure_needed") == "Phase-OCR-Mainline-Final-Closure-v1-001",
        "handoff_alternative_next_phase",
    )
    must_not_insert = set(handoff.get("must_not_insert_before_vision_return") or [])
    for item in [
        "gaode_or_real_map_api_program",
        "external_product_observation",
        "face_recognition",
        "voiceprint_runtime",
        "facial_expression_runtime",
        "real_map_api",
        "real_voice_output",
    ]:
        ok(item in must_not_insert, f"handoff_must_not_insert_{item}")
    ok(handoff.get("must_not_recommend_real_tts_next") is True, "handoff_must_not_recommend_real_tts_next")
    ok(handoff.get("must_not_recommend_live_audio_next") is True, "handoff_must_not_recommend_live_audio_next")
    ok(handoff.get("must_not_recommend_camera_enablement_next") is True, "handoff_must_not_recommend_camera_enablement_next")
    ok(handoff.get("must_not_recommend_map_api_enablement_next") is True, "handoff_must_not_recommend_map_api_enablement_next")
    ok(
        handoff.get("must_not_recommend_memory_or_worldmodel_write_next") is True,
        "handoff_must_not_recommend_memory_or_worldmodel_write_next",
    )
    ok(handoff.get("source_chain") == "minimal_runtime_integration_closure_v1", "handoff_source_chain")

    ok(
        next_phase.get("primary_next_phase_recommendation") == "Phase-Return-To-Vision-Mainline-Planning-v1-001",
        "next_phase_primary",
    )
    ok(
        next_phase.get("alternative_if_ocr_mainline_final_closure_needed") == "Phase-OCR-Mainline-Final-Closure-v1-001",
        "next_phase_alternative",
    )
    ok(next_phase.get("must_not_recommend_real_tts") is True, "next_phase_must_not_recommend_real_tts")
    ok(next_phase.get("must_not_recommend_live_audio") is True, "next_phase_must_not_recommend_live_audio")
    ok(next_phase.get("must_not_recommend_camera_enablement") is True, "next_phase_must_not_recommend_camera_enablement")
    ok(next_phase.get("must_not_recommend_map_api_enablement") is True, "next_phase_must_not_recommend_map_api_enablement")
    ok(
        next_phase.get("must_not_recommend_memory_or_worldmodel_write") is True,
        "next_phase_must_not_recommend_memory_or_worldmodel_write",
    )
    ok(next_phase.get("source_chain") == "minimal_runtime_integration_closure_v1", "next_phase_source_chain")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        ok(report.get("closure_only") is True, f"{report_key}_closure_only")
        ok(report.get("new_runtime_enabled") is False, f"{report_key}_new_runtime_enabled")
        ok(report.get("controlled_output_expanded") is False, f"{report_key}_controlled_output_expanded")
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
        ]:
            ok(report.get(flag) is False, f"{report_key}_{flag}")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Closure-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
