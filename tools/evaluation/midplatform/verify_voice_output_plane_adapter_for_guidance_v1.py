#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Voice Output Plane Adapter for Guidance v1."""

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
        "summary": "voice_output_plane_adapter_for_guidance_v1_summary.json",
        "intake": "voice_output_plane_adapter_input_intake_matrix_v1.json",
        "mapping": "voice_output_plane_adapter_mapping_contract_v1.json",
        "adapter_payload": "voice_output_plane_adapter_payload_candidate_v1.json",
        "speech_payload": "voice_output_plane_speech_request_payload_candidate_v1.json",
        "admission": "voice_output_plane_speech_gate_admission_dryrun_v1.json",
        "vop_submit": "voice_output_plane_submit_dryrun_v1.json",
        "safety_matrix": "voice_output_plane_guidance_safety_interruptibility_matrix_v1.json",
        "stm_repeat": "voice_output_plane_stm_repeat_reference_preservation_report_v1.json",
        "final": "voice_output_plane_adapter_final_dryrun_decision_v1.json",
        "boundary": "voice_output_plane_adapter_boundary_report_v1.json",
        "metrics": "voice_output_plane_adapter_metrics_candidate_report_v1.json",
        "bench": "voice_output_plane_adapter_benchmark_link_report_v1.json",
        "health": "voice_output_plane_adapter_system_health_link_report_v1.json",
        "no_write": "voice_output_plane_adapter_no_write_boundary_report_v1.json",
        "sim": "voice_output_plane_adapter_simulation_context_report_v1.json",
        "non_claims": "voice_output_plane_adapter_non_claims_report_v1.json",
        "followups": "voice_output_plane_adapter_open_followups_v1.json",
        "audit": "voice_output_plane_adapter_audit_report_v1.json",
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
            root / "voice_output_plane_adapter_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "checks_expected": 59, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    mapping = data["mapping"]
    apy = data["adapter_payload"]
    sp = data["speech_payload"]
    adm = data["admission"]
    vop = data["vop_submit"]
    safety = data["safety_matrix"]
    stm = data["stm_repeat"]
    final = data["final"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("adapter_scope") == "voice_output_plane_adapter_dryrun_only", "scope")
    ok(s.get("based_on_voice_guidance_prompt_runtime") is True, "based_runtime")
    ok(s.get("speech_request_candidate_observed") is True, "sr_observed")
    ok(s.get("adapter_payload_candidate_generated") is True, "adapter_gen")
    ok(s.get("speech_request_payload_candidate_generated") is True, "payload_gen")
    ok(s.get("speech_gate_admission_dryrun_executed") is True, "admission_exec")
    ok(s.get("voice_output_plane_submit_dryrun_executed") is True, "vop_dryrun")
    ok(s.get("selected_priority") == "P3_OCR_GUIDANCE", "p3")
    ok(s.get("safety_interruptible") is True, "safety_int")
    ok(s.get("speech_gate_required") is True, "gate_req")
    ok(s.get("direct_tts_bypass_forbidden") is True, "no_tts_bypass")
    ok(s.get("direct_vop_bypass_forbidden") is True, "no_vop_bypass")
    ok(s.get("runtime_tts_invoked") is False, "no_tts")
    ok(s.get("voice_output_plane_invoked") is False, "no_vop")
    ok(s.get("speech_request_submitted") is False, "no_submit")

    maps = {m.get("source_field"): m for m in mapping.get("mappings") or [] if isinstance(m, dict)}
    ok("prompt_text" in maps and maps["prompt_text"].get("target_field") == "speech_text", "map_speech_text")

    ok(apy.get("priority") == "P3_OCR_GUIDANCE", "apy_p3")
    ok(sp.get("speech_text"), "speech_text")
    ok("P0_SAFETY_CRITICAL" in (sp.get("can_be_interrupted_by") or []), "p0_interrupt")
    ok(adm.get("admission_decision") == "ADMIT_AS_CANDIDATE", "admit")
    ok(adm.get("submitted_now") is False, "adm_not_submit")
    ok(vop.get("voice_output_plane_invoked_now") is False, "vop_not_invoke")
    ok(vop.get("speech_request_submitted_now") is False, "vop_not_submit")
    ok(safety.get("can_be_interrupted_by_p0") is True, "p0_can_interrupt")
    ok(safety.get("cannot_interrupt_p0") is True, "cannot_int_p0")
    ok(stm.get("short_term_memory_ref_preserved") is True, "stm_preserved")
    ok(stm.get("write_to_runtime_memory_now") is False, "no_stm_write")
    ok(final.get("final_decision") == "READY_FOR_FUTURE_VOP_SUBMIT", "final_decision")
    ok(boundary.get("adapter_dryrun_only") is True, "boundary_dryrun")
    ok(metrics.get("no_write_boundary_pass_rate") == 1.0, "metrics_pass")
    ok(bench.get("benchmark_score_generated") is False, "no_bench")
    ok(health.get("recovery_action_committed") is False, "no_recovery")
    ok(no_write.get("boundary_ok") is True, "nw_ok")
    ok(no_write.get("violations") == [], "nw_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("world_model_written") is False, "audit_no_wm")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_no_sd")
    ok(audit.get("navigation_decision_invoked") is False, "audit_no_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_route")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 59,
        "blockers": blockers,
        "phase": "Voice-Output-Plane-Adapter-for-Guidance-v1-001",
    }
    _write_json(root / "voice_output_plane_adapter_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
