#!/usr/bin/env python3
"""
Step5 最小可行 nightly 回归：跑 3-seed，输出 KPI，触发 RED/YELLOW 报警。

输出: exploit_win_rate, champion_eg, champion_vol, top10 alpha_mean, guarded_ratio_delta
报警:
  RED: champion_eg < 4.0、champion_vol > 0.02、guarded_frames_total==0 或 eligible_early_gain_frames_total==0
  YELLOW: exploit_win_rate < 0.4（连续 3 天）

用法:
  python3 tools/run_d1_nightly_regression.py [--run-only] [run_dirs...]
  若指定 run_dirs 则直接汇总；否则先跑 step5_freeze 再汇总。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _get_eff_smoothing(run_dir: Path, patch_id: str) -> dict:
    for name in ("effective_patch.stress_responsive.json", "effective_patch.stress.json"):
        p = run_dir / patch_id / name
        if p.is_file():
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                return {"alpha": d.get("smoothing.alpha"), "bucket": (d.get("metadata") or {}).get("bucket")}
            except Exception:
                pass
    return {}


def main() -> None:
    ap = argparse.ArgumentParser(description="Step5 nightly 回归：KPI + RED/YELLOW")
    ap.add_argument("run_dirs", nargs="*", type=Path, help="已完成 run 目录，空则先跑 step5_freeze")
    ap.add_argument("--run-only", action="store_true", help="仅跑 tournament，不汇总")
    ap.add_argument("--labels", nargs="+", default=["seed42", "seed123", "seed777"])
    args = ap.parse_args()

    run_dirs = [Path(p).resolve() for p in args.run_dirs]
    if not run_dirs:
        cmd = ["bash", str(ROOT / "tools" / "run_d1_step5_freeze_seeds.sh"), "all"]
        subprocess.run(cmd, cwd=str(ROOT), check=True)
        base = ROOT / "outputs" / "d1_runs" / "phase3_step5_freeze"
        run_dirs = sorted(base.iterdir()) if base.is_dir() else []
        run_dirs = [d for d in run_dirs if d.is_dir() and (d / "rank_report.json").is_file()]
        run_dirs = run_dirs[-3:]  # 最新 3 个

    if not run_dirs:
        print("ERROR: no run dirs", file=sys.stderr)
        sys.exit(1)

    if args.run_only:
        return

    labels = args.labels[: len(run_dirs)]
    exploit_wins = 0
    eg_list = []
    vol_list = []
    alpha_list = []
    gr_delta_list = []

    for run_dir, label in zip(run_dirs, labels):
        rp = run_dir / "rank_report.json"
        if not rp.is_file():
            continue
        data = json.loads(rp.read_text(encoding="utf-8"))
        ranked = data.get("ranked") or []
        champ_id = data.get("champion_id") or (ranked[0].get("patch_id") if ranked else None)
        champ = next((r for r in ranked if r.get("patch_id") == champ_id), ranked[0] if ranked else {})
        reg = champ.get("regular_metrics") or {}
        stress = champ.get("stress_metrics") or {}
        eg = stress.get("early_gain_weighted_mean")
        vol = reg.get("volatility_mean")
        gr = reg.get("guarded_ratio_delta_mean")
        if eg is not None:
            eg_list.append(float(eg))
        if vol is not None:
            vol_list.append(float(vol))
        if gr is not None:
            gr_delta_list.append(float(gr))
        eff = _get_eff_smoothing(run_dir, champ_id) if champ_id else {}
        b = eff.get("bucket")
        if b == "exploit":
            exploit_wins += 1
        for r in ranked[:10]:
            effr = _get_eff_smoothing(run_dir, r.get("patch_id") or "")
            a = effr.get("alpha")
            if a is not None:
                alpha_list.append(float(a))

    n = len(run_dirs)
    exploit_rate = exploit_wins / n if n else 0
    eg_min = min(eg_list) if eg_list else 0
    vol_max = max(vol_list) if vol_list else 0
    alpha_mean = sum(alpha_list) / len(alpha_list) if alpha_list else 0
    gr_mean = sum(gr_delta_list) / len(gr_delta_list) if gr_delta_list else 0

    print("exploit_win_rate: %.2f" % exploit_rate)
    print("champion_eg: min=%.4f" % eg_min)
    print("champion_vol: max=%.4f" % vol_max)
    print("top10_alpha_mean: %.4f" % alpha_mean)
    print("guarded_ratio_delta_mean: %.4f" % gr_mean)

    ch_stress = {}
    for run_dir in run_dirs:
        rp = run_dir / "rank_report.json"
        if rp.is_file():
            d = json.loads(rp.read_text(encoding="utf-8"))
            ch = (d.get("channels") or {}).get("stress") or {}
            if ch:
                ch_stress = ch
                break
    eligible_hr = ch_stress.get("high_risk_frames_total") or 0
    guarded_total = ch_stress.get("guarded_frames_total") or 0

    red = False
    yellow = False
    if eg_min < 4.0:
        print("RED: champion_eg < 4.0", file=sys.stderr)
        red = True
    if vol_max > 0.02:
        print("RED: champion_vol > 0.02", file=sys.stderr)
        red = True
    if eligible_hr == 0:
        print("RED: eligible_early_gain_frames_total == 0", file=sys.stderr)
        red = True
    if guarded_total == 0:
        print("RED: guarded_frames_total == 0", file=sys.stderr)
        red = True
    if exploit_rate < 0.4:
        print("YELLOW: exploit_win_rate < 0.4 (连续3天需人工核查)", file=sys.stderr)
        yellow = True

    if red:
        sys.exit(2)
    if yellow:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
