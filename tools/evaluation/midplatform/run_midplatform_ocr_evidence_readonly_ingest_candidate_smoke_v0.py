#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001 — build ingest candidate from OCR consumer outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    ap.add_argument(
        "--consumer-root",
        default="",
        help="Absolute path to ocr_evidence_readonly_consumer_smoke_v0 directory",
    )
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    default_root = Path(
        "/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_evidence_readonly_consumer_smoke_v0"
    )
    cr = Path(args.consumer_root).expanduser() if args.consumer_root.strip() else default_root
    if not cr.is_absolute():
        cr = (WS_ROOT / cr).resolve()
    consumer_root = _require_abs(str(cr), "--consumer-root (resolved)")

    view_p = consumer_root / "ocr_evidence_readonly_consumer_view.json"
    roi_p = consumer_root / "ocr_evidence_by_roi_matrix.json"
    geom_p = consumer_root / "ocr_evidence_geometry_matrix.json"
    chain_p = consumer_root / "ocr_evidence_source_chain_summary.json"

    for label, p in (
        ("consumer_view", view_p),
        ("by_roi_matrix", roi_p),
        ("geometry_matrix", geom_p),
        ("source_chain_summary", chain_p),
    ):
        if not p.is_file():
            raise SystemExit(f"ERROR: missing input {label}: {p}")

    view = _read_json(view_p)
    evidence_by_roi = _read_json(roi_p)
    geometry_matrix = _read_json(geom_p)
    source_chain_summary = _read_json(chain_p)

    provider_summary = view.get("provider_summary")
    if not isinstance(provider_summary, dict):
        provider_summary = {}

    from capabilities.midplatform.ocr_evidence_readonly_ingest_candidate_v0 import (
        build_ingest_summary_v0,
        build_midplatform_ocr_evidence_ingest_audit_v0,
        build_midplatform_ocr_evidence_ingest_candidate_v0,
        build_text_matrix_from_evidence_by_roi_v0,
    )

    candidate, val_errs = build_midplatform_ocr_evidence_ingest_candidate_v0(
        consumer_view=view if isinstance(view, dict) else {},
        evidence_by_roi=evidence_by_roi if isinstance(evidence_by_roi, dict) else {},
        geometry_matrix=geometry_matrix if isinstance(geometry_matrix, list) else [],
        source_chain_summary=source_chain_summary if isinstance(source_chain_summary, dict) else {},
        provider_summary=provider_summary,
        source_consumer_view_ref=str(view_p),
    )

    audit = build_midplatform_ocr_evidence_ingest_audit_v0()
    text_matrix = build_text_matrix_from_evidence_by_roi_v0(
        evidence_by_roi if isinstance(evidence_by_roi, dict) else {}
    )

    input_paths = {
        "ocr_evidence_readonly_consumer_view.json": str(view_p),
        "ocr_evidence_by_roi_matrix.json": str(roi_p),
        "ocr_evidence_geometry_matrix.json": str(geom_p),
        "ocr_evidence_source_chain_summary.json": str(chain_p),
    }

    summary = build_ingest_summary_v0(
        input_consumer_root=str(consumer_root),
        candidate=candidate,
        validation_errors=val_errs,
        input_paths=input_paths,
    )

    cand_path = out / "midplatform_ocr_evidence_ingest_candidate.json"
    _write_json(cand_path, candidate)
    summary["ingest_candidate_path"] = str(cand_path.resolve())
    _write_json(out / "midplatform_ocr_evidence_ingest_candidate_summary.json", summary)
    _write_json(out / "midplatform_ocr_evidence_ingest_text_matrix.json", text_matrix)
    _write_json(out / "midplatform_ocr_evidence_ingest_geometry_matrix.json", geometry_matrix)
    _write_json(out / "midplatform_ocr_evidence_ingest_source_chain_summary.json", source_chain_summary)
    _write_json(out / "midplatform_ocr_evidence_ingest_audit_report.json", audit)

    (out / "midplatform_ocr_evidence_ingest_notes.md").write_text(
        "# Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001\n\n"
        "Builds **`midplatform_ocr_evidence_ingest_candidate_v0`** from OCR read-only consumer outputs. "
        "**Read-only candidate only** — no MidPlatform fact write, no Scene Delta, no WorldModel, "
        "no AI interpretation, no OCR provider invocation.\n",
        encoding="utf-8",
    )

    if val_errs:
        _write_json(out / "midplatform_ocr_evidence_ingest_validation_errors.json", {"errors": val_errs})

    print(
        json.dumps(
            {
                "midplatform_ocr_evidence_readonly_ingest_smoke_root": str(out),
                "input_consumer_root": str(consumer_root),
                "ingest_candidate": str(cand_path.resolve()),
                "status": "success" if not val_errs else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not val_errs else 3


if __name__ == "__main__":
    raise SystemExit(main())
