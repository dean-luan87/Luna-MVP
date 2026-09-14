#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A3 决策敏感度诊断：单 episode 下打印 raw_risk_score / smoothed_risk_score(EMA) / 阈值，
并统计 risk_score_max, mean, p95 与「距离最近阈值的 margin」。
用于判断是「阈值真空区」还是「边界前」。
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _load_jsonl(path: str) -> list:
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


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="A3 risk_score vs threshold diagnostic (single episode)")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode-id", default="", help="Golden episode id; if empty, pick first")
    p.add_argument("--patch", default="", help="Optional patch JSON path (e.g. risk_density 3x)")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    golden_dir = os.path.join(base_dir, version, "golden")
    if not os.path.isdir(golden_dir):
        print("ERROR: golden dir not found:", golden_dir, file=sys.stderr)
        return 2

    if args.episode_id:
        ep_id = args.episode_id
        rel = f"{version}/golden/{ep_id}"
        if not os.path.isdir(os.path.join(base_dir, rel)):
            print("ERROR: episode not found:", rel, file=sys.stderr)
            return 2
    else:
        ep_ids = sorted(d for d in os.listdir(golden_dir) if os.path.isdir(os.path.join(golden_dir, d)))
        if not ep_ids:
            print("ERROR: no episodes in golden", file=sys.stderr)
            return 2
        ep_id = ep_ids[0]
        rel = f"{version}/golden/{ep_id}"

    records_path = os.path.join(base_dir, rel, "records.jsonl")
    records = _load_jsonl(records_path)
    OBS_V1 = "OBS_V1"
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    if not obs_v1:
        print("ERROR: no OBS_V1 in episode", file=sys.stderr)
        return 2

    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter

    patch_config = {}
    if args.patch and os.path.isfile(args.patch):
        with open(args.patch, "r", encoding="utf-8") as f:
            patch_config = json.load(f) or {}
    # 诊断允许 weights.* 与 thresholds.*（如 threshold_probe_30down），from_flat_dict 会忽略未知 key
    patch_config = {k: v for k, v in patch_config.items() if isinstance(k, str) and (k.startswith("weights.") or k.startswith("thresholds."))}

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()

    raw_scores = []
    ema_scores = []
    thresh_caution = None
    thresh_danger = None
    hyst = None

    for r in obs_v1:
        ts = r.get("ts", 0.0)
        out = adapter.tick(r, virtual_ts=ts)
        db = out.get("a3_debug") or {}
        raw_scores.append(float(db.get("raw", 0)))
        ema_scores.append(float(db.get("ema", 0)))
        if thresh_caution is None:
            thresh_caution = db.get("threshold_safe_to_caution")
            thresh_danger = db.get("threshold_caution_to_danger")
            hyst = db.get("hysteresis")

    n = len(ema_scores)
    if n == 0:
        print("ERROR: no frames", file=sys.stderr)
        return 2

    def p95(x: list) -> float:
        if not x:
            return 0.0
        s = sorted(x)
        i = min(int(len(s) * 0.95), len(s) - 1)
        return float(s[i])

    raw_max = max(raw_scores)
    raw_mean = sum(raw_scores) / n
    raw_p95 = p95(raw_scores)
    ema_max = max(ema_scores)
    ema_mean = sum(ema_scores) / n
    ema_p95 = p95(ema_scores)

    thresh_caution = float(thresh_caution) if thresh_caution is not None else 0.38
    thresh_danger = float(thresh_danger) if thresh_danger is not None else 0.68
    hyst = float(hyst) if hyst is not None else 0.06

    # 距离「升到 CAUTION」的阈值：safe_to_caution + hysteresis
    threshold_guarded = thresh_caution + hyst
    margin_to_caution = threshold_guarded - ema_p95
    margin_to_caution_mean = threshold_guarded - ema_mean

    print("episode:", ep_id, "frames:", n)
    if args.patch:
        print("patch:", args.patch)
    print()
    print("--- raw_risk_score ---")
    print("  max:", round(raw_max, 4))
    print("  mean:", round(raw_mean, 4))
    print("  p95:", round(raw_p95, 4))
    print()
    print("--- smoothed_risk_score (EMA) ---")
    print("  max:", round(ema_max, 4))
    print("  mean:", round(ema_mean, 4))
    print("  p95:", round(ema_p95, 4))
    print()
    print("--- thresholds ---")
    print("  threshold_safe_to_caution:", thresh_caution)
    print("  threshold_caution_to_danger:", thresh_danger)
    print("  hysteresis:", hyst)
    print("  effective_guarded (safe→caution):", round(threshold_guarded, 4))
    print()
    print("--- margin (distance to decision boundary) ---")
    print("  margin_to_caution (threshold_guarded - ema_p95):", round(margin_to_caution, 4))
    print("  margin_to_caution_mean:", round(margin_to_caution_mean, 4))
    print()
    if margin_to_caution > 0.3:
        print("→ risk_score 离阈值很远（阈值真空区）：调权重难以触发分叉，需拉低阈值或做 calibration。")
    elif margin_to_caution > 0.1:
        print("→ risk_score 接近但未到阈值：D1 有潜力，可加强高压 Golden 或微调阈值。")
    else:
        print("→ risk_score 已接近/越过阈值：权重变化应能产生 decision 分叉。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
