#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 TTSGuard 文本防抖功能
"""

import time
import sys
import os
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@dataclass
class TTSGuardConfig:
    same_text_interval: float = 8.0    # 同一句话 8 秒内只说一次
    min_interval_any: float = 0.3      # 全局调用最小间隔 300ms


class TTSGuard:
    """TTS 文本级防抖器（防止重复播报）"""
    
    def __init__(self, cfg: Optional[TTSGuardConfig] = None) -> None:
        self._cfg = cfg or TTSGuardConfig()
        self._last_text: Optional[str] = None
        self._last_text_ts: float = 0.0
        self._last_any_ts: float = 0.0

    def allow(self, text: str) -> bool:
        """
        检查是否允许播报
        
        Returns:
            bool: True 允许，False 拒绝
        """
        now = time.time()
        if not text or not text.strip():
            return False

        # 全局频率限制：避免在极端情况下每帧都来一个
        if now - self._last_any_ts < self._cfg.min_interval_any:
            print(f"  ❌ 全局间隔限制（{(now - self._last_any_ts)*1000:.0f}ms < {self._cfg.min_interval_any*1000:.0f}ms）")
            return False

        # 同一句话防抖：避免"已到达目的地"这类话刷屏
        if text == self._last_text and now - self._last_text_ts < self._cfg.same_text_interval:
            print(f"  ❌ 同句冷却限制（{(now - self._last_text_ts):.1f}s < {self._cfg.same_text_interval}s）")
            return False

        self._last_any_ts = now
        self._last_text_ts = now
        self._last_text = text
        print(f"  ✅ 允许播报")
        return True


def main():
    print("=== 测试 TTSGuard 文本防抖 ===\n")
    guard = TTSGuard()

    # 测试 1: 第一次允许
    print("测试1 - 第一次播报 '测试文本1':")
    result1 = guard.allow('测试文本1')
    print(f"  结果: {result1} (应该 True)\n")

    # 测试 2: 立即重复（应该被拒绝）
    print("测试2 - 立即重复 '测试文本1':")
    result2 = guard.allow('测试文本1')
    print(f"  结果: {result2} (应该 False)\n")

    # 测试 3: 不同文本（但受全局间隔限制）
    print("测试3 - 不同文本 '测试文本2'（立即）:")
    result3 = guard.allow('测试文本2')
    print(f"  结果: {result3} (应该 False，因为全局间隔)\n")

    # 测试 4: 等待后不同文本
    print("测试4 - 等待 0.5 秒后播报 '测试文本2':")
    time.sleep(0.5)
    result4 = guard.allow('测试文本2')
    print(f"  结果: {result4} (应该 True)\n")

    # 测试 5: 再次重复（应该被拒绝）
    print("测试5 - 再次重复 '测试文本2':")
    result5 = guard.allow('测试文本2')
    print(f"  结果: {result5} (应该 False)\n")

    # 测试 6: 等待 8 秒后重复（应该允许）
    print("测试6 - 等待 8.1 秒后重复 '测试文本2':")
    time.sleep(8.1)
    result6 = guard.allow('测试文本2')
    print(f"  结果: {result6} (应该 True)\n")

    print("✅ TTSGuard 测试完成")


if __name__ == "__main__":
    main()














