# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Segment Runtime（场景段运行时状态）

职责：
- SceneRuntime 的定义与管理
- 维护场景段的 relevance、confidence、lifecycle_state

原则：
- relevance 用于渐变切换
- confidence 仅慢升快降
- lifecycle_state: ACTIVE / CANDIDATE / FADING
"""

from dataclasses import dataclass, field
import time


@dataclass
class SceneRuntime:
    """
    场景段运行时状态
    
    字段说明：
    - relevance: 当前相关度 [0.0 ~ 1.0]，用于渐变切换
    - confidence: 可信度 [0.0 ~ 1.0]，仅慢升快降
    - lifecycle_state: 生命周期状态（ACTIVE / CANDIDATE / FADING）
    - first_seen_ts: 首次出现时间戳
    - last_update_ts: 最后更新时间戳
    """
    relevance: float = 0.0
    confidence: float = 0.0
    lifecycle_state: str = "ACTIVE"  # ACTIVE | CANDIDATE | FADING
    first_seen_ts: float = field(default_factory=time.time)
    last_update_ts: float = field(default_factory=time.time)


