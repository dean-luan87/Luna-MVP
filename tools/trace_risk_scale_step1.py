#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STEP 1 量纲审计：对单条 episode 逐帧输出 raw_weighted_sum / effective_risk / ema_risk / final_risk_used_for_decision，
并打印分布（min, max, mean, p50, p95），用于确认压扁发生在哪一段。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _quantile(sorted_arr, q: float):
    if not sorted_arr:
        return None
    n = len(sorted_arr)
    i = max(0, min(n - 1, int(q * n)))
    return sorted_arr[i]


def run_trace_stats(records_path: Path, patch_config: dict, max_frames: int = 0) -> dict:
    """对单条 episode 跑 A3 trace，返回 ema_max, ema_p95, clamp_hit_ratio, n_frames 等，供 sweep 聚合。"""
    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()
    rows = []
    with open(records_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            if max_frames and len(rows) >= max_frames:
                break
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (r.get("record_type") or "").strip() != "OBS_V1":
                continue
            ts = float(r.get("ts", 0.0))
            out = adapter.tick(r, virtual_ts=ts)
            debug = out.get("a3_debug") or {}
            effective = debug.get("raw_effective")
            ema = debug.get("ema")
            clamp_hit = debug.get("clamp_hit")
            if isinstance(clamp_hit, bool):
                clamp_hit = 1.0 if clamp_hit else 0.0
            rows.append({"effective_risk": effective, "ema_risk": ema, "clamp_hit": clamp_hit})
    if not rows:
        return {"n_frames": 0, "ema_max": None, "ema_p95": None, "clamp_hit_ratio": None}
    ema_vals = [r["ema_risk"] for r in rows if r.get("ema_risk") is not None]
    clamp_vals = [r.get("clamp_hit", 0) for r in rows]
    n = len(rows)
    s = sorted(ema_vals) if ema_vals else []
    return {
        "n_frames": n,
        "ema_max": max(ema_vals) if ema_vals else None,
        "ema_p95": s[int(0.95 * len(s))] if s else None,
        "clamp_hit_ratio": sum(clamp_vals) / n if n else None,
    }


def main():
    ap = argparse.ArgumentParser(description="STEP 1: trace risk chain for one episode")
    ap.add_argument("--records", required=True, help="path to episode records.jsonl")
    ap.add_argument("--risk-scale", type=float, default=1.0, help="risk_scale_factor (default 1.0)")
    ap.add_argument("--patch", default="", help="optional patch JSON path (overrides risk-scale for full config)")
    ap.add_argument("--out-trace", default="", help="write per-frame trace to this jsonl (default: stdout only summary)")
    ap.add_argument("--max-frames", type=int, default=0, help="max frames to process (0 = all)")
    args = ap.parse_args()

    records_path = Path(args.records)
    if not records_path.is_file():
        print("ERROR: records not found:", records_path, file=sys.stderr)
        return 2

    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter

    if args.patch and Path(args.patch).is_file():
        with open(args.patch, "r", encoding="utf-8") as f:
            patch = json.load(f)
    else:
        patch = {"risk_scale_factor": args.risk_scale}
    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch)
    adapter.reset()

    rows = []
    with open(records_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if not line.strip():
                continue
            if args.max_frames and len(rows) >= args.max_frames:
                break
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if (r.get("record_type") or "").strip() != "OBS_V1":
                continue
            ts = float(r.get("ts", 0.0))
            out = adapter.tick(r, virtual_ts=ts)
            debug = out.get("a3_debug") or {}
            raw_weighted_sum = debug.get("weighted_sum_before_clamp")
            scaled_sum = debug.get("scaled_sum_before_clamp")
            effective_risk = debug.get("raw_effective")
            ema_risk = debug.get("ema")
            final_risk = ema_risk  # 当前设计里决策直接用 ema
            clamp_hit = debug.get("clamp_hit")
            if isinstance(clamp_hit, bool):
                clamp_hit = 1.0 if clamp_hit else 0.0
            row = {
                "seq": r.get("seq"),
                "ts": ts,
                "raw_weighted_sum": raw_weighted_sum,
                "scaled_sum_before_clamp": scaled_sum,
                "effective_risk": effective_risk,
                "ema_risk": ema_risk,
                "final_risk_used_for_decision": final_risk,
                "clamp_hit": clamp_hit,
                "safety_level": out.get("safety_level"),
                "control_mode": out.get("control_mode"),
                "threshold_safe_to_caution": debug.get("threshold_safe_to_caution"),
            }
            rows.append(row)

    if not rows:
        print("ERROR: no OBS_V1 records found", file=sys.stderr)
        return 2

    # 分布统计
    def series(key):
        return [r[key] for r in rows if r.get(key) is not None]

    def stats(name, vals):
        if not vals:
            return None
        s = sorted(vals)
        n = len(s)
        return {
            "min": min(vals),
            "max": max(vals),
            "mean": sum(vals) / n,
            "p50": _quantile(s, 0.5),
            "p95": _quantile(s, 0.95),
        }

    raw_ws = series("raw_weighted_sum")
    eff = series("effective_risk")
    ema = series("ema_risk")
    final = series("final_risk_used_for_decision")

    if args.out_trace:
        out_path = Path(args.out_trace)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("[OK] trace written to", out_path.resolve(), "(%d rows)" % len(rows))

    # 打印四段分布
    th = rows[0].get("threshold_safe_to_caution")
    print("\n=== STEP 1 量纲审计 (risk_scale=%.1f, threshold_safe_to_caution=%s) ===" % (args.risk_scale, th))
    print("frames =", len(rows))
    print()
    for label, vals in [
        ("raw_weighted_sum (权重和，scale 前)", raw_ws),
        ("effective_risk (raw × view_confidence 后)", eff),
        ("ema_risk (EMA 平滑后)", ema),
        ("final_risk_used_for_decision (参与阈值判定)", final),
    ]:
        s = stats(label, vals)
        if s is None:
            print("%s: (无数据)" % label)
            continue
        print("%s:" % label)
        print("  min=%.4f max=%.4f mean=%.4f p50=%.4f p95=%.4f" % (s["min"], s["max"], s["mean"], s["p50"], s["p95"]))
        print()

    # 简要结论
    if raw_ws:
        r_max = max(raw_ws)
        if th is not None and r_max < float(th) * 0.5:
            print("→ raw_weighted_sum 最大 %.4f 远低于阈值 %.4f：量纲在 weighted_sum 段就偏小。" % (r_max, th))
    if ema and th is not None:
        e_max = max(ema)
        if e_max < float(th) * 0.5:
            print("→ ema_risk 最大 %.4f 远低于阈值：可能 view_confidence 压低或 EMA alpha 使信号未跟上。" % e_max)
    return 0


if __name__ == "__main__":
    sys.exit(main())
