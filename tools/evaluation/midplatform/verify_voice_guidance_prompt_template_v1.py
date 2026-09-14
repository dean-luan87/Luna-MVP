#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Guidance Prompt Template v1."""

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


def _action_ids(matrix: Dict[str, Any]) -> List[str]:
    return [t.get("action_id") for t in matrix.get("templates") or [] if isinstance(t, dict)]


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
        "summary": "voice_guidance_prompt_template_v1_summary.json",
        "integration": "voice_guidance_trigger_governance_integration_report_v1.json",
        "priority": "voice_guidance_speech_priority_policy_v1.json",
        "templates": "voice_guidance_prompt_template_matrix_v1.json",
        "safety": "voice_guidance_prompt_safety_constraint_matrix_v1.json",
        "stm": "voice_guidance_short_term_memory_mount_contract_v1.json",
        "repeat": "voice_guidance_repeat_on_user_inquiry_policy_v1.json",
        "cooldown": "voice_guidance_cooldown_repetition_policy_v1.json",
        "selection": "voice_guidance_prompt_candidate_selection_policy_v1.json",
        "adapter": "voice_guidance_voice_output_plane_adapter_placeholder_v1.json",
        "state": "voice_guidance_prompt_runtime_state_placeholder_v1.json",
        "current": "voice_guidance_current_case_prompt_dryrun_v1.json",
        "boundary": "voice_guidance_prompt_template_boundary_report_v1.json",
        "metrics": "voice_guidance_prompt_template_metrics_candidate_report_v1.json",
        "bench": "voice_guidance_prompt_template_benchmark_link_report_v1.json",
        "health": "voice_guidance_prompt_template_system_health_link_report_v1.json",
        "no_write": "voice_guidance_prompt_template_no_write_boundary_report_v1.json",
        "sim": "voice_guidance_prompt_template_simulation_context_report_v1.json",
        "non_claims": "voice_guidance_prompt_template_non_claims_report_v1.json",
        "followups": "voice_guidance_prompt_template_open_followups_v1.json",
        "audit": "voice_guidance_prompt_template_audit_report_v1.json",
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
            root / "voice_guidance_prompt_template_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "checks_expected": 65, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ig = data["integration"]
    pri = data["priority"]
    tmpl = data["templates"]
    safety = data["safety"]
    stm = data["stm"]
    rep = data["repeat"]
    sel = data["selection"]
    adp = data["adapter"]
    st = data["state"]
    cur = data["current"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("template_scope") == "voice_guidance_prompt_template_only", "scope")
    ok(s.get("based_on_user_guidance_runtime_dryrun") is True, "based_ug_rt")
    ok(s.get("voice_trigger_governance_integration_defined") is True, "gov_int")
    ok(s.get("speech_priority_policy_defined") is True, "pri_def")
    ok(s.get("safety_priority_above_guidance") is True, "safety_above")
    ok(s.get("short_term_memory_mount_defined") is True, "stm_def")
    ok(s.get("repeat_on_user_inquiry_policy_defined") is True, "repeat_def")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("speech_request_submitted") is False, "no_speech_req")

    ok(ig.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")
    ok(ig.get("direct_voice_output_plane_bypass_forbidden") is True, "no_vop_bypass")

    levels = {x.get("priority_level"): x for x in pri.get("levels") or [] if isinstance(x, dict)}
    ok("P0_SAFETY_CRITICAL" in levels, "p0")
    ok("P3_OCR_GUIDANCE" in levels, "p3")
    p0 = levels.get("P0_SAFETY_CRITICAL") or {}
    p3 = levels.get("P3_OCR_GUIDANCE") or {}
    ok(p0.get("can_interrupt_lower_priority") is True, "p0_interrupts")
    ok("P0_SAFETY_CRITICAL" in (p3.get("can_be_interrupted_by") or []), "p3_interrupted_by_p0")

    aids = _action_ids(tmpl)
    for aid in ("hold_still", "center_target", "pause_for_static_capture", "ask_external_assistance"):
        ok(aid in aids, aid)
    ok(all(t.get("tts_invoked_now") is False for t in tmpl.get("templates") or [] if isinstance(t, dict)), "tmpl_no_tts")

    cids = [c.get("constraint_id") for c in safety.get("constraints") or [] if isinstance(c, dict)]
    ok("do_not_interrupt_safety_alert" in cids, "no_interrupt_safety")
    ok("do_not_claim_success" in cids, "no_claim_success")

    ok(stm.get("memory_scope") == "short_term_only", "stm_scope")
    ok("guidance_session_id" in (stm.get("field_list") or []), "session_id")
    ok("last_prompt_text" in (stm.get("field_list") or []), "last_text")
    ok("prompt_repeat_count" in (stm.get("field_list") or []), "repeat_count")

    ok(rep.get("repeat_allowed_when_user_asks") is True, "repeat_on_ask")
    ok(data["cooldown"].get("allow_repeat_on_user_inquiry") is True, "cooldown_inquiry")

    ok(sel.get("selected_primary_prompt_action") == "hold_still", "primary_hold")
    ok(sel.get("selected_priority") == "P3_OCR_GUIDANCE", "sel_p3")

    ok(adp.get("current_phase_invoked") is False, "adp_not_invoked")
    ok("USER_ASKED_REPEAT" in (st.get("states") or []), "user_asked_repeat_state")

    ok(cur.get("selected_prompt_text"), "selected_text")
    ok(cur.get("speech_request_submitted_now") is False, "cur_no_speech")
    ok(cur.get("tts_invoked_now") is False, "cur_no_tts")

    ok(boundary.get("template_only") is True, "boundary_template")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass_rate")
    ok(bench.get("benchmark_score_generated") is False, "no_bench_score")
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
        "checks_expected": 65,
        "blockers": blockers,
        "phase": "Voice-Guidance-Prompt-Template-v1-001",
    }
    _write_json(root / "voice_guidance_prompt_template_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
