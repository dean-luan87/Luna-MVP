#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for User Clarification Prompt Runtime DryRun for Reading v1."""

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
        "summary": "user_clarification_prompt_runtime_dryrun_for_reading_v1_summary.json",
        "intake": "user_clarification_prompt_runtime_input_intake_matrix_v1.json",
        "selection": "user_clarification_prompt_runtime_selection_v1.json",
        "priority_safety": "user_clarification_prompt_runtime_priority_safety_check_v1.json",
        "cooldown": "user_clarification_prompt_runtime_cooldown_repeat_check_v1.json",
        "speech_candidate": "user_clarification_prompt_runtime_speech_request_candidate_v1.json",
        "speech_gate": "user_clarification_prompt_runtime_speech_gate_pre_submit_v1.json",
        "vop_candidate": "user_clarification_prompt_runtime_vop_adapter_candidate_v1.json",
        "wait_state": "user_clarification_prompt_runtime_wait_for_user_response_state_v1.json",
        "response_handoff": "user_clarification_prompt_runtime_response_handoff_candidate_v1.json",
        "long_term": "user_clarification_prompt_runtime_long_term_candidate_link_v1.json",
        "trace": "user_clarification_prompt_runtime_decision_trace_v1.json",
        "final": "user_clarification_prompt_runtime_final_decision_v1.json",
        "boundary": "user_clarification_prompt_runtime_boundary_report_v1.json",
        "metrics": "user_clarification_prompt_runtime_metrics_candidate_report_v1.json",
        "bench": "user_clarification_prompt_runtime_benchmark_link_report_v1.json",
        "health": "user_clarification_prompt_runtime_system_health_link_report_v1.json",
        "no_write": "user_clarification_prompt_runtime_no_write_boundary_report_v1.json",
        "sim": "user_clarification_prompt_runtime_simulation_context_report_v1.json",
        "non_claims": "user_clarification_prompt_runtime_non_claims_report_v1.json",
        "followups": "user_clarification_prompt_runtime_open_followups_v1.json",
        "audit": "user_clarification_prompt_runtime_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "user_clarification_prompt_runtime_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(True, "summary")
    ok(s.get("dryrun_scope") == "reading_clarification_prompt_runtime_dryrun_only", "scope")
    ok(s.get("based_on_clarification_prompt_template") is True, "based_uclar")
    ok(s.get("selected_template_type") == "missing_both_task_and_scene", "tpl_type")
    ok(s.get("selected_prompt_text"), "prompt_text")
    ok(s.get("selected_priority") == "P3_OCR_GUIDANCE", "priority")
    ok(s.get("priority_safety_check_executed") is True, "prio_check")
    ok(s.get("cooldown_repeat_check_executed") is True, "cooldown_check")
    ok(s.get("speech_request_candidate_generated") is True, "speech_cand")
    ok(s.get("speech_gate_pre_submit_dryrun_executed") is True, "gate_dryrun")
    ok(s.get("vop_adapter_candidate_generated") is True, "vop_cand")
    ok(s.get("wait_for_user_response_state_generated") is True, "wait_state")
    ok(s.get("user_response_observed") is False, "no_response")
    ok(s.get("task_context_filled_now") is False, "no_task_fill")
    ok(s.get("scene_context_filled_now") is False, "no_scene_fill")
    ok(s.get("task_context_fabricated") is False, "no_task_fab")
    ok(s.get("scene_context_fabricated") is False, "no_scene_fab")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("speech_request_submitted") is False, "no_submit")

    ok(data["priority_safety"].get("can_be_interrupted_by_p0") is True, "p0_interrupt")
    ok(data["speech_candidate"].get("speech_text"), "speech_text_field")
    ok(data["speech_gate"].get("admission_decision") == "ADMIT_AS_CANDIDATE", "admit")
    ok(data["vop_candidate"].get("vop_submit_ready_later") is True, "vop_later")
    ok(data["wait_state"].get("current_state") == "WAIT_FOR_USER_RESPONSE", "wait_state")
    ok(data["response_handoff"].get("handoff_invoked_now") is False, "handoff_not_now")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "WAIT_FOR_USER_RESPONSE", "final_decision")
    ok(data["boundary"].get("runtime_dryrun_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("recovery_action_committed") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_sd")
    ok(data["audit"].get("navigation_decision_invoked") is False, "audit_nav")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 61,
        "blockers": blockers,
        "phase": "User-Clarification-Prompt-Runtime-DryRun-for-Reading-v1-001",
    }
    _write_json(root / "user_clarification_prompt_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
