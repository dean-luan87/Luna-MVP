"""
C1 基础类型定义（API 契约）

这是 C1 的"API 契约"，后面不要随便改。
所有字段都"可假造"，不依赖模型。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class C1Input:
    """
    C1 输入信号
    
    所有字段都"可假造"，不依赖模型。
    """
    timestamp: float

    # 稳定性 / 运动
    motion_score: float          # 镜头晃动强度（0~1）
    frame_diff_score: float      # 帧变化幅度（0~1）

    # 世界与记忆提示
    next_scene_hint: Optional[str] = None
    risk_hint: Optional[str] = None

    # 隐私与用户
    privacy_zone: Optional[str] = None   # A / B / C
    user_camera_override: bool = False


@dataclass
class C1Decision:
    """
    C1 输出决策
    
    PipelineController 只依赖这个结果，其余一概不关心。
    """
    allow_frame: bool
    target_fps: int
    observation_mode: str        # forward / surround / local
    priority: str                # safety / navigation / environment
    reason: str
