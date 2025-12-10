# core/model_scheduler/registry.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Callable, Any


class ModelType(str, Enum):
    VISION_DETECT = "vision_detect"
    OCR = "ocr"
    NAVIGATION = "navigation"
    RISK_ASSESS = "risk_assess"
    FUSION = "fusion"  # 多模态融合/后处理


@dataclass
class CapabilityDescriptor:
    """描述模型的能力，用于 Context-Aware 选择."""
    can_detect_people: bool = False
    can_detect_road_edge: bool = False
    can_detect_obstacle: bool = False
    can_ocr_text: bool = False
    can_work_low_light: bool = False
    can_estimate_traversable_area: bool = False
    latency_level: int = 2  # 1=最快, 3=最慢
    accuracy_level: int = 2  # 1=粗略, 3=高精度


@dataclass
class ModelDescriptor:
    id: str
    model_type: ModelType
    provider: str  # "local", "remote", "onnx", "openvino" 等
    version: str
    capabilities: CapabilityDescriptor
    input_spec: Dict[str, Any] = field(default_factory=dict)
    output_spec: Dict[str, Any] = field(default_factory=dict)
    # 实际调用函数的引用由上层注入
    runner: Optional[Callable[..., Any]] = None


class ModelRegistry:
    """集中维护所有可用模型的注册信息."""

    def __init__(self) -> None:
        self._models: Dict[str, ModelDescriptor] = {}

    def register_model(self, descriptor: ModelDescriptor) -> None:
        self._models[descriptor.id] = descriptor

    def get_model(self, model_id: str) -> Optional[ModelDescriptor]:
        return self._models.get(model_id)

    def list_models(self, model_type: Optional[ModelType] = None) -> List[ModelDescriptor]:
        if model_type is None:
            return list(self._models.values())
        return [m for m in self._models.values() if m.model_type == model_type]
