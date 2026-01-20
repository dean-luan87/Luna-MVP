"""
B2 Corridor - 任务走廊构建（无任务链也能跑）
"""

from typing import Dict, Any
from .b2_types import TaskCorridor
from .b2_config import B2_HORIZON_SEC_DEFAULT


def build_task_corridor(observe_input: Dict[str, Any]) -> TaskCorridor:
    """
    构建任务走廊
    
    Args:
        observe_input: 观察输入，包含：
            - task_corridor: 任务走廊几何（可选）
            - horizon_sec: 时间窗口（可选）
            - ego_motion: 自运动信息（可选，包含 heading）
    
    Returns:
        TaskCorridor: 任务走廊
    """
    # 如果有明确的任务走廊，使用 route
    if observe_input.get("task_corridor"):
        return TaskCorridor(
            corridor_id="route_based",
            source="route",
            horizon_sec=observe_input.get("horizon_sec", B2_HORIZON_SEC_DEFAULT),
            confidence=0.9,
            geometry=observe_input["task_corridor"],
        )
    
    # 否则使用方向猜测
    ego_motion = observe_input.get("ego_motion", {})
    heading = ego_motion.get("heading", 0)
    
    return TaskCorridor(
        corridor_id="heading_guess",
        source="heading_guess",
        horizon_sec=observe_input.get("horizon_sec", B2_HORIZON_SEC_DEFAULT),
        confidence=0.6,
        geometry={"heading": heading, "cone_deg": 30},
    )

