#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase B2：高压 Golden v2 —— 强制连续触边。
从 6m42s trace 筛：weighted_sum 分布 → P0/fallback 触发 → 连续窗口(≥3 帧 ≥0.9*阈值 或 ≥4 帧 ≥0.85*阈值)
→ 取压力段后 ±4s 切片 → 去重(重叠>60% 合并) → 输出 8~12 条到 golden_stress_v2。
用法：先跑 run_video_a3_trace.py --video test_video_complex_6m42s.mp4，再跑本脚本 --trace logs/a3_trace.jsonl。
"""
import json
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SAFE_TO_CAUTION = 0.195  # 校准档，用于 0.9/0.85/0.5 倍数
THRESHOLD_90 = 0.9 * SAFE_TO_CAUTION   # 0.1755
THRESHOLD_85 = 0.85 * SAFE_TO_CAUTION  # 0.16575
THRESHOLD_50 = 0.5 * SAFE_TO_CAUTION   # 0.0975
WINDOW_SEC = 4.0  # ±4s


def _load_trace(path: str) -> list:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _trace_row_to_record(row: dict, seq: int) -> dict:
    return {
        "record_type": "OBS_V1",
        "ts": row.get("ts", 0),
        "seq": row.get("seq", seq),
        "sampled": row.get("sampled", False),
        "obs": row.get("obs", {}),
        "decision": row.get("decision", {}),
    }


def _compute_weighted_sum_per_frame(records: list) -> list:
    """对每条 record 跑 A3 adapter，返回 (weighted_sum, motion_raw, path_raw, branch) 列表。"""
    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter
    adapter = A3HeadlessAdapter(base_config={}, patch_config={})
    adapter.reset()
    out = []
    for i, r in enumerate(records):
        ts = r.get("ts", 0.0)
        tick = adapter.tick(r, virtual_ts=ts)
        db = tick.get("a3_debug") or {}
        ws = float(db.get("weighted_sum_before_clamp", 0))
        motion = float(db.get("motion_instability_raw", db.get("motion_instability", 0)))
        path = float(db.get("path_instability_raw", db.get("path_instability", 0)))
        obs = r.get("obs") or {}
        branch = obs.get("branch")
        if branch is None:
            branch = 0.0
        branch = float(branch) if isinstance(branch, (int, float)) else 0.0
        out.append((ws, motion, path, branch))
    return out


def _percentile(sorted_vals: list, pct: float) -> float:
    if not sorted_vals:
        return 0.0
    i = min(int(len(sorted_vals) * pct / 100.0), len(sorted_vals) - 1)
    return float(sorted_vals[max(0, i)])


def _find_consecutive_run(ws_list: list, start_idx: int, threshold: float, min_len: int) -> tuple:
    """从 start_idx 向两侧找连续 >= threshold 的区间，返回 (run_start, run_end) 若长度 >= min_len 否则 (-1,-1)。"""
    n = len(ws_list)
    # 以 start_idx 为中心向两边扩展
    lo = start_idx
    while lo > 0 and ws_list[lo - 1][0] >= threshold:
        lo -= 1
    hi = start_idx
    while hi < n - 1 and ws_list[hi + 1][0] >= threshold:
        hi += 1
    if hi - lo + 1 >= min_len:
        return (lo, hi)
    return (-1, -1)


def _merge_overlapping(intervals: list, overlap_ratio: float = 0.6) -> list:
    """(start_idx, end_idx) 列表，重叠 > overlap_ratio 的合并。"""
    if not intervals:
        return []
    sorted_i = sorted(intervals, key=lambda x: x[0])
    merged = [list(sorted_i[0])]
    for a, b in sorted_i[1:]:
        prev_a, prev_b = merged[-1]
        len_prev = prev_b - prev_a + 1
        len_cur = b - a + 1
        overlap = max(0, min(prev_b, b) - max(prev_a, a) + 1)
        if overlap >= overlap_ratio * min(len_prev, len_cur):
            merged[-1][1] = max(prev_b, b)
        else:
            merged.append([a, b])
    return [tuple(x) for x in merged]


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Generate stress_v2 episodes from 6m42s trace (continuous near-threshold)")
    p.add_argument("--trace", default=os.path.join(ROOT, "logs", "a3_trace.jsonl"), help="a3_trace.jsonl path")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--out-dir", default="", help="default: base_dir/version/golden_stress_v2")
    p.add_argument("--min-episodes", type=int, default=8)
    p.add_argument("--max-episodes", type=int, default=12)
    p.add_argument("--safe-to-caution", type=float, default=SAFE_TO_CAUTION)
    args = p.parse_args()

    trace_path = args.trace if os.path.isabs(args.trace) else os.path.join(ROOT, args.trace)
    if not os.path.isfile(trace_path):
        print("ERROR: trace not found:", trace_path, file=sys.stderr)
        print("Run first: python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4", file=sys.stderr)
        return 2

    rows = _load_trace(trace_path)
    if not rows:
        print("ERROR: empty trace", file=sys.stderr)
        return 2

    records = [_trace_row_to_record(r, i) for i, r in enumerate(rows)]
    print("computing weighted_sum per frame (A3)...")
    ws_per = _compute_weighted_sum_per_frame(records)
    n = len(ws_per)
    ws_vals = [x[0] for x in ws_per]
    motion_vals = [x[1] for x in ws_per]
    sorted_ws = sorted(ws_vals)
    p99 = _percentile(sorted_ws, 99)
    p99_5 = _percentile(sorted_ws, 99.5)
    motion_p95 = _percentile(sorted(motion_vals), 95)
    top50_frames = sorted(range(n), key=lambda i: -ws_vals[i])[:50]
    print("p99:", round(p99, 4), "p99.5:", round(p99_5, 4), "motion_p95:", round(motion_p95, 4))

    # 触发候选：P0 或 fallback
    trigger_candidates = []
    for i in range(n):
        ws, motion, path, branch = ws_per[i]
        if ws < p99:
            continue
        if branch > 0 and motion > motion_p95:
            trigger_candidates.append((i, "P0"))
        elif branch > 0 or motion > motion_p95:
            trigger_candidates.append((i, "P1"))

    # 连续窗口筛选：先固定阈值(0.9/0.85*stc)，若无则用数据驱动(0.9*p99, 0.85*p99)
    th90 = 0.9 * args.safe_to_caution
    th85 = 0.85 * args.safe_to_caution
    th50 = 0.5 * args.safe_to_caution
    th_p99_90 = 0.9 * p99
    th_p99_85 = 0.85 * p99
    valid_centers = []
    effective_near_threshold = None  # 写入 meta，验收脚本用同一根“近线”

    for idx, _ in trigger_candidates:
        for th, min_len in [(th90, 3), (th85, 4)]:
            run_lo, run_hi = _find_consecutive_run(ws_per, idx, th, min_len)
            if run_lo >= 0:
                center = (run_lo + run_hi) // 2
                valid_centers.append(center)
                if effective_near_threshold is None:
                    effective_near_threshold = th
                break
    if not valid_centers:
        for idx, _ in trigger_candidates:
            for th, min_len in [(th_p99_90, 3), (th_p99_85, 4)]:
                run_lo, run_hi = _find_consecutive_run(ws_per, idx, th, min_len)
                if run_lo >= 0:
                    center = (run_lo + run_hi) // 2
                    valid_centers.append(center)
                    if effective_near_threshold is None:
                        effective_near_threshold = th
                    break
    if not valid_centers:
        print("WARN: no valid consecutive trigger; using top weighted_sum frames as centers (near_threshold=0.9*p99)")
        effective_near_threshold = th_p99_90
        for i in top50_frames[:20]:
            valid_centers.append(i)
    if effective_near_threshold is None:
        effective_near_threshold = th_p99_90

    # 对每个 center：向后扫到 ws < 0.5*阈值，向前扫到 ws < 0.5*阈值；再取 ±4s 窗口
    ts_list = [records[i]["ts"] for i in range(n)]
    intervals = []
    for center in valid_centers:
        center_ts = ts_list[center]
        # 向后
        start_i = center
        while start_i > 0 and ws_per[start_i - 1][0] >= th50:
            start_i -= 1
        # 向前
        end_i = center
        while end_i < n - 1 and ws_per[end_i + 1][0] >= th50:
            end_i += 1
        # ±4s
        t_start = center_ts - WINDOW_SEC
        t_end = center_ts + WINDOW_SEC
        i_start = start_i
        while i_start > 0 and ts_list[i_start - 1] >= t_start:
            i_start -= 1
        i_end = end_i
        while i_end < n - 1 and ts_list[i_end + 1] <= t_end:
            i_end += 1
        intervals.append((i_start, i_end))

    # 去重：重叠 > 60% 合并
    intervals = _merge_overlapping(list(set(intervals)), overlap_ratio=0.6)
    # 按窗口内 weighted_sum 总和排序，取前 max_episodes
    def score_interval(ab):
        a, b = ab
        return sum(ws_per[i][0] for i in range(a, b + 1))
    intervals = sorted(intervals, key=score_interval, reverse=True)[: args.max_episodes]
    if len(intervals) < args.min_episodes:
        print("WARN: only", len(intervals), "episodes after dedup (min", args.min_episodes, ")")

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    out_dir = args.out_dir or os.path.join(ROOT, base_dir, version, "golden_stress_v2")
    os.makedirs(out_dir, exist_ok=True)
    # 每次生成前清空目录，避免换 trace（如 --frame-step）后与旧 episode 混在一起
    for name in os.listdir(out_dir):
        p = os.path.join(out_dir, name)
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)
    src_name = Path(trace_path).stem

    for ep_idx, (start_idx, end_idx) in enumerate(intervals):
        slice_records = [records[i] for i in range(start_idx, end_idx + 1)]
        start_ts = ts_list[start_idx]
        end_ts = ts_list[end_idx]
        ep_id = f"stress_v2_{src_name}_tr{start_idx}_{end_idx}"
        ep_path = os.path.join(out_dir, ep_id)
        os.makedirs(ep_path, exist_ok=True)
        with open(os.path.join(ep_path, "records.jsonl"), "w", encoding="utf-8") as f:
            for r in slice_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        meta = {
            "version_tag": version,
            "episode_id": ep_id,
            "source_episode_path": f"{version}/golden_stress_v2/{ep_id}",
            "tags": ["stress_v2", "continuous_near_threshold"],
            "reason": f"B2 continuous stress: trace {src_name} seg [{start_idx},{end_idx}] ±4s",
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "trace_path": str(trace_path),
            "start_idx": start_idx,
            "end_idx": end_idx,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "stress_v2_near_threshold": effective_near_threshold,
        }
        with open(os.path.join(ep_path, "meta.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

    print("wrote", len(intervals), "episodes to", out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
