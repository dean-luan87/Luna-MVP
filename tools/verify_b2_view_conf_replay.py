#!/usr/bin/env python3
"""
B2 生效验证（只做一次）：用一条 responsive replay 判定
  (1) view_conf 分布是否接近 1（解释“无梯度”）；
  (2) gate 是否参与计算（raw_effective 与 floor + (1-floor)*vc^k 一致）。

用法:
  # 3.1 抽样 view_conf 分布
  python3 tools/verify_b2_view_conf_replay.py --stats REPLAY.jsonl

  # 3.2 抽一帧校验 gate 手算
  python3 tools/verify_b2_view_conf_replay.py --gate REPLAY.jsonl

REPLAY 示例: outputs/d1_runs/phase3_b2_view_conf/floor0.5_k1.0/<ts>/sim_out/.../replay_output.jsonl
  或任意含 a3_debug.view_confidence / raw / raw_effective 的 jsonl。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _gate_expect(vc: float, floor: float, k: float) -> float:
    if vc <= 0:
        return floor
    if vc >= 1:
        return 1.0
    return floor + (1.0 - floor) * (vc ** k)


def cmd_stats(path: Path) -> None:
    v = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            dbg = d.get("a3_debug") or {}
            if "view_confidence" in dbg:
                v.append(float(dbg["view_confidence"]))
    print("n =", len(v))
    if not v:
        print("no view_confidence in a3_debug")
        return
    v.sort()
    n = len(v)
    print("min / median / p90 / max =", v[0], v[n // 2], v[int(n * 0.9)], v[-1])
    if v[n // 2] >= 0.98 and v[-1] >= 0.98:
        print("→ view_conf 基本≥0.98，B2 gate 在当前 suite 下无梯度（noop）")


def cmd_gate(path: Path) -> None:
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        dbg = d.get("a3_debug") or {}
        if "raw" not in dbg or "raw_effective" not in dbg or "view_confidence" not in dbg:
            continue
        raw = float(dbg["raw"])
        re = float(dbg["raw_effective"])
        vc = float(dbg["view_confidence"])
        floor = float(dbg.get("view_conf_gate_floor", 0.5))
        k = float(dbg.get("view_conf_gate_k", 1.0))
        gate = _gate_expect(vc, floor, k)
        expect = raw * gate
        diff = re - expect
        print("raw", raw, "vc", vc, "floor", floor, "k", k)
        print("raw_effective", re, "expect(raw*gate)", expect, "diff", diff)
        if abs(diff) < 1e-5:
            print("→ diff≈0：B2 gate 已参与计算，当前 suite 数据域不敏感。")
        else:
            print("→ diff 大：请检查 patch/引擎是否接入 view_conf_gate。")
        return
    print("no frame with raw/raw_effective/view_confidence in a3_debug")


def main() -> None:
    ap = argparse.ArgumentParser(description="B2 生效验证：view_conf 分布 + gate 手算")
    ap.add_argument("replay", type=Path, help="replay_output.jsonl 路径")
    ap.add_argument("--stats", action="store_true", help="输出 view_conf 分布")
    ap.add_argument("--gate", action="store_true", help="抽一帧校验 raw_effective = raw * gate")
    args = ap.parse_args()
    if not args.replay.is_file():
        print("not a file:", args.replay, file=sys.stderr)
        sys.exit(1)
    if args.stats:
        cmd_stats(args.replay)
    elif args.gate:
        cmd_gate(args.replay)
    else:
        print("指定 --stats 或 --gate", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
