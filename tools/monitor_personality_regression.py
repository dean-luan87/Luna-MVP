#!/usr/bin/env python3
"""
人格回归哨兵：固定 seeds/suites/n-candidates，跑 det=3，硬 Gate 不通过则 exit 1（CI 阻断）。

固定：seeds 42/123/777，pulse/sustain，regular 用 golden_regular_v3_50eps（若未构建先跑 tools/build_regular_suite_50eps.py），n-candidates 60。

Gate:
  champion_eg >= 4.10
  champion_vol <= 0.005
  high_risk_frames_total > 0
  guarded_frames_total > 0
  det=3 同 seed 内 hash 一致（由 tournament 内部校验）
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EG_MIN = 4.10
VOL_MAX = 0.005


def main() -> int:
    env = {
        "PYTHONHASHSEED": "0",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
    }
    out_root = ROOT / "outputs" / "d1_runs" / "personality_regression_sentinel"
    out_root.mkdir(parents=True, exist_ok=True)

    for seed in (42, 123, 777):
        cmd = [
            sys.executable,
            str(ROOT / "tools" / "run_d1_tournament.py"),
            "--dual-channel", "--determinism-check", "3",
            "--stress-base-patch", "patches/physics/stress_channel_phys_v1_conservative.json",
            "--stress-base-patch-responsive", "patches/physics/stress_channel_phys_v1_responsive.json",
            "--stress-suite-sustain", "library_store/v1.1/golden_stress_v2_powerclips_sustain",
            "--stress-suite-pulse", "library_store/v1.1/golden_stress_v2_powerclips_pulse",
            "--regular-suite", "library_store/v1.1/golden_regular_v3_50eps",
            "--n-candidates", "60", "--seed", str(seed),
            "--out-dir", str(out_root), "--mode", "recompute",
            "--phase3-mode", "convergent",
            "--converge-exploit-ratio", "0.85", "--converge-peak-hold-fixed", "3",
            "--converge-alpha-mean", "0.696", "--converge-alpha-std", "0.013",
            "--converge-alpha-min", "0.65", "--converge-alpha-max", "0.73",
            "--converge-decay-mean", "0.869", "--converge-decay-std", "0.004",
            "--converge-decay-min", "0.86", "--converge-decay-max", "0.88",
            "--converge-explore-alpha-min", "0.69", "--converge-explore-alpha-max", "0.72",
            "--converge-explore-decay-min", "0.865", "--converge-explore-decay-max", "0.885",
        ]
        r = subprocess.run(cmd, cwd=str(ROOT), env={**subprocess.os.environ, **env})
        if r.returncode != 0:
            print("[SENTINEL] tournament seed %s failed" % seed, file=sys.stderr)
            return 1

    run_dirs = sorted(
        [d for d in out_root.iterdir() if d.is_dir() and (d / "rank_report.json").is_file()],
        key=lambda p: p.name,
        reverse=True,
    )[:3]
    if len(run_dirs) < 3:
        print("[SENTINEL] expected 3 run dirs", file=sys.stderr)
        return 1

    rows = []
    for rd in run_dirs:
        d = json.loads((rd / "rank_report.json").read_text())
        ranked = d.get("ranked") or []
        champ = ranked[0] if ranked else {}
        ch = (d.get("channels") or {}).get("stress") or {}
        eg = (champ.get("stress_metrics") or {}).get("early_gain_weighted_mean")
        vol = (champ.get("regular_metrics") or {}).get("volatility_mean")
        hr = ch.get("high_risk_frames_total", 0)
        gtd = ch.get("guarded_frames_total", 0)
        cid = d.get("champion_id") or champ.get("patch_id")
        rows.append({"seed": (rd / "run_manifest.json").is_file() and json.loads((rd / "run_manifest.json").read_text()).get("seed") or rd.name, "champion_id": cid, "champion_eg": eg, "champion_vol": vol, "high_risk_frames_total": hr, "guarded_frames_total": gtd})

    print("| seed | champion_id | champion_eg | champion_vol | high_risk_frames_total | guarded_frames_total |")
    print("|------|-------------|--------------|--------------|------------------------|----------------------|")
    for r in rows:
        print("| %s | %s | %s | %s | %s | %s |" % (
            r["seed"], r["champion_id"],
            "%.4f" % r["champion_eg"] if r["champion_eg"] is not None else "—",
            "%.4f" % r["champion_vol"] if r["champion_vol"] is not None else "—",
            r["high_risk_frames_total"], r["guarded_frames_total"],
        ))

    fail = False
    for r in rows:
        eg = r["champion_eg"]
        if eg is None or float(eg) < EG_MIN:
            print("[SENTINEL] FAIL: champion_eg %.4f < %s" % (float(eg) if eg is not None else 0, EG_MIN), file=sys.stderr)
            fail = True
        vol = r["champion_vol"]
        if vol is not None and float(vol) > VOL_MAX:
            print("[SENTINEL] FAIL: champion_vol %.4f > %s" % (float(vol), VOL_MAX), file=sys.stderr)
            fail = True
        if int(r["high_risk_frames_total"] or 0) <= 0:
            print("[SENTINEL] FAIL: high_risk_frames_total <= 0", file=sys.stderr)
            fail = True
        if int(r["guarded_frames_total"] or 0) <= 0:
            print("[SENTINEL] FAIL: guarded_frames_total <= 0", file=sys.stderr)
            fail = True
    if fail:
        return 1
    print("[SENTINEL] all gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
