#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default="")
    ap.add_argument(
        "--vision-consumer-root",
        required=True,
        help="Absolute path to vision_recognition_evidence_readonly_consumer smoke output.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path to write midplatform ingest artifacts.")
    args = ap.parse_args()

    cons = _require_abs(args.vision_consumer_root, "--vision-consumer-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_recognition_evidence_readonly_consumer_view.json",
        "vision_recognition_evidence_by_frame_matrix.json",
        "vision_recognition_evidence_by_roi_matrix.json",
        "vision_recognition_evidence_geometry_summary.json",
        "vision_recognition_evidence_readonly_consumer_audit_report.json",
        "vision_recognition_evidence_readonly_consumer_summary.json",
    ):
        p = cons / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing consumer input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.midplatform.vision_recognition_evidence_readonly_ingest_candidate_v0 import (
        build_midplatform_vision_recognition_ingest_summary_v0,
        run_midplatform_vision_recognition_readonly_ingest_candidate_bundle_v0,
    )

    bundle = run_midplatform_vision_recognition_readonly_ingest_candidate_bundle_v0(cons)

    cand_path = out / "midplatform_vision_recognition_ingest_candidate.json"
    _write_json(cand_path, bundle["candidate"])
    _write_json(out / "midplatform_vision_recognition_ingest_matrix.json", bundle["ingest_matrix"])
    _write_json(out / "midplatform_vision_recognition_ingest_source_chain_summary.json", bundle["source_chain_summary"])
    _write_json(out / "midplatform_vision_recognition_ingest_audit_report.json", bundle["audit"])

    summary = build_midplatform_vision_recognition_ingest_summary_v0(
        input_consumer_root=str(cons),
        candidate=bundle["candidate"],
        validation_errors=bundle["validation_errors"],
        ingest_candidate_path=str(cand_path.resolve()),
    )
    _write_json(out / "midplatform_vision_recognition_ingest_candidate_summary.json", summary)

    if bundle["validation_errors"]:
        _write_json(
            out / "midplatform_vision_recognition_ingest_validation_errors.json",
            {"errors": bundle["validation_errors"]},
        )

    (out / "midplatform_vision_recognition_ingest_notes.md").write_text(
        "# Phase-MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001\n\n"
        "Builds **`midplatform_vision_recognition_ingest_candidate_v0`** from Vision read-only consumer outputs. "
        "**Read-only candidate** — no MidPlatform fact, no Scene Delta, no WorldModel, no AI interpretation, "
        "no navigation, no real vision / YOLO / Supervision mainline / VLM / OCR.\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "midplatform_vision_recognition_ingest_smoke_root": str(out),
                "input_vision_consumer_root": str(cons),
                "ingest_candidate": str(cand_path.resolve()),
                "status": "success" if not bundle["validation_errors"] else "validation_failed",
            },
            ensure_ascii=False,
        )
    )
    return 0 if not bundle["validation_errors"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
