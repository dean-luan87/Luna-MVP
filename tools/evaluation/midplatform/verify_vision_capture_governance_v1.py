#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision Capture Governance v1."""

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
        "summary": "vision_capture_governance_v1_summary.json",
        "quality": "vision_capture_quality_gate_policy_v1.json",
        "frame": "vision_frame_readiness_gate_v1.json",
        "region": "vision_region_crop_text_readiness_gate_v1.json",
        "dyn_static": "vision_dynamic_vs_static_capture_policy_v1.json",
        "hardware": "vision_capture_hardware_placeholder_contract_v1.json",
        "sys_adj": "vision_capture_system_self_adjustment_policy_v1.json",
        "ug": "vision_capture_user_guidance_policy_v1.json",
        "fail": "vision_capture_failure_reason_taxonomy_v1.json",
        "retry": "vision_capture_retry_timeout_stale_policy_v1.json",
        "expired": "vision_expired_capture_candidate_policy_v1.json",
        "lt": "vision_long_term_context_candidate_routing_policy_v1.json",
        "safety": "vision_safety_marker_capture_path_policy_v1.json",
        "task": "vision_task_triggered_capture_path_policy_v1.json",
        "current": "vision_capture_current_case_decision_dryrun_v1.json",
        "ocr_link": "vision_capture_ocr_activation_link_report_v1.json",
        "stc_link": "vision_capture_stc_link_report_v1.json",
        "boundary": "vision_capture_governance_boundary_report_v1.json",
        "metrics": "vision_capture_governance_metrics_candidate_report_v1.json",
        "bench": "vision_capture_governance_benchmark_link_report_v1.json",
        "health": "vision_capture_governance_system_health_link_report_v1.json",
        "no_write": "vision_capture_governance_no_write_boundary_report_v1.json",
        "sim": "vision_capture_governance_simulation_context_report_v1.json",
        "non_claims": "vision_capture_governance_non_claims_report_v1.json",
        "followups": "vision_capture_governance_open_followups_v1.json",
        "audit": "vision_capture_governance_audit_report_v1.json",
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
            root / "vision_capture_governance_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    quality = data["quality"]
    frame = data["frame"]
    region = data["region"]
    dyn = data["dyn_static"]
    hw = data["hardware"]
    sys_adj = data["sys_adj"]
    ug = data["ug"]
    fail = data["fail"]
    retry = data["retry"]
    expired = data["expired"]
    lt = data["lt"]
    safety = data["safety"]
    task = data["task"]
    current = data["current"]
    ocr_link = data["ocr_link"]
    stc_link = data["stc_link"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("governance_scope") == "vision_capture_governance_policy_only", "scope")
    ok(s.get("based_on_ocr_activation_governance") is True, "based_ocr_act")
    ok(s.get("based_on_stc_sampling_guidance") is True, "based_stc")
    ok(s.get("based_on_user_guidance_recovery") is True, "based_ug")
    ok(s.get("capture_quality_gate_defined") is True, "quality_def")
    ok(s.get("frame_readiness_gate_defined") is True, "frame_def")
    ok(s.get("region_readiness_gate_defined") is True, "region_def")
    ok(s.get("crop_readiness_gate_defined") is True, "crop_def")
    ok(s.get("text_region_capture_readiness_defined") is True, "text_region_def")
    ok(s.get("hardware_capability_placeholder_defined") is True, "hw_def")
    ok(s.get("runtime_camera_invoked") is False, "no_camera")
    ok(s.get("runtime_frame_captured") is False, "no_frame")
    ok(s.get("runtime_ocr_invoked") is False, "no_ocr")

    gate_names = {g.get("gate_name") for g in quality.get("gates") or [] if isinstance(g, dict)}
    dims = set()
    for g in quality.get("gates") or []:
        if isinstance(g, dict):
            dims.update(g.get("quality_dimensions") or [])
    for d in ("blur", "brightness", "target_centering", "perspective_angle"):
        ok(d in dims, d)
    ok("frame_quality_gate" in gate_names, "frame_gate")

    ok(frame.get("stale_allows_long_term_candidate") is True, "frame_stale_lt")

    reg = region.get("region_readiness") or {}
    ok(reg.get("projection_crop_is_not_detected_text_region") is True, "proj_not_detected")
    ok(reg.get("detected_region_preferred") is True, "detected_preferred")

    static = dyn.get("static_capture_required_for") or []
    ok("repeated_dynamic_empty" in static, "repeated_dynamic_static")

    cap_names = {c.get("capability_name") for c in hw.get("capabilities") or [] if isinstance(c, dict)}
    ok("zoom_available" in cap_names, "zoom_avail")
    ok("depth_or_tof_available" in cap_names, "depth_tof")
    ok(hw.get("hardware_capability_unknown_allowed") is True, "hw_unknown_ok")

    sys_ids = {a.get("action_id") for a in sys_adj.get("actions") or [] if isinstance(a, dict)}
    for aid in ("request_zoom", "request_autofocus", "request_resampling"):
        ok(aid in sys_ids, aid)

    ug_ids = {a.get("action_id") for a in ug.get("actions") or [] if isinstance(a, dict)}
    for aid in ("ask_user_move_closer", "ask_user_center_target", "ask_user_hold_still"):
        ok(aid in ug_ids, aid)

    codes = {r.get("reason_code") for r in fail.get("reasons") or [] if isinstance(r, dict)}
    for code in ("projection_drift", "text_region_not_detected", "repeated_empty_after_capture_retry"):
        ok(code in codes, code)

    ok(retry.get("stale_allows_long_term_candidate") is True, "retry_stale_lt")

    cands = expired.get("candidates") or []
    ok(
        any(
            c.get("can_feed_emotional_context_background_candidate") is True
            for c in cands
            if isinstance(c, dict)
        ),
        "emotional_feed",
    )

    pools = {r.get("target_candidate_pool") for r in lt.get("routes") or [] if isinstance(r, dict)}
    ok("emotional_context_background_candidate" in pools, "emotional_route")

    ok(safety.get("visual_symbol_first") is True, "safety_visual_first")
    ok(task.get("midplatform_pre_activation_required") is True, "task_mp_pre")

    ok(current.get("internal_recrop_should_stop") is True, "recrop_stop")
    ok(
        current.get("recommended_capture_decision") == "USER_GUIDANCE_OR_STATIC_CAPTURE",
        "capture_decision",
    )

    ok(ocr_link.get("expired_information_value_principle_respected") is True, "expired_principle")
    ok(stc_link.get("no_runtime_sampling_now") is True, "no_sampling")
    ok(boundary.get("governance_policy_only") is True, "policy_only")
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
        "checks_expected": 70,
        "blockers": blockers,
        "phase": "Vision-Capture-Governance-v1-001",
    }
    _write_json(root / "vision_capture_governance_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
