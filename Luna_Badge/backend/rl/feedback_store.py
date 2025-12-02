#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
强化学习数据入口：存储 AI判断错误 + 人工修正的数据
"""

import os
import json
import time
from typing import Dict, Any, Optional
import threading


class FeedbackStore:
    """
    强化学习数据入口：
    - 专门存储"AI判断错误 + 人工修正"的数据
    - 先简单写 JSONL / 小 JSON，后面再接训练流水线
    """

    def __init__(self, base_dir: str = "training_data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.file_path = os.path.join(self.base_dir, "feedback.jsonl")
        self._lock = threading.Lock()

    def append_feedback(self, item: Dict[str, Any]):
        """
        item 建议格式：
        {
          "timestamp": int,
          "image_path": str or None,
          "keyword": str or None,    # 测试使用的目标标签
          "ai_description": str,
          "ai_tags": [str, ...],
          "ai_decision": str,        # e.g. "match" / "mismatch"
          "human_label": str,        # 人工认为的真值（如 "扶梯"）
          "context": {...}           # 场景上下文（导航/测试场景等）
        }
        """
        item = dict(item)
        item.setdefault("timestamp", int(time.time()))
        os.makedirs(self.base_dir, exist_ok=True)

        with self._lock:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")


