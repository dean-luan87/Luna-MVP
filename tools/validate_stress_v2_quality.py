#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stress_v2 质量验收（segment-first）：slice 内 hot 比例 ≥ X，且存在连续 hot 段长度 ≥ 2。
hot_line 用 slice 内部分布的 percentile 计算，不依赖固定阈值。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import numpy as np
except ImportError:
    np = None


def read_records(records_path: Path) -> list:
    xs = []
    with open(records_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            obs = r.get("obs") or {}
            v = obs.get("weighted_sum", obs.get("motion", 0.0))
            xs.append(float(v) if v is not None else 0.0)
    return xs


def _percentile(xs: list, p: float) -> float:
    if not xs:
        return 0.0
    if np is not None:
        return float(np.percentile(np.array(xs), p))
    sorted_xs = sorted(xs)
    i = min(int(len(sorted_xs) * p / 100.0), len(sorted_xs) - 1)
    return float(sorted_xs[max(0, i)])


def longest_run(mask: list) -> int:
    best = 0
    cur = 0
    for m in mask:
        if m:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episodes-dir", required=True, help=".../library_store/v1.1/episodes/YYYYMMDD/stress_v2_xxx")
    ap.add_argument("--min-episodes", type=int, default=8)
    ap.add_argument("--hot-percentile", type=float, default=95.0, help="inside-slice hot line percentile")
    ap.add_argument("--min-hot-ratio", type=float, default=0.02, help=">=2%% hot frames")
    ap.add_argument("--min-run", type=int, default=2, help=">=2 consecutive hot frames")
    args = ap.parse_args()

    episodes_dir = args.episodes_dir
    if "YYYYMMDD" in episodes_dir:
        # 用今日或最近存在的日期替换 YYYYMMDD
        today = datetime.now(timezone.utc).strftime("%Y%m%d")
        try_dir = episodes_dir.replace("YYYYMMDD", today)
        base = ROOT / try_dir if not Path(try_dir).is_absolute() else Path(try_dir)
        if not base.exists():
            # 在 episodes 下找最近日期的同名 stress 目录
            parts = Path(episodes_dir).parts
            if "episodes" in parts:
                idx = list(parts).index("episodes")
                prefix = Path(*parts[: idx + 1])
                stem = Path(episodes_dir).name
                if not prefix.is_absolute():
                    prefix = ROOT / prefix
                if prefix.exists():
                    dates = sorted([p.name for p in prefix.iterdir() if p.is_dir() and p.name.isdigit()], reverse=True)
                    for d in dates:
                        cand = prefix / d / stem
                        if cand.exists():
                            base = cand
                            episodes_dir = str(cand)
                            break
        if not base.exists():
            base = ROOT / episodes_dir if not Path(episodes_dir).is_absolute() else Path(episodes_dir)
    else:
        base = Path(episodes_dir)
        if not base.is_absolute():
            base = ROOT / base
    if not base.exists():
        raise SystemExit("episodes-dir not found: %s" % base)

    episode_dirs = [p for p in base.iterdir() if p.is_dir() and (p / "records.jsonl").exists()]
    if not episode_dirs:
        raise SystemExit("no episodes found under episodes-dir")

    reports = []
    passed = 0
    for ep in sorted(episode_dirs):
        xs = read_records(ep / "records.jsonl")
        if len(xs) == 0:
            reports.append((ep.name, False, {"reason": "empty_records"}))
            continue
        hot_line = _percentile(xs, args.hot_percentile)
        hot_mask = [x >= hot_line for x in xs]
        hot_ratio = sum(hot_mask) / max(1, len(hot_mask))
        run = longest_run(hot_mask)
        ok = (hot_ratio >= args.min_hot_ratio) and (run >= args.min_run)
        if ok:
            passed += 1
        reports.append((ep.name, ok, {"frames": len(xs), "hot_line": hot_line, "hot_ratio": hot_ratio, "max_run": run}))

    print("=== STRESS_V2_QUALITY ===")
    print("episodes_total=%d passed=%d min_required=%d" % (len(reports), passed, args.min_episodes))
    for name, ok, info in reports:
        flag = "PASS" if ok else "FAIL"
        print(
            "%s %s hot_ratio=%.4f max_run=%d hot_line=%.4f frames=%d"
            % (flag, name, info.get("hot_ratio", 0), info.get("max_run", 0), info.get("hot_line", 0), info.get("frames", 0))
        )
    if passed < args.min_episodes:
        raise SystemExit("[FAIL] only %d episodes passed (need %d)" % (passed, args.min_episodes))
    print("[OK] stress_v2 quality gate passed")


if __name__ == "__main__":
    main()
