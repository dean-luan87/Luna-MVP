#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.2-Explain Core CLI。
读 library_store index + episode records，写 outputs/<version>/episode_explanations.jsonl。
不接 LLM、不修改 runtime、不写 library_store。
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from library.episode_explainer import EpisodeExplainer
from library.analyzer.episode_loader import EpisodeLoader


def main():
    parser = argparse.ArgumentParser(
        description="Episode Explainer: read episodes, write episode_explanations.jsonl (structured_explain only)."
    )
    parser.add_argument("--base-dir", default="library_store", help="Library store root")
    parser.add_argument("--version-tag", default="v1.1", help="Version tag")
    parser.add_argument("--out-dir", default="outputs", help="Output directory")
    parser.add_argument("--limit", type=int, default=None, help="Max episodes (optional)")
    args = parser.parse_args()

    base_dir = args.base_dir
    version_tag = args.version_tag
    out_dir = args.out_dir.rstrip("/")
    limit = args.limit

    out_version = os.path.join(out_dir, version_tag)
    os.makedirs(out_version, exist_ok=True)
    out_path = os.path.join(out_version, "episode_explanations.jsonl")

    loader = EpisodeLoader(base_dir=base_dir, version_tag=version_tag)
    explainer = EpisodeExplainer()
    count = 0

    with open(out_path, "w", encoding="utf-8") as f:
        for index_row in loader.iter_index():
            if limit is not None and count >= limit:
                break
            full = loader.load_episode_full(index_row)
            if full is None:
                continue
            meta = full["meta"]
            records = full["records"]
            episode_id = (meta.get("episode_id") or index_row.get("episode_id") or "").strip()
            trigger_type = (meta.get("trigger_type") or index_row.get("trigger_type") or "").strip()

            out = explainer.explain_episode(
                episode_id=episode_id,
                trigger_type=trigger_type,
                records=records,
            )
            from datetime import datetime
            out["generated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            count += 1

    print("episodes explained:", count)
    print("output:", out_path)


if __name__ == "__main__":
    main()
