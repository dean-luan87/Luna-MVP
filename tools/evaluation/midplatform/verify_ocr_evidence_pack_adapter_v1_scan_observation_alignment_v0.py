#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR Evidence Pack Adapter v1 Scan Observation Alignment."""

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
        "summary": "ocr_evidence_pack_adapter_v1_scan_observation_alignment_summary.json",
        "schema_delta": "ocr_evidence_pack_v1_schema_delta_v0.json",
        "gated": "ocr_evidence_pack_v1_gated_collection.json",
        "scan_sidecar": "ocr_evidence_pack_v1_scan_observation_sidecar_collection.json",
        "hierarchy": "ocr_scan_vs_gated_evidence_hierarchy_report.json",
        "coverage": "ocr_evidence_pack_v1_field_coverage_report.json",
        "semantic": "ocr_semantic_candidate_v1_readiness_report.json",
        "boundary": "ocr_evidence_pack_adapter_v1_no_write_boundary_report.json",
        "audit": "ocr_evidence_pack_adapter_v1_audit_report.json",
        "non_claims": "ocr_evidence_pack_adapter_v1_non_claims_report.json",
    }
    data = {}
    for k, f in files.items():
        p = root / f
        if not p.is_file():
            blockers.append(f"missing:{k}")
        else:
            data[k] = _read_json(p)

    if blockers:
        _write_json(root / "ocr_evidence_pack_adapter_v1_verifier_report.json", {"verdict": "NO_GO", "blockers": blockers})
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    s = data["summary"]
    delta = data["schema_delta"]
    gated = data["gated"]
    scan = data["scan_sidecar"]
    hier = data["hierarchy"]
    cov = data["coverage"]
    sem = data["semantic"]
    boundary = data["boundary"]
    audit = data["audit"]

    ok(s.get("adapter_scope") == "evidence_pack_v1_from_mixed_batch_v2_gated_only", "scope")
    ok(s.get("pack_schema_upgraded_to") == "ocr_text_evidence_pack_v1", "schema_v1")
    ok(s.get("scan_observation_not_primary_evidence") is True, "scan_not_primary")
    ok(s.get("ocr_invoked") is False, "ocr_invoked_false")
    ok("scan_observation_ref" in (delta.get("new_top_level_fields") or []), "delta_scan_ref")
    ok("gated_path_ref" in (delta.get("new_top_level_fields") or []), "delta_gated_ref")
    ok("source_quality_grade" in (delta.get("new_top_level_fields") or []), "delta_sq")
    ok("readability_gate_ref" in (delta.get("new_top_level_fields") or []), "delta_read")

    packs = gated.get("packs") or []
    ok(gated.get("every_pack_has_ocr_request_ref") is True, "collection_flag")
    for p in packs:
        if not isinstance(p, dict):
            continue
        ok(p.get("schema_version") == "ocr_text_evidence_pack_v1", "pack_schema_v1")
        ok((p.get("ocr_request_ref") or {}).get("request_id"), "pack_ocr_request_ref")
        ok(p.get("source_quality_grade"), "pack_sq")
        ok(p.get("readability_gate_ref"), "pack_read_ref")
        ok(p.get("gated_path_ref"), "pack_gated_ref")
        ok(p.get("evidence_tier") == "gated_ocr_primary", "pack_tier")
        ok((p.get("governance") or {}).get("scan_observation_not_primary_evidence") is True, "gov_scan_not_primary")

    for sc in scan.get("scan_observations") or []:
        if isinstance(sc, dict):
            ok(sc.get("evidence_tier") == "scan_observation_only", "sidecar_tier")
            ok(sc.get("ocr_request_ref") is None, "sidecar_no_ocr_request")
            ok((sc.get("governance") or {}).get("is_ocr_text_evidence_pack") is False, "sidecar_not_pack")

    ok(hier.get("full_frame_scan_not_primary_evidence") is True, "hier_ff")
    ok(cov.get("all_gated_have_ocr_request_ref") is True, "cov_all_ref")
    ok(sem.get("ready_for_semantic_candidate_v1") is True, "sem_ready")
    ok("scan_saw_but_not_ocr" in str(sem.get("distinction_matrix", {})), "sem_distinction")
    ok(boundary.get("boundary_ok") is True, "boundary")
    ok(audit.get("ocr_invoked") is False, "audit_ocr")
    ok(audit.get("world_model_attach_executed") is False, "audit_wm")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_evidence_pack_adapter_v1_verifier_report.json",
        {"schema_version": "ocr_evidence_pack_adapter_v1_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
