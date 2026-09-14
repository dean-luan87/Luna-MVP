#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视觉输出状态枚举 (v1.8.1)

功能：定义视觉输出的三种状态
原则：不包含任何判断逻辑，仅定义枚举
"""

from enum import Enum


class VisionOutputState(str, Enum):
    """
    视觉输出状态枚举
    
    定义视觉识别输出的三种状态：
    - BACKGROUND: 后台观察模式
    - CONFIRM: 确认模式（需要用户确认）
    - INTERVENE: 干预模式（必须打断）
    """
    BACKGROUND = "background"
    CONFIRM = "confirm"
    INTERVENE = "intervene"


