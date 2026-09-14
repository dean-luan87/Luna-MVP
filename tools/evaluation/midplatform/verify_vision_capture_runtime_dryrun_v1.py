#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision Capture Runtime DryRun v1."""

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
        "summary": "vision_capture_runtime_dryrun_v1_summary.json",
        "intake": "vision_capture_runtime_input_intake_matrix_v1.json",
        "readiness": "vision_capture_runtime_readiness_evaluation_matrix_v1.json",
        "trace": "vision_capture_runtime_decision_trace_v1.json",
        "matrix": "vision_capture_runtime_decision_matrix_v1.json",
        "ug": "vision_capture_runtime_user_guidance_candidate_v1.json",
        "sys": "vision_capture_runtime_system_self_adjustment_candidate_v1.json",
        "static": "vision_capture_runtime_static_capture_candidate_v1.json",
        "expired": "vision_capture_runtime_expired_capture_candidate_v1.json",
        "lt": "vision_capture_runtime_long_term_context_routing_v1.json",
        "vis": "vision_capture_runtime_visual_semantic_fallback_v1.json",
        "boundary": "vision_capture_runtime_boundary_report_v1.json",
        "metrics": "vision_capture_runtime_metrics_candidate_report_v1.json",
        "bench": "vision_capture_runtime_benchmark_link_report_v1.json",
        "health": "vision_capture_runtime_system_health_link_report_v1.json",
        "no_write": "vision_capture_runtime_no_write_boundary_report_v1.json",
        "sim": "vision_capture_runtime_simulation_context_report_v1.json",
        "non_claims": "vision_capture_runtime_non_claims_report_v1.json",
        "followups": "vision_capture_runtime_open_followups_v1.json",
        "audit": "vision_capture_runtime_audit_report_v1.json",
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
            root / "vision_capture_runtime_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    readiness = data["readiness"]
    trace = data["trace"]
    matrix = data["matrix"]
    ug = data["ug"]
    sys_adj = data["sys"]
    static = data["static"]
    expired = data["expired"]
    lt = data["lt"]
    vis = data["vis"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "vision_capture_runtime_decision_dryrun_only", "scope")
    ok(s.get("based_on_vision_capture_governance") is True, "based_vc")
    ok(s.get("current_case_loaded") is True, "case_loaded")
    ok(s.get("capture_readiness_evaluated") is True, "readiness_eval")
    ok(s.get("capture_decision_generated") is True, "decision_gen")
    ok(s.get("recommended_capture_decision") == "USER_GUIDANCE_OR_STATIC_CAPTURE", "final_decision")
    ok(s.get("internal_recrop_should_stop") is True, "recrop_stop")
    ok(s.get("dynamic_reocr_allowed_now") is False, "no_dynamic_reocr")
    ok(s.get("runtime_camera_invoked") is False, "no_camera")
    ok(s.get("runtime_frame_captured") is False, "no_frame")
    ok(s.get("runtime_ocr_invoked") is False, "no_ocr")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")

    rows = intake.get("rows") or []
    loaded = [r for r in rows if isinstance(r, dict) and r.get("loaded")]
    ok(len(loaded) >= 7, "key_roots_loaded")

    rrows = readiness.get("rows") or []
    agg = readiness.get("aggregate_same_bbox_risk") or any(
        (r.get("observed_signals") or {}).get("same_bbox_risk") for r in rrows if isinstance(r, dict)
    )
    ok(bool(agg), "same_bbox_risk")
    ok(readiness.get("aggregate_projection_problem_likely") is True, "projection_problem")
    ok(readiness.get("aggregate_capture_quality_problem_likely") is True, "quality_problem")

    steps = {st.get("step_name"): st for st in trace.get("steps") or [] if isinstance(st, dict)}
    ok("generate_final_capture_decision" in steps, "final_step")
    ok(trace.get("final_capture_decision") == "USER_GUIDANCE_OR_STATIC_CAPTURE", "trace_final")

    mrows = {r.get("decision"): r for r in matrix.get("rows") or [] if isinstance(r, dict)}
    ug_row = mrows.get("USER_GUIDANCE_OR_STATIC_CAPTURE", {})
    dyn_row = mrows.get("CONTINUE_DYNAMIC_CAPTURE", {})
    ok(ug_row.get("selected") is True, "ug_selected")
    ok(dyn_row.get("selected") is False, "dyn_not_selected")

    ok(all(c.get("tts_allowed_now") is False for c in ug.get("candidates") or [] if isinstance(c, dict)), "ug_no_tts")
    ok(
        all(c.get("hardware_action_invoked_now") is False for c in sys_adj.get("candidates") or [] if isinstance(c, dict)),
        "sys_no_hw",
    )
    ok(static.get("runtime_capture_invoked") is False, "static_no_capture")

    ec = expired.get("candidates") or []
    ok(any(c.get("cannot_use_for_action") is True for c in ec if isinstance(c, dict)), "expired_no_action")
    ok(
        any(c.get("can_feed_emotional_context_background_candidate") is True for c in ec if isinstance(c, dict)),
        "emotional_feed",
    )

    pools = {r.get("target_candidate_pool") for r in lt.get("routes") or [] if isinstance(r, dict)}
    ok("emotional_context_background_candidate" in pools, "emotional_pool")
    ok(all(r.get("write_allowed_now") is False for r in lt.get("routes") or [] if isinstance(r, dict)), "lt_no_write")

    ok(vis.get("ocr_default_off_for_world_modeling_respected") is True, "ocr_default_off")
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
        "checks_expected": 57,
        "blockers": blockers,
        "phase": "Vision-Capture-Runtime-DryRun-v1-001",
    }
    _write_json(root / "vision_capture_runtime_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
