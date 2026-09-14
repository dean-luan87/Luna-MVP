#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-Vision-VideoFrame-Minimal-Ingest-001 — offline video frame ingest smoke (no YOLO/OCR/VLM/camera)."""

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
    ap.add_argument("--repo-root", default="", help="Repository root (absolute); defaults to runner-derived repo root.")
    ap.add_argument("--video", default="", help="Absolute path to input MP4 (offline file).")
    ap.add_argument("--generate-test-video", action="store_true", help="Generate a short synthetic MP4 under output_root.")
    ap.add_argument("--max-frames", type=int, default=10)
    ap.add_argument("--sample-stride", type=int, default=1)
    ap.add_argument("--max-width", type=int, default=1280)
    ap.add_argument("--max-height", type=int, default=720)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out = _require_abs(args.output_root, "--output-root")
    out.mkdir(parents=True, exist_ok=True)

    repo = _require_abs(args.repo_root, "--repo-root") if args.repo_root.strip() else WS_ROOT
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))

    gen = bool(args.generate_test_video)
    vin = args.video.strip()
    if gen == (bool(vin)):
        raise SystemExit("ERROR: specify exactly one of --generate-test-video OR --video /ABS/PATH.mp4")

    from capabilities.vision_runtime.video_frame_ingest_v0 import generate_test_video_mp4_v0, ingest_video_frames_offline_v0
    from capabilities.vision_runtime.video_frame_sampling_policy_v0 import VideoFrameSamplingParamsV0

    params = VideoFrameSamplingParamsV0(
        max_frames=max(1, int(args.max_frames)),
        sample_stride=max(1, int(args.sample_stride)),
        max_width=max(1, int(args.max_width)),
        max_height=max(1, int(args.max_height)),
        decode_mode="offline_file",
        realtime_claim=False,
    )

    generated_meta: dict | None = None
    if gen:
        gdir = out / "generated"
        gdir.mkdir(parents=True, exist_ok=True)
        vpath = gdir / "video_frame_minimal_ingest_test.mp4"
        generated_meta = generate_test_video_mp4_v0(vpath, width=640, height=480, fps=10.0, duration_sec=3.0)
        video_path = Path(generated_meta["path"])
        input_mode = "generate_test_video"
    else:
        video_path = _require_abs(vin, "--video")
        input_mode = "offline_video_file"

    result = ingest_video_frames_offline_v0(video_path, out, params)
    summary = dict(result["summary"])
    summary["input_mode"] = input_mode
    if generated_meta is not None:
        summary["generated_test_video"] = generated_meta

    _write_json(out / "video_frame_ingest_summary.json", summary)
    _write_json(out / "video_frame_sampling_report.json", result["sampling_report"])
    _write_json(out / "video_frame_matrix.json", result["matrix"])
    _write_json(out / "video_frame_audit_report.json", result["audit"])

    notes = (
        "# Phase-Vision-VideoFrame-Minimal-Ingest-001\n\n"
        "Offline **video frame** ingest skeleton: decode → stride/cap sampling → PNG `image_ref` + `video_frame_envelope_v0` JSONL. "
        "**No** YOLO, OCR, VLM, camera, MidPlatform fact, Scene Delta, WorldModel, AI interpretation, navigation.\n"
    )
    (out / "video_frame_ingest_notes.md").write_text(notes, encoding="utf-8")

    print(
        json.dumps(
            {
                "video_frame_minimal_ingest_smoke_root": str(out),
                "input_mode": input_mode,
                "source_video_ref": str(video_path),
                "status": "success",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
