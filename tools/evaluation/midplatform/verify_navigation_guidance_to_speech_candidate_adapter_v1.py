#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Navigation Guidance to Speech Candidate Adapter v1."""

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
        "summary": "navigation_guidance_to_speech_candidate_adapter_v1_summary.json",
        "intake": "navigation_guidance_speech_adapter_input_intake_matrix_v1.json",
        "guidance_source": "navigation_guidance_source_intake_matrix_v1.json",
        "mapping_policy": "navigation_guidance_to_speech_mapping_policy_v1.json",
        "priority_policy": "navigation_guidance_speech_priority_policy_v1.json",
        "suppression_policy": "navigation_guidance_safety_suppression_policy_v1.json",
        "uncertainty_policy": "navigation_guidance_uncertainty_language_policy_v1.json",
        "speech_schema": "navigation_guidance_speech_request_candidate_schema_v1.json",
        "speech_collection": "navigation_guidance_speech_candidate_collection_v1.json",
        "vop_handoff": "navigation_guidance_vop_handoff_candidate_v1.json",
        "gate_admission": "navigation_guidance_speech_gate_admission_dryrun_candidate_v1.json",
        "nav_boundary": "navigation_guidance_speech_adapter_navigation_action_boundary_v1.json",
        "freshness_check": "navigation_guidance_evidence_freshness_speech_check_v1.json",
        "trace": "navigation_guidance_to_speech_adapter_decision_trace_v1.json",
        "final": "navigation_guidance_to_speech_adapter_final_decision_v1.json",
        "boundary": "navigation_guidance_to_speech_adapter_boundary_report_v1.json",
        "metrics": "navigation_guidance_to_speech_adapter_metrics_candidate_report_v1.json",
        "benchmark_link": "navigation_guidance_to_speech_adapter_benchmark_link_report_v1.json",
        "health_report": "navigation_guidance_to_speech_adapter_system_health_report_v1.json",
        "no_write": "navigation_guidance_to_speech_adapter_no_write_boundary_report_v1.json",
        "sim_report": "navigation_guidance_to_speech_adapter_simulation_context_report_v1.json",
        "non_claims": "navigation_guidance_to_speech_adapter_non_claims_report_v1.json",
        "followups": "navigation_guidance_to_speech_adapter_open_followups_v1.json",
        "audit": "navigation_guidance_to_speech_adapter_audit_report_v1.json",
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
            root / "navigation_guidance_to_speech_adapter_verifier_report_v1.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0, "checks_expected": 62},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    ok(s.get("adapter_scope") == "navigation_guidance_to_speech_candidate_adapter_only", "scope")
    ok(s.get("based_on_vision_ocr_ingest") is True, "vision_ocr")
    ok(s.get("action_support_candidate_count_observed") == 16, "action_16")
    ok(s.get("guidance_to_speech_mapping_defined") is True, "mapping")
    ok(s.get("speech_priority_policy_defined") is True, "priority")
    ok(s.get("safety_suppression_policy_defined") is True, "suppression")
    ok(s.get("uncertainty_language_policy_defined") is True, "uncertainty")
    ok(s.get("speech_request_candidate_schema_defined") is True, "schema")
    ok(s.get("vop_handoff_candidate_defined") is True, "vop_handoff")
    ok(s.get("speech_response_candidates_generated") is True, "speech_gen")
    ok(s.get("speech_gate_required") is True, "gate_req")
    ok(s.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")
    ok(s.get("direct_vop_bypass_forbidden") is True, "no_vop_bypass")
    ok(s.get("tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("navigation_action_triggered") is False, "no_nav")

    gs = data["guidance_source"]
    accepted = [r for r in gs.get("rows", []) if r.get("accepted_for_speech_adapter")]
    ok(len(accepted) >= 16, "guidance_accepted")

    mp = data["mapping_policy"]
    maps = {m.get("source_type"): m.get("target_speech_candidate") for m in mp.get("mappings", [])}
    ok(maps.get("safety_guidance_support") == "safety_warning_speech_candidate", "map_safety")
    ok(maps.get("navigation_guidance_support") == "navigation_hint_speech_candidate", "map_nav")

    pp = data["priority_policy"]
    ok("P0_safety_immediate" in (pp.get("priority_levels") or []), "P0")
    ok(pp.get("safety_priority_above_task") is True, "safety_above_task")

    sp = data["suppression_policy"]
    ok(sp.get("safety_alert_active_blocks_low_priority_speech") is True, "suppress_low")

    up = data["uncertainty_policy"]
    ok(up.get("evidence_candidate_not_fact_must_not_be_stated_as_fact") is True, "not_fact_lang")
    ok("已经确认" in (up.get("forbidden_wording") or []), "forbidden_wording")

    sch = data["speech_schema"]
    ok(sch.get("speech_gate_required") is True, "schema_gate")

    sc = data["speech_collection"]
    cands = sc.get("candidates") or []
    ok(sc.get("speech_candidate_count", 0) >= 16, "speech_16")
    ok(all(c.get("submitted_now") is False for c in cands), "not_submitted")
    ok(all(c.get("tts_invoked_now") is False for c in cands), "cand_no_tts")
    ok(all(c.get("vop_invoked_now") is False for c in cands), "cand_no_vop")

    vh = data["vop_handoff"]
    ok(vh.get("vop_handoff_defined") is True, "handoff_def")
    ok(vh.get("handoff_invoked_now") is False, "handoff_not_now")

    ga = data["gate_admission"]
    ok(ga.get("speech_gate_admission_candidate_defined") is True, "admission_def")
    ok(ga.get("admission_invoked_now") is False, "admission_not_now")

    nb = data["nav_boundary"]
    ok(
        nb.get("guidance_is_not_action") is True
        or nb.get("speech_candidate_is_not_navigation_action") is True,
        "not_nav_action",
    )

    fc = data["freshness_check"]
    ok(fc.get("stale_evidence_blocks_current_action_prompt") is True, "stale_block")

    fin = data["final"]
    ok(
        fin.get("final_decision") == "NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_READY_FOR_BASIC_NAVIGATION_LOOP",
        "final_decision",
    )

    bnd = data["boundary"]
    ok(bnd.get("adapter_only") is True, "adapter_only")

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
        "checks_expected": 62,
        "blockers": blockers,
        "final_decision": fin.get("final_decision"),
        "phase": "Navigation-Guidance-to-Speech-Candidate-Adapter-v1-001",
    }
    _write_json(root / "navigation_guidance_to_speech_adapter_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
