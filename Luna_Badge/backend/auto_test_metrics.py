#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试结果记录和统计
"""

import os
import json
import time
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "auto_test_results.jsonl")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def log_auto_test_result(record: dict):
    """
    记录一次测试结果（image-level 或 keyword-level）
    
    record 示例：
    {
        "type": "single" | "playlist" | "video",
        "keyword": "斑马线",
        "playlist": "出门散步",
        "match": True,
        "timestamp": 1234567890
    }
    """
    rec = dict(record)
    if "timestamp" not in rec:
        rec["timestamp"] = time.time()

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning(f"记录测试结果失败: {e}")


def load_all_records(limit=5000):
    """
    加载所有测试记录
    
    Args:
        limit: 最多加载多少条记录（None 表示全部）
        
    Returns:
        list: 测试记录列表
    """
    if not os.path.exists(LOG_PATH):
        return []

    records = []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except Exception:
                    continue
    except Exception as e:
        logger.error(f"加载测试记录失败: {e}")
        return []
    
    if limit and len(records) > limit:
        records = records[-limit:]
    return records


def compute_summary():
    """
    计算测试统计摘要
    
    Returns:
        dict: {
            "total": {"total": int, "pass": int},
            "keywords": [{"name": str, "total": int, "pass": int, "pass_rate": float}, ...],
            "playlists": [{"name": str, "total": int, "pass": int, "pass_rate": float}, ...],
            "records_count": int
        }
    """
    recs = load_all_records()

    by_keyword = defaultdict(lambda: {"total": 0, "pass": 0})
    by_playlist = defaultdict(lambda: {"total": 0, "pass": 0})
    total = {"total": 0, "pass": 0}

    for r in recs:
        m = bool(r.get("match"))
        total["total"] += 1
        if m:
            total["pass"] += 1

        kw = r.get("keyword")
        if kw:
            by_keyword[kw]["total"] += 1
            if m:
                by_keyword[kw]["pass"] += 1

        pl = r.get("playlist")
        if pl:
            by_playlist[pl]["total"] += 1
            if m:
                by_playlist[pl]["pass"] += 1

    def to_list(d):
        out = []
        for name, v in d.items():
            t = v["total"]
            p = v["pass"]
            rate = (p / t) if t > 0 else 0.0
            out.append({
                "name": name,
                "total": t,
                "pass": p,
                "pass_rate": rate,
            })
        out.sort(key=lambda x: x["pass_rate"])
        return out

    summary = {
        "total": total,
        "keywords": to_list(by_keyword),
        "playlists": to_list(by_playlist),
        "records_count": len(recs),
    }
    return summary


