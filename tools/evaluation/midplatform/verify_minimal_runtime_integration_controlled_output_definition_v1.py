#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Minimal Runtime Integration Controlled Output Definition v1."""

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
        "controlled_output_definition": "controlled_output_definition.json",
        "speech_gate_controlled_output_contract": "speech_gate_controlled_output_contract.json",
        "vop_controlled_output_contract": "vop_controlled_output_contract.json",
        "tts_placeholder_policy": "tts_placeholder_policy.json",
        "user_visible_output_boundary": "user_visible_output_boundary.json",
        "output_abort_conditions": "output_abort_conditions.json",
        "output_recovery_policy": "output_recovery_policy.json",
        "controlled_output_observability": "controlled_output_observability.json",
        "go_no_go_criteria": "go_no_go_criteria.json",
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
            "phase": "Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001",
        }
        _write_json(smoke_root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    cod = data["controlled_output_definition"]
    sg = data["speech_gate_controlled_output_contract"]
    vop = data["vop_controlled_output_contract"]
    tts = data["tts_placeholder_policy"]
    boundary = data["user_visible_output_boundary"]
    aborts = data["output_abort_conditions"]
    recovery = data["output_recovery_policy"]
    obs = data["controlled_output_observability"]
    go_no_go = data["go_no_go_criteria"]
    next_phase = data["next_phase_recommendation"]

    ok(
        summary.get("definition_scope") == "minimal_runtime_integration_controlled_output_definition_only",
        "definition_scope",
    )
    ok(summary.get("definition_only") is True, "definition_only")
    ok(summary.get("post_shadow_review_input_loaded") is True, "post_shadow_review_input_loaded")
    ok(summary.get("controlled_shadow_trial_input_loaded") is True, "controlled_shadow_trial_input_loaded")
    ok(summary.get("trial_definition_input_loaded") is True, "trial_definition_input_loaded")
    ok(summary.get("controlled_output_definition_generated") is True, "controlled_output_definition_generated")
    ok(summary.get("speech_gate_controlled_output_contract_defined") is True, "speech_gate_controlled_output_contract_defined")
    ok(summary.get("vop_controlled_output_contract_defined") is True, "vop_controlled_output_contract_defined")
    ok(summary.get("tts_placeholder_policy_defined") is True, "tts_placeholder_policy_defined")
    ok(summary.get("user_visible_output_boundary_defined") is True, "user_visible_output_boundary_defined")
    ok(summary.get("output_abort_conditions_defined") is True, "output_abort_conditions_defined")
    ok(summary.get("output_recovery_policy_defined") is True, "output_recovery_policy_defined")
    ok(summary.get("controlled_output_observability_defined") is True, "controlled_output_observability_defined")
    ok(summary.get("go_no_go_criteria_defined") is True, "go_no_go_criteria_defined")

    for flag in [
        "controlled_output_enabled",
        "controlled_output_executed",
        "runtime_trial_executed",
        "runtime_tts_invoked",
        "runtime_audio_output_invoked",
        "speech_gate_runtime_invoked",
        "vop_runtime_invoked",
        "runtime_camera_invoked",
        "runtime_microphone_invoked",
        "runtime_asr_invoked",
        "map_api_invoked",
        "ocr_provider_invoked",
        "task_state_committed_now",
        "navigation_action_triggered",
        "memory_written",
        "world_model_written",
        "fact_written",
    ]:
        ok(summary.get(flag) is False, f"summary_{flag}")
    ok(summary.get("boundary_ok") is True, "summary_boundary_ok")
    ok(summary.get("fact_status") == "not_fact", "summary_fact_status")
    ok(summary.get("write_allowed") is False, "summary_write_allowed")
    ok(
        summary.get("final_decision") == "CONTROLLED_OUTPUT_DEFINITION_READY_FOR_TEXT_ONLY_CONTROLLED_OUTPUT_TRIAL",
        "summary_final_decision",
    )

    ok(cod.get("controlled_output_definition_id") == "cod_v1_001", "cod_id")
    ok(cod.get("source_post_shadow_review_id") == "psr_mrit_v1_001", "cod_source_post_shadow_review_id")
    ok(cod.get("definition_scope") == "minimal_runtime_integration_controlled_output_definition", "cod_scope")
    ok(
        cod.get("allowed_future_output_modes")
        == [
            "text_console_output_controlled",
            "structured_log_output_controlled",
            "speech_request_candidate_to_shadow",
            "speech_gate_controlled_decision_candidate",
            "vop_controlled_event_candidate",
            "tts_placeholder_or_dry_output_candidate",
        ],
        "cod_allowed_modes",
    )
    ok(
        cod.get("shadow_only_output_modes")
        == [
            "speech_request_candidate_to_shadow",
            "speech_gate_controlled_decision_candidate",
            "vop_controlled_event_candidate",
        ],
        "cod_shadow_only_modes",
    )
    forbidden_modes = cod.get("forbidden_output_modes") or []
    for item in [
        "REAL_AUDIO_PLAYBACK",
        "REAL_TTS_STREAM",
        "UNCONTROLLED_AUDIO",
        "direct_tts",
        "direct_vop_runtime",
        "audio_playback",
        "navigation_instruction_execution",
        "route_modification",
        "external_notification",
        "mobile_push",
        "device_vibration",
        "haptic_output",
        "worldmodel_memory_fact_write",
    ]:
        ok(item in forbidden_modes, f"cod_forbidden_{item}")
    ok(cod.get("speech_gate_controlled_output_contract_ref") == "speech_gate_controlled_output_contract_v1_001", "cod_sg_ref")
    ok(cod.get("vop_controlled_output_contract_ref") == "vop_controlled_output_contract_v1_001", "cod_vop_ref")
    ok(cod.get("tts_placeholder_policy_ref") == "tts_placeholder_policy_v1_001", "cod_tts_ref")
    ok(cod.get("user_visible_output_boundary_ref") == "user_visible_output_boundary_v1_001", "cod_boundary_ref")
    ok(
        cod.get("output_priority_policy_ref")
        == "speech_gate_controlled_output_contract_v1_001.output_priority_policy",
        "cod_priority_policy_ref",
    )
    ok(
        cod.get("interruption_output_control_policy_ref")
        == "tts_placeholder_policy_v1_001.interruption_stop_pause_resume_only_as_candidate",
        "cod_interruption_ref",
    )
    ok(cod.get("abort_conditions_ref") == "output_abort_conditions_v1_001", "cod_abort_ref")
    ok(cod.get("recovery_policy_ref") == "output_recovery_policy_v1_001", "cod_recovery_ref")
    ok(cod.get("observability_requirements_ref") == "controlled_output_observability_v1_001", "cod_obs_ref")
    ok(cod.get("go_no_go_criteria_ref") == "controlled_output_go_no_go_criteria_v1_001", "cod_go_no_go_ref")
    ok(
        cod.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001",
        "cod_next_phase",
    )
    ok(cod.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "cod_source_chain")

    ok(sg.get("input") == "speech_request_candidate", "sg_input")
    ok(
        sg.get("required_fields")
        == [
            "priority",
            "text_ref",
            "source_chain",
            "safety_status",
            "ownership_status",
            "interruption_status",
            "freshness_status",
        ],
        "sg_required_fields",
    )
    ok(sg.get("output") == "controlled_speech_gate_decision_candidate", "sg_output")
    ok(
        sg.get("allowed_decisions")
        == [
            "ALLOW_TEXT_ONLY",
            "ALLOW_DRY_TTS_PLACEHOLDER",
            "DELAY",
            "SUPPRESS",
            "REQUIRE_CONFIRMATION",
            "ABORT_OUTPUT",
        ],
        "sg_allowed_decisions",
    )
    sg_forbidden = sg.get("forbidden") or []
    for item in ["direct_tts", "direct_vop_runtime", "audio_playback", "speech_without_source_chain"]:
        ok(item in sg_forbidden, f"sg_forbidden_{item}")
    output_priority_policy = sg.get("output_priority_policy") or {}
    ok(output_priority_policy.get("p0_p1_safety_protection_required") is True, "sg_p0p1_protection")
    ok(output_priority_policy.get("p0_p1_lower_priority_must_not_preempt") is True, "sg_no_lower_preempt")
    ok(output_priority_policy.get("p0_p1_can_abort_lower_priority_output") is True, "sg_p0p1_abort_lower")
    ok(sg.get("stale_safety_speech_historical_only_required") is True, "sg_stale_historical_only")
    ok(sg.get("non_owner_speech_cannot_trigger_output") is True, "sg_non_owner_block")
    ok(sg.get("source_chain_required") is True, "sg_source_chain_required")
    ok(sg.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "sg_source_chain")

    ok(vop.get("input") == "controlled_speech_gate_decision_candidate", "vop_input")
    ok(vop.get("output") == "vop_controlled_event_candidate", "vop_output")
    ok(vop.get("allowed_modes") == ["SHADOW_ONLY", "TEXT_ONLY", "DRY_OUTPUT_PLACEHOLDER"], "vop_allowed_modes")
    forbidden_vop = vop.get("forbidden_modes") or []
    for item in ["REAL_AUDIO_PLAYBACK", "REAL_TTS_STREAM", "UNCONTROLLED_AUDIO"]:
        ok(item in forbidden_vop, f"vop_forbidden_{item}")
    ok(vop.get("must_preserve_speech_request_id") is True, "vop_preserve_request_id")
    ok(vop.get("must_preserve_source_chain") is True, "vop_preserve_source_chain")
    ok(vop.get("must_expose_output_boundary_flags") is True, "vop_expose_boundary_flags")
    ok(vop.get("no_audio_device_call") is True, "vop_no_audio_device")
    ok(vop.get("no_tts_engine_call") is True, "vop_no_tts_engine")
    ok(vop.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "vop_source_chain")

    ok(tts.get("dry_tts_placeholder_allowed_later") is True, "tts_dry_allowed_later")
    ok(tts.get("real_tts_invocation_allowed_now") is False, "tts_real_now_false")
    ok(tts.get("local_audio_playback_allowed_now") is False, "tts_local_audio_false")
    ok(tts.get("external_tts_api_allowed") is False, "tts_external_api_false")
    ok(tts.get("text_only_output_preferred_for_first_controlled_output") is True, "tts_text_only_preferred")
    ok(isinstance(tts.get("max_output_length_chars"), int) and tts.get("max_output_length_chars") > 0, "tts_max_output_length")
    ok(isinstance(tts.get("max_output_events_per_run"), int) and tts.get("max_output_events_per_run") > 0, "tts_max_events")
    ok(
        tts.get("p0_p1_output_preemption_policy") == "P0_P1_PREEMPT_LOWER_PRIORITY_OUTPUTS",
        "tts_p0p1_preemption_policy",
    )
    ok(tts.get("interruption_stop_pause_resume_only_as_candidate") is True, "tts_interruption_candidate_only")
    ok(tts.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "tts_source_chain")

    allowed_visible = boundary.get("allowed_user_visible_outputs") or []
    for item in [
        "console_text_line",
        "structured_jsonl_event",
        "dry_speech_text_preview",
        "controlled_debug_panel_entry",
    ]:
        ok(item in allowed_visible, f"boundary_allowed_{item}")
    forbidden_visible = boundary.get("forbidden_user_visible_outputs") or []
    for item in [
        "real_audio_output",
        "navigation_instruction_execution",
        "route_modification",
        "external_notification",
        "mobile_push",
        "device_vibration",
        "haptic_output",
        "worldmodel_memory_fact_write",
    ]:
        ok(item in forbidden_visible, f"boundary_forbidden_{item}")
    ok(boundary.get("text_only_first_trial_required") is True, "boundary_text_only_first_trial")
    ok(boundary.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "boundary_source_chain")

    conditions = aborts.get("conditions") or []
    for item in [
        "speech_request_missing_source_chain",
        "speech_gate_decision_missing_source_chain",
        "vop_event_missing_source_chain",
        "real_tts_invoked",
        "audio_output_invoked",
        "speech_gate_runtime_invoked_unexpectedly",
        "vop_runtime_invoked_unexpectedly",
        "uncontrolled_output_mode_detected",
        "p0_safety_suppressed_by_lower_priority",
        "stale_safety_speech_output_as_current_fact",
        "non_owner_voice_triggers_output",
        "worldmodel_memory_fact_write",
        "task_state_commit",
        "navigation_action_triggered",
        "external_api_invoked",
    ]:
        ok(item in conditions, f"abort_condition_{item}")
    ok(aborts.get("abort_on_uncontrolled_output") is True, "abort_on_uncontrolled_output")
    ok(aborts.get("abort_on_missing_source_chain") is True, "abort_on_missing_source_chain")
    ok(aborts.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "aborts_source_chain")

    recovery_steps = recovery.get("steps") or []
    for item in [
        "abort_output",
        "write_abort_report",
        "disable_controlled_output_flag",
        "return_to_shadow_only_mode",
        "preserve_logs",
        "require_manual_review",
        "no_state_rollback_needed_because_no_state_commit_allowed",
    ]:
        ok(item in recovery_steps, f"recovery_step_{item}")
    ok(recovery.get("recovery_returns_to_shadow_only") is True, "recovery_returns_to_shadow_only")
    ok(recovery.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "recovery_source_chain")

    required_fields = obs.get("required_fields") or []
    for item in [
        "run_id",
        "source_chain",
        "speech_request_id",
        "speech_gate_decision_id",
        "vop_event_id",
        "output_mode",
        "priority",
        "safety_status",
        "ownership_status",
        "interruption_status",
        "freshness_status",
        "boundary_flags",
        "abort_flags",
        "output_length",
        "output_event_count",
        "final_output_decision",
    ]:
        ok(item in required_fields, f"obs_required_{item}")
    ok(obs.get("source_chain_required_for_every_output_contract") is True, "obs_source_chain_required")
    ok(obs.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "obs_source_chain")

    go_conditions = go_no_go.get("go_conditions") or []
    no_go_conditions = go_no_go.get("no_go_conditions") or []
    for item in [
        "controlled_output_definition_generated",
        "speech_gate_controlled_output_contract_defined",
        "vop_controlled_output_contract_defined",
        "tts_placeholder_policy_defined",
        "user_visible_output_boundary_defined",
        "output_abort_conditions_defined",
        "output_recovery_policy_defined",
        "controlled_output_observability_defined",
        "no_real_output_enabled",
        "no_runtime_invoked",
        "no_write_occurred",
        "boundary_ok_true",
    ]:
        ok(item in go_conditions, f"go_condition_{item}")
    for item in [
        "any_real_audio_output_allowed_now",
        "real_tts_allowed_now",
        "vop_runtime_allowed_now",
        "speech_gate_runtime_allowed_now",
        "missing_source_chain_requirement",
        "no_abort_policy",
        "no_recovery_policy",
        "p0_p1_safety_protection_missing",
        "stale_safety_speech_protection_missing",
        "non_owner_output_protection_missing",
        "external_api_side_effect_allowed",
        "memory_worldmodel_fact_write_allowed",
    ]:
        ok(item in no_go_conditions, f"no_go_condition_{item}")
    ok(go_no_go.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "go_no_go_source_chain")

    ok(
        next_phase.get("next_phase_recommendation")
        == "Phase-Minimal-Runtime-Integration-Text-Only-Controlled-Output-Trial-v1-001",
        "next_phase_recommendation",
    )
    ok(next_phase.get("must_not_recommend_live_audio") is True, "must_not_recommend_live_audio")
    ok(next_phase.get("must_not_recommend_camera_enablement") is True, "must_not_recommend_camera_enablement")
    ok(next_phase.get("must_not_recommend_map_api_enablement") is True, "must_not_recommend_map_api_enablement")
    ok(
        next_phase.get("must_not_recommend_memory_or_worldmodel_write") is True,
        "must_not_recommend_memory_or_worldmodel_write",
    )
    ok(bool(next_phase.get("rationale")), "next_phase_rationale")
    ok(next_phase.get("source_chain") == "minimal_runtime_integration_controlled_output_definition_v1", "next_phase_source_chain")

    for report_key in ["no_runtime_boundary_report", "no_write_boundary_report"]:
        report = data[report_key]
        ok(report.get("definition_only") is True, f"{report_key}_definition_only")
        ok(report.get("controlled_output_enabled") is False, f"{report_key}_controlled_output_enabled")
        ok(report.get("controlled_output_executed") is False, f"{report_key}_controlled_output_executed")
        ok(report.get("runtime_trial_executed") is False, f"{report_key}_runtime_trial_executed")
        ok(report.get("boundary_ok") is True, f"{report_key}_boundary_ok")
        ok(report.get("violations") == [], f"{report_key}_violations")
        ok(report.get("fact_status") == "not_fact", f"{report_key}_fact_status")
        ok(report.get("write_allowed") is False, f"{report_key}_write_allowed")
        for flag in [
            "runtime_tts_invoked",
            "runtime_audio_output_invoked",
            "speech_gate_runtime_invoked",
            "vop_runtime_invoked",
            "runtime_camera_invoked",
            "runtime_microphone_invoked",
            "runtime_asr_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "task_state_committed_now",
            "navigation_action_triggered",
            "memory_written",
            "world_model_written",
            "fact_written",
        ]:
            ok(report.get(flag) is False, f"{report_key}_{flag}")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks_passed,
        "checks_expected": MIN_CHECKS,
        "blockers": blockers,
        "final_decision": summary.get("final_decision"),
        "phase": "Minimal-Runtime-Integration-Controlled-Output-Definition-v1-001",
    }
    _write_json(smoke_root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
