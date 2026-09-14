#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segment-first 高压 stress 生成：p95 连续段 ≥2 帧，扩窗 ±3s，写 slice episode。
输出：library_store/<version_tag>/episodes/<YYYYMMDD>/stress_v2_<trace_stem>/slice_*/records.jsonl
     + episodes.index.jsonl + meta.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
except ImportError:
    np = None

from tools.stress_v2.trace_reader import iter_trace_frames
from tools.stress_v2.window_ops import merge_overlaps, expand_window


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _percentile(xs: list, p: float) -> float:
    if not xs:
        return 0.0
    if np is not None:
        return float(np.percentile(np.array(xs, dtype=np.float64), p))
    sorted_xs = sorted(xs)
    i = min(int(len(sorted_xs) * p / 100.0), len(sorted_xs) - 1)
    return float(sorted_xs[max(0, i)])


def _infer_fps(ts_ms_list: list) -> float:
    if not ts_ms_list or len(ts_ms_list) < 50:
        return 30.0
    diffs = []
    for a, b in zip(ts_ms_list[:-1], ts_ms_list[1:]):
        if a is None or b is None:
            continue
        d = b - a
        if 5 <= d <= 200:
            diffs.append(d)
    if not diffs:
        return 30.0
    if np is not None:
        med = float(np.median(np.array(diffs)))
    else:
        sorted_d = sorted(diffs)
        med = sorted_d[len(sorted_d) // 2]
    fps = 1000.0 / med if med > 0 else 30.0
    return max(10.0, min(120.0, fps))


def build_segments(weighted_sums: list, min_run: int, hot_line: float) -> list:
    is_hot = [x >= hot_line for x in weighted_sums]
    segs = []
    cur = []
    for i, hot in enumerate(is_hot):
        if hot:
            cur.append(i)
        else:
            if len(cur) >= min_run:
                segs.append((cur[0], cur[-1]))
            cur = []
    if len(cur) >= min_run:
        segs.append((cur[0], cur[-1]))
    return segs


def write_slice_episode(out_dir: Path, slice_id: str, frames: list) -> str:
    ep_dir = out_dir / slice_id
    _ensure_dir(ep_dir)
    rec_path = ep_dir / "records.jsonl"
    with open(rec_path, "w", encoding="utf-8") as f:
        for fr in frames:
            ts = fr.get("ts_ms")
            if ts is not None:
                ts_sec = ts / 1000.0
            else:
                ts_sec = fr.get("seq", 0) / 30.0
            rec = {
                "record_type": "OBS_V1",
                "seq": fr["seq"],
                "ts": ts_sec,
                "timestamp": fr.get("ts_ms"),
                "obs": {
                    "motion": fr.get("motion_instability", 0.0),
                    "path": fr.get("path_instability", 0.0),
                    "branch": fr.get("branch_load", 0.0),
                    "complexity": fr.get("complexity_raw", 0.0),
                    "weighted_sum": fr.get("weighted_sum", 0.0),
                    "complexity_raw": fr.get("complexity_raw", 0.0),
                    "motion_instability": fr.get("motion_instability", 0.0),
                    "path_instability": fr.get("path_instability", 0.0),
                    "branch_load": fr.get("branch_load", 0.0),
                },
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return str(rec_path.resolve())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trace", required=True, help="e.g. logs/a3_trace.jsonl")
    ap.add_argument("--base-dir", default="library_store")
    ap.add_argument("--version-tag", required=True, help="e.g. v1.1")
    ap.add_argument("--date", default=None, help="YYYYMMDD, default=UTC today")
    ap.add_argument("--stress-name", default=None, help="subdir name, default=stress_v2_<trace_stem>")
    ap.add_argument("--percentile", type=float, default=95.0, help="hot line percentile")
    ap.add_argument("--min-run", type=int, default=2, help="min consecutive hot frames for a segment")
    ap.add_argument("--window-sec", type=float, default=3.0, help="expand window +- seconds")
    ap.add_argument("--max-slices", type=int, default=12, help="cap slices")
    args = ap.parse_args()

    trace_path = Path(args.trace)
    if not trace_path.is_absolute():
        trace_path = ROOT / trace_path
    if not trace_path.exists():
        raise SystemExit("trace not found: %s" % trace_path)

    frames = []
    ts_list = []
    for fr in iter_trace_frames(str(trace_path)):
        frames.append(fr)
        ts_list.append(fr.ts_ms)

    if not frames:
        raise SystemExit("no frames parsed from trace")

    fps = _infer_fps(ts_list)
    win = int(round(args.window_sec * fps))
    weighted = [fr.weighted_sum for fr in frames]
    hot_line = _percentile(weighted, args.percentile)

    segs = build_segments(weighted, min_run=args.min_run, hot_line=hot_line)
    if not segs:
        raise SystemExit(
            "no segments found: percentile=%s, min_run=%s, hot_line=%.6f"
            % (args.percentile, args.min_run, hot_line)
        )

    max_i = len(frames) - 1
    windows = []
    for s, e in segs:
        w = expand_window((s, e), left=win, right=win, lo=0, hi=max_i)
        windows.append(w)
    windows = merge_overlaps(windows)

    def score_window(se):
        s, e = se
        sub = frames[s : e + 1]
        comp = max((x.complexity_raw for x in sub), default=0.0)
        br = max((x.branch_load for x in sub), default=0.0)
        mot = max((x.motion_instability for x in sub), default=0.0)
        return comp * 1.0 + br * 2.0 + mot * 0.5

    scored = [(w, score_window(w)) for w in windows]
    scored.sort(key=lambda x: x[1], reverse=True)
    chosen = scored[: max(1, min(args.max_slices, len(scored)))]

    date = args.date
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y%m%d")
    stress_name = args.stress_name or ("stress_v2_%s" % trace_path.stem)
    base = Path(args.base_dir)
    if not base.is_absolute():
        base = ROOT / base
    out_dir = base / args.version_tag / "episodes" / date / stress_name
    _ensure_dir(out_dir)

    meta = {
        "trace": str(trace_path.resolve()),
        "fps_inferred": fps,
        "percentile": args.percentile,
        "hot_line": hot_line,
        "min_run": args.min_run,
        "window_sec": args.window_sec,
        "max_slices": args.max_slices,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(out_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    written = []
    for idx, (w, score) in enumerate(chosen):
        s, e = w
        slice_id = "slice_tr%d_%d_p%s_%02d" % (
            frames[s].seq,
            frames[e].seq,
            str(args.percentile).replace(".", "_"),
            idx,
        )
        slice_frames = []
        for fr in frames[s : e + 1]:
            slice_frames.append({
                "seq": fr.seq,
                "ts_ms": fr.ts_ms,
                "weighted_sum": fr.weighted_sum,
                "complexity_raw": fr.complexity_raw,
                "motion_instability": fr.motion_instability,
                "path_instability": fr.path_instability,
                "branch_load": fr.branch_load,
            })
        rec_path = write_slice_episode(out_dir, slice_id, slice_frames)
        sub = frames[s : e + 1]
        comp = max((x.complexity_raw for x in sub), default=0.0)
        br = max((x.branch_load for x in sub), default=0.0)
        mot = max((x.motion_instability for x in sub), default=0.0)
        index_rec = {
            "episode_id": slice_id,
            "episode_path": str((out_dir / slice_id).resolve()),
            "records_path": rec_path,
            "segment": {"start_i": s, "end_i": e, "start_seq": frames[s].seq, "end_seq": frames[e].seq},
            "rank_score": score,
            "signals": {"max_complexity": comp, "max_branch": br, "max_motion": mot},
            "tags": ["stress_v2"],
        }
        written.append(index_rec)

    with open(out_dir / "episodes.index.jsonl", "w", encoding="utf-8") as f:
        for r in written:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("[OK] fps=%.2f, hot_line(p%s)=%.6f" % (fps, args.percentile, hot_line))
    print("[OK] segments=%d, windows=%d, chosen=%d" % (len(segs), len(windows), len(written)))
    print("[OK] out_dir=%s" % out_dir.resolve())
    print("[OK] index=%s" % (out_dir / "episodes.index.jsonl").resolve())


if __name__ == "__main__":
    main()
