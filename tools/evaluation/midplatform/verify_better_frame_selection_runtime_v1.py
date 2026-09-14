#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Better Frame Selection Runtime v1."""

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
        "summary": "better_frame_selection_runtime_v1_summary.json",
        "intake": "better_frame_candidate_intake_matrix_v1.json",
        "rules": "better_frame_selection_rule_matrix_v1.json",
        "schema": "better_frame_candidate_schema_v1.json",
        "collection": "better_frame_candidate_collection_v1.json",
        "reason": "better_frame_selection_reason_report_v1.json",
        "existing": "better_frame_existing_candidate_report_v1.json",
        "neighbor": "better_frame_neighboring_multiframe_requirement_report_v1.json",
        "readiness": "better_frame_future_roi_crop_readiness_matrix_v1.json",
        "routing": "better_frame_routing_matrix_v1.json",
        "future": "better_frame_future_execution_plan_v1.json",
        "boundary": "better_frame_boundary_report_v1.json",
        "source_chain": "better_frame_source_chain_report_v1.json",
        "metrics": "better_frame_metrics_candidate_report_v1.json",
        "bench": "better_frame_benchmark_link_report_v1.json",
        "health": "better_frame_system_health_link_report_v1.json",
        "no_write": "better_frame_no_write_boundary_report_v1.json",
        "sim": "better_frame_simulation_context_report_v1.json",
        "non_claims": "better_frame_non_claims_report_v1.json",
        "followups": "better_frame_open_followups_v1.json",
        "audit": "better_frame_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "better_frame_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    rules = data["rules"]
    schema = data["schema"]
    collection = data["collection"]
    existing = data["existing"]
    neighbor = data["neighbor"]
    readiness = data["readiness"]
    routing = data["routing"]
    future = data["future"]
    boundary = data["boundary"]
    source_chain = data["source_chain"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("runtime_scope") == "better_frame_selection_runtime_only", "scope")
    ok(s.get("based_on_roi_crop_execution_dryrun") is True, "based_crop")
    ok(s.get("better_frame_candidate_generated") is True, "candidates_generated")
    ok(s.get("selection_planning_only") is True, "planning_only")
    ok(s.get("new_video_decoded") is False, "no_decode")
    ok(s.get("new_frame_extracted") is False, "no_extract")
    ok(s.get("roi_crop_executed") is False, "no_crop")
    ok(s.get("ocr_request_generated") is False, "no_ocr_req")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")
    ok(intake.get("row_count", 0) >= 1, "intake_exists")
    ok(intake.get("row_count") == s.get("deferred_crop_item_count_observed", -1), "intake_matches_deferred")

    rule_ids = {r.get("rule_id") for r in (rules.get("rules") or []) if isinstance(r, dict)}
    ok("no_new_frame_extraction_in_this_phase" in rule_ids, "rule_no_extract")
    ok("no_video_decoding_in_this_phase" in rule_ids, "rule_no_decode")
    ok("no_crop_execution_in_this_phase" in rule_ids, "rule_no_crop")

    ok(schema.get("defaults", {}).get("new_frame_extracted") is False, "schema_no_extract")
    ok(schema.get("defaults", {}).get("crop_executed") is False, "schema_no_crop")
    ok(collection.get("candidate_count", 0) > 0, "collection_count")

    for cand in collection.get("candidates") or []:
        if isinstance(cand, dict):
            ok(cand.get("new_frame_extracted") is False, "cand_no_extract")
            ok(cand.get("crop_executed") is False, "cand_no_crop")
            readiness_val = cand.get("expected_roi_crop_readiness")
            ok(readiness_val != "crop_ready", "not_crop_ready_label")
            if cand.get("current_source_quality_grade") == "SQ_E":
                ok(readiness_val in ("needs_better_source", "needs_detector", "needs_multiframe", "unavailable", "ready_later"), "sq_e_readiness")
            break

    ok(data["reason"].get("row_count", 0) >= 1, "reason_report")
    ok(existing.get("row_count", 0) >= 1, "existing_report")
    for row in existing.get("rows") or []:
        if isinstance(row, dict) and row.get("source_quality_grade") == "SQ_E":
            ok(row.get("reuse_as_better_frame_candidate") is False, "sq_e_not_reuse_crop_ready")
            break

    ok(neighbor.get("row_count", 0) >= 0, "neighbor_report")
    for row in neighbor.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("new_frame_extraction_allowed_in_this_phase") is False, "no_extract_neighbor")
            break

    ok(readiness.get("row_count", 0) >= 1, "readiness_matrix")
    for row in readiness.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("ocr_request_allowed_now") is False, "ocr_not_now")
            break

    ok(routing.get("row_count", 0) >= 1, "routing_matrix")
    for row in routing.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("crop_executed") is False, "route_no_crop")
            ok(row.get("ocr_request_generated") is False, "route_no_ocr")
            break

    phases = [p.get("future_phase") for p in (future.get("phases") or []) if isinstance(p, dict)]
    ok("ROI-Crop-Execution-DryRun-v1-rerun" in phases, "future_crop_rerun")

    ok(boundary.get("better_frame_selection_only") is True, "boundary_only")
    ok(boundary.get("evidence_pack_generated") is False, "boundary_no_ep")
    ok(source_chain.get("all_traceable_to_roi_crop_execution") is True, "trace_crop")
    ok(metrics.get("new_frame_extracted_count") == 0, "metrics_no_extract")
    ok(metrics.get("roi_crop_executed_count") == 0, "metrics_no_crop")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("better_frame_selection_runtime_v1_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "better_frame_verifier_report_v1.json",
        {"schema_version": "better_frame_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
