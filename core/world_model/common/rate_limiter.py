# -*- coding: utf-8 -*-
"""
v1.8.5 Phase C 包 C: Rate Limiter（限频器）

职责：
- 去重/限频缓存（内存级）
- 防刷屏、防恶意输入

设计原则：
- 同一用户、同一 scene、同一 claim_key，在窗口内只记一次
- window 推荐：60s ~ 300s
- 目的：防刷屏、避免用户反复一句话把 support 撑爆
"""

import time
from typing import Dict, Optional


class SimpleRateLimiter:
    """
    简单限频器（内存级）
    
    规则：
    - 同一 key 在窗口内只允许一次
    - 窗口过期后，允许再次写入
    """
    
    def __init__(self, window_s: float = 120.0):
        """
        初始化限频器
        
        Args:
            window_s: 限频窗口（秒，默认 120 秒）
        """
        self.window_s = window_s
        self._last_seen: Dict[str, float] = {}
    
    def allow(self, key: str, now_ts: Optional[float] = None) -> bool:
        """
        检查是否允许通过限频
        
        Args:
            key: 限频键（格式：user_id:scene_id:report_type:claim_key）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            bool: True 表示允许通过，False 表示被限频
        """
        now = now_ts or time.time()
        last = self._last_seen.get(key)
        
        if last and (now - last) < self.window_s:
            # 在窗口内，拒绝
            return False
        
        # 允许通过，更新最后时间
        self._last_seen[key] = now
        return True
    
    def clear(self) -> None:
        """清空限频缓存"""
        self._last_seen.clear()


