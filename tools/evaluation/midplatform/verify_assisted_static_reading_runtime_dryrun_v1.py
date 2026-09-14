#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Assisted Static Reading Runtime DryRun v1."""

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
        "summary": "assisted_static_reading_runtime_dryrun_v1_summary.json",
        "intake": "assisted_static_reading_runtime_input_intake_matrix_v1.json",
        "mode_entry": "assisted_static_reading_runtime_mode_entry_evaluation_v1.json",
        "state_trace": "assisted_static_reading_runtime_state_machine_trace_v1.json",
        "readiness": "assisted_static_reading_runtime_readiness_evaluation_matrix_v1.json",
        "guidance": "assisted_static_reading_runtime_guidance_step_candidate_v1.json",
        "static_cap": "assisted_static_reading_runtime_static_capture_ready_candidate_v1.json",
        "ocr_gate": "assisted_static_reading_runtime_ocrrequest_future_gate_evaluation_v1.json",
        "self_adj": "assisted_static_reading_runtime_system_self_adjustment_candidate_v1.json",
        "exit_fb": "assisted_static_reading_runtime_exit_fallback_candidate_v1.json",
        "expired": "assisted_static_reading_runtime_expired_candidate_v1.json",
        "trace": "assisted_static_reading_runtime_decision_trace_v1.json",
        "final": "assisted_static_reading_runtime_final_decision_v1.json",
        "voice": "assisted_static_reading_runtime_voice_vop_link_report_v1.json",
        "vision": "assisted_static_reading_runtime_vision_ocr_stc_link_report_v1.json",
        "boundary": "assisted_static_reading_runtime_boundary_report_v1.json",
        "metrics": "assisted_static_reading_runtime_metrics_candidate_report_v1.json",
        "bench": "assisted_static_reading_runtime_benchmark_link_report_v1.json",
        "health": "assisted_static_reading_runtime_system_health_link_report_v1.json",
        "no_write": "assisted_static_reading_runtime_no_write_boundary_report_v1.json",
        "sim": "assisted_static_reading_runtime_simulation_context_report_v1.json",
        "non_claims": "assisted_static_reading_runtime_non_claims_report_v1.json",
        "followups": "assisted_static_reading_runtime_open_followups_v1.json",
        "audit": "assisted_static_reading_runtime_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "assisted_static_reading_runtime_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    me = data["mode_entry"]
    st = data["state_trace"]
    rd = data["readiness"]
    g = data["guidance"]
    sc = data["static_cap"]
    og = data["ocr_gate"]
    sa = data["self_adj"]
    ex = data["expired"]
    tr = data["trace"]
    final = data["final"]
    voice = data["voice"]
    vision = data["vision"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary")
    ok(s.get("dryrun_scope") == "assisted_static_reading_runtime_dryrun_only", "scope")
    ok(s.get("based_on_assisted_static_reading_mode") is True, "based_asm")
    ok(s.get("mode_entry_decision") == "ENTER_ASSISTED_STATIC_READING_CANDIDATE", "mode_entry")
    ok(s.get("current_state") == "WAITING_FOR_USER_STABILIZATION", "current_state")
    ok(s.get("first_guidance_action") == "hold_still", "hold_still")
    ok(s.get("ocrrequest_eligible_now") is False, "ocr_now_false")
    ok(s.get("ocrrequest_generated_now") is False, "no_ocrreq")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")
    ok(s.get("runtime_ocr_invoked") is False, "no_ocr")

    ok(me.get("entry_allowed") is True, "entry_allowed")
    states_in_trace = [x.get("to_state") for x in st.get("steps") or [] if isinstance(x, dict)]
    ok("WAITING_FOR_USER_STABILIZATION" in states_in_trace or st.get("final_state") == "WAITING_FOR_USER_STABILIZATION", "fsm_wait")

    dims = rd.get("dimensions") or []
    dim_names = {d.get("readiness_dimension") for d in dims if isinstance(d, dict)}
    for dim in ("user_stability", "target_centering", "viewing_angle", "distance_and_scale", "lighting_and_clarity"):
        ok(dim in dim_names, dim)
    ok(not all(d.get("current_phase_passed") is True for d in dims if isinstance(d, dict)), "no_all_passed")

    ok(g.get("prompt_text_candidate"), "prompt_text")
    ok(sc.get("static_capture_ready_now") is False, "cap_not_ready")
    ok(og.get("ocrrequest_eligible_now") is False, "gate_now_false")
    ok(og.get("ocrrequest_eligible_later") is True, "gate_later_true")
    ok(all(c.get("hardware_action_invoked_now") is False for c in sa.get("candidates") or [] if isinstance(c, dict)), "adj_no_hw")
    ok(any(c.get("can_feed_long_term_candidate") is True for c in ex.get("candidates") or [] if isinstance(c, dict)), "expired_lt")
    trace_names = [t.get("step_name") for t in tr.get("steps") or [] if isinstance(t, dict)]
    ok("generate_final_runtime_dryrun_decision" in trace_names, "trace_final_step")
    ok(final.get("final_decision") == "WAIT_FOR_USER_STABILIZATION", "final_decision")
    ok(voice.get("vop_submit_ready_later") is True, "vop_later")
    ok(vision.get("dynamic_reocr_allowed_now") is False, "no_dynamic_reocr")
    ok(boundary.get("runtime_dryrun_only") is True, "boundary_dryrun")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("recovery_action_committed") is False, "no_recovery")
    ok(no_write.get("boundary_ok") is True, "nw_ok")
    ok(no_write.get("violations") == [], "nw_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 67,
        "blockers": blockers,
        "phase": "Assisted-Static-Reading-Runtime-DryRun-v1-001",
    }
    _write_json(root / "assisted_static_reading_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
