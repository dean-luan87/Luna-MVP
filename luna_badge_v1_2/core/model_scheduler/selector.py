# core/model_scheduler/selector.py
from dataclasses import dataclass
from typing import Optional, List
from .registry import ModelRegistry, ModelDescriptor, ModelType


@dataclass
class ModelSelectionContext:
    """模型选择时的上下文信息."""
    scene_type: str  # "outdoor", "hospital", "metro", ...
    task_node_type: str  # "detect_obstacle", "ocr_sign", ...
    low_light: bool = False
    need_high_accuracy: bool = False
    real_time_required: bool = True


class ContextAwareModelSelector:
    """根据任务链节点 + 场景上下文，选择合适模型."""

    def __init__(self, registry: ModelRegistry) -> None:
        self._registry = registry

    def select_best_model(
        self,
        model_type: ModelType,
        context: ModelSelectionContext
    ) -> Optional[ModelDescriptor]:
        candidates: List[ModelDescriptor] = self._registry.list_models(model_type)
        if not candidates:
            return None

        scored: List[tuple[ModelDescriptor, float]] = []
        for m in candidates:
            score = 0.0
            caps = m.capabilities

            # 极简打分策略：后续可以替换为复杂权重
            if context.low_light and caps.can_work_low_light:
                score += 2.0
            if context.need_high_accuracy:
                score += caps.accuracy_level
            else:
                score += 1.0  # 默认给一点基础分

            if context.real_time_required:
                # 延迟越低越好
                score -= (caps.latency_level - 1) * 0.5

            # 轻量规则：根据场景 & node type 调整
            if context.task_node_type == "ocr_sign" and caps.can_ocr_text:
                score += 1.5
            if context.task_node_type == "detect_obstacle" and caps.can_detect_obstacle:
                score += 1.5

            scored.append((m, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        best_model, best_score = scored[0]
        if best_score <= 0:
            return None
        return best_model
