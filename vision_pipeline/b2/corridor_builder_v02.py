"""
Corridor Builder v0.2 - 路径构造

B2 v0.2: 构建未来行进 corridor

逻辑顺序：
1. 有 task_chain → 用 task_chain
2. 无 task_chain → ego heading + speed（直线 corridor）
"""

import math
from typing import Optional, Any
from .motion_corridor import MotionCorridor
from .task_corridor_v02 import TaskCorridor
from .world_snapshot import WorldSnapshot, EgoPose


def build_corridor(
    navigation_result: Optional[Any],
    ego_pose: EgoPose,
    horizon_sec: float = 5.0,
    corridor_width_m: float = 1.2,
) -> MotionCorridor:
    """
    构建未来行进 corridor
    
    B2 v0.2: 优先级顺序
    
    Args:
        navigation_result: 导航结果（可选）
        ego_pose: 自位姿
        horizon_sec: 时间窗口（秒）
        corridor_width_m: 走廊宽度（米）
    
    Returns:
        MotionCorridor: 未来行进 corridor
    """
    # 优先级 1: 有 task_chain → 用 task_chain
    if navigation_result and hasattr(navigation_result, 'route'):
        route = navigation_result.route
        if route and hasattr(route, 'points') and route.points:
            # 使用导航路径构建 polygon
            polygon = route.points  # 简化：直接使用 points
            return MotionCorridor(
                polygon=polygon,
                horizon_sec=horizon_sec,
                source="NAV",
                width_m=corridor_width_m,
                meta={
                    "route_id": getattr(route, 'route_id', None),
                }
            )
    
    # 优先级 2: 无 task_chain → ego heading + speed（直线 corridor）
    heading = ego_pose.heading
    speed = ego_pose.speed or 1.0  # 默认 1.0 m/s
    heading_rad = math.radians(heading)
    
    # 计算未来路径长度
    path_length = speed * horizon_sec
    
    # 构建简单的矩形 corridor（从当前位置向前延伸）
    half_width = corridor_width_m / 2.0
    
    # 简化：构建 4 个点的矩形
    if ego_pose.pos and len(ego_pose.pos) >= 2:
        start_x, start_y = ego_pose.pos[0], ego_pose.pos[1]
    else:
        start_x, start_y = 0.0, 0.0
    
    # 计算方向向量
    dx = math.cos(heading_rad)
    dy = math.sin(heading_rad)
    
    # 计算垂直向量（用于宽度）
    perp_dx = -dy
    perp_dy = dx
    
    # 构建矩形 polygon（4 个点）
    polygon = [
        [start_x + perp_dx * half_width, start_y + perp_dy * half_width],
        [start_x + dx * path_length + perp_dx * half_width, start_y + dy * path_length + perp_dy * half_width],
        [start_x + dx * path_length - perp_dx * half_width, start_y + dy * path_length - perp_dy * half_width],
        [start_x - perp_dx * half_width, start_y - perp_dy * half_width],
    ]
    
    return MotionCorridor(
        polygon=polygon,
        horizon_sec=horizon_sec,
        source="EGO",
        width_m=corridor_width_m,
        meta={
            "heading": heading,
            "speed": speed,
            "path_length": path_length,
        }
    )

