# -*- coding: utf-8 -*-
"""
v1.8.5 Phase D Lite: Emotional Context（情绪上下文，只读、只叠加）

职责：
- 聚合多个情绪信号
- 只作为 ContextBundle 的附加信息
- 不单独存 Library
- 不影响 SceneRegistry

设计原则：
- 只读、只叠加
- 不参与事实判断
- 只影响体验权重
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .emotional_signal import EmotionalSignal


@dataclass
class EmotionalContext:
    """
    情绪上下文（只读、只叠加）
    
    注意：
    - 只作为 ContextBundle 的附加信息
    - 不单独存 Library
    - 不影响 SceneRegistry
    - 不参与事实判断，只影响体验权重
    
    字段说明：
    - signals: 情绪信号列表
    - aggregate_valence: 聚合效价（-1 ~ +1，简单加权）
    - last_update_ts: 最后更新时间戳
    """
    signals: List[EmotionalSignal] = field(default_factory=list)
    aggregate_valence: float = 0.0  # -1 ~ +1（简单加权）
    last_update_ts: Optional[float] = None
    
    def add_signal(self, signal: EmotionalSignal, now_ts: Optional[float] = None) -> None:
        """
        添加情绪信号（并更新聚合效价）
        
        Args:
            signal: 情绪信号
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        """
        if now_ts is None:
            import time
            now_ts = time.time()
        
        # 清理过期信号
        self.signals = [s for s in self.signals if not s.is_expired(now_ts)]
        
        # 添加新信号
        self.signals.append(signal)
        
        # 更新聚合效价（简单加权平均）
        if self.signals:
            total_valence = sum(s.get_valence() * s.confidence for s in self.signals)
            total_confidence = sum(s.confidence for s in self.signals)
            if total_confidence > 0:
                self.aggregate_valence = total_valence / total_confidence
            else:
                self.aggregate_valence = 0.0
        else:
            self.aggregate_valence = 0.0
        
        self.last_update_ts = now_ts
    
    def clear_expired(self, now_ts: Optional[float] = None) -> int:
        """
        清理过期信号
        
        Args:
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            int: 清理的信号数量
        """
        if now_ts is None:
            import time
            now_ts = time.time()
        
        before_count = len(self.signals)
        self.signals = [s for s in self.signals if not s.is_expired(now_ts)]
        after_count = len(self.signals)
        
        # 重新计算聚合效价
        if self.signals:
            total_valence = sum(s.get_valence() * s.confidence for s in self.signals)
            total_confidence = sum(s.confidence for s in self.signals)
            if total_confidence > 0:
                self.aggregate_valence = total_valence / total_confidence
            else:
                self.aggregate_valence = 0.0
        else:
            self.aggregate_valence = 0.0
        
        return before_count - after_count
    
    def is_empty(self) -> bool:
        """
        检查是否为空
        
        Returns:
            bool: True 表示为空
        """
        return len(self.signals) == 0


