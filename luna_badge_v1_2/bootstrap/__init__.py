"""
Bootstrap: 统一构建和初始化模块

提供各种 pipeline 的快速初始化入口。
"""

from .vision_pipeline import (
    VisionPipeline,
    create_vision_pipeline,
    DefaultSceneClassifier,
)

__all__ = [
    "VisionPipeline",
    "create_vision_pipeline",
    "DefaultSceneClassifier",
]












