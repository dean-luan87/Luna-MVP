"""
B2 Task Corridor Builder - 任务走廊构建器

职责：
- 构建 B2 的"预演舞台"
- 有导航任务 → 用 route
- 无导航任务 → 用 heading + speed
"""

from typing import Optional, Dict, Any
from .b2_types import TaskCorridor
from .b2_config import B2_HORIZON_SEC_DEFAULT


class TaskCorridorBuilder:
    """
    B2 任务走廊构建器
    
    核心职责：
    - 从导航结果或自运动信息构建任务走廊
    - 为未来预演提供"预演舞台"
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化任务走廊构建器
        
        Args:
            config: 配置字典
        """
        self.config = config or {}
    
    def build(
        self,
        ego_pose: Dict[str, Any],
        navigation_route: Optional[Any] = None,
    ) -> TaskCorridor:
        """
        构建任务走廊
        
        Args:
            ego_pose: 自位姿信息，包含：
                - heading: 朝向（度，0~360）
                - position: 位置（可选）
                - velocity: 速度（可选）
            navigation_route: 导航路径（可选）
        
        Returns:
            TaskCorridor: 任务走廊
        """
        # 如果有导航任务，使用 route
        if navigation_route:
            return self._build_from_route(navigation_route)
        
        # 否则使用 heading + speed
        return self._build_from_heading(ego_pose)
    
    def _build_from_route(self, route: Any) -> TaskCorridor:
        """
        从导航路径构建任务走廊
        
        Args:
            route: 导航路径对象
        
        Returns:
            TaskCorridor: 任务走廊
        """
        # 简化：假设 route 有 polyline 属性
        if hasattr(route, "polyline"):
            geometry = {"polyline": route.polyline}
        elif isinstance(route, (list, tuple)):
            geometry = {"polyline": route}
        else:
            geometry = {"route": route}
        
        return TaskCorridor(
            corridor_id="route_based",
            source="route",
            horizon_sec=B2_HORIZON_SEC_DEFAULT,
            confidence=0.9,
            geometry=geometry,
        )
    
    def _build_from_heading(self, ego_pose: Dict[str, Any]) -> TaskCorridor:
        """
        从朝向构建任务走廊（无导航任务时）
        
        Args:
            ego_pose: 自位姿信息
        
        Returns:
            TaskCorridor: 任务走廊
        """
        heading = ego_pose.get("heading", 0)
        velocity = ego_pose.get("velocity", 1.0)  # 默认 1.0 m/s
        
        # 构建基于朝向的走廊（扇形）
        geometry = {
            "heading": heading,
            "cone_deg": 30,  # 30 度扇形
            "velocity": velocity,
        }
        
        return TaskCorridor(
            corridor_id="heading_guess",
            source="heading_guess",
            horizon_sec=B2_HORIZON_SEC_DEFAULT,
            confidence=0.6,
            geometry=geometry,
        )

