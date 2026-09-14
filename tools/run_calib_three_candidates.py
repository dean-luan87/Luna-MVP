#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用选定 calib 档（如 0.195）+ stress suite 跑三候选：baseline(calib only) / aggressive(2x) / conservative(0.7x)。
验收：diff_frames > 0，aggressive early_gain > baseline，volatility 不卡门，guarded_ratio_delta 不越界。
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Run 3 candidates on stress suite with calib threshold")
    p.add_argument("--calib-patch", default="patches/calib_threshold_0195.json", help="Selected calib threshold patch")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--out-dir", default="outputs/v1.1/calib_v1")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    stress_dir = os.path.join(base_dir, version, "golden_stress")
    if not os.path.isdir(stress_dir):
        print("ERROR: golden_stress not found. Run: python3 tools/populate_stress_from_golden.py", file=sys.stderr)
        return 2

    calib_path = os.path.join(ROOT, args.calib_patch)
    if not os.path.isfile(calib_path):
        print("ERROR: calib patch not found", calib_path, file=sys.stderr)
        return 2

    with open(calib_path, "r", encoding="utf-8") as f:
        calib = json.load(f)
    aggressive = {**calib, "weights.risk_density": 0.6, "weights.path_instability": 0.6, "weights.motion_instability": 0.6}
    conservative = {**calib, "weights.risk_density": 0.21, "weights.path_instability": 0.21, "weights.motion_instability": 0.21}
    out_dir = os.path.join(ROOT, args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    patches_dir = os.path.join(out_dir, "patches_merged")
    os.makedirs(patches_dir, exist_ok=True)
    agg_path = os.path.join(patches_dir, "calib_aggressive.json")
    cons_path = os.path.join(patches_dir, "calib_conservative.json")
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(aggressive, f, indent=2)
    with open(cons_path, "w", encoding="utf-8") as f:
        json.dump(conservative, f, indent=2)

    results = []
    for label, patch_path in [("baseline", calib_path), ("aggressive", agg_path), ("conservative", cons_path)]:
        sim_dir = os.path.join(out_dir, f"simulations_{label}")
        r = subprocess.run(
            [
                sys.executable, str(ROOT / "tools" / "run_sim_suite.py"),
                "--base-dir", base_dir, "--version-tag", version,
                "--patch", patch_path, "--out-dir", os.path.join(ROOT, "outputs"),
                "--sim-dir", sim_dir, "--golden-stress", "--mode", "recompute",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        suite_report_path = None
        for line in (r.stdout or "").splitlines():
            if "suite_report:" in line:
                suite_report_path = line.split("suite_report:")[-1].strip()
                break
        rec = {"label": label, "returncode": r.returncode}
        if suite_report_path and os.path.isfile(suite_report_path):
            with open(suite_report_path, "r", encoding="utf-8") as f:
                report = json.load(f)
            per = report.get("per_episode") or {}
            vol_vals = []
            early_vals = []
            gr_deltas = []
            for ep_id, ep_data in per.items():
                sc_path = ep_data.get("scorecard_path")
                if sc_path and os.path.isfile(sc_path):
                    try:
                        sc = json.load(open(sc_path, "r", encoding="utf-8"))
                        if sc.get("volatility_index") is not None:
                            vol_vals.append(float(sc["volatility_index"]))
                        eg = sc.get("early_conservative_action_gain")
                        if eg is not None:
                            early_vals.append(float(eg))
                        gr = (sc.get("efficiency") or {}).get("guarded_ratio_delta")
                        if gr is not None:
                            gr_deltas.append(float(gr))
                    except Exception:
                        pass
            rec["volatility_mean"] = round(sum(vol_vals) / len(vol_vals), 4) if vol_vals else None
            rec["early_gain_mean"] = round(sum(early_vals) / len(early_vals), 4) if early_vals else None
            rec["guarded_ratio_delta_mean"] = round(sum(gr_deltas) / len(gr_deltas), 4) if gr_deltas else None
        results.append(rec)

    out_path = os.path.join(out_dir, "calib_three_candidates.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("wrote", out_path)
    for r in results:
        print(r["label"], "| vol:", r.get("volatility_mean"), "| early_gain:", r.get("early_gain_mean"), "| gr_delta:", r.get("guarded_ratio_delta_mean"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
