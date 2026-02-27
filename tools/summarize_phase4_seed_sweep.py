#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汇总 Phase4 seed sweep 下各 run_dir 的 health_report.json，输出「每个 seed × 每档 λ」的 gate 指标对比表，
以及可选统计（均值/方差/p95）。输入为 sweep 根目录或若干 lam 子目录。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]


def _find_run_dirs(sweep_root: Path) -> List[Tuple[str, str, Path]]:
    """返回 [(lam_str, seed_str, run_dir), ...]，按 lam 再 seed 排序。"""
    out: List[Tuple[str, str, Path]] = []
    sweep_root = Path(sweep_root).resolve()
    if not sweep_root.is_dir():
        return out
    for lam_dir in sorted(sweep_root.iterdir()):
        if not lam_dir.is_dir() or not lam_dir.name.startswith("lam_"):
            continue
        lam_str = lam_dir.name.replace("lam_", "")
        for seed_dir in sorted(lam_dir.iterdir()):
            if not seed_dir.is_dir() or not seed_dir.name.startswith("seed_"):
                continue
            rp = seed_dir / "rank_report.json"
            if rp.is_file():
                seed_str = seed_dir.name.replace("seed_", "")
                out.append((lam_str, seed_str, seed_dir))
    return out


def _read_health(run_dir: Path) -> Optional[Dict[str, Any]]:
    hp = run_dir / "health_report.json"
    if not hp.is_file():
        return None
    try:
        return json.loads(hp.read_text(encoding="utf-8"))
    except Exception:
        return None


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="汇总 Phase4 seed sweep 的 health 报告")
    ap.add_argument("dirs", nargs="*", type=Path,
                    help="Sweep 根目录或若干 lam 父目录，默认 outputs/d1_runs/phase4_seed_sweep")
    ap.add_argument("--stats", action="store_true", help="输出均值/方差/p95")
    ap.add_argument("--run-monitor", action="store_true", help="对缺少 health_report 的 run_dir 先跑 monitor")
    args = ap.parse_args()

    # 解析输入：若给的是 sweep 根则用；若给的是 lam_0.10 等则把父目录当 sweep 根
    dirs = args.dirs if args.dirs else [ROOT / "outputs/d1_runs/phase4_seed_sweep"]
    run_entries: List[Tuple[str, str, Path]] = []
    seen: set = set()
    for d in dirs:
        d = Path(d).resolve()
        if not d.is_dir():
            continue
        if d.name.startswith("lam_"):
            sweep_root = d.parent
            entries = _find_run_dirs(sweep_root)
        else:
            entries = _find_run_dirs(d)
        for e in entries:
            key = (e[0], e[1])
            if key not in seen:
                seen.add(key)
                run_entries.append(e)
    run_entries.sort(key=lambda x: (x[0], x[1]))

    if args.run_monitor:
        import subprocess
        for _lam, _seed, run_dir in run_entries:
            if (run_dir / "health_report.json").is_file():
                continue
            if (run_dir / "rank_report.json").is_file():
                subprocess.run([sys.executable, str(ROOT / "tools/monitor_personality_health.py"), str(run_dir)], check=False)

    rows: List[Dict[str, Any]] = []
    for lam_str, seed_str, run_dir in run_entries:
        h = _read_health(run_dir)
        if h is None:
            rows.append({
                "lam": lam_str, "seed": seed_str,
                "overall": "—", "eg": None, "overreact_rate": None, "miss_rate": None, "champion_vol": None,
                "determinism_pass": None,
            })
            continue
        eg = h.get("stress", {}).get("early_gain_mean")
        rows.append({
            "lam": lam_str,
            "seed": seed_str,
            "overall": h.get("overall", "PASS" if all((h.get("gates") or {}).values()) else "FAIL"),
            "eg": round(float(eg), 4) if eg is not None else None,
            "overreact_rate": h.get("overreact_rate"),
            "miss_rate": h.get("miss_rate"),
            "champion_vol": round(float(h["champion_vol"]), 4) if h.get("champion_vol") is not None else None,
            "determinism_pass": h.get("determinism_pass"),
        })

    # 表：每个 seed × 两档 λ（或所有出现的 lam）
    lams = sorted({r["lam"] for r in rows})
    seeds = sorted({r["seed"] for r in rows}, key=int)
    print("=== Phase4 seed sweep: gate 指标对比 ===\n")
    print("%-8s" % "seed", end="")
    for lam in lams:
        print("  %-6s %-4s %-8s %-12s %-6s %-8s" % ("lam", "overall", "eg", "overreact", "miss", "vol"), end="")
    print()
    print("-" * (8 + len(lams) * (6 + 4 + 8 + 12 + 6 + 8 + 2)))

    for seed in seeds:
        print("%-8s" % seed, end="")
        for lam in lams:
            r = next((x for x in rows if x["lam"] == lam and x["seed"] == seed), None)
            if r is None:
                print("  %-6s %-4s %-8s %-12s %-6s %-8s" % (lam, "—", "—", "—", "—", "—"), end="")
            else:
                eg_s = str(r["eg"]) if r["eg"] is not None else "—"
                over_s = str(r["overreact_rate"]) if r["overreact_rate"] is not None else "—"
                miss_s = str(r["miss_rate"]) if r["miss_rate"] is not None else "—"
                vol_s = str(r["champion_vol"]) if r["champion_vol"] is not None else "—"
                print("  %-6s %-4s %-8s %-12s %-6s %-8s" % (lam, r["overall"], eg_s, over_s, miss_s, vol_s), end="")
        print()

    if args.stats and rows:
        print("\n=== 按 λ 汇总（均值 / 方差 / p95）===")
        for lam in lams:
            sub = [r for r in rows if r["lam"] == lam and r["eg"] is not None]
            if not sub:
                print("lam=%s: no numeric data" % lam)
                continue
            eg_vals = [r["eg"] for r in sub]
            over_vals = [r["overreact_rate"] for r in sub if r["overreact_rate"] is not None]
            vol_vals = [r["champion_vol"] for r in sub if r["champion_vol"] is not None]

            def p95(x: List[float]) -> float:
                if not x:
                    return float("nan")
                x = sorted(x)
                i = max(0, int(len(x) * 0.95) - 1)
                return x[i]

            def mean_var(x: List[float]) -> Tuple[float, float]:
                if not x:
                    return float("nan"), float("nan")
                m = sum(x) / len(x)
                v = sum((t - m) ** 2 for t in x) / len(x)
                return m, v

            m_eg, v_eg = mean_var(eg_vals)
            m_over, v_over = (mean_var(over_vals) if over_vals else (float("nan"), float("nan")))
            m_vol, v_vol = (mean_var(vol_vals) if vol_vals else (float("nan"), float("nan")))
            print("lam=%s: eg mean=%.4f var=%.4f p95=%.4f | overreact mean=%.4f var=%.4f p95=%.4f | vol mean=%.4f p95=%.4f" % (
                lam, m_eg, v_eg, p95(eg_vals),
                m_over, v_over, p95(over_vals) if over_vals else float("nan"),
                m_vol, p95(vol_vals) if vol_vals else float("nan"),
            ))
    return 0


if __name__ == "__main__":
    sys.exit(main())
