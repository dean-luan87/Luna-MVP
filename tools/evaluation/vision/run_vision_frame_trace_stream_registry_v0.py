#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-FrameTrace-StreamRegistry-001 — stream registry + frame trace from ingest artifacts (read-only)."""

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
    ap.add_argument("--repo-root", default="", help="Repository root (absolute); optional.")
    ap.add_argument(
        "--video-ingest-root",
        required=True,
        help="Absolute path to video_frame_minimal_ingest_smoke output root.",
    )
    ap.add_argument("--output-root", required=True, help="Absolute path for this phase artifacts.")
    args = ap.parse_args()

    ingest = _require_abs(args.video_ingest_root, "--video-ingest-root")
    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    repo = _require_abs(args.repo_root, "--repo-root") if args.repo_root.strip() else WS_ROOT
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))

    for name in (
        "video_frame_ingest_summary.json",
        "video_frame_sampling_report.json",
        "video_frame_envelopes.jsonl",
        "video_frame_matrix.json",
        "video_frame_audit_report.json",
    ):
        p = ingest / name
        if not p.is_file():
            raise SystemExit(f"ERROR: missing ingest artifact: {p}")

    from capabilities.vision_runtime.vision_frame_trace_v0 import run_vision_frame_trace_stream_registry_from_ingest_v0

    bundle = run_vision_frame_trace_stream_registry_from_ingest_v0(ingest, out)

    _write_json(out / "vision_frame_trace_stream_registry_summary.json", bundle["summary"])
    _write_json(out / "vision_stream_registry.json", bundle["registry"])
    _write_json(out / "vision_frame_lineage_matrix.json", bundle["lineage"])
    _write_json(out / "vision_sampling_consistency_report.json", bundle["consistency"])
    _write_json(out / "vision_frame_trace_audit_report.json", bundle["audit"])

    notes = (
        "# Phase-Vision-FrameTrace-StreamRegistry-001\n\n"
        "Read-only **stream registry** + **frame trace** (JSONL) + **lineage matrix** + **sampling consistency** "
        "from `Vision-VideoFrame-Minimal-Ingest-001` outputs. **No** YOLO/OCR/VLM/camera/MidPlatform fact/"
        "Scene Delta/WorldModel/AI/navigation.\n\n"
        "**Not** a vision recognition pre-stage — **only** standard frame trajectory registration. "
        "Before any recognition provider: **Vision-Frame-Input-Governance-001** then "
        "**Vision-Frame-ROI-Proposal-And-Segmentation-Stub-001** (see "
        "`docs/architecture/vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md`).\n"
    )
    (out / "vision_frame_trace_stream_registry_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "vision_frame_trace_stream_registry_root": str(out),
                "video_ingest_root": str(ingest),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
