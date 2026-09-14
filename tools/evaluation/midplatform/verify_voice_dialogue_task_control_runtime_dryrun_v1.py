#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Dialogue Task Control Runtime DryRun v1."""

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

    def ok(c: bool, name: str) -> None:
        nonlocal checks
        if c:
            checks += 1
        else:
            blockers.append(name)

    files = {
        "summary": "voice_dialogue_task_control_runtime_dryrun_v1_summary.json",
        "intake": "voice_dialogue_runtime_input_intake_matrix_v1.json",
        "utterance_set": "voice_dialogue_runtime_simulated_utterance_set_v1.json",
        "intent_collection": "voice_dialogue_runtime_intent_candidate_collection_v1.json",
        "command_collection": "voice_dialogue_runtime_command_candidate_collection_v1.json",
        "policy_matrix": "voice_dialogue_runtime_policy_application_matrix_v1.json",
        "state_trace": "voice_dialogue_runtime_state_dryrun_trace_v1.json",
        "handoff_collection": "voice_dialogue_runtime_handoff_candidate_collection_v1.json",
        "speech_collection": "voice_dialogue_runtime_speech_response_candidate_collection_v1.json",
        "stm_collection": "voice_dialogue_runtime_short_term_context_candidate_collection_v1.json",
        "safety_dryrun": "voice_dialogue_runtime_safety_suppression_dryrun_v1.json",
        "query_status_dryrun": "voice_dialogue_runtime_query_status_dryrun_v1.json",
        "cancel_confirmation_dryrun": "voice_dialogue_runtime_cancel_confirmation_dryrun_v1.json",
        "repeat_guidance_dryrun": "voice_dialogue_runtime_repeat_guidance_dryrun_v1.json",
        "human_assistance_dryrun": "voice_dialogue_runtime_human_assistance_dryrun_v1.json",
        "midplatform_boundary": "voice_dialogue_runtime_midplatform_boundary_check_v1.json",
        "nav_link_check": "voice_dialogue_runtime_navigation_guidance_link_check_v1.json",
        "trace": "voice_dialogue_task_control_runtime_decision_trace_v1.json",
        "final": "voice_dialogue_task_control_runtime_final_decision_v1.json",
        "boundary": "voice_dialogue_task_control_runtime_boundary_report_v1.json",
        "metrics": "voice_dialogue_task_control_runtime_metrics_candidate_report_v1.json",
        "benchmark_link": "voice_dialogue_task_control_runtime_benchmark_link_report_v1.json",
        "health_report": "voice_dialogue_task_control_runtime_system_health_report_v1.json",
        "no_write": "voice_dialogue_task_control_runtime_no_write_boundary_report_v1.json",
        "sim_report": "voice_dialogue_task_control_runtime_simulation_context_report_v1.json",
        "non_claims": "voice_dialogue_task_control_runtime_non_claims_report_v1.json",
        "followups": "voice_dialogue_task_control_runtime_open_followups_v1.json",
        "audit": "voice_dialogue_task_control_runtime_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "voice_dialogue_task_control_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("dryrun_scope") == "voice_dialogue_task_control_runtime_dryrun_only", "scope")
    ok(s.get("based_on_voice_dialogue_contract") is True, "contract")
    ok(s.get("simulated_utterance_set_defined") is True, "utterances")
    ok(s.get("voice_intent_candidates_generated") is True, "intents")
    ok(s.get("task_manager_invoked") is False, "no_tm")
    ok(s.get("task_state_changed_now") is False, "no_task_change")
    ok(s.get("asr_invoked") is False, "no_asr")
    ok(s.get("tts_invoked") is False, "no_tts")

    utts = data["utterance_set"].get("utterances") or []
    ok(len(utts) >= 12, "utterances_12")

    intents = {c.get("normalized_intent_type") for c in data["intent_collection"].get("candidates") or []}
    ok("START_TASK" in intents, "start_task")
    ok("QUERY_TASK_STATUS" in intents, "query")
    ok("REPEAT_LAST_GUIDANCE" in intents, "repeat")
    ok("CANCEL_TASK" in intents, "cancel")
    for ic in data["intent_collection"].get("candidates") or []:
        if ic.get("direct_task_state_change_allowed") is not False:
            blockers.append("direct_change")
            break
    else:
        checks += 1

    for cc in data["command_collection"].get("candidates") or []:
        if cc.get("task_state_changed_now") is not False:
            blockers.append("cmd_changed")
            break
    else:
        checks += 1

    policies = data["policy_matrix"].get("policies") or []
    ok(any(p.get("policy_id") == "safety_suppression_policy" for p in policies), "safety_policy")

    handoffs = data["handoff_collection"].get("candidates") or []
    ok(all(h.get("handoff_invoked_now") is False for h in handoffs), "handoff_not_now")
    ok(all(h.get("task_manager_invoked_now") is False for h in handoffs), "tm_not_now")

    speeches = data["speech_collection"].get("candidates") or []
    ok(len(speeches) > 0, "speech_count")
    ok(all(sp.get("requires_speech_gate") is True for sp in speeches), "speech_gate")
    ok(all(sp.get("tts_invoked_now") is False for sp in speeches), "speech_no_tts")

    stm = data["stm_collection"].get("candidates") or []
    ok(len(stm) > 0, "stm_count")
    ok(all(c.get("memory_scope") == "short_term_only" for c in stm), "stm_scope")

    scenarios = data["safety_dryrun"].get("scenarios") or []
    inactive = next((x for x in scenarios if x.get("safety_alert_active") is False), None)
    active = next((x for x in scenarios if x.get("safety_alert_active") is True), None)
    ok(inactive and inactive.get("dialogue_candidate_allowed") is True, "safety_false_ok")
    ok(active and active.get("repeat_allowed") is False, "safety_true_repeat")

    qs = data["query_status_dryrun"]
    ok(qs.get("status_response_must_not_expose_internal_debug") is True, "no_debug")

    cc = data["cancel_confirmation_dryrun"]
    ok(cc.get("cancel_requires_confirmation") is True, "cancel_confirm")
    ok(cc.get("task_cancelled_now") is False, "not_cancelled")
    ok(cc.get("confirm_cancel_depends_on_pending_context") is True, "pending_ctx")

    rep = data["repeat_guidance_dryrun"]
    ok(rep.get("short_term_context_required") is True, "repeat_stm")

    ha = data["human_assistance_dryrun"]
    ok(ha.get("navigation_action_triggered") is False, "no_nav")

    mb = data["midplatform_boundary"]
    ok(mb.get("voice_cannot_create_task_directly") is True, "no_create")
    ok(mb.get("voice_cannot_cancel_task_directly") is True, "no_cancel_direct")

    nav = data["nav_link_check"]
    ok(nav.get("dialogue_cannot_trigger_navigation_action_directly") is True, "no_nav_direct")

    final = data["final"]
    ok(
        final.get("final_decision")
        == "VOICE_DIALOGUE_TASK_CONTROL_RUNTIME_DRYRUN_READY_FOR_TASK_MANAGER_INTEGRATION",
        "final",
    )

    ok(data["boundary"].get("runtime_dryrun_only") is True, "dryrun_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 71,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Voice-Dialogue-Task-Control-Runtime-DryRun-v1-001",
    }
    _write_json(root / "voice_dialogue_task_control_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
