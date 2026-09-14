# -*- coding: utf-8 -*-
"""
v1.8.5 Phase D Lite: Emotion Port（情绪信号入口）

职责：
- 提供 ingest(signal) 接口
- 内部只缓存，不扩散
- 必须继承 Phase B/C 的护栏

设计原则：
- 情绪信号 → EmotionalContext → ContextBundle → TaskPlanner（软影响）
- 绝对禁止：EmotionalSignal → SceneRegistry/MapRegistry/LibraryRegistry
- 只允许：情绪 → 体验记忆（低权重、快衰减）
- 必须继承 Phase B/C 的护栏（位置失衡 Gate、限频、衰减）
"""

import time
from typing import Optional, Dict, Any

from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes
from core.world_model.common.rate_limiter import SimpleRateLimiter
from .emotional_signal import EmotionalSignal
from .emotional_context import EmotionalContext


class EmotionPort:
    """
    情绪信号入口（占位接口）
    
    设计原则：
    - 情绪信号 → EmotionalContext → ContextBundle → TaskPlanner（软影响）
    - 绝对禁止：EmotionalSignal → SceneRegistry/MapRegistry/LibraryRegistry
    - 只允许：情绪 → 体验记忆（低权重、快衰减）
    - 必须继承 Phase B/C 的护栏
    
    护栏：
    1. 位置失衡 Gate：drift_suspected / relocalizing → 情绪信号不写入
    2. 限频：同一用户、同一场景、短时间内情绪信号合并
    3. 衰减：EmotionalSignal 必须自带 TTL（如 5~15 分钟）
    """
    
    def __init__(
        self,
        rate_limiter: Optional[SimpleRateLimiter] = None,
        enable_emotion_influence: bool = False,  # 默认关闭
    ):
        """
        初始化情绪信号入口
        
        Args:
            rate_limiter: 限频器（如果为 None 则创建默认实例）
            enable_emotion_influence: 是否启用情绪影响（默认 False，一期关闭）
        """
        self.rate_limiter = rate_limiter or SimpleRateLimiter(window_s=60.0)  # 60 秒窗口
        self.enable_emotion_influence = enable_emotion_influence
        self.context = EmotionalContext()
    
    def ingest(
        self,
        signal: EmotionalSignal,
        user_id: str,
        scene_id: str,
        position_state: PositionState,
        now_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        处理情绪信号（入口）
        
        规则：
        - 位置失衡 Gate：drift_suspected / relocalizing → 情绪信号不写入
        - 限频：同一用户、同一场景、短时间内情绪信号合并
        - 衰减：EmotionalSignal 必须自带 TTL（如 5~15 分钟）
        
        Args:
            signal: 情绪信号
            user_id: 用户 ID
            scene_id: 场景 ID
            position_state: 位置状态
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Dict[str, Any]: 处理结果（accepted, reason）
        """
        now = now_ts or signal.ts or time.time()
        
        # Gate 1：位置失衡 Gate（继承 Phase B/C）
        if should_freeze_world_writes(position_state):
            return {"accepted": False, "reason": "world_write_frozen"}
        
        # Gate 2：限频（同一用户、同一场景、短时间内情绪信号合并）
        key = f"{user_id}:{scene_id}:{signal.emotion}"
        if not self.rate_limiter.allow(key, now_ts=now):
            return {"accepted": False, "reason": "rate_limited"}
        
        # Gate 3：清理过期信号
        self.context.clear_expired(now_ts=now)
        
        # 添加信号
        self.context.add_signal(signal, now_ts=now)
        
        return {
            "accepted": True,
            "reason": "emotion_signal_recorded",
            "aggregate_valence": self.context.aggregate_valence,
            "signal_count": len(self.context.signals),
        }
    
    def get_context(self) -> EmotionalContext:
        """
        获取情绪上下文（只读）
        
        Returns:
            EmotionalContext: 情绪上下文
        """
        return self.context
    
    def clear(self) -> None:
        """清空情绪上下文"""
        self.context = EmotionalContext()


