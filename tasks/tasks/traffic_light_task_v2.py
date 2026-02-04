"""
TrafficLightTask v2: 使用 BaseTask，支持 WAITING/BLOCKED/TIMEOUT。
直接读取 world_entities，不依赖 snapshot。
"""
from typing import Dict, Optional

from tasks.base_v2 import BaseTask
from tasks.types import TaskStatus
from common.change_demand import ChangeDemand
from dynamic_view.entity import ObservedEntity
from dynamic_view.types import ObservationState


class TrafficLightTask(BaseTask):
    """TrafficLightTask v2：支持等待红灯、遮挡、超时。"""

    task_name = "TrafficLightTask"

    def __init__(self, *, max_wait_time: float = 30.0):
        super().__init__(max_wait_time=max_wait_time)

    def tick(self, world_entities: Dict[str, ObservedEntity], now: float, attr_map: Optional[Dict[str, Dict]] = None):
        """
        状态机：
        - INIT → ACTIVE（找到红绿灯）
        - ACTIVE/WAITING → WAITING（红灯）
        - ACTIVE/WAITING → BLOCKED（INVISIBLE/UNSTABLE）
        - WAITING/BLOCKED → COMPLETED（绿灯）
        - WAITING/BLOCKED → TIMEOUT（超时）
        """
        # 找到任意红绿灯实体
        lights = [
            e for e in world_entities.values()
            if "traffic_light" in e.entity_id
        ]

        # INIT → ACTIVE
        if self.state == TaskStatus.PENDING:
            if lights:
                self._start(now)
                # 启动后立即检查颜色和状态，如果是红灯且稳定直接进入 WAITING
                light = lights[0]
                if light.state == ObservationState.STABLE:
                    color = "unknown"
                    if attr_map:
                        attrs = attr_map.get(light.entity_id, {})
                        color = attrs.get("color", "unknown")
                    if color == "red":
                        self.state = TaskStatus.WAITING
                        self.last_reason = "WAIT_RED"
                        return
                # 如果启动时不稳定，保持 ACTIVE，等待下一个 tick 检查
                return

        # 如果任务已完成或超时，不再处理
        if self.state in (TaskStatus.COMPLETED, TaskStatus.TIMEOUT):
            return

        # ACTIVE/WAITING/BLOCKED 状态处理
        if self.state in (TaskStatus.ACTIVE, TaskStatus.WAITING, TaskStatus.BLOCKED):
            # 检查超时
            if self._timeout(now):
                return

            # 没有红绿灯 → BLOCKED
            if not lights:
                self.state = TaskStatus.BLOCKED
                self.last_reason = "LIGHT_INVISIBLE"
                return

            light = lights[0]

            # 红绿灯不稳定 → BLOCKED
            if light.state != ObservationState.STABLE:
                self.state = TaskStatus.BLOCKED
                self.last_reason = "LIGHT_UNSTABLE"
                return

            # 从 attr_map 获取颜色
            color = "unknown"
            if attr_map:
                attrs = attr_map.get(light.entity_id, {})
                color = attrs.get("color", "unknown")

            # 红灯 → WAITING
            if color == "red":
                self.state = TaskStatus.WAITING
                self.last_reason = "WAIT_RED"
                return

            # 绿灯 → COMPLETED
            if color == "green":
                self.state = TaskStatus.COMPLETED
                self.last_reason = "GO_GREEN"
                return

            # 颜色未知 → BLOCKED
            if color == "unknown":
                self.state = TaskStatus.BLOCKED
                self.last_reason = "LIGHT_COLOR_UNKNOWN"
                return

    def change_demands(self):
        """
        只读地产生 ChangeDemand，不影响任何任务逻辑。
        """
        if self.state == TaskStatus.WAITING and self.last_reason == "WAIT_RED":
            return [
                ChangeDemand(
                    demand_type="signal_state_change",
                    priority=10,
                    constraints={"object_type": "traffic_light"},
                    source="task",
                )
            ]
        return []
