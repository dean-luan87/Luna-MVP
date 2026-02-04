# core/flow_templates/base_templates.py
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from ..flow_engine.flow_types import FlowDefinition
from ..flow_engine.planner import PlanningInput


class BaseFlowTemplate(ABC):
    """
    所有任务链模板的抽象基类.
    
    模板负责定义流程骨架和 Hook 点，不负责扩展逻辑。
    扩展由 TaskPiece 通过 CompositionEngine 完成。
    """
    id: str
    supported_intents: List[str]
    supported_scenes: List[str]
    
    # Hook 点定义：{hook_point: node_id}
    # 例如：{"before_navigate": "navigate", "after_navigate": "navigate"}
    hook_points: Dict[str, str] = {}

    @abstractmethod
    def instantiate(self, planning_input: PlanningInput) -> FlowDefinition:
        """
        实例化模板，生成流程骨架
        
        注意：此方法只生成骨架，不包含积木扩展。
        积木扩展由 CompositionEngine 在后续步骤完成。
        """
        raise NotImplementedError
    
    def get_hook_points(self) -> Dict[str, str]:
        """获取所有 Hook 点定义"""
        return self.hook_points.copy()
    
    def get_hook_node_id(self, hook_point: str) -> Optional[str]:
        """获取指定 Hook 点对应的节点 ID"""
        return self.hook_points.get(hook_point)
