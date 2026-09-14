#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Hardware Camera Control Contract v1."""

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
        "summary": "hardware_camera_control_contract_v1_summary.json",
        "intake": "hardware_camera_control_input_intake_matrix_v1.json",
        "request_schema": "hardware_camera_control_request_schema_v1.json",
        "capability_schema": "hardware_capability_report_schema_v1.json",
        "action_matrix": "hardware_camera_control_action_matrix_v1.json",
        "capture_collection": "hardware_static_capture_request_candidate_collection_v1.json",
        "unknown_policy": "hardware_capability_unknown_unsupported_policy_v1.json",
        "fallback_policy": "hardware_camera_failure_fallback_policy_v1.json",
        "health_link_policy": "hardware_camera_system_health_link_policy_v1.json",
        "ocr_gate_link": "hardware_static_capture_to_ocrrequest_future_gate_link_v1.json",
        "guardedtrial": "hardware_camera_guardedtrial_handoff_policy_v1.json",
        "long_term": "hardware_camera_control_long_term_candidate_link_v1.json",
        "trace": "hardware_camera_control_contract_decision_trace_v1.json",
        "final": "hardware_camera_control_contract_final_decision_v1.json",
        "boundary": "hardware_camera_control_boundary_report_v1.json",
        "metrics": "hardware_camera_control_metrics_candidate_report_v1.json",
        "bench": "hardware_camera_control_benchmark_link_report_v1.json",
        "health": "hardware_camera_control_system_health_link_report_v1.json",
        "no_write": "hardware_camera_control_no_write_boundary_report_v1.json",
        "sim": "hardware_camera_control_simulation_context_report_v1.json",
        "non_claims": "hardware_camera_control_non_claims_report_v1.json",
        "followups": "hardware_camera_control_open_followups_v1.json",
        "audit": "hardware_camera_control_audit_report_v1.json",
    }
    data: Dict[str, Any] = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = json.loads(p.read_text(encoding="utf-8"))

    if blockers:
        _write_json(root / "hardware_camera_control_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    rs = data["request_schema"]
    am = data["action_matrix"]
    cap = data["capability_schema"]
    coll = data["capture_collection"]

    ok(True, "summary")
    ok(s.get("contract_scope") == "hardware_camera_control_contract_only", "scope")
    ok(s.get("based_on_rrd_runtime") is True, "based_rrd")
    ok(s.get("static_capture_handoff_candidate_count_observed") == 26, "handoff_26")
    ok(s.get("camera_control_request_schema_defined") is True, "req_schema")
    ok(s.get("hardware_capability_report_schema_defined") is True, "cap_schema")
    ok(s.get("camera_control_action_matrix_defined") is True, "action_matrix")
    ok(s.get("static_capture_request_candidate_schema_defined") is True, "capture_schema")
    ok(s.get("hardware_failure_fallback_policy_defined") is True, "fallback_def")
    ok(s.get("system_health_link_defined") is True, "health_def")
    ok(s.get("guarded_trial_handoff_defined") is True, "guarded_def")
    ok(s.get("hardware_capability_unknown_allowed") is True, "unknown_ok")
    ok(s.get("runtime_camera_invoked") is False, "no_cam")
    ok(s.get("hardware_action_invoked") is False, "no_hw")
    ok(s.get("ocr_invoked") is False, "no_ocr")

    types = rs.get("request_types") or []
    ok("STATIC_CAPTURE_REQUEST" in types, "static_cap_type")
    ok("ZOOM_REQUEST" in types, "zoom_type")
    ok("AUTOFOCUS_REQUEST" in types, "af_type")
    ok(cap.get("capability_unknown_allowed") is True, "cap_unknown")

    actions = am.get("actions") or []
    names = {a.get("action_name") for a in actions if isinstance(a, dict)}
    ok("request_zoom" in names, "action_zoom")
    ok("request_autofocus" in names, "action_af")
    ok("request_static_capture" in names, "action_capture")
    ok(all(a.get("action_invoked_now") is False for a in actions if isinstance(a, dict)), "action_not_now")

    ok(coll.get("static_capture_request_candidate_count") == 26, "capture_26")
    ok(all(c.get("hardware_action_invoked_now") is False for c in coll.get("candidates") or [] if isinstance(c, dict)), "cap_not_now")

    unknown = data["unknown_policy"].get("conditions") or []
    ok(any(u.get("condition") == "hardware_profile_missing" for u in unknown if isinstance(u, dict)), "profile_missing")

    fb = data["fallback_policy"].get("fallbacks") or []
    ok(any(f.get("fallback_type") == "return_to_user_guidance" for f in fb if isinstance(f, dict)), "fb_guidance")

    hlp = data["health_link_policy"]
    ok("CAMERA_UNAVAILABLE" in (hlp.get("failure_classes") or []), "cam_unavail")
    ok("AUTOFOCUS_FAILED" in (hlp.get("failure_classes") or []), "af_failed")

    ok(data["ocr_gate_link"].get("ocrrequest_eligible_now") is False, "ocr_not_now")
    ok(data["guardedtrial"].get("guardedtrial_invoked_now") is False, "gt_not_now")
    ok(data["long_term"].get("can_feed_long_term_candidate") is True, "lt")
    ok(data["final"].get("final_decision") == "READY_FOR_HARDWARE_CAMERA_RUNTIME_DRYRUN_LATER", "final")
    ok(data["boundary"].get("contract_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "metrics")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("recovery_action_committed") is False, "health_rec")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_fact")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("scene_delta_candidate_generated") is False, "audit_delta")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "Hardware-Camera-Control-Contract-v1-001",
    }
    _write_json(root / "hardware_camera_control_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
