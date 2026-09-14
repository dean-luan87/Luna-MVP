#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for ROI-to-OCRRequest Reference v2 BBoxExpansion."""

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
        "summary": "roi_to_ocrrequest_reference_v2_bbox_expansion_summary.json",
        "intake": "roi_ocrrequest_v2_expanded_crop_intake_matrix.json",
        "schema": "roi_ocrrequest_reference_v2_bbox_expansion_schema.json",
        "collection": "roi_ocrrequest_reference_v2_bbox_expansion_collection.json",
        "preservation": "roi_ocrrequest_v2_expansion_ref_preservation_report.json",
        "gate": "roi_ocrrequest_v2_gate_metadata_report.json",
        "payload": "roi_ocrrequest_v2_payload_candidate_matrix.json",
        "alignment": "roi_ocrrequest_reference_v2_alignment_report.json",
        "chain": "roi_ocrrequest_reference_v2_source_chain_report.json",
        "future": "roi_ocrrequest_v2_future_gated_submission_plan.json",
        "boundary": "roi_ocrrequest_reference_v2_boundary_report.json",
        "metrics": "roi_ocrrequest_reference_v2_metrics_candidate_report.json",
        "bench": "roi_ocrrequest_reference_v2_benchmark_link_report.json",
        "health": "roi_ocrrequest_reference_v2_system_health_link_report.json",
        "no_write": "roi_ocrrequest_reference_v2_no_write_boundary_report.json",
        "sim": "roi_ocrrequest_reference_v2_simulation_context_report.json",
        "non_claims": "roi_ocrrequest_reference_v2_non_claims_report.json",
        "followups": "roi_ocrrequest_reference_v2_open_followups.json",
        "audit": "roi_ocrrequest_reference_v2_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "roi_ocrrequest_reference_v2_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    audit = data["audit"]
    tmpl = (data["schema"].get("template") or {})

    ok(s.get("reference_scope") == "ocrrequest_reference_v2_bbox_expansion_only", "scope")
    ok(s.get("based_on_roi_crop_v2_bbox_expansion") is True, "based_v2")
    ok(s.get("expanded_crop_count_observed") == 4, "crop_4")
    ok(s.get("eligible_expanded_crop_count") == 4, "eligible_4")
    ok(s.get("ocrrequest_reference_v2_generated") is True, "ref_gen")
    ok(s.get("ocrrequest_submitted") is False, "no_submit")
    ok(s.get("ocr_invoked") is False, "no_ocr")
    ok(s.get("provider_invoked") is False, "no_provider")

    ok(data["intake"].get("row_count") == 4, "intake_4")
    ok(tmpl.get("image_source_type") == "expanded_roi_crop", "schema_img_type")
    ok(tmpl.get("submission_status") == "not_submitted", "schema_not_submitted")

    coll = data["collection"]
    ok(coll.get("reference_count") == 4, "ref_4")
    for ref in coll.get("references") or []:
        if isinstance(ref, dict):
            ok(ref.get("submission_status") == "not_submitted", "ref_not_submitted")
            ok(ref.get("full_frame_ocr_allowed") is False, "no_full_frame")
            ok(ref.get("mock_text_allowed") is False, "no_mock")
            ok(ref.get("source_bbox_expansion_candidate_id"), "has_exp_cand")
            ok(ref.get("source_expanded_crop_artifact_id"), "has_crop_art")
            ok(ref.get("source_bbox_xyxy") is not None, "has_src_bbox")
            ok(ref.get("expanded_bbox_xyxy") is not None, "has_exp_bbox")
            break

    pres = data["preservation"]
    ok(pres.get("expansion_candidate_ref_preserved") is True, "pres_exp_cand")
    ok(pres.get("expanded_crop_artifact_ref_preserved") is True, "pres_crop")
    ok(pres.get("source_bbox_preserved") is True, "pres_src_bbox")
    ok(pres.get("expanded_bbox_preserved") is True, "pres_exp_bbox")

    for row in data["gate"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("bbox_expansion_applied") is True, "gate_bbox_exp")
            ok(row.get("direct_provider_bypass_allowed") is False, "gate_no_bypass")
            break

    for row in data["payload"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("current_phase_submission_allowed") is False, "payload_no_submit")
            break

    align = data["alignment"]
    ok(align.get("one_to_one_mapping") is True, "one_to_one")
    ok(align.get("orphan_reference_count", 1) == 0, "no_orphan_ref")

    for row in data["chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_expanded_crop_artifact") is True, "chain_crop")
            ok(row.get("traceable_to_bbox_expansion_candidate") is True, "chain_exp")
            break

    ok(data["future"].get("future_phase") == "OCRRequest-Gated-Submission-from-ROI-v2-BBoxExpansion", "future_phase")
    ok(data["boundary"].get("ocrrequest_submitted") is False, "boundary_submit")
    ok(data["boundary"].get("direct_provider_bypass") is False, "boundary_bypass")
    ok(data["metrics"].get("ocrrequest_submitted_count") == 0, "metrics_submit")
    ok(data["metrics"].get("provider_invoked_count") == 0, "metrics_provider")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("roi_to_ocrrequest_reference_v2_bbox_expansion_executed") is True, "audit")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "roi_ocrrequest_reference_v2_verifier_report.json",
        {"schema_version": "roi_ocrrequest_reference_v2_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
