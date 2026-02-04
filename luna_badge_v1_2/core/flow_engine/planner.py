# core/flow_engine/planner.py
import uuid
from typing import Optional, TYPE_CHECKING, Dict, Any
from .flow_types import FlowDefinition, FlowContext, FlowInstance, PlanningInput

if TYPE_CHECKING:
    from ..flow_templates.templates_registry import FlowTemplateRegistry
    from ..composition.composition_engine import CompositionEngine


class FlowPlanner:
    """
    根据 Intent + Scene，从模板库拼装任务链.
    
    在 v1.4.5a 中，支持可选注入 CompositionEngine（软接入）：
    - 如果不注入 composition_engine，行为与 v1.4.5 完全一致（零风险）
    - 如果注入，则在模板生成骨架后应用积木组合
    """

    def __init__(
        self,
        template_registry: "FlowTemplateRegistry",
        composition_engine: Optional["CompositionEngine"] = None,
    ) -> None:
        self._template_registry = template_registry
        self._composition_engine = composition_engine

    def plan(
        self,
        planning_input: PlanningInput,
        env: Optional[Dict[str, Any]] = None,
    ) -> Optional[FlowInstance]:
        """
        规划流程实例
        
        Args:
            planning_input: 规划输入
            env: 环境变量（用于积木条件判断，仅在启用 CompositionEngine 时使用）
        
        Returns:
            FlowInstance 或 None（如果找不到模板）
        """
        # 延迟导入避免循环依赖
        from ..flow_templates.templates_registry import FlowTemplateRegistry
        template = self._template_registry.select_template(
            intent=planning_input.intent,
            scene_type=planning_input.scene_type,
        )
        if not template:
            return None

        # 1. 从模板生成骨架（原有流程，保持不变）
        flow_def: FlowDefinition = template.instantiate(planning_input)

        # 2. 创建上下文
        ctx = FlowContext(
            task_id=self._generate_task_id(planning_input),
            user_id=planning_input.user_id,
            scene_type=planning_input.scene_type,
            intent=planning_input.intent,
            data={
                "raw_utterance": planning_input.raw_utterance,
                **(planning_input.extra or {}),
            },
        )

        # 3. 软接入：如果配置了 CompositionEngine，应用积木组合
        # 注意：composition_engine 目前是 no-op，不会对现有任务链造成任何影响
        if self._composition_engine:
            flow_def = self._composition_engine.compose(
                flow_def=flow_def,
                context=ctx,
                env=env or {},
            )

        # 4. 创建 FlowInstance
        instance = FlowInstance(
            definition=flow_def,
            context=ctx,
            current_node_id=flow_def.entry_node_id,
        )
        return instance

    def _generate_task_id(self, planning_input: PlanningInput) -> str:
        return f"{planning_input.user_id}-{planning_input.intent}-{uuid.uuid4().hex[:8]}"
