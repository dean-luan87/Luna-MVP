#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用现有 Golden 按 weighted_sum 选高压 episode，复制到 golden_stress（打 tag stress）。
当暂无 6m42s trace 时，用此脚本先凑 10~15 条 stress，跑 calib 验收。
有 trace 后可用 generate_stress_slices_from_trace.py 从 6m42s 生成更准的 stress。
"""
import json
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description="Populate golden_stress from golden by weighted_sum (top N)")
    p.add_argument("--base-dir", default="library_store")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--top-n", type=int, default=15, help="Number of episodes to copy (by max weighted_sum)")
    p.add_argument("--dry-run", action="store_true", help="Only print would-copy list")
    args = p.parse_args()

    base_dir = args.base_dir.rstrip("/")
    version = args.version_tag
    golden_dir = os.path.join(base_dir, version, "golden")
    stress_dir = os.path.join(base_dir, version, "golden_stress")
    if not os.path.isdir(golden_dir):
        print("ERROR: golden dir not found:", golden_dir, file=sys.stderr)
        return 2

    # 1) 录 risk_debug（带 episode_id）
    debug_path = os.path.join(ROOT, "logs", "risk_debug_golden_for_stress.jsonl")
    os.makedirs(os.path.dirname(debug_path), exist_ok=True)
    import subprocess
    r = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "record_risk_debug.py"), "--golden", "--base-dir", base_dir, "--version-tag", version, "--out", debug_path],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print("ERROR: record_risk_debug failed", r.stderr, file=sys.stderr)
        return 2
    if not os.path.isfile(debug_path):
        print("ERROR: no risk_debug output", file=sys.stderr)
        return 2
    ep_ids = sorted(d for d in os.listdir(golden_dir) if os.path.isdir(os.path.join(golden_dir, d)))

    # 2) 按 episode_id 聚合并取 max weighted_sum
    from collections import defaultdict
    by_ep = defaultdict(list)
    with open(debug_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            ep_id = row.get("episode_id", "")
            if ep_id:
                by_ep[ep_id].append(float(row.get("weighted_sum_before_clamp", 0)))

    ep_max = [(ep_id, max(vals)) for ep_id, vals in by_ep.items() if vals]
    ep_max.sort(key=lambda x: -x[1])
    top = ep_max[: args.top_n]
    if not top:
        print("ERROR: no episodes with risk_debug", file=sys.stderr)
        return 2

    print("top episodes by max weighted_sum:", [x[0] for x in top])
    if args.dry_run:
        return 0

    os.makedirs(stress_dir, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    for ep_id, _ in top:
        src = os.path.join(golden_dir, ep_id)
        dst = os.path.join(stress_dir, ep_id)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        meta_path = os.path.join(dst, "meta.json")
        meta = json.load(open(meta_path, "r", encoding="utf-8"))
        orig_tags = meta.get("tags") or meta.get("golden_tags") or []
        meta["tags"] = ["stress"] + [t for t in orig_tags if t != "stress"]
        meta["source_episode_path"] = f"{version}/golden_stress/{ep_id}"
        meta["reason"] = "stress: populated from golden by weighted_sum (calib_v1)"
        meta["created_at"] = now
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    print("wrote", len(top), "episodes to", stress_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
