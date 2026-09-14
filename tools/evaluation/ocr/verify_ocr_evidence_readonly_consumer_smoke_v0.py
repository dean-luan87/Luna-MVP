#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR evidence read-only consumer smoke (Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

WS_ROOT = Path(__file__).resolve().parents[3]


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


def _has_original_geometry(row: Dict[str, Any]) -> bool:
    ob = row.get("original_bbox")
    if isinstance(ob, list) and len(ob) == 4:
        return True
    op = row.get("original_polygon")
    return isinstance(op, list) and len(op) > 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    sum_p = root / "ocr_evidence_readonly_consumer_summary.json"
    view_p = root / "ocr_evidence_readonly_consumer_view.json"
    roi_p = root / "ocr_evidence_by_roi_matrix.json"
    geom_p = root / "ocr_evidence_geometry_matrix.json"
    chain_p = root / "ocr_evidence_source_chain_summary.json"
    aud_p = root / "ocr_evidence_readonly_consumer_audit_report.json"

    for name, p in (
        ("summary", sum_p),
        ("consumer_view", view_p),
        ("by_roi", roi_p),
        ("geometry", geom_p),
        ("chain", chain_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "ocr_evidence_readonly_consumer_verifier_report_v0",
            "phase": "Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
        }
        _write_json(root / "ocr_evidence_readonly_consumer_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(sum_p)
    view = _read_json(view_p)
    aud = _read_json(aud_p)
    by_roi = _read_json(roi_p)

    bp_path = str(summary.get("input_bridge_pack_path") or "")
    if not bp_path or not Path(bp_path).is_file():
        blockers.append("summary_must_record_existing_input_bridge_pack_path")

    elig_count = int(view.get("evidence_count") or 0)
    if elig_count < 2:
        blockers.append("eligible_text_evidence_count_must_be_at_least_2")

    joined = str(view.get("text_joined") or "").strip()
    if not joined:
        blockers.append("consumer_view_text_joined_must_be_non_empty")

    if not isinstance(by_roi, dict) or not by_roi:
        blockers.append("evidence_by_roi_must_be_non_empty")

    for k in (
        "midplatform_written",
        "scene_delta_written",
        "world_model_written",
        "ai_interpretation_invoked",
        "paddleocr_invoked",
        "ocr_routing_changed",
    ):
        if aud.get(k) is not False:
            blockers.append(f"audit_forbidden_or_missing_false:{k}")

    elig_rows = []
    for _rid, rows in (by_roi.items() if isinstance(by_roi, dict) else []):
        if isinstance(rows, list):
            elig_rows.extend([r for r in rows if isinstance(r, dict)])

    if not elig_rows and elig_count >= 2:
        blockers.append("evidence_by_roi_rows_missing")

    for i, it in enumerate(elig_rows):
        if not str(it.get("text") or "").strip():
            blockers.append(f"evidence_missing_text_at_{i}")
        if not str(it.get("roi_id") or "").strip() and not str(it.get("unit_id") or "").strip():
            blockers.append(f"evidence_missing_roi_or_unit_id_at_{i}")
        ref = str(it.get("source_unit_ref") or "")
        if not ref.startswith("/"):
            blockers.append(f"evidence_missing_source_unit_ref_at_{i}")
        if not _has_original_geometry(it):
            blockers.append(f"evidence_missing_original_geometry_at_{i}")

    prov = view.get("provider_summary") if isinstance(view.get("provider_summary"), dict) else {}
    if not prov:
        blockers.append("provider_summary_missing")

    chs = view.get("source_reference_chain_summary") if isinstance(view.get("source_reference_chain_summary"), dict) else {}
    if "chain_item_count" not in chs:
        blockers.append("source_reference_chain_summary_incomplete")

    soft: List[str] = []
    if not blockers:
        verdict = "GO"
        if summary.get("validation_ok") is False:
            verdict = "NO_GO"
            blockers.append("bridge_pack_schema_validation_failed")
        if chs.get("chain_item_count") == 0:
            verdict = "CONDITIONAL_GO"
            soft.append("source_chain_empty_optional_input")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "ocr_evidence_readonly_consumer_verifier_report_v0",
        "phase": "Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "input_bridge_pack_path": bp_path,
        "evidence_count": elig_count,
        "text_joined_non_empty": bool(joined),
    }
    _write_json(root / "ocr_evidence_readonly_consumer_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
