"""
Vision 模块
包含视觉处理、模型、流水线等功能
"""
# 导出主要接口
try:
    from .models.yolo import YoloDetector, DetectionResult
    from .model_registry import ModelRegistry
except ImportError:
    # 如果新路径不可用，尝试从旧路径导入
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.yolo_detector import YoloDetector, DetectionResult
    from core.model_registry import ModelRegistry

__all__ = [
    "YoloDetector",
    "DetectionResult",
    "ModelRegistry",
]
















