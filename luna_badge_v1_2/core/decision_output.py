# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 决策输出结构定义

定义 DecisionOutput 结构，表示决策层的输出结果。
"""

from dataclasses import dataclass
from typing import Dict, Optional
from .decision_actions import DecisionAction


@dataclass
class DecisionOutput:
    """
    决策输出结构
    
    Attributes:
        action: 决策动作类型（DecisionAction 枚举值）
        params: 动作参数，如 insert_task_spec / new_task_spec / question_type 等
        narration: 给 TTS 播报用的自然语言文案
    """
    action: DecisionAction
    params: Optional[Dict] = None      # 如 insert_task_spec / new_task_spec / question_type 等
    narration: str = ""                # 给 TTS 播报用的自然语言文案
    
    def __post_init__(self):
        """初始化后处理：确保 params 不为 None"""
        if self.params is None:
            self.params = {}
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"DecisionOutput(action={self.action.value}, "
            f"params={self.params}, narration='{self.narration[:30]}...')"
        )


