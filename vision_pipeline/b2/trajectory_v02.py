"""
Trajectory v0.2 - 简单外推

B2 v0.2: 轨迹外推（极简）

⚠️ v0.2 禁止加速度、转向建模
"""

from typing import List, Optional
from .dynamic_object import BoundingBox, Vector2D
from .world_snapshot import WorldObject


def extract_dynamic_objects(
    modeling_result: Optional[Any],
    min_confidence: float = 0.3,
) -> List[WorldObject]:
    """
    动态对象抽取（真实信号）
    
    B2 v0.2: 从 modeling_result 中提取动态对象
    
    规则：
    - 有 velocity → 用
    - 没 velocity → 默认 0
    - confidence < 阈值 → 忽略
    
    Args:
        modeling_result: 建模结果（可选）
        min_confidence: 最小置信度阈值
    
    Returns:
        List[WorldObject]: 动态对象列表
    """
    objects = []
    
    if not modeling_result:
        return objects
    
    # 从 modeling_result 中提取对象
    if hasattr(modeling_result, 'objects'):
        for obj in modeling_result.objects:
            # 检查置信度
            confidence = getattr(obj, 'confidence', 0.5)
            if confidence < min_confidence:
                continue
            
            # 检查是否有 velocity
            if not hasattr(obj, 'vel') or not obj.vel:
                # 没 velocity → 默认 0
                obj.vel = [0.0, 0.0]
            
            objects.append(obj)
    
    return objects


def extrapolate_bbox(
    bbox: BoundingBox,
    velocity: Vector2D,
    dt: float,
) -> BoundingBox:
    """
    轨迹外推（极简）
    
    B2 v0.2: 不考虑加速度、转向建模
    
    Args:
        bbox: 当前边界框
        velocity: 速度向量
        dt: 时间步长（秒）
    
    Returns:
        BoundingBox: 未来位置的边界框
    """
    # 计算位移
    dx = velocity.x * dt
    dy = velocity.y * dt
    
    # 平移 bbox
    return bbox.translate(dx, dy)

