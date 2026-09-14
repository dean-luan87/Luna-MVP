#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Basic Navigation Guidance Loop DryRun v1."""

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
        "summary": "basic_navigation_guidance_loop_dryrun_v1_summary.json",
        "intake": "basic_navigation_guidance_loop_input_intake_matrix_v1.json",
        "baseline_matrix": "basic_navigation_baseline_safety_loop_dryrun_matrix_v1.json",
        "task_matrix": "basic_navigation_task_driven_loop_dryrun_matrix_v1.json",
        "guidance_decisions": "basic_navigation_guidance_decision_candidate_collection_v1.json",
        "speech_readiness": "basic_navigation_speech_chain_readiness_matrix_v1.json",
        "safety_priority": "basic_navigation_safety_priority_preservation_matrix_v1.json",
        "nav_boundary": "basic_navigation_guidance_action_boundary_check_v1.json",
        "ocr_boundary": "basic_navigation_ocr_use_boundary_check_v1.json",
        "freshness_uncertainty": "basic_navigation_evidence_freshness_uncertainty_check_v1.json",
        "e2e_trace": "basic_navigation_guidance_loop_end_to_end_candidate_trace_v1.json",
        "trace": "basic_navigation_guidance_loop_decision_trace_v1.json",
        "final": "basic_navigation_guidance_loop_final_decision_v1.json",
        "boundary": "basic_navigation_guidance_loop_boundary_report_v1.json",
        "metrics": "basic_navigation_guidance_loop_metrics_candidate_report_v1.json",
        "benchmark_link": "basic_navigation_guidance_loop_benchmark_link_report_v1.json",
        "health_report": "basic_navigation_guidance_loop_system_health_report_v1.json",
        "no_write": "basic_navigation_guidance_loop_no_write_boundary_report_v1.json",
        "sim_report": "basic_navigation_guidance_loop_simulation_context_report_v1.json",
        "non_claims": "basic_navigation_guidance_loop_non_claims_report_v1.json",
        "followups": "basic_navigation_guidance_loop_open_followups_v1.json",
        "audit": "basic_navigation_guidance_loop_audit_report_v1.json",
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
            root / "basic_navigation_guidance_loop_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0, "checks_expected": 64},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("dryrun_scope") == "basic_navigation_guidance_loop_dryrun_only", "scope")
    ok(s.get("based_on_basic_loop_audit") is True, "audit")
    ok(s.get("based_on_task_observation_request") is True, "obs")
    ok(s.get("based_on_vision_ocr_ingest") is True, "ingest")
    ok(s.get("based_on_navigation_guidance_speech_adapter") is True, "adapter")
    ok(s.get("baseline_safety_loop_dryrun_generated") is True, "baseline_gen")
    ok(s.get("task_driven_guidance_loop_dryrun_generated") is True, "task_gen")
    ok(s.get("baseline_safety_request_count_observed") == 4, "baseline_4")
    ok(s.get("task_driven_request_count_observed") == 12, "task_12")
    ok(s.get("vision_evidence_candidate_count_observed") == 16, "vision_16")
    ok(s.get("ocr_evidence_candidate_count_observed") == 7, "ocr_7")
    ok(s.get("action_support_candidate_count_observed") == 16, "action_16")
    ok(s.get("speech_candidate_count_observed") == 28, "speech_28")
    ok(s.get("guidance_decision_candidates_generated") is True, "decisions")
    ok(s.get("speech_chain_readiness_generated") is True, "speech_chain")
    ok(s.get("navigation_guidance_action_boundary_preserved") is True, "nav_boundary")
    ok(s.get("safety_priority_preserved") is True, "safety_pri")
    ok(s.get("uncertainty_language_preserved") is True, "uncertainty")
    ok(s.get("camera_invoked") is False, "no_camera")
    ok(s.get("ocr_provider_invoked") is False, "no_ocr")
    ok(s.get("tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("navigation_action_triggered") is False, "no_nav")

    bm = data["baseline_matrix"]
    brows = bm.get("rows") or []
    ok(len(brows) >= 4, "baseline_rows")
    ok(all(r.get("allowed_without_task") is True for r in brows), "baseline_no_task")

    tm = data["task_matrix"]
    trows = tm.get("rows") or []
    ok(len(trows) >= 12, "task_rows")
    ok(all(r.get("requires_task_context") is True for r in trows), "task_context")

    gd = data["guidance_decisions"]
    ok((gd.get("guidance_decision_candidate_count") or 0) > 0, "guidance_count")

    sr = data["speech_readiness"]
    srows = sr.get("rows") or []
    ok(len(srows) > 0, "speech_readiness_rows")
    ok(all(r.get("speech_gate_required") is True for r in srows), "gate_required")

    sp = data["safety_priority"]
    ok(sp.get("safety_priority_above_task") is True, "safety_above")

    nb = data["nav_boundary"]
    ok(nb.get("guidance_candidate_is_not_navigation_action") is True, "not_action")

    ob = data["ocr_boundary"]
    ok(ob.get("ocr_provider_invoked") is False, "ocr_no_invoke")
    ok(ob.get("empty_ocr_is_not_no_text_fact") is True, "empty_ocr")

    fu = data["freshness_uncertainty"]
    ok(fu.get("stale_evidence_blocks_current_navigation_prompt") is True, "stale_block")

    e2e = data["e2e_trace"]
    ok(e2e.get("trace_count", 0) >= 16, "trace_16")

    fin = data["final"]
    ok(
        fin.get("final_decision") == "BASIC_NAVIGATION_GUIDANCE_LOOP_DRYRUN_READY_FOR_STABILIZATION_TEST",
        "final_decision",
    )

    bnd = data["boundary"]
    ok(bnd.get("dryrun_only") is True, "dryrun_only")

    met = data["metrics"]
    ok(met.get("no_write_boundary_pass_rate") == 1.0, "pass_rate")

    hr = data["health_report"]
    ok(hr.get("no_runtime_health_claim") is True, "no_health_claim")

    nw = data["no_write"]
    ok(nw.get("boundary_ok") is True, "boundary_ok")
    ok(nw.get("violations") == [], "no_violations")

    sim = data["sim_report"]
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")

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
        "phase": "Basic-Navigation-Guidance-Loop-DryRun-v1-001",
    }
    _write_json(root / "basic_navigation_guidance_loop_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
