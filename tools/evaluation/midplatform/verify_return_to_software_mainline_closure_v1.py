#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Return To Software Mainline Closure v1."""

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


def _blocker_ids(reg: Dict[str, Any]) -> List[str]:
    return [b.get("blocker_id") for b in reg.get("blockers") or [] if isinstance(b, dict)]


def _entrypoint(reg: Dict[str, Any], name: str) -> Dict[str, Any]:
    for e in reg.get("entrypoints") or []:
        if isinstance(e, dict) and e.get("entrypoint_name") == name:
            return e
    return {}


def _forbidden(reg: Dict[str, Any], action: str) -> Dict[str, Any]:
    for a in reg.get("actions") or []:
        if isinstance(a, dict) and a.get("action") == action:
            return a
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
        "summary": "return_to_software_mainline_closure_v1_summary.json",
        "intake": "return_to_software_mainline_input_intake_matrix_v1.json",
        "completed_phases": "return_to_software_mainline_completed_phase_matrix_v1.json",
        "closed_chains": "return_to_software_mainline_closed_chain_summary_v1.json",
        "blockers": "return_to_software_mainline_blocker_register_v1.json",
        "allowed_entrypoints": "return_to_software_mainline_allowed_next_entrypoint_matrix_v1.json",
        "forbidden_actions": "return_to_software_mainline_forbidden_next_action_matrix_v1.json",
        "roadmap": "return_to_software_mainline_candidate_roadmap_v1.json",
        "staticreading_ocr_closure": "return_to_software_mainline_staticreading_ocr_closure_report_v1.json",
        "hardware_closure": "return_to_software_mainline_hardware_chain_closure_report_v1.json",
        "memory_closure": "return_to_software_mainline_memory_handoff_closure_report_v1.json",
        "wm_fragment_link": "return_to_software_mainline_worldmodel_fragment_future_link_v1.json",
        "trace": "return_to_software_mainline_closure_decision_trace_v1.json",
        "final": "return_to_software_mainline_closure_final_decision_v1.json",
        "boundary": "return_to_software_mainline_closure_boundary_report_v1.json",
        "metrics": "return_to_software_mainline_closure_metrics_candidate_report_v1.json",
        "bench": "return_to_software_mainline_closure_benchmark_link_report_v1.json",
        "health": "return_to_software_mainline_closure_system_health_report_v1.json",
        "no_write": "return_to_software_mainline_closure_no_write_boundary_report_v1.json",
        "sim": "return_to_software_mainline_closure_simulation_context_report_v1.json",
        "non_claims": "return_to_software_mainline_closure_non_claims_report_v1.json",
        "followups": "return_to_software_mainline_closure_open_followups_v1.json",
        "audit": "return_to_software_mainline_closure_audit_report_v1.json",
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
            root / "return_to_software_mainline_closure_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    chains = data["closed_chains"]
    bl = _blocker_ids(data["blockers"])
    ok(True, "summary")
    ok(s.get("closure_scope") == "software_mainline_closure_only", "scope")
    ok(s.get("based_on_staticreading_ocrrequest_gate") is True, "ocr_gate")
    ok(s.get("based_on_memory_handoff") is True, "mem_ho")
    ok(s.get("based_on_hardware_adapter_stub") is True, "hw_stub")
    ok(s.get("hardware_chain_frozen") is True, "hw_frozen")
    ok(s.get("staticreading_ocrrequest_gate_closed") is True, "ocr_closed")
    ok(s.get("memory_handoff_dryrun_closed") is True, "mem_closed")
    ok(s.get("static_capture_result_available") is False, "no_cap")
    ok(s.get("capture_status_observed") == "not_captured", "not_captured")
    ok(s.get("ocrrequest_eligible_now") is False, "ocr_not_eligible")
    ok(s.get("ep_v5_allowed_now") is False, "no_ep5")
    ok(s.get("semantic_v5_allowed_now") is False, "no_sem")
    ok(s.get("source_validation_v3_allowed_now") is False, "no_sv")
    ok(s.get("software_mainline_ready_for_next_planning") is True, "ready_plan")
    ok(data["completed_phases"].get("completed_phase_count", 0) >= 10, "ten_phases")
    ok(chains.get("hardware_chain", {}).get("status") == "frozen", "hw_status")
    ok(chains.get("staticreading_chain", {}).get("status") == "blocked_until_captured_frame", "sr_status")
    ok(chains.get("memory_handoff_chain", {}).get("status") == "handoff_dryrun_ready", "mem_status")
    ok("no_real_camera" in bl, "bl_camera")
    ok("capture_status_not_captured" in bl, "bl_cap")
    ok("ep_v5_missing_ocr_result" in bl, "bl_ep5")
    ok(_entrypoint(data["allowed_entrypoints"], "WorldModel-Lookup-for-Reading-DryRun-v1").get("allowed_now") is True, "wm_now")
    ok(_entrypoint(data["allowed_entrypoints"], "Hardware-Camera-Control-GuardedTrial-Precheck-v1").get("allowed_now") is False, "gt_later")
    ok(_forbidden(data["forbidden_actions"], "run_staticreading_ocr_now").get("forbidden_now") is True, "forbid_ocr")
    ok(_forbidden(data["forbidden_actions"], "submit_ocrrequest_without_captured_frame").get("forbidden_now") is True, "forbid_submit")
    ok(any(
        c.get("candidate_phase") == "WorldModel-Lookup-for-Reading-DryRun-v1"
        for c in data["roadmap"].get("candidates") or []
        if isinstance(c, dict)
    ), "roadmap_wm")
    ocr_cl = data["staticreading_ocr_closure"]
    ok(ocr_cl.get("blocked_ocrrequest_candidate_count") == 34, "blocked_34")
    ok(data["hardware_closure"].get("hardware_chain_frozen") is True, "hw_cl")
    ok(data["memory_closure"].get("append_request_candidate_count") == 11, "append_11")
    ok(data["wm_fragment_link"].get("worldmodel_write_allowed_now") is False, "no_wm_write")
    ok(data["final"].get("final_decision") == "SOFTWARE_MAINLINE_READY_FOR_NEXT_PLANNING", "final")
    ok(data["boundary"].get("closure_only") is True, "boundary")
    ok(data["metrics"].get("no_write_boundary_pass_rate") == 1.0, "nw_rate")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("no_runtime_health_claim") is True, "health")
    ok(data["no_write"].get("boundary_ok") is True, "nw_ok")
    ok(data["no_write"].get("violations") == [], "violations")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(data["audit"].get("midplatform_fact_written") is False, "audit_mp")
    ok(data["audit"].get("world_model_written") is False, "audit_wm")
    ok(data["audit"].get("runtime_routing_changed") is False, "audit_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "Return-To-Software-Mainline-Closure-v1-001",
    }
    _write_json(root / "return_to_software_mainline_closure_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
