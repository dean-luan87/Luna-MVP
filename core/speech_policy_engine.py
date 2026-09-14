# -*- coding: utf-8 -*-
"""
播报策略引擎（Speech Policy Engine）

v1.8.2: 基于优先级的播报决策
"""

from core.speech_deduplicator import SpeechDeduplicator


class SpeechPolicyEngine:
    """播报策略引擎"""
    
    def __init__(self):
        """初始化播报策略引擎"""
        self.deduplicator = SpeechDeduplicator()
    
    def should_speak(
        self,
        text: str,
        priority: int,
        scene_is_stable: bool
    ) -> bool:
        """
        判断是否应该播报（最终裁决）
        
        Args:
            text: 要播报的文本
            priority: 播报优先级（3=危险, 2=提醒, 1=描述）
            scene_is_stable: 场景是否稳定
        
        Returns:
            bool: True 表示应该播报，False 表示不应该播报
        """
        # priority 3 = danger, always allowed (still deduped)
        if priority == 3:
            return self.deduplicator.should_speak(text)
        
        if scene_is_stable:
            return False
        
        return self.deduplicator.should_speak(text)
