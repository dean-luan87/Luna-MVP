# -*- coding: utf-8 -*-
"""
Phase 3.2: EpisodeLoader — 只读 index + meta + records，不做分析。
禁止 import: runtime / a3 / intervention / external / main
"""
import json
import os
from typing import Any, Dict, Generator, List, Optional, Tuple


class EpisodeLoader:
    """
    从 index 和 episode 目录只读加载；遍历 index 必须排序保证可复现。
    """

    def __init__(self, base_dir: str = "library_store", version_tag: str = "v1.1") -> None:
        self.base_dir = base_dir.rstrip("/")
        self.version_tag = version_tag
        self.index_path = os.path.join(self.base_dir, version_tag, "episodes_index.jsonl")

    def iter_index(self) -> Generator[Dict[str, Any], None, None]:
        """读 episodes_index.jsonl 后排序 yield。坏行跳过。"""
        if not os.path.isfile(self.index_path):
            return
        rows: List[Dict[str, Any]] = []
        with open(self.index_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        for row in sorted(rows, key=lambda r: (r.get("session_id", ""), r.get("episode_id", ""), r.get("path", ""))):
            yield row

    def load_episode(self, meta_path: str) -> Optional[Dict[str, Any]]:
        """读取 meta.json。"""
        if not os.path.isfile(meta_path):
            return None
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    def iter_records(self, records_path: str) -> Tuple[List[Dict[str, Any]], int]:
        """
        逐行读 records.jsonl；坏行跳过并计数。
        返回 (records, parse_errors)。
        """
        records: List[Dict[str, Any]] = []
        parse_errors = 0
        if not os.path.isfile(records_path):
            return records, parse_errors
        with open(records_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    parse_errors += 1
        return records, parse_errors

    def load_episode_full(self, index_row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        根据 index 行加载完整 episode：meta + records + paths。
        返回 dict: meta, records, paths{episode_dir, meta_path, records_path}, parse_errors。
        """
        rel_path = index_row.get("path") or ""
        episode_dir = os.path.join(self.base_dir, rel_path)
        meta_path = os.path.join(episode_dir, "meta.json")
        records_path = os.path.join(episode_dir, "records.jsonl")

        meta = self.load_episode(meta_path)
        if meta is None:
            return None
        records, parse_errors = self.iter_records(records_path)
        return {
            "meta": meta,
            "records": records,
            "paths": {
                "episode_dir": episode_dir,
                "meta_path": meta_path,
                "records_path": records_path,
            },
            "parse_errors": parse_errors,
        }

