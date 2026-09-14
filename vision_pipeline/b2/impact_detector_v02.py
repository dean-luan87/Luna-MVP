"""
Impact Detector v0.2 - 相交判断

B2 v0.2: 冲突检测（唯一判断）

只返回：
- ttc (time to conflict)
- overlap_ratio
"""

from typing import Optional, List
from .b2_types_v02 import ImpactEvent
from .motion_corridor import MotionCorridor
from .dynamic_object import BoundingBox


def detect_overlap(
    corridor: MotionCorridor,
    future_bbox: BoundingBox,
    t_sec: float,
    obj_id: str,
    obj_confidence: float = 0.5,
) -> Optional[ImpactEvent]:
    """
    冲突检测（唯一判断）
    
    B2 v0.2: 只关心会不会进入 corridor，发生在几秒后
    
    Args:
        corridor: 未来行进 corridor
        future_bbox: 未来对象边界框
        t_sec: 未来时间（秒）
        obj_id: 对象 ID
        obj_confidence: 对象置信度
    
    Returns:
        ImpactEvent 或 None（如果不相交）
    """
    # 计算 bbox 中心
    bbox_center_x = (future_bbox.x1 + future_bbox.x2) / 2.0
    bbox_center_y = (future_bbox.y1 + future_bbox.y2) / 2.0
    
    # 简化：如果 corridor 是矩形，检查中心是否在矩形内
    if isinstance(corridor.polygon, list) and len(corridor.polygon) >= 3:
        # 使用简化的点-in-polygon 算法
        intersects = _point_in_polygon(bbox_center_x, bbox_center_y, corridor.polygon)
        
        if intersects:
            # 计算重叠比例（简化：基于 bbox 大小和 corridor 宽度）
            bbox_area = (future_bbox.x2 - future_bbox.x1) * (future_bbox.y2 - future_bbox.y1)
            corridor_area = corridor.width_m * corridor.horizon_sec * 1.0  # 简化
            overlap_ratio = min(bbox_area / max(corridor_area, 0.01), 1.0)
            
            return ImpactEvent(
                obj_id=obj_id,
                t_sec=t_sec,
                score=overlap_ratio,
                ttc=t_sec,  # time to conflict
                overlap_ratio=overlap_ratio,
                obj_confidence=obj_confidence,
                meta={}
            )
    
    # 如果 corridor 格式不对或不相交，返回 None
    return None


def _point_in_polygon(x: float, y: float, polygon: List[List[float]]) -> bool:
    """
    简化的点-in-polygon 判断（射线法）
    
    Args:
        x, y: 点坐标
        polygon: 多边形顶点列表
    
    Returns:
        bool: 点是否在多边形内
    """
    if len(polygon) < 3:
        return False
    
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

