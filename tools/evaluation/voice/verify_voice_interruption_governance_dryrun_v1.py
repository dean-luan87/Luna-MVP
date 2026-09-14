#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Interruption Governance DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks
        if cond:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "summary.json",
        "input_root_matrix": "input_root_matrix.json",
        "intent_policy": "interruption_intent_policy.json",
        "priority_policy": "speech_priority_interruption_policy.json",
        "state_schema": "speech_request_state_candidate_schema.json",
        "decision_schema": "interruption_decision_candidate_schema.json",
        "freshness_policy": "freshness_repeat_resume_policy.json",
        "correction_policy": "correction_policy.json",
        "emergency_policy": "emergency_interruption_policy.json",
        "new_task_policy": "new_task_cancel_task_policy.json",
        "source_matrix": "interruption_source_matrix.json",
        "decisions": "interruption_decision_candidates.json",
        "priority_scenarios": "priority_scenario_matrix.json",
        "handoffs": "handoff_contracts.json",
        "boundary": "boundary_report.json",
    }
    data: Dict[str, Any] = {}
    for key, fname in files.items():
        path = root / fname
        if not path.is_file():
            blockers.append(f"missing:{key}")
        else:
            data[key] = json.loads(path.read_text(encoding="utf-8"))

    if blockers:
        report = {"verdict": "NO_GO", "checks_passed": 0, "checks_expected": 64, "blockers": blockers}
        _write_json(root / "verifier_report.json", report)
        print(json.dumps(report, ensure_ascii=False))
        return 2

    summary = data["summary"]
    ok(summary.get("dryrun_scope") == "voice_interruption_governance_dryrun_only", "scope")
    ok(summary.get("ownership_gate_input_loaded") is True, "ownership_loaded")
    ok(summary.get("safety_task_arbitration_input_loaded") is True, "safety_loaded")
    ok(summary.get("interruption_intent_policy_defined") is True, "intent_policy_defined")
    ok(summary.get("speech_priority_policy_defined") is True, "priority_policy_defined")
    ok(summary.get("speech_request_state_candidate_schema_defined") is True, "state_schema_defined")
    ok(summary.get("interruption_decision_candidate_schema_defined") is True, "decision_schema_defined")
    ok(summary.get("freshness_policy_defined") is True, "freshness_defined")
    ok(summary.get("correction_policy_defined") is True, "correction_defined")
    ok(summary.get("emergency_policy_defined") is True, "emergency_defined")
    ok(summary.get("new_task_cancel_task_policy_defined") is True, "new_task_defined")
    ok((summary.get("interruption_decision_candidate_count") or 0) >= 24, "decision_count")
    ok(summary.get("runtime_asr_invoked") is False, "no_asr")
    ok(summary.get("runtime_audio_recorded") is False, "no_audio")
    ok(summary.get("runtime_tts_stopped") is False, "no_tts_stop")
    ok(summary.get("speech_gate_invoked") is False, "no_speech_gate")
    ok(summary.get("vop_invoked") is False, "no_vop")
    ok(summary.get("task_state_committed_now") is False, "no_task_commit")
    ok(summary.get("navigation_action_triggered") is False, "no_nav_action")
    ok(summary.get("ocr_invoked") is False, "no_ocr")
    ok(summary.get("camera_invoked") is False, "no_camera")
    ok(summary.get("memory_written") is False, "no_memory")
    ok(summary.get("world_model_written") is False, "no_world")
    ok(summary.get("scene_delta_generated") is False, "no_scene_delta")
    ok(summary.get("fact_status") == "not_fact", "not_fact")
    ok(summary.get("write_allowed") is False, "no_write")
    ok(summary.get("boundary_ok") is True, "boundary_ok_summary")

    intents = data["intent_policy"].get("interruption_intent_types") or []
    for name in [
        "STOP",
        "PAUSE",
        "REPEAT",
        "RESUME",
        "CLARIFY",
        "CORRECT",
        "EMERGENCY",
        "NEW_TASK",
        "CANCEL_TASK",
        "UNKNOWN_OR_AMBIGUOUS",
    ]:
        ok(name in intents, f"intent_{name}")

    priority_rules = data["priority_policy"].get("priority_rules") or {}
    ok(priority_rules.get("P0_not_cancelled_by_ordinary_stop") is True, "p0_stop")
    ok(priority_rules.get("P1_risk_state_not_deleted") is True, "p1_preserve")
    ok(priority_rules.get("P2_pause_requires_resume_condition") is True, "p2_resume")
    ok(priority_rules.get("P3_resume_requires_stc_frame_region_freshness") is True, "p3_resume")

    states = data["state_schema"].get("states") or []
    ok("expired_before_resume_candidate" in states, "expired_state")

    actions = data["decision_schema"].get("selected_action_candidate_enum") or []
    ok("CREATE_CORRECTION_EVENT_CANDIDATE" in actions, "correction_action")
    ok("CREATE_SAFETY_OBSERVATION_CANDIDATE" in actions, "safety_action")

    freshness = data["freshness_policy"]
    ok(freshness.get("repeat_requires_freshness_check") is True, "repeat_freshness")
    ok(freshness.get("P0_P1_stale_repeat_not_current_fact") is True, "stale_p0p1")
    ok(freshness.get("P2_resume_requires_STC_route_freshness") is True, "p2_stc")
    ok(freshness.get("P3_resume_requires_STC_frame_region_freshness") is True, "p3_stc")

    correction = data["correction_policy"]
    ok(correction.get("correction_event_candidate_only") is True, "correction_candidate_only")
    ok(correction.get("fact_write_forbidden") is True, "correction_no_fact")

    emergency = data["emergency_policy"]
    ok(emergency.get("owner_confirmed_emergency_allowed") is True, "owner_emergency")
    ok(emergency.get("ownership_uncertain_only_safety_observation_candidate") is True, "uncertain_emergency")
    ok(emergency.get("media_public_voice_cannot_control_luna") is True, "media_block")

    new_task = data["new_task_policy"]
    ok(new_task.get("new_task_not_direct_task_commit") is True, "new_task_no_commit")
    ok(new_task.get("cancel_task_not_direct_cancel") is True, "cancel_no_direct")
    ok(new_task.get("pending_confirmation_preserved") is True, "pending_confirmation")
    ok(new_task.get("task_context_preserved") is True, "task_context")

    source_rows = data["source_matrix"].get("rows") or []
    ok(len(source_rows) >= 24, "source_rows")

    decisions = data["decisions"].get("candidates") or []
    ok(len(decisions) >= 24, "decision_rows")
    ok(all(d.get("source_chain") == "voice_interruption_governance_dryrun_v1" for d in decisions), "source_chain")

    case17 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_17"), None)
    ok(case17 and case17.get("selected_action_candidate") == "SUPPRESS_INTERRUPTION_CANDIDATE", "case17_p0_block")
    case18 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_18"), None)
    ok(case18 and case18.get("target_speech_state_candidate") == "paused_candidate", "case18_pause")
    case19 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_19"), None)
    ok(case19 and bool(case19.get("resume_condition")), "case19_resume_condition")
    case20 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_20"), None)
    ok(case20 and "frame_region_freshness" in str(case20.get("resume_condition")), "case20_p3_freshness")
    case24 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_24"), None)
    ok(case24 and case24.get("stale_risk") is True, "case24_stale")
    ok(case24 and case24.get("target_speech_state_candidate") == "expired_before_resume_candidate", "case24_expired")

    case06 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_06"), None)
    ok(case06 and case06.get("selected_action_candidate") == "SUPPRESS_INTERRUPTION_CANDIDATE", "case06_non_owner")
    case09 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_09"), None)
    ok(case09 and "phone_call" in str(case09.get("blocked_reason")), "case09_phone")
    case10 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_10"), None)
    ok(case10 and "human_conversation" in str(case10.get("blocked_reason")), "case10_conversation")
    case11 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_11"), None)
    ok(case11 and case11.get("selected_action_candidate") == "SUPPRESS_INTERRUPTION_CANDIDATE", "case11_media")
    case13 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_13"), None)
    ok(case13 and case13.get("selected_action_candidate") == "CREATE_SAFETY_OBSERVATION_CANDIDATE", "case13_safety")
    case15 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_15"), None)
    ok(case15 and case15.get("selected_action_candidate") == "CREATE_NEW_TASK_CANDIDATE", "case15_new_task")
    case16 = next((d for d in decisions if d.get("interruption_decision_id") == "idc_case_16"), None)
    ok(case16 and case16.get("selected_action_candidate") == "RESUME_SPEECH_CANDIDATE", "case16_resume")

    ok(all(d.get("task_context_preserved") is True for d in decisions), "all_task_context")
    ok(all(d.get("pending_confirmation_preserved") is True for d in decisions), "all_pending_preserved")
    ok(all(d.get("runtime_tts_stopped") is False for d in decisions), "all_no_tts_stop")
    ok(all(d.get("speech_gate_invoked") is False for d in decisions), "all_no_speech_gate")
    ok(all(d.get("vop_invoked") is False for d in decisions), "all_no_vop")
    ok(all(d.get("task_state_committed_now") is False for d in decisions), "all_no_task_commit")
    ok(all(d.get("navigation_action_triggered") is False for d in decisions), "all_no_nav")
    ok(all(d.get("ocr_invoked") is False for d in decisions), "all_no_ocr")
    ok(all(d.get("camera_invoked") is False for d in decisions), "all_no_camera")
    ok(all(d.get("memory_written") is False for d in decisions), "all_no_memory")
    ok(all(d.get("world_model_written") is False for d in decisions), "all_no_world")
    ok(all(d.get("fact_status") == "not_fact" for d in decisions), "all_not_fact")
    ok(all(d.get("write_allowed") is False for d in decisions), "all_no_write")

    priority_scenarios = data["priority_scenarios"].get("rows") or []
    ok(len(priority_scenarios) >= 8, "priority_rows")

    handoffs = data["handoffs"]
    ok("to_safety_task_arbitration_runtime" in handoffs, "handoff_safety")
    ok("to_speech_gate" in handoffs, "handoff_gate")
    ok("to_voice_output_plane" in handoffs, "handoff_vop")
    ok("to_task_manager" in handoffs, "handoff_tm")
    ok("to_stc_ocr_navigation" in handoffs, "handoff_stc")
    ok(handoffs["to_speech_gate"].get("invoked_now") is False, "handoff_gate_not_now")

    boundary = data["boundary"]
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "violations")
    ok(boundary.get("runtime_tts_stopped") is False, "boundary_no_tts_stop")
    ok(boundary.get("speech_gate_invoked") is False, "boundary_no_gate")
    ok(boundary.get("vop_invoked") is False, "boundary_no_vop")
    ok(boundary.get("task_state_committed_now") is False, "boundary_no_commit")
    ok(boundary.get("navigation_action_triggered") is False, "boundary_no_nav")
    ok(boundary.get("memory_written") is False, "boundary_no_memory")
    ok(boundary.get("world_model_written") is False, "boundary_no_world")

    report = {
        "verdict": "GO" if not blockers else "NO_GO",
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "final_decision": "VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_READY_FOR_LOOP_STABILIZATION_TEST",
        "phase": "Voice-Interruption-Governance-DryRun-v1-001",
    }
    _write_json(root / "verifier_report.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
