#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Dialogue Task Control Contract v1."""

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
        "summary": "voice_dialogue_task_control_contract_v1_summary.json",
        "intake": "voice_dialogue_task_control_input_intake_matrix_v1.json",
        "intent_schema": "voice_dialogue_intent_candidate_schema_v1.json",
        "command_schema": "voice_dialogue_task_control_command_candidate_schema_v1.json",
        "handoff_policy": "voice_dialogue_to_task_handoff_policy_v1.json",
        "short_term_context": "voice_dialogue_short_term_context_policy_v1.json",
        "repeat_pause_resume_cancel": "voice_dialogue_repeat_pause_resume_cancel_policy_v1.json",
        "query_status": "voice_dialogue_query_status_policy_v1.json",
        "task_clarification": "voice_dialogue_task_clarification_policy_v1.json",
        "safety_priority": "voice_dialogue_safety_priority_suppression_policy_v1.json",
        "speech_gate_vop": "voice_dialogue_speech_gate_vop_output_policy_v1.json",
        "template_matrix": "voice_dialogue_minimal_template_matrix_v1.json",
        "state_machine": "voice_dialogue_state_machine_contract_v1.json",
        "future_dryrun": "voice_dialogue_task_control_future_runtime_dryrun_entrypoint_v1.json",
        "midplatform_boundary": "voice_dialogue_midplatform_task_manager_boundary_v1.json",
        "nav_link": "voice_dialogue_navigation_guidance_link_policy_v1.json",
        "trace": "voice_dialogue_task_control_decision_trace_v1.json",
        "final": "voice_dialogue_task_control_final_decision_v1.json",
        "boundary": "voice_dialogue_task_control_boundary_report_v1.json",
        "metrics": "voice_dialogue_task_control_metrics_candidate_report_v1.json",
        "benchmark_link": "voice_dialogue_task_control_benchmark_link_report_v1.json",
        "health_report": "voice_dialogue_task_control_system_health_report_v1.json",
        "no_write": "voice_dialogue_task_control_no_write_boundary_report_v1.json",
        "sim_report": "voice_dialogue_task_control_simulation_context_report_v1.json",
        "non_claims": "voice_dialogue_task_control_non_claims_report_v1.json",
        "followups": "voice_dialogue_task_control_open_followups_v1.json",
        "audit": "voice_dialogue_task_control_audit_report_v1.json",
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
            root / "voice_dialogue_task_control_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("contract_scope") == "voice_dialogue_task_control_contract_only", "scope")
    ok(s.get("based_on_basic_functional_loop_plan") is True, "loop_plan")
    ok(s.get("voice_dialogue_contract_defined") is True, "contract_def")
    ok(s.get("voice_input_runtime_invoked") is False, "no_voice_rt")
    ok(s.get("asr_invoked") is False, "no_asr")
    ok(s.get("task_state_changed_now") is False, "no_task_change")

    intents = data["intent_schema"].get("intent_types") or []
    ok("START_TASK" in intents, "start_task")
    ok("CANCEL_TASK" in intents, "cancel_task")
    ok("REPEAT_LAST_GUIDANCE" in intents, "repeat")
    ok(data["intent_schema"].get("requires_midplatform_decision") is True, "mp_decision")
    ok(data["intent_schema"].get("direct_task_state_change_allowed") is False, "no_direct")

    cmds = data["command_schema"].get("command_types") or []
    ok("CREATE_TASK_CANDIDATE" in cmds, "create_cmd")
    ok("CANCEL_TASK_CANDIDATE" in cmds, "cancel_cmd")
    ok(data["command_schema"].get("midplatform_task_manager_required") is True, "mp_tm")

    hp = data["handoff_policy"]
    ok(hp.get("voice_intent_cannot_mutate_task_state_directly") is True, "no_mutate")

    st = data["short_term_context"]
    ok(st.get("memory_scope") == "short_term_only", "stm_scope")

    rpc = data["repeat_pause_resume_cancel"]
    ok(rpc.get("cancel_task_requires_confirmation") is True, "cancel_confirm")

    qs = data["query_status"]
    ok(qs.get("status_response_must_not_expose_internal_debug") is True, "no_debug")

    tc = data["task_clarification"]
    ok(tc.get("user_response_is_not_fact_by_default") is True, "user_not_fact")

    saf = data["safety_priority"]
    ok(saf.get("safety_alert_priority_above_dialogue") is True, "safety_prio")

    sg = data["speech_gate_vop"]
    ok(sg.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")
    ok(sg.get("direct_vop_bypass_forbidden") is True, "no_vop_bypass")

    ok(len(data["template_matrix"].get("templates") or []) >= 10, "templates_10")

    fd = data["future_dryrun"]
    ok(fd.get("recommended_next_phase") == "Voice-Dialogue-Task-Control-Runtime-DryRun-v1", "next_phase")

    mb = data["midplatform_boundary"]
    ok(mb.get("voice_cannot_create_task_directly") is True, "no_create")
    ok(mb.get("voice_cannot_cancel_task_directly") is True, "no_cancel_direct")

    nav = data["nav_link"]
    ok(nav.get("dialogue_cannot_trigger_navigation_action_directly") is True, "no_nav_direct")

    final = data["final"]
    ok(final.get("final_decision") == "VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_READY", "final")

    ok(data["boundary"].get("contract_only") is True, "contract_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim_report"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 69,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "Voice-Dialogue-Task-Control-Contract-v1-001",
    }
    _write_json(root / "voice_dialogue_task_control_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
