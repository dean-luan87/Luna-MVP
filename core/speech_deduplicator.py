# -*- coding: utf-8 -*-
"""
语义去重器（Speech Deduplicator）

v1.8.2: TTL 基于文本去重
"""

import time
from typing import Dict


class SpeechDeduplicator:
    """语义去重器"""
    
    def __init__(self, ttl_seconds: int = 8):
        """
        初始化语义去重器
        
        Args:
            ttl_seconds: 去重时间窗口（秒），默认 8 秒
        """
        self.ttl = ttl_seconds
        self._spoken_cache: Dict[str, float] = {}
    
    def should_speak(self, text: str) -> bool:
        """
        判断是否应该播报（去重检查）
        
        Args:
            text: 要播报的文本
        
        Returns:
            bool: True 表示可以播报，False 表示在 TTL 内已播过
        """
        now = time.time()
        last_time = self._spoken_cache.get(text)
        
        if last_time and (now - last_time) < self.ttl:
            return False
        
        self._spoken_cache[text] = now
        return True
