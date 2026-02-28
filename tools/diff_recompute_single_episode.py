#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断：单 episode + 单 candidate，recompute 下 baseline vs candidate 逐帧对比。
用于确认 recompute 是否真的产生不同 decision，还是被 obs 温和性掩盖。
输出：seq, baseline_mode, candidate_mode；以及 不同帧数、safety_level 差异数、control_mode 差异数。
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REPLAY_FILENAME = "replay_output.jsonl"


def _load_replay_decisions(bundle_path: str) -> list:
    path = os.path.join(bundle_path.rstrip("/"), REPLAY_FILENAME)
    out = []
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            dec = rec.get("decision") or {}
            out.append({
                "seq": rec.get("seq"),
                "safety_level": dec.get("safety_level"),
                "control_mode": dec.get("control_mode"),
                "pal_lookahead_m": dec.get("pal_lookahead_m"),
            })
    return out


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Single-episode baseline vs candidate recompute diff")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--patch", required=True, help="Candidate patch JSON path")
    p.add_argument("--episode-id", default="", help="Golden episode id (e.g. slice_EPISODE_6M42S_complexity_rise_11_11). If empty, pick first from golden.")
    p.add_argument("--out-dir", default="", help="Sim output dir; default outputs/v1.1/diff_recompute_episode")
    p.add_argument("--max-print", type=int, default=0, help="Max lines to print (0=all). Use e.g. 20 to cap output.")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    golden_dir = os.path.join(base_dir, version, "golden")
    if not os.path.isdir(golden_dir):
        print("ERROR: golden dir not found:", golden_dir, file=sys.stderr)
        return 2
    if not os.path.isfile(args.patch):
        print("ERROR: patch file not found:", args.patch, file=sys.stderr)
        return 2

    # Resolve episode
    if args.episode_id:
        ep_id = args.episode_id
        rel = f"{version}/golden/{ep_id}"
        if not os.path.isdir(os.path.join(base_dir, rel)):
            print("ERROR: episode dir not found:", os.path.join(base_dir, rel), file=sys.stderr)
            return 2
    else:
        ep_ids = sorted(d for d in os.listdir(golden_dir) if os.path.isdir(os.path.join(golden_dir, d)))
        if not ep_ids:
            print("ERROR: no episodes in golden", file=sys.stderr)
            return 2
        ep_id = ep_ids[0]
        rel = f"{version}/golden/{ep_id}"
    print("episode:", ep_id, "rel:", rel)

    out_dir = args.out_dir or os.path.join("outputs", version, "diff_recompute_episode")
    os.makedirs(out_dir, exist_ok=True)

    from simulation.sim_runner import run_episode

    # Baseline (recompute, no patch)
    baseline_bundle = run_episode(
        base_dir, version, rel, "", out_dir,
        bundle_episode_id=ep_id, mode="recompute",
    )
    candidate_bundle = run_episode(
        base_dir, version, rel, args.patch, out_dir,
        bundle_episode_id=ep_id, baseline_bundle_path=baseline_bundle, mode="recompute",
    )

    base_dec = _load_replay_decisions(baseline_bundle)
    cand_dec = _load_replay_decisions(candidate_bundle)
    n = max(len(base_dec), len(cand_dec))
    if n == 0:
        print("ERROR: no replay frames", file=sys.stderr)
        return 2
    # 逐行对齐：按帧序比较，不按 seq 去重
    diff_frames = 0
    safety_level_diff = 0
    control_mode_diff = 0
    print("seq\tbaseline_mode\tcandidate_mode\tbaseline_safety\tcandidate_safety")
    print("-" * 72)
    for i in range(n):
        b = base_dec[i] if i < len(base_dec) else {}
        c = cand_dec[i] if i < len(cand_dec) else {}
        seq = b.get("seq") or c.get("seq") or i
        b_mode = b.get("control_mode") or ""
        c_mode = c.get("control_mode") or ""
        b_safe = b.get("safety_level") or ""
        c_safe = c.get("safety_level") or ""
        any_diff = (b_mode != c_mode) or (b_safe != c_safe)
        if b_mode != c_mode:
            control_mode_diff += 1
        if b_safe != c_safe:
            safety_level_diff += 1
        if any_diff:
            diff_frames += 1
        if args.max_print <= 0 or i < args.max_print:
            print(seq, b_mode, c_mode, b_safe, c_safe, sep="\t")
        elif i == args.max_print:
            print("...")
    all_seqs = n
    print("-" * 72)
    print("total_frames:", all_seqs)
    print("diff_frames:", diff_frames)
    print("safety_level_diff_count:", safety_level_diff)
    print("control_mode_diff_count:", control_mode_diff)
    if diff_frames == 0:
        print("→ 差异数 = 0：recompute 执行了但权重变化未穿透 decision 边界（或 obs 在线性区）。")
    else:
        print("→ 差异数 > 0：recompute 正常，决策边界被触碰。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
