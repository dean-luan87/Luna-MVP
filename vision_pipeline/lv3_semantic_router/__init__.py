# -*- coding: utf-8 -*-
"""
LV3: Semantic Router（一级语义调度层）

职责：
- 决定这帧是否必须进入实时链路
- 只做粗分类，不做理解

本模块禁止做什么：
- ❌ 禁止做深度语义理解
- ❌ 禁止直接调用 LV4.1 或 LV4.2
- ❌ 禁止修改任务态
- ❌ 禁止触发感知重拍
"""

from .semantic_router import SemanticRouter, RouteResult

__all__ = ["SemanticRouter", "RouteResult"]


