"""
C1 Replay Tool 数据模型

定义两类记录：
1. C1 决策记录（C1DecisionRecord）
2. Pipeline 执行记录（PipelineExecutionRecord）
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class C1DecisionRecord:
    """
    C1 决策记录
    
    每一次 C1 决策的结构化记录。
    """
    timestamp: float

    prev_state: str
    current_state: str

    motion_score: float
    frame_diff_score: float

    privacy_hit: bool
    user_override: bool

    allow_frame: bool
    target_fps: int
    priority: str
    observation_mode: str

    reason: str


@dataclass
class PipelineExecutionRecord:
    """
    Pipeline 执行记录
    
    Pipeline 执行摘要，用于验证 C1 决策是否被正确执行。
    """
    timestamp: float
    navigation_executed: bool
    modeling_executed: bool
    latency_ms: float
