#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.2: Episode Analyzer CLI — 离线全链路，输出写 outputs/，不写 library_store。
单线程、遍历排序，保证可复现。
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from library.analyzer.annotation_tasks import build_annotation_tasks, write_annotation_tasks
from library.analyzer.episode_loader import EpisodeLoader
from library.analyzer.episode_summary import build_summary
from library.analyzer.episode_tagging import compute_tags, write_episode_tags


def main():
    parser = argparse.ArgumentParser(
        description="Episode Analyzer: read library_store, write outputs/ (summary/tags/annotation_tasks)."
    )
    parser.add_argument("--base-dir", default="library_store", help="Library store root")
    parser.add_argument("--version-tag", default="v1.1", help="Version tag")
    parser.add_argument("--out-dir", default="outputs", help="Output directory")
    parser.add_argument("--limit", type=int, default=None, help="Max episodes to process (optional)")
    args = parser.parse_args()

    base_dir = args.base_dir
    version_tag = args.version_tag
    out_dir = args.out_dir.rstrip("/")
    limit = args.limit

    out_version = os.path.join(out_dir, version_tag)
    os.makedirs(out_version, exist_ok=True)
    summaries_path = os.path.join(out_version, "episode_summaries.jsonl")
    tags_path = os.path.join(out_version, "episode_tags.jsonl")
    tasks_path = os.path.join(out_version, "annotation_tasks.jsonl")

    loader = EpisodeLoader(base_dir=base_dir, version_tag=version_tag)
    summaries = []
    tag_rows = []
    tags_by_episode = {}
    total_parse_errors = 0
    processed = 0

    for index_row in loader.iter_index():
        if limit is not None and processed >= limit:
            break
        full = loader.load_episode_full(index_row)
        if full is None:
            continue
        meta = full["meta"]
        records = full["records"]
        parse_errors = full.get("parse_errors", 0)
        total_parse_errors += parse_errors

        summary = build_summary(meta, records, parse_errors)
        summaries.append(summary)
        tags = compute_tags(summary, records)
        sid = summary.get("session_id") or ""
        eid = summary.get("episode_id") or ""
        tags_by_episode[(sid, eid)] = tags
        tag_rows.append(
            {
                "version_tag": version_tag,
                "session_id": sid,
                "episode_id": eid,
                "tags": tags,
            }
        )
        processed += 1

    with open(summaries_path, "w", encoding="utf-8") as f:
        for s in summaries:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    write_episode_tags(tag_rows, tags_path)
    tasks = build_annotation_tasks(summaries, tags_by_episode)
    write_annotation_tasks(tasks, tasks_path)

    print("episodes processed:", processed)
    print("parse_errors:", total_parse_errors)
    print("outputs:", summaries_path, tags_path, tasks_path)


if __name__ == "__main__":
    main()

