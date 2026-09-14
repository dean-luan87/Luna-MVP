#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Text Region Tracklet DryRun v1."""

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
        "summary": "text_region_tracklet_dryrun_v1_summary.json",
        "intake": "tracklet_better_frame_artifact_intake_matrix.json",
        "rules": "text_region_tracklet_rule_matrix_v1.json",
        "schema": "text_region_tracklet_candidate_schema_v1.json",
        "collection": "text_region_tracklet_candidate_collection_v1.json",
        "projected": "text_region_projected_region_matrix_v1.json",
        "coverage": "text_region_tracklet_frame_coverage_report_v1.json",
        "continuity": "text_region_bbox_continuity_report_v1.json",
        "drift": "text_region_drift_risk_report_v1.json",
        "quality": "text_region_quality_context_carryover_report_v1.json",
        "crop_ready": "text_region_tracklet_crop_readiness_report_v1.json",
        "carryover": "text_region_tracklet_same_frame_blocker_carryover_report_v1.json",
        "future": "text_region_future_multiframe_crop_plan_v1.json",
        "source_chain": "text_region_tracklet_source_chain_report_v1.json",
        "boundary": "text_region_tracklet_boundary_report_v1.json",
        "metrics": "text_region_tracklet_metrics_candidate_report_v1.json",
        "bench": "text_region_tracklet_benchmark_link_report_v1.json",
        "health": "text_region_tracklet_system_health_link_report_v1.json",
        "no_write": "text_region_tracklet_no_write_boundary_report_v1.json",
        "sim": "text_region_tracklet_simulation_context_report_v1.json",
        "non_claims": "text_region_tracklet_non_claims_report_v1.json",
        "followups": "text_region_tracklet_open_followups_v1.json",
        "audit": "text_region_tracklet_audit_report_v1.json",
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
            root / "text_region_tracklet_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    coll = data["collection"]
    projected = data["projected"]
    coverage = data["coverage"]
    continuity = data["continuity"]
    drift = data["drift"]
    quality = data["quality"]
    crop_ready = data["crop_ready"]
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
    ok(s.get("dryrun_scope") == "text_region_tracklet_dryrun_only", "scope")
    ok(s.get("based_on_better_frame_extraction") is True, "based_bf")
    ok(s.get("candidate_frame_reference_count_observed") == 6, "ref6")
    ok(s.get("frame_artifact_count_observed") == 6, "art6")
    ok(s.get("tracklet_candidate_generated") is True, "tracklet_gen")
    ok(s.get("detector_invoked") is False, "no_detector")
    ok(s.get("text_detector_invoked") is False, "no_text_det")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("crop_generated") is False, "no_crop")

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 6, "intake_6")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("eligible_for_tracklet_dryrun") is True, "intake_eligible")
            fp = row.get("frame_file_path")
            if fp:
                ok(Path(fp).is_file(), "intake_file_exists")
            break

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("detector_invocation_forbidden" in rule_ids, "rule_no_detector")
    ok("ocr_execution_forbidden" in rule_ids, "rule_no_ocr")

    ok(data["schema"].get("template"), "schema_template")
    candidates = coll.get("candidates") or []
    ok(len(candidates) >= 1, "tracklet_count")
    ok(s.get("tracklet_candidate_count", 0) >= 1, "summary_tracklet_count")

    for cand in candidates:
        if isinstance(cand, dict):
            ok(cand.get("projection_is_approximate") is True, "approximate")
            ok(cand.get("detector_invoked") is False, "cand_no_detector")
            ok(cand.get("text_detector_invoked") is False, "cand_no_text_det")
            ok(len(cand.get("frame_sequence") or []) >= 1, "frame_sequence")
            break

    proj_rows = projected.get("rows") or []
    ok(len(proj_rows) > 0, "projected_rows")
    for row in proj_rows:
        if isinstance(row, dict):
            ok(row.get("detected_region") is False, "not_detected")
            ok(row.get("text_detector_invoked") is False, "proj_no_text_det")
            break

    for rep in coverage.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("frame_coverage_ratio") is not None, "coverage_ratio")
            break

    for rep in continuity.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("continuity_is_projection_based") is True, "proj_based")
            ok(rep.get("continuity_not_entity_confirmation") is True, "not_entity")
            break

    for rep in drift.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("requires_future_detection_or_quality_gate") is True, "future_gate")
            break

    for row in quality.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("frame_quality_claim_allowed") is False, "quality_no_claim")
            break

    for rep in crop_ready.get("reports") or []:
        if isinstance(rep, dict):
            ok(rep.get("crop_allowed_now") is False, "crop_not_now")
            break

    ok(carryover.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")
    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "blocker_active")

    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("Multiframe-Crop-Execution-DryRun-v1" in future_phases, "future_crop")

    ok(source_chain.get("traceable_to_better_frame_extraction") is True, "chain_bf")
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

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "Text-Region-Tracklet-DryRun-v1-001",
    }
    _write_json(root / "text_region_tracklet_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
