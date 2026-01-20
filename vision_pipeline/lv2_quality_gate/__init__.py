# -*- coding: utf-8 -*-
"""
LV2: Quality Gate（质量过滤层）

职责：
- 用最小算力，筛掉不值得浪费后端资源的帧
- 纯物理质量评估，不涉及任何语义

本模块禁止做什么：
- ❌ 禁止做任何语义理解
- ❌ 禁止调用下游模块
- ❌ 禁止修改输入帧
- ❌ 禁止触发重拍请求
"""

from .quality_gate import QualityGate, QualityResult

__all__ = ["QualityGate", "QualityResult"]


