"""
Cache v0.2 - 未来剧本缓存（TTL）

B2 v0.2: 缓存机制，控制 B2 的运行频率

职责：
- TTL 管理（支持动态 TTL）
- 避免频繁运行
- 缓存未来剧本
"""

import time
from typing import Optional, Any
from .b2_types_v02 import B2Advisory


class FutureCache:
    """
    B2 未来剧本缓存 v0.2
    
    核心职责：
    - TTL 管理（支持动态 TTL，C阶段增强）
    - 缓存未来剧本
    - 避免频繁运行
    """
    
    def __init__(self, ttl_sec: float = 10.0):
        """
        初始化缓存
        
        Args:
            ttl_sec: TTL 过期时间（秒），默认 10 秒（会被动态 TTL 覆盖）
        """
        self.base_ttl_sec = ttl_sec
        self.current_ttl_sec = ttl_sec  # 当前动态 TTL
        self._last_run_ts: Optional[float] = None
        self._last_advisory: Optional[B2Advisory] = None
        self._last_corridor_sig: Optional[str] = None
        self._last_objects_count: int = 0
    
    def set_dynamic_ttl(self, ttl_sec: float):
        """
        设置动态 TTL（C阶段：决策节律动态拉长）
        
        Args:
            ttl_sec: 动态 TTL（秒）
        """
        self.current_ttl_sec = ttl_sec
    
    def should_run(self, timestamp: float) -> bool:
        """
        判断是否应该运行 B2
        
        触发条件（任一）：
        - TTL 到期
        - corridor 变化
        - 新动态对象出现
        - 上一次有风险
        
        Args:
            timestamp: 当前时间戳
        
        Returns:
            bool: 是否应该运行
        """
        # 首次运行
        if self._last_run_ts is None:
            return True
        
        # TTL 到期（使用动态 TTL）
        elapsed = timestamp - self._last_run_ts
        if elapsed >= self.current_ttl_sec:
            return True
        
        # 其他触发条件在 B2Controller 中处理
        return False
    
    def update(
        self,
        timestamp: float,
        advisory: Optional[B2Advisory],
        corridor_sig: Optional[str] = None,
        objects_count: int = 0,
    ):
        """
        更新缓存
        
        Args:
            timestamp: 当前时间戳
            advisory: B2 Advisory（可选）
            corridor_sig: 走廊签名（可选）
            objects_count: 对象数量（可选）
        """
        self._last_run_ts = timestamp
        self._last_advisory = advisory
        if corridor_sig is not None:
            self._last_corridor_sig = corridor_sig
        if objects_count > 0:
            self._last_objects_count = objects_count
    
    def get_last_advisory(self) -> Optional[B2Advisory]:
        """获取最后一次的 Advisory"""
        return self._last_advisory

