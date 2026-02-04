"""
Rate Limiter (C-4.2)

表达节流器

职责：
"我刚刚是不是已经说过了？"

这是避免"唠叨"的核心。

一期节流规则（够用）：
- 同类 action，最短间隔 2 秒
- 高紧急（urgency ≥4）可绕过
- 状态变化可重置计时器
"""

import time
from typing import Dict, Optional


class RateLimiter:
    """
    表达节流器
    
    职责：
    - 控制表达频率
    - 避免重复表达
    - 一期：时间窗口
    - 二期：可接入语义相似度
    """
    
    def __init__(self, default_interval: float = 2.0):
        """
        初始化节流器
        
        Args:
            default_interval: 默认最小间隔（秒，默认 2.0）
        """
        self.default_interval = default_interval
        self._last_time: Dict[str, float] = {}
        self._last_key: Optional[str] = None
    
    def allow(
        self,
        key: str,
        min_interval: Optional[float] = None,
        urgency: int = 1
    ) -> bool:
        """
        判断是否允许表达
        
        Args:
            key: 表达键（如 "turn_left", "obstacle_warning"）
            min_interval: 最小间隔（秒，可选，默认使用 default_interval）
            urgency: 紧急程度（1-5，≥4 可绕过节流）
            
        Returns:
            bool: True 才允许表达
        """
        # 高紧急（urgency ≥4）可绕过节流
        if urgency >= 4:
            self._last_time[key] = time.time()
            return True
        
        # 检查时间间隔
        now = time.time()
        last = self._last_time.get(key, 0)
        interval = min_interval if min_interval is not None else self.default_interval
        
        if now - last < interval:
            return False
        
        # 更新最后表达时间
        self._last_time[key] = now
        self._last_key = key
        return True
    
    def reset(self, key: Optional[str] = None):
        """
        重置节流器
        
        Args:
            key: 要重置的键（None 表示重置所有）
        """
        if key is None:
            self._last_time.clear()
            self._last_key = None
        else:
            if key in self._last_time:
                del self._last_time[key]
            if self._last_key == key:
                self._last_key = None
    
    def reset_on_state_change(self, new_state: str):
        """
        状态变化时重置计时器
        
        Args:
            new_state: 新状态
        """
        # 状态变化时，重置所有节流器
        # 允许在新状态下立即表达
        self.reset()
