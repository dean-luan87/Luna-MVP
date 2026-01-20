# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B: Vision Pipeline（视觉流水线中台）

职责：
- 视觉感知 → 世界模型之间的工程化中介层
- 实现 LV2-LV7 的完整流程
- 切断视觉输入 → core 的直通路径

设计原则：
- 这是中台，不属于 core/world_model
- 所有视觉结果必须先进入 vision_pipeline
- core/world_model 只能接收来自 modeling_executor 的候选或 UserReportRouter 的用户反馈
"""

from .lv2_quality_gate.quality_gate import QualityGate, QualityResult
from .lv3_semantic_router.semantic_router import SemanticRouter, RouteResult
from .lv4_executors.navigation_executor import NavigationExecutor, NavigationResult
from .lv4_executors.modeling_executor import ModelingExecutor, ModelingResult
from .pipeline_controller import PipelineController

__all__ = [
    "QualityGate",
    "QualityResult",
    "SemanticRouter",
    "RouteResult",
    "NavigationExecutor",
    "NavigationResult",
    "ModelingExecutor",
    "ModelingResult",
    "PipelineController",
]


