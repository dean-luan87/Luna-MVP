#!/usr/bin/env python3
"""
从多个 phase3 run 中抽取「种子稳定性验证」指标 + Top3 + 盆地统计，
用于 Step3 验收（A/B/C 判定）。

用法:
  python3 tools/run_d1_seed_stability_summary.py \\
    outputs/d1_runs/phase3_step3_gradualshift/<run1> ... \\
    --labels seed42 seed123 seed777 seed888 seed2024 --topk 10

输出: champion_id, champion_bucket, champion_vol, champion_eg, top3, top3_buckets,
      top10 alpha/decay mean/std, exploit_win_rate。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _get_eff_smoothing(run_dir: Path, patch_id: str) -> Dict[str, Any]:
    """从 effective_patch 取 alpha/decay/bucket。"""
    for name in ("effective_patch.stress_responsive.json", "effective_patch.stress.json"):
        p = run_dir / patch_id / name
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                bucket = (d.get("metadata") or {}).get("bucket")
                return {
                    "alpha": d.get("smoothing.alpha"),
                    "peak_decay": d.get("smoothing.peak_decay"),
                    "bucket": bucket,
                }
            except Exception:
                pass
    return {}


def _infer_bucket(patch_id: str, eff: Dict[str, Any]) -> str:
    """推断 bucket：conservative/baseline 优先，否则用 metadata.bucket。"""
    if patch_id == "conservative":
        return "conservative"
    if patch_id == "baseline":
        return "baseline"
    b = eff.get("bucket")
    if b:
        return str(b)
    return "—"


def _vol(r: dict) -> str:
    reg = (r.get("regular_metrics") or {})
    v = reg.get("volatility_mean")
    if v is None:
        return "—"
    return f"{v:.4f}"


def _eg_val(r: dict) -> Optional[float]:
    stress = (r.get("stress_metrics") or r.get("aggregated") or {})
    return stress.get("early_gain_weighted_mean")


def _eg(r: dict) -> str:
    v = _eg_val(r)
    if v is None:
        return "—"
    return f"{v:.4f}"


def main() -> None:
    ap = argparse.ArgumentParser(description="D1 seed stability: champion/bucket/top3/top10/exploit_win_rate")
    ap.add_argument("run_dirs", nargs="+", type=Path, help="rank_report.json 所在 run 目录")
    ap.add_argument("--labels", nargs="+", default=None, help="每行标签")
    ap.add_argument("--topk", type=int, default=10, help="TopK 盆地统计")
    args = ap.parse_args()

    run_dirs = [Path(p).resolve() for p in args.run_dirs]
    labels = args.labels or [d.name for d in run_dirs]
    if len(labels) != len(run_dirs):
        labels = [d.name for d in run_dirs]

    rows: List[Tuple[Any, ...]] = []
    champion_buckets: List[str] = []
    all_alphas: List[float] = []
    all_decays: List[float] = []

    for run_dir, label in zip(run_dirs, labels):
        rank_path = run_dir / "rank_report.json"
        if not rank_path.is_file():
            rows.append((label, "MISSING", "—", "—", "—", "—", "—", "—"))
            champion_buckets.append("—")
            continue
        with open(rank_path) as f:
            data = json.load(f)
        ranked = data.get("ranked") or []
        champion_id = data.get("champion_id") or "—"
        by_id = {r["patch_id"]: r for r in ranked}
        champ = by_id.get(champion_id, {})
        r001 = by_id.get("d1_candidate_001", {})
        r022 = by_id.get("d1_candidate_022", {})
        top3 = ", ".join((r.get("patch_id") or "") for r in ranked[:3])

        # champion_bucket
        eff_champ = _get_eff_smoothing(run_dir, champion_id) if champion_id != "—" else {}
        champ_bucket = _infer_bucket(champion_id, eff_champ) if champion_id != "—" else "—"
        champion_buckets.append(champ_bucket)

        # top3_buckets
        top3_buckets: List[str] = []
        for r in ranked[:3]:
            pid = r.get("patch_id") or ""
            eff = _get_eff_smoothing(run_dir, pid)
            top3_buckets.append(_infer_bucket(pid, eff))
        top3_buckets_s = ", ".join(top3_buckets)

        # top10 alpha/decay
        topk = ranked[: args.topk]
        alphas: List[float] = []
        decays: List[float] = []
        for r in topk:
            pid = r.get("patch_id") or ""
            eff = _get_eff_smoothing(run_dir, pid)
            a = eff.get("alpha")
            d = eff.get("peak_decay")
            if a is not None:
                alphas.append(float(a))
            if d is not None:
                decays.append(float(d))
        all_alphas.extend(alphas)
        all_decays.extend(decays)

        a_mean = sum(alphas) / len(alphas) if alphas else 0
        a_std = (sum((x - a_mean) ** 2 for x in alphas) / len(alphas)) ** 0.5 if len(alphas) > 1 else 0
        d_mean = sum(decays) / len(decays) if decays else 0
        d_std = (sum((x - d_mean) ** 2 for x in decays) / len(decays)) ** 0.5 if len(decays) > 1 else 0
        top10_s = f"α{a_mean:.3f}±{a_std:.3f} δ{d_mean:.3f}±{d_std:.3f}" if alphas else "—"

        rows.append((
            label,
            champion_id,
            champ_bucket,
            _vol(champ),
            _eg(champ),
            top3,
            top3_buckets_s,
            top10_s,
        ))

    # 表 1：主表
    print("| run | champion_id | champion_bucket | champion_vol | champion_eg | top3 | top3_buckets | top10_αδ |")
    print("|-----|-------------|-----------------|--------------|-------------|------|--------------|----------|")
    for row in rows:
        print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(*row))

    # 表 2：盆地统计 + exploit_win_rate
    n = len(run_dirs)
    exploit_wins = sum(1 for b in champion_buckets if b == "exploit")
    eg_high = sum(1 for row in rows if row[4] != "—" and row[4] != "MISSING" and float(row[4]) >= 4.1617)
    vols = []
    for row in rows:
        v = row[3]
        if v != "—" and v != "MISSING":
            try:
                vols.append(float(v))
            except ValueError:
                pass
    vol_p95 = sorted(vols)[min(len(vols) - 1, int(len(vols) * 0.95))] if vols else 0

    print()
    print("## 盆地统计 (merged Top%d across runs)" % args.topk)
    if all_alphas:
        a_m = sum(all_alphas) / len(all_alphas)
        a_s = (sum((x - a_m) ** 2 for x in all_alphas) / len(all_alphas)) ** 0.5
        d_m = sum(all_decays) / len(all_decays)
        d_s = (sum((x - d_m) ** 2 for x in all_decays) / len(all_decays)) ** 0.5
        print("alpha: mean=%.4f std=%.4f  decay: mean=%.4f std=%.4f" % (a_m, a_s, d_m, d_s))
    else:
        print("alpha/decay: no data")
    print()
    print("## 验收指标")
    print("exploit_win_rate: %d/%d" % (exploit_wins, n))
    print("champion_eg>=4.1617 count: %d/%d" % (eg_high, n))
    if vols:
        print("champion_vol p95: %.4f" % vol_p95)
    print()
    print("## A/B/C 判定 (参考 docs/PHASE3_BASELINE_WINS_DIAGNOSIS.md Step3)")
