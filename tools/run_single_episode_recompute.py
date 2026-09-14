#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单片 recompute：对单条 episode 的 records 用指定 patch 跑 recompute，写出带 risk 字段的 replay。
用于 Spark Test：验证当前物理链路能否产生 risk_used_max >= 0.38、high_risk_frames > 0。
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulation.sim_runner import run_episode


def main():
    ap = argparse.ArgumentParser(description="Single episode recompute with current physics (writes risk fields to replay)")
    ap.add_argument("--records", required=True, help="Path to episode records.jsonl")
    ap.add_argument("--patch", default="patches/physics/stress_v2_phys_v1.json", help="Patch JSON path")
    ap.add_argument("--out", default="outputs/spark_recompute_test", help="Output dir; replay in <out>/<bundle_name>/replay_output.jsonl")
    args = ap.parse_args()

    records_path = Path(args.records)
    if not records_path.is_file():
        print("ERROR: records not found:", records_path, file=sys.stderr)
        return 2
    episode_dir = records_path.resolve().parent
    # base_dir + version + rel 指向 episode_dir；与 run_sim_suite 一致
    base_dir = str(ROOT / "library_store")
    version = "v1.1"
    try:
        rel = episode_dir.relative_to(ROOT / "library_store" / version)
    except ValueError:
        rel = episode_dir.name
    episode_rel_path = f"{version}/{rel}".replace("\\", "/")
    ep_id = episode_dir.name

    patch_path = Path(args.patch)
    if not patch_path.is_absolute():
        patch_path = ROOT / patch_path
    if not patch_path.is_file():
        print("ERROR: patch not found:", patch_path, file=sys.stderr)
        return 2

    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    bundle_dir = run_episode(
        base_dir, version, episode_rel_path, str(patch_path), str(out_dir),
        bundle_episode_id=ep_id, baseline_bundle_path=None, mode="recompute",
    )
    print("replay_output.jsonl at:", Path(bundle_dir) / "replay_output.jsonl")
    return 0


if __name__ == "__main__":
    sys.exit(main())
