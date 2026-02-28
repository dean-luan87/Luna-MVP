#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_score 尺度诊断：找出「压扁器」。
在单 episode 或完整 Golden Suite 上跑 A3，输出 weighted_sum_before_clamp / raw(clamped) / 各 component 的分布：
raw_p50, raw_p90, raw_p95, raw_max；以及是否存在 >0.5 的帧。
用于判断 risk 宇宙是 0~1 还是 0~0.2 量纲，进而决定 calibration 是重设阈值还是重标定 feature。
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

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


def _quantile(x: List[float], q: float) -> float:
    if not x:
        return 0.0
    s = sorted(x)
    i = min(int(len(s) * q), len(s) - 1)
    return float(s[i])


def _run_episode_and_collect_debug(
    base_dir: str,
    version: str,
    rel: str,
    patch_config: Dict[str, Any],
) -> List[Dict[str, Any]]:
    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter

    records_path = os.path.join(base_dir, rel, "records.jsonl")
    records = _load_jsonl(records_path)
    OBS_V1 = "OBS_V1"
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    if not obs_v1:
        return []

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()

    out = []
    for r in obs_v1:
        ts = r.get("ts", 0.0)
        tick_out = adapter.tick(r, virtual_ts=ts)
        db = tick_out.get("a3_debug") or {}
        out.append(db)
    return out


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="risk_score distribution: weighted_sum_before_clamp / raw / components")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode-id", default="", help="Single golden episode id; if empty and not --golden, pick first")
    p.add_argument("--golden", action="store_true", help="Run on full Golden Suite and aggregate")
    p.add_argument("--patch", default="", help="Optional patch (e.g. baseline = no patch)")
    p.add_argument("--out-json", default="", help="Write risk_score_distribution.json to this path")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    golden_dir = os.path.join(base_dir, version, "golden")
    if not os.path.isdir(golden_dir):
        print("ERROR: golden dir not found:", golden_dir, file=sys.stderr)
        return 2

    patch_config = {}
    if args.patch and os.path.isfile(args.patch):
        with open(args.patch, "r", encoding="utf-8") as f:
            patch_config = json.load(f) or {}
    patch_config = {k: v for k, v in patch_config.items() if isinstance(k, str) and (k.startswith("weights.") or k.startswith("thresholds."))}

    if args.golden:
        ep_ids = sorted(d for d in os.listdir(golden_dir) if os.path.isdir(os.path.join(golden_dir, d)))
        all_debug: List[Dict[str, Any]] = []
        for ep_id in ep_ids:
            rel = f"{version}/golden/{ep_id}"
            all_debug.extend(_run_episode_and_collect_debug(base_dir, version, rel, patch_config))
        debug_list = all_debug
        scope = "full Golden Suite"
    else:
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
        debug_list = _run_episode_and_collect_debug(base_dir, version, rel, patch_config)
        scope = ep_id

    if not debug_list:
        print("ERROR: no debug frames", file=sys.stderr)
        return 2

    n = len(debug_list)
    weighted_sum = [float(d.get("weighted_sum_before_clamp", d.get("raw", 0))) for d in debug_list]
    raw_clamped = [float(d.get("raw", 0)) for d in debug_list]
    ema_list = [float(d.get("ema", 0)) for d in debug_list]

    # 各 component 的 key（与 engine 一致）
    comp_keys = [
        "risk_density", "redline_hit", "occlusion_ratio", "roi_load",
        "path_instability", "motion_instability", "branch_load",
        "speak_pressure", "reject_pressure",
    ]
    comp_stats: Dict[str, Dict[str, float]] = {}
    for k in comp_keys:
        vals = [float(d.get(k, 0)) for d in debug_list]
        comp_stats[k] = {
            "max": max(vals) if vals else 0,
            "p95": _quantile(vals, 0.95),
            "mean": sum(vals) / n if vals else 0,
        }

    # 分布统计
    ws_p50 = _quantile(weighted_sum, 0.5)
    ws_p90 = _quantile(weighted_sum, 0.9)
    ws_p95 = _quantile(weighted_sum, 0.95)
    ws_max = max(weighted_sum)
    ws_mean = sum(weighted_sum) / n
    n_above_03 = sum(1 for x in weighted_sum if x > 0.3)
    n_above_05 = sum(1 for x in weighted_sum if x > 0.5)

    dist = {
        "scope": scope,
        "frame_count": n,
        "weighted_sum_before_clamp": {
            "p50": round(ws_p50, 4),
            "p90": round(ws_p90, 4),
            "p95": round(ws_p95, 4),
            "max": round(ws_max, 4),
            "mean": round(ws_mean, 4),
        },
        "raw_clamped": {
            "p50": round(_quantile(raw_clamped, 0.5), 4),
            "p95": round(_quantile(raw_clamped, 0.95), 4),
            "max": round(max(raw_clamped), 4),
        },
        "ema": {
            "p95": round(_quantile(ema_list, 0.95), 4),
            "max": round(max(ema_list), 4),
        },
        "frames_above_0.3": n_above_03,
        "frames_above_0.5": n_above_05,
        "components": {k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in comp_stats.items()},
    }

    print("scope:", scope, "frames:", n)
    if args.patch:
        print("patch:", args.patch)
    print()
    print("--- weighted_sum_before_clamp (pre-clamp risk) ---")
    print("  p50:", dist["weighted_sum_before_clamp"]["p50"])
    print("  p90:", dist["weighted_sum_before_clamp"]["p90"])
    print("  p95:", dist["weighted_sum_before_clamp"]["p95"])
    print("  max:", dist["weighted_sum_before_clamp"]["max"])
    print("  mean:", dist["weighted_sum_before_clamp"]["mean"])
    print("  frames with sum > 0.3:", n_above_03)
    print("  frames with sum > 0.5:", n_above_05)
    print()
    print("--- raw (after clamp 0~1) ---")
    print("  p50:", dist["raw_clamped"]["p50"])
    print("  p95:", dist["raw_clamped"]["p95"])
    print("  max:", dist["raw_clamped"]["max"])
    print()
    print("--- ema ---")
    print("  p95:", dist["ema"]["p95"])
    print("  max:", dist["ema"]["max"])
    print()
    print("--- components (max / p95 / mean) ---")
    for k, v in comp_stats.items():
        print(f"  {k}: max={v['max']:.4f} p95={v['p95']:.4f} mean={v['mean']:.4f}")

    if ws_max < 0.25:
        print()
        print("→ weighted_sum 长期 < 0.25：风险宇宙在 0~0.2 量纲，阈值 0.38 为空中楼阁；应设 safe_to_caution ≈ raw_p95 * 1.1 或重标定 feature。")
    elif n_above_05 == 0:
        print()
        print("→ 无任何帧 > 0.5：风险未进入高段，阈值可基于 raw_p95 做 calibration。")
    else:
        print()
        print("→ 存在 >0.5 帧：风险尺度可达 0~1，当前 EMA/阈值关系需用 raw 分布校准。")

    if args.out_json:
        out_path = args.out_json
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(dist, f, ensure_ascii=False, indent=2)
        print()
        print("wrote:", out_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
