#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对三档 calib 阈值 patch 在 stress suite 上跑四指标验收：
near_threshold_ratio, max_consecutive_near_frames, volatility_delta_vs_baseline, (blind_patch 仍 FAIL)。
结果写 outputs/v1.1/calib_v1/calib_three_tiers.json。
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CALIB_PATCHES = [
    ("0.21", "patches/calib_threshold_021.json", 0.21),
    ("0.195", "patches/calib_threshold_0195.json", 0.195),
    ("0.19", "patches/calib_threshold_019.json", 0.19),
]


def _load_jsonl(path):
    out = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _compute_near_metrics(rows, safe_to_caution):
    """near_threshold_ratio, max_consecutive_near_frames."""
    threshold_90 = 0.9 * safe_to_caution
    total = len(rows)
    near = [1 if float(r.get("weighted_sum_before_clamp", 0)) >= threshold_90 else 0 for r in rows]
    near_count = sum(near)
    ratio = near_count / total if total else 0.0
    # max consecutive near
    best = 0
    cur = 0
    for x in near:
        if x:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return ratio, best


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Run calib 3 tiers on stress suite, output 4 metrics")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--out-dir", default="outputs/v1.1/calib_v1")
    p.add_argument("--skip-suite", action="store_true", help="Only compute near_* from risk_debug (no sim suite)")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    stress_dir = os.path.join(base_dir, version, "golden_stress")
    if not os.path.isdir(stress_dir):
        print("ERROR: golden_stress not found. Run: python3 tools/populate_stress_from_golden.py", file=sys.stderr)
        return 2

    out_dir = os.path.join(ROOT, args.out_dir)
    os.makedirs(out_dir, exist_ok=True)
    logs_dir = os.path.join(ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    results = []
    baseline_volatility_mean = None
    # 先跑 baseline (empty) 取 volatility
    if not args.skip_suite:
        empty_patch = os.path.join(ROOT, "patches", "empty_patch.json")
        sim_dir_baseline = os.path.join(out_dir, "simulations_calib_baseline")
        r = subprocess.run(
            [
                sys.executable, str(ROOT / "tools" / "run_sim_suite.py"),
                "--base-dir", base_dir, "--version-tag", version,
                "--patch", empty_patch, "--out-dir", os.path.join(ROOT, "outputs"),
                "--sim-dir", sim_dir_baseline, "--golden-stress", "--mode", "recompute",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        for line in (r.stdout or "").splitlines():
            if "suite_report:" in line:
                suite_report_path = line.split("suite_report:")[-1].strip()
                if os.path.isfile(suite_report_path):
                    with open(suite_report_path, "r", encoding="utf-8") as f:
                        report = json.load(f)
                    per = report.get("per_episode") or {}
                    vol_vals = []
                    for ep_id, ep_data in per.items():
                        sc_path = ep_data.get("scorecard_path")
                        if sc_path and os.path.isfile(sc_path):
                            try:
                                sc = json.load(open(sc_path, "r", encoding="utf-8"))
                                v = sc.get("volatility_index")
                                if v is not None:
                                    vol_vals.append(float(v))
                            except Exception:
                                pass
                    if vol_vals:
                        baseline_volatility_mean = sum(vol_vals) / len(vol_vals)
                break

    for label, patch_rel, safe_to_caution in CALIB_PATCHES:
        patch_path = os.path.join(ROOT, patch_rel)
        if not os.path.isfile(patch_path):
            print("WARN: patch not found", patch_path, file=sys.stderr)
            continue
        debug_out = os.path.join(logs_dir, f"risk_debug_calib_{label.replace('.', '')}.jsonl")
        if os.path.isfile(debug_out):
            os.remove(debug_out)
        subprocess.run(
            [
                sys.executable, str(ROOT / "tools" / "record_risk_debug.py"),
                "--golden-stress", "--base-dir", base_dir, "--version-tag", version,
                "--out", debug_out,
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        rows = _load_jsonl(debug_out)
        near_ratio, max_consec_near = _compute_near_metrics(rows, safe_to_caution)

        vol_mean = None
        if not args.skip_suite:
            sim_dir = os.path.join(out_dir, f"simulations_calib_{label.replace('.', '')}")
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
            if r.returncode not in (0, 2):
                print("WARN: run_sim_suite failed for", label, r.stderr[:500], file=sys.stderr)
            # 从 suite_report 读 volatility（需解析 stdout 或读 suite_report 文件）
            suite_report_path = None
            for line in (r.stdout or "").splitlines():
                if "suite_report:" in line:
                    suite_report_path = line.split("suite_report:")[-1].strip()
                    break
            if suite_report_path and os.path.isfile(suite_report_path):
                with open(suite_report_path, "r", encoding="utf-8") as f:
                    report = json.load(f)
                per = report.get("per_episode") or {}
                vol_vals = []
                for ep_id, ep_data in per.items():
                    sc_path = ep_data.get("scorecard_path")
                    if sc_path and os.path.isfile(sc_path):
                        try:
                            sc = json.load(open(sc_path, "r", encoding="utf-8"))
                            v = sc.get("volatility_index")
                            if v is not None:
                                vol_vals.append(float(v))
                        except Exception:
                            pass
                vol_mean = sum(vol_vals) / len(vol_vals) if vol_vals else None
        volatility_delta = None
        if vol_mean is not None and baseline_volatility_mean is not None and baseline_volatility_mean > 0:
            volatility_delta = (vol_mean - baseline_volatility_mean) / baseline_volatility_mean

        results.append({
            "patch": label,
            "safe_to_caution": safe_to_caution,
            "near_threshold_ratio": round(near_ratio, 4),
            "max_consecutive_near_frames": max_consec_near,
            "volatility_mean": round(vol_mean, 4) if vol_mean is not None else None,
            "volatility_delta_vs_baseline": round(volatility_delta, 4) if volatility_delta is not None else None,
        })
        if baseline_volatility_mean is None and vol_mean is not None:
            baseline_volatility_mean = vol_mean

    out_path = os.path.join(out_dir, "calib_three_tiers.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"tiers": results, "note": "near_threshold_ratio: % frames with weighted_sum >= 0.9*safe_to_caution"}, f, ensure_ascii=False, indent=2)
    print("wrote", out_path)
    print("--- 三档汇总 ---")
    for r in results:
        print(r["patch"], "| near_ratio:", r["near_threshold_ratio"], "| max_consec_near:", r["max_consecutive_near_frames"], "| vol_delta:", r.get("volatility_delta_vs_baseline"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
