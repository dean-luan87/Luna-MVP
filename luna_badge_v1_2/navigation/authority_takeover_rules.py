"""
Authority Takeover Rules (v1.4.8 Step 6)

接管阈值与策略表

关键设计原则（必须遵守）：
- 时间 > 分数
- 连续稳定 > 单次高分
- 接管慢，回退更慢
- 室内优先级永远最高
"""

from typing import Dict, Any, List, Optional


# 不同 authority 的接管阈值
TAKEOVER_RULES: Dict[str, Dict[str, Any]] = {
    "VISUAL": {
        "min_score": 0.70,          # 最小分数阈值
        "min_gap": 0.20,            # 最小置信度差距
        "lock_s": 1.5,              # 锁定观察窗口（秒）- 防抖
        "cooldown_s": 3.0,          # 冷却期（秒）- 防止频繁切换
        "scene_required": ["INDOOR", "TRANSITION"],  # 允许接管的场景
        "min_distance_m": None,     # 最小距离要求（None 表示无要求）
    },
    "MAP_VISION": {
        "min_score": 0.80,
        "min_gap": 0.25,
        "lock_s": 2.0,              # 地标匹配允许稍快锁定
        "cooldown_s": 4.0,
        "scene_required": ["OUTDOOR"],
        "min_distance_m": None,
    },
    "GPS": {
        "min_score": 0.75,
        "min_gap": 0.30,            # GPS 需要更大的差距
        "lock_s": 3.0,              # GPS 接管最慢
        "cooldown_s": 6.0,          # GPS 冷却期最长
        "scene_required": ["OUTDOOR"],  # 只允许室外
        "min_distance_m": 50,       # GPS 接管需要最小距离 50m
    }
}


def get_takeover_rule(authority: str) -> Dict[str, Any]:
    """
    获取接管规则
    
    Args:
        authority: 目标主权（"VISUAL" / "MAP_VISION" / "GPS"）
        
    Returns:
        接管规则字典
    """
    return TAKEOVER_RULES.get(authority, {})


def is_scene_allowed(authority: str, scene: str) -> bool:
    """
    检查场景是否允许接管
    
    Args:
        authority: 目标主权
        scene: 当前场景（"INDOOR" / "OUTDOOR" / "TRANSITION"）
        
    Returns:
        是否允许接管
    """
    rule = get_takeover_rule(authority)
    scene_required = rule.get("scene_required", [])
    return scene in scene_required if scene_required else False


def check_distance_requirement(authority: str, distance_m: Optional[float]) -> bool:
    """
    检查距离要求
    
    Args:
        authority: 目标主权
        distance_m: 当前距离（米）
        
    Returns:
        是否满足距离要求
    """
    rule = get_takeover_rule(authority)
    min_distance_m = rule.get("min_distance_m")
    
    if min_distance_m is None:
        return True  # 无距离要求
    
    if distance_m is None:
        return False  # 需要距离但未提供
    
    return distance_m >= min_distance_m


def check_score_requirements(
    authority: str,
    snapshot_score: float,
    snapshot_gap: float
) -> bool:
    """
    检查分数要求
    
    Args:
        authority: 目标主权
        snapshot_score: 快照分数
        snapshot_gap: 快照置信度差距
        
    Returns:
        是否满足分数要求
    """
    rule = get_takeover_rule(authority)
    min_score = rule.get("min_score", 0.0)
    min_gap = rule.get("min_gap", 0.0)
    
    return snapshot_score >= min_score and snapshot_gap >= min_gap






