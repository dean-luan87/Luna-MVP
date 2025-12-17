"""
Scene Classifier (C-2.2)

场景分类器

它解决的是：
"在这个身体里，我现在处于哪种'表达语境'？"

一期规则：
- indoor → INDOOR
- distance ≤ 50m → NAVIGATION_SHORT
- distance > 50m → NAVIGATION_LONG
"""

from typing import Optional, Dict, Any
from .scene_types import SceneType
from .scene_context import SceneContext


class SceneClassifier:
    """
    场景分类器
    
    职责：
    - 根据导航上下文分类场景
    - 一期：规则驱动
    - 二期：模型 + 记忆
    """
    
    def __init__(self, distance_threshold_m: float = 50.0):
        """
        初始化场景分类器
        
        Args:
            distance_threshold_m: 距离阈值（米，默认 50.0）
        """
        self.distance_threshold_m = distance_threshold_m
    
    def classify(self, nav_context: Dict[str, Any]) -> SceneContext:
        """
        分类场景
        
        一期规则：
        - indoor → INDOOR
        - distance ≤ 50m → NAVIGATION_SHORT
        - distance > 50m → NAVIGATION_LONG
        
        Args:
            nav_context: 导航上下文（包含 scene, distance_m 等）
            
        Returns:
            SceneContext: 场景上下文
        """
        scene_str = nav_context.get("scene", "outdoor")
        distance_m = nav_context.get("distance_m")
        is_safe_mode = nav_context.get("safe_mode", False)
        
        # 安全模式优先
        if is_safe_mode:
            return SceneContext(
                scene=SceneType.SAFE_MODE,
                confidence=0.9,
                source="system"
            )
        
        # 室内场景
        if scene_str == "indoor":
            return SceneContext(
                scene=SceneType.INDOOR,
                confidence=0.85,
                source="vision"
            )
        
        # 室外场景：根据距离分类
        if distance_m is not None:
            if distance_m <= self.distance_threshold_m:
                return SceneContext(
                    scene=SceneType.NAVIGATION_SHORT,
                    confidence=0.8,
                    source="fsm"
                )
            else:
                return SceneContext(
                    scene=SceneType.NAVIGATION_LONG,
                    confidence=0.8,
                    source="fsm"
                )
        
        # 默认：室外
        return SceneContext(
            scene=SceneType.OUTDOOR,
            confidence=0.6,
            source="system"
        )
