#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for User Guidance Recovery Runtime DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List


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
        "summary": "user_guidance_recovery_runtime_dryrun_v1_summary.json",
        "intake": "user_guidance_runtime_input_intake_matrix_v1.json",
        "triggers": "user_guidance_trigger_evaluation_matrix_v1.json",
        "plan": "user_guidance_runtime_plan_v1.json",
        "prompts": "user_guidance_prompt_candidate_matrix_v1.json",
        "transitions": "user_guidance_response_state_transition_dryrun_v1.json",
        "static": "user_guidance_static_capture_entry_candidate_v1.json",
        "sys": "user_guidance_system_self_adjustment_escalation_candidate_v1.json",
        "ext": "user_guidance_external_assistance_escalation_candidate_v1.json",
        "vis": "user_guidance_visual_semantic_fallback_candidate_v1.json",
        "expired": "user_guidance_expired_long_term_context_candidate_v1.json",
        "trace": "user_guidance_runtime_decision_trace_v1.json",
        "final": "user_guidance_final_dryrun_decision_v1.json",
        "boundary": "user_guidance_runtime_boundary_report_v1.json",
        "metrics": "user_guidance_runtime_metrics_candidate_report_v1.json",
        "bench": "user_guidance_runtime_benchmark_link_report_v1.json",
        "health": "user_guidance_runtime_system_health_link_report_v1.json",
        "no_write": "user_guidance_runtime_no_write_boundary_report_v1.json",
        "sim": "user_guidance_runtime_simulation_context_report_v1.json",
        "non_claims": "user_guidance_runtime_non_claims_report_v1.json",
        "followups": "user_guidance_runtime_open_followups_v1.json",
        "audit": "user_guidance_runtime_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(
            root / "user_guidance_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    triggers = data["triggers"]
    plan = data["plan"]
    prompts = data["prompts"]
    transitions = data["transitions"]
    static = data["static"]
    sys_esc = data["sys"]
    ext = data["ext"]
    vis = data["vis"]
    expired = data["expired"]
    trace = data["trace"]
    final = data["final"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "user_guidance_recovery_runtime_decision_dryrun_only", "scope")
    ok(s.get("based_on_vision_capture_runtime_dryrun") is True, "based_vc_rt")
    ok(s.get("current_case_loaded") is True, "case_loaded")
    ok(s.get("vision_capture_decision_observed") == "USER_GUIDANCE_OR_STATIC_CAPTURE", "vc_decision")
    ok(s.get("internal_recrop_should_stop") is True, "recrop_stop")
    ok(s.get("dynamic_reocr_allowed_now") is False, "no_reocr")
    ok(s.get("guidance_plan_generated") is True, "plan_gen")
    ok(s.get("prompt_candidate_generated") is True, "prompt_gen")
    ok(s.get("user_response_state_transition_generated") is True, "fsm_gen")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("runtime_guidance_action_committed") is False, "no_guidance_action")

    loaded = sum(1 for r in data["intake"].get("rows") or [] if isinstance(r, dict) and r.get("loaded"))
    ok(loaded >= 8, "intake_loaded")

    trows = {r.get("trigger_id"): r for r in triggers.get("rows") or [] if isinstance(r, dict)}
    for tid in ("repeated_dynamic_empty", "same_bbox_no_gain", "internal_retry_limit_reached"):
        ok(trows.get(tid, {}).get("active") is True, tid)

    actions = plan.get("selected_guidance_actions") or []
    for aid in ("ask_user_hold_still", "ask_user_center_target", "ask_user_pause_for_static_capture"):
        ok(aid in actions, aid)

    prows = prompts.get("rows") or []
    ok(all(r.get("tts_invoked_now") is False for r in prows if isinstance(r, dict)), "prompt_no_tts")
    ok(all(r.get("voice_output_plane_invoked_now") is False for r in prows if isinstance(r, dict)), "prompt_no_vop")

    states = transitions.get("states") or []
    ok("WAITING_FOR_USER_ACTION" in states, "waiting_state")
    ok("STATIC_CAPTURE_CANDIDATE" in states, "static_state")
    ok(
        all(t.get("runtime_state_changed_now") is False for t in transitions.get("transitions") or [] if isinstance(t, dict)),
        "no_state_change",
    )

    ok(static.get("runtime_capture_invoked") is False, "static_no_capture")
    ok(
        all(c.get("hardware_action_invoked_now") is False for c in sys_esc.get("candidates") or [] if isinstance(c, dict)),
        "sys_no_hw",
    )
    ok(all(c.get("action_committed_now") is False for c in ext.get("candidates") or [] if isinstance(c, dict)), "ext_no_action")
    ok(vis.get("ocr_default_off_for_world_modeling_respected") is True, "ocr_default_off")
    ok(
        any(c.get("can_feed_long_term_candidate") is True for c in expired.get("candidates") or [] if isinstance(c, dict)),
        "lt_feed",
    )

    steps = {st.get("step_name"): st for st in trace.get("steps") or [] if isinstance(st, dict)}
    ok("generate_final_guidance_dryrun_decision" in steps, "final_step")
    ok(final.get("selected_primary_path") == "ASSISTED_STATIC_CAPTURE_GUIDANCE", "primary_path")

    ok(boundary.get("runtime_dryrun_only") is True, "dryrun_only")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("recovery_action_committed") is False, "health_no_recovery")
    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_scene")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "phase": "User-Guidance-Recovery-Runtime-DryRun-v1-001",
    }
    _write_json(root / "user_guidance_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
