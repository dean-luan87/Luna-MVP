#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Safety Task Arbitration Policy v1."""

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
        "summary": "safety_task_arbitration_policy_v1_summary.json",
        "intake": "safety_task_arbitration_input_intake_matrix_v1.json",
        "source_matrix": "safety_task_arbitration_source_matrix_v1.json",
        "schema": "safety_task_arbitration_schema_v1.json",
        "priority_policy": "safety_task_priority_policy_v1.json",
        "suppression_policy": "safety_task_suppression_policy_v1.json",
        "delay_policy": "safety_task_delay_policy_v1.json",
        "interrupt_policy": "safety_task_interrupt_policy_v1.json",
        "speech_handoff": "safety_task_speech_arbitration_handoff_policy_v1.json",
        "commit_policy": "safety_task_commit_arbitration_policy_v1.json",
        "ocr_policy": "safety_task_ocr_guidance_arbitration_policy_v1.json",
        "human_policy": "safety_task_human_assistance_arbitration_policy_v1.json",
        "arb_collection": "safety_task_arbitration_candidate_collection_v1.json",
        "scenario_matrix": "safety_task_safety_active_scenario_matrix_v1.json",
        "feedback": "safety_task_arbitration_feedback_contract_v1.json",
        "trace": "safety_task_arbitration_decision_trace_v1.json",
        "final": "safety_task_arbitration_final_decision_v1.json",
        "boundary": "safety_task_arbitration_boundary_report_v1.json",
        "metrics": "safety_task_arbitration_metrics_candidate_report_v1.json",
        "benchmark_link": "safety_task_arbitration_benchmark_link_report_v1.json",
        "health_report": "safety_task_arbitration_system_health_report_v1.json",
        "no_write": "safety_task_arbitration_no_write_boundary_report_v1.json",
        "sim_report": "safety_task_arbitration_simulation_context_report_v1.json",
        "non_claims": "safety_task_arbitration_non_claims_report_v1.json",
        "followups": "safety_task_arbitration_open_followups_v1.json",
        "audit": "safety_task_arbitration_audit_report_v1.json",
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
            root / "safety_task_arbitration_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0, "checks_expected": 64},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("policy_scope") == "safety_task_arbitration_policy_only", "scope")
    ok(s.get("based_on_basic_navigation_loop") is True, "nav_loop")
    ok(s.get("baseline_safety_loop_supported") is True, "baseline")
    ok(s.get("task_driven_loop_supported") is True, "task_driven")
    ok(s.get("arbitration_schema_defined") is True, "schema_def")
    ok(s.get("priority_policy_defined") is True, "priority")
    ok(s.get("suppression_policy_defined") is True, "suppression")
    ok(s.get("delay_policy_defined") is True, "delay")
    ok(s.get("interrupt_policy_defined") is True, "interrupt")
    ok(s.get("speech_arbitration_handoff_defined") is True, "speech_handoff")
    ok(s.get("task_commit_arbitration_policy_defined") is True, "commit")
    ok(s.get("ocr_guidance_arbitration_policy_defined") is True, "ocr")
    ok(s.get("human_assistance_arbitration_policy_defined") is True, "human")
    ok(s.get("runtime_arbitration_invoked") is False, "no_runtime")
    ok(s.get("tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")

    sm = data["source_matrix"]
    accepted = [r for r in sm.get("rows", []) if r.get("accepted_for_arbitration_policy")]
    ok(len(accepted) >= 16, "sources_accepted")

    sch = data["schema"]
    types = sch.get("arbitration_decision_types") or []
    ok("SUPPRESS_BY_SAFETY" in types, "suppress_type")
    ok("DELAY_UNTIL_SAFETY_CLEAR" in types, "delay_type")

    pp = data["priority_policy"]
    ok(pp.get("P0_interrupts_all_lower") is True, "P0_interrupt")

    sp = data["suppression_policy"]
    ok(sp.get("safety_active_suppresses_repeat_guidance") is True, "suppress_repeat")

    dp = data["delay_policy"]
    ok(dp.get("safety_active_delays_task_commit") is True, "delay_commit")

    ip = data["interrupt_policy"]
    ok(ip.get("safety_interrupt_preserves_pending_confirmation") is True, "preserve_confirm")

    sh = data["speech_handoff"]
    ok(sh.get("speech_gate_required") is True, "gate_req")

    cp = data["commit_policy"]
    ok(cp.get("task_state_committed_now") is False, "no_commit")

    op = data["ocr_policy"]
    ok(op.get("ocr_provider_invoked_now") is False, "no_ocr")

    hp = data["human_policy"]
    ok(hp.get("human_assistance_requires_confirmation") is True, "human_confirm")

    ac = data["arb_collection"]
    ok(ac.get("arbitration_candidate_count", 0) >= 16, "arb_16")

    scen = data["scenario_matrix"]
    rows = scen.get("rows") or []
    ok(len(rows) == 2, "scenario_2")
    active_row = next((r for r in rows if r.get("safety_active") is True), None)
    ok(active_row and active_row.get("low_priority_suppressed_or_delayed_count", 0) > 0, "active_suppress")

    fb = data["feedback"]
    ok(fb.get("feedback_invoked_now") is False, "feedback_not_now")

    fin = data["final"]
    ok(
        fin.get("final_decision") == "SAFETY_TASK_ARBITRATION_POLICY_READY_FOR_LOOP_STABILIZATION_TEST",
        "final_decision",
    )

    bnd = data["boundary"]
    ok(bnd.get("policy_only") is True, "policy_only")

    met = data["metrics"]
    ok(met.get("no_write_boundary_pass_rate") == 1.0, "pass_rate")

    hr = data["health_report"]
    ok(hr.get("no_runtime_health_claim") is True, "no_health")

    nw = data["no_write"]
    ok(nw.get("boundary_ok") is True, "boundary_ok")
    ok(nw.get("violations") == [], "violations")

    sim = data["sim_report"]
    ok(sim.get("simulation_profile_id") == "developer_full", "sim")

    aud = data["audit"]
    ok(aud.get("midplatform_fact_written") is False, "no_fact")
    ok(aud.get("runtime_routing_changed") is False, "no_routing")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 64,
        "blockers": blockers,
        "final_decision": fin.get("final_decision"),
        "phase": "Safety-Task-Arbitration-Policy-v1-001",
    }
    _write_json(root / "safety_task_arbitration_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
