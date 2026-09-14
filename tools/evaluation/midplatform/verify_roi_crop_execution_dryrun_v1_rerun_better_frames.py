#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI Crop Rerun With Better Frames."""

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
        "summary": "roi_crop_rerun_better_frames_summary.json",
        "intake": "roi_crop_rerun_better_frame_candidate_intake_matrix.json",
        "policy": "roi_crop_rerun_execution_policy_v1.json",
        "resolution": "roi_crop_rerun_source_resolution_report.json",
        "bbox": "roi_crop_rerun_bbox_validation_report.json",
        "schema": "roi_crop_rerun_artifact_schema_v1.json",
        "collection": "roi_crop_rerun_artifact_collection_v1.json",
        "trace": "roi_crop_rerun_execution_trace_v1.json",
        "deferred": "roi_crop_rerun_deferred_report_v1.json",
        "mixed": "roi_crop_rerun_mixed_region_handling_report_v1.json",
        "ocr_plan": "roi_crop_rerun_to_ocr_request_reference_plan_v1.json",
        "boundary": "roi_crop_rerun_boundary_report_v1.json",
        "source_chain": "roi_crop_rerun_source_chain_report_v1.json",
        "metrics": "roi_crop_rerun_metrics_candidate_report_v1.json",
        "bench": "roi_crop_rerun_benchmark_link_report_v1.json",
        "health": "roi_crop_rerun_system_health_link_report_v1.json",
        "no_write": "roi_crop_rerun_no_write_boundary_report_v1.json",
        "sim": "roi_crop_rerun_simulation_context_report_v1.json",
        "non_claims": "roi_crop_rerun_non_claims_report_v1.json",
        "followups": "roi_crop_rerun_open_followups_v1.json",
        "audit": "roi_crop_rerun_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_crop_rerun_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    policy = data["policy"]
    resolution = data["resolution"]
    bbox = data["bbox"]
    schema = data["schema"]
    collection = data["collection"]
    trace = data["trace"]
    deferred = data["deferred"]
    mixed = data["mixed"]
    ocr_plan = data["ocr_plan"]
    boundary = data["boundary"]
    source_chain = data["source_chain"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("dryrun_scope") == "roi_crop_rerun_with_better_frames_only", "scope")
    ok(s.get("based_on_better_frame_selection") is True, "based_bf")
    ok(s.get("ready_later_candidate_count_observed") == 12, "ready_12")
    ok(s.get("rerun_crop_candidate_count") == 12, "rerun_12")
    ok(s.get("new_video_decoded") is False, "no_decode")
    ok(s.get("new_frame_extracted") is False, "no_extract")
    ok(s.get("ocr_request_generated") is False, "no_ocr_req")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")

    ok(intake.get("row_count") == 12, "intake_12")

    rule_ids = {r.get("rule_id") for r in (policy.get("rules") or []) if isinstance(r, dict)}
    ok("no_new_video_decoding" in rule_ids, "rule_no_decode")
    ok("no_new_frame_extraction" in rule_ids, "rule_no_extract")
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")

    ok(resolution.get("row_count", 0) >= 1, "resolution")
    for row in resolution.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("new_video_decoding_required") is False, "res_no_decode")
            ok(row.get("new_frame_extraction_required") is False, "res_no_extract")
            break

    ok(bbox.get("row_count", 0) >= 1, "bbox")
    ok(schema.get("defaults", {}).get("ocr_request_allowed_in_this_phase") is False, "schema_ocr")

    art_count = collection.get("artifact_count", 0)
    ok(art_count > 0, "artifacts")
    for row in collection.get("artifacts") or []:
        if isinstance(row, dict):
            ok(row.get("crop_generation_status") != "crop_ready", "not_crop_ready")
            break

    ok(trace.get("row_count", 0) >= 1, "trace")
    for row in trace.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("new_video_decoded") is False, "trace_no_decode")
            ok(row.get("new_frame_extracted") is False, "trace_no_extract")
            ok(row.get("ocr_invoked") is False, "trace_no_ocr")
            ok(row.get("provider_invoked") is False, "trace_no_provider")
            break

    ok(deferred.get("future_detector_deferred_count") == 8, "fd_8")
    ok(deferred.get("multiframe_deferred_count") == 7, "mf_7")
    ok(deferred.get("row_count", 0) >= 15, "deferred_rows")

    ok(mixed.get("row_count", 0) >= 0, "mixed")
    for row in mixed.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("semantic_join_allowed") is False, "no_join")
            ok(row.get("cross_region_text_join_allowed") is False, "no_cross")
            break

    ok(ocr_plan.get("current_phase_ocr_request_generated") is False, "plan_no_ocr")
    ok(boundary.get("roi_crop_rerun_dryrun_only") is True, "boundary")
    ok(boundary.get("evidence_pack_generated") is False, "boundary_ep")
    ok(source_chain.get("all_traceable_to_better_frame_selection") is True, "trace_bf")
    ok(metrics.get("ocr_request_generated_count") == 0, "metrics_ocr")
    ok(metrics.get("new_frame_extracted_count") == 0, "metrics_extract")
    ok(metrics.get("roi_crop_executed_count", 0) >= 0, "metrics_crop")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_crop_rerun_better_frames_executed") is True, "audit")
    ok(audit.get("new_frame_extracted") is False, "audit_extract")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_crop_rerun_verifier_report_v1.json",
        {"schema_version": "roi_crop_rerun_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
