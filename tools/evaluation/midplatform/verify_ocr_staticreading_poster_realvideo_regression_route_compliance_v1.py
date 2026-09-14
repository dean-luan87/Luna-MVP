#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR StaticReading Poster RealVideo Regression Route Compliance v1."""

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


def _route(data: Dict[str, Any], rid: str) -> Dict[str, Any]:
    for r in data.get("routes") or []:
        if isinstance(r, dict) and r.get("route_id") == rid:
            return r
    return {}


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
        "summary": "ocr_staticreading_poster_realvideo_regression_route_compliance_v1_summary.json",
        "intake": "ocr_regression_route_compliance_input_intake_matrix_v1.json",
        "route_matrix": "ocr_regression_route_compliance_matrix_v1.json",
        "realvideo_check": "ocr_regression_realvideo_route_check_v1.json",
        "poster_check": "ocr_regression_poster_route_check_v1.json",
        "staticreading_check": "ocr_regression_staticreading_route_check_v1.json",
        "memory_check": "ocr_regression_memory_handoff_route_check_v1.json",
        "hardware_check": "ocr_regression_hardware_stub_route_check_v1.json",
        "boundary_matrix": "ocr_regression_boundary_matrix_v1.json",
        "blocker_validation": "ocr_regression_expected_blocker_validation_v1.json",
        "bypass_audit": "ocr_regression_provider_bypass_audit_v1.json",
        "wm_sd_check": "ocr_regression_worldmodel_scenedelta_no_write_v1.json",
        "coverage": "ocr_regression_coverage_report_v1.json",
        "trace": "ocr_regression_route_compliance_decision_trace_v1.json",
        "final": "ocr_regression_route_compliance_final_decision_v1.json",
        "boundary": "ocr_regression_route_compliance_boundary_report_v1.json",
        "metrics": "ocr_regression_route_compliance_metrics_candidate_report_v1.json",
        "bench": "ocr_regression_route_compliance_benchmark_link_report_v1.json",
        "health": "ocr_regression_route_compliance_system_health_report_v1.json",
        "no_write": "ocr_regression_route_compliance_no_write_boundary_report_v1.json",
        "sim": "ocr_regression_route_compliance_simulation_context_report_v1.json",
        "non_claims": "ocr_regression_route_compliance_non_claims_report_v1.json",
        "followups": "ocr_regression_route_compliance_open_followups_v1.json",
        "audit": "ocr_regression_route_compliance_audit_report_v1.json",
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
            root / "ocr_regression_route_compliance_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    final = data["final"]["final_decision"]
    ok(True, "summary")
    ok(s.get("regression_scope") == "route_compliance_regression_only", "scope")
    ok(s.get("based_on_software_mainline_closure") is True, "closure")
    ok(s.get("based_on_staticreading_ocrrequest_gate") is True, "ocr_gate")
    ok(s.get("based_on_memory_handoff") is True, "mem")
    ok(s.get("based_on_hardware_stub") is True, "hw")
    ok(s.get("route_compliance_matrix_generated") is True, "matrix")
    ok(s.get("regression_runtime_executed") is False, "no_rt")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("ocrrequest_submitted") is False, "no_submit")
    ok(s.get("ep_v5_generated") is False, "no_ep5")
    ok(len(data["route_matrix"].get("routes") or []) >= 5, "five_routes")
    ok(_route(data["route_matrix"], "realvideo"), "rv_route")
    ok(_route(data["route_matrix"], "poster"), "poster_route")
    ok(_route(data["route_matrix"], "staticreading"), "sr_route")
    sr = data["staticreading_check"]
    ok(sr.get("blocked_ocrrequest_candidate_count") == 34, "blocked_34")
    ok(sr.get("capture_status_observed") == "not_captured", "not_captured")
    ok(sr.get("ocrrequest_submitted_now") is False, "sr_no_submit")
    mem = data["memory_check"]
    ok(mem.get("append_only_preserved") is True, "append_only")
    hw = data["hardware_check"]
    ok(hw.get("real_hardware_call_count") == 0, "hw_calls_0")
    ok(data["boundary_matrix"].get("violations") == [], "boundary_violations")
    bl_ids = [b.get("blocker_id") for b in data["blocker_validation"].get("blockers") or [] if isinstance(b, dict)]
    ok("no_real_camera" in bl_ids, "bl_camera")
    ok("capture_status_not_captured" in bl_ids, "bl_cap")
    ok("ep_v5_missing_ocr_result" in bl_ids, "bl_ep5")
    ok(all(not b.get("bypass_detected") for b in data["blocker_validation"].get("blockers") or [] if isinstance(b, dict)), "no_bypass")
    ok(data["bypass_audit"].get("direct_provider_bypass") is False, "no_bypass")
    ok(data["wm_sd_check"].get("world_model_written_now") is False, "no_wm")
    ok(data["wm_sd_check"].get("scene_delta_candidate_generated_now") is False, "no_sd")
    ok(final in (
        "REGRESSION_ROUTE_COMPLIANCE_PASS",
        "REGRESSION_ROUTE_COMPLIANCE_CONDITIONAL_PASS",
    ), "final_ok")
    ok(data["boundary"].get("regression_only") is True, "regression_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    if final == "REGRESSION_ROUTE_COMPLIANCE_FAIL":
        verdict = "NO_GO"
        if "final_fail" not in blockers:
            blockers.append("final_fail")

    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 66,
        "blockers": blockers,
        "final_decision": final,
        "phase": "OCR-StaticReading-Poster-RealVideo-Regression-RouteCompliance-v1-001",
    }
    _write_json(root / "ocr_regression_route_compliance_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
