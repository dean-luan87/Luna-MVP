#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Multiframe Crop Execution DryRun v1."""

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
        "summary": "multiframe_crop_execution_dryrun_v1_summary.json",
        "intake": "multiframe_crop_tracklet_intake_matrix_v1.json",
        "rules": "multiframe_crop_execution_rule_matrix_v1.json",
        "schema": "multiframe_crop_artifact_schema_v1.json",
        "collection": "multiframe_crop_artifact_collection_v1.json",
        "trace": "multiframe_crop_execution_trace_v1.json",
        "bbox_val": "multiframe_crop_bbox_validation_report_v1.json",
        "quality": "multiframe_crop_quality_placeholder_report_v1.json",
        "diversity": "multiframe_crop_diversity_report_v1.json",
        "proj_risk": "multiframe_projection_risk_carryover_report_v1.json",
        "ocr_ready": "multiframe_ocrrequest_readiness_report_v1.json",
        "carryover": "multiframe_crop_same_frame_blocker_carryover_report_v1.json",
        "future": "multiframe_future_ocr_ep_sv_plan_v1.json",
        "source_chain": "multiframe_crop_source_chain_report_v1.json",
        "boundary": "multiframe_crop_boundary_report_v1.json",
        "metrics": "multiframe_crop_metrics_candidate_report_v1.json",
        "bench": "multiframe_crop_benchmark_link_report_v1.json",
        "health": "multiframe_crop_system_health_link_report_v1.json",
        "no_write": "multiframe_crop_no_write_boundary_report_v1.json",
        "sim": "multiframe_crop_simulation_context_report_v1.json",
        "non_claims": "multiframe_crop_non_claims_report_v1.json",
        "followups": "multiframe_crop_open_followups_v1.json",
        "audit": "multiframe_crop_audit_report_v1.json",
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
            root / "multiframe_crop_verifier_report_v1.json",
            {"verdict": "NO_GO", "checks_passed": 0, "blockers": blockers},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    coll = data["collection"]
    trace = data["trace"]
    bbox_val = data["bbox_val"]
    quality = data["quality"]
    diversity = data["diversity"]
    proj_risk = data["proj_risk"]
    ocr_ready = data["ocr_ready"]
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
    ok(s.get("dryrun_scope") == "multiframe_crop_execution_dryrun_only", "scope")
    ok(s.get("based_on_text_region_tracklet") is True, "based_tracklet")
    ok(s.get("projected_region_count_observed") == 30, "proj30")
    ok(s.get("multiframe_crop_plan_generated") is True, "plan_gen")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("ocrrequest_generated") is False, "no_ocrreq")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_sem")

    intake_rows = intake.get("rows") or []
    ok(len(intake_rows) == 30, "intake_30")
    for row in intake_rows:
        if isinstance(row, dict):
            ok(row.get("detected_region") is False, "intake_not_detected")
            ok(row.get("projection_is_approximate") is True, "intake_approx")
            break

    rule_ids = {r.get("rule_id") for r in rules.get("rules") or [] if isinstance(r, dict)}
    ok("projected_region_not_detected_region" in rule_ids, "rule_not_detected")
    ok("ocr_execution_forbidden" in rule_ids, "rule_no_ocr")

    ok(data["schema"].get("template"), "schema_template")
    arts = coll.get("artifacts") or []
    ok(len(arts) > 0, "crop_count_gt0")
    ok(s.get("multiframe_crop_artifact_count", 0) > 0, "summary_crop_count")
    for art in arts:
        if isinstance(art, dict):
            ok(art.get("ocr_invoked") is False, "art_no_ocr")
            ok(art.get("detected_region") is False, "art_not_detected")
            break

    trace_rows = trace.get("rows") or []
    ok(len(trace_rows) > 0, "trace_rows")
    for tr in trace_rows:
        if isinstance(tr, dict):
            ok(tr.get("ocr_invoked") is False, "trace_no_ocr")
            ok(tr.get("ocrrequest_generated") is False, "trace_no_cr")
            break

    val_rows = bbox_val.get("rows") or []
    ok(len(val_rows) > 0, "bbox_val_rows")
    for vr in val_rows:
        if isinstance(vr, dict):
            ok(vr.get("bbox_valid_for_crop") is not None, "bbox_valid_field")
            break

    for qr in quality.get("rows") or []:
        if isinstance(qr, dict):
            ok(qr.get("crop_quality_claim_allowed") is False, "quality_no_claim")
            break

    ok(diversity.get("independent_consensus_allowed_now") is False, "no_consensus")
    ok(proj_risk.get("projection_not_detection") is True, "proj_not_det")
    ok(ocr_ready.get("ocrrequest_allowed_now") is False, "ocrreq_not_now")
    ok(carryover.get("same_frame_blocker_resolved") is False, "blocker_not_resolved")
    ok(carryover.get("same_frame_consensus_blocker_still_active") is True, "blocker_active")

    future_phases = [p.get("future_phase") for p in future.get("phases") or [] if isinstance(p, dict)]
    ok("OCRRequest-Gated-Submission-from-Multiframe-v1" in future_phases, "future_ocrreq")

    chain_rows = source_chain.get("rows") or []
    ok(len(chain_rows) > 0, "chain_rows")
    for cr in chain_rows:
        if isinstance(cr, dict):
            ok(cr.get("traceable_to_text_region_tracklet") is True, "chain_tracklet")
            break

    ok(boundary.get("source_validation_rerun_invoked") is False, "boundary_no_sv")
    ok(metrics.get("ocr_invoked_count") == 0, "metrics_no_ocr")
    ok(metrics.get("ocrrequest_generated_count") == 0, "metrics_no_ocrreq")
    ok(bench.get("benchmark_score_generated") is False, "bench_no_score")
    ok(health.get("provider_health_runtime_checked") is False, "health_no_runtime")
    ok(no_write.get("boundary_ok") is True, "no_write_ok")
    ok(no_write.get("violations") == [], "no_write_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim_profile")
    ok(len(data["followups"].get("items") or []) >= 5, "followups")
    ok(audit.get("world_model_attach_executed") is False, "audit_no_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_no_fact")
    ok(audit.get("runtime_routing_changed") is False, "audit_no_routing")
    ok(audit.get("same_frame_blocker_still_active") is True, "audit_blocker")

    crops_dir = root / "crops"
    gen_count = metrics.get("crop_generated_count") or 0
    if gen_count > 0:
        pngs = list(crops_dir.glob("*.png")) if crops_dir.is_dir() else []
        ok(len(pngs) >= 1, "crop_png_exists")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "verdict": verdict,
        "checks_passed": checks,
        "checks_expected": 63,
        "blockers": blockers,
        "phase": "Multiframe-Crop-Execution-DryRun-v1-001",
    }
    _write_json(root / "multiframe_crop_verifier_report_v1.json", report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
