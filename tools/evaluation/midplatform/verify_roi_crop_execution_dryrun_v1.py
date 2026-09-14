#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI Crop Execution DryRun v1."""

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
        "summary": "roi_crop_execution_dryrun_v1_summary.json",
        "intake": "roi_crop_candidate_intake_matrix_v1.json",
        "policy": "roi_crop_execution_policy_v1.json",
        "schema": "roi_crop_artifact_schema_v1.json",
        "collection": "roi_crop_artifact_collection_v1.json",
        "bbox": "roi_crop_bbox_validation_report_v1.json",
        "resolution": "roi_crop_source_resolution_report_v1.json",
        "trace": "roi_crop_execution_trace_v1.json",
        "mixed": "roi_crop_mixed_region_handling_report_v1.json",
        "deferred": "roi_crop_better_frame_deferred_report_v1.json",
        "ocr_plan": "roi_crop_to_ocr_request_reference_plan_v1.json",
        "boundary": "roi_crop_boundary_report_v1.json",
        "source_chain": "roi_crop_source_chain_report_v1.json",
        "metrics": "roi_crop_metrics_candidate_report_v1.json",
        "bench": "roi_crop_benchmark_link_report_v1.json",
        "health": "roi_crop_system_health_link_report_v1.json",
        "no_write": "roi_crop_no_write_boundary_report_v1.json",
        "sim": "roi_crop_simulation_context_report_v1.json",
        "non_claims": "roi_crop_non_claims_report_v1.json",
        "followups": "roi_crop_open_followups_v1.json",
        "audit": "roi_crop_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_crop_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    policy = data["policy"]
    schema = data["schema"]
    collection = data["collection"]
    bbox = data["bbox"]
    resolution = data["resolution"]
    trace = data["trace"]
    mixed = data["mixed"]
    deferred = data["deferred"]
    ocr_plan = data["ocr_plan"]
    boundary = data["boundary"]
    source_chain = data["source_chain"]
    metrics = data["metrics"]
    bench = data["bench"]
    health = data["health"]
    no_write = data["no_write"]
    sim = data["sim"]
    audit = data["audit"]

    ok(s.get("dryrun_scope") == "roi_crop_execution_dryrun_only", "scope")
    ok(s.get("based_on_roi_retry_proposal_runtime") is True, "based_roi_retry")
    ok(s.get("proposal_count_observed", 0) > 0, "proposal_count")
    ok(s.get("crop_execution_attempted") is True, "attempted")
    ok(s.get("ocr_request_generated") is False, "no_ocr_req")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(s.get("evidence_pack_generated") is False, "no_ep")
    ok(s.get("semantic_candidate_generated") is False, "no_semantic")
    ok(s.get("world_model_attach_executed") is False, "no_wm")
    ok(s.get("midplatform_fact_written") is False, "no_fact")
    ok(s.get("runtime_routing_changed") is False, "no_routing")

    ok(intake.get("row_count", 0) >= 1, "intake_exists")

    rule_ids = {r.get("rule_id") for r in (policy.get("rules") or []) if isinstance(r, dict)}
    ok("no_ocr_execution_in_this_phase" in rule_ids, "rule_no_ocr")
    ok("no_ocr_request_generation_in_this_phase" in rule_ids, "rule_no_ocr_req")

    ok(schema.get("defaults", {}).get("ocr_request_allowed_in_this_phase") is False, "schema_ocr_false")
    ok("crop_bbox_xyxy" in (schema.get("template") or {}), "schema_bbox")

    art_count = collection.get("artifact_count", 0)
    ok(art_count > 0, "artifact_count")
    for row in collection.get("artifacts") or []:
        if isinstance(row, dict):
            ok(row.get("fact_status") == "not_fact", "art_not_fact")
            break

    ok(bbox.get("row_count", 0) >= 1, "bbox_report")
    has_null_defer = False
    for row in bbox.get("rows") or []:
        if isinstance(row, dict) and row.get("bbox_validation_status") == "null_bbox_deferred":
            has_null_defer = True
            ok(row.get("crop_allowed") is False, "null_no_crop")
            break
    ok(has_null_defer or bbox.get("row_count", 0) > 0, "bbox_null_handling")

    ok(resolution.get("row_count", 0) >= 1, "resolution_report")

    ok(trace.get("row_count", 0) >= 1, "trace_exists")
    for row in trace.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("ocr_invoked") is False, "trace_no_ocr")
            ok(row.get("provider_invoked") is False, "trace_no_provider")
            ok(row.get("evidence_pack_generated") is False, "trace_no_ep")
            break

    ok(mixed.get("row_count", 0) >= 1, "mixed_report")
    for row in mixed.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("semantic_join_allowed") is False, "no_semantic_join")
            ok(row.get("cross_region_text_join_allowed") is False, "no_cross_join")
            break

    ok(deferred.get("row_count", 0) >= 1, "deferred_report")
    ok(ocr_plan.get("current_phase_ocr_request_generated") is False, "plan_no_ocr_req")

    ok(boundary.get("roi_crop_dryrun_only") is True, "boundary_dryrun")
    ok(boundary.get("evidence_pack_generated") is False, "boundary_no_ep")

    ok(source_chain.get("row_count", 0) >= 1, "chain_exists")
    ok(source_chain.get("all_traceable_to_roi_retry_proposal") is True, "trace_proposal")
    for row in source_chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_roi_retry_proposal") is True, "row_trace")
            ok(row.get("source_chain_preserved") is True, "chain_preserved")
            break

    ok(metrics.get("ocr_request_generated_count") == 0, "metrics_ocr")
    ok(metrics.get("provider_invoked_count") == 0, "metrics_provider")
    ok(bench.get("benchmark_score_generated") is False, "bench")
    ok(health.get("provider_health_runtime_checked") is False, "health")
    ok(no_write.get("boundary_ok") is True, "boundary_ok")
    ok(no_write.get("violations") == [], "no_violations")
    ok(sim.get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_crop_execution_dryrun_v1_executed") is True, "audit_run")
    ok(audit.get("ocr_request_generated") is False, "audit_ocr_req")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_crop_verifier_report_v1.json",
        {"schema_version": "roi_crop_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
