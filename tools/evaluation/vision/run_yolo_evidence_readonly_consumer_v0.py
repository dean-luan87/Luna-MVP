#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001 — consume YOLO evidence pack."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    candidates: list[Path] = []
    for parent in here.parents:
        if (parent / "capabilities" / "vision_runtime").is_dir():
            candidates.append(parent)
    for parent in candidates:
        if (parent / "_eval_out").is_dir():
            return parent
        sibling = parent.parent / "Luna-Workspace-Min"
        if (sibling / "_eval_out").is_dir():
            return sibling
    return candidates[0] if candidates else here.parents[3]


WS_ROOT = _find_ws_root()
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
    ap.add_argument("--yolo-evidence-pack-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    pack_root = _require_abs(args.yolo_evidence_pack_root, "--yolo-evidence-pack-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    for name in (
        "yolo_vision_recognition_evidence_pack.json",
        "yolo_vision_recognition_evidence_matrix.json",
        "yolo_provider_summary.json",
        "yolo_evidence_pack_audit_report.json",
    ):
        p = pack_root / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing YOLO pack input: {p}")

    from capabilities.vision_runtime.yolo_evidence_readonly_consumer_v0 import run_yolo_evidence_readonly_consumer_v0

    bundle = run_yolo_evidence_readonly_consumer_v0(pack_root)

    _write_json(out / "yolo_evidence_readonly_consumer_summary.json", bundle["summary"])
    _write_json(out / "yolo_evidence_readonly_consumer_view.json", bundle["consumer_view"])
    _write_json(out / "yolo_evidence_by_frame_matrix.json", bundle["by_frame_matrix"])
    _write_json(out / "yolo_evidence_by_roi_matrix.json", bundle["by_roi_matrix"])
    _write_json(out / "yolo_evidence_geometry_summary.json", bundle["geometry_summary"])
    _write_json(out / "yolo_evidence_readonly_consumer_audit_report.json", bundle["audit"])

    (out / "yolo_evidence_readonly_consumer_notes.md").write_text(
        "# Phase-Vision-YOLO-Evidence-Pack-ReadOnly-Consumer-001\n\n"
        "Read-only consumer over **YOLO** `vision_recognition_evidence_pack_v0`. "
        "No writes, no facts, no navigation.\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "yolo_evidence_readonly_consumer_root": str(out),
                "yolo_evidence_pack_root": str(pack_root),
                "evidence_count_observed": bundle["summary"].get("evidence_count_observed"),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
