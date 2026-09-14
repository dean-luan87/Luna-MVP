# -*- coding: utf-8 -*-
"""
RestrictedDeviceModeState (Stage-1 placeholder).

受限设备模式优先级最高：限制输入/输出与执行权限。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RestrictedDeviceModeState:
    enabled: bool = False
    reason: str = ""

