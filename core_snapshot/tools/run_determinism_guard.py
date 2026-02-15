#!/usr/bin/env python3
"""
Determinism regression guard (REPLAY ONLY).
工程护栏：只允许 Replay Mode；未提供 video 直接失败。
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def root_dir():
    return Path(__file__).resolve().parents[1]


def run(cmd, env=None):
    print(">>", " ".join(cmd))
    r = subprocess.run(cmd, env=env)
    if r.returncode != 0:
        sys.exit(r.returncode)


def write_meta(out_dir, meta):
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "run_meta.json", "w") as f:
        json.dump(meta, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Determinism regression guard (REPLAY ONLY)."
    )
    parser.add_argument("--video", required=True, help="Input video path (required)")
    parser.add_argument("--frames", type=int, default=900, help="Max frames to process")
    parser.add_argument("--fps", type=float, default=30.0, help="FPS for replay clock")
    parser.add_argument(
        "--out-root",
        default="logs/determinism",
        help="Root output dir (two runs will be created inside)",
    )
    parser.add_argument(
        "--policy",
        default=None,
        help="Optional policy identifier (string) to record in meta",
    )
    args = parser.parse_args()

    # Strictness: REPLAY ONLY
    video = Path(args.video)
    if not video.exists():
        print(f"❌ Video not found: {video}")
        sys.exit(2)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_root = Path(args.out_root) / f"replay_{ts}"
    run1 = out_root / "run1"
    run2 = out_root / "run2"

    meta = {
        "mode": "REPLAY_ONLY",
        "video": str(video.resolve()),
        "frames": args.frames,
        "fps": args.fps,
        "policy": args.policy,
        "timestamp_utc": ts,
    }

    write_meta(run1, meta)
    write_meta(run2, meta)

    # Phase 2.1: 外部感知只写不读硬门禁（先于 replay 执行）
    print("\n=== Phase 2.1-Guard (no external field reads) ===")
    guard_result = subprocess.run(
        [sys.executable, "tools/guard_no_external_field_reads.py"],
        cwd=str(root_dir()),
    )
    if guard_result.returncode != 0:
        print("❌ Phase 2.1-Guard failed; determinism guard aborted.")
        sys.exit(guard_result.returncode)

    # Command to produce trace (REPLAY MODE enforced by script)
    base_cmd = [
        sys.executable,
        "tools/run_video_a3_trace.py",
        "--video", str(video),
        "--max-frames", str(args.frames),
        "--fps", str(args.fps),
        "--out",
    ]

    print("\n=== Run 1 (REPLAY) ===")
    run(base_cmd + [str(run1)])

    print("\n=== Run 2 (REPLAY) ===")
    run(base_cmd + [str(run2)])

    trace1 = run1 / "a3_trace.jsonl"
    trace2 = run2 / "a3_trace.jsonl"

    if not trace1.exists() or not trace2.exists():
        print("❌ Missing trace output(s).")
        sys.exit(2)

    print("\n=== Determinism Guard ===")
    guard_cmd = [
        sys.executable,
        "tools/determinism_guard.py",
        str(trace1),
        str(trace2),
    ]
    run(guard_cmd)

    print("\n✅ Determinism regression PASSED.")
    print(f"Artifacts saved to: {out_root}")


if __name__ == "__main__":
    main()
