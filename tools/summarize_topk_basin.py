#!/usr/bin/env python3
"""
跨 run 的 TopK 参数盆地对齐：用「参数盆地稳定」替代「patch_id 重合」判定收敛。
从 rank_report.json + effective_patch.stress_responsive.json 抓 TopK 的 alpha/decay，
输出每个 run 的 TopK 表 + 合并后的 alpha/decay 区间统计。

用法:
  python3 tools/summarize_topk_basin.py \\
    outputs/d1_runs/phase3_convergent/20260224020809 \\
    outputs/d1_runs/phase3_convergent/20260224021402 \\
    outputs/d1_runs/phase3_convergent/20260224021720 \\
    --topk 10 --out outputs/d1_runs/phase3_convergent/basin_summary.json

判据：若三次 run 的 Top10 落在同一小区间（alpha [0.62,0.66], decay [0.885,0.905]），
视为形成吸引子；若区间漂移大，再调 exploit_ratio/方差。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _get_eff_smoothing(run_dir: Path, patch_id: str) -> Dict[str, Any]:
    """从 effective_patch.stress_responsive.json 取 alpha/peak_decay/peak_hold；若无则从 stress.json。"""
    for name in ("effective_patch.stress_responsive.json", "effective_patch.stress.json"):
        p = run_dir / patch_id / name
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                return {
                    "alpha": d.get("smoothing.alpha"),
                    "peak_decay": d.get("smoothing.peak_decay"),
                    "peak_hold_frames": d.get("smoothing.peak_hold_frames"),
                    "bucket": (d.get("metadata") or {}).get("bucket"),
                }
            except Exception:
                pass
    return {}


def main() -> None:
    ap = argparse.ArgumentParser(description="TopK 参数盆地对齐：alpha/decay 区间统计")
    ap.add_argument("run_dirs", nargs="+", type=Path)
    ap.add_argument("--topk", type=int, default=10)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--labels", nargs="+", default=None)
    args = ap.parse_args()

    run_dirs = [Path(p).resolve() for p in args.run_dirs]
    labels = args.labels or [d.name for d in run_dirs]
    if len(labels) != len(run_dirs):
        labels = [d.name for d in run_dirs]

    per_run: List[Dict[str, Any]] = []
    all_alphas: List[float] = []
    all_decays: List[float] = []
    all_buckets: List[str] = []

    for run_dir, label in zip(run_dirs, labels):
        rp = run_dir / "rank_report.json"
        if not rp.is_file():
            per_run.append({"label": label, "rows": [], "error": "rank_report.json not found"})
            continue
        data = json.loads(rp.read_text(encoding="utf-8"))
        ranked = (data.get("ranked") or [])[: args.topk]
        rows: List[Dict[str, Any]] = []
        for r in ranked:
            pid = r.get("patch_id") or ""
            stress = r.get("stress_metrics") or {}
            reg = r.get("regular_metrics") or {}
            eg = stress.get("early_gain_weighted_mean")
            vol = reg.get("volatility_mean")
            eff = _get_eff_smoothing(run_dir, pid)
            alpha = eff.get("alpha")
            decay = eff.get("peak_decay")
            hold = eff.get("peak_hold_frames")
            bucket = eff.get("bucket")
            rows.append({
                "patch_id": pid,
                "early_gain": eg,
                "volatility": vol,
                "alpha": alpha,
                "peak_decay": decay,
                "peak_hold_frames": hold,
                "bucket": bucket,
            })
            if alpha is not None:
                all_alphas.append(float(alpha))
            if decay is not None:
                all_decays.append(float(decay))
            if bucket:
                all_buckets.append(str(bucket))
        per_run.append({"label": label, "rows": rows})

    # 合并统计
    def _stats(vals: List[float]) -> Dict[str, float]:
        if not vals:
            return {"min": 0, "max": 0, "mean": 0, "std": 0}
        n = len(vals)
        mean = sum(vals) / n
        var = sum((x - mean) ** 2 for x in vals) / n
        return {
            "min": round(min(vals), 4),
            "max": round(max(vals), 4),
            "mean": round(mean, 4),
            "std": round(var ** 0.5, 4),
        }

    basin_stats = {
        "alpha": _stats(all_alphas),
        "peak_decay": _stats(all_decays),
        "bucket_exploit": all_buckets.count("exploit"),
        "bucket_explore": all_buckets.count("explore"),
    }

    out_data: Dict[str, Any] = {
        "per_run": per_run,
        "basin_stats": basin_stats,
    }

    # 打印到 stdout
    print("## Per-run Top%d\n" % args.topk)
    for pr in per_run:
        print("### %s" % pr["label"])
        if pr.get("error"):
            print(pr["error"])
            continue
        print("| patch_id | early_gain | vol | alpha | peak_decay | bucket |")
        print("|----------|------------|-----|-------|------------|--------|")
        for row in pr["rows"]:
            eg = row.get("early_gain")
            eg_s = "%.4f" % eg if eg is not None else "—"
            vol = row.get("volatility")
            vol_s = "%.4f" % vol if vol is not None else "—"
            a = row.get("alpha")
            a_s = "%.4f" % a if a is not None else "—"
            d = row.get("peak_decay")
            d_s = "%.4f" % d if d is not None else "—"
            b = row.get("bucket") or "—"
            print("| %s | %s | %s | %s | %s | %s |" % (row["patch_id"], eg_s, vol_s, a_s, d_s, b))
        print()

    print("## Basin stats (merged Top%d across all runs)\n" % args.topk)
    print("alpha:  min=%.4f max=%.4f mean=%.4f std=%.4f" % (
        basin_stats["alpha"]["min"], basin_stats["alpha"]["max"],
        basin_stats["alpha"]["mean"], basin_stats["alpha"]["std"]))
    print("decay:  min=%.4f max=%.4f mean=%.4f std=%.4f" % (
        basin_stats["peak_decay"]["min"], basin_stats["peak_decay"]["max"],
        basin_stats["peak_decay"]["mean"], basin_stats["peak_decay"]["std"]))
    print("bucket: exploit=%d explore=%d" % (basin_stats["bucket_exploit"], basin_stats["bucket_explore"]))

    if args.out:
        args.out = Path(args.out)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print("\n[D1] basin summary written:", args.out)


if __name__ == "__main__":
    main()
