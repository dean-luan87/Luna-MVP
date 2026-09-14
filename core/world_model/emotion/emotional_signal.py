# -*- coding: utf-8 -*-
"""
v1.8.5 Phase D Lite: Emotional Signal（情绪信号，占位结构）

职责：
- 定义情绪信号的数据结构
- 这是信号，不是事实
- 一期不做复杂分类，枚举即可

设计原则：
- confidence 默认 ≤ 0.3（一期通常很低）
- 这是信号，不是事实
- 不参与事实判断，只影响体验权重
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EmotionalSignal:
    """
    情绪信号（占位结构）
    
    注意：
    - 这是信号，不是事实
    - confidence 默认 ≤ 0.3（一期通常很低）
    - 一期不做复杂分类，枚举即可
    
    字段说明：
    - source: 来源（"dialog" | "voice" | "behavior"）
    - emotion: 情绪类型（"anxious" | "calm" | "irritated" | "happy" | "neutral"）
    - intensity: 强度 [0.0 ~ 1.0]
    - confidence: 置信度 [0.0 ~ 1.0]（一期通常很低，默认 ≤ 0.3）
    - ts: 时间戳
    - ttl_s: 生存时间（秒，默认 5~15 分钟）
    """
    source: str  # "dialog" | "voice" | "behavior"
    emotion: str  # "anxious" | "calm" | "irritated" | "happy" | "neutral"
    intensity: float  # 0~1
    confidence: float = 0.3  # 0~1（一期通常很低，默认 ≤ 0.3）
    ts: Optional[float] = None
    ttl_s: float = 600.0  # 默认 10 分钟（快衰减）
    
    def __post_init__(self):
        """后处理：确保 confidence 不超过一期上限"""
        if self.confidence > 0.3:
            self.confidence = 0.3
        
        if self.ts is None:
            import time
            self.ts = time.time()
    
    def is_expired(self, now_ts: Optional[float] = None) -> bool:
        """
        检查信号是否已过期
        
        Args:
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            bool: True 表示已过期
        """
        if now_ts is None:
            import time
            now_ts = time.time()
        
        return (now_ts - self.ts) > self.ttl_s
    
    def get_valence(self) -> float:
        """
        获取情绪效价（-1 ~ +1）
        
        Returns:
            float: 情绪效价（-1 为负面，+1 为正面，0 为中性）
        """
        valence_map = {
            "anxious": -0.7,
            "irritated": -0.5,
            "calm": 0.3,
            "happy": 0.8,
            "neutral": 0.0,
        }
        base_valence = valence_map.get(self.emotion, 0.0)
        return base_valence * self.intensity


