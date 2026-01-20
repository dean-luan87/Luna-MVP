"""
Advisory Cache - B2 v0.2 缓存逻辑：第三层

建议缓存（AdvisoryCache）

核心思想：
避免同一句"前方安全"反复告诉 C

这是决策数自然下降的关键机制。
"""

import time
from typing import Optional, Tuple
from .b2_types_v02 import B2Advisory
from .world_signature import WorldSignature


class AdvisoryCache:
    """
    B2 v0.2 缓存逻辑：第三层 - 建议缓存
    
    核心职责：
    - 抑制重复的 advisory 输出
    - 避免同一句"前方安全"反复告诉 C
    - 决策数自然下降
    
    设计原则：
    - Advisory TTL（15-20s）比 Future TTL（8s）更长
    - 原因：事实更新 ≠ 建议更新
    """
    
    def __init__(self, ttl_sec: float = 15.0):
        """
        初始化建议缓存
        
        Args:
            ttl_sec: Advisory TTL（秒），默认 15 秒
        """
        self.ttl_sec = ttl_sec
        self._last_advisory: Optional[B2Advisory] = None
        self._last_world_signature: Optional[WorldSignature] = None
        self._last_emit_ts: Optional[float] = None
    
    def should_suppress(
        self,
        advisory: B2Advisory,
        world_signature: WorldSignature,
        current_ts: float,
    ) -> Tuple[bool, Optional[float]]:
        """
        Task 3.2: Advisory 抑制逻辑
        
        抑制条件（全部满足）：
        1. advisory.type == last_advisory.type
        2. world_signature == last_world_signature
        3. within_advisory_ttl
        
        Args:
            advisory: 当前生成的 Advisory
            world_signature: 当前世界指纹
            current_ts: 当前时间戳
        
        Returns:
            Tuple[bool, Optional[float]]: (是否抑制, 缓存年龄)
        """
        # 首次输出，不抑制
        if self._last_advisory is None:
            return False, None
        
        # 1. Advisory 类型是否一致
        if self._last_advisory.advisory_type != advisory.advisory_type:
            return False, None
        
        # 2. WorldSignature 是否一致（使用 digest 比较）
        if self._last_world_signature is None:
            return False, None
        if self._last_world_signature.digest() != world_signature.digest():
            return False, None
        
        # 3. 是否在 TTL 内
        if self._last_emit_ts is None:
            return False, None
        elapsed = current_ts - self._last_emit_ts
        if elapsed >= self.ttl_sec:
            return False, None
        
        # 全部满足，抑制输出
        return True, elapsed
    
    def update(
        self,
        advisory: B2Advisory,
        world_signature: WorldSignature,
        current_ts: float,
    ):
        """
        更新缓存（只有在输出时调用）
        
        Args:
            advisory: 输出的 Advisory
            world_signature: 当前世界指纹
            current_ts: 当前时间戳
        """
        self._last_advisory = advisory
        self._last_world_signature = world_signature
        self._last_emit_ts = current_ts
    
    def get_last_advisory(self) -> Optional[B2Advisory]:
        """获取最后一次的 Advisory"""
        return self._last_advisory

