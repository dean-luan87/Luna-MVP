#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for STC Sampling Guidance Policy v1."""

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
        "summary": "stc_sampling_guidance_policy_v1_summary.json",
        "safety": "stc_safety_trigger_policy_v1.json",
        "task": "stc_task_trigger_prediction_policy_v1.json",
        "geo": "stc_geolocation_route_pre_activation_policy_v1.json",
        "validity": "stc_sampling_validity_window_policy_v1.json",
        "motion": "stc_motion_aware_ocr_downgrade_policy_v1.json",
        "retry": "stc_ocr_retry_budget_timeout_policy_v1.json",
        "static": "stc_static_assisted_reading_trigger_policy_v1.json",
        "dynamic": "stc_dynamic_short_text_scope_policy_v1.json",
        "ocr_act": "stc_ocr_activation_governance_link_report_v1.json",
        "vision": "stc_vision_capture_governance_link_report_v1.json",
        "current": "stc_current_case_decision_dryrun_v1.json",
        "boundary": "stc_sampling_guidance_boundary_report_v1.json",
        "metrics": "stc_sampling_guidance_metrics_candidate_report_v1.json",
        "bench": "stc_sampling_guidance_benchmark_link_report_v1.json",
        "health": "stc_sampling_guidance_system_health_link_report_v1.json",
        "no_write": "stc_sampling_guidance_no_write_boundary_report_v1.json",
        "sim": "stc_sampling_guidance_simulation_context_report_v1.json",
        "non_claims": "stc_sampling_guidance_non_claims_report_v1.json",
        "followups": "stc_sampling_guidance_open_followups_v1.json",
        "audit": "stc_sampling_guidance_audit_report_v1.json",
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
            root / "stc_sampling_guidance_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    safety = data["safety"]
    task = data["task"]
    geo = data["geo"]
    validity = data["validity"]
    motion = data["motion"]
    retry = data["retry"]
    static = data["static"]
    dynamic = data["dynamic"]
    ocr_act = data["ocr_act"]
    vision = data["vision"]
    current = data["current"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("policy_scope") == "stc_sampling_guidance_policy_only", "scope")
    ok(s.get("safety_trigger_policy_defined") is True, "safety_defined")
    ok(s.get("task_trigger_prediction_policy_defined") is True, "task_defined")
    ok(s.get("geolocation_pre_activation_policy_defined") is True, "geo_defined")
    ok(s.get("route_progress_pre_activation_policy_defined") is True, "route_defined")
    ok(s.get("sampling_validity_window_defined") is True, "validity_defined")
    ok(s.get("ocr_retry_budget_policy_defined") is True, "retry_defined")
    ok(s.get("motion_aware_downgrade_policy_defined") is True, "motion_defined")
    ok(s.get("runtime_sampling_invoked") is False, "no_sampling")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    ok(safety.get("default_background_enabled") is True, "safety_bg")
    ok(safety.get("user_prompt_required") is False, "safety_no_prompt")
    markers = safety.get("target_marker_types") or []
    ok("warning_sign" in markers and "danger_text" in markers, "safety_markers")
    path = safety.get("preferred_detection_path") or []
    ok("visual_symbol_first" in path, "visual_first")
    ok(safety.get("full_text_ocr_forbidden_by_default") is True, "no_full_ocr")

    ok(task.get("ocr_self_activation_allowed") is False, "no_self_activation")
    ok(task.get("midplatform_pre_activation_required") is True, "mp_pre_activation")
    scenarios = {x.get("task_type") for x in task.get("scenarios") or [] if isinstance(x, dict)}
    ok("destination_arrival_confirmation" in scenarios, "dest_scenario")
    ok("shop_name_confirmation" in scenarios, "shop_scenario")

    ok(geo.get("no_real_map_api_invoked") is True, "no_map_api")
    ok(len(validity.get("stale_conditions") or []) > 0, "stale_conditions")

    states = {x.get("user_motion_state") for x in motion.get("user_motion_states") or [] if isinstance(x, dict)}
    ok("fast_walk" in states and "vehicle_motion" in states, "motion_states")
    fw = next((x for x in motion.get("user_motion_states") or [] if x.get("user_motion_state") == "fast_walk"), {})
    ok(fw.get("dynamic_reading_allowed") is False, "fast_walk_downgrade")

    ok(retry.get("max_empty_result_before_guidance") is not None, "max_empty_guidance")
    triggers = {t.get("trigger_id") for t in static.get("triggers") or [] if isinstance(t, dict)}
    ok("long_text_detected" in triggers, "long_text_trigger")

    dmarkers = {m.get("marker_type") for m in dynamic.get("markers") or [] if isinstance(m, dict)}
    ok("doorplate" in dmarkers and "room_number" in dmarkers and "safety_short_warning" in dmarkers, "dynamic_markers")

    ok(ocr_act.get("ocr_default_off_for_world_modeling") is True, "ocr_off_wm")
    ok(ocr_act.get("task_trigger_pre_activation_required") is True, "task_pre_activation")
    ok(vision.get("hardware_placeholder_required") is True, "vision_hw_placeholder")

    ok(current.get("internal_retry_should_stop") is True, "retry_stop")
    ok(current.get("user_guidance_recommended") is True, "ug_recommended")
    ok(boundary.get("policy_only") is True, "policy_only")
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
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "STC-Sampling-Guidance-Policy-v1-001",
    }
    _write_json(root / "stc_sampling_guidance_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
