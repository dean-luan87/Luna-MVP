#!/usr/bin/env python3
"""
Step5-A 工业级冻结验收：输出 4 项指标 + 判据，不要求 champion_id 一致。

每 seed 验证：
  1. champion_eg ≥ 4.1617
  2. champion_vol < 0.005
  3. eligible_early_gain_frames_total > 0 (high_risk_frames_total)
  4. guarded_frames_total > 0

用法:
  python3 tools/run_d1_freeze_verify.py \\
    outputs/d1_runs/phase3_step5_freeze/<run1> \\
    outputs/d1_runs/phase3_step5_freeze/<run2> \\
    outputs/d1_runs/phase3_step5_freeze/<run3> \\
    --labels seed42 seed123 seed777
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="Step5-A 冻结验收：4 项指标 + 判据")
    ap.add_argument("run_dirs", nargs="+", type=Path)
    ap.add_argument("--labels", nargs="+", default=None)
    args = ap.parse_args()

    run_dirs = [Path(p).resolve() for p in args.run_dirs]
    labels = args.labels or [d.name for d in run_dirs]
    if len(labels) != len(run_dirs):
        labels = [d.name for d in run_dirs]

    rows = []
    for run_dir, label in zip(run_dirs, labels):
        rp = run_dir / "rank_report.json"
        if not rp.is_file():
            rows.append((label, "MISSING", "—", "—", "—", "—", "—"))
            continue
        data = json.load(f := open(rp))
        f.close()
        ranked = data.get("ranked") or []
        champ = ranked[0] if ranked else {}
        ch_stress = (data.get("channels") or {}).get("stress") or {}
        reg = champ.get("regular_metrics") or {}
        stress_m = champ.get("stress_metrics") or {}
        eg = stress_m.get("early_gain_weighted_mean")
        vol = reg.get("volatility_mean")
        eg_s = f"{eg:.4f}" if eg is not None else "—"
        vol_s = f"{vol:.4f}" if vol is not None else "—"
        hr = ch_stress.get("high_risk_frames_total")
        gtd = ch_stress.get("guarded_frames_total")
        hr_s = str(hr) if hr is not None else "—"
        gtd_s = str(gtd) if gtd is not None else "—"
        cid = data.get("champion_id") or champ.get("patch_id") or "—"
        rows.append((label, cid, eg_s, vol_s, hr_s, gtd_s, data.get("run_status") or "OK"))

    print("| run | champion_id | champion_eg | champion_vol | high_risk_frames_total | guarded_frames_total | run_status |")
    print("|-----|-------------|-------------|--------------|------------------------|----------------------|------------|")
    for row in rows:
        print("| %s | %s | %s | %s | %s | %s | %s |" % row)

    # 判据
    eg_ok = sum(1 for r in rows if r[2] != "—" and float(r[2]) >= 4.1617)
    vol_ok = sum(1 for r in rows if r[3] != "—" and float(r[3]) < 0.005)
    hr_ok = sum(1 for r in rows if r[4] != "—" and int(r[4]) > 0)
    gtd_ok = sum(1 for r in rows if r[5] != "—" and int(r[5]) > 0)
    n = len(run_dirs)

    print()
    print("## 验收判据")
    print("champion_eg >= 4.1617:  %d/%d  %s" % (eg_ok, n, "PASS" if eg_ok == n else "FAIL"))
    print("champion_vol < 0.005:   %d/%d  %s" % (vol_ok, n, "PASS" if vol_ok == n else "FAIL"))
    print("high_risk_frames > 0:   %d/%d  %s" % (hr_ok, n, "PASS" if hr_ok == n else "FAIL"))
    print("guarded_frames_total>0: %d/%d  %s" % (gtd_ok, n, "PASS" if gtd_ok == n else "FAIL"))
    if eg_ok == n and vol_ok == n and hr_ok == n and gtd_ok == n:
        print()
        print("PHASE3_PRODUCTION_RECIPE_v1 冻结成功")


if __name__ == "__main__":
    main()
