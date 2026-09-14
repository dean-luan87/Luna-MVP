# -*- coding: utf-8 -*-
"""
主线 1：决策显示器（Decision Monitor）— 目标驱动的感知—理解—决策—行动链 + 决策显示器。

开发态「真相窗」：每关键周期产出一条 DecisionMonitorFrame（六层：goal / inputs / state / decision / outputs / consequence），
输出 JSONL + 终端摘要，不做复杂 UI。
"""

from .schema import (
    DecisionMonitorFrame,
    GoalLayer,
    InputsLayer,
    StateLayer,
    DecisionLayer,
    OutputsLayer,
    ConsequenceLayer,
    LocalGoalState,
)
from .builder import DecisionMonitorBuilder
from .logger import DecisionMonitorLogger

__all__ = [
    "DecisionMonitorFrame",
    "GoalLayer",
    "InputsLayer",
    "StateLayer",
    "DecisionLayer",
    "OutputsLayer",
    "ConsequenceLayer",
    "LocalGoalState",
    "DecisionMonitorBuilder",
    "DecisionMonitorLogger",
]
