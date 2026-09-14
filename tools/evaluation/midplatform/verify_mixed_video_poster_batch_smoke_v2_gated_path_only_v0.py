#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Mixed Video Poster Batch Smoke v2 Gated Path Only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
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
        "summary": "mixed_batch_v2_gated_path_summary.json",
        "manifest": "mixed_batch_v2_input_manifest.json",
        "input": "mixed_batch_v2_input_candidate_matrix.json",
        "sq": "mixed_batch_v2_source_quality_gate_decision_matrix.json",
        "read": "mixed_batch_v2_readability_gate_decision_matrix.json",
        "routing": "mixed_batch_v2_routing_matrix.json",
        "req": "mixed_batch_v2_ocr_request_candidate_matrix.json",
        "trace": "mixed_batch_v2_ocr_request_gated_submission_trace.json",
        "bypass": "mixed_batch_v2_direct_provider_bypass_detection_report.json",
        "ff": "mixed_batch_v2_full_frame_scan_boundary_report.json",
        "packs": "mixed_batch_v2_ocr_evidence_pack_collection.json",
        "pack_align": "mixed_batch_v2_evidence_pack_request_alignment_report.json",
        "sem": "mixed_batch_v2_ocr_semantic_candidate_collection.json",
        "sem_align": "mixed_batch_v2_semantic_candidate_request_alignment_report.json",
        "scan": "mixed_batch_v2_scan_observation_report.json",
        "vs_pf": "mixed_batch_v2_visual_symbol_public_facility_routing_report.json",
        "sq_rej": "mixed_batch_v2_source_quality_rejection_degrade_report.json",
        "unc": "mixed_batch_v2_uncertainty_guard_report.json",
        "metrics": "mixed_batch_v2_metrics_candidate_report.json",
        "bench": "mixed_batch_v2_benchmark_link_report.json",
        "health": "mixed_batch_v2_system_health_link_report.json",
        "boundary": "mixed_batch_v2_no_write_boundary_report.json",
        "sim": "mixed_batch_v2_simulation_context_report.json",
        "non_claims": "mixed_batch_v2_non_claims_report.json",
        "followups": "mixed_batch_v2_open_followups.json",
        "audit": "mixed_batch_v2_audit_report.json",
    }

    data = {}
    for k, fname in files.items():
        p = root / fname
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "mixed_batch_v2_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    bypass = data["bypass"]
    ff = data["ff"]
    trace = data["trace"]
    packs = data["packs"]
    pack_align = data["pack_align"]
    sem_align = data["sem_align"]
    sq = data["sq"]
    req = data["req"]
    scan = data["scan"]
    vs_pf = data["vs_pf"]
    sq_rej = data["sq_rej"]
    unc = data["unc"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    boundary = data["boundary"]
    sim = data["sim"]
    non_claims = data["non_claims"]
    followups = data["followups"]
    audit = data["audit"]
    manifest = data["manifest"]
    inp = data["input"]

    ok(s.get("batch_scope") == "mixed_video_poster_gated_path_only_smoke", "batch_scope")
    ok(s.get("uses_gated_runtime_path") is True, "uses_gated")
    ok(s.get("direct_provider_bypass") is False, "summary_bypass")
    ok(bypass.get("capability_imports_rapidocr") is False, "no_rapidocr_import")
    ok(bypass.get("direct_rapidocr_call_detected") is False, "no_rapidocr_call")
    ok(s.get("ocr_mainline_bridge_required") is True, "bridge_required")
    ok(len(manifest.get("videos") or []) == 8, "video_count")
    ok(len(manifest.get("images") or []) == 10, "image_count")
    ok(inp.get("row_count", 0) > 0, "input_candidates")
    ok(sq.get("sq_e_submitted_to_ocr") is False, "sq_e_not_submitted")
    ok(sq_rej.get("sq_e_submitted_to_ocr") is False, "sq_rej_e")
    ok(all(isinstance(r, dict) and r.get("readability_grade") for r in (data["read"].get("rows") or [])), "read_grades")
    ok(all(isinstance(r, dict) and r.get("source_quality_grade") for r in (req.get("rows") or [])), "req_sq")
    ok(all(isinstance(r, dict) and r.get("readability_grade") for r in (req.get("rows") or [])), "req_read")
    ok(trace.get("direct_provider_bypass") is False, "trace_bypass")
    ok(trace.get("every_provider_call_has_ocr_request_ref") is True, "trace_ref")
    ok(bypass.get("provider_calls_without_ocr_request_ref", 1) == 0, "no_orphan_provider")
    ok(bypass.get("evidence_packs_without_ocr_request_ref", 1) == 0, "no_orphan_pack")
    ok(ff.get("full_frame_scan_allowed_for_primary_evidence") is False, "ff_not_primary")
    ok(packs.get("every_evidence_pack_has_ocr_request_ref") is True, "packs_ref")
    ok(pack_align.get("every_evidence_pack_has_ocr_request_ref") is True, "pack_align")
    for p in packs.get("packs") or []:
        if isinstance(p, dict):
            ref = p.get("ocr_request_ref") or (p.get("source") or {}).get("ocr_request_ref")
            ok(ref is not None and ref.get("request_id"), "pack_request_id")
    ok(sem_align.get("every_semantic_candidate_traceable_to_request") is True, "sem_trace")
    ok(scan.get("scan_observation_count", 0) >= 0, "scan_report")
    ok(vs_pf.get("no_brand_fact_without_registry_or_review") is True, "no_brand_fact")
    ok(sq_rej.get("low_quality_not_equal_provider_failure") is True, "lq_not_fail")
    ok(unc.get("empty_text_is_not_no_text_fact") is True, "empty_guard")
    ok(metrics.get("direct_provider_bypass") is False, "metrics_bypass")
    ok(metrics.get("every_provider_call_has_ocr_request_ref") is True, "metrics_provider_ref")
    ok(bench.get("benchmark_score_generated") is False, "bench_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_runtime")
    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(non_claims.get("go_means_gated_path_replacement_only") is True, "non_claims_go")
    ok(len(followups.get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(root / "mixed_batch_v2_verifier_report.json", {"schema_version": "mixed_batch_v2_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks})
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
