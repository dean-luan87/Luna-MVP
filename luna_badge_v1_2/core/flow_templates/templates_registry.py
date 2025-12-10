# core/flow_templates/templates_registry.py
from typing import List, Optional
from .base_templates import BaseFlowTemplate


class FlowTemplateRegistry:
    """统一管理所有模板."""

    def __init__(self) -> None:
        self._templates: List[BaseFlowTemplate] = []

    def register_template(self, template: BaseFlowTemplate) -> None:
        self._templates.append(template)

    def select_template(self, intent: str, scene_type: str) -> Optional[BaseFlowTemplate]:
        # 极简选择逻辑：第一个匹配的模板
        for t in self._templates:
            if intent in t.supported_intents and scene_type in t.supported_scenes:
                return t
        return None
