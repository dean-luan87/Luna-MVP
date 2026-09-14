#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI-to-OCRRequest Reference v1."""

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
        "summary": "roi_to_ocrrequest_reference_v1_summary.json",
        "intake": "roi_to_ocrrequest_crop_intake_matrix_v1.json",
        "schema": "roi_ocrrequest_reference_schema_v1.json",
        "collection": "roi_ocrrequest_reference_collection_v1.json",
        "excluded": "roi_to_ocrrequest_excluded_crop_report_v1.json",
        "gate": "roi_ocrrequest_gate_metadata_report_v1.json",
        "payload": "roi_ocrrequest_payload_candidate_matrix_v1.json",
        "alignment": "roi_ocrrequest_reference_alignment_report_v1.json",
        "source_chain": "roi_ocrrequest_reference_source_chain_report_v1.json",
        "future": "roi_ocrrequest_future_submission_plan_v1.json",
        "boundary": "roi_ocrrequest_reference_boundary_report_v1.json",
        "metrics": "roi_ocrrequest_reference_metrics_candidate_report_v1.json",
        "bench": "roi_ocrrequest_reference_benchmark_link_report_v1.json",
        "health": "roi_ocrrequest_reference_system_health_link_report_v1.json",
        "no_write": "roi_ocrrequest_reference_no_write_boundary_report_v1.json",
        "sim": "roi_ocrrequest_reference_simulation_context_report_v1.json",
        "non_claims": "roi_ocrrequest_reference_non_claims_report_v1.json",
        "followups": "roi_ocrrequest_reference_open_followups_v1.json",
        "audit": "roi_ocrrequest_reference_audit_report_v1.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_ocrrequest_reference_verifier_report_v1.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    intake = data["intake"]
    schema = data["schema"]
    collection = data["collection"]
    excluded = data["excluded"]
    gate = data["gate"]
    payload = data["payload"]
    alignment = data["alignment"]
    future = data["future"]
    boundary = data["boundary"]
    source_chain = data["source_chain"]
    metrics = data["metrics"]
    audit = data["audit"]

    ok(s.get("reference_scope") == "ocrrequest_reference_only", "scope")
    ok(s.get("based_on_roi_crop_rerun") is True, "based_rerun")
    ok(s.get("generated_crop_count_observed") == 12, "crop_12")
    ok(s.get("ocrrequest_reference_generated") is True, "ref_generated")
    ok(s.get("ocrrequest_reference_count") == 12, "ref_count_12")
    ok(s.get("ocrrequest_submitted") is False, "no_submit")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")

    ok(intake.get("row_count") == 12, "intake_12")
    for row in intake.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("eligible_for_ocrrequest_reference") is True, "intake_eligible")
            ok(bool(row.get("crop_file_path")), "intake_path")
            break

    tmpl = schema.get("template") or {}
    ok(tmpl.get("submission_status") == "not_submitted", "schema_not_submitted")
    ok(schema.get("defaults", {}).get("ocr_invoked") is False, "schema_no_ocr")

    ok(collection.get("reference_count") == 12, "coll_12")
    for ref in collection.get("references") or []:
        if isinstance(ref, dict):
            ok(ref.get("submission_status") == "not_submitted", "ref_not_submitted")
            ok(ref.get("full_frame_ocr_allowed") is False, "no_full_frame")
            ok(ref.get("mock_text_allowed") is False, "no_mock")
            ok(ref.get("ocr_invoked") is False, "ref_no_ocr")
            ok(ref.get("provider_invoked") is False, "ref_no_provider")
            break

    ok(excluded.get("future_detector_deferred_count") == 8, "fd_8")
    ok(excluded.get("multiframe_deferred_count") == 7, "mf_7")

    ok(gate.get("row_count") == 12, "gate_12")
    for row in gate.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("gated_submission_required") is True, "gated")
            ok(row.get("direct_provider_bypass_allowed") is False, "no_bypass")
            break

    ok(payload.get("row_count") == 12, "payload_12")
    for row in payload.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("current_phase_submission_allowed") is False, "payload_no_submit")
            ok(row.get("current_phase_provider_invoked") is False, "payload_no_provider")
            break

    ok(alignment.get("all_one_to_one_mapping") is True, "one_to_one")
    ok(alignment.get("orphan_reference") is False, "no_orphan_ref")
    for row in alignment.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("one_to_one_mapping") is True, "row_one_to_one")
            break

    ok(source_chain.get("all_traceable_to_crop_artifact") is True, "trace_crop")
    for row in source_chain.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_better_frame_selection") is True, "trace_bf")
            break

    phases = [p.get("future_phase") for p in (future.get("phases") or []) if isinstance(p, dict)]
    ok("OCRRequest-Gated-Submission-from-ROI-v1" in phases, "future_phase")

    ok(boundary.get("ocrrequest_reference_only") is True, "boundary_only")
    ok(boundary.get("direct_provider_bypass") is False, "boundary_bypass")
    ok(boundary.get("evidence_pack_generated") is False, "boundary_ep")

    ok(metrics.get("ocrrequest_submitted_count") == 0, "metrics_submit")
    ok(metrics.get("provider_invoked_count") == 0, "metrics_provider")
    ok(metrics.get("orphan_reference_count") == 0, "orphan_ref")

    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_to_ocrrequest_reference_v1_executed") is True, "audit")
    ok(audit.get("direct_provider_bypass") is False, "audit_bypass")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_ocrrequest_reference_verifier_report_v1.json",
        {"schema_version": "roi_ocrrequest_reference_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
