# core/flow_engine/runtime.py
from typing import Optional, Dict, Any, List
from .flow_types import FlowInstance, FlowNode, FlowEdge, FlowContext
from task_engine.tts import tts_manager
from task_engine.tts.router_facade import get_tts_router_facade


class FlowRuntime:
    """负责任务链执行、暂停、恢复、插入任务等."""

    def __init__(self) -> None:
        self._instances: Dict[str, FlowInstance] = {}

    def start(self, instance: FlowInstance) -> None:
        self._instances[instance.context.task_id] = instance
        
        # P5-3: 自动播报任务链开始
        # Step 13: 使用统一入口
        task_title = instance.context.task_id.replace("_", " ")
        get_tts_router_facade().speak_task(
            f"开始执行任务：{task_title}",
            meta={"stage": "task_start", "task_id": instance.context.task_id},
        )
        
        self._run_current_node(instance)

    def resume(self, task_id: str) -> None:
        instance = self._instances.get(task_id)
        if not instance:
            return
        instance.paused = False
        self._run_current_node(instance)

    def pause(self, task_id: str) -> None:
        instance = self._instances.get(task_id)
        if not instance:
            return
        instance.paused = True

    def get_instance(self, task_id: str) -> Optional[FlowInstance]:
        return self._instances.get(task_id)

    def _run_current_node(self, instance: FlowInstance) -> None:
        while not instance.finished and not instance.paused:
            node = instance.definition.nodes[instance.current_node_id]
            
            # P5-3: 自动播报节点动作提示（若节点提供 voice_hint 或描述）
            voice_hint = None
            if hasattr(node, "voice_hint") and node.voice_hint:
                voice_hint = node.voice_hint
            elif hasattr(node, "description") and node.description:
                voice_hint = node.description
            elif node.params.get("voice_hint"):
                voice_hint = node.params.get("voice_hint")
            elif node.params.get("description"):
                voice_hint = node.params.get("description")
            
            if voice_hint:
                # Step 13: 使用统一入口
                get_tts_router_facade().speak_task(
                    voice_hint,
                    meta={"stage": "task_node", "node_id": node.id, "task_id": instance.context.task_id},
                )
            
            result = self._execute_node(node, instance.context)

            # 将结果写入 context
            instance.context.data[f"node_result_{node.id}"] = result

            # P5-3: 检查节点执行是否失败（通过 result 状态判断）
            if isinstance(result, dict):
                status = result.get("status")
                if status == "abort" or status == "failed":
                    # Step 13: 使用统一入口
                    get_tts_router_facade().speak_task(
                        "任务中断，已停止执行。",
                        meta={"stage": "task_abort", "task_id": instance.context.task_id},
                    )
                    instance.finished = True
                    break

            next_node_id = self._resolve_next_node(instance, node, result)
            if next_node_id is None:
                instance.finished = True
                # P5-3: 自动播报任务完成
                # Step 13: 使用统一入口
                task_title = instance.context.task_id.replace("_", " ")
                get_tts_router_facade().speak_task(
                    f"任务 {task_title} 已完成。",
                    meta={"stage": "task_done", "task_id": instance.context.task_id},
                )
                break
            instance.current_node_id = next_node_id

    def _execute_node(self, node: FlowNode, context: FlowContext) -> Any:
        if not node.executor:
            # 默认行为：什么都不做，返回 success
            return {"status": "success"}
        return node.executor(context, node.params)

    def _resolve_next_node(
        self,
        instance: FlowInstance,
        node: FlowNode,
        result: Any,
    ) -> Optional[str]:
        edges: List[FlowEdge] = [
            e for e in instance.definition.edges if e.source_id == node.id
        ]
        if not edges:
            return None

        # 支持 result 为 dict 且含 status
        status = None
        if isinstance(result, dict):
            status = result.get("status")

        # 先匹配条件等于 status 的边
        for e in edges:
            if e.condition is not None and e.condition == status:
                return e.target_id

        # 再找 condition 为 None 的默认边
        for e in edges:
            if e.condition is None:
                return e.target_id

        # 都没有则终止
        return None
