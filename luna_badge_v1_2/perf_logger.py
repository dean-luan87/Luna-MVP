#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一性能日志记录器

功能：
- 统一日志格式（run/frame/event）
- 自动写入 JSONL 文件
- 线程安全
"""

import json
import os
import time
import threading
from pathlib import Path
from typing import List, Dict, Any

LOG_DIR = Path("perf_logs")
LOG_DIR.mkdir(exist_ok=True)

_lock = threading.Lock()
_handles = {}


def _get_handle(run_id: str):
    """获取或创建日志文件句柄"""
    with _lock:
        if run_id not in _handles:
            fname = LOG_DIR / f"run_{run_id}.jsonl"
            _handles[run_id] = open(fname, "a", buffering=1)
        return _handles[run_id]


def log_records(run_id: str, records: List[Dict[str, Any]]):
    """
    批量写入日志记录
    
    Args:
        run_id: 运行ID
        records: 日志记录列表（每个记录是一个字典）
    """
    if not records:
        return
    
    f = _get_handle(run_id)
    ts = time.time()
    
    with _lock:
        for rec in records:
            # 确保每条记录都有时间戳
            if "log_ts" not in rec:
                rec["log_ts"] = ts
            # 确保有 run_id
            if "run_id" not in rec:
                rec["run_id"] = run_id
            
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()  # 立即刷新，确保数据不丢失


def log_frame(run_id: str, frame_log: Dict[str, Any]):
    """记录单帧日志"""
    frame_log["type"] = "frame"
    log_records(run_id, [frame_log])


def log_event(run_id: str, event_log: Dict[str, Any]):
    """记录事件日志"""
    event_log["type"] = "event"
    log_records(run_id, [event_log])


def log_run(run_id: str, run_log: Dict[str, Any]):
    """记录运行级别日志"""
    run_log["type"] = "run"
    log_records(run_id, [run_log])


def close_all():
    """关闭所有日志文件句柄"""
    with _lock:
        for f in _handles.values():
            f.close()
        _handles.clear()


def get_log_file(run_id: str) -> Path:
    """获取日志文件路径"""
    return LOG_DIR / f"run_{run_id}.jsonl"


__all__ = ["log_records", "log_frame", "log_event", "log_run", "close_all", "get_log_file"]


