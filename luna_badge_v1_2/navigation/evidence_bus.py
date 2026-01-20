"""
Evidence Bus (v1.4.8 Step 5)

重要禁令：
- 本模块当前为 Skeleton 插桩版，不得修改现有导航控制逻辑
- 只负责证据存储、衰减、查询
- 不参与导航决策
"""

from collections import deque
from typing import List, Optional
import time
from navigation.evidence_models import Evidence


class EvidenceBus:
    """
    证据总线：存储/衰减/查询
    
    职责：
    - 维护滑动窗口
    - 存储证据
    - 清理过期证据
    """
    
    def __init__(self, window_s: float = 10.0, enable_debug_log: bool = False):
        """
        初始化证据总线
        
        Args:
            window_s: 滑动窗口大小（秒）
            enable_debug_log: 是否启用调试日志
        """
        self.window_s = window_s
        self.enable_debug_log = enable_debug_log
        self._evidences: deque = deque()  # 内部存储：collections.deque
    
    def add(self, evidence: Evidence) -> None:
        """
        添加证据
        
        Args:
            evidence: 证据对象
        """
        self._evidences.append(evidence)
        
        # 日志插桩
        if self.enable_debug_log:
            print(
                f"[EVIDENCE_ADD] kind={evidence.kind.value} "
                f"src={evidence.source.value} value={evidence.value:.3f} "
                f"ttl={evidence.ttl_s:.1f}s meta={evidence.meta}"
            )
    
    def get_window(self, now_ts: Optional[float] = None) -> List[Evidence]:
        """
        获取窗口内未过期的证据
        
        Args:
            now_ts: 当前时间戳（默认 time.time()）
            
        Returns:
            未过期的证据列表
        """
        if now_ts is None:
            now_ts = time.time()
        
        # 先清理过期证据
        self.purge(now_ts)
        
        # 返回窗口内所有证据
        return list(self._evidences)
    
    def purge(self, now_ts: Optional[float] = None) -> int:
        """
        清理过期证据
        
        Args:
            now_ts: 当前时间戳（默认 time.time()）
            
        Returns:
            清理的证据数量
        """
        if now_ts is None:
            now_ts = time.time()
        
        removed_count = 0
        valid_evidences = deque()
        
        for evidence in self._evidences:
            # 检查是否过期（基于 TTL）
            age = now_ts - evidence.ts
            if age <= evidence.ttl_s:
                # 检查是否在窗口内
                if age <= self.window_s:
                    valid_evidences.append(evidence)
            else:
                removed_count += 1
        
        self._evidences = valid_evidences
        
        # 日志插桩
        if self.enable_debug_log and removed_count > 0:
            print(
                f"[EVIDENCE_PURGE] removed={removed_count} remain={len(self._evidences)}"
            )
        
        return removed_count
    
    def size(self) -> int:
        """获取当前证据数量"""
        return len(self._evidences)
    
    def clear(self) -> None:
        """清空所有证据"""
        self._evidences.clear()






