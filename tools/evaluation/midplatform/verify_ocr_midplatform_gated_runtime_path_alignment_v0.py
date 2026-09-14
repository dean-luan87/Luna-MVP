#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR MidPlatform Gated Runtime Path Alignment v0."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    checks = 0

    def ok(cond: bool, name: str) -> None:
        nonlocal checks
        if cond:
            checks += 1
        else:
            blockers.append(name)

    paths = {
        "summary": root / "ocr_midplatform_gated_runtime_path_summary.json",
        "input": root / "ocr_input_candidate_matrix.json",
        "sq": root / "ocr_source_quality_gate_decision_matrix.json",
        "read": root / "ocr_readability_gate_decision_matrix.json",
        "roi": root / "ocr_roi_crop_or_scan_observation_matrix.json",
        "req": root / "ocr_request_candidate_matrix.json",
        "trace": root / "ocr_request_gated_submission_trace.json",
        "bypass": root / "ocr_direct_provider_bypass_detection_report.json",
        "ff": root / "ocr_full_frame_scan_observation_boundary_report.json",
        "pack_align": root / "ocr_evidence_pack_request_ref_alignment_report.json",
        "sem_align": root / "ocr_semantic_candidate_request_ref_alignment_report.json",
        "boundary": root / "ocr_midplatform_gated_runtime_path_no_write_boundary_report.json",
        "audit": root / "ocr_midplatform_gated_runtime_path_audit_report.json",
        "packs": root / "ocr_midplatform_gated_evidence_pack_collection.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        _write_json(
            root / "ocr_midplatform_gated_runtime_path_verifier_report.json",
            {"verdict": "NO_GO", "blockers": blockers, "checks_passed": 0},
        )
        print(json.dumps({"verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    bypass = _read_json(paths["bypass"])
    ff = _read_json(paths["ff"])
    pack_align = _read_json(paths["pack_align"])
    sem_align = _read_json(paths["sem_align"])
    boundary = _read_json(paths["boundary"])
    audit = _read_json(paths["audit"])
    sq = _read_json(paths["sq"])
    read_m = _read_json(paths["read"])
    req = _read_json(paths["req"])
    trace = _read_json(paths["trace"])
    packs_doc = _read_json(paths["packs"])

    ok(bypass.get("direct_provider_bypass") is False, "direct_bypass_false")
    ok(bypass.get("every_provider_call_has_ocr_request_ref") is True, "provider_ref")
    ok(summary.get("direct_provider_bypass") is False, "summary_bypass_false")
    ok(summary.get("source_quality_gate_executed_before_ocr_request") is True, "sq_before_req")
    ok(summary.get("readability_gate_executed_before_ocr_request") is True, "read_before_req")
    ok(ff.get("full_frame_scan_not_primary_evidence") is True, "ff_not_primary")
    ok(pack_align.get("every_evidence_pack_has_ocr_request_ref") is True, "pack_ref")
    ok(pack_align.get("full_frame_primary_evidence_count", 1) == 0, "no_ff_primary_pack")
    ok(summary.get("sq_e_submitted_to_ocr") is False, "sq_e_not_submitted")

    sq_rows = sq.get("rows") or []
    ok(any(r.get("source_quality_grade") == "SQ_D" for r in sq_rows if isinstance(r, dict)), "sq_d_present")
    ok(len(sq_rows) >= 5, "sq_rows")

    read_rows = read_m.get("rows") or []
    ok(all(r.get("readability_gate_executed") for r in read_rows if isinstance(r, dict)), "read_executed")

    req_rows = req.get("rows") or []
    ok(all(isinstance(r, dict) and r.get("source_quality_grade") for r in req_rows), "req_sq_grade")
    ok(all(isinstance(r, dict) and r.get("readability_grade") for r in req_rows), "req_read_grade")
    ok(all(isinstance(r, dict) and r.get("governance_route") for r in req_rows), "req_route")

    trace_rows = trace.get("rows") or []
    ok(
        all(t.get("direct_provider_bypass") is False for t in trace_rows if isinstance(t, dict) and t.get("bridge_invoked")),
        "trace_no_bypass",
    )
    ok(
        all(t.get("ocr_request_ref") for t in trace_rows if isinstance(t, dict) and t.get("bridge_invoked")),
        "trace_request_ref",
    )

    for p in packs_doc.get("packs") or []:
        if not isinstance(p, dict):
            continue
        ref = (p.get("source") or {}).get("ocr_request_ref")
        ok(ref is not None and ref.get("request_id"), "pack_has_request_id")
        ok((p.get("governance") or {}).get("full_frame_scan_primary") is False, "pack_not_ff_primary")

    ok(boundary.get("boundary_ok") is True, "boundary_ok")
    ok(boundary.get("violations") == [], "violations")
    ok(audit.get("world_model_write_executed") is False, "audit_wm")
    ok(audit.get("midplatform_fact_written") is False, "audit_fact")
    ok(audit.get("scene_delta_candidate_generated") is False, "audit_sd")
    ok(audit.get("navigation_decision_invoked") is False, "audit_nav")
    ok(audit.get("runtime_routing_changed") is False, "audit_routing")

    verdict = "GO" if not blockers else "NO_GO"
    _write_json(
        root / "ocr_midplatform_gated_runtime_path_verifier_report.json",
        {"schema_version": "ocr_midplatform_gated_runtime_path_verifier_report_v0", "verdict": verdict, "blockers": blockers, "checks_passed": checks},
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers, "checks_passed": checks}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
