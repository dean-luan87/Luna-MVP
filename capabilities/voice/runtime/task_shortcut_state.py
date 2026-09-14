# -*- coding: utf-8 -*-
"""
TaskShortcutState (Stage-1 placeholder).

用于“任务短指令入口”的受控状态占位。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TaskShortcutState:
    enabled: bool = False
    last_used_ts: float = 0.0

