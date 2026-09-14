#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Determinism 漂移定位：对比 pass1 vs pass2 的 stress_per_episode_metrics.json，
输出 early_gain_weighted 不一致的 episode_id、最大/总和差值，以及便于抓帧的 replay 路径提示。
用法: python3 tools/diff_stress_per_episode.py <path_pass1/metrics.json> <path_pass2/metrics.json>
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]


def load_metrics(path: Path) -> List[Dict[str, Any]]:
    if not path.is_file():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


def _f(x: Any) -> Optional[float]:
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def run_diff(path1: Path, path2: Path, top_n: int = 10) -> None:
    m1 = load_metrics(path1)
    m2 = load_metrics(path2)
    by_id1 = {e["episode_id"]: e for e in m1 if e.get("episode_id")}
    by_id2 = {e["episode_id"]: e for e in m2 if e.get("episode_id")}
    all_ids = sorted(set(by_id1) | set(by_id2))

    diffs: List[Tuple[str, float, float, float]] = []
    for eid in all_ids:
        a = _f((by_id1.get(eid) or {}).get("early_gain_weighted"))
        b = _f((by_id2.get(eid) or {}).get("early_gain_weighted"))
        if a is None and b is None:
            continue
        if a is None:
            a = float("nan")
        if b is None:
            b = float("nan")
        diff = abs(a - b) if (a == a and b == b) else float("nan")
        if diff != 0 and diff == diff:
            diffs.append((eid, a, b, diff))

    diffs.sort(key=lambda x: -x[3])
    top = diffs[:top_n]

    print("[diff_stress_per_episode] pass1=%s pass2=%s" % (path1, path2))
    print("[diff_stress_per_episode] episodes in pass1=%d pass2=%d common_ids=%d" % (len(by_id1), len(by_id2), len(all_ids)))
    print("[diff_stress_per_episode] early_gain_weighted 不一致的 episode 数: %d" % len(diffs))
    if diffs:
        total_diff = sum(d[3] for d in diffs)
        max_diff = max(d[3] for d in diffs)
        print("[diff_stress_per_episode] 差值总和=%.6f 最大差值=%.6f" % (total_diff, max_diff))
        print("[diff_stress_per_episode] 漂移 Top-%d (episode_id, pass1, pass2, |diff|):" % len(top))
        for eid, v1, v2, d in top:
            print("  %s  %.6f  %.6f  %.6f" % (eid, v1, v2, d))
        print("[diff_stress_per_episode] 抓帧提示: 上述 episode_id 对应 suite 下 clip 目录名，replay 在 run_dir/<champion_id>/episodes_stress_responsive/<episode_id>/ 或 sim_out 对应 episode 目录下 candidate_replay_path。")
    else:
        print("[diff_stress_per_episode] 无 early_gain_weighted 数值差异（或均为 None）。")


def main() -> int:
    if len(sys.argv) < 3:
        print("用法: python3 tools/diff_stress_per_episode.py <stress_per_episode_metrics_pass1.json> <stress_per_episode_metrics_pass2.json> [top_n]", file=sys.stderr)
        return 2
    path1 = Path(sys.argv[1])
    path2 = Path(sys.argv[2])
    if not path1.is_absolute():
        path1 = ROOT / path1
    if not path2.is_absolute():
        path2 = ROOT / path2
    top_n = 10
    if len(sys.argv) > 3:
        try:
            top_n = int(sys.argv[3])
        except ValueError:
            pass
    run_diff(path1, path2, top_n=top_n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
