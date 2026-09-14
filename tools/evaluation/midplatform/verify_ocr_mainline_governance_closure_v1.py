#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Mainline Governance Closure v1."""

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


def _forbidden(data: Dict[str, Any], action: str) -> bool:
    for row in data.get("forbidden_actions") or []:
        if isinstance(row, dict) and row.get("action") == action:
            return row.get("forbidden_now") is True
    return False


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
        "summary": "ocr_mainline_governance_closure_v1_summary.json",
        "intake": "ocr_mainline_governance_closure_input_intake_matrix_v1.json",
        "status_matrix": "ocr_mainline_governance_closure_status_matrix_v1.json",
        "caveat": "ocr_mainline_governance_regression_caveat_acceptance_v1.json",
        "runtime_closed": "ocr_mainline_runtime_ocr_closed_report_v1.json",
        "reopen": "ocr_mainline_future_reopen_condition_matrix_v1.json",
        "forbidden": "ocr_mainline_forbidden_continuation_matrix_v1.json",
        "mem_wm": "ocr_mainline_memory_worldmodel_boundary_status_v1.json",
        "handoff": "ocr_mainline_next_software_mainline_handoff_v1.json",
        "trace": "ocr_mainline_governance_closure_decision_trace_v1.json",
        "final": "ocr_mainline_governance_closure_final_decision_v1.json",
        "boundary": "ocr_mainline_governance_closure_boundary_report_v1.json",
        "metrics": "ocr_mainline_governance_closure_metrics_candidate_report_v1.json",
        "bench": "ocr_mainline_governance_closure_benchmark_link_report_v1.json",
        "health": "ocr_mainline_governance_closure_system_health_report_v1.json",
        "no_write": "ocr_mainline_governance_closure_no_write_boundary_report_v1.json",
        "sim": "ocr_mainline_governance_closure_simulation_context_report_v1.json",
        "non_claims": "ocr_mainline_governance_closure_non_claims_report_v1.json",
        "followups": "ocr_mainline_governance_closure_open_followups_v1.json",
        "audit": "ocr_mainline_governance_closure_audit_report_v1.json",
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
            root / "ocr_mainline_governance_closure_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("closure_scope") == "ocr_mainline_governance_closure_only", "scope")
    ok(s.get("based_on_software_closure") is True, "sw_closure")
    ok(s.get("based_on_regression_route_compliance") is True, "regression")
    ok(s.get("ocr_governance_closed") is True, "ocr_closed")
    ok(s.get("closed_for_governance") is True, "closed_gov")
    ok(s.get("closed_for_production") is False, "not_prod")
    ok(s.get("runtime_ocr_enabled") is False, "no_runtime_ocr")
    ok(s.get("dynamic_ocr_retry_closed") is True, "dyn_closed")
    ok(s.get("staticreading_ocrrequest_blocked_until_captured_frame") is True, "sr_blocked")
    ok(s.get("hardware_chain_frozen") is True, "hw_frozen")
    ok(s.get("memory_handoff_dryrun_ready") is True, "mem_ready")
    ok(s.get("regression_route_compliance_status") == "conditional_pass", "reg_cond")
    ok(s.get("regression_coverage_caveat_present") is True, "caveat_present")
    ok(s.get("testboard_metrics_optional_missing") is True, "testboard_missing")
    ok(s.get("ep_v5_allowed_now") is False, "no_ep5")
    ok(s.get("worldmodel_write_allowed_now") is False, "no_wm")
    ok(s.get("recommended_next_phase") == "WorldModel-Lookup-for-Reading-DryRun-v1", "next_phase")

    cav = data["caveat"]
    ok(cav.get("conditional_go_accepted") is True, "caveat_accepted")
    ok(cav.get("full_regression_claimed") is False, "no_full_reg")

    rt = data["runtime_closed"]
    ok(rt.get("runtime_ocr_enabled") is False, "rt_disabled")

    reopen = data["reopen"]
    for c in reopen.get("conditions") or []:
        if isinstance(c, dict) and c.get("allowed_now") is True:
            blockers.append("reopen_allowed_now")
            break
    else:
        checks += 1

    ok(_forbidden(data["forbidden"], "run_staticreading_ocr_now"), "forbid_sr_ocr")

    mw = data["mem_wm"]
    ok(mw.get("memory_runtime_allowed_now") is False, "mem_rt")
    ok(mw.get("worldmodel_write_allowed_now") is False, "wm_write")

    handoff = data["handoff"]
    ok(handoff.get("recommended_next_phase") == "WorldModel-Lookup-for-Reading-DryRun-v1", "handoff_next")

    final = data["final"]
    ok(final.get("final_decision") == "OCR_MAINLINE_CLOSED_FOR_GOVERNANCE", "final_dec")

    ok(data["boundary"].get("closure_only") is True, "closure_only")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "nw_violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 59,
        "blockers": blockers,
        "final_decision": final.get("final_decision"),
        "phase": "OCR-Mainline-Governance-Closure-v1-001",
    }
    _write_json(root / "ocr_mainline_governance_closure_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
