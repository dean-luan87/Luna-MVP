#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量纲审计 Step 1：在 risk 计算链末端插桩，将 raw feature + weighted_sum_before_clamp 写入 logs/risk_debug.jsonl。
只记录 raw feature 与 weighted_sum，不记录 EMA、不记录 decision。
供 analyze_risk_distribution.py 统计分布。
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


def _run_episode_and_write_debug(
    base_dir: str,
    version: str,
    rel: str,
    out_path: str,
    patch_config: Dict[str, Any],
    episode_id: str = "",
) -> int:
    from simulation.logic.a3_headless_adapter import A3HeadlessAdapter

    records_path = os.path.join(base_dir, rel, "records.jsonl")
    records = _load_jsonl(records_path)
    OBS_V1 = "OBS_V1"
    obs_v1 = [r for r in records if (r.get("record_type") or "").strip() == OBS_V1]
    if not obs_v1:
        return 0

    adapter = A3HeadlessAdapter(base_config={}, patch_config=patch_config)
    adapter.reset()

    n = 0
    with open(out_path, "a", encoding="utf-8") as f:
        for r in obs_v1:
            ts = r.get("ts", 0.0)
            seq = r.get("seq", n)
            tick_out = adapter.tick(r, virtual_ts=ts)
            db = tick_out.get("a3_debug") or {}
            row = {
                "seq": seq,
                "risk_density": float(db.get("risk_density_raw", db.get("risk_density", 0))),
                "redline_hit": float(db.get("redline_hit_raw", db.get("redline_hit", 0))),
                "path_instability": float(db.get("path_instability_raw", db.get("path_instability", 0))),
                "motion_instability": float(db.get("motion_instability_raw", db.get("motion_instability", 0))),
                "occlusion_ratio": float(db.get("occlusion_ratio_raw", db.get("occlusion_ratio", 0))),
                "roi_load": float(db.get("roi_load_raw", db.get("roi_load", 0))),
                "weighted_sum_before_clamp": float(db.get("weighted_sum_before_clamp", 0)),
            }
            if episode_id:
                row["episode_id"] = episode_id
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    return n


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Record risk_debug.jsonl (raw features + weighted_sum_before_clamp)")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode-id", default="", help="Single golden episode id; if empty and not --golden, pick first")
    p.add_argument("--golden", action="store_true", help="Run on full Golden Suite (incl. 6m42s slices)")
    p.add_argument("--golden-stress", action="store_true", help="Run on golden_stress episodes")
    p.add_argument("--golden-stress-v2", action="store_true", help="Run on golden_stress_v2 (B2 continuous stress)")
    p.add_argument("--out", default="logs/risk_debug.jsonl", help="Output jsonl path")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    if args.golden_stress_v2:
        episode_dir_name = "golden_stress_v2"
    elif args.golden_stress:
        episode_dir_name = "golden_stress"
    else:
        episode_dir_name = "golden"
    golden_dir = os.path.join(base_dir, version, episode_dir_name)
    if not os.path.isdir(golden_dir):
        print("ERROR: dir not found:", golden_dir, file=sys.stderr)
        return 2

    out_path = args.out
    if not os.path.isabs(out_path):
        out_path = os.path.join(ROOT, out_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    if os.path.isfile(out_path):
        os.remove(out_path)

    patch_config = {}

    if args.golden or args.golden_stress or args.golden_stress_v2:
        ep_ids = sorted(d for d in os.listdir(golden_dir) if os.path.isdir(os.path.join(golden_dir, d)))
        total = 0
        for ep_id in ep_ids:
            rel = f"{version}/{episode_dir_name}/{ep_id}"
            total += _run_episode_and_write_debug(base_dir, version, rel, out_path, patch_config, episode_id=ep_id)
        print("wrote", total, "rows to", out_path, f"({episode_dir_name}, {len(ep_ids)} episodes)")
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
        total = _run_episode_and_write_debug(base_dir, version, rel, out_path, patch_config, episode_id=ep_id or "")
        print("wrote", total, "rows to", out_path, "(", ep_id, ")")

    return 0


if __name__ == "__main__":
    sys.exit(main())
