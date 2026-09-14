#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Better Frame Extraction DryRun v1."""

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


def _read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


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
        "summary": "better_frame_extraction_dryrun_v1_summary.json",
        "window_intake": "better_frame_multiframe_window_intake_matrix.json",
        "rules": "better_frame_extraction_rule_matrix.json",
        "frame_ref_schema": "better_frame_candidate_frame_reference_schema.json",
        "frame_ref_collection": "better_frame_candidate_frame_reference_collection.json",
        "materialization_plan": "better_frame_materialization_plan.json",
        "artifact_collection": "better_frame_artifact_collection.json",
        "extraction_trace": "better_frame_extraction_trace.json",
        "quality": "better_frame_quality_placeholder_report.json",
        "coverage": "better_frame_region_coverage_hint_report.json",
        "diversity": "better_frame_candidate_diversity_report.json",
        "carryover": "better_frame_same_frame_blocker_carryover_report.json",
        "future": "better_frame_future_tracklet_crop_plan.json",
        "source_chain": "better_frame_source_chain_report.json",
        "boundary": "better_frame_boundary_report.json",
        "metrics": "better_frame_metrics_candidate_report.json",
        "bench": "better_frame_benchmark_link_report.json",
        "health": "better_frame_system_health_link_report.json",
        "no_write": "better_frame_no_write_boundary_report.json",
        "sim": "better_frame_simulation_context_report.json",
        "non_claims": "better_frame_non_claims_report.json",
        "followups": "better_frame_open_followups.json",
        "audit": "better_frame_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(
            root / "better_frame_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["window_intake"]
    rules = data["rules"]
    refs = data["frame_ref_collection"]
    mat_plan = data["materialization_plan"]
    artifacts = data["artifact_collection"]
    traces = data["extraction_trace"]
    quality = data["quality"]
    coverage = data["coverage"]
    diversity = data["diversity"]
    carryover = data["carryover"]
    future = data["future"]
    source_chain = data["source_chain"]
    boundary = data["boundary"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(True, "summary_exists")
    ok(s.get("dryrun_scope") == "better_frame_extraction_dryrun_only", "scope")
    ok(s.get("based_on_multiframe_merge_proposal") is True, "based_mf")
    ok("f001620" in str(s.get("source_frame_id") or ""), "source_frame")
    ok(s.get("candidate_frame_reference_generated") is True, "refs_generated")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("crop_generated") is False, "no_crop")
    ok(s.get("ocrrequest_generated") is False, "no_ocrreq")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")

    window_types = {r.get("window_type") for r in intake.get("rows") or [] if isinstance(r, dict)}
    ok("tight" in window_types and "wide" in window_types, "tight_wide_intake")

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")
    ok("no_crop_generation_in_this_phase" in rule_ids, "rule_no_crop")

    ok(data["frame_ref_schema"].get("template"), "schema_template")
    ref_list = refs.get("references") or []
    ok(len(ref_list) > 0, "ref_count")
    ok(s.get("candidate_frame_reference_count", 0) > 0, "summary_ref_count")

    for plan in mat_plan.get("plans") or []:
        if isinstance(plan, dict):
            ok(plan.get("video_scan_invoked") is False, "plan_no_scan")
            ok(plan.get("new_frame_discovery") is False, "plan_no_discovery")
            break

    art_list = artifacts.get("artifacts") or []
    ok(len(art_list) > 0, "artifacts_exist")
    statuses = {a.get("frame_materialization_status") for a in art_list if isinstance(a, dict)}
    ok(statuses.issubset({"generated", "deferred", "failed", None}) or "generated" in statuses, "artifact_status")

    for tr in traces.get("traces") or []:
        if isinstance(tr, dict):
            ok(tr.get("ocr_invoked") is False, "trace_no_ocr")
            ok(tr.get("crop_generated") is False, "trace_no_crop")
            ok(tr.get("video_scan_invoked") is False, "trace_no_scan")
            break

    for row in quality.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("frame_quality_claim_allowed") is False, "quality_no_claim")
            break

    for row in coverage.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("region_tracking_not_executed") is True, "no_tracking")
            break

    ok(diversity.get("same_frame_blocker_resolved") is False, "diversity_blocker")
    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "carryover_active")

    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Text-Region-Tracklet-DryRun-v1" in future_phases, "future_tracklet")

    ok(source_chain.get("traceable_to_multiframe_proposal") is True, "chain_mf")

    ok(boundary.get("source_validation_rerun_invoked") is False, "boundary_no_sv")
    ok(metrics.get("ocr_invoked_count") == 0, "metrics_no_ocr")
    ok(metrics.get("crop_generated_count") == 0, "metrics_no_crop")

    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")

    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")

    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")

    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")

    for art in art_list:
        if isinstance(art, dict) and art.get("frame_materialization_status") == "generated":
            fp = art.get("frame_file_path")
            if fp and not Path(fp).is_file():
                blockers.append(f"missing_artifact_file:{fp}")
            break

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 61,
        "blockers": blockers,
        "phase": "Better-Frame-Extraction-DryRun-v1-001",
    }
    _write_json(root / "better_frame_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
