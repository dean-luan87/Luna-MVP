# -*- coding: utf-8 -*-
"""
v1.8.4: 几何计算工具

职责：
- 计算点到几何体的距离（POINT/LINE/AREA）
- 判断点是否在多边形内部
- 计算折线长度

这是风险系统"只看空间关系"的根基。
"""

import math
from typing import List, Tuple, Optional
from core.risk.risk_object import RiskGeometry


def distance_point_to_point(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """计算两点之间的欧式距离"""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def distance_point_to_line_segment(
    point: Tuple[float, float],
    line_start: Tuple[float, float],
    line_end: Tuple[float, float]
) -> float:
    """
    计算点到线段的最短距离
    
    Args:
        point: 点坐标 (x, y)
        line_start: 线段起点 (x, y)
        line_end: 线段终点 (x, y)
    
    Returns:
        float: 最短距离
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # 线段长度的平方
    dx = x2 - x1
    dy = y2 - y1
    line_len_sq = dx * dx + dy * dy
    
    if line_len_sq == 0:
        # 线段退化为点
        return distance_point_to_point(point, line_start)
    
    # 计算投影参数 t
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / line_len_sq))
    
    # 投影点
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    
    # 返回点到投影点的距离
    return distance_point_to_point(point, (proj_x, proj_y))


def distance_point_to_polyline(
    point: Tuple[float, float],
    polyline: List[Tuple[float, float]]
) -> float:
    """
    计算点到折线的最短距离
    
    Args:
        point: 点坐标 (x, y)
        polyline: 折线点列表 [(x, y), ...]
    
    Returns:
        float: 最短距离
    """
    if not polyline:
        return float('inf')
    
    if len(polyline) == 1:
        return distance_point_to_point(point, polyline[0])
    
    min_dist = float('inf')
    for i in range(len(polyline) - 1):
        dist = distance_point_to_line_segment(point, polyline[i], polyline[i + 1])
        min_dist = min(min_dist, dist)
    
    return min_dist


def point_in_polygon(
    point: Tuple[float, float],
    polygon: List[Tuple[float, float]]
) -> bool:
    """
    判断点是否在多边形内部（射线法）
    
    Args:
        point: 点坐标 (x, y)
        polygon: 多边形顶点列表 [(x, y), ...]（按顺序）
    
    Returns:
        bool: 是否在多边形内部
    """
    if len(polygon) < 3:
        return False
    
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def distance_point_to_polygon_boundary(
    point: Tuple[float, float],
    polygon: List[Tuple[float, float]]
) -> float:
    """
    计算点到多边形边界的最短距离
    
    如果点在多边形内部，返回到边界的距离（便于"别太靠近边界"）
    如果点在多边形外部，返回到边界的最短距离
    
    Args:
        point: 点坐标 (x, y)
        polygon: 多边形顶点列表 [(x, y), ...]（按顺序）
    
    Returns:
        float: 到边界的最短距离
    """
    # 先判断是否在内部
    if point_in_polygon(point, polygon):
        # 在内部：计算到各条边的最短距离
        return distance_point_to_polyline(point, polygon)
    else:
        # 在外部：计算到折线的最短距离
        return distance_point_to_polyline(point, polygon)


def distance_to_geometry(
    user_xy: Tuple[float, float],
    geometry: RiskGeometry
) -> float:
    """
    计算用户位置到危险几何体的距离
    
    Args:
        user_xy: 用户位置 (x, y)
        geometry: 危险几何体
    
    Returns:
        float: 距离（米）
    """
    if not geometry.points:
        return float('inf')
    
    if geometry.type == "POINT":
        # POINT：欧式距离
        return distance_point_to_point(user_xy, geometry.points[0])
    
    elif geometry.type == "LINE":
        # LINE：点到折线最短距离
        return distance_point_to_polyline(user_xy, geometry.points)
    
    elif geometry.type == "AREA":
        # AREA：点到多边形边界距离
        return distance_point_to_polygon_boundary(user_xy, geometry.points)
    
    else:
        return float('inf')


def is_inside_area(
    user_xy: Tuple[float, float],
    polygon: List[Tuple[float, float]]
) -> bool:
    """
    判断点是否在多边形内部
    
    Args:
        user_xy: 用户位置 (x, y)
        polygon: 多边形顶点列表 [(x, y), ...]
    
    Returns:
        bool: 是否在多边形内部
    """
    return point_in_polygon(user_xy, polygon)


def polyline_length(points: List[Tuple[float, float]]) -> float:
    """
    计算折线长度（若传入未带 length_m）
    
    Args:
        points: 折线点列表 [(x, y), ...]
    
    Returns:
        float: 折线长度（米）
    """
    if len(points) < 2:
        return 0.0
    
    total_length = 0.0
    for i in range(len(points) - 1):
        total_length += distance_point_to_point(points[i], points[i + 1])
    
    return total_length


