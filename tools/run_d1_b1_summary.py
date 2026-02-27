#!/usr/bin/env python3
"""
B1 扩容汇总：从 rank_report 提取 6 字段，输出与 freeze 表同结构。

字段: champion_eg, champion_vol, champion_id/bucket, top3(bucket), vol_001, exploit_win_rate

Seed 映射：以 run_manifest.json["seed"] 为准，无则 rank_report.metadata.seed；缺则报错退出。
表按 seed 42/123/777 排序，避免错位。

用法:
  python3 tools/run_d1_b1_summary.py
  python3 tools/run_d1_b1_summary.py outputs/d1_runs/phase3_b1_expansion/20260224xxx ...
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _get_bucket(run_dir: Path, patch_id: str) -> str:
    if patch_id in ("conservative", "responsive"):
        return patch_id
    for name in ("effective_patch.stress_responsive.json", "effective_patch.stress.json"):
        p = run_dir / patch_id / name
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                return (d.get("metadata") or {}).get("bucket") or "—"
            except Exception:
                pass
    return "—"


def _get_seed(run_dir: Path) -> int:
    """从 run_manifest.json 读 seed；无则从 rank_report metadata；缺则报错。"""
    mp = run_dir / "run_manifest.json"
    if mp.is_file():
        d = json.loads(mp.read_text(encoding="utf-8"))
        s = d.get("seed")
        if s is not None:
            return int(s)
    rp = run_dir / "rank_report.json"
    if rp.is_file():
        d = json.loads(rp.read_text(encoding="utf-8"))
        m = d.get("metadata") or {}
        s = m.get("seed")
        if s is not None:
            return int(s)
    raise SystemExit("FATAL: run %s 缺 seed（run_manifest.json 或 rank_report.metadata），无法映射" % run_dir)


def main() -> None:
    ap = argparse.ArgumentParser(description="B1 扩容汇总：6 字段 + 判据")
    ap.add_argument("run_dirs", nargs="*", type=Path)
    ap.add_argument("--base", type=Path, default=ROOT / "outputs" / "d1_runs" / "phase3_b1_expansion")
    ap.add_argument("--labels", nargs="+", default=None, help="显式指定 label，空则用 seed42/123/777")
    args = ap.parse_args()

    run_dirs = list(args.run_dirs)
    if not run_dirs and args.base.is_dir():
        run_dirs = [d for d in args.base.iterdir() if d.is_dir() and (d / "rank_report.json").is_file()]
        run_dirs = sorted(run_dirs, key=lambda p: p.name)[-3:]  # 最新 3 个
    if not run_dirs:
        print("No run dirs", file=sys.stderr)
        sys.exit(1)

    run_with_seed = []
    for d in run_dirs:
        try:
            s = _get_seed(d)
            run_with_seed.append((s, d))
        except SystemExit:
            raise
    run_with_seed.sort(key=lambda x: x[0])  # 按 seed 42/123/777 排序
    run_dirs = [d for _, d in run_with_seed]
    seeds = [s for s, _ in run_with_seed]
    labels = args.labels[: len(run_dirs)] if args.labels else ["seed%d" % s for s in seeds]
    rows = []
    exploit_wins = 0

    for rd, lb in zip(run_dirs, labels):
        rp = rd / "rank_report.json"
        if not rp.is_file():
            rows.append((lb, "—", "—", "—", "—", "—", "—"))
            continue
        data = json.loads(rp.read_text(encoding="utf-8"))
        ranked = data.get("ranked") or []
        champ = ranked[0] if ranked else {}
        cid = data.get("champion_id") or champ.get("patch_id") or "—"
        reg = champ.get("regular_metrics") or {}
        stress_m = champ.get("stress_metrics") or {}
        eg = stress_m.get("early_gain_weighted_mean")
        vol = reg.get("volatility_mean")
        bucket = _get_bucket(rd, cid) if cid != "—" else "—"
        if bucket == "exploit":
            exploit_wins += 1
        top3 = []
        for r in ranked[:3]:
            pid = r.get("patch_id") or "—"
            top3.append("%s(%s)" % (pid, _get_bucket(rd, pid)))
        vol_001 = "—"
        for r in ranked:
            if r.get("patch_id") == "volatility_0.001":
                vol_001 = "%.4f" % (r.get("regular_metrics") or {}).get("volatility_mean", 0)
                break
        rows.append((
            lb,
            "%.4f" % eg if eg is not None else "—",
            "%.4f" % vol if vol is not None else "—",
            "%s/%s" % (cid, bucket),
            ", ".join(top3),
            vol_001,
            "—",
        ))

    n = len(run_dirs)
    exploit_rate = exploit_wins / n if n else 0

    print("| run | champion_eg | champion_vol | champion_id/bucket | top3(bucket) | vol_001 | exploit_win_rate |")
    print("|-----|-------------|--------------|--------------------|--------------|---------|------------------|")
    for i, r in enumerate(rows):
        rr = list(r)
        rr[-1] = "%.2f" % exploit_rate if i == 0 else ""
        print("| %s | %s | %s | %s | %s | %s | %s |" % tuple(rr))

    eg_vals = [float(r[1]) for r in rows if r[1] != "—"]
    vol_vals = [float(r[2]) for r in rows if r[2] != "—"]
    eg_min = min(eg_vals) if eg_vals else 0
    vol_max = max(vol_vals) if vol_vals else 0
    print()
    print("B1 Gate: champion_eg>=4.0? %s  champion_vol<0.005? %s  exploit_win_rate>=2/3? %s" % (
        "PASS" if eg_min >= 4.0 else "FAIL",
        "PASS" if vol_max < 0.005 else "FAIL",
        "PASS" if exploit_rate >= 2 / 3 else "FAIL",
    ))


if __name__ == "__main__":
    main()
