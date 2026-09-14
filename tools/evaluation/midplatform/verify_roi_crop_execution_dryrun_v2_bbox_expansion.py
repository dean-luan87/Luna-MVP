#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI Crop Execution DryRun v2 BBoxExpansion."""

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
        "summary": "roi_crop_v2_bbox_expansion_summary.json",
        "intake": "roi_crop_v2_expansion_candidate_intake_matrix.json",
        "policy": "roi_crop_v2_bbox_expansion_execution_policy.json",
        "resolution": "roi_crop_v2_source_frame_resolution_report.json",
        "bbox": "roi_crop_v2_expanded_bbox_validation_report.json",
        "schema": "roi_crop_v2_expanded_artifact_schema.json",
        "collection": "roi_crop_v2_expanded_artifact_collection.json",
        "trace": "roi_crop_v2_execution_trace.json",
        "comparison": "roi_crop_v2_size_context_comparison_report.json",
        "diversity": "roi_crop_v2_expanded_crop_diversity_report.json",
        "deferred": "roi_crop_v2_deferred_report.json",
        "ocr_plan": "roi_crop_v2_to_ocrrequest_reference_plan.json",
        "boundary": "roi_crop_v2_boundary_report.json",
        "chain": "roi_crop_v2_source_chain_report.json",
        "metrics": "roi_crop_v2_metrics_candidate_report.json",
        "bench": "roi_crop_v2_benchmark_link_report.json",
        "health": "roi_crop_v2_system_health_link_report.json",
        "no_write": "roi_crop_v2_no_write_boundary_report.json",
        "sim": "roi_crop_v2_simulation_context_report.json",
        "non_claims": "roi_crop_v2_non_claims_report.json",
        "followups": "roi_crop_v2_open_followups.json",
        "audit": "roi_crop_v2_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_crop_v2_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    audit = data["audit"]
    rule_ids = [r.get("rule_id") for r in (data["policy"].get("rules") or []) if isinstance(r, dict)]

    ok(s.get("dryrun_scope") == "bbox_expansion_crop_execution_only", "scope")
    ok(s.get("based_on_bbox_expansion_proposal") is True, "based_exp")
    ok(s.get("expansion_candidate_count_observed") == 4, "cand_4")
    ok(s.get("crop_execution_attempted") is True, "exec_attempted")
    ok(s.get("expanded_crop_artifact_generated") is True, "artifact_gen")
    ok(s.get("new_ocr_invoked") is False, "no_ocr")
    ok(s.get("new_frame_extracted") is False, "no_frame")

    ok(data["intake"].get("row_count") == 4, "intake_4")
    ok("preserve_original_bbox" in rule_ids, "rule_preserve")
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")

    for row in data["resolution"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("new_frame_extracted") is False, "res_no_new_frame")
            ok(row.get("video_scan_invoked") is False, "res_no_scan")
            break

    for row in data["bbox"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("bbox_within_bounds") is True, "bbox_in_bounds")
            break

    ok(data["schema"].get("template"), "schema_tpl")
    coll = data["collection"]
    ok(coll.get("artifact_count") == 4, "coll_4")

    gen_count = 0
    for art in coll.get("rows") or []:
        if not isinstance(art, dict):
            continue
        if art.get("crop_generation_status") == "generated":
            gen_count += 1
            fp = art.get("crop_file_path")
            if fp:
                ok(Path(fp).is_file(), f"file_exists:{art.get('expansion_strategy')}")
            ok(art.get("source_bbox_xyxy") == [292.0, 367.0, 381.0, 395.0], "src_bbox_preserved")
            ok(art.get("source_bbox_expansion_candidate_id"), "exp_ref")

    ok(gen_count >= 4 or s.get("expanded_crop_deferred_count", 0) > 0, "gen_or_defer")

    for row in data["trace"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("ocr_invoked") is False, "trace_no_ocr")
            break

    ok(data["diversity"].get("unique_expanded_bbox_count", 0) >= 4 or gen_count < 4, "div_bbox")
    ok(data["diversity"].get("quality_claim_allowed") is False, "no_quality_claim")
    ok(data["ocr_plan"].get("future_phase") == "ROI-to-OCRRequest-Reference-v2-BBoxExpansion", "ocr_plan_phase")
    for row in data["ocr_plan"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("current_phase_ocrrequest_generated") is False, "ocr_plan_no_gen")
            break

    ok(data["boundary"].get("ocrrequest_generated") is False, "boundary_ocr")
    ok(data["chain"].get("rows"), "chain_rows")
    for row in data["chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_bbox_expansion_candidate") is True, "chain_exp")
            break

    ok(data["metrics"].get("new_ocr_invoked_count") == 0, "metrics_no_ocr")
    ok(data["metrics"].get("ocrrequest_generated_count") == 0, "metrics_no_req")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_crop_execution_dryrun_v2_bbox_expansion_executed") is True, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_crop_v2_verifier_report_v1.json",
        {"schema_version": "roi_crop_v2_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
