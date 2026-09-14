"""
B2 World Accumulator - 世界去抖动 + 世界稳定判断

职责：
- 世界去抖动
- 世界稳定判断
- 支撑"上帝视角"
"""

from typing import Dict, Any, Optional
from collections import deque
from .b2_digest import compute_world_digest, digest_delta


class WorldAccumulator:
    """
    B2 世界累积器
    
    核心职责：
    - 世界去抖动（使用滑动窗口）
    - 世界稳定判断（基于 digest 稳定性）
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化世界累积器
        
        Args:
            config: 配置字典，包含：
                - stability_window_size: 稳定窗口大小（默认 5）
                - stability_threshold: 稳定阈值（默认 0.1）
        """
        self.config = config or {}
        self.stability_window_size = self.config.get("stability_window_size", 5)
        self.stability_threshold = self.config.get("stability_threshold", 0.1)
        
        # 滑动窗口：存储最近的 digest
        self.digest_window: deque = deque(maxlen=self.stability_window_size)
        self.last_digest: Optional[tuple] = None
    
    def update(self, world_snapshot: Dict[str, Any]) -> bool:
        """
        更新世界快照，判断是否稳定
        
        Args:
            world_snapshot: 世界快照，包含 world_update 字典
        
        Returns:
            bool: 是否稳定
        """
        world_update = world_snapshot.get("world_update", {}) or {}
        digest = compute_world_digest(world_update)
        
        # 添加到滑动窗口
        self.digest_window.append(digest)
        self.last_digest = digest
        
        # 判断稳定性：窗口内所有 digest 的变化量都小于阈值
        if len(self.digest_window) < self.stability_window_size:
            return False
        
        # 计算窗口内所有 digest 之间的最大变化量
        max_delta = 0.0
        for i in range(len(self.digest_window)):
            for j in range(i + 1, len(self.digest_window)):
                delta = digest_delta(self.digest_window[i], self.digest_window[j])
                max_delta = max(max_delta, delta)
        
        # 如果最大变化量小于阈值，认为稳定
        return max_delta < self.stability_threshold

