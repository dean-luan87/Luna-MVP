#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001 — read-only aggregation."""

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
        "--evidence-pack-root",
        required=True,
        help="Absolute path to vision_recognition_evidence_pack_stub smoke output root.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path to write consumer artifacts.")
    args = ap.parse_args()

    ev_root = _require_abs(args.evidence_pack_root, "--evidence-pack-root")
    out = _require_abs(args.output_root, "--output-root")

    for name in (
        "vision_recognition_evidence_pack.json",
        "vision_recognition_evidence_matrix.json",
        "vision_recognition_provider_summary.json",
        "vision_recognition_evidence_audit_report.json",
    ):
        p = ev_root / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing evidence pack input: {p}")

    if args.repo_root.strip():
        repo = _require_abs(args.repo_root, "--repo-root")
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))

    from capabilities.vision_runtime.vision_recognition_evidence_readonly_consumer_v0 import (
        run_vision_recognition_evidence_readonly_consumer_v0,
    )

    bundle = run_vision_recognition_evidence_readonly_consumer_v0(ev_root)

    _write_json(out / "vision_recognition_evidence_readonly_consumer_summary.json", bundle["summary"])
    _write_json(out / "vision_recognition_evidence_readonly_consumer_view.json", bundle["consumer_view"])
    _write_json(out / "vision_recognition_evidence_by_frame_matrix.json", bundle["by_frame_matrix"])
    _write_json(out / "vision_recognition_evidence_by_roi_matrix.json", bundle["by_roi_matrix"])
    _write_json(out / "vision_recognition_evidence_geometry_summary.json", bundle["geometry_summary"])
    _write_json(out / "vision_recognition_evidence_readonly_consumer_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-Recognition-Evidence-ReadOnly-Consumer-001\n\n"
        "Read-only traversal of **`vision_recognition_evidence_pack_v0`** into a **consumer_view** "
        "with frame / ROI-type aggregations. **No** MidPlatform fact, Scene Delta, WorldModel, "
        "AI interpretation, navigation, YOLO, Supervision mainline, VLM, OCR, or confirmed facts.\n"
    )
    (out / "vision_recognition_evidence_readonly_consumer_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_recognition_evidence_readonly_consumer_root": str(out),
                "evidence_pack_root": str(ev_root),
                "evidence_count_observed": bundle["summary"].get("evidence_count_observed"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
