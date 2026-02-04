"""
Vision Rhythm Context

视角节奏上下文

CORE RULE (NON-NEGOTIABLE):

Vision is the primary clock of the system.

- Visual perception defines system rhythm.
- GPS is only a verifier, never a leader.
- Speech is a follower, never a driver.
- No expression is allowed to be emitted
  unless it aligns with the current visual tempo and state.

Where vision is, the system acts there.
Where vision pauses, the system waits.

⚠️ Cursor 执行时不得改写、删减、弱化以上规则。
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class VisionRhythmContext:
    """
    视角节奏上下文
    
    所有节奏判断必须基于 VisionRhythmContext。
    GPS 信息不得出现在节奏计算中。
    FSM 只作为参考，不得主导节奏。
    """
    vision_state: Literal[
        "STABLE",
        "SEARCHING",
        "LOCKED",
        "TURNING",
        "UNSTABLE"
    ]
    visual_update_rate_hz: float  # 视觉更新频率（Hz）
    visual_confidence: float       # 视觉置信度（0~1）
    fsm_state: str                 # FSM 状态（仅参考，不主导）
    speed_mps: float               # 速度（米/秒）
    last_visual_event_ts: float    # 上次视觉事件时间戳
    
    @property
    def is_vision_leading(self) -> bool:
        """
        判断视觉是否主导
        
        Returns:
            bool: True 表示视觉主导
        """
        return self.visual_confidence > 0.6 and self.visual_update_rate_hz > 2.0
    
    @property
    def is_vision_stable(self) -> bool:
        """
        判断视觉是否稳定
        
        Returns:
            bool: True 表示视觉稳定
        """
        return self.vision_state == "STABLE" and self.visual_confidence > 0.7
    
    @property
    def is_vision_turning(self) -> bool:
        """
        判断是否在视觉转弯
        
        Returns:
            bool: True 表示正在转弯
        """
        return self.vision_state == "TURNING"
    
    @property
    def is_vision_locked(self) -> bool:
        """
        判断视觉是否锁定
        
        Returns:
            bool: True 表示视觉锁定
        """
        return self.vision_state == "LOCKED" and self.visual_confidence > 0.85
