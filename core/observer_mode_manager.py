#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observer Mode 状态管理器 (v1.8.1)

功能：管理观察模式的激活、状态和生命周期
原则：不破坏 v1.8 冻结态，可随时关闭回滚
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class ObserverLevel(str, Enum):
    """观察模式级别"""
    BACKGROUND = "background"  # 后台观察
    CONFIRM = "confirm"  # 确认模式
    INTERVENE = "intervene"  # 干预模式


@dataclass
class ObserverMode:
    """
    Observer Mode 状态对象
    
    用于管理观察模式的激活状态和级别
    """
    active: bool = False
    level: str = ObserverLevel.BACKGROUND.value
    confidence: float = 1.0
    last_trigger: Optional[float] = None
    trigger_reason: Optional[str] = None


def init_observer_mode() -> ObserverMode:
    """
    初始化 Observer Mode 对象
    
    Returns:
        ObserverMode: 初始化的观察模式对象（默认未激活）
    """
    return ObserverMode(
        active=False,
        level=ObserverLevel.BACKGROUND.value,
        confidence=1.0,
        last_trigger=None,
        trigger_reason=None
    )


def should_activate_observer(context: Dict[str, Any]) -> bool:
    """
    Observer Mode 激活判断函数
    
    判断是否应该激活观察模式，仅返回 true/false，不触发任何状态变更
    
    Args:
        context: 上下文信息，可包含：
            - navigation_state: 导航状态
            - scene_type: 场景类型
            - user_utterance: 用户语音输入（字符串）
    
    Returns:
        bool: True 表示应该激活，False 表示不激活
    
    激活条件（任一满足）：
        - navigation_state == "active"
        - scene_type 属于复杂场景集合（hospital / mall / metro / gov）
        - user_utterance 命中关键词："帮我看" / "不确定" / "是不是"
    """
    # 条件1: 导航状态激活
    navigation_state = context.get("navigation_state", "")
    if navigation_state == "active":
        return True
    
    # 条件2: 复杂场景
    complex_scenes = {"hospital", "mall", "metro", "gov", "gov_hall"}
    scene_type = context.get("scene_type", "")
    if scene_type in complex_scenes:
        return True
    
    # 条件3: 用户语音触发
    user_utterance = context.get("user_utterance", "")
    if user_utterance:
        trigger_keywords = ["帮我看", "不确定", "是不是"]
        user_utterance_lower = user_utterance.lower()
        for keyword in trigger_keywords:
            if keyword in user_utterance_lower:
                return True
    
    return False


def update_observer_lifecycle(
    observer_mode: ObserverMode,
    event: str
) -> ObserverMode:
    """
    Observer Mode 生命周期控制
    
    根据事件更新观察模式的生命周期状态
    
    Args:
        observer_mode: 当前的观察模式对象
        event: 生命周期事件，可选值：
            - "task_end": 任务结束
            - "user_opt_out": 用户选择退出
            - "timeout": 超时
    
    Returns:
        ObserverMode: 更新后的观察模式对象
    
    规则：
        - task_end 或 user_opt_out 时，将 observer_mode.active 设为 false
        - 不删除 observer_mode 对象
        - 不影响 v1.8 原任务结束逻辑
    """
    # 创建新对象，避免修改原对象（函数式编程）
    updated_mode = ObserverMode(
        active=observer_mode.active,
        level=observer_mode.level,
        confidence=observer_mode.confidence,
        last_trigger=observer_mode.last_trigger,
        trigger_reason=observer_mode.trigger_reason
    )
    
    # 处理生命周期事件
    if event in ("task_end", "user_opt_out"):
        updated_mode.active = False
        # 最小日志输出（用于调试）
        print(f"[ObserverMode] Lifecycle event: {event}, deactivated")
    elif event == "timeout":
        # 超时处理（可根据需求扩展）
        updated_mode.active = False
        print(f"[ObserverMode] Lifecycle event: {event}, deactivated")
    
    return updated_mode

