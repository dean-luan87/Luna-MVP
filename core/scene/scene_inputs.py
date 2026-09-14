# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B: Scene Inputs（场景输入统一封装）

职责：
- 统一封装所有场景输入源（GPS / Map / Vision / Behavior）
- 后续 GPS / Map / Vision 都只喂 SceneInputs

原则：
- 不直接暴露原始数据
- 只提供"提示"（hint），不做判断
- 时间/天气作为环境上下文，不触发场景切换
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import time

from .environment_context import EnvironmentContext


@dataclass
class SceneInputs:
    """
    场景输入（统一封装）
    
    所有场景输入源的统一接口：
    - geometry_hint: 几何提示（GPS / 惯导 / 视觉推断）
    - semantic_hint: 语义提示（离线地图 / OCR / 视觉标识）
    - behavior_hint: 行为提示（用户行为稳定性）
    - environment_context: 环境上下文（时间/天气/季节）- 只影响权重，不触发切换
    - timestamp: 时间戳
    
    后续 GPS / Map / Vision 都只喂 SceneInputs。
    
    重要约定：
    - 时间/天气不是场景切换条件，而是"环境修正因子"
    - 它们能改变风险权重、通行可信度、任务建议倾向
    - 它们不能直接切 Scene 或生成新 SceneSegment
    """
    geometry_hint: Optional[Dict[str, Any]] = None  # GPS / 惯导 / 视觉推断
    semantic_hint: Optional[Dict[str, Any]] = None  # 离线地图 / OCR / 视觉标识
    behavior_hint: Optional[Dict[str, Any]] = None  # 用户行为稳定性
    environment_context: Optional[EnvironmentContext] = None  # 环境上下文（时间/天气/季节）
    timestamp: float = field(default_factory=time.time)
    
    def is_valid(self) -> bool:
        """
        判断输入是否有效
        
        Returns:
            bool: 是否至少有一个 hint 不为空
        """
        return (
            self.geometry_hint is not None or
            self.semantic_hint is not None or
            self.behavior_hint is not None
        )

