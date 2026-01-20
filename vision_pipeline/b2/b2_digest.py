"""
B2 Digest - 粗粒度世界摘要（抗噪）

v0.1：粗粒度摘要，避免抖动导致持续变化
"""

from typing import Tuple, Optional, Dict, Any


def compute_world_digest(world_update: Dict[str, Any]) -> Tuple[int, int, int, int]:
    """
    计算世界摘要（粗粒度，避免抖动导致持续变化）
    
    world_update 可由上游封装（无需 B2 关心细节）
    
    Args:
        world_update: 世界更新字典，包含：
            - density: 密度（0~100）
            - motion_level: 运动强度（0~100）
            - illumination: 亮度（0~100）
            - dominant_direction: 主方向（0~7，8方向）
    
    Returns:
        tuple: (density_bucket, motion_bucket, illum_bucket, dom_dir)
    """
    density = int(world_update.get("density", 0) / 10)  # 0-9 桶
    motion = int(world_update.get("motion_level", 0) / 10)  # 0-9 桶
    illum = int(world_update.get("illumination", 0) / 10)  # 0-9 桶
    dom_dir = int(world_update.get("dominant_direction", 0)) % 8  # 0-7，8方向
    
    return (density, motion, illum, dom_dir)


def digest_delta(a: Optional[Tuple], b: Optional[Tuple]) -> float:
    """
    计算摘要变化量
    
    Args:
        a: 当前摘要
        b: 上次摘要
    
    Returns:
        float: 变化量（0~1），1.0 表示完全不同
    """
    if a is None or b is None:
        return 1.0
    
    diffs = sum(1 for x, y in zip(a, b) if x != y)
    return diffs / max(1, len(a))

