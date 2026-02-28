#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2: 将 episode 晋升为 Golden，写入 library_store/<version>/golden/<golden_id>/。
golden_id = episode_id__<ts> 避免覆盖。meta 必填：version_tag, episode_id, source_episode_path, tags, reason, created_at。
强制 tags 非空且必须在枚举内。
"""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN_TAGS = frozenset({"low_light", "cross_traffic", "dynamic_object", "crowded", "reflection", "narrow_passage"})


def main():
    p = argparse.ArgumentParser(description="Promote episode to golden set")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"), help="Library store root")
    p.add_argument("--version-tag", default="v1.1")
    p.add_argument("--episode-path", required=True, help="Episode path relative to base_dir, e.g. v1.1/episodes/20260209/session/ep_id")
    p.add_argument("--tags", required=True, nargs="+", help="Tags (must be from: low_light, cross_traffic, dynamic_object, crowded, reflection, narrow_passage)")
    p.add_argument("--reason", default="", help="Reason for promotion")
    args = p.parse_args()
    base = Path(args.base_dir)
    version = args.version_tag
    ep_path = args.episode_path.strip().strip("/")
    tags = [t.strip().lower() for t in args.tags if t.strip()]
    if not tags:
        print("ERROR: tags must be non-empty", file=sys.stderr)
        return 1
    bad = [t for t in tags if t not in GOLDEN_TAGS]
    if bad:
        print("ERROR: invalid tags (must be in enum):", bad, "allowed:", sorted(GOLDEN_TAGS), file=sys.stderr)
        return 1
    src_dir = base / ep_path
    if not src_dir.is_dir():
        print("ERROR: episode dir not found:", src_dir, file=sys.stderr)
        return 1
    episode_id = src_dir.name
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    golden_id = f"{episode_id}__{ts}"
    golden_root = base / version / "golden"
    dest_dir = golden_root / golden_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    records_src = src_dir / "records.jsonl"
    if records_src.is_file():
        shutil.copy2(records_src, dest_dir / "records.jsonl")
    meta = {
        "version_tag": version,
        "episode_id": episode_id,
        "source_episode_path": ep_path,
        "tags": list(tags),
        "reason": args.reason,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    meta_path = dest_dir / "meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("promoted:", dest_dir)
    print("golden_id:", golden_id)
    print("tags:", tags)
    return 0


if __name__ == "__main__":
    sys.exit(main())
