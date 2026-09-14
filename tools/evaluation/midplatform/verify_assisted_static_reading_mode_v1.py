#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Assisted Static Reading Mode v1."""

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
        "summary": "assisted_static_reading_mode_v1_summary.json",
        "intake": "assisted_static_reading_input_intake_matrix_v1.json",
        "entry": "assisted_static_reading_mode_entry_policy_v1.json",
        "fsm": "assisted_static_reading_state_machine_v1.json",
        "readiness": "assisted_static_reading_readiness_gate_v1.json",
        "quality": "assisted_static_capture_quality_requirement_v1.json",
        "guidance": "assisted_static_reading_user_guidance_sequence_v1.json",
        "self_adj": "assisted_static_reading_system_self_adjustment_policy_v1.json",
        "ocr_gate": "assisted_static_reading_ocrrequest_future_gate_v1.json",
        "pipeline": "assisted_static_reading_result_pipeline_plan_v1.json",
        "exit_pol": "assisted_static_reading_exit_fallback_escalation_policy_v1.json",
        "expired": "assisted_static_reading_expired_candidate_policy_v1.json",
        "current": "assisted_static_reading_current_case_decision_v1.json",
        "voice": "assisted_static_reading_voice_guidance_link_report_v1.json",
        "vc": "assisted_static_reading_vision_capture_link_report_v1.json",
        "boundary": "assisted_static_reading_boundary_report_v1.json",
        "metrics": "assisted_static_reading_metrics_candidate_report_v1.json",
        "bench": "assisted_static_reading_benchmark_link_report_v1.json",
        "health": "assisted_static_reading_system_health_link_report_v1.json",
        "no_write": "assisted_static_reading_no_write_boundary_report_v1.json",
        "sim": "assisted_static_reading_simulation_context_report_v1.json",
        "non_claims": "assisted_static_reading_non_claims_report_v1.json",
        "followups": "assisted_static_reading_open_followups_v1.json",
        "audit": "assisted_static_reading_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "assisted_static_reading_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    entry = data["entry"]
    fsm = data["fsm"]
    readiness = data["readiness"]
    quality = data["quality"]
    guidance = data["guidance"]
    self_adj = data["self_adj"]
    ocr_gate = data["ocr_gate"]
    pipeline = data["pipeline"]
    exit_pol = data["exit_pol"]
    expired = data["expired"]
    current = data["current"]
    voice = data["voice"]
    vc = data["vc"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary")
    ok(s.get("mode_scope") == "assisted_static_reading_mode_policy_only", "scope")
    ok(s.get("based_on_voice_output_plane_adapter") is True, "based_vop")
    ok(s.get("assisted_static_reading_mode_defined") is True, "mode_def")
    ok(s.get("ocrrequest_future_gate_defined") is True, "ocr_gate_def")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")
    ok(s.get("runtime_ocr_invoked") is False, "no_ocr")
    ok(s.get("ocrrequest_generated") is False, "no_ocrreq")

    entries = {e.get("entry_condition"): e for e in entry.get("entries") or [] if isinstance(e, dict)}
    ok(entries.get("repeated_dynamic_empty", {}).get("allowed_entry") is True, "entry_dynamic")
    ok(entries.get("same_bbox_no_gain", {}).get("allowed_entry") is True, "entry_bbox")

    states = fsm.get("states") or []
    ok("WAITING_FOR_USER_STABILIZATION" in states, "state_stabilize")
    ok("STATIC_CAPTURE_READY_CANDIDATE" in states, "state_capture")
    ok("OCRREQUEST_READY_CANDIDATE" in states, "state_ocr_ready")

    dims = {d.get("readiness_dimension"): d for d in readiness.get("dimensions") or [] if isinstance(d, dict)}
    for dim in ("user_stability", "target_centering", "viewing_angle", "distance_and_scale", "lighting_and_clarity"):
        ok(dim in dims, dim)

    ok(quality.get("threshold_is_policy_placeholder") is True, "quality_placeholder")

    steps = guidance.get("steps") or []
    ok(any(st.get("action_id") == "hold_still" for st in steps if isinstance(st, dict)), "hold_still_step")
    ok(all(st.get("tts_invoked_now") is False for st in steps if isinstance(st, dict)), "guidance_no_tts")

    adj_ids = [c.get("action_id") for c in self_adj.get("candidates") or [] if isinstance(c, dict)]
    ok("request_zoom" in adj_ids and "request_autofocus" in adj_ids, "self_adj_zoom_af")

    ok(ocr_gate.get("ocrrequest_generated_now") is False, "gate_no_gen")
    phases = [st.get("future_phase") for st in pipeline.get("steps") or [] if isinstance(st, dict)]
    ok("OCRRequest-Gated-Submission-from-StaticReading-v1" in phases, "pipeline_ocr_static")

    routes = [r.get("route_to") for r in exit_pol.get("routes") or [] if isinstance(r, dict)]
    ok("EXTERNAL_ASSISTANCE_CANDIDATE" in routes or "VISUAL_SEMANTIC_FALLBACK" in routes, "exit_routes")

    ok(any(c.get("can_feed_long_term_candidate") is True for c in expired.get("candidates") or [] if isinstance(c, dict)), "expired_lt")

    ok(current.get("mode_entry_decision") == "ENTER_ASSISTED_STATIC_READING_CANDIDATE", "mode_entry")
    ok(current.get("first_prompt_text"), "first_prompt")
    ok(voice.get("first_prompt_ready_as_speech_request_candidate") is True, "voice_ready")
    ok(vc.get("static_capture_required") is True, "static_required")
    ok(boundary.get("mode_policy_only") is True, "boundary_policy")
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
    report = {"verdict": verdict, "checks_passed": checks, "checks_expected": 66, "blockers": blockers, "phase": "Assisted-Static-Reading-Mode-v1-001"}
    _write_json(root / "assisted_static_reading_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
