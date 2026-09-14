#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Evidence Pack Adapter v2 ROIRef."""

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
        "summary": "evidence_pack_adapter_v2_roiref_summary.json",
        "intake": "evidence_pack_v2_roi_result_intake_matrix.json",
        "schema": "evidence_pack_v2_roiref_schema.json",
        "collection": "evidence_pack_v2_roiref_collection.json",
        "alignment": "evidence_pack_v2_roiref_alignment_matrix.json",
        "text_pres": "evidence_pack_v2_text_item_preservation_report.json",
        "risk": "evidence_pack_v2_raw_text_risk_report.json",
        "coord": "evidence_pack_v2_coordinate_attachment_report.json",
        "provider": "evidence_pack_v2_provider_metadata_report.json",
        "chain": "evidence_pack_v2_source_chain_report.json",
        "readiness": "evidence_pack_v2_semantic_readiness_report.json",
        "boundary": "evidence_pack_v2_boundary_report.json",
        "metrics": "evidence_pack_v2_metrics_candidate_report.json",
        "bench": "evidence_pack_v2_benchmark_link_report.json",
        "health": "evidence_pack_v2_system_health_link_report.json",
        "no_write": "evidence_pack_v2_no_write_boundary_report.json",
        "sim": "evidence_pack_v2_simulation_context_report.json",
        "non_claims": "evidence_pack_v2_non_claims_report.json",
        "followups": "evidence_pack_v2_open_followups.json",
        "audit": "evidence_pack_v2_audit_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "evidence_pack_v2_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    collection = data["collection"]
    alignment = data["alignment"]
    risk = data["risk"]
    coord = data["coord"]
    audit = data["audit"]

    ok(s.get("adapter_scope") == "roi_ocr_result_to_evidence_pack_v2_only", "scope")
    ok(s.get("based_on_roi_ocr_gated_submission") is True, "based")
    ok(s.get("roi_ocr_result_count_observed") == 12, "result_12")
    ok(s.get("evidence_pack_v2_generated") is True, "ep_gen")
    ok(s.get("evidence_pack_v2_count") == 12, "ep_12")
    ok(s.get("raw_ocr_text_preserved") is True, "raw_preserved")
    ok(s.get("text_items_preserved") is True, "items_preserved")
    ok(s.get("ocrrequest_ref_preserved") is True, "ref_preserved")
    ok(s.get("crop_ref_preserved") is True, "crop_preserved")
    ok(s.get("semantic_candidate_generated") is False, "no_semantic")

    ok(data["intake"].get("row_count") == 12, "intake_12")
    tmpl = data["schema"].get("template") or {}
    ok(tmpl.get("evidence_tier") == "roi_ocr_primary", "tier")

    ok(collection.get("pack_count") == 12, "pack_12")
    for pack in collection.get("packs") or []:
        if isinstance(pack, dict):
            ok(pack.get("fact_status") == "not_fact", "pack_not_fact")
            ok(pack.get("write_allowed") is False, "pack_no_write")
            ok(pack.get("raw_ocr", {}).get("raw_ocr_text_preserved") is True, "pack_raw_preserved")
            rf = pack.get("risk_flags") or {}
            ok(rf.get("non_empty_text_not_accuracy") is True, "risk_not_accuracy")
            break

    ok(alignment.get("all_one_to_one_mapping") is True, "one_to_one")
    ok(alignment.get("orphan_pack") is False, "no_orphan")

    for row in data["text_pres"].get("rows") or []:
        if isinstance(row, dict) and row.get("text_item_count", 0) > 0:
            ok(row.get("text_items_have_bbox") is True, "has_bbox")
            ok(row.get("text_items_have_confidence") is True, "has_conf")
            break

    ok(risk.get("non_empty_text_not_accuracy") is True, "risk_global")
    ok(risk.get("global_repeated_same_text_detected") is True, "repeated_detected")
    repeated_rows = sum(1 for r in (risk.get("rows") or []) if (r.get("risk_flags") or {}).get("repeated_same_text"))
    low_rows = sum(1 for r in (risk.get("rows") or []) if (r.get("risk_flags") or {}).get("low_information_text"))
    ok(repeated_rows >= 1, "repeated_rows")
    ok(low_rows >= 1, "low_info_rows")

    for row in coord.get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("coordinate_fabrication_detected") is False, "no_fabrication")
            ok(row.get("gps_lat") is None, "gps_lat")
            ok(row.get("gps_lng") is None, "gps_lng")
            break

    ok(data["provider"].get("rows"), "provider_rows")
    for row in data["provider"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("provider_comparison_claimed") is False, "no_comparison")
            break

    ok(data["chain"].get("all_traceable_to_roi_ocr_result") is True, "trace_ocr")
    for row in data["chain"].get("rows") or []:
        if isinstance(row, dict):
            ok(row.get("traceable_to_ocrrequest_reference") is True, "trace_ref")
            ok(row.get("traceable_to_crop_artifact") is True, "trace_crop")
            break

    ok(data["readiness"].get("semantic_candidate_generated_now") is False, "sem_now_false")
    ok(data["boundary"].get("ocr_invoked") is False, "boundary_no_ocr")
    ok(data["boundary"].get("provider_invoked") is False, "boundary_no_provider")
    ok(data["metrics"].get("fact_write_allowed_count") == 0, "metrics_fact")
    ok(data["bench"].get("benchmark_score_generated") is False, "bench")
    ok(data["health"].get("provider_health_runtime_checked") is False, "health")
    ok(data["no_write"].get("boundary_ok") is True, "boundary_ok")
    ok(data["sim"].get("simulation_profile_id") == "developer_full", "sim")
    ok(audit.get("evidence_pack_adapter_v2_roiref_executed") is True, "audit")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "evidence_pack_v2_verifier_report.json",
        {"schema_version": "evidence_pack_v2_verifier_report_v1", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
