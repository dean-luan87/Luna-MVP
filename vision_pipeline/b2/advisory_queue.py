"""
Advisory Queue - B2 → C 的唯一接口

B2 → C 对接方案：结构化 Advisory Queue

核心原则：
- B2 永远不控制 C
- B2 只提供"未来信息包（Future Advisory）"
- C 可以：用、不用、延迟用、降权用
- 但 B2 没有否决权
"""

from collections import deque
from typing import List, Optional
from .b2_types_v02 import B2Advisory


class AdvisoryQueue:
    """
    B2 Advisory 队列（C 可读取）
    
    核心职责：
    - 存储 B2 产生的 Advisory
    - 提供 C 只读接口
    - 自动过期管理
    """
    
    def __init__(self, max_active: int = 3):
        """
        初始化 Advisory Queue
        
        Args:
            max_active: 最大活跃 Advisory 数量（防爆炸规则）
        """
        self.queue = deque(maxlen=max_active)  # 自动限制大小
        self.max_active = max_active
    
    def push(self, advisory: B2Advisory):
        """
        推送新的 Advisory
        
        Args:
            advisory: B2 Advisory
        """
        # 如果队列已满，自动丢弃最旧的（deque maxlen 自动处理）
        self.queue.append(advisory)
    
    def get_active(self, now_ts: float) -> List[B2Advisory]:
        """
        获取活跃的 Advisory（C 只读接口）
        
        ⚠️ 注意：
        - C 只读 get_active
        - 不 pop、不 ack、不修改
        
        Args:
            now_ts: 当前时间戳
        
        Returns:
            List[B2Advisory]: 活跃的 Advisory 列表
        """
        active = []
        for adv in self.queue:
            # 检查是否过期（使用 B2Advisory 的 property）
            ttl_sec = adv.ttl_sec
            timestamp = adv.timestamp
            if timestamp > 0 and (now_ts - timestamp) <= ttl_sec:
                active.append(adv)
            elif timestamp == 0:
                # 如果没有 timestamp，默认有效（兼容旧数据）
                active.append(adv)
        
        return active
    
    def clear_expired(self, now_ts: float):
        """
        清理过期的 Advisory（可选，用于维护）
        
        Args:
            now_ts: 当前时间戳
        """
        # 简化：deque 会自动限制大小，过期项会在下次 get_active 时被过滤
        pass
    
    def count(self) -> int:
        """获取队列中的 Advisory 数量"""
        return len(self.queue)

