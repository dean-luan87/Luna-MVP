#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D2.2: 按 tag 分桶统计 Golden 数量与缺口。
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_TAG_BUCKETS = ["low_light", "cross_traffic", "dynamic_object", "crowded", "reflection", "narrow_passage"]


def main():
    import argparse
    p = argparse.ArgumentParser(description="Golden bucket report")
    p.add_argument("--base-dir", default=os.path.join(ROOT, "library_store"))
    p.add_argument("--version-tag", default="v1.1")
    args = p.parse_args()
    golden_dir = Path(args.base_dir) / args.version_tag / "golden"
    if not golden_dir.is_dir():
        print("golden_dir not found:", golden_dir)
        return 0
    bucket = {t: [] for t in REQUIRED_TAG_BUCKETS}
    for ep_dir in sorted(golden_dir.iterdir()):
        if not ep_dir.is_dir():
            continue
        meta_path = ep_dir / "meta.json"
        if not meta_path.is_file():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        tags = meta.get("tags") or meta.get("golden_tags") or []
        for t in tags:
            if t in bucket:
                bucket[t].append(ep_dir.name)
    print("--- Golden bucket report ---")
    missing = []
    for tag in REQUIRED_TAG_BUCKETS:
        eps = bucket[tag]
        n = len(eps)
        if n == 0:
            missing.append(tag)
        print(f"  {tag}: {n} episodes", eps[:5] if eps else [])
    if missing:
        print("MISSING_COVERAGE:", ",".join(missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
