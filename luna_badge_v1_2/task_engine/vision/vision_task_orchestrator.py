"""
VisionTaskOrchestrator: 视觉事件到任务执行的编排器

非侵入式 Orchestrator：
- 用 VisionSceneTaskBridge 得到任务建议
- 若没有活动任务，则自动 register_task 并启动
- 若已有活动任务，默认不抢占（策略保守）
"""

from typing import Optional

from task_engine.vision.vision_event import VisionEvent
from task_engine.vision.vision_scene_bridge import VisionSceneTaskBridge, VisionSceneTaskResult
from task_chain.task_chain_manager import TaskChainManager
from task_engine.task_execution_result import TaskExecutionResult


class VisionTaskOrchestrator:
    """
    非侵入式 Orchestrator：

    - 用 VisionSceneTaskBridge 得到任务建议
    - 若没有活动任务，则自动 register_task 并启动
    - 若已有活动任务，默认不抢占（策略保守）

    注意：本版本只返回任务建议，不直接创建 FlowInstance。
    上层需要根据 task_meta 通过 FlowPlanner 创建 FlowInstance 后再调用 register_task。
    """

    def __init__(
        self,
        bridge: VisionSceneTaskBridge,
        task_manager: TaskChainManager,
    ) -> None:
        """
        Args:
            bridge: VisionSceneTaskBridge 实例
            task_manager: TaskChainManager 实例
        """
        self._bridge = bridge
        self._task_manager = task_manager

    def handle_vision(self, event: VisionEvent) -> Optional[VisionSceneTaskResult]:
        """
        处理视觉事件，返回场景识别结果和任务建议。

        注意：本方法只返回建议，不直接注册任务。
        上层需要根据 suggested_task_meta 创建 FlowInstance 后再注册。

        Args:
            event: VisionEvent 实例

        Returns:
            Optional[VisionSceneTaskResult]: 如果当前有活动任务则不返回建议，否则返回结果
        """
        result = self._bridge.handle_vision_event(event)
        meta = result.suggested_task_meta

        # 无任务建议：仅更新场景
        if not meta:
            return result

        # 检查是否有活动任务（通过 lifecycle 状态判断）
        if self._task_manager.lifecycle.is_active:
            # 若任务正在执行，不抢占
            return None

        # 返回建议，由上层决定是否创建任务
        return result

    def suggest_task_from_vision(self, event: VisionEvent) -> Optional[dict]:
        """
        简化接口：只返回任务建议的 task_meta，不返回完整结果。

        Args:
            event: VisionEvent 实例

        Returns:
            Optional[dict]: 推荐的任务元数据，如果没有建议或当前有活动任务则返回 None
        """
        result = self.handle_vision(event)
        if result and result.suggested_task_meta:
            return result.suggested_task_meta
        return None

