# -*- coding: utf-8 -*-
"""
Luna Badge v1.4.3 - 意图解析结果结构定义

定义 ParsedIntent 结构，用于表示用户意图的解析结果。
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ParsedIntent:
    """
    解析后的用户意图结构
    
    Attributes:
        intent_name: 意图名称，如 INSERT_TASK / CHANGE_DESTINATION / CONFIRM / 
                     REJECT / RESUME_MAIN_TASK / AMBIGUOUS / UNKNOWN 等
        slots: 结构化参数，如 {"task_type": "toilet"} / {"destination": "hospital"} 等
        source: 意图来源，"inquiry" / "asr" / "system"
        need_confirm: 是否需要二次确认
        raw: 原始用户输入文本
    """
    intent_name: str          # e.g. INSERT_TASK, CHANGE_DESTINATION, CONFIRM, REJECT, RESUME_MAIN_TASK, AMBIGUOUS, UNKNOWN
    slots: Optional[Dict] = None        # structured args, like {"task_type": "toilet"}
    source: str = "inquiry"   # "inquiry" | "asr" | "system"
    need_confirm: bool = False
    raw: str = ""
    
    def __post_init__(self):
        """初始化后处理：确保 slots 不为 None"""
        if self.slots is None:
            self.slots = {}
    
    def __repr__(self) -> str:
        """字符串表示"""
        return (
            f"ParsedIntent(intent_name='{self.intent_name}', "
            f"slots={self.slots}, source='{self.source}', "
            f"need_confirm={self.need_confirm}, raw='{self.raw[:30]}...')"
        )













