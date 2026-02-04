#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动测试训练样本存储器（用于 V6）
- 以 JSONL 形式落盘：一行一个样本，方便追加
- 后续可用于导出 CSV / JSON 做训练数据
"""

import os
import json
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TrainingSampleStore:
    """
    自动测试训练样本存储器（用于 V6）
    - 以 JSONL 形式落盘：一行一个样本，方便追加
    - 后续可用于导出 CSV / JSON 做训练数据
    """

    def __init__(self, base_dir: str = None, filename: str = "training_samples.jsonl"):
        # 默认存到项目根目录下的 auto_test 目录
        if base_dir is None:
            # 获取项目根目录
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            base_dir = os.path.join(project_root, "auto_test")
        
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

        self.file_path = os.path.join(self.base_dir, filename)
        logger.info(f"TrainingSampleStore 初始化完成，存储路径: {self.file_path}")

    def add_sample(self, sample: Dict[str, Any]) -> None:
        """
        追加一个训练样本
        sample 必须是可 JSON 序列化的字典
        """
        # 自动补充一些公共字段
        sample = dict(sample)
        sample.setdefault("created_at", time.time())
        sample.setdefault("version", "auto_test_v6")

        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
            logger.debug(f"训练样本已保存: {sample.get('keyword', 'unknown')}")
        except Exception as e:
            logger.error(f"保存训练样本失败: {e}")
            raise

    def list_samples(self, limit: int = None) -> List[Dict[str, Any]]:
        """
        读取所有训练样本（调试用）
        limit: 只取前 N 条（从最新往前）
        """
        if not os.path.exists(self.file_path):
            return []

        samples: List[Dict[str, Any]] = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        samples.append(data)
                    except Exception as e:
                        logger.warning(f"解析训练样本行失败: {e}")
                        continue
        except Exception as e:
            logger.error(f"读取训练样本失败: {e}")
            return []

        # 默认按时间排序（旧→新），limit 为最近 N 条
        samples.sort(key=lambda x: x.get("created_at", 0))
        if limit is not None and limit > 0:
            samples = samples[-limit:]

        return samples

    def get_count(self) -> int:
        """获取样本总数"""
        if not os.path.exists(self.file_path):
            return 0
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return sum(1 for line in f if line.strip())
        except Exception:
            return 0


