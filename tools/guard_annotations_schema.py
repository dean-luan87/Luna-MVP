#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3.3: 答案一致性 Guard（轻量）

检查项：
- JSON 可解析
- 必须字段存在
- (session_id, episode_id) 在 episodes_index.jsonl 中存在
- task_id 在 annotation_tasks.jsonl 中存在

不检查“答得对不对”。
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"version_tag", "session_id", "episode_id", "task_id", "answer", "annotator", "annotated_at"}


def load_index_pairs(base_dir: str, version_tag: str) -> set:
    path = os.path.join(base_dir, version_tag, "episodes_index.jsonl")
    out = set()
    if not os.path.isfile(path):
        return out
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            out.add(((row.get("session_id") or ""), (row.get("episode_id") or "")))
    return out


def load_task_ids(tasks_path: str) -> set:
    out = set()
    if not os.path.isfile(tasks_path):
        return out
    with open(tasks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            tid = row.get("task_id")
            if tid:
                out.add(tid)
    return out


def main():
    parser = argparse.ArgumentParser(description="Phase 3.3: guard annotations answers schema")
    parser.add_argument("--base-dir", default=str(ROOT / "library_store"), help="library_store 根目录")
    parser.add_argument("--version-tag", default="v1.1", help="version_tag")
    parser.add_argument("--answers-path", default=None, help="answers.jsonl 路径（默认 annotations/<v>/answers.jsonl）")
    parser.add_argument("--tasks-path", default=None, help="annotation_tasks.jsonl 路径（默认 outputs/<v>/annotation_tasks.jsonl）")
    args = parser.parse_args()

    version = args.version_tag
    answers_path = args.answers_path or str(ROOT / "annotations" / version / "answers.jsonl")
    tasks_path = args.tasks_path or str(ROOT / "outputs" / version / "annotation_tasks.jsonl")

    if not os.path.isfile(answers_path):
        print("PASS: no answers file (nothing to validate)")
        return 0

    valid_pairs = load_index_pairs(args.base_dir, version)
    valid_task_ids = load_task_ids(tasks_path)

    errors = []
    with open(answers_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{answers_path}:{line_no} JSON 解析失败: {e}")
                continue

            missing = REQUIRED - set(row.keys())
            if missing:
                errors.append(f"{answers_path}:{line_no} 缺少字段: {sorted(missing)}")

            sid = row.get("session_id") or ""
            eid = row.get("episode_id") or ""
            if (sid, eid) not in valid_pairs:
                errors.append(f"{answers_path}:{line_no} episode 不在 index: session_id={sid!r} episode_id={eid!r}")

            tid = row.get("task_id")
            if tid and tid not in valid_task_ids:
                errors.append(f"{answers_path}:{line_no} task_id 不在 annotation_tasks: {tid!r}")

    if errors:
        for e in errors:
            print(e)
        print("FAIL: annotations schema / reference check failed")
        return 1

    print("PASS: annotations schema and references OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

