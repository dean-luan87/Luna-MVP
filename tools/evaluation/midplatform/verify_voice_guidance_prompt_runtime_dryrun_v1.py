#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Guidance Prompt Runtime DryRun v1."""

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
        "summary": "voice_guidance_prompt_runtime_dryrun_v1_summary.json",
        "intake": "voice_guidance_runtime_input_intake_matrix_v1.json",
        "selection": "voice_guidance_runtime_prompt_selection_v1.json",
        "arbitration": "voice_guidance_runtime_priority_arbitration_dryrun_v1.json",
        "safety": "voice_guidance_runtime_safety_suppression_check_v1.json",
        "cooldown": "voice_guidance_runtime_cooldown_repetition_check_v1.json",
        "stm": "voice_guidance_runtime_stm_mount_candidate_v1.json",
        "speech_request": "voice_guidance_runtime_speech_request_candidate_v1.json",
        "speech_gate": "voice_guidance_runtime_speech_gate_pre_submit_dryrun_v1.json",
        "user_inquiry": "voice_guidance_runtime_user_inquiry_repeat_dryrun_v1.json",
        "state": "voice_guidance_runtime_state_dryrun_v1.json",
        "final": "voice_guidance_runtime_final_decision_v1.json",
        "boundary": "voice_guidance_runtime_boundary_report_v1.json",
        "metrics": "voice_guidance_runtime_metrics_candidate_report_v1.json",
        "bench": "voice_guidance_runtime_benchmark_link_report_v1.json",
        "health": "voice_guidance_runtime_system_health_link_report_v1.json",
        "no_write": "voice_guidance_runtime_no_write_boundary_report_v1.json",
        "sim": "voice_guidance_runtime_simulation_context_report_v1.json",
        "non_claims": "voice_guidance_runtime_non_claims_report_v1.json",
        "followups": "voice_guidance_runtime_open_followups_v1.json",
        "audit": "voice_guidance_runtime_audit_report_v1.json",
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
            root / "voice_guidance_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "checks_expected": 64, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    sel = data["selection"]
    arb = data["arbitration"]
    safety = data["safety"]
    cd = data["cooldown"]
    stm = data["stm"]
    sr = data["speech_request"]
    gate = data["speech_gate"]
    inq = data["user_inquiry"]
    st = data["state"]
    final = data["final"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "voice_guidance_prompt_runtime_dryrun_only", "scope")
    ok(s.get("based_on_voice_guidance_prompt_template") is True, "based_template")
    ok(s.get("current_case_loaded") is True, "case_loaded")
    ok(s.get("prompt_candidate_selected") is True, "prompt_selected")
    ok(s.get("selected_prompt_action") == "hold_still", "hold_still")
    ok(s.get("selected_priority") == "P3_OCR_GUIDANCE", "p3")
    ok(s.get("priority_arbitration_dryrun_executed") is True, "arb_exec")
    ok(s.get("safety_suppression_check_executed") is True, "safety_exec")
    ok(s.get("cooldown_repetition_check_executed") is True, "cd_exec")
    ok(s.get("short_term_memory_mount_candidate_generated") is True, "stm_gen")
    ok(s.get("speech_request_candidate_generated") is True, "sr_gen")
    ok(s.get("speech_gate_pre_submit_dryrun_executed") is True, "gate_exec")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("speech_request_submitted") is False, "no_submit")
    ok(s.get("short_term_memory_written") is False, "no_stm_write")

    ok(sel.get("selected_prompt_text"), "selected_text")
    ok(arb.get("incoming_prompt_priority") == "P3_OCR_GUIDANCE", "incoming_p3")
    ok("P0_SAFETY_CRITICAL" in (arb.get("can_be_interrupted_by") or []), "p0_interrupts")
    ok(safety.get("safety_priority_above_guidance") is True, "safety_above")
    ok(cd.get("repeat_allowed_when_user_asks") is True, "repeat_on_ask")
    ok(stm.get("memory_scope") == "short_term_only", "stm_scope")
    ok(stm.get("write_to_runtime_memory_now") is False, "no_stm_write_now")
    ok(sr.get("speech_gate_required") is True, "gate_required")
    ok(sr.get("voice_output_plane_required") is True, "vop_required")
    ok(sr.get("speech_request_submitted_now") is False, "sr_not_submitted")
    ok(gate.get("submit_allowed_later") is True, "submit_later")
    ok(inq.get("repeat_candidate_generated") is True, "inq_repeat")
    ok(inq.get("runtime_repeat_invoked_now") is False, "inq_no_invoke")
    ok("USER_ASKED_REPEAT_CANDIDATE" in (st.get("states") or []), "repeat_state")
    ok(final.get("final_decision") == "GENERATE_SPEECH_REQUEST_CANDIDATE_ONLY", "final_decision")
    ok(boundary.get("runtime_dryrun_only") is True, "boundary_dryrun")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("recovery_action_committed") is False, "no_recovery")
    ok(no_write.get("boundary_ok") is True, "nw_ok")
    ok(no_write.get("violations") == [], "nw_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "phase": "Voice-Guidance-Prompt-Runtime-DryRun-v1-001",
    }
    _write_json(root / "voice_guidance_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
